import re
import xml.etree.ElementTree as et
from typing import List, Dict


def get_institution_codes(authors: List[dict]) -> List[List[str]]:
    return [a['Institution Code'].split(',') for a in authors]


def get_institution_addresses(authors: List[dict]) -> List[List[str]]:
    return [a['Institution'] for a in authors]


def get_institution_dict(institution_codes: List[List[str]], institution_addresses: List[List[str]]) -> Dict[str, str]:
    inst_dict = {}
    for code, inst in zip(institution_codes, institution_addresses):
        for c in code:
            for i in re.findall(r'\{([^{}]*)\}', inst):
                inst_dict[c.strip()] = i.strip()
    return inst_dict


def assign_institution_ids(unique_institutions: List[str]) -> Dict[str, str]:
    return {inst: f"a{i}" for i, inst in enumerate(unique_institutions, 1)}


def get_unique_institution_codes(institutions: List[List[str]]) -> List[str]:
    return list(set(code.strip() for sublist in institutions for code in sublist))


def setup_root_element() -> et.Element:
    root = et.Element("collaborationauthorlist")
    namespaces = {"cal": "http://inspirehep.net/info/HepNames/tools/authors_xml/",
                  "foaf": "http://xmlns.com/foaf/0.1/"}
    for prefix, uri in namespaces.items():
        root.set(f"xmlns:{prefix}", uri)
    return root


def create_sub_ce(parent: et.Element, ns: str, tag: str, **kwargs) -> et.Element:
    return et.SubElement(parent, f"{ns}:{tag}", kwargs)


def create_text_sub_ce(parent: et.Element, ns: str, tag: str, text: str = None, **kwargs) -> et.Element:
    if text:
        el = create_sub_ce(parent, ns, tag, **kwargs)
        el.text = text
        return el
    return None


def pretty_print(current: et.Element, parent: et.Element = None, index: int = -1, depth: int = 0) -> None:
    for i, node in enumerate(current):
        pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '' + ('	' * depth)
        else:
            parent[index - 1].tail = '' + ('	' * depth)
        if index == len(parent) - 1:
            current.tail = '' + ('	' * (depth - 1))