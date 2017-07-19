a sphinx extension
==================
that reads a project A and checks for all uses of project B and
generates a glossary of all usages of project B in project A
(eg generate a glossary for unit and integration/functional tests to serve as
usage documentation)
a project may be a package or a module

[![Build Status](https://travis-ci.org/michaelhaberler/glossario.svg?branch=master)](https://travis-ci.org/michaelhaberler/glossario)

ideas/inspiration
-----------------
* use a sphinx builder - like
  [sphinx.ext.coverage](http://www.sphinx-doc.org/en/stable/_modules/sphinx/ext/coverage.html#CoverageBuilder)
  - and combine with [sphinx.ext.intersphinx]()
* pylint (pyreverse, astroid)

status
------

```
cd glossario
export PYTHONPATH=`pwd`
cd tests/doc_example
sphinx-build -b html -d ../build/doc/doctrees   . ../build/doc/html -vv
```
