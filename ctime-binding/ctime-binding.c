#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>
#include <sys/time.h>

static PyObject* get_c_time(PyObject* self, PyObject* args) {
    struct timeval time;
    gettimeofday(&time, NULL);

    return Py_BuildValue("(LL)", time.tv_sec, time.tv_usec);
}

static PyMethodDef methods[] = {
    { "get_c_time", get_c_time, METH_VARARGS, "Get the time according to the gettimeofday function in sys/time.h\nReturns (sec, msec)" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "ctime_binding",
    NULL,
    -1,

    methods
};

PyMODINIT_FUNC PyInit_ctime_binding(void) {
    return PyModule_Create(&module);
}
