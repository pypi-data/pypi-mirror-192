# -*- coding: utf-8 -*-
"""
Module defining several useful functions that will be used inside
the transform actions defined in the other modules of this sub-package.
"""

from glamconv.utils import NS


def write_hierarchy(xml_elt):
    ancest = xml_elt.xpath("ancestor-or-self::*")
    hierarchy = ""
    for idx, elt in enumerate(ancest):
        hierarchy += f"/{elt.xpath('name()')}"
        if elt.get("id"):
            hierarchy += f'[id="{elt.get("id")}"]'
        elif idx != 0:
            xpath_expr = f"count(../{elt.xpath('name()')})"
            max_index = int(elt.xpath(xpath_expr, namespaces=NS))
            if max_index > 1:
                xpath_expr = f"count(preceding-sibling::{elt.xpath('name()')})+1"
                elt_index = int(elt.xpath(xpath_expr, namespaces=NS))
                hierarchy += f"[{elt_index}]"
    return hierarchy


def log_element(xml_elt, attributes=None, text_content=False, msg=""):
    log_entry = write_hierarchy(xml_elt)
    if msg:
        log_entry += "\n    " + msg
    if attributes:
        log_entry += "\n   "
        for attrname in attributes:
            attrval = xml_elt.xpath(f"string(@{attrname})", namespaces=NS)
            if len(attrval) == 0:
                continue
            if len(attrval) > 50:
                attrval = attrval[:47] + "..."
            log_entry += f' {attrname}="{attrval}"'
    if text_content:
        log_entry += "\n    Text content: "
        txt = xml_elt.xpath("string()")
        if len(txt) > 50:
            txt = txt[:47] + "..."
        log_entry += txt
    return log_entry
