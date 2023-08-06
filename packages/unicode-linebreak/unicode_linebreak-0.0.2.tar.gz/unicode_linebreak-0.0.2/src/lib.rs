use pyo3::prelude::*;
use unicode_linebreak::{
    linebreaks as rust_linebreaks,
    BreakOpportunity::{
        Allowed as RustAllowed
    }
};

#[pyclass]
struct Linebreaks {
    inner: std::vec::IntoIter<(usize, bool)>,
}

#[pymethods]
impl Linebreaks {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    
    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<(usize, bool)> {
        slf.inner.next()
    }
}


#[pyfunction]
fn linebreaks(text: &str) -> PyResult<Linebreaks> {
    Ok(Linebreaks {
        inner: rust_linebreaks(text)
            .map(|(i, opp)| {
                match opp {
                    RustAllowed => (i, false),
                    _ => (i, true),
                }
            })
            .collect::<Vec<(usize, bool)>>()
            .into_iter(),
    })
}

#[pymodule]
#[pyo3(name = "unicode_linebreak")]
fn py_unicode_linebreak(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(linebreaks, m)?)?;
    m.add("Allowed", false)?;
    m.add("Mandatory", true)?;
    Ok(())
}
