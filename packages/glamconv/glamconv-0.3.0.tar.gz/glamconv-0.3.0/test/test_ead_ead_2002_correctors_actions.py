# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.ead_2002_correcters import (
    ChangeChildrenOrderer,
    EadheaderChildrenOrderer,
    ArchdescChildrenOrderer,
    CChildrenOrderer,
    EmptyEltsEraser,
    ParagraphAdder,
    EmptyAttrsEraser,
    IdentifierConverter,
    UnitdateCertainlyConverter,
    COTHERlevelConverter,
    LowercaseElements,
    NormalizeIdAttributes,
)


DATA1 = """
<ead xmlns:xlink="http://www.w3.org/1999/xlink">
  <eadheader>
    <eadid countrycode="FR" identifier="ID1" mainagencycode="LGLB-2022">LGLB-2022-ID1</eadid>
    <filedesc>
      <titlestmt>
        <titleproper>Example 1</titleproper>
      </titlestmt>
    </filedesc>
  </eadheader>
  <archdesc level="fonds">
  </archdesc>
</ead>
"""

DATA2 = """
    <did xmlns:xlink="http://www.w3.org/1999/xlink">
      <unitid>UID1</unitid>
      <unittitle>Exemple 1</unittitle>
      <unitdate>2016-2022</unitdate>
      <dao xlink:href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
"""


class TestIdAttributesNormalizer(ActionTestCase):
    action_class = NormalizeIdAttributes

    def test_id_normalizing(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root.set("id", "A1")  # Should not change
        inp_root[0].set("id", "25")  # Should become _25
        inp_root[0][1].set("id", " _2  ")  # Should become _2
        inp_root[1].set("id", "  id -  25 F.G  ")  # Should become id-25-F.G
        inp_root[1][0].set("id", "#56")  # Can't be corrected so don't change
        inp_root[1][0][-1].set("id", "    ")  # Should be deleted
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root.get("id"), "A1")
        self.assertEqual(out_root[0].get("id"), "_25")
        self.assertEqual(out_root[0][1].get("id"), "_2")
        self.assertEqual(out_root[1].get("id"), "id-25-F.G")
        self.assertEqual(out_root[1][0].get("id"), "#56")
        self.assertEqual(out_root[1][0][-1].get("id"), None)


class TestElementCaseLowerer(ActionTestCase):
    action_class = LowercaseElements

    def test_elements_name_lowercasing(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root.tag = "EAD"
        inp_root[0][0].tag = "EADID"
        inp_root[0][0].set("COUNTRYCODE", inp_root[0][0].attrib.pop("countrycode"))
        inp_root[1][0].tag = "DID"
        inp_root[1][0][2].tag = "UNITDATE"
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root.tag, "ead")
        self.assertEqual(out_root[0].tag, "eadheader")
        self.assertEqual(out_root[0][0].tag, "eadid")
        self.assertEqual(out_root[0][0].get("countrycode"), None)
        self.assertEqual(out_root[0][0].get("COUNTRYCODE"), "FR")
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(out_root[1][0][0].tag, "unitid")
        self.assertEqual(out_root[1][0][2].tag, "unitdate")

    def test_elements_name_lowercasing_with_comments(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root.tag = "EAD"
        inp_root[0].tag = "EADHEADER"
        inp_root[0][0].tag = "EADID"
        inp_root.insert(0, etree.Comment("A simple comment"))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root.tag, "ead")
        self.assertEqual(out_root[1].tag, "eadheader")
        self.assertEqual(out_root[1][0].tag, "eadid")


class TestCOTHERlevelConverter(ActionTestCase):
    action_class = COTHERlevelConverter

    def test_c_otherlevel_converter(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        c_elt = etree.fromstring('<c level="collection"></c>')
        did_elt = etree.fromstring(DATA2)
        c_elt.append(did_elt)
        c_elt.set("level", "otherlevel")
        c_elt.set("OTHERlevel", "TEST001")
        inp_root[1][1][0].append(c_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].get("level"), "collection")
        self.assertEqual(out_root[1][1][0].get("otherlevel"), None)
        self.assertEqual(out_root[1][1][0][1].get("level"), "otherlevel")
        self.assertEqual(out_root[1][1][0][1].get("otherlevel"), "TEST001")
        self.assertEqual(out_root[1][1][0][1].get("OTHERlevel"), None)


class TestUnitdateCertainlyConverter(ActionTestCase):
    action_class = UnitdateCertainlyConverter

    def test_unitdate_certainly_converter(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        inp_root[1][0][2].set("certainty", "TEST001")
        inp_root[1][1][0][0][2].set("certainly", "TEST002")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][0][2].get("certainty"), "TEST001")
        self.assertEqual(out_root[1][0][2].get("certainly"), None)
        self.assertEqual(out_root[1][1][0][0][2].get("certainty"), "TEST002")
        self.assertEqual(out_root[1][1][0][0][2].get("certainly"), None)


class TestIdentifierConverter(ActionTestCase):
    action_class = IdentifierConverter

    def test_id_converter_without_identifier(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root[0][0].attrib.pop("identifier")
        inp_root[0][0].set("id", "TEST001")
        inp_root[1][0][0].set("id", "TEST002")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][0].get("identifier"), "TEST001")
        self.assertEqual(out_root[0][0].get("id"), None)
        self.assertEqual(out_root[1][0][0].get("identifier"), "TEST002")
        self.assertEqual(out_root[1][0][0].get("id"), None)

    def test_id_converter_with_identifier(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root[0][0].set("id", "TEST001")
        inp_root[1][0][0].set("identifier", "ID2")
        inp_root[1][0][0].set("id", "TEST002")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][0].get("identifier"), "ID1")
        self.assertEqual(out_root[0][0].get("id"), None)
        self.assertEqual(out_root[1][0][0].get("identifier"), "ID2")
        self.assertEqual(out_root[1][0][0].get("id"), None)

    def test_identifier_converter_without_id(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root[0].set("identifier", "TEST001")
        inp_root[1].set("identifier", "TEST002")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0].get("id"), "TEST001")
        self.assertEqual(out_root[0].get("identifier"), None)
        self.assertEqual(out_root[1].get("id"), "TEST002")
        self.assertEqual(out_root[1].get("identifier"), None)

    def test_identifier_converter_wit_id(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        inp_root[0].set("identifier", "TEST001")
        inp_root[0].set("id", "ID2")
        inp_root[1].set("identifier", "TEST002")
        inp_root[1].set("id", "ID3")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0].get("id"), "ID2")
        self.assertEqual(out_root[0].get("identifier"), None)
        self.assertEqual(out_root[1].get("id"), "ID3")
        self.assertEqual(out_root[1].get("identifier"), None)


class TestEmpyAttributesEraser(ActionTestCase):
    action_class = EmptyAttrsEraser

    def test_c_empty_attributes_eraser(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        c_elt = etree.fromstring('<c level="collection"></c>')
        did_elt = etree.fromstring(DATA2)
        c_elt.append(did_elt)
        c_elt.set("level", "")
        inp_root[1][1][0].append(c_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c")
        self.assertEqual(out_root[1][1][0].get("level"), "collection")
        self.assertEqual(out_root[1][1][0][1].tag, "c")
        self.assertEqual(out_root[1][1][0][1].get("level"), None)

    def test_c01_c02_c03_empty_attributes_eraser(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt[0].tag = "c01"
        dsc_elt[0].set("level", "")
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        c_elt = etree.fromstring('<c level="collection"></c>')
        c_elt.tag = "c02"
        c_elt.set("level", "")
        did_elt = etree.fromstring(DATA2)
        c_elt.append(did_elt)
        inp_root[1][1][0].append(c_elt)
        c_elt = etree.fromstring('<c level="collection"></c>')
        c_elt.tag = "c03"
        c_elt.set("level", "")
        did_elt = etree.fromstring(DATA2)
        c_elt.append(did_elt)
        inp_root[1][1][0][1].append(c_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c01")
        self.assertEqual(out_root[1][1][0].get("level"), None)
        self.assertEqual(out_root[1][1][0][1].tag, "c02")
        self.assertEqual(out_root[1][1][0][1].get("level"), None)
        self.assertEqual(out_root[1][1][0][1][1].tag, "c03")
        self.assertEqual(out_root[1][1][0][1][1].get("level"), None)


class TestParagraphAdderr(ActionTestCase):
    action_class = ParagraphAdder

    def test_paragraph_adder(self):
        elt_names = (
            "accessrestrict",
            "accruals",
            "acqinfo",
            "altformavail",
            "appraisal",
            "arrangement",
            "bibliography",
            "bioghist",
            "controlaccess",
            "custodhist",
            "descgrp",
            "dsc",
            "fileplan",
            "odd",
            "originalsloc",
            "otherfindaid",
            "phystech",
            "prefercite",
            "processinfo",
            "relatedmaterial",
            "scopecontent",
            "separatedmaterial",
            "seriesstmt",
            "userestrict",
        )
        for name in elt_names:
            with self.subTest(element_name=name):
                inp_root = etree.fromstring(DATA1)
                did_elt = etree.fromstring(DATA2)
                inp_root[1].append(did_elt)
                elt = etree.Element(name)
                elt.append(etree.Element("head"))
                elt[0].text = "TEST01"
                inp_root[1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, name)
                self.assertEqual(len(out_root[1][1]), 2)
                self.assertEqual(out_root[1][1][0].tag, "head")
                self.assertEqual(out_root[1][1][0].text, "TEST01")
                self.assertEqual(out_root[1][1][1].tag, "p")
                self.assertEqual(out_root[1][1][1].text or "", "")


class TestEmptyElementsEraser(ActionTestCase):
    action_class = EmptyEltsEraser

    def test_archdesc_subelements_with_text(self):
        elt_names = (
            "accessrestrict",
            "accruals",
            "acqinfo",
            "altformavail",
            "appraisal",
            "arrangement",
            "bibliography",
            "bioghist",
            "controlaccess",
            "custodhist",
            "descgrp",
            "dsc",
            "fileplan",
            "note",
            "odd",
            "originalsloc",
            "otherfindaid",
            "phystech",
            "prefercite",
            "processinfo",
            "relatedmaterial",
            "scopecontent",
            "separatedmaterial",
            "seriesstmt",
            "userestrict",
        )
        for name in elt_names:
            with self.subTest(subelement_name=name):
                inp_root = etree.fromstring(DATA1)
                did_elt = etree.fromstring(DATA2)
                inp_root[1].append(did_elt)
                elt = etree.Element(name)
                elt.text = "TEST01"
                inp_root[1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, name)
                self.assertEqual(len(out_root[1][1]), 1)
                self.assertEqual(out_root[1][1].text or "", "")
                self.assertEqual(out_root[1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][0].text, "TEST01")

    def test_empty_archdesc_subelements(self):
        elt_names = (
            "accessrestrict",
            "accruals",
            "acqinfo",
            "altformavail",
            "appraisal",
            "arrangement",
            "bibliography",
            "bioghist",
            "controlaccess",
            "custodhist",
            "descgrp",
            "dsc",
            "fileplan",
            "note",
            "odd",
            "originalsloc",
            "otherfindaid",
            "phystech",
            "prefercite",
            "processinfo",
            "relatedmaterial",
            "scopecontent",
            "separatedmaterial",
            "seriesstmt",
            "userestrict",
        )
        for name in elt_names:
            with self.subTest(subelement_name=name):
                inp_root = etree.fromstring(DATA1)
                did_elt = etree.fromstring(DATA2)
                inp_root[1].append(did_elt)
                elt = etree.Element(name)
                inp_root[1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(len(out_root[1]), 1)
                self.assertEqual(out_root[1][0].tag, "did")

    def test_publicationstmt_with_text(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        elt = etree.Element("publicationstmt")
        elt.text = "TEST01"
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][1].tag, "publicationstmt")
        self.assertEqual(len(out_root[0][1][1]), 1)
        self.assertEqual(out_root[0][1][1].text or "", "")
        self.assertEqual(out_root[0][1][1][0].tag, "p")
        self.assertEqual(out_root[0][1][1][0].text, "TEST01")

    def test_empty_publicationstmt(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        elt = etree.Element("publicationstmt")
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0][1]), 1)
        self.assertEqual(out_root[0][1][0].tag, "titlestmt")

    def test_empty_c(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt.insert(0, etree.Element("p"))
        dsc_elt[0].text = "TEST01"
        inp_root[1].append(dsc_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "dsc")
        self.assertEqual(len(out_root[1][1]), 1)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0].text, "TEST01")

    def test_empty_did(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.Element("did")
        inp_root[1].append(did_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[1]), 0)

    def test_empty_notestmt(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        elt = etree.Element("notestmt")
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0][1]), 1)
        self.assertEqual(out_root[0][1][0].tag, "titlestmt")

    def test_empty_profiledesc(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        elt = etree.Element("profiledesc")
        inp_root[0].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(out_root[0][0].tag, "eadid")
        self.assertEqual(out_root[0][1].tag, "filedesc")

    def test_empty_revisiondesc(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        elt = etree.Element("revisiondesc")
        inp_root[0].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(out_root[0][0].tag, "eadid")
        self.assertEqual(out_root[0][1].tag, "filedesc")

    def test_empty_change(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        data = (
            "<revisiondesc><change><date>2022-07-31</date>"
            + "<item>TEST01</item></change></revisiondesc>"
        )
        elt = etree.fromstring(data)
        elt.append(etree.Element("change"))
        inp_root[0].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2].tag, "revisiondesc")
        self.assertEqual(len(out_root[0][2]), 1)
        self.assertEqual(out_root[0][2][0].tag, "change")
        self.assertEqual(len(out_root[0][2][0]), 2)

    def test_empty_text_level_elements(self):
        elt_names = (
            "address",
            "list",
            "table",
        )
        for name in elt_names:
            with self.subTest(element_name=name):
                inp_root = etree.fromstring(DATA1)
                did_elt = etree.fromstring(DATA2)
                inp_root[1].append(did_elt)
                elt = etree.Element("accessrestrict")
                elt.append(etree.Element(name))
                elt.append(etree.Element("p"))
                elt[1].text = "TEST01"
                inp_root[1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "accessrestrict")
                self.assertEqual(len(out_root[1][1]), 1)
                self.assertEqual(out_root[1][1][0].tag, "p")
                self.assertEqual(out_root[1][1][0].text, "TEST01")


class TestCChildrenOrderer(ActionTestCase):
    action_class = CChildrenOrderer

    def test_reordering_element_before_did(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt[0].set("id", "TEST")
        dsc_elt[0].append(etree.fromstring("<fileplan><p>TEST01</p></fileplan>"))
        dsc_elt[0].append(etree.fromstring("<note><p>TEST02</p></note>"))
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        c_elt_1 = etree.Element("c")
        did_elt = etree.fromstring(DATA2)
        c_elt_1.append(did_elt)
        dsc_elt[0].append(c_elt_1)
        c_elt_2 = etree.Element("c")
        did_elt = etree.fromstring(DATA2)
        c_elt_2.append(did_elt)
        dsc_elt[0].append(c_elt_2)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c")
        self.assertEqual(out_root[1][1][0].get("id"), "TEST")
        self.assertEqual(len(out_root[1][1][0]), 5)
        self.assertEqual(out_root[1][1][0][0].tag, "did")
        self.assertEqual(out_root[1][1][0][-2].tag, "c")
        self.assertEqual(out_root[1][1][0][-1].tag, "c")
        self.assertEqual(out_root[1][1][0][1].tag, "fileplan")
        self.assertEqual(out_root[1][1][0][1][0].text, "TEST01")
        self.assertEqual(out_root[1][1][0][2][0].text, "TEST02")

    def test_reordering_element_after_c(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt[0].set("id", "TEST")
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        c_elt_1 = etree.Element("c")
        did_elt = etree.fromstring(DATA2)
        c_elt_1.append(did_elt)
        dsc_elt[0].append(c_elt_1)
        dsc_elt[0].append(etree.fromstring("<fileplan><p>TEST01</p></fileplan>"))
        c_elt_2 = etree.Element("c")
        did_elt = etree.fromstring(DATA2)
        c_elt_2.append(did_elt)
        dsc_elt[0].append(c_elt_2)
        dsc_elt[0].append(etree.fromstring("<note><p>TEST02</p></note>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c")
        self.assertEqual(out_root[1][1][0].get("id"), "TEST")
        self.assertEqual(len(out_root[1][1][0]), 5)
        self.assertEqual(out_root[1][1][0][0].tag, "did")
        self.assertEqual(out_root[1][1][0][-2].tag, "c")
        self.assertEqual(out_root[1][1][0][-1].tag, "c")
        self.assertEqual(out_root[1][1][0][1].tag, "fileplan")
        self.assertEqual(out_root[1][1][0][1][0].text, "TEST01")
        self.assertEqual(out_root[1][1][0][2][0].text, "TEST02")


class TestArchdescChildrenOrderer(ActionTestCase):
    action_class = ArchdescChildrenOrderer

    def test_reordering_elements_before_did(self):
        eltnames = (
            "accessrestrict",
            "accruals",
            "acqinfo",
            "altformavail",
            "appraisal",
            "arrangement",
            "bibliography",
            "bioghist",
            "controlaccess",
            "custodhist",
            "descgrp",
            "fileplan",
            "index",
            "note",
            "odd",
            "originalsloc",
            "otherfindaid",
            "phystech",
            "prefercite",
            "processinfo",
            "relatedmaterial",
            "scopecontent",
            "separatedmaterial",
            "userestrict",
        )
        for name in eltnames:
            with self.subTest(sub_element=name):
                inp_root = etree.fromstring(DATA1)
                elt = etree.Element(name)
                elt.append(etree.Element("p"))
                elt[0].text = "TEST01"
                inp_root[1].append(elt)
                elt = etree.Element(name)
                elt.append(etree.Element("p"))
                elt[0].text = "TEST02"
                inp_root[1].append(elt)
                did_elt = etree.fromstring(DATA2)
                did_elt.set("id", "TEST03")
                inp_root[1].append(did_elt)
                dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
                dsc_elt.set("id", "TEST04")
                did_elt = etree.fromstring(DATA2)
                dsc_elt[0].append(did_elt)
                inp_root[1].append(dsc_elt)
                dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
                dsc_elt.set("id", "TEST05")
                did_elt = etree.fromstring(DATA2)
                dsc_elt[0].append(did_elt)
                inp_root[1].append(dsc_elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(len(out_root[1]), 5)
                self.assertEqual(out_root[1][0].tag, "did")
                self.assertEqual(out_root[1][0].get("id"), "TEST03")
                self.assertEqual(out_root[1][-2].tag, "dsc")
                self.assertEqual(out_root[1][-2].get("id"), "TEST04")
                self.assertEqual(out_root[1][-1].tag, "dsc")
                self.assertEqual(out_root[1][-1].get("id"), "TEST05")
                self.assertEqual(out_root[1][1].tag, name)
                self.assertEqual(out_root[1][1][0].text, "TEST01")
                self.assertEqual(out_root[1][2].tag, name)
                self.assertEqual(out_root[1][2][0].text, "TEST02")

    def test_reordering_elements_after_dsc(self):
        eltnames = (
            "accessrestrict",
            "accruals",
            "acqinfo",
            "altformavail",
            "appraisal",
            "arrangement",
            "bibliography",
            "bioghist",
            "controlaccess",
            "custodhist",
            "descgrp",
            "fileplan",
            "index",
            "note",
            "odd",
            "originalsloc",
            "otherfindaid",
            "phystech",
            "prefercite",
            "processinfo",
            "relatedmaterial",
            "scopecontent",
            "separatedmaterial",
            "userestrict",
        )
        for name in eltnames:
            with self.subTest(sub_element=name):
                inp_root = etree.fromstring(DATA1)
                did_elt = etree.fromstring(DATA2)
                did_elt.set("id", "TEST03")
                inp_root[1].append(did_elt)
                dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
                dsc_elt.set("id", "TEST04")
                did_elt = etree.fromstring(DATA2)
                dsc_elt[0].append(did_elt)
                inp_root[1].append(dsc_elt)
                elt = etree.Element(name)
                elt.append(etree.Element("p"))
                elt[0].text = "TEST01"
                inp_root[1].append(elt)
                dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
                dsc_elt.set("id", "TEST05")
                did_elt = etree.fromstring(DATA2)
                dsc_elt[0].append(did_elt)
                inp_root[1].append(dsc_elt)
                elt = etree.Element(name)
                elt.append(etree.Element("p"))
                elt[0].text = "TEST02"
                inp_root[1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(len(out_root[1]), 5)
                self.assertEqual(out_root[1][0].tag, "did")
                self.assertEqual(out_root[1][0].get("id"), "TEST03")
                self.assertEqual(out_root[1][-2].tag, "dsc")
                self.assertEqual(out_root[1][-2].get("id"), "TEST04")
                self.assertEqual(out_root[1][-1].tag, "dsc")
                self.assertEqual(out_root[1][-1].get("id"), "TEST05")
                self.assertEqual(out_root[1][1].tag, name)
                self.assertEqual(out_root[1][1][0].text, "TEST01")
                self.assertEqual(out_root[1][2].tag, name)
                self.assertEqual(out_root[1][2][0].text, "TEST02")

    def test_reordering_dao_elements_before_did(self):
        inp_root = etree.fromstring(DATA1)
        elt = etree.Element("daogrp")
        elt.append(etree.Element("daoloc"))
        elt[0].set("href", "TEST01")
        inp_root[1].append(elt)
        elt = etree.Element("dao")
        elt.set("href", "TEST02")
        inp_root[1].append(elt)
        did_elt = etree.fromstring(DATA2)
        did_elt.set("id", "TEST03")
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt.set("id", "TEST04")
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt.set("id", "TEST05")
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[1]), 5)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(out_root[1][0].get("id"), "TEST03")
        self.assertEqual(out_root[1][-2].tag, "dsc")
        self.assertEqual(out_root[1][-2].get("id"), "TEST04")
        self.assertEqual(out_root[1][-1].tag, "dsc")
        self.assertEqual(out_root[1][-1].get("id"), "TEST05")
        self.assertEqual(out_root[1][1].tag, "daogrp")
        self.assertEqual(out_root[1][1][0].get("href"), "TEST01")
        self.assertEqual(out_root[1][2].tag, "dao")
        self.assertEqual(out_root[1][2].get("href"), "TEST02")

    def test_reordering_dao_elements_after_dsc(self):
        inp_root = etree.fromstring(DATA1)
        did_elt = etree.fromstring(DATA2)
        did_elt.set("id", "TEST03")
        inp_root[1].append(did_elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt.set("id", "TEST04")
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        elt = etree.Element("daogrp")
        elt.append(etree.Element("daoloc"))
        elt[0].set("href", "TEST01")
        inp_root[1].append(elt)
        dsc_elt = etree.fromstring('<dsc><c level="collection"></c></dsc>')
        dsc_elt.set("id", "TEST05")
        did_elt = etree.fromstring(DATA2)
        dsc_elt[0].append(did_elt)
        inp_root[1].append(dsc_elt)
        elt = etree.Element("dao")
        elt.set("href", "TEST02")
        inp_root[1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[1]), 5)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(out_root[1][0].get("id"), "TEST03")
        self.assertEqual(out_root[1][-2].tag, "dsc")
        self.assertEqual(out_root[1][-2].get("id"), "TEST04")
        self.assertEqual(out_root[1][-1].tag, "dsc")
        self.assertEqual(out_root[1][-1].get("id"), "TEST05")
        self.assertEqual(out_root[1][1].tag, "daogrp")
        self.assertEqual(out_root[1][1][0].get("href"), "TEST01")
        self.assertEqual(out_root[1][2].tag, "dao")
        self.assertEqual(out_root[1][2].get("href"), "TEST02")


class TestEadheaderChildrenOrderer(ActionTestCase):
    action_class = EadheaderChildrenOrderer

    def test_children_ordering(self):
        inp_root = etree.fromstring(DATA1)
        inp_root[0].insert(0, inp_root[0][1])
        inp_root[0].insert(0, etree.Element("profiledesc"))
        inp_root[0][0].text = "TEST01"
        inp_root[0].insert(0, etree.Element("revisiondesc"))
        data = "<change><date>2022-07-31</date><item>TEST02</item></change>"
        inp_root[0][0].append(etree.fromstring(data))
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 4)
        self.assertEqual(out_root[0][0].tag, "eadid")
        self.assertEqual(out_root[0][0].get("identifier"), "ID1")
        self.assertEqual(out_root[0][1].tag, "filedesc")
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1")
        self.assertEqual(out_root[0][2].tag, "profiledesc")
        self.assertEqual(out_root[0][2].text, "TEST01")
        self.assertEqual(out_root[0][3].tag, "revisiondesc")
        self.assertEqual(out_root[0][3][0][1].tag, "item")
        self.assertEqual(out_root[0][3][0][1].text, "TEST02")

    def test_children_ordering_nothing_to_do(self):
        inp_root = etree.fromstring(DATA1)
        inp_root[0].append(etree.Element("profiledesc"))
        inp_root[0][-1].text = "TEST01"
        inp_root[0].append(etree.Element("revisiondesc"))
        data = "<change><date>2022-07-31</date><item>TEST02</item></change>"
        inp_root[0][-1].append(etree.fromstring(data))
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 4)
        self.assertEqual(out_root[0][0].tag, "eadid")
        self.assertEqual(out_root[0][0].get("identifier"), "ID1")
        self.assertEqual(out_root[0][1].tag, "filedesc")
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1")
        self.assertEqual(out_root[0][2].tag, "profiledesc")
        self.assertEqual(out_root[0][2].text, "TEST01")
        self.assertEqual(out_root[0][3].tag, "revisiondesc")
        self.assertEqual(out_root[0][3][0][1].tag, "item")
        self.assertEqual(out_root[0][3][0][1].text, "TEST02")


class TestChangeChildrenOrderer(ActionTestCase):
    action_class = ChangeChildrenOrderer

    def test_children_ordering(self):
        inp_root = etree.fromstring(DATA1)
        inp_root[0].append(etree.Element("revisiondesc"))
        data = "<change><date>2022-07-29</date><item>TEST01</item></change>"
        inp_root[0][-1].append(etree.fromstring(data))
        data = "<change><item>TEST02</item><date>2022-07-30</date><item>TEST03</item></change>"
        inp_root[0][-1].append(etree.fromstring(data))
        data = "<change><item>TEST04</item><item>TEST05</item><date>2022-07-31</date></change>"
        inp_root[0][-1].append(etree.fromstring(data))
        did_elt = etree.fromstring(DATA2)
        inp_root[1].append(did_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][-1].tag, "revisiondesc")
        self.assertEqual(len(out_root[0][-1]), 3)
        self.assertEqual(out_root[0][-1][0].tag, "change")
        self.assertEqual(out_root[0][-1][0][0].tag, "date")
        self.assertEqual(out_root[0][-1][0][0].text, "2022-07-29")
        self.assertEqual(out_root[0][-1][0][1].tag, "item")
        self.assertEqual(out_root[0][-1][0][1].text, "TEST01")
        self.assertEqual(out_root[0][-1][1].tag, "change")
        self.assertEqual(out_root[0][-1][1][0].tag, "date")
        self.assertEqual(out_root[0][-1][1][0].text, "2022-07-30")
        self.assertEqual(out_root[0][-1][1][1].tag, "item")
        self.assertEqual(out_root[0][-1][1][1].text, "TEST02")
        self.assertEqual(out_root[0][-1][1][2].tag, "item")
        self.assertEqual(out_root[0][-1][1][2].text, "TEST03")
        self.assertEqual(out_root[0][-1][2].tag, "change")
        self.assertEqual(out_root[0][-1][2][0].tag, "date")
        self.assertEqual(out_root[0][-1][2][0].text, "2022-07-31")
        self.assertEqual(out_root[0][-1][2][1].tag, "item")
        self.assertEqual(out_root[0][-1][2][1].text, "TEST04")
        self.assertEqual(out_root[0][-1][2][2].tag, "item")
        self.assertEqual(out_root[0][-1][2][2].text, "TEST05")


if __name__ == "__main__":
    unittest.main()
