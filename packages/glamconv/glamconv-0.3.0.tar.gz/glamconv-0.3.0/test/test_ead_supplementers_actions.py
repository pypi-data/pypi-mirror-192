# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.supplementers import ApeEadSchemaDeclarationAdder


DATA_APE_EAD = """
<ead xmlns="urn:isbn:1-931666-22-9"
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


class TestApeEadSchemaDeclarer(ActionTestCase):
    action_class = ApeEadSchemaDeclarationAdder

    def test_schema_declaration(self):
        inp_root = etree.fromstring(DATA_APE_EAD)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root.tag, "{urn:isbn:1-931666-22-9}ead")
        decl = out_root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
        self.assertEqual(
            decl,
            "urn:isbn:1-931666-22-9 "
            "https://www.archivesportaleurope.net/schemas/ead/apeEAD.xsd "
            "http://www.w3.org/1999/xlink "
            "http://www.loc.gov/standards/xlink/xlink.xsd",
        )


if __name__ == "__main__":
    unittest.main()
