//
// Created by Joe Yu on 11/17/22.
//
#include <stdio.h>
#include <stdlib.h>
#include <Python.h>
#include "wiipointer.h"

static PyObject *ir(PyObject *self, PyObject *args) {
    int raw_x, raw_y, raw_z;
    struct ir_t *ir1 = malloc(sizeof(struct ir_t));
    initialize_ir(ir1);

    if (!PyArg_ParseTuple(args, "iiiiiiiiiii",
                          &ir1->dot[0].rx,
                          &ir1->dot[0].ry,
                          &ir1->dot[1].rx,
                          &ir1->dot[1].ry,
                          &ir1->dot[2].rx,
                          &ir1->dot[2].ry,
                          &ir1->dot[3].rx,
                          &ir1->dot[3].ry,
                          &raw_x,
                          &raw_y,
                          &raw_z)) {
        return NULL;
    }

    for (int i = 0; i < 4; ++i) {
        if (ir1->dot[i].rx != 1023 || ir1->dot[i].ry != 1023) ir1->dot[i].visible = 1;
    }

    ir1->roll = atan2(raw_x, -raw_z);

    process_ir_data(ir1);

    PyObject *python_val = Py_BuildValue("[iffifff]", ir1->raw_valid, ir1->ax, ir1->ay,
                                         ir1->smooth_valid, ir1->sx, ir1->sy, ir1->distance);
    free(ir1);
    return python_val;
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef irMethods[] = {
        {"ir", ir, METH_VARARGS, "Process IR data"},
        {NULL, NULL, 0, NULL}
};

// Our Module Definition struct
static struct PyModuleDef irModule = {
        PyModuleDef_HEAD_INIT,
        "ir",
        "ir Module",
        -1,
        irMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_irProcessing(void) {
    return PyModule_Create(&irModule);
}
