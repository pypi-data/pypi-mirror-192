# -*- coding: utf-8 -*-
"""
Module containing actions for adding required elements in the XML tree.
These actions actually have a parameter to specify the value of the element
if it is not present.
"""

import datetime as dtm
from lxml import etree
from glamconv.eac.utils import log_element
from glamconv.eac.formats import EAC_CPF
from glamconv.transformer.actions import TransformAction
from glamconv.transformer.parameters import SingleParameter


class PlaceEntryAdder(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "placeentry-adder"
    name = "Adding a <placeEntry> element in <place>"
    category = "Required elements adding"
    desc = (
        "This action adds a <placeEntry> element in the <place> elements if "
        "it is not present. This element is required in Ape-EAC."
    )
    params_def = (
        SingleParameter(
            "default_value",
            "Place entry default value",
            "Value to be used for the place entry if it is not present in a "
            "<place> element.",
            "Text",
            str,
            "unknown",
        ),
    )

    def _execute(self, xml_root, logger, log_details, default_value):
        count = 0
        corrected_elts = []
        for xml_elt in xml_root.xpath(".//place[not(placeEntry)]"):
            idx = 1 if xml_elt.find("placeRole") is not None else 0
            entry_elt = etree.Element("placeEntry")
            entry_elt.text = default_value
            xml_elt.insert(idx, entry_elt)
            count += 1
            if log_details:
                corrected_elts.append(log_element(xml_elt))
        if count > 0:
            logger.warning(
                "A <placeEntry> element with a default value has been added "
                f"in {count:d} <place> elements."
            )
            if log_details:
                logger.warning(
                    "The following <place> elements have been completed:\n"
                    + "\n".join(corrected_elts)
                )
        return xml_root


class AgencyCodeAdder(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "agencycode-adder"
    name = "Adding an <agencyCode> element in <maintenanceAgency>"
    category = "Required elements adding"
    desc = (
        "This action adds an <agencyCode> element in the "
        "<maintenanceAgency> element if it is not present. This element is "
        "required in Ape-EAC."
    )
    params_def = (
        SingleParameter(
            "default_value",
            "Agency code default value",
            "Value to be used for the agency code if it is not present in the "
            "<maintenanceAgency> element.",
            "Text",
            str,
            "XX-unknown",
        ),
    )

    def _execute(self, xml_root, logger, log_details, default_value):
        count = 0
        corrected_elts = []
        for xml_elt in xml_root.xpath(".//maintenanceAgency[not(agencyCode)]"):
            code_elt = etree.Element("agencyCode")
            code_elt.text = default_value
            xml_elt.insert(0, code_elt)
            count += 1
            if log_details:
                corrected_elts.append(log_element(xml_elt))
        if count > 0:
            logger.warning(
                "An <agencyCode> element with a default value has been added "
                f"in {count:d} <maintenanceAgency> elements."
            )
            if log_details:
                logger.warning(
                    "The following <maintenanceAgency> elements have been "
                    "completed:\n" + "\n".join(corrected_elts)
                )
        return xml_root


class ExistDatesAdder(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "existdates-adder"
    name = "Adding an <existDates> element in <description>"
    category = "Required elements adding"
    desc = (
        "This action adds an <existDates> element in the <description> "
        "element if it is not present. This element is required in Ape-EAC. "
        "If the <description> element doesn't exist in the <cpfDescription> "
        "element, it will be added before adding the <existDates> element."
    )
    params_def = (
        SingleParameter(
            "default_value",
            "exist dates default value",
            "Value to be used for the exist dates if it is not present in the "
            "<description> element.",
            "Text",
            str,
            "<string value of today's date>",
        ),
    )

    def _execute(self, xml_root, logger, log_details, default_value):
        if default_value == "<string value of today's date>":
            default_value = dtm.date.today().strftime("%Y-%m-%d")
        # First, check a <description> element exists in <cpfDescription>
        count = 0
        corrected_elts = []
        for xml_elt in xml_root.xpath(".//cpfDescription[not(description)]"):
            idx = 1 if xml_elt.find("identity") is not None else 0
            desc_elt = etree.Element("description")
            xml_elt.insert(idx, desc_elt)
            count += 1
            if log_details:
                corrected_elts.append(log_element(xml_elt))
        if count > 0:
            logger.warning(
                f"A <description> element has been added in {count:d} "
                "<cpfDescription> elements."
            )
            if log_details:
                logger.warning(
                    "The following <cpfDescription> elements have been "
                    "completed:\n" + "\n".join(corrected_elts)
                )
        # Then, check a <existDates> element exists in <description>
        count = 0
        corrected_elts = []
        for xml_elt in xml_root.xpath(".//description[not(existDates)]"):
            exd_elt = etree.Element("existDates")
            xml_elt.insert(0, exd_elt)
            date_elt = etree.Element("date")
            date_elt.text = default_value
            exd_elt.append(date_elt)
            count += 1
            if log_details:
                corrected_elts.append(log_element(xml_elt))
        if count > 0:
            logger.warning(
                f"An <existDates> element has been added in {count:d} "
                "<description> elements."
            )
            if log_details:
                logger.warning(
                    "The following <description> elements have been "
                    "completed:\n" + "\n".join(corrected_elts)
                )
        return xml_root
