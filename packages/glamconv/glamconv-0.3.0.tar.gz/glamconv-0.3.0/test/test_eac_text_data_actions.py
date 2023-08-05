# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.eac.text_data import (
    SpanConverter,
    BioghistListOutlineConverter,
    GeneralcontextListCitationConverter,
    DescriptionChildrenTextElementsConverter,
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
      <biogHist>
        <abstract>TEST10</abstract>
        <citation>TEST11</citation>
        <p>TEST12</p>
      </biogHist>
    </description>
  </cpfDescription>
</eac-cpf>
"""


class TestSpanConverter(ActionTestCase):
    action_class = SpanConverter

    def test_span_in_p(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][1][1].append(
            etree.fromstring(
                "<p>TEST20 <span>TEST21</span> TEST22<span>TEST23</span>TEST24</p>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][1][3].tag, "p")
        self.assertEqual(len(out_root[1][1][1][3]), 0)
        self.assertEqual(out_root[1][1][1][3].text, "TEST20 TEST21 TEST22TEST23TEST24")

    def test_span_in_abstract(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][1][1].insert(
            0,
            etree.fromstring(
                "<abstract>TEST20 <span>TEST21</span> TEST22"
                "<span>TEST23</span>TEST24</abstract>"
            ),
        )
        inp_root[1][1][1].remove(inp_root[1][1][1][1])
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][1][0].tag, "abstract")
        self.assertEqual(len(out_root[1][1][1][0]), 0)
        self.assertEqual(out_root[1][1][1][0].text, "TEST20 TEST21 TEST22TEST23TEST24")

    def test_span_in_citation(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][1][1].append(
            etree.fromstring(
                "<citation>TEST20 <span>TEST21</span> TEST22"
                "<span>TEST23</span>TEST24</citation>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][1][3].tag, "citation")
        self.assertEqual(len(out_root[1][1][1][3]), 0)
        self.assertEqual(out_root[1][1][1][3].text, "TEST20 TEST21 TEST22TEST23TEST24")

    def test_span_in_item(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][1][1].append(
            etree.fromstring(
                "<list><item>TEST20 <span>TEST21</span> TEST22"
                "<span>TEST23</span>TEST24</item></list>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][1][3].tag, "list")
        self.assertEqual(out_root[1][1][1][3][0].tag, "item")
        self.assertEqual(len(out_root[1][1][1][3][0]), 0)
        self.assertEqual(
            out_root[1][1][1][3][0].text, "TEST20 TEST21 TEST22TEST23TEST24"
        )


class TestBioghistListOutlineConverter(ActionTestCase):
    action_class = BioghistListOutlineConverter

    def test_list(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][1][1].append(
            etree.fromstring(
                "<list xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                "<item>TEST20</item>"
                "<item localType='TEST21.a' xml:lang='TEST21.b'>TEST21</item>"
                "</list>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][1].tag, "biogHist")
        self.assertEqual(len(out_root[1][1][1]), 5)
        self.assertEqual(out_root[1][1][1][3].tag, "p")
        self.assertEqual(out_root[1][1][1][3].text, "TEST20")
        self.assertEqual(out_root[1][1][1][4].tag, "p")
        self.assertEqual(out_root[1][1][1][4].text, "TEST21")
        self.assertIsNone(out_root[1][1][1][4].get("localType"))
        self.assertEqual(
            out_root[1][1][1][4].get("{http://www.w3.org/XML/1998/namespace}lang"),
            "TEST21.b",
        )

    def test_outline(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][1][1].append(
            etree.fromstring(
                "<outline xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                "<level>"
                "<item>TEST20</item>"
                "<item localType='TEST21.a' xml:lang='TEST21.b'>TEST21</item>"
                "</level><level>"
                "<item>TEST30</item>"
                "<level><item>TEST40</item><item>TEST41</item></level>"
                "<item>TEST31</item>"
                "</level></outline>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][1].tag, "biogHist")
        self.assertEqual(len(out_root[1][1][1]), 9)
        self.assertEqual(out_root[1][1][1][3].tag, "p")
        self.assertEqual(out_root[1][1][1][3].text, "TEST20")
        self.assertEqual(out_root[1][1][1][4].tag, "p")
        self.assertEqual(out_root[1][1][1][4].text, "TEST21")
        self.assertIsNone(out_root[1][1][1][4].get("localType"))
        self.assertEqual(
            out_root[1][1][1][4].get("{http://www.w3.org/XML/1998/namespace}lang"),
            "TEST21.b",
        )
        for idx, num in ((5, 30), (6, 40), (7, 41), (8, 31)):
            self.assertEqual(out_root[1][1][1][idx].tag, "p")
            self.assertEqual(out_root[1][1][1][idx].text, f"TEST{num}")


class TestGeneralcontextListCitationConverter(ActionTestCase):
    action_class = GeneralcontextListCitationConverter

    def test_list(self):
        for parent_name in ("generalContext", "structureOrGenealogy"):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}><p>TEST10</p>"
                        "<list xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                        "<item>TEST20</item>"
                        "<item localType='TEST21.a' "
                        "xml:lang='TEST21.b'>TEST21</item>"
                        f"</list></{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 3)
                self.assertEqual(out_root[1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][0].text, "TEST10")
                self.assertEqual(out_root[1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1].text, "TEST20")
                self.assertEqual(out_root[1][1][1][2].tag, "p")
                self.assertEqual(out_root[1][1][1][2].text, "TEST21")
                self.assertIsNone(out_root[1][1][1][2].get("localType"))
                self.assertEqual(
                    out_root[1][1][1][2].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )

    def test_citation(self):
        for parent_name in ("generalContext", "structureOrGenealogy"):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}><p>TEST10</p>"
                        "<citation>TEST20</citation><citation>TEST21</citation>"
                        f"</{parent_name}>"
                    ),
                )
                for num, att_name in enumerate(
                    (
                        "lastDateTimeVerified",
                        "{http://www.w3.org/1999/xlink}actuate",
                        "{http://www.w3.org/1999/xlink}arcrole",
                        "{http://www.w3.org/1999/xlink}href",
                        "{http://www.w3.org/1999/xlink}role",
                        "{http://www.w3.org/1999/xlink}show",
                        "{http://www.w3.org/1999/xlink}title",
                        "{http://www.w3.org/1999/xlink}type",
                        "{http://www.w3.org/XML/1998/namespace}lang",
                    )
                ):
                    inp_root[1][1][1][2].set(att_name, f"TEST21.{num}")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 3)
                self.assertEqual(out_root[1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][0].text, "TEST10")
                self.assertEqual(out_root[1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1].text, "TEST20")
                self.assertEqual(out_root[1][1][1][2].tag, "p")
                self.assertEqual(out_root[1][1][1][2].text, "TEST21")
                for att_name in (
                    "lastDateTimeVerified",
                    "{http://www.w3.org/1999/xlink}actuate",
                    "{http://www.w3.org/1999/xlink}arcrole",
                    "{http://www.w3.org/1999/xlink}href",
                    "{http://www.w3.org/1999/xlink}role",
                    "{http://www.w3.org/1999/xlink}show",
                    "{http://www.w3.org/1999/xlink}title",
                    "{http://www.w3.org/1999/xlink}type",
                ):
                    self.assertIsNone(out_root[1][1][1][2].get(att_name))
                self.assertEqual(
                    out_root[1][1][1][2].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.8",
                )


class TestDescriptionChildrenTextElementsConverter(ActionTestCase):
    action_class = DescriptionChildrenTextElementsConverter

    def test_p_no_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<p>TEST20</p>"
                        "<p xmlns:xml='http://www.w3.org/XML/1998/namespace'"
                        " xml:lang='TEST21.b'>TEST21</p>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}></{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST21")
                self.assertEqual(
                    out_root[1][1][1][1][1].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )

    def test_p_with_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<p>TEST20</p>"
                        "<p xmlns:xml='http://www.w3.org/XML/1998/namespace'"
                        " xml:lang='TEST21.b'>TEST21</p>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}>"
                        "<descriptiveNote><p>TEST30</p></descriptiveNote>"
                        f"</{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 3)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST30")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][2].tag, "p")
                self.assertEqual(out_root[1][1][1][1][2].text, "TEST21")
                self.assertEqual(
                    out_root[1][1][1][1][2].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )

    def test_citation_no_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<citation>TEST20</citation>"
                        "<citation>TEST21</citation>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}></{parent_name}>"
                    ),
                )
                for num, att_name in enumerate(
                    (
                        "lastDateTimeVerified",
                        "{http://www.w3.org/1999/xlink}actuate",
                        "{http://www.w3.org/1999/xlink}arcrole",
                        "{http://www.w3.org/1999/xlink}href",
                        "{http://www.w3.org/1999/xlink}role",
                        "{http://www.w3.org/1999/xlink}show",
                        "{http://www.w3.org/1999/xlink}title",
                        "{http://www.w3.org/1999/xlink}type",
                        "{http://www.w3.org/XML/1998/namespace}lang",
                    )
                ):
                    inp_root[1][1][1][1].set(att_name, f"TEST21.{num}")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST21")
                for att_name in (
                    "lastDateTimeVerified",
                    "{http://www.w3.org/1999/xlink}actuate",
                    "{http://www.w3.org/1999/xlink}arcrole",
                    "{http://www.w3.org/1999/xlink}href",
                    "{http://www.w3.org/1999/xlink}role",
                    "{http://www.w3.org/1999/xlink}show",
                    "{http://www.w3.org/1999/xlink}title",
                    "{http://www.w3.org/1999/xlink}type",
                ):
                    self.assertIsNone(out_root[1][1][1][1][1].get(att_name))
                self.assertEqual(
                    out_root[1][1][1][1][1].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.8",
                )

    def test_citation_with_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<citation>TEST20</citation>"
                        "<citation>TEST21</citation>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}>"
                        "<descriptiveNote><p>TEST30</p></descriptiveNote>"
                        f"</{parent_name}>"
                    ),
                )
                for num, att_name in enumerate(
                    (
                        "lastDateTimeVerified",
                        "{http://www.w3.org/1999/xlink}actuate",
                        "{http://www.w3.org/1999/xlink}arcrole",
                        "{http://www.w3.org/1999/xlink}href",
                        "{http://www.w3.org/1999/xlink}role",
                        "{http://www.w3.org/1999/xlink}show",
                        "{http://www.w3.org/1999/xlink}title",
                        "{http://www.w3.org/1999/xlink}type",
                        "{http://www.w3.org/XML/1998/namespace}lang",
                    )
                ):
                    inp_root[1][1][1][1].set(att_name, f"TEST21.{num}")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 3)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST30")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][2].tag, "p")
                self.assertEqual(out_root[1][1][1][1][2].text, "TEST21")
                for att_name in (
                    "lastDateTimeVerified",
                    "{http://www.w3.org/1999/xlink}actuate",
                    "{http://www.w3.org/1999/xlink}arcrole",
                    "{http://www.w3.org/1999/xlink}href",
                    "{http://www.w3.org/1999/xlink}role",
                    "{http://www.w3.org/1999/xlink}show",
                    "{http://www.w3.org/1999/xlink}title",
                    "{http://www.w3.org/1999/xlink}type",
                ):
                    self.assertIsNone(out_root[1][1][1][1][2].get(att_name))
                self.assertEqual(
                    out_root[1][1][1][1][2].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.8",
                )

    def test_list_no_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<list xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                        "<item>TEST20</item>"
                        "<item localType='TEST21.a' xml:lang='TEST21.b'>TEST21"
                        "</item></list>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}></{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST21")
                self.assertIsNone(out_root[1][1][1][1][1].get("localType"))
                self.assertEqual(
                    out_root[1][1][1][1][1].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )

    def test_list_with_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<list xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                        "<item>TEST20</item>"
                        "<item localType='TEST21.a' xml:lang='TEST21.b'>TEST21"
                        "</item></list>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}>"
                        "<descriptiveNote><p>TEST30</p></descriptiveNote>"
                        f"</{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 3)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST30")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][2].tag, "p")
                self.assertEqual(out_root[1][1][1][1][2].text, "TEST21")
                self.assertIsNone(out_root[1][1][1][1][2].get("localType"))
                self.assertEqual(
                    out_root[1][1][1][1][2].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )

    def test_outline_no_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<outline xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                        "<level>"
                        "<item>TEST20</item>"
                        "<item localType='TEST21.a'"
                        " xml:lang='TEST21.b'>TEST21</item>"
                        "</level><level>"
                        "<item>TEST22</item>"
                        "<level><item>TEST23</item><item>TEST24</item></level>"
                        "<item>TEST25</item>"
                        "</level></outline>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}></{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 6)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST21")
                self.assertIsNone(out_root[1][1][1][1][1].get("localType"))
                self.assertEqual(
                    out_root[1][1][1][1][1].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )
                for idx in range(2, 6):
                    self.assertEqual(out_root[1][1][1][1][idx].tag, "p")
                    self.assertEqual(out_root[1][1][1][1][idx].text, f"TEST{20 + idx}")

    def test_outline_with_descriptivenote(self):
        for parent_name, child_name in (
            ("functions", "function"),
            ("legalStatuses", "legalStatus"),
            ("localDescriptions", "localDescription"),
            ("mandates", "mandate"),
            ("occupations", "occupation"),
            ("places", "place"),
        ):
            with self.subTest(parent=parent_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][1].insert(
                    1,
                    etree.fromstring(
                        f"<{parent_name}>"
                        "<outline xmlns:xml='http://www.w3.org/XML/1998/namespace'>"
                        "<level>"
                        "<item>TEST20</item>"
                        "<item localType='TEST21.a'"
                        " xml:lang='TEST21.b'>TEST21</item>"
                        "</level><level>"
                        "<item>TEST22</item>"
                        "<level><item>TEST23</item><item>TEST24</item></level>"
                        "<item>TEST25</item>"
                        "</level></outline>"
                        f"<{child_name}><placeEntry>TEST19</placeEntry>"
                        f"</{child_name}>"
                        "<descriptiveNote><p>TEST30</p></descriptiveNote>"
                        f"</{parent_name}>"
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][1].tag, parent_name)
                self.assertEqual(len(out_root[1][1][1]), 2)
                self.assertEqual(out_root[1][1][1][0].tag, child_name)
                self.assertEqual(out_root[1][1][1][1].tag, "descriptiveNote")
                self.assertEqual(len(out_root[1][1][1][1]), 7)
                self.assertEqual(out_root[1][1][1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][1][1][0].text, "TEST30")
                self.assertEqual(out_root[1][1][1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1][1][1].text, "TEST20")
                self.assertEqual(out_root[1][1][1][1][2].tag, "p")
                self.assertEqual(out_root[1][1][1][1][2].text, "TEST21")
                self.assertIsNone(out_root[1][1][1][1][2].get("localType"))
                self.assertEqual(
                    out_root[1][1][1][1][2].get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    "TEST21.b",
                )
                for idx in range(3, 7):
                    self.assertEqual(out_root[1][1][1][1][idx].tag, "p")
                    self.assertEqual(out_root[1][1][1][1][idx].text, f"TEST{19 + idx}")


if __name__ == "__main__":
    unittest.main()
