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


def get_full_used_names(path):
    """
    https://gist.github.com/jargnar/0946ab1d985e2b4ab776#file-function_calls_ast-py
    http://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
    """
    calls = []
    with open(path) as fh:
        root = ast.parse(fh.read(), path)

        for n in ast.walk(root):
            #LOGGER.debug(n)
            #for m in ast.iter_fields(n):
            #    LOGGER.debug('    ' + repr(m))
            if isinstance(n, ast.Call):
                #try:
                #    LOGGER.debug(repr(n.func.attr))
                #except AttributeError:
                #    pass
                visitor = CallVisitor()
                visitor.visit(n.func)
                calls.append((visitor.name, visitor.lineno))
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


    LOGGER.info("get_full_import_names")
    for imp in get_full_import_names(args.file):
        LOGGER.debug(imp)


    LOGGER.info("get_full_used_names")
    names = get_full_used_names(args.file)
    for name in names:
        LOGGER.debug(name)
