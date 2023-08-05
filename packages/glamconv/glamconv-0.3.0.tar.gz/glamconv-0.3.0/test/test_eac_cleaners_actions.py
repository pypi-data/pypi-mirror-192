# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.utils import NS
from glamconv.eac.cleaners import (
    AttributesEraser,
    MultipleIdentitiesEraser,
    AdditionalLanguageDeclarationEraser,
    AdditionalNameOrEntryEraser,
    WrappingObjectsEraser,
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


def build_qname(prefixed_name):
    prefix, *local_name = prefixed_name.split(":", 1)
    qname = f"{{{NS[prefix]}}}{local_name[0]}" if len(local_name) > 0 else prefixed_name
    return qname


class TestWrappingObjectsEraser(ActionTestCase):
    action_class = WrappingObjectsEraser

    def test_wrapping_objects_in_relations_children(self):
        for prt_name in ("cpfRelation", "resourceRelation", "functionRelation"):
            with self.subTest(parent_name=prt_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        f"<relations><{prt_name}>"
                        "<objectXMLWrap>TEST01</objectXMLWrap>"
                        "<objectBinWrap>TEST02</objectBinWrap>"
                        f"</{prt_name}></relations>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, prt_name)
                self.assertEqual(len(out_root[1][1][0]), 0)

    def test_wrapping_objects_in_setcomponent(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<alternativeSet><setComponent>"
                "<objectXMLWrap>TEST01</objectXMLWrap>"
                "<objectBinWrap>TEST02</objectBinWrap>"
                "</setComponent></alternativeSet>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "setComponent")
        self.assertEqual(len(out_root[1][1][0]), 0)

    def test_wrapping_objects_in_source(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<sources><source>"
                "<objectXMLWrap>TEST01</objectXMLWrap>"
                "<objectBinWrap>TEST02</objectBinWrap>"
                "</source></sources>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "source")
        self.assertEqual(len(out_root[1][1][0]), 0)


class TestAdditionalNameOrEntryEraser(ActionTestCase):
    action_class = AdditionalNameOrEntryEraser

    def test_eventdescription(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0][3][0].append(
            etree.fromstring("<eventDescription>TEST50</eventDescription>")
        )
        inp_root[0][3].append(
            etree.fromstring(
                "<maintenanceEvent><eventType>created</eventType>"
                "<eventDateTime>2022-09-01</eventDateTime>"
                "<agentType>human</agentType><agent>TEST100</agent>"
                "<eventDescription>TEST101</eventDescription>"
                "<eventDescription>TEST102</eventDescription>"
                "<eventDescription>TEST103</eventDescription>"
                "</maintenanceEvent>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][3][0].tag, "maintenanceEvent")
        self.assertEqual(len(out_root[0][3][0]), 5)
        self.assertEqual(out_root[0][3][0][4].tag, "eventDescription")
        self.assertEqual(out_root[0][3][0][4].text, "TEST50")
        self.assertEqual(out_root[0][3][1].tag, "maintenanceEvent")
        self.assertEqual(len(out_root[0][3][1]), 5)
        self.assertEqual(out_root[0][3][1][4].tag, "eventDescription")
        self.assertEqual(out_root[0][3][1][4].text, "TEST101")

    def test_one_agencyname(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(len(out_root[0][2]), 1)
        self.assertEqual(out_root[0][2][0].tag, "agencyName")
        self.assertEqual(out_root[0][2][0].text, "TEST02")

    def test_several_agencyname(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0][2].append(etree.fromstring("<agencyName>TEST100</agencyName>"))
        inp_root[0][2].append(etree.fromstring("<agencyName>TEST101</agencyName>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(len(out_root[0][2]), 1)
        self.assertEqual(out_root[0][2][0].tag, "agencyName")
        self.assertEqual(out_root[0][2][0].text, "TEST02")

    def test_placeentry_in_relations_children(self):
        for prt_name in ("resourceRelation", "functionRelation"):
            with self.subTest(parent_name=prt_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        f"<relations><{prt_name}>"
                        "<placeEntry>TEST100</placeEntry>"
                        f"</{prt_name}><{prt_name}>"
                        "<placeEntry>TEST200</placeEntry>"
                        "<placeEntry>TEST201</placeEntry>"
                        "<placeEntry>TEST202</placeEntry>"
                        f"</{prt_name}></relations>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, prt_name)
                self.assertEqual(len(out_root[1][1][0]), 1)
                self.assertEqual(out_root[1][1][0][0].tag, "placeEntry")
                self.assertEqual(out_root[1][1][0][0].text, "TEST100")
                self.assertEqual(out_root[1][1][1].tag, prt_name)
                self.assertEqual(len(out_root[1][1][1]), 1)
                self.assertEqual(out_root[1][1][1][0].tag, "placeEntry")
                self.assertEqual(out_root[1][1][1][0].text, "TEST200")

    def test_sourceentry(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1].append(
            etree.fromstring(
                "<sources><source>"
                "<sourceEntry>TEST100</sourceEntry>"
                "</source><source>"
                "<sourceEntry>TEST200</sourceEntry>"
                "<sourceEntry>TEST201</sourceEntry>"
                "<sourceEntry>TEST202</sourceEntry>"
                "</source></sources>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "source")
        self.assertEqual(len(out_root[1][1][0]), 1)
        self.assertEqual(out_root[1][1][0][0].tag, "sourceEntry")
        self.assertEqual(out_root[1][1][0][0].text, "TEST100")
        self.assertEqual(out_root[1][1][1].tag, "source")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "sourceEntry")
        self.assertEqual(out_root[1][1][1][0].text, "TEST200")


class TestAdditionalLanguageDeclarationEraser(ActionTestCase):
    action_class = AdditionalLanguageDeclarationEraser

    def test_one_languagedeclaration(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0].insert(
            3,
            etree.fromstring(
                "<languageDeclaration>"
                "<language languageCode='eng'>TEST100</language>"
                "<script scriptCode='Engl'>TEST101</script>"
                "</languageDeclaration>"
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 5)
        self.assertEqual(out_root[0][3].tag, "languageDeclaration")
        self.assertEqual(len(out_root[0][3]), 2)
        self.assertEqual(out_root[0][3][0].tag, "language")
        self.assertEqual(out_root[0][3][0].text, "TEST100")
        self.assertEqual(out_root[0][3][1].tag, "script")
        self.assertEqual(out_root[0][3][1].text, "TEST101")
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(out_root[0][4].tag, "maintenanceHistory")

    def test_several_languagedeclaration(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0].insert(
            3,
            etree.fromstring(
                "<languageDeclaration>"
                "<language languageCode='eng'>TEST120</language>"
                "<script scriptCode='Engl'>TEST121</script>"
                "</languageDeclaration>"
            ),
        )
        inp_root[0].insert(
            3,
            etree.fromstring(
                "<languageDeclaration>"
                "<language languageCode='eng'>TEST110</language>"
                "<script scriptCode='Engl'>TEST111</script>"
                "</languageDeclaration>"
            ),
        )
        inp_root[0].insert(
            3,
            etree.fromstring(
                "<languageDeclaration>"
                "<language languageCode='eng'>TEST100</language>"
                "<script scriptCode='Engl'>TEST101</script>"
                "</languageDeclaration>"
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 5)
        self.assertEqual(out_root[0][3].tag, "languageDeclaration")
        self.assertEqual(len(out_root[0][3]), 2)
        self.assertEqual(out_root[0][3][0].tag, "language")
        self.assertEqual(out_root[0][3][0].text, "TEST100")
        self.assertEqual(out_root[0][3][1].tag, "script")
        self.assertEqual(out_root[0][3][1].text, "TEST101")
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(out_root[0][4].tag, "maintenanceHistory")


class TestMultipleIdentitiesEraser(ActionTestCase):
    action_class = MultipleIdentitiesEraser

    def test_multipleidentity(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root.remove(inp_root[1])
        inp_root.append(
            etree.fromstring(
                "<multipleIdentities><cpfDescription><identity>"
                "<entityType>person</entityType><nameEntry>"
                "<part>TEST101</part></nameEntry></identity>"
                "</cpfDescription><cpfDescription><identity>"
                "<entityType>person</entityType><nameEntry>"
                "<part>TEST102</part></nameEntry></identity>"
                "</cpfDescription></multipleIdentities>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root), 2)
        self.assertEqual(out_root[0].tag, "control")
        self.assertEqual(out_root[1].tag, "cpfDescription")
        self.assertEqual(out_root[1][0][1][0].tag, "part")
        self.assertEqual(out_root[1][0][1][0].text, "TEST101")


class TestAttributesEraser(ActionTestCase):
    action_class = AttributesEraser

    def test_abbreviation(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0].insert(
            3,
            etree.fromstring(
                "<conventionDeclaration>"
                "<abbreviation>X</abbreviation>"
                "<citation>X</citation>"
                "</conventionDeclaration>"
            ),
        )
        inp_root[0][3][0].set(f"{{{NS['xml']}}}id", "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][3][0].tag, "abbreviation")
        self.assertEqual(
            out_root[0][3][0].get(f"{{{NS['xml']}}}id"),
            None,
        )

    def test_bioghist(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist><p>X</p>" "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "biogHist")
                self.assertEqual(
                    out_root[1][1][0].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_bioghist_textual_children(self):
        atts = {
            "abstract": (("localType", "xml:id"), ("xml:lang",)),
            "citation": (
                ("xml:id",),
                (
                    "lastDateTimeVerified",
                    "xlink:actuate",
                    "xlink:arcrole",
                    "xlink:href",
                    "xlink:role",
                    "xlink:show",
                    "xlink:title",
                    "xlink:type",
                    "xml:lang",
                ),
            ),
            "p": (("xml:id",), ("xml:lang",)),
        }
        for elt_name, (names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            "<description><biogHist>"
                            f"<{elt_name}>X</{elt_name}>"
                            "</biogHist></description>"
                        )
                    )
                    qname = build_qname(att_name)
                    inp_root[1][1][0][0].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0][0].tag, elt_name)
                    self.assertEqual(
                        out_root[1][1][0][0].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_list(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<list><item>X</item></list>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "list")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    None,
                )

    def test_item(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<list><item>X</item></list>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "item")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_outline(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<outline><level><item>X</item></level></outline>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "outline")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    None,
                )

    def test_level(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<outline><level><item>X</item></level></outline>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "level")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_chronlist(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<chronList><chronItem><date>X</date>"
                        "<event>X</event></chronItem></chronList>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "chronList")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    None,
                )

    def test_chronitem(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<chronList><chronItem><date>X</date>"
                        "<event>X</event></chronItem></chronList>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "chronItem")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_event(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><biogHist>"
                        "<chronList><chronItem><date>X</date>"
                        "<event>X</event></chronItem></chronList>"
                        "</biogHist></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0][1].tag, "event")
                self.assertEqual(
                    out_root[1][1][0][0][0][1].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_place_textual_children(self):
        atts = {
            "placeRole": (
                ("xml:id",),
                (
                    "lastDateTimeVerified",
                    "scriptCode",
                    "transliteration",
                    "vocabularySource",
                    "xml:lang",
                ),
            ),
            "placeEntry": (
                ("accuracy", "altitude", "xml:id"),
                (
                    "countryCode",
                    "latitude",
                    "localType",
                    "longitude",
                    "scriptCode",
                    "transliteration",
                    "vocabularySource",
                    "xml:lang",
                ),
            ),
            "date": (
                ("xml:id",),
                ("localType", "notAfter", "notBefore", "standardDate", "xml:lang"),
            ),
        }
        for elt_name, (names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            "<description><place>"
                            f"<{elt_name}>X</{elt_name}>"
                            "</place></description>"
                        )
                    )
                    qname = build_qname(att_name)
                    inp_root[1][1][0][0].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0][0].tag, elt_name)
                    self.assertEqual(
                        out_root[1][1][0][0].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_daterange(self):
        for att_name in ("xml:id", "xml:lang", "localType"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><place><dateRange>"
                        "<fromDate>X</fromDate><toDate>X</toDate>"
                        "</dateRange></place></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "dateRange")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_fromdate_todate(self):
        for pos, elt_name in ((0, "fromDate"), (1, "toDate")):
            for att_name in (
                "localType",
                "notAfter",
                "notBefore",
                "standardDate",
                "xml:id",
                "xml:lang",
            ):
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            "<description><place><dateRange>"
                            "<fromDate>X</fromDate><toDate>X</toDate>"
                            "</dateRange></place></description>"
                        )
                    )
                    qname = build_qname(att_name)
                    inp_root[1][1][0][0][pos].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0][0][pos].tag, elt_name)
                    self.assertEqual(
                        out_root[1][1][0][0][pos].get(qname),
                        "TEST" if att_name not in ("xml:id", "localType") else None,
                    )

    def test_dateset(self):
        for att_name in ("xml:id", "xml:lang", "localType"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><place><dateSet>"
                        "<date>X</date><date>X</date>"
                        "</dateSet></place></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "dateSet")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    None,
                )

    def test_address(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><place>"
                        "<address><addressLine>X</addressLine></address>"
                        "</place></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "address")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_addressline(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><place>"
                        "<address><addressLine>X</addressLine></address>"
                        "</place></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "addressLine")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_descriptivenote(self):
        for att_name in ("xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><place>"
                        "<descriptiveNote><p>X</p></descriptiveNote>"
                        "</place></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "descriptiveNote")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    None,
                )

    def test_agencycode(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0][2].insert(
            0,
            etree.fromstring("<agencyCode>X</agencyCode>"),
        )
        inp_root[0][2][0].set(f"{{{NS['xml']}}}id", "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0].tag, "agencyCode")
        self.assertEqual(
            out_root[0][2][0].get(f"{{{NS['xml']}}}id"),
            None,
        )

    def test_agencyname(self):
        for att_name in ("xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[0][2][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][2][0].tag, "agencyName")
                self.assertEqual(
                    out_root[0][2][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_otheragencycode(self):
        for att_name in ("localType", "xml:id"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0][2].insert(
                    0,
                    etree.fromstring(
                        "<otherAgencyCode localType='X'>X</otherAgencyCode>"
                    ),
                )
                qname = build_qname(att_name)
                inp_root[0][2][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][2][0].tag, "otherAgencyCode")
                self.assertEqual(
                    out_root[0][2][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_maintenanceevent_children(self):
        atts = {
            "eventType": (0, ("xml:id",), tuple()),
            "eventDateTime": (1, ("xml:id", "xml:lang"), ("standardDateTime",)),
            "agentType": (2, ("xml:id",), tuple()),
            "agent": (3, ("xml:id",), ("xml:lang",)),
            "eventDescription": (4, ("xml:id",), ("xml:lang",)),
        }
        for elt_name, (pos, names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[0][3][0].append(
                        etree.fromstring("<eventDescription>X</eventDescription>")
                    )
                    qname = build_qname(att_name)
                    inp_root[0][3][0][pos].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[0][3][0][pos].tag, elt_name)
                    self.assertEqual(
                        out_root[0][3][0][pos].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_nameentry_textual_children(self):
        atts = {
            "part": (("xml:id",), ("localType", "xml:lang")),
            "alternativeForm": (("xml:id",), tuple()),
            "authorizedForm": (("xml:id",), tuple()),
        }
        for elt_name, (names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    if elt_name != "part":
                        inp_root[1][0][1].append(
                            etree.fromstring(f"<{elt_name}>X</{elt_name}>")
                        )
                    qname = build_qname(att_name)
                    inp_root[1][0][1][-1].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][0][1][-1].tag, elt_name)
                    self.assertEqual(
                        out_root[1][0][1][-1].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_usedates(self):
        for att_name in ("xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][0][1].append(
                    etree.fromstring("<useDates><date>X</date></useDates>")
                )
                qname = build_qname(att_name)
                inp_root[1][0][1][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][1][1].tag, "useDates")
                self.assertEqual(
                    out_root[1][0][1][1].get(qname),
                    None,
                )

    def test_alternativeset(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<alternativeSet><setComponent>"
                        "<componentEntry>X</componentEntry>"
                        "</setComponent></alternativeSet>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "alternativeSet")
                self.assertEqual(
                    out_root[1][1].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_setcomponent(self):
        for att_name in (
            "lastDateTimeVerified",
            "xlink:actuate",
            "xlink:arcrole",
            "xlink:href",
            "xlink:role",
            "xlink:show",
            "xlink:title",
            "xlink:type",
            "xml:id",
            "xml:lang",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<alternativeSet><setComponent>"
                        "<componentEntry>X</componentEntry>"
                        "</setComponent></alternativeSet>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "setComponent")
                self.assertEqual(
                    out_root[1][1][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_componententry(self):
        for att_name in (
            "localType",
            "scriptCode",
            "transliteration",
            "xml:id",
            "xml:lang",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<alternativeSet><setComponent>"
                        "<componentEntry>X</componentEntry>"
                        "</setComponent></alternativeSet>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "componentEntry")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_control(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0].tag, "control")
                self.assertEqual(out_root[0].get(qname), None)

    def test_cpfdescription(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1].tag, "cpfDescription")
                self.assertEqual(out_root[1].get(qname), None)

    def test_control_declaration_children(self):
        atts = {
            "conventionDeclaration": (("xml:id", "xml:lang"), tuple()),
            "rightsDeclaration": (("xml:id",), ("localType", "xml:lang")),
            "localTypeDeclaration": (("xml:id", "xml:lang"), tuple()),
        }
        for elt_name, (names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[0].insert(
                        3,
                        etree.fromstring(
                            f"<{elt_name}><citation>X</citation></{elt_name}>"
                        ),
                    )
                    qname = build_qname(att_name)
                    inp_root[0][3].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[0][3].tag, elt_name)
                    self.assertEqual(
                        out_root[0][3].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_relations_children(self):
        atts = {
            "cpfRelation": (
                ("xml:id", "xml:lang"),
                (
                    "cpfRelationType",
                    "lastDateTimeVerified",
                    "xlink:actuate",
                    "xlink:arcrole",
                    "xlink:href",
                    "xlink:role",
                    "xlink:show",
                    "xlink:title",
                    "xlink:type",
                ),
            ),
            "resourceRelation": (
                ("xml:id", "xml:lang"),
                (
                    "resourceRelationType",
                    "lastDateTimeVerified",
                    "xlink:actuate",
                    "xlink:arcrole",
                    "xlink:href",
                    "xlink:role",
                    "xlink:show",
                    "xlink:title",
                    "xlink:type",
                ),
            ),
            "functionRelation": (
                ("xml:id", "xml:lang"),
                (
                    "functionRelationType",
                    "lastDateTimeVerified",
                    "xlink:actuate",
                    "xlink:arcrole",
                    "xlink:href",
                    "xlink:role",
                    "xlink:show",
                    "xlink:title",
                    "xlink:type",
                ),
            ),
        }
        for elt_name, (names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            f"<relations><{elt_name}>"
                            "<relationEntry>X</relationEntry>"
                            f"</{elt_name}></relations>"
                        )
                    )
                    qname = build_qname(att_name)
                    inp_root[1][1][0].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0].tag, elt_name)
                    self.assertEqual(
                        out_root[1][1][0].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_relationentry(self):
        for att_name in (
            "localType",
            "scriptCode",
            "transliteration",
            "xml:id",
            "xml:lang",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<relations><cpfRelation>"
                        "<relationEntry>X</relationEntry>"
                        "</cpfRelation></relations>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "relationEntry")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_description(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><existDates>"
                        "<date>X</date>"
                        "</existDates></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "description")
                self.assertEqual(out_root[1][1].get(qname), None)

    def test_existdates(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><existDates>"
                        "<date>X</date>"
                        "</existDates></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "existDates")
                self.assertEqual(out_root[1][1][0].get(qname), None)

    def test_eaccpf(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root.set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root.tag, "eac-cpf")
                self.assertEqual(
                    out_root.get(qname), "TEST" if att_name != "xml:id" else None
                )

    def test_identity(self):
        for att_name in ("identityType", "localType", "xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[1][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0].tag, "identity")
                self.assertEqual(
                    out_root[1][0].get(qname),
                    "TEST" if att_name == "identityType" else None,
                )

    def test_identity_entity_children(self):
        atts = {
            "entityId": (0, ("xml:id",), ("localType",)),
            "entityType": (1, ("xml:id",), tuple()),
        }
        for elt_name, (pos, names, kept_names) in atts.items():
            for att_name in names + kept_names:
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1][0].insert(0, etree.fromstring("<entityId>X</entityId>"))
                    qname = build_qname(att_name)
                    inp_root[1][0][pos].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][0][pos].tag, elt_name)
                    self.assertEqual(
                        out_root[1][0][pos].get(qname),
                        "TEST" if att_name in kept_names else None,
                    )

    def test_nameentry(self):
        for att_name in (
            "localType",
            "scriptCode",
            "transliteration",
            "xml:id",
            "xml:lang",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[1][0][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][1].tag, "nameEntry")
                self.assertEqual(
                    out_root[1][0][1].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_nameentryparallel(self):
        for att_name in ("localType", "xml:id"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1][0].append(
                    etree.fromstring(
                        "<nameEntryParallel><nameEntry><part>X1</part>"
                        "</nameEntry><nameEntry><part>X2</part></nameEntry>"
                        "</nameEntryParallel>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][0][2].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][2].tag, "nameEntryParallel")
                self.assertEqual(
                    out_root[1][0][2].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_preferredform(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[1][0].append(
            etree.fromstring(
                "<nameEntryParallel><nameEntry><part>X1</part>"
                "<preferredForm>X</preferredForm></nameEntry>"
                "<nameEntry><part>X2</part></nameEntry></nameEntryParallel>"
            )
        )
        qname = build_qname("xml:id")
        inp_root[1][0][2][0][1].set(qname, "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][0][2][0][1].tag, "preferredForm")
        self.assertEqual(out_root[1][0][2][0][1].get(qname), None)

    def test_description_children(self):
        atts = {
            "functions": "function",
            "legalStatuses": "legalStatus",
            "localDescriptions": "localDescription",
            "mandates": "mandate",
            "occupations": "occupation",
        }
        for elt_name, sub_elt_name in atts.items():
            for att_name in ("localType", "xml:id", "xml:lang"):
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            f"<description><{elt_name}><{sub_elt_name}>"
                            "<term>X</term>"
                            f"</{sub_elt_name}></{elt_name}></description>"
                        )
                    )
                    if elt_name == "localDescriptions":
                        inp_root[1][1][0].set("localType", "X")
                        inp_root[1][1][0][0].set("localType", "X")
                    qname = build_qname(att_name)
                    inp_root[1][1][0].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0].tag, elt_name)
                    expected = (
                        "TEST"
                        if elt_name == "localDescriptions" and att_name == "localType"
                        else None
                    )
                    self.assertEqual(out_root[1][1][0].get(qname), expected)

    def test_description_grandchildren(self):
        atts = {
            "function": "functions",
            "legalStatus": "legalStatuses",
            "localDescription": "localDescriptions",
            "mandate": "mandates",
            "occupation": "occupations",
        }
        for elt_name, parent_name in atts.items():
            for att_name in ("localType", "xml:id", "xml:lang"):
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            f"<description><{parent_name}><{elt_name}>"
                            "<term>X</term>"
                            f"</{elt_name}></{parent_name}></description>"
                        )
                    )
                    if elt_name == "localDescription":
                        inp_root[1][1][0].set("localType", "X")
                        inp_root[1][1][0][0].set("localType", "X")
                    qname = build_qname(att_name)
                    inp_root[1][1][0][0].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0][0].tag, elt_name)
                    self.assertEqual(
                        out_root[1][1][0][0].get(qname),
                        "TEST" if att_name == "localType" else None,
                    )

    def test_term(self):
        for att_name in (
            "lastDateTimeVerified",
            "scriptCode",
            "transliteration",
            "vocabularySource",
            "xml:id",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><functions><function>"
                        "<term>X</term>"
                        "</function></functions></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "term")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_languagesused(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><languagesUsed><languageUsed>"
                        "<language languageCode='eng'>X</language>"
                        "<script scriptCode='Engl'>X</script>"
                        "</languageUsed></languagesUsed></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "languagesUsed")
                self.assertEqual(out_root[1][1][0].get(qname), None)

    def test_languageused(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><languagesUsed><languageUsed>"
                        "<language languageCode='eng'>X</language>"
                        "<script scriptCode='Engl'>X</script>"
                        "</languageUsed></languagesUsed></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "languageUsed")
                self.assertEqual(
                    out_root[1][1][0][0].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_language(self):
        for att_name in ("languageCode", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><languagesUsed><languageUsed>"
                        "<language languageCode='eng'>X</language>"
                        "<script scriptCode='Engl'>X</script>"
                        "</languageUsed></languagesUsed></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][0].set(qname, "tst")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "language")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(qname),
                    "tst" if att_name != "xml:id" else None,
                )

    def test_script(self):
        for att_name in ("languageCode", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><languagesUsed><languageUsed>"
                        "<language languageCode='eng'>X</language>"
                        "<script scriptCode='Engl'>X</script>"
                        "</languageUsed></languagesUsed></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0][1].set(qname, "Test")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][1].tag, "script")
                self.assertEqual(
                    out_root[1][1][0][0][1].get(qname),
                    "Test" if att_name != "xml:id" else None,
                )

    def test_places(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><places><place>"
                        "<placeEntry>X</placeEntry>"
                        "</place></places></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "places")
                self.assertEqual(out_root[1][1][0].get(qname), None)

    def test_place(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<description><places><place>"
                        "<placeEntry>X</placeEntry>"
                        "</place></places></description>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "place")
                self.assertEqual(out_root[1][1][0][0].get(qname), None)

    def test_description_textual_children(self):
        for elt_name in ("generalContext", "structureOrGenealogy"):
            for att_name in ("localType", "xml:id", "xml:lang"):
                with self.subTest(element=elt_name, attribute=att_name):
                    inp_root = etree.fromstring(DATA_EAC_CPF)
                    inp_root[1].append(
                        etree.fromstring(
                            f"<description><{elt_name}><p>X</p>"
                            f"</{elt_name}></description>"
                        )
                    )
                    qname = build_qname(att_name)
                    inp_root[1][1][0].set(qname, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0].tag, elt_name)
                    self.assertEqual(out_root[1][1][0].get(qname), None)

    def test_recordId(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0][0].set(f"{{{NS['xml']}}}id", "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][0].tag, "recordId")
        self.assertEqual(
            out_root[0][0].get(f"{{{NS['xml']}}}id"),
            None,
        )

    def test_maintenanceStatus(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0][1].set(f"{{{NS['xml']}}}id", "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][0].tag, "recordId")
        self.assertEqual(
            out_root[0][1].get(f"{{{NS['xml']}}}id"),
            None,
        )

    def test_otherrecordid(self):
        for att_name in (
            "localType",
            "xml:id",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0].insert(
                    1,
                    etree.fromstring("<otherRecordId>X</otherRecordId>"),
                )
                qname = build_qname(att_name)
                inp_root[0][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][1].tag, "otherRecordId")
                self.assertEqual(
                    out_root[0][1].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_publicationstatus(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        inp_root[0].insert(
            2,
            etree.fromstring("<publicationStatus>X</publicationStatus>"),
        )
        qname = build_qname("xml:id")
        inp_root[0][2].set(qname, "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "publicationStatus")
        self.assertEqual(out_root[0][2].get(qname), None)

    def test_maintenanceagency(self):
        inp_root = etree.fromstring(DATA_EAC_CPF)
        qname = build_qname("xml:id")
        inp_root[0][2].set(qname, "TEST")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "maintenanceAgency")
        self.assertEqual(out_root[0][2].get(qname), None)

    def test_languagedeclaration(self):
        for att_name in ("xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0].insert(
                    3,
                    etree.fromstring(
                        "<languageDeclaration>"
                        "<language languageCode='eng'>X</language>"
                        "<script scriptCode='Engl'>X</script>"
                        "</languageDeclaration>"
                    ),
                )
                qname = build_qname(att_name)
                inp_root[0][3].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][3].tag, "languageDeclaration")
                self.assertEqual(out_root[0][3].get(qname), None)

    def test_localcontrol(self):
        for att_name in ("localType", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0].insert(
                    3,
                    etree.fromstring(
                        "<localControl localType='X'><term>X</term>"
                        "<language languageCode='eng'>X</language>"
                        "</localControl>"
                    ),
                )
                qname = build_qname(att_name)
                inp_root[0][3].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][3].tag, "localControl")
                self.assertEqual(
                    out_root[0][3].get(qname),
                    "TEST" if att_name == "localType" else None,
                )

    def test_maintenancehistory(self):
        for att_name in ("xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[0][3].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][3].tag, "maintenanceHistory")
                self.assertEqual(out_root[0][3].get(qname), None)

    def test_maintenanceevent(self):
        for att_name in ("xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                qname = build_qname(att_name)
                inp_root[0][3][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][3][0].tag, "maintenanceEvent")
                self.assertEqual(
                    out_root[0][3][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_sources(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0].append(
                    etree.fromstring(
                        "<sources><source><sourceEntry>X</sourceEntry>"
                        "</source></sources>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[0][4].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][4].tag, "sources")
                self.assertEqual(out_root[0][4].get(qname), None)

    def test_source(self):
        for att_name in (
            "lastDateTimeVerified",
            "xlink:actuate",
            "xlink:arcrole",
            "xlink:href",
            "xlink:role",
            "xlink:show",
            "xlink:title",
            "xlink:type",
            "xml:id",
        ):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0].append(
                    etree.fromstring(
                        "<sources><source><sourceEntry>X</sourceEntry>"
                        "</source></sources>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[0][4][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][4][0].tag, "source")
                self.assertEqual(
                    out_root[0][4][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_sourceentry(self):
        for att_name in ("scriptCode", "transliteration", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[0].append(
                    etree.fromstring(
                        "<sources><source><sourceEntry>X</sourceEntry>"
                        "</source></sources>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[0][4][0][0].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][4][0][0].tag, "sourceEntry")
                self.assertEqual(
                    out_root[0][4][0][0].get(qname),
                    "TEST" if att_name != "xml:id" else None,
                )

    def test_relations(self):
        for att_name in ("xml:base", "xml:id", "xml:lang"):
            with self.subTest(attribute=att_name):
                inp_root = etree.fromstring(DATA_EAC_CPF)
                inp_root[1].append(
                    etree.fromstring(
                        "<relations><cpfRelation>"
                        "<relationEntry>X</relationEntry>"
                        "</cpfRelation></relations>"
                    )
                )
                qname = build_qname(att_name)
                inp_root[1][1].set(qname, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "relations")
                self.assertEqual(out_root[1][1].get(qname), None)


if __name__ == "__main__":
    unittest.main()
