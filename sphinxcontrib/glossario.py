#!/usr/bin/env python
"""
* https://pymotw.com/2/inspect/
* https://pymotw.com/2/imp/
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import argparse
import logging
import pprint
from collections import deque

import imp
import inspect
import ast
from collections import namedtuple


LOGGER = logging.getLogger(os.path.basename(__file__))


def import_file(filename):
    dirname = os.path.abspath(os.path.dirname(filename))
    base, ext = os.path.splitext(os.path.basename(filename))
    f, filename, desc = imp.find_module(base, [dirname])
    LOGGER.debug("file=%s, desc=%s", filename, desc)
    return imp.load_module(base, f, filename, desc)


def module_members(module):
    return inspect.getmembers(mod, inspect.ismodule)


Import = namedtuple("Import", ["module", "name", "alias", "ast_node"])

def get_imports(path):
    """
    http://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module
    """
    with open(path) as fh:
        root = ast.parse(fh.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname, n)


def get_full_import_names(path):
    """
    .. todo::
        Create a visitor from get_imports and get_full_import_names
    """
    imports = get_imports(path)
    names = []
    for imp in imports:
        name = ''
        if imp.module:
            name += '.'.join([m for m in imp.module])
        if imp.name:
            if name:
                name += '.'
            name += '.'.join([m for m in imp.name])
        names.append(name)
    LOGGER.debug(names)
    return names


class CallVisitor(ast.NodeVisitor):

    def __init__(self):
        self._name = deque()
        self.lineno = None

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)
        self.lineno = node.lineno

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)
        if not self.lineno:
            self.lineno = node.lineno

    #def visit_Call(self, node):
    #    self.generic_visit(node)


class ImportedVisitor(ast.NodeVisitor):

    def __init__(self, imports):
        self._import_stmts = imports
        self._imported = []

    def _in_imported(self, node_attr):
        return any(node_attr in _import
                   for _import in self._import_stmts)

    def visit_Name(self, node):
        if any(node.id in _import
               for _import in self._import_stmts):
            import ipdb; ipdb.set_trace()
            self._imported.append(node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if any(node.value.id in _import
               for _import in self._import_stmts):
            import ipdb; ipdb.set_trace()
            #node.attr + node.value
            self._imported.append(node)
        self.generic_visit(node)


Call = namedtuple("Call", ["name", "lineno", "ast_node"])

def get_full_used_names(path):
    """
    https://gist.github.com/jargnar/0946ab1d985e2b4ab776#file-function_calls_ast-py
    http://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
    """
    calls = []
    with open(path) as fh:
        root = ast.parse(fh.read(), path)

        for n in ast.walk(root):
            LOGGER.debug(n)
            #for m in ast.iter_fields(n):
            #    LOGGER.debug('    ' + repr(m))
            if isinstance(n, ast.Module):
                #import ipdb; ipdb.set_trace()
                LOGGER.debug('    %s', getattr(n, 'id', 'none'))
            if isinstance(n, ast.ClassDef):
                #import ipdb; ipdb.set_trace()
                LOGGER.debug('%d: %s', n.lineno, getattr(n, 'name', 'none'))
            if isinstance(n, ast.FunctionDef):
                #import ipdb; ipdb.set_trace()
                LOGGER.debug('%d: %s', n.lineno, getattr(n, 'name', 'none'))
                #n.body
            if isinstance(n, ast.Call):
                LOGGER.debug('%d: %s', n.lineno, getattr(n, 'name', 'none'))
                #try:
                #    LOGGER.debug(repr(n.func.attr))
                #except AttributeError:
                #    pass
                visitor = CallVisitor()
                visitor.visit(n.func)
                calls.append(Call(visitor.name, visitor.lineno, n))
            #if isinstance(n, ast.Alias):
            #    LOGGER.debug(repr(n))

        #CallVisitor().visit(root)
    return calls


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)-12s %(levelname)-8s %(message)s')
    LOGGER.debug("args = %s", vars(args))


    #mod = import_file(args.file)
    #LOGGER.debug(pprint.pformat(module_members(mod)))


    LOGGER.info("get_imports")
    for imp in get_imports(args.file):
        LOGGER.debug(imp)

    LOGGER.info("get_full_import_names")
    full_import_names = get_full_import_names(args.file)
    for imp in full_import_names:
        LOGGER.debug(imp)

    with open(args.file) as fh:
        root = ast.parse(fh.read(), args.file)
        impvisitor = ImportedVisitor(full_import_names)
        impvisitor.visit(root)
        #import ipdb; ipdb.set_trace()

    # modulefinder
    # https://docs.python.org/2/library/modulefinder.html

    LOGGER.info("get_full_used_names")
    names = get_full_used_names(args.file)
    for name in names:
        LOGGER.debug(name)
