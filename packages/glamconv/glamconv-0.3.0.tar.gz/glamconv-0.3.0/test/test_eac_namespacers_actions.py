# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.eac.namespacers import (
    EacCpfNamespaceAdder,
    EacCpfNamespaceRemover,
)


DATA_EAC_CPF = """
<eac-cpf {default_namespace}
         xmlns:xlink="http://www.w3.org/1999/xlink"
         xmlns:dbk="http://docbook.org/ns/docbook">
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
      <nameEntry localType="preferred">
        <part>TEST04</part>
      </nameEntry>
    </identity>
    <description>
      <existDates>
        <date>2022-08-01</date>
      </existDates>
    </description>
    <biogHist>
      <citation xlink:href="TEST05.a">TEST05</citation>
    </biogHist>
  </cpfDescription>
  <dbk:para>Documentation in a specific namespace</dbk:para>
</eac-cpf>
"""


class TestEacCpfNamespaceAdder(ActionTestCase):
    action_class = EacCpfNamespaceAdder

    def test_namespace_adding(self):
        inp_root = etree.fromstring(DATA_EAC_CPF.format(default_namespace=""))
        out_root = self.run_action(inp_root)
        expected_names = (
            "eac-cpf",
            "control",
            "recordId",
            "maintenanceStatus",
            "maintenanceAgency",
            "agencyName",
            "maintenanceHistory",
            "maintenanceEvent",
            "eventType",
            "eventDateTime",
            "agentType",
            "agent",
            "cpfDescription",
            "identity",
            "entityType",
            "nameEntry",
            "part",
            "description",
            "existDates",
            "date",
            "biogHist",
            "citation",
        )
        # EAC Elements are in the expected order and with the EAC namespace
        for (_, elt), exp_name in zip(
            etree.iterwalk(out_root, events=("start",)), expected_names
        ):
            loc_name = elt.xpath("local-name()")
            if loc_name != "para":
                self.assertEqual(loc_name, exp_name)
                self.assertEqual(elt.xpath("namespace-uri()"), "urn:isbn:1-931666-33-4")
        # Elements in a given namespace have still in the same namespace
        elt = out_root[2]
        self.assertEqual(elt.xpath("local-name()"), "para")
        self.assertEqual(elt.xpath("namespace-uri()"), "http://docbook.org/ns/docbook")
        # EAC Attributes have  no namespace
        elt = out_root[1][0][1]
        self.assertEqual(elt.xpath("local-name()"), "nameEntry")
        for name in elt.keys():
            self.assertTrue(name.startswith("{}") or not name.startswith("{"))
        # Attributes in a given namespace have still in the same namespace
        elt = out_root[1][2][0]
        self.assertEqual(elt.xpath("local-name()"), "citation")
        for name in elt.keys():
            self.assertTrue(name.startswith("{http://www.w3.org/1999/xlink}"))


class TestEacCpfNamespaceRemover(ActionTestCase):
    action_class = EacCpfNamespaceRemover

    def test_namespace_removing(self):
        inp_root = etree.fromstring(
            DATA_EAC_CPF.format(default_namespace='xmlns="urn:isbn:1-931666-33-4"')
        )
        out_root = self.run_action(inp_root)
        expected_names = (
            "eac-cpf",
            "control",
            "recordId",
            "maintenanceStatus",
            "maintenanceAgency",
            "agencyName",
            "maintenanceHistory",
            "maintenanceEvent",
            "eventType",
            "eventDateTime",
            "agentType",
            "agent",
            "cpfDescription",
            "identity",
            "entityType",
            "nameEntry",
            "part",
            "description",
            "existDates",
            "date",
            "biogHist",
            "citation",
        )
        # EAC Elements are in the expected order and with the EAC namespace
        for (_, elt), exp_name in zip(
            etree.iterwalk(out_root, events=("start",)), expected_names
        ):
            loc_name = elt.xpath("local-name()")
            if loc_name != "para":
                self.assertEqual(loc_name, exp_name)
                self.assertEqual(elt.xpath("namespace-uri()"), "")
        # Elements in a given namespace have still in the same namespace
        elt = out_root[2]
        self.assertEqual(elt.xpath("local-name()"), "para")
        self.assertEqual(elt.xpath("namespace-uri()"), "http://docbook.org/ns/docbook")
        # EAC Attributes have  no namespace
        elt = out_root[1][0][1]
        self.assertEqual(elt.xpath("local-name()"), "nameEntry")
        for name in elt.keys():
            self.assertTrue(name.startswith("{}") or not name.startswith("{"))
        # Attributes in a given namespace have still in the same namespace
        elt = out_root[1][2][0]
        self.assertEqual(elt.xpath("local-name()"), "citation")
        for name in elt.keys():
            self.assertTrue(name.startswith("{http://www.w3.org/1999/xlink}"))


if __name__ == "__main__":
    unittest.main()
