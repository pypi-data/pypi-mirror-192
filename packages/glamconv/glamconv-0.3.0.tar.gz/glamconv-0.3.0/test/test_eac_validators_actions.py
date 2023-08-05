# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.eac.validators import EacCpfValidator, EacApeValidator

EAC_NAMESPACE = "urn:isbn:1-931666-33-4"

DATA_EAC_CPF_VALIDATOR = f"""
<eac-cpf xmlns="{EAC_NAMESPACE}"
         xmlns:xlink="http://www.w3.org/1999/xlink">
  <control>
    <recordId>TEST01</recordId>
    <maintenanceStatus>new</maintenanceStatus>
    <maintenanceAgency>
      <agencyName>TEST02</agencyName>
    </maintenanceAgency>
    <maintenanceHistory>
      <maintenanceEvent>
        <eventType>created</eventType>
        <eventDateTime>2022-09-01</eventDateTime>
        <agentType>human</agentType>
        <agent>TEST03</agent>
      </maintenanceEvent>
    </maintenanceHistory>
  </control>
  <cpfDescription>
    <identity>
      <entityType>person</entityType>
      <nameEntry>
        <part>TEST04</part>
      </nameEntry>
    </identity>
  </cpfDescription>
</eac-cpf>
"""

DATA_EAC_APE_VALIDATOR = f"""
<eac-cpf xmlns="{EAC_NAMESPACE}"
         xmlns:xlink="http://www.w3.org/1999/xlink">
  <control>
    <recordId>TEST01</recordId>
    <maintenanceStatus>new</maintenanceStatus>
    <maintenanceAgency>
      <agencyCode>FR-LGLB2022</agencyCode>
      <agencyName>TEST02</agencyName>
    </maintenanceAgency>
    <maintenanceHistory>
      <maintenanceEvent>
        <eventType>created</eventType>
        <eventDateTime>2022-09-01</eventDateTime>
        <agentType>human</agentType>
        <agent>TEST03</agent>
      </maintenanceEvent>
    </maintenanceHistory>
  </control>
  <cpfDescription>
    <identity>
      <entityType>person</entityType>
      <nameEntry>
        <part>TEST04</part>
      </nameEntry>
    </identity>
    <description>
      <existDates>
        <date>2022-09-01</date>
      </existDates>
    </description>
  </cpfDescription>
</eac-cpf>
"""


class TestEacCpfValidator(ActionTestCase):
    action_class = EacCpfValidator

    def test_valid_document(self):
        inp_root = etree.fromstring(DATA_EAC_CPF_VALIDATOR)
        out = self.run_action(inp_root)
        self.assertTrue(out)

    def test_invalid_document_no_nameentry(self):
        inp_root = etree.fromstring(DATA_EAC_CPF_VALIDATOR)
        inp_root[1][0].remove(inp_root[1][0][1])
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_document_empty_description(self):
        inp_root = etree.fromstring(DATA_EAC_CPF_VALIDATOR)
        inp_root[1].append(etree.Element(f"{{{EAC_NAMESPACE}}}description"))
        out = self.run_action(inp_root)
        self.assertTrue(out)


class TestEacApeValidator(ActionTestCase):
    action_class = EacApeValidator

    def test_valid_document(self):
        inp_root = etree.fromstring(DATA_EAC_APE_VALIDATOR)
        out = self.run_action(inp_root)
        self.assertTrue(out)

    def test_invalid_document_no_nameentry(self):
        inp_root = etree.fromstring(DATA_EAC_APE_VALIDATOR)
        inp_root[1][0].remove(inp_root[1][0][1])
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_invalid_document_no_agencycode(self):
        inp_root = etree.fromstring(DATA_EAC_APE_VALIDATOR)
        inp_root[0][2].remove(inp_root[0][2][0])
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_invalid_document_wrong_agencycode(self):
        inp_root = etree.fromstring(DATA_EAC_APE_VALIDATOR)
        inp_root[0][2][0].text = "TEST101"
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_invalid_document_empty_description(self):
        inp_root = etree.fromstring(DATA_EAC_APE_VALIDATOR)
        inp_root[1][1].remove(inp_root[1][1][0])
        out = self.run_action(inp_root)
        self.assertFalse(out)


if __name__ == "__main__":
    unittest.main()
