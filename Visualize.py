from graphviz import Digraph, render
import os
import XmlHelper

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

engine='dot'
file_type='svg'
graph_file='outputvis'


def generate_clean_xml(_file):
    _tree, _root = XmlHelper.parse_file(_file)

    # clean up flags file
    XmlHelper.remove_namespace_from_branch(_root)
    XmlHelper.remove_tag_from_branch(_root, 'Changes')
    XmlHelper.collapse_tag_from_branch(_root, 'Flags')
    XmlHelper.collapse_tag_from_branch(_root, 'Categories')
    XmlHelper.collapse_empty_nodes(_root)
    XmlHelper.clean_long_tails(_root)
    _root.tag = 'Categories'
    # save flags output
    _tree.write('output.xml')
    return _tree, _root

def recursive_link_children(_graph,parent):
    for child in list(parent):
        _graph.edge(XmlHelper.safe_caption(parent), XmlHelper.safe_caption(child))
        recursive_link_children(_graph,child)

def build_graph(_branch):
    _g = initialize_graph()
    recursive_link_children(_g,_branch)
    return _g

def ensure_xml_data():
    try:
        if os.stat('output.xml').st_size > 0:
           print('Prepared XML ready, Skipping generation')
           tree, root = XmlHelper.parse_file('output.xml')
        else:
           print('Empty XML file, Generating new')
           tree, root = generate_clean_xml('Flags.xml')
    except OSError:
        print('No output.xml file, Generating new')
        tree, root = generate_clean_xml('Flags.xml')
    return tree, root

def ensure_graph_data():
    try:
        if os.stat(graph_file).st_size > 0:
            print('Graph Ready, Skipping Generation')
            _g, _tree, _root = None, None, None
        else:
            print('Empty graph file, Generating new')
            _tree, _root = ensure_xml_data()
            _g = build_graph(_root)
    except OSError:
        print('No outputvis file, Generating new')
        _tree, _root = ensure_xml_data()
        _g = build_graph(_root)
    return _g, _tree, _root

def initialize_graph():
    _g = Digraph(engine=engine, format=file_type)
    _g.attr('node', shape="rectangle", spline="line")
    _g.attr(rankdir="LR")
    return _g

def main():
    g, tree, root = ensure_graph_data()
    if g:
        g.render(graph_file, view=False, cleanup=True)
    else:
        print('!!!!!Cached Response!!!!!')
        render(engine, file_type, graph_file)

if __name__ =="__main__":
    main()