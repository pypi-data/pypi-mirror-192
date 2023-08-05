# -*- coding: utf-8 -*-
"""
Module defining the formats for Ape-EAC and EAC-CPF (instances of
:class:`~glamconv.transformer.formats.DataFormat`)
"""

from glamconv.transformer.formats import DataFormat
from glamconv.transformer.rw_actions import XmlReader, XmlWriter
from glamconv.eac.validators import EacCpfValidator, EacApeValidator


EAC_CPF = DataFormat(
    "eac-cpf",
    "XML / EAC-CPF",
    "text/xml",
    ".xml",
    "XML data complying with the EAC-CPF standard as defined in the EAC-CPF "
    "XML Schema",
)
XmlReader.applicable_for.add(EAC_CPF)
XmlWriter.applicable_for.add(EAC_CPF)
EacCpfValidator.applicable_for.add(EAC_CPF)
EAC_CPF.reading_class = XmlReader
EAC_CPF.writing_class = XmlWriter
EAC_CPF.validating_class = EacCpfValidator

EAC_APE = DataFormat(
    "eac-ape",
    "XML / Ape-EAC",
    "text/xml",
    ".xml",
    "XML data complying with the Ape-EAC standard as defined in the Ape-EAC "
    "XML Schema",
)
XmlReader.applicable_for.add(EAC_APE)
XmlWriter.applicable_for.add(EAC_APE)
EacApeValidator.applicable_for.add(EAC_APE)
EAC_APE.reading_class = XmlReader
EAC_APE.writing_class = XmlWriter
EAC_APE.validating_class = EacApeValidator
