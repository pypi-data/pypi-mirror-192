# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.namespacers import EadNamespaceAdder, EadNamespaceRemover


DATA_NAMESPACE_ADDER = """
<ead xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:dbk="http://docbook.org/ns/docbook">
  <eadheader>
    <eadid countrycode="FR" identifier="ID1" mainagencycode="LGLB-2022">LGLB-2022-ID1</eadid>
    <filedesc>
      <titlestmt>
        <titleproper>Example 1</titleproper>
      </titlestmt>
    </filedesc>
  </eadheader>
  <archdesc level="fonds">
    <did>
      <unitid>UID1</unitid>
      <unittitle>Exemple 1</unittitle>
      <unitdate>2016-2022</unitdate>
      <dao xlink:href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
  </archdesc>
  <dbk:para>Documentation in a specific namespace</dbk:para>
</ead>
"""


class TestEadNamespaceAdder(ActionTestCase):
    action_class = EadNamespaceAdder

    def test_namespace_adding(self):
        inp_root = etree.fromstring(DATA_NAMESPACE_ADDER)
        out_root = self.run_action(inp_root)
        expected_names = (
            "ead",
            "eadheader",
            "eadid",
            "filedesc",
            "titlestmt",
            "titleproper",
            "archdesc",
            "did",
            "unitid",
            "unittitle",
            "unitdate",
            "dao",
        )
        # EAD Elements are in the expected order and with the EAD namespace
        for (_, elt), exp_name in zip(
            etree.iterwalk(out_root, events=("start",)), expected_names
        ):
            self.assertEqual(elt.xpath("local-name()"), exp_name)
            self.assertEqual(elt.xpath("namespace-uri()"), "urn:isbn:1-931666-22-9")
        # Elements in a given namespace have still in the same namespace
        elt = out_root[2]
        self.assertEqual(elt.xpath("local-name()"), "para")
        self.assertEqual(elt.xpath("namespace-uri()"), "http://docbook.org/ns/docbook")
        # EAD Attributes have with no namespace
        elt = out_root[0][0]
        self.assertEqual(elt.xpath("local-name()"), "eadid")
        for name in elt.keys():
            self.assertTrue(name.startswith("{}") or not name.startswith("{"))
        # Attributes in a given namespace have still in the same namespace
        elt = out_root[1][0][3]
        self.assertEqual(elt.xpath("local-name()"), "dao")
        for name in elt.keys():
            self.assertTrue(name.startswith("{http://www.w3.org/1999/xlink}"))


DATA_NAMESPACE_REMOVER = """
<ead xmlns="urn:isbn:1-931666-22-9"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:dbk="http://docbook.org/ns/docbook">
  <eadheader>
    <eadid countrycode="FR" identifier="ID1" mainagencycode="LGLB-2022">LGLB-2022-ID1</eadid>
    <filedesc>
      <titlestmt>
        <titleproper>Example 1</titleproper>
      </titlestmt>
    </filedesc>
  </eadheader>
  <archdesc level="fonds">
    <did>
      <unitid>UID1</unitid>
      <unittitle>Exemple 1</unittitle>
      <unitdate>2016-2022</unitdate>
      <dao xlink:href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
  </archdesc>
  <dbk:para>Documentation in a specific namespace</dbk:para>
</ead>
"""


class TestEadNamespaceRemover(ActionTestCase):
    action_class = EadNamespaceRemover

    def test_namespace_removing(self):
        inp_root = etree.fromstring(DATA_NAMESPACE_REMOVER)
        out_root = self.run_action(inp_root)
        expected_names = (
            "ead",
            "eadheader",
            "eadid",
            "filedesc",
            "titlestmt",
            "titleproper",
            "archdesc",
            "did",
            "unitid",
            "unittitle",
            "unitdate",
            "dao",
        )
        # EAD Elements are in the expected order and have no namespace
        for (_, elt), exp_name in zip(
            etree.iterwalk(out_root, events=("start",)), expected_names
        ):
            self.assertEqual(elt.xpath("local-name()"), exp_name)
            self.assertEqual(elt.xpath("namespace-uri()"), "")
        # Elements in a given namespace have still in the same namespace
        elt = out_root[2]
        self.assertEqual(elt.xpath("local-name()"), "para")
        self.assertEqual(elt.xpath("namespace-uri()"), "http://docbook.org/ns/docbook")
        # EAD Attributes have with no namespace
        elt = out_root[0][0]
        self.assertEqual(elt.xpath("local-name()"), "eadid")
        for name in elt.keys():
            self.assertTrue(name.startswith("{}") or not name.startswith("{"))
        # Attributes in a given namespace have still in the same namespace
        elt = out_root[1][0][3]
        self.assertEqual(elt.xpath("local-name()"), "dao")
        for name in elt.keys():
            self.assertTrue(name.startswith("{http://www.w3.org/1999/xlink}"))


if __name__ == "__main__":
    unittest.main()
