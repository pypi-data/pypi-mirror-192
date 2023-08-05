# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.eac.supplementers import ApeEacSchemaDeclarationAdder


DATA_EAC_APE = """
<eac-cpf xmlns="urn:isbn:1-931666-33-4"
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


class TestApeEacSchemaDeclarer(ActionTestCase):
    action_class = ApeEacSchemaDeclarationAdder

    def test_schema_declaration(self):
        inp_root = etree.fromstring(DATA_EAC_APE)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root.tag, "{urn:isbn:1-931666-33-4}eac-cpf")
        decl = out_root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
        self.assertEqual(
            decl,
            "urn:isbn:1-931666-33-4 "
            "http://www.archivesportaleurope.net/Portal/profiles/apeEAC-CPF.xsd "
            "http://www.w3.org/1999/xlink "
            "http://www.loc.gov/standards/xlink/xlink.xsd",
        )


if __name__ == "__main__":
    unittest.main()
