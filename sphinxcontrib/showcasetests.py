
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx import addnodes


class tested(nodes.Element):
    # eg li_example_a.A in test_lib_example_a.test_A
    pass


class testedlist(nodes.General, nodes.Element):
    # a list of all tested nodes and the nodes where they are tested
    pass


class TestedListDirective(Directive):

    def run(self):
        return [testedlist('')]


def process_tested_nodes(app, doctree, fromdocname):
    # 1) Add link to tested node
    # 2) Replace all testedlist nodes with a list of the collected tested nodes.
    # Augment each tested with a backlink to the original location.
    env = app.builder.env
    app.debug("fromdocname = %s" % fromdocname)
    app.debug("document.attributes['source'] = %s" %
              doctree.document.attributes['source']) # the rst-file
    for objnode in doctree.traverse(addnodes.desc):
        for signode in objnode:
            if not isinstance(signode, addnodes.desc_signature):
                continue
            module = signode.get('module')
            fullname = signode.get('fullname')
            if not module and not fullname:
                continue
            if 'test' in fullname:
                import ipdb; ipdb.set_trace()
                app.debug("%s: %s" % (module, fullname))
            # signode.document.attributes
            # signode.rawsource
            # signode.attributes['ids'] or 'names'



def setup(app):
    #import ipdb; ipdb.set_trace()
    #app.add_config_value('showcasetests_directories', [], 'env')

    app.add_node(tested)
    app.add_node(testedlist)
    app.add_directive('testedlist', TestedListDirective)

    #app.connect('doctree-read', process_tested_nodes)
    app.connect('doctree-resolved', process_tested_nodes)
    #app.connect('env-purge-doc', purge_todos)

    return {'version': '0.0'}
