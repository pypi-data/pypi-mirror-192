# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.eac.adjusters import (
    LocalTypeAttributeAdjuster,
    DescriptionChildrenMover,
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
    <description>
      <existDates>
        <date>2022-08-01</date>
      </existDates>
    </description>
  </cpfDescription>
</eac-cpf>
"""


class TestLocalTypeAttributeAdjuster(ActionTestCase):
    action_class = LocalTypeAttributeAdjuster

    def test_address_localtype(self):
        for att_val in ("postal address", "other", "visitors address"):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].append(
                    etree.fromstring(
                        "<places><place><placeEntry>TEST10</placeEntry><address>"
                        "<addressLine>TEST11</addressLine></address></place>"
                        "</places>"
                    )
                )
                inp_root[1][1][1][0][1].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1][0][1].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][1].append(
                etree.fromstring(
                    "<places><place><placeEntry>TEST10</placeEntry>"
                    "<address><addressLine>TEST11</addressLine></address></place>"
                    "</places>"
                )
            )
            inp_root[1][1][1][0][1].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][1][1][0][1].get("localType"), "other")

    def test_addressline_localtype(self):
        for att_val in (
            "street",
            "other",
            "postalcode",
            "localentity",
            "firstdem",
            "secondem",
            "country",
        ):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].append(
                    etree.fromstring(
                        "<places><place><placeEntry>TEST10</placeEntry>"
                        "<address><addressLine>TEST11</addressLine></address>"
                        "</place></places>"
                    )
                )
                inp_root[1][1][1][0][1][0].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1][0][1][0].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][1].append(
                etree.fromstring(
                    "<places><place><placeEntry>TEST10</placeEntry>"
                    "<address><addressLine>TEST11</addressLine></address></place>"
                    "</places>"
                )
            )
            inp_root[1][1][1][0][1][0].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][1][1][0][1][0].get("localType"), "other")

    def test_date_localtype(self):
        for att_val in ("unknown", "open", "unknownEnd", "unknownStart"):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].append(
                    etree.fromstring(
                        "<places><place><placeEntry>TEST10</placeEntry>"
                        "<date>2022-08-01</date></place></places>"
                    )
                )
                inp_root[1][1][1][0][1].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1][0][1].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][1].append(
                etree.fromstring(
                    "<places><place><placeEntry>TEST10</placeEntry>"
                    "<date>2022-08-01</date></place></places>"
                )
            )
            inp_root[1][1][1][0][1].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][1][1][0][1].get("localType"), "unknown")

    def test_daterange_localtype(self):
        for att_val in ("unknown", "open", "unknownEnd", "unknownStart"):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].append(
                    etree.fromstring(
                        "<places><place><placeEntry>TEST10</placeEntry>"
                        "<dateRange><fromDate>2022-08-01</fromDate>"
                        "<toDate>2022-08-05</toDate></dateRange></place></places>"
                    )
                )
                inp_root[1][1][1][0][1].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1][0][1].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][1].append(
                etree.fromstring(
                    "<places><place><placeEntry>TEST10</placeEntry>"
                    "<dateRange><fromDate>2022-08-01</fromDate>"
                    "<toDate>2022-08-05</toDate></dateRange></place></places>"
                )
            )
            inp_root[1][1][1][0][1].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][1][1][0][1].get("localType"), "unknown")

    def test_nameentry_localtype(self):
        for att_val in (
            "abbreviation",
            "other",
            "authorized",
            "alternative",
            "preferred",
        ):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][0][1].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][1].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][0][1].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][0][1].get("localType"), "other")

    def test_nameentryparallel_localtype(self):
        for att_val in (
            "abbreviation",
            "other",
            "authorized",
            "alternative",
            "preferred",
        ):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][0].remove(inp_root[1][0][1])
                inp_root[1][0].append(
                    etree.fromstring(
                        "<nameEntryParallel><nameEntry><part>TEST10</part>"
                        "</nameEntry><nameEntry><part>TEST11</part></nameEntry>"
                        "</nameEntryParallel>"
                    )
                )
                inp_root[1][0][1].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][1].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][0].remove(inp_root[1][0][1])
            inp_root[1][0].append(
                etree.fromstring(
                    "<nameEntryParallel><nameEntry><part>TEST10</part></nameEntry>"
                    "<nameEntry><part>TEST11</part></nameEntry></nameEntryParallel>"
                )
            )
            inp_root[1][0][1].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][0][1].get("localType"), "other")

    def test_part_localtype(self):
        for att_val in (
            "posttitle",
            "infixtitle",
            "suffix",
            "legalform",
            "persname",
            "pretitle",
            "initials",
            "patronymic",
            "title",
            "firstname",
            "alias",
            "birthname",
            "corpname",
            "prefix",
            "famname",
            "surname",
            "infix",
        ):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][0][1][0].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][1][0].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][0][1][0].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][0][1][0].get("localType"), "title")

    def test_placeentry_localtype(self):
        for att_val in (
            "death",
            "birth",
            "other",
            "foundation",
            "private-residence",
            "business-residence",
            "suppression",
        ):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].append(
                    etree.fromstring(
                        "<places><place><placeEntry>TEST10</placeEntry></place>"
                        "</places>"
                    )
                )
                inp_root[1][1][1][0][0].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1][0][0].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1][1].append(
                etree.fromstring(
                    "<places><place><placeEntry>TEST10</placeEntry></place>" "</places>"
                )
            )
            inp_root[1][1][1][0][0].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][1][1][0][0].get("localType"), "other")

    def test_relationentry_localtype(self):
        for att_val in ("agencyCode", "agencyName", "title", "id"):
            with self.subTest(localtype_value=att_val):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<relations><cpfRelation>"
                        "<relationEntry>TEST10</relationEntry></cpfRelation>"
                        "</relations>"
                    )
                )
                inp_root[1][2][0][0].set("localType", att_val)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][2][0][0].get("localType"), att_val)
        with self.subTest(localtype_value="TEST100"):
            inp_root = etree.fromstring(DATA_EAC_CPF)
            inp_root[1].append(
                etree.fromstring(
                    "<relations><cpfRelation><relationEntry>TEST10</relationEntry>"
                    "</cpfRelation></relations>"
                )
            )
            inp_root[1][2][0][0].set("localType", "TEST100")
            out_root = self.run_action(inp_root)
            self.assertEqual(out_root[1][2][0][0].get("localType"), "title")


class TestDescriptionChildrenMover(ActionTestCase):
    action_class = DescriptionChildrenMover

    def test_children_no_children_parent(self):
        for elt_name, parent_name in (
            ("function", "functions"),
            ("legalStatus", "legalStatuses"),
            ("localDescription", "localDescriptions"),
            ("mandate", "mandates"),
            ("occupation", "occupations"),
        ):
            with self.subTest(elt_name=elt_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                for num in range(10, 13):
                    inp_root[1][1].append(
                        etree.fromstring(
                            f"<{elt_name}><term>TEST{num}</term></{elt_name}>"
                        )
                    )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "description")
                self.assertEqual(len(out_root[1][1]), 2)
                self.assertEqual(out_root[1][1][0].tag, "existDates")
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 3)
                for idx in range(3):
                    self.assertEqual(out_root[1][1][1][idx].tag, elt_name)
                    self.assertEqual(out_root[1][1][1][idx][0].tag, "term")
                    self.assertEqual(out_root[1][1][1][idx][0].text, f"TEST{10 + idx}")

    def test_children_with_children_parent(self):
        for elt_name, parent_name in (
            ("function", "functions"),
            ("legalStatus", "legalStatuses"),
            ("localDescription", "localDescriptions"),
            ("mandate", "mandates"),
            ("occupation", "occupations"),
        ):
            with self.subTest(elt_name=elt_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                for num in range(10, 13):
                    inp_root[1][1].append(
                        etree.fromstring(
                            f"<{elt_name}><term>TEST{num}</term></{elt_name}>"
                        )
                    )
                inp_root[1][1].insert(
                    2,
                    etree.fromstring(
                        f"<{parent_name}><{elt_name}><term>TEST100</term>"
                        f"</{elt_name}></{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "description")
                self.assertEqual(len(out_root[1][1]), 3)
                self.assertEqual(out_root[1][1][0].tag, "existDates")
                self.assertEqual(out_root[1][1][2].tag, parent_name)
                self.assertEqual(len(out_root[1][1][2]), 1)
                self.assertEqual(out_root[1][1][2][0].tag, elt_name)
                self.assertEqual(out_root[1][1][2][0][0].tag, "term")
                self.assertEqual(out_root[1][1][2][0][0].text, "TEST100")
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 3)
                for idx in range(3):
                    self.assertEqual(out_root[1][1][1][idx].tag, elt_name)
                    self.assertEqual(out_root[1][1][1][idx][0].tag, "term")
                    self.assertEqual(out_root[1][1][1][idx][0].text, f"TEST{10 + idx}")

    def test_languageused_no_languagesused(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        for num in range(10, 13):
            inp_root[1][1].append(
                etree.fromstring(
                    "<languageUsed>"
                    f"<language languageCode='eng'>TEST{num}</language>"
                    f"<script scriptCode='Engl'>TEST{num + 10}</script>"
                    "</languageUsed>"
                )
            )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][1].tag, "languagesUsed")
        self.assertEqual(len(out_root[1][1][1]), 3)
        for idx in range(3):
            self.assertEqual(out_root[1][1][1][idx].tag, "languageUsed")
            self.assertEqual(out_root[1][1][1][idx][0].tag, "language")
            self.assertEqual(out_root[1][1][1][idx][0].text, f"TEST{10 + idx}")
            self.assertEqual(out_root[1][1][1][idx][1].tag, "script")
            self.assertEqual(out_root[1][1][1][idx][1].text, f"TEST{20 + idx}")

    def test_languageused_with_languagesused(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        for num in range(10, 13):
            inp_root[1][1].append(
                etree.fromstring(
                    "<languageUsed>"
                    f"<language languageCode='eng'>TEST{num}</language>"
                    f"<script scriptCode='Engl'>TEST{num + 10}</script>"
                    "</languageUsed>"
                )
            )
        inp_root[1][1].insert(
            2,
            etree.fromstring(
                "<languagesUsed><languageUsed>"
                "<language languageCode='eng'>TEST40</language>"
                "<script scriptCode='Engl'>TEST41</script></languageUsed>"
                "</languagesUsed>"
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 3)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][2].tag, "languagesUsed")
        self.assertEqual(out_root[1][1][2][0].tag, "languageUsed")
        self.assertEqual(out_root[1][1][2][0][0].tag, "language")
        self.assertEqual(out_root[1][1][2][0][0].text, "TEST40")
        self.assertEqual(out_root[1][1][2][0][1].tag, "script")
        self.assertEqual(out_root[1][1][2][0][1].text, "TEST41")
        self.assertEqual(out_root[1][1][1].tag, "languagesUsed")
        self.assertEqual(len(out_root[1][1][1]), 3)
        for idx in range(3):
            self.assertEqual(out_root[1][1][1][idx].tag, "languageUsed")
            self.assertEqual(out_root[1][1][1][idx][0].tag, "language")
            self.assertEqual(out_root[1][1][1][idx][0].text, f"TEST{10 + idx}")
            self.assertEqual(out_root[1][1][1][idx][1].tag, "script")
            self.assertEqual(out_root[1][1][1][idx][1].text, f"TEST{20 + idx}")

    def test_place_no_places(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        for num in range(10, 13):
            inp_root[1][1].append(
                etree.fromstring(f"<place><placeEntry>TEST{num}</placeEntry></place>")
            )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(len(out_root[1][1][1]), 3)
        for idx in range(3):
            self.assertEqual(out_root[1][1][1][idx].tag, "place")
            self.assertEqual(out_root[1][1][1][idx][0].tag, "placeEntry")
            self.assertEqual(out_root[1][1][1][idx][0].text, f"TEST{10 + idx}")

    def test_place_with_places(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        for num in range(10, 13):
            inp_root[1][1].append(
                etree.fromstring(f"<place><placeEntry>TEST{num}</placeEntry></place>")
            )
        inp_root[1][1].insert(
            2,
            etree.fromstring(
                "<places><place><placeEntry>TEST40</placeEntry></place></places>"
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "description")
        self.assertEqual(len(out_root[1][1]), 3)
        self.assertEqual(out_root[1][1][0].tag, "existDates")
        self.assertEqual(out_root[1][1][2].tag, "places")
        self.assertEqual(out_root[1][1][2][0].tag, "place")
        self.assertEqual(out_root[1][1][2][0][0].tag, "placeEntry")
        self.assertEqual(out_root[1][1][2][0][0].text, "TEST40")
        self.assertEqual(out_root[1][1][1].tag, "places")
        self.assertEqual(len(out_root[1][1][1]), 3)
        for idx in range(3):
            self.assertEqual(out_root[1][1][1][idx].tag, "place")
            self.assertEqual(out_root[1][1][1][idx][0].tag, "placeEntry")
            self.assertEqual(out_root[1][1][1][idx][0].text, f"TEST{10 + idx}")


if __name__ == "__main__":
    unittest.main()
