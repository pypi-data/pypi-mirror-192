# -*- coding: utf-8 -*-
"""
Module containing actions for adding interesting information such as the
a link towards the XML Schema used for the validation.
"""

from glamconv.utils import NS
from glamconv.ead.formats import EAD_APE
from glamconv.transformer.actions import TransformAction


class ApeEadSchemaDeclarationAdder(TransformAction):
    applicable_for = (EAD_APE,)
    uid = "ape-ead-schema-declarer"
    name = "Adding the Ape-EAD XML Schema declaration"
    category = "Supplementing"
    desc = (
        "This action adds, on the XML root element, the xsi:schemaLocation "
        "attribute that declares the Ape-EAD XML Schema, i.e. that gives a "
        "link towards the XML Schema."
    )

    def _execute(self, xml_root, logger, log_details):
        APE_EAD_SCHEMA_DECL = (
            "urn:isbn:1-931666-22-9 "
            "https://www.archivesportaleurope.net/schemas/ead/apeEAD.xsd"
        )
        XLINK_SCHEMA_DECL = (
            "http://www.w3.org/1999/xlink "
            "http://www.loc.gov/standards/xlink/xlink.xsd"
        )
        xml_root.set(
            f"{{{NS['xsi']}}}schemaLocation",
            f"{APE_EAD_SCHEMA_DECL} {XLINK_SCHEMA_DECL}",
        )
        logger.info(
            "The Ape-EAD XML Schema declaration has been added on the "
            "XML root element."
        )
        return xml_root
