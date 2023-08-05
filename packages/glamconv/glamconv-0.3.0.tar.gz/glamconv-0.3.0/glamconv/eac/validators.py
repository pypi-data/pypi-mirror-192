# -*- coding: utf-8 -*-

from os import path as osp
from lxml import etree
from glamconv.transformer.actions import ValidateAction


EAC_CPF_DIR = osp.join(osp.abspath(osp.dirname(__file__)), "eac-cpf-schema")
EAC_CPF_SCHEMA_XML = etree.parse(osp.join(EAC_CPF_DIR, "cpf.xsd"))
EAC_CPF_SCHEMA = etree.XMLSchema(EAC_CPF_SCHEMA_XML)

EAC_APE_DIR = osp.join(osp.abspath(osp.dirname(__file__)), "ape-eac-schema")
EAC_APE_SCHEMA_XML = etree.parse(osp.join(EAC_APE_DIR, "apeEAC-CPF.xsd"))
EAC_APE_SCHEMA = etree.XMLSchema(EAC_APE_SCHEMA_XML)


class EacCpfValidator(ValidateAction):
    uid = "eac-cpf-validator"
    name = "Validating XML data in EAC-CPF format"
    desc = "This action validates XML data against the EAC-CPF XML Schema."

    def _execute(self, xml_root, logger, log_details):
        result = EAC_CPF_SCHEMA.validate(xml_root)
        if result is False:
            error_list = [
                f"Line {err.line}: {err.message}" for err in EAC_CPF_SCHEMA.error_log
            ]
            err_num = len(error_list)
            if err_num > 100:
                error_list = error_list[:100]
                error_list.append(f"... and {(err_num - 100):d} more errors! ...")
            logger.error(
                "The XML data doesn't comply with the constraints defined in "
                "the EAC-CPF standard (XML Schema). The following validation "
                "errors have been found:",
                "\n".join(error_list),
            )
        else:
            logger.info("The XML data complies with the EAC-CPF standard (XML Schema).")
        return result


class EacApeValidator(ValidateAction):
    uid = "eac-ape-validator"
    name = "Validating XML data in Ape-EAC format"
    desc = "This action validates XML data against the Ape-EAC XML Schema."

    def _execute(self, xml_root, logger, log_details):
        result = EAC_APE_SCHEMA.validate(xml_root)
        if result is False:
            error_list = [
                f"Line {err.line}: {err.message}" for err in EAC_APE_SCHEMA.error_log
            ]
            err_num = len(error_list)
            if err_num > 100:
                error_list = error_list[:100]
                error_list.append(f"... and {(err_num - 100):d} more errors! ...")
            logger.error(
                "The XML data doesn't comply with the constraints defined in "
                "the Ape-EAC standard (XML Schema). The following validation "
                "errors have been found:",
                "\n".join(error_list),
            )
        else:
            logger.info("The XML data complies with the Ape-EAC standard (XML Schema).")
        return result
