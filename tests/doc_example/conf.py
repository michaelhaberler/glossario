# -*- coding: utf-8 -*-

import sys
import os


sys.path.append('..')
sys.path.append(os.path.join(['..', '..']))

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.showcasetests',
]

source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'

# Output file base name for HTML help builder.
#htmlhelp_basename = 'lib_exampledoc'
