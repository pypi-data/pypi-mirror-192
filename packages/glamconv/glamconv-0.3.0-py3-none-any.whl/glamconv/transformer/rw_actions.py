# -*- coding: utf-8 -*-
"""
Module defining basic read / write actions
"""

from lxml import etree

from glamconv.transformer.actions import ReadAction, WriteAction
from glamconv.utils import NS, split_qname


class XmlReader(ReadAction):
    uid = "xml-reader"
    name = "Reading of an XML file"
    desc = "This action reads an XML file and returns the XML data it contains."

    def _execute(self, input_flow, logger, log_details):
        if isinstance(input_flow, etree._Element):
            return input_flow
        if isinstance(input_flow, etree._ElementTree):
            return input_flow.getroot()
        tree = etree.parse(input_flow)
        xml_root = tree.getroot()
        return xml_root


class XmlWriter(WriteAction):
    uid = "xml-writer"
    name = "Writing an XML file"
    desc = "This action writes the XML data it receives into an XML file."

    def _execute(self, xml_root, logger, log_details):
        root_ns, _ = split_qname(xml_root.tag)
        if root_ns not in (NS["ead"], NS["cpf"]):
            new_root = xml_root
        else:
            # Beautify namespaces in output: use the namespace of the root
            # element as the default namespace
            nsmap = {prfx: nmsp for prfx, nmsp in NS.items() if nmsp != root_ns}
            nsmap[None] = root_ns
            new_root = etree.Element(xml_root.tag, nsmap=nsmap)
            new_root.text = xml_root.text
            new_root.tail = xml_root.tail
            for att, val in xml_root.attrib.items():
                new_root.set(att, val)
            new_root[:] = xml_root[:]
        # Return the XML root element serialization
        return etree.tostring(
            new_root, encoding="UTF-8", xml_declaration=True, pretty_print=True
        )
