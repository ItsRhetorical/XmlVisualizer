import xml.etree.ElementTree as ETree

def parse_file(_file):
    tree = ETree.parse(_file)
    root = tree.getroot()
    return tree, root

# cleans the namespace off the whole branch
def remove_namespace_from_branch(_branch):
    for element in _branch.iter():
        ns_end = element.tag.find('}') + 1
        clean_tag = element.tag[ns_end:]
        element.tag = clean_tag
        # print(_branch)


# removes nodes that hold only whitespace
def collapse_empty_nodes(_branch):
    for element in _branch.iter():
        if len(list(element)) == 0:# no children
            if element.text:
                element.text = None


# removes element and all children by tag name
def remove_tag_from_branch(_branch,_tag):
    for element in _branch.iter():
        for sub_element in element:
            if sub_element.tag == _tag:
                element.remove(sub_element)
        # print(element)
    # print(_branch)


# like remove_tag_from_branch but keeps the children
def collapse_tag_from_branch(_branch,_tag):
    for element in _branch.iter():
        for sub_element in element:
            if sub_element.tag == _tag:
                for child in sub_element:
                    element.append(child)
                element.remove(sub_element)


# removes extra line returns after a closed element
def clean_long_tails(_branch):
    for element in _branch.iter():
        if element.tail:
            if element.tail.count('\n')>1:
                element.tail = element.tail[element.tail.rfind('\n'):]

def safe_caption(_element):
    try:
        return _element.attrib['FlagKey']
    except KeyError:
        try:
            return _element.attrib['CategoryCode']
        except KeyError:
            return _element.tag


