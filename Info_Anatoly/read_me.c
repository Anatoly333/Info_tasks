#include <Python.h>

#include "pegen.h"
#include "string_parser.h"

static PyObject *
_create_dummy_identifier(Parser *p)
{
    return _PyPegen_new_identifier(p, "");
}

void *
_PyPegen_dummy_name(Parser *p, ...)
{
    static void *cache = NULL;

    if (cache != NULL) {
        return cache;
    }

    PyObject *id = _create_dummy_identifier(p);
    if (!id) {
        return NULL;
    }
    cache = _PyAST_Name(id, Load, 1, 0, 1, 0, p->arena);
    return cache;
}

/* Creates a single-element asdl_seq* that contains a */
asdl_seq *
_PyPegen_singleton_seq(Parser *p, void *a)
{
    assert(a != NULL);
    asdl_seq *seq = (asdl_seq*)_Py_asdl_generic_seq_new(1, p->arena);
    if (!seq) {
        return NULL;
    }
    asdl_seq_SET_UNTYPED(seq, 0, a);
    return seq;
}

/* Creates a copy of seq and prepends a to it */
asdl_seq *
_PyPegen_seq_insert_in_front(Parser *p, void *a, asdl_seq *seq)
{
    assert(a != NULL);
    if (!seq) {
        return _PyPegen_singleton_seq(p, a);
    }

    asdl_seq *new_seq = (asdl_seq*)_Py_asdl_generic_seq_new(asdl_seq_LEN(seq) + 1, p->arena);
    if (!new_seq) {
        return NULL;
    }

    asdl_seq_SET_UNTYPED(new_seq, 0, a);
    for (Py_ssize_t i = 1, l = asdl_seq_LEN(new_seq); i < l; i++) {
        asdl_seq_SET_UNTYPED(new_seq, i, asdl_seq_GET_UNTYPED(seq, i - 1));
    }
    return new_seq;
}

/* Creates a copy of seq and appends a to it */
asdl_seq *
_PyPegen_seq_append_to_end(Parser *p, asdl_seq *seq, void *a)
{
    assert(a != NULL);
    if (!seq) {
        return _PyPegen_singleton_seq(p, a);
    }

    asdl_seq *new_seq = (asdl_seq*)_Py_asdl_generic_seq_new(asdl_seq_LEN(seq) + 1, p->arena);
    if (!new_seq) {
        return NULL;
    }

    for (Py_ssize_t i = 0, l = asdl_seq_LEN(new_seq); i + 1 < l; i++) {
        asdl_seq_SET_UNTYPED(new_seq, i, asdl_seq_GET_UNTYPED(seq, i));
    }
    asdl_seq_SET_UNTYPED(new_seq, asdl_seq_LEN(new_seq) - 1, a);
    return new_seq;
}

static Py_ssize_t
_get_flattened_seq_size(asdl_seq *seqs)