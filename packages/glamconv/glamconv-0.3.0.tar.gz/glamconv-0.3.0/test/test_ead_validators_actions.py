# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.validators import Ead2002Validator, ApeEadValidator


DATA_APE_EAD_VALIDATOR = """
<ead {default_ns}
     xmlns:xlink="http://www.w3.org/1999/xlink">
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
</ead>
"""


class TestApeEadValidator(ActionTestCase):
    action_class = ApeEadValidator

    def test_valid_document(self):
        data = DATA_APE_EAD_VALIDATOR.format(
            default_ns='xmlns="urn:isbn:1-931666-22-9"'
        )
        inp_root = etree.fromstring(data)
        out = self.run_action(inp_root)
        self.assertTrue(out)

    def test_invalid_document_empty_did(self):
        data = DATA_APE_EAD_VALIDATOR.format(
            default_ns='xmlns="urn:isbn:1-931666-22-9"'
        )
        inp_root = etree.fromstring(data)
        inp_root[1].append(etree.Element("{urn:isbn:1-931666-22-9}did"))
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_invalid_document_incorrect_mainagencycode(self):
        data = DATA_APE_EAD_VALIDATOR.format(
            default_ns='xmlns="urn:isbn:1-931666-22-9"'
        )
        inp_root = etree.fromstring(data)
        inp_root[0][0].set("mainagencycode", "LGLB")
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_invalid_document_no_namespace(self):
        data = DATA_APE_EAD_VALIDATOR.format(default_ns="")
        inp_root = etree.fromstring(data)
        out = self.run_action(inp_root)
        self.assertFalse(out)


DATA_EAD_2002_VALIDATOR = """
<ead>
  <eadheader>
    <eadid>LGLB-2022-ID1</eadid>
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
      <dao href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
  </archdesc>
</ead>
"""


class TestEad2002Validator(ActionTestCase):
    action_class = Ead2002Validator

    def test_valid_document(self):
        inp_root = etree.fromstring(DATA_EAD_2002_VALIDATOR)
        out = self.run_action(inp_root)
        self.assertTrue(out)

    def test_invalid_document_empty_did(self):
        inp_root = etree.fromstring(DATA_EAD_2002_VALIDATOR)
        inp_root[1].append(etree.Element("did"))
        out = self.run_action(inp_root)
        self.assertFalse(out)

    def test_invalid_document_incorrect_audience(self):
        inp_root = etree.fromstring(DATA_EAD_2002_VALIDATOR)
        inp_root[0].set("audience", "INCORRECT_VALUE")
        out = self.run_action(inp_root)
        self.assertFalse(out)


if __name__ == "__main__":
    unittest.main()
