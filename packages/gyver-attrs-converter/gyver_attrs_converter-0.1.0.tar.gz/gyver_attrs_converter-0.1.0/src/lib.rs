use pyo3::{
    exceptions::{PyAttributeError, PyKeyError},
    impl_::pyclass::PyMethods,
    prelude::pymodule,
    pyfunction,
    types::{PyDict, PyFunction, PyList, PyModule, PySequence, PySet, PyString, PyTuple, PyType},
    wrap_pyfunction, IntoPy, Py, PyAny, PyObject, PyResult, Python,
};

#[pyfunction]
#[pyo3(signature = (obj, by_alias = true))]
fn make_mapping(py: Python, obj: PyObject, by_alias: Option<bool>) -> PyResult<Py<PyDict>> {
    let gyver_attrs = match obj.getattr(py, "__gyver_attrs__") {
        Ok(x) => x.extract::<Py<PyDict>>(py)?,
        Err(err) => return Err(err),
    };
    let should_alias = by_alias.unwrap_or(false);
    let result = PyDict::new(py);

    Python::with_gil(|py| {
        for (key, field) in gyver_attrs.into_ref(py) {
            let field_key = if should_alias {
                field.getattr("alias").unwrap().extract::<&PyString>()
            } else {
                key.extract::<&PyString>()
            }
            .unwrap();
            match obj.getattr(py, key.extract::<&PyString>().unwrap()) {
                Ok(value) => result.set_item(field_key, value).unwrap(),
                _ => (),
            };
        }
    });
    Ok(result.into())
}

fn deserialize(py: Python, value: &PyAny) -> PyResult<PyObject> {
    if let Ok(parser) = value.getattr("__parse_dict__") {
        let result = parser.call0()?;
        Ok(result.into())
    } else if let Ok(sequence) = value.extract::<&PySequence>() {
        let result: &PyAny = if sequence.is_instance_of::<PyList>()? {
            let items = sequence
                .iter()?
                .map(|item| deserialize(py, item.unwrap()))
                .collect::<PyResult<Vec<_>>>()?;
            PyList::new(py, items)
        } else if sequence.is_instance_of::<PyTuple>()? {
            let items = sequence
                .iter()?
                .map(|item| deserialize(py, item.unwrap()))
                .collect::<PyResult<Vec<_>>>()?;
            PyTuple::new(py, items)
        } else if sequence.is_instance_of::<PySet>()? {
            let items = sequence
                .iter()?
                .map(|item| deserialize(py, item?))
                .collect::<PyResult<Vec<_>>>()?;
            PySet::new(py, items.as_slice()).unwrap()
        } else {
            sequence
        };
        Ok(result.into())
    } else if let Ok(mapping) = value.extract::<&PyDict>() {
        let result = deserialize(py, mapping.into())?;
        Ok(result.into())
    } else if let Ok(_) = value.getattr("__gyver_attrs__") {
        let mapping = make_mapping(py, value.into_py(py), None)?;
        let result = deserialize(py, mapping.extract(py)?)?;
        Ok(result.into())
    } else {
        Ok(value.into())
    }
}
#[pyfunction]
fn deserialize_mapping(py: Python, mapping: &PyDict) -> PyResult<Py<PyDict>> {
    let result = PyDict::new(py);

    for (key, value) in mapping.iter() {
        let unwrapped = deserialize(py, value)?;
        result.set_item(key, unwrapped)?;
    }

    Ok(result.into())
}

#[pymodule]
#[pyo3(name = "gattrs_converter")]
fn gyver_attrs_extras(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(make_mapping, m)?)?;
    m.add_function(wrap_pyfunction!(deserialize_mapping, m)?)?;

    Ok(())
}
