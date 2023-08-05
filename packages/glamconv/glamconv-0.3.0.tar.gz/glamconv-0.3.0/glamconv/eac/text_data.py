# -*- coding: utf-8 -*-
"""
Module containing actions for converting, moving or correcting XML elements
that contain text data.
"""

from lxml import etree
from glamconv.utils import NS, suppress_element
from glamconv.eac.utils import log_element
from glamconv.eac.formats import EAC_CPF
from glamconv.transformer.actions import TransformAction


def convert_p(elt):
    return [elt]


def convert_citation(elt):
    for att_name in elt.attrib:
        if att_name != f"{{{NS['xml']}}}lang":
            elt.attrib.pop(att_name)
    elt.tag = "p"
    return [elt]


def convert_list(elt):
    converted_elts = []
    for itm_elt in elt.xpath("item"):
        converted_elts.extend(convert_item(itm_elt))
    return converted_elts


def convert_outline(elt):
    converted_elts = []
    for lvl_elt in elt.xpath("level"):
        converted_elts.extend(convert_level(lvl_elt))
    return converted_elts


def convert_item(elt):
    if "localType" in elt.attrib:
        elt.attrib.pop("localType")
    elt.tag = "p"
    return [elt]


def convert_level(elt):
    converted_elts = []
    for child_elt in elt.xpath("level|item"):
        if child_elt.tag == "item":
            converted_elts.extend(convert_item(child_elt))
        else:
            converted_elts.extend(convert_level(child_elt))
    return converted_elts


CONVERT_FUNCTION = {
    "p": convert_p,
    "citation": convert_citation,
    "list": convert_list,
    "outline": convert_outline,
}


class SpanConverter(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "span-converter"
    name = "Removing the <span> elements but keeping the text they contain"
    category = "Text data conversion"
    desc = (
        "In Ape-EAC, the <span> element doesn't exist anymore. This action "
        "moves the textual content of these elements into their parents "
        "(paragraphs, etc.) and then removes these elements."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        for elt in xml_root.xpath(".//span"):
            count += 1
            if log_details:
                deleted_elts.append(log_element(elt))
            suppress_element(elt)
        if count > 0:
            logger.info(
                f"{count:d} <span> elements have been removed (but their "
                "textual content has been kept)."
            )
            if log_details:
                logger.info(
                    "The following elements have been removed:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root


class BioghistListOutlineConverter(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "bioghist-list-outline-converter"
    name = "Removing the <list> and <outline> elements from <biogHist> elements"
    category = "Text data conversion"
    desc = (
        "In Ape-EAC, the <biogHist> element can't contain <list> or <outline> "
        "elements. This action puts the textual content from these elements "
        "into paragraphs that are kept in the <biogHist> element, and then "
        "removes these elements."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        for elt in xml_root.xpath(".//biogHist/list|.//biogHist/outline"):
            count += 1
            if log_details:
                deleted_elts.append(log_element(elt))
            idx = elt.getparent().index(elt)
            for conv_elt in reversed(CONVERT_FUNCTION[elt.tag](elt)):
                elt.getparent().insert(idx, conv_elt)
            elt.getparent().remove(elt)
        if count > 0:
            logger.info(
                f"{count:d} <list> and <outline> elements have been removed "
                "from <biogHist> elements (but their textual content has been "
                "kept)."
            )
            if log_details:
                logger.info(
                    "The following elements have been removed:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root


class GeneralcontextListCitationConverter(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "generalcontext-list-citation-converter"
    name = (
        "Removing the <list> and <citation> elements from <generalContext> "
        "or <structureOrGenealogy> elements"
    )
    category = "Text data conversion"
    desc = (
        "In Ape-EAC, the <generalContext> and the <structureOrGenealogy> "
        "elements can't contain <list> or <citation> elements. This action "
        "puts the textual content from these elements into paragraphs that "
        "are kept in the <generalContext> or the <structureOrGenealogy> "
        "element, and then removes these elements."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        request = " | ".join(
            f".//{parent}/{element}"
            for parent in ("generalContext", "structureOrGenealogy")
            for element in ("list", "citation")
        )
        for elt in xml_root.xpath(request):
            count += 1
            if log_details:
                deleted_elts.append(log_element(elt))
            idx = elt.getparent().index(elt)
            del_elt = elt.tag != "citation"
            for conv_elt in reversed(CONVERT_FUNCTION[elt.tag](elt)):
                elt.getparent().insert(idx, conv_elt)
            if del_elt:
                elt.getparent().remove(elt)
        if count > 0:
            logger.info(
                f"{count:d} <list> and <citation> elements have been removed "
                "from <generalContext> or <structureOrGenealogy> elements "
                "(but their textual content has been kept)."
            )
            if log_details:
                logger.info(
                    "The following elements have been removed:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root


class DescriptionChildrenTextElementsConverter(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "description-children-text-elements-converter"
    name = (
        "Removing the <p>, <citation>, <list> and <outline> elements from "
        "<functions>, <legalStatuses>, <localDescriptions>, <mandates>, "
        "<occupations>, <places> elements"
    )
    category = "Text data conversion"
    desc = (
        "In Ape-EAC, the <functions>, <legalStatuses>, <localDescriptions>, "
        "<mandates>, <occupations>, <places> elements can't contain text "
        "elements such as <p>, <citation>, <list> or <outline> elements. "
        "This action puts the textual content from these elements into "
        "paragraphs that are inserted in the <descriptiveNote> child element "
        "of the parent elements (<functions>, etc.), and then removes these "
        "elements."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        request = " | ".join(
            f".//{parent}/{element}"
            for parent in (
                "functions",
                "legalStatuses",
                "localDescriptions",
                "mandates",
                "occupations",
                "places",
            )
            for element in ("p", "citation", "list", "outline")
        )
        for elt in xml_root.xpath(request):
            count += 1
            if log_details:
                deleted_elts.append(log_element(elt))
            del_elt = elt.tag != "citation" and elt.tag != "p"
            parent_elt = elt.getparent()
            note_elt = parent_elt.find("descriptiveNote")
            if note_elt is None:
                note_elt = etree.Element("descriptiveNote")
                parent_elt.append(note_elt)
            for conv_elt in CONVERT_FUNCTION[elt.tag](elt):
                note_elt.append(conv_elt)
            if del_elt:
                parent_elt.remove(elt)
        if count > 0:
            logger.info(
                f"{count:d} <p>, <citation>, <list> and <outline> elements "
                "have been removed from <functions>, <legalStatuses>, "
                "<localDescriptions>, <mandates>, <occupations> or <places> "
                "elements (but their textual content has been kept)."
            )
            if log_details:
                logger.info(
                    "The following elements have been removed:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root
