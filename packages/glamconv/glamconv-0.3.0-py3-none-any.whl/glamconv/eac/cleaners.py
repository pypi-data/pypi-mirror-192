# -*- coding: utf-8 -*-
"""
Module containing actions for deleting attributes or sub-elements from the XML
elements because they don't exist anymore in Ape-EAC format.
"""

from lxml import etree
from glamconv.utils import split_qname, NS
from glamconv.eac.utils import log_element
from glamconv.eac.formats import EAC_CPF
from glamconv.transformer.actions import TransformAction


ATTR_TO_ERASE = {
    "abbreviation": ("xml:id",),
    "abstract": ("localType", "xml:id"),
    "address": ("xml:id", "xml:lang"),
    "addressLine": ("xml:id",),
    "agencyCode": ("xml:id",),
    "agencyName": ("xml:id",),
    "agent": ("xml:id",),
    "agentType": ("xml:id",),
    "alternativeForm": ("xml:id",),
    "alternativeSet": ("xml:id",),
    "authorizedForm": ("xml:id",),
    "biogHist": (
        "xml:id",
        "xml:lang",
    ),
    "chronItem": ("xml:id",),
    "chronList": ("localType", "xml:id", "xml:lang"),
    "citation": ("xml:id",),
    "componentEntry": ("xml:id",),
    "control": ("xml:base", "xml:id", "xml:lang"),
    "conventionDeclaration": ("xml:id", "xml:lang"),
    "cpfDescription": ("xml:base", "xml:id", "xml:lang"),
    "cpfRelation": ("xml:id", "xml:lang"),
    "date": ("xml:id",),
    "dateRange": ("xml:id", "xml:lang"),
    "dateSet": ("localType", "xml:id", "xml:lang"),
    "description": ("xml:base", "xml:id", "xml:lang"),
    "descriptiveNote": ("xml:id", "xml:lang"),
    "eac-cpf": ("xml:id",),
    "entityId": ("xml:id",),
    "entityType": ("xml:id",),
    "event": ("xml:id",),
    "eventDateTime": ("xml:id", "xml:lang"),
    "eventDescription": ("xml:id",),
    "eventType": ("xml:id",),
    "existDates": (
        "localType",
        "xml:id",
        "xml:lang",
    ),
    "fromDate": ("localType", "xml:id"),
    "function": ("xml:id", "xml:lang"),
    "functionRelation": ("xml:id", "xml:lang"),
    "functions": ("localType", "xml:id", "xml:lang"),
    "generalContext": ("localType", "xml:id", "xml:lang"),
    "identity": ("localType", "xml:base", "xml:id", "xml:lang"),
    "item": ("xml:id",),
    "language": ("xml:id",),
    "languageDeclaration": ("xml:id", "xml:lang"),
    "languageUsed": ("xml:id", "xml:lang"),
    "languagesUsed": ("localType", "xml:id", "xml:lang"),
    "legalStatus": ("xml:id", "xml:lang"),
    "legalStatuses": ("localType", "xml:id", "xml:lang"),
    "level": ("xml:id",),
    "list": ("localType", "xml:id", "xml:lang"),
    "localControl": ("xml:id", "xml:lang"),
    "localDescription": ("xml:id", "xml:lang"),
    "localDescriptions": ("xml:id", "xml:lang"),
    "localTypeDeclaration": ("xml:id", "xml:lang"),
    "maintenanceAgency": ("xml:id",),
    "maintenanceEvent": ("xml:id",),
    "maintenanceHistory": ("xml:id", "xml:lang"),
    "maintenanceStatus": ("xml:id",),
    "mandate": ("xml:id", "xml:lang"),
    "mandates": ("localType", "xml:id", "xml:lang"),
    "nameEntry": ("scriptCode", "transliteration", "xml:id", "xml:lang"),
    "nameEntryParallel": ("xml:id",),
    "occupation": ("xml:id", "xml:lang"),
    "occupations": ("localType", "xml:id", "xml:lang"),
    "otherAgencyCode": ("xml:id",),
    "otherRecordId": ("xml:id",),
    "outline": ("localType", "xml:id", "xml:lang"),
    "p": ("xml:id",),
    "part": ("xml:id",),
    "place": ("localType", "xml:id", "xml:lang"),
    "placeEntry": ("accuracy", "altitude", "xml:id"),
    "placeRole": ("xml:id",),
    "places": ("localType", "xml:id", "xml:lang"),
    "preferredForm": ("xml:id",),
    "publicationStatus": ("xml:id",),
    "recordId": ("xml:id",),
    "relationEntry": ("xml:id",),
    "relations": ("xml:base", "xml:id", "xml:lang"),
    "resourceRelation": ("xml:id", "xml:lang"),
    "rightsDeclaration": ("xml:id",),
    "script": ("xml:id",),
    "setComponent": ("xml:id",),
    "source": ("xml:id",),
    "sourceEntry": ("xml:id",),
    "sources": ("xml:base", "xml:id", "xml:lang"),
    "structureOrGenealogy": ("localType", "xml:id", "xml:lang"),
    "term": ("xml:id",),
    "toDate": ("localType", "xml:id"),
    "useDates": ("xml:id", "xml:lang"),
}


def _delete_attributes_and_log(xml_elt, attrs_to_delete, log_data):
    count_elts = 0
    count_atts = 0
    deleted = []
    for att_qname in xml_elt.attrib:
        att_ns, att_name = split_qname(att_qname)
        key = "xml:" + att_name if att_ns == NS["xml"] else att_name
        if key in attrs_to_delete:
            deleted.append(key)
            xml_elt.attrib.pop(att_qname)
            count_elts = 1
            count_atts += 1
    if len(deleted) > 0:
        msg = f"    Deleted attributes: {' '.join(deleted)}"
        log_data.append(log_element(xml_elt, msg=msg))
    return count_elts, count_atts


def _delete_attributes(xml_elt, attrs_to_delete):
    count_elts = 0
    count_atts = 0
    for att_qname in xml_elt.attrib:
        att_ns, att_name = split_qname(att_qname)
        key = "xml:" + att_name if att_ns == NS["xml"] else att_name
        if key in attrs_to_delete:
            xml_elt.attrib.pop(att_qname)
            count_elts = 1
            count_atts += 1
    return count_elts, count_atts


class AttributesEraser(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "attributes-eraser"
    name = "Erasing attributes that don't exist in Ape-EAC"
    category = "Cleansing"
    desc = (
        "Ape-EAC has more constraints than EAC-CPF. Numerous elements "
        "cannot contain some attributes that were authorized in EAC-CPF. "
        "This action deletes these attributes."
    )

    def _execute(self, xml_root, logger, log_details):
        count_elts, count_atts = 0, 0
        if log_details:
            log_data = []
            for elt in xml_root.iter(etree.Element):
                namespace, name = split_qname(elt.tag)
                if len(elt.attrib) == 0:
                    continue
                cnt_e, cnt_a = _delete_attributes_and_log(
                    elt, ATTR_TO_ERASE.get(name, tuple()), log_data
                )
                count_elts += cnt_e
                count_atts += cnt_a
        else:
            for elt in xml_root.iter(etree.Element):
                namespace, name = split_qname(elt.tag)
                if len(elt.attrib) == 0:
                    continue
                cnt_e, cnt_a = _delete_attributes(elt, ATTR_TO_ERASE.get(name, tuple()))
                count_elts += cnt_e
                count_atts += cnt_a
        if count_elts > 0:
            logger.warning(
                "Deleting non-legit attributes from the elements. "
                f"{count_atts:d} attributes have been deleted from "
                f"{count_elts:d} elements."
            )
            if log_details:
                logger.warning(
                    "The following elements have had some attributes deleted:\n"
                    + "\n".join(log_data)
                )
        return xml_root


class MultipleIdentitiesEraser(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "multiple-identities-eraser"
    name = "Erasing the <multipleIdentities> element"
    category = "Cleansing"
    desc = (
        "Ape-EAC doesn't allow the description of multiple identities in "
        "the <multipleIdentities> element. This action keeps the first "
        "<cpfDescription> child of <multipleIdentities> and deletes the "
        "followings and the <multipleIdentities>element."
    )

    def _execute(self, xml_root, logger, log_details):
        for xml_elt in xml_root.xpath("multipleIdentities"):
            descs = xml_elt.xpath("cpfDescription")
            logger.warning(
                "Deleting the non-legit <multipleIdentities> element but "
                "keeping the first identity described"
            )
            if log_details:
                logger.warning(
                    "The following elements have been deleted:\n"
                    + log_element(xml_elt)
                    + "\n"
                    + "\n".join(log_element(elt) for elt in descs[1:])
                )
            if len(descs) > 0:
                xml_elt.getparent().append(descs[0])
            xml_elt.getparent().remove(xml_elt)
        return xml_root


class AdditionalLanguageDeclarationEraser(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "additional-language-declarations-eraser"
    name = (
        "Erasing the additional <languageDeclaration> elements (after the " "first one)"
    )
    category = "Cleansing"
    desc = (
        "Ape-EAC only allows one <languageDeclaration> element in <control> "
        "element. This action deletes all the existing elements after the "
        "first one and their contents."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        for xml_elt in xml_root.xpath(
            "control/languageDeclaration[preceding-sibling::languageDeclaration]"
        ):
            count += 1
            if log_details:
                deleted_elts.append(log_element(xml_elt))
            xml_elt.getparent().remove(xml_elt)
        if count > 0:
            logger.warning(
                "Deleting additional <languageDeclaration> elements (after "
                f"the first one) in <control>. {count} elements have been "
                "deleted."
            )
            if log_details:
                logger.warning(
                    "The following elements have been deleted:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root


class AdditionalNameOrEntryEraser(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "additional-names-entries-eraser"
    name = (
        "Erasing the additional elements (after the first one) giving a "
        "name, an entry or a description in some elements"
    )
    category = "Cleansing"
    desc = (
        "In some elements, Ape-EAC only allows one element giving the name, "
        "the entry or the description. These elements are <eventDescription> "
        "in <maintenanceEvent>, <agencyName> in <maintenanceAgency>, "
        "<placeEntry> in <functionRelation>, <placeEntry> in "
        "<resourceRelation> and <sourceEntry> in <source>. This action deletes "
        "the additional elements (but keeps the first one)."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        parts = []
        for prt_name, elt_name in (
            ("maintenanceEvent", "eventDescription"),
            ("maintenanceAgency", "agencyName"),
            ("functionRelation", "placeEntry"),
            ("resourceRelation", "placeEntry"),
            ("source", "sourceEntry"),
        ):
            parts.append(f".//{prt_name}/{elt_name}[preceding-sibling::{elt_name}]")
        for xml_elt in xml_root.xpath(" | ".join(parts)):
            count += 1
            deleted_elts.append(log_element(xml_elt, text_content=True))
            xml_elt.getparent().remove(xml_elt)
        if count > 0:
            logger.warning(
                "Deleting additional elements (after the first one) giving a "
                "a name, an entry or a description in some elements. "
                f"{count:d} elements have been deleted."
            )
            if log_details:
                logger.warning(
                    "The following elements have been deleted:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root


class WrappingObjectsEraser(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "wrapping-objects-eraser"
    name = "Erasing the elements wrapping XML or binary data"
    category = "Cleansing"
    desc = (
        "Ape-EAC doesn't allow the <objectBinWrap> and <objectXMLWrap> "
        "elements that can contain binary or XML data. This action deletes "
        "these elements and their content."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        deleted_elts = []
        for xml_elt in xml_root.xpath(".//objectBinWrap | .//objectXMLWrap"):
            count += 1
            if log_details:
                deleted_elts.append(log_element(xml_elt))
            xml_elt.getparent().remove(xml_elt)
        if count > 0:
            logger.warning(
                "Deleting <objectBinWrap> and <objectXMLWrap> elements "
                f"wrapping XML or binary data. {count:d} elements have been "
                "deleted."
            )
            if log_details:
                logger.warning(
                    "The following elements have been deleted:\n"
                    + "\n".join(deleted_elts)
                )
        return xml_root
