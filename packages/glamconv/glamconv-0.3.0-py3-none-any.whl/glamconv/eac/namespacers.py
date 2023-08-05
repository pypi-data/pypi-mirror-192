# -*- coding: utf-8 -*-
"""
Module containing actions that modify the namespace of the XML elements.
"""

from lxml import etree
from glamconv.utils import NS, split_qname
from glamconv.eac.formats import EAC_CPF, EAC_APE
from glamconv.transformer.actions import TransformAction


class EacCpfNamespaceAdder(TransformAction):
    applicable_for = (EAC_CPF, EAC_APE)
    uid = "eac-cpf-namespace-adder"
    name = "Adding the EAC-CPF / Ape-EAC namespace"
    category = "Naming"
    desc = (
        "This action puts all the XML elements with an empty namespace "
        "inside the Ape-EAC / EAC-CPF standard namespace (it's the same one). "
        "The attribute names are not changed. All the other actions designed "
        "for EAC-CPF documents expect the elements to have an empty namespace. "
        "Therefore, be sure to run this action at the end of the "
        "transformation, just before the Ape-EAC validation."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        for elt in xml_root.iter(etree.Element):
            namespace, local_name = split_qname(elt.tag)
            if namespace is None:
                elt.tag = f"{{{NS['cpf']}}}{local_name}"
                count += 1
        if count > 0:
            logger.info(
                f"{count:d} elements with an empty namespace have been "
                "transfered in Ape-EAC / EAC-CPF namespace"
            )
        return xml_root


class EacCpfNamespaceRemover(TransformAction):
    applicable_for = (EAC_CPF, EAC_APE)
    uid = "eac-cpf-namespace-remover"
    name = "Removing the EAC-CPF / Ape-EAC namespace"
    category = "Naming"
    desc = (
        "This action puts all the XML elements with the EAC-CPF / Ape-EAC "
        "standard namespace (it's the same one) inside the empty namespace. "
        "The attribute names are not changed. This action does the opposite "
        "of the action that adds the Ape-EAC / EAC-CPF namespace to the XML "
        "elements."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        for elt in xml_root.iter(etree.Element):
            namespace, local_name = split_qname(elt.tag)
            if namespace == NS["cpf"]:
                elt.tag = f"{{}}{local_name}"
                count += 1
        if count > 0:
            logger.info(
                f"{count:d} elements with the EAC-CPF / Ape-EAC namespace have "
                "been transfered in the empty namespace"
            )
        return xml_root
