# -*- coding: utf-8 -*-
import unittest

from lxml import etree
import datetime as dtm

from test import ActionTestCase
from glamconv.eac.required_elts_adders import (
    PlaceEntryAdder,
    AgencyCodeAdder,
    ExistDatesAdder,
)


DATA_EAC_CPF = """
<eac-cpf xmlns:xlink="http://www.w3.org/1999/xlink">
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


class TestPlaceEntryAdder(ActionTestCase):
    action_class = PlaceEntryAdder

    def test_no_agencycode_no_code_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><existDates><date>2022-08-01</date></existDates>"
                "<places><place><address><addressLine>TEST10</addressLine>"
                "</address></place></places></description>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "place")
        self.assertEqual(len(out_root[1][1][1][0]), 2)
        self.assertEqual(out_root[1][1][1][0][1].tag, "address")
        self.assertEqual(out_root[1][1][1][0][0].tag, "placeEntry")
        self.assertEqual(out_root[1][1][1][0][0].text, "unknown")

    def test_no_agencycode_with_code_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><existDates><date>2022-08-01</date></existDates>"
                "<places><place><address><addressLine>TEST10</addressLine>"
                "</address></place></places></description>"
            )
        )
        out_root = self.run_action(inp_root, {"default_value": "TEST20"})
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "place")
        self.assertEqual(len(out_root[1][1][1][0]), 2)
        self.assertEqual(out_root[1][1][1][0][1].tag, "address")
        self.assertEqual(out_root[1][1][1][0][0].tag, "placeEntry")
        self.assertEqual(out_root[1][1][1][0][0].text, "TEST20")

    def test_no_agencycode_with_placerole(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><existDates><date>2022-08-01</date></existDates>"
                "<places><place><placeRole>TEST20</placeRole>"
                "<address><addressLine>TEST10</addressLine></address>"
                "</place></places></description>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "place")
        self.assertEqual(len(out_root[1][1][1][0]), 3)
        self.assertEqual(out_root[1][1][1][0][2].tag, "address")
        self.assertEqual(out_root[1][1][1][0][0].tag, "placeRole")
        self.assertEqual(out_root[1][1][1][0][1].tag, "placeEntry")
        self.assertEqual(out_root[1][1][1][0][1].text, "unknown")

    def test_with_placeEntry(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><existDates><date>2022-08-01</date></existDates>"
                "<places><place><placeEntry>TEST10</placeEntry></place></places>"
                "</description>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "place")
        self.assertEqual(len(out_root[1][1][1][0]), 1)
        self.assertEqual(out_root[1][1][1][0][0].tag, "placeEntry")
        self.assertEqual(out_root[1][1][1][0][0].text, "TEST10")


class TestAgencyCodeAdder(ActionTestCase):
    action_class = AgencyCodeAdder

    def test_no_agencycode_no_code_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(len(out_root[0][2]), 2)
        self.assertEqual(out_root[0][2][1].tag, "agencyName")
        self.assertEqual(out_root[0][2][1].text, "TEST02")
        self.assertEqual(out_root[0][2][0].tag, "agencyCode")
        self.assertEqual(out_root[0][2][0].text, "XX-unknown")

    def test_no_agencycode_and_code_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        out_root = self.run_action(inp_root, {"default_value": "TEST10"})
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(len(out_root[0][2]), 2)
        self.assertEqual(out_root[0][2][1].tag, "agencyName")
        self.assertEqual(out_root[0][2][1].text, "TEST02")
        self.assertEqual(out_root[0][2][0].tag, "agencyCode")
        self.assertEqual(out_root[0][2][0].text, "TEST10")

    def test_with_agencycode(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0][2].insert(0, etree.fromstring("<agencyCode>TEST10</agencyCode>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(len(out_root[0][2]), 2)
        self.assertEqual(out_root[0][2][1].tag, "agencyName")
        self.assertEqual(out_root[0][2][1].text, "TEST02")
        self.assertEqual(out_root[0][2][0].tag, "agencyCode")
        self.assertEqual(out_root[0][2][0].text, "TEST10")


class TestExistDatesAdder(ActionTestCase):
    action_class = ExistDatesAdder

    def test_no_description_no_date_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][0].tag, "identity")
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 1)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][0][0].tag, "date")
        self.assertEqual(
            out_root[1][1][0][0].text, dtm.date.today().strftime("%Y-%m-%d")
        )

    def test_no_description_and_date_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        out_root = self.run_action(inp_root, {"default_value": "2022-08-01"})
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][0].tag, "identity")
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 1)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][0][0].tag, "date")
        self.assertEqual(out_root[1][1][0][0].text, "2022-08-01")

    def test_no_existdates_no_date_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><places><place><placeEntry>TEST10</placeEntry>"
                "</place></places></description>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][0].tag, "identity")
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][0][0].tag, "date")
        self.assertEqual(
            out_root[1][1][0][0].text, dtm.date.today().strftime("%Y-%m-%d")
        )

    def test_no_existdates_and_date_param(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><places><place><placeEntry>TEST10</placeEntry>"
                "</place></places></description>"
            )
        )
        out_root = self.run_action(inp_root, {"default_value": "2022-08-01"})
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][0].tag, "identity")
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][0][0].tag, "date")
        self.assertEqual(out_root[1][1][0][0].text, "2022-08-01")

    def test_with_existdates(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<description><existDates><date>2022-08-01</date></existDates>"
                "</description>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][0].tag, "identity")
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 1)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][0][0].tag, "date")
        self.assertEqual(out_root[1][1][0][0].text, "2022-08-01")


if __name__ == "__main__":
    unittest.main()
