# -*- coding: utf-8 -*-
import unittest
from itertools import product

from lxml import etree

from test import ActionTestCase
from glamconv.ead.arch_data import (
    NumberedCConverter,
    HierarchicalArchEltsCollapser,
    ArchEltsLinksInPMover,
    ArchdescCNoteInDidMover,
    DidAbstractConverter,
    UnittitleUnitdateInDidCopier,
    IncorrectNormalDateEraser,
)


DATA = """
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
    <did xmlns:xlink="http://www.w3.org/1999/xlink">
      <unitid>UID1</unitid>
      <unittitle>Exemple 1</unittitle>
      <unitdate>2016-2022</unitdate>
      <dao xlink:href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
  </archdesc>
</ead>
"""

DATA2 = """
    <did xmlns:xlink="http://www.w3.org/1999/xlink">
      <unitid>{}</unitid>
      <unittitle>Exemple 1</unittitle>
      <unitdate>2016-2022</unitdate>
      <dao xlink:href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
"""


class TestNumberedCConverter(ActionTestCase):
    action_class = NumberedCConverter

    def test_converter(self):
        inp_root = etree.fromstring(DATA)
        dsc_elt = etree.Element("dsc")
        inp_root[1].append(dsc_elt)
        c1_elt = etree.Element("c01")
        c1_elt.append(etree.fromstring(DATA2.format("ID01")))
        dsc_elt.append(c1_elt)
        c2_elt = etree.Element("c02")
        c2_elt.append(etree.fromstring(DATA2.format("ID02-1")))
        c1_elt.append(c2_elt)
        c3_elt = etree.Element("c03")
        c3_elt.append(etree.fromstring(DATA2.format("ID03")))
        c2_elt.append(c3_elt)
        c2_elt = etree.Element("c02")
        c2_elt.append(etree.fromstring(DATA2.format("ID02-2")))
        c1_elt.append(c2_elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c")
        self.assertEqual(out_root[1][1][0][0][0].tag, "unitid")
        self.assertEqual(out_root[1][1][0][0][0].text, "ID01")
        self.assertEqual(out_root[1][1][0][1].tag, "c")
        self.assertEqual(out_root[1][1][0][1][0][0].tag, "unitid")
        self.assertEqual(out_root[1][1][0][1][0][0].text, "ID02-1")
        self.assertEqual(out_root[1][1][0][1][1].tag, "c")
        self.assertEqual(out_root[1][1][0][1][1][0][0].tag, "unitid")
        self.assertEqual(out_root[1][1][0][1][1][0][0].text, "ID03")
        self.assertEqual(out_root[1][1][0][2].tag, "c")
        self.assertEqual(out_root[1][1][0][2][0][0].tag, "unitid")
        self.assertEqual(out_root[1][1][0][2][0][0].text, "ID02-2")


class TestHierarchicalArchEltsCollapser(ActionTestCase):
    action_class = HierarchicalArchEltsCollapser

    def test_collapser(self):
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
            "fileplan",
            "odd",
            "originalsloc",
            "otherfindaid",
            "phystech",
            "prefercite",
            "relatedmaterial",
            "processinfo",
            "scopecontent",
            "separatedmaterial",
            "userestrict",
        )
        for name in eltnames:
            with self.subTest(element_name=name):
                inp_root = etree.fromstring(DATA)
                elt = etree.Element(name)
                elt.append(etree.Element("p"))
                elt[0].text = "TEST01"
                elt2 = etree.Element(name)
                elt2.append(etree.Element("p"))
                elt2[0].text = "TEST02"
                elt.append(elt2)
                elt3 = etree.Element(name)
                elt3.append(etree.Element("p"))
                elt3[0].text = "TEST03"
                elt2.append(elt3)
                elt4 = etree.Element(name)
                elt4.append(etree.Element("p"))
                elt4[0].text = "TEST04"
                elt.append(elt4)
                inp_root[1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, name)
                self.assertEqual(len(out_root[1][1]), 4)
                for num, sub_elt in enumerate(out_root[1][1]):
                    self.assertEqual(sub_elt.tag, "p")
                    self.assertEqual(sub_elt.text, f"TEST0{num + 1}")


class TestArchEltsLinksInPMover(ActionTestCase):
    action_class = ArchEltsLinksInPMover

    def test_mover(self):
        eltnames = ("otherfindaid", "relatedmaterial", "separatedmaterial")
        refnames = ("archref", "bibref", "extref", "ref")
        for name in eltnames:
            for refname in refnames:
                with self.subTest(element_name=name, ref_name=refname):
                    inp_root = etree.fromstring(DATA)
                    elt = etree.Element(name)
                    elt.append(etree.Element("p"))
                    elt[-1].text = "TEST01"
                    elt.append(etree.Element(refname))
                    elt[-1].set("href", "TEST02")
                    elt.append(etree.Element(refname))
                    elt[-1].set("href", "TEST03")
                    elt.append(etree.Element("p"))
                    elt[-1].text = "TEST04"
                    inp_root[1].append(elt)
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1].tag, name)
                    self.assertEqual(len(out_root[1][1]), 4)
                    self.assertEqual(out_root[1][1][0].tag, "p")
                    self.assertEqual(out_root[1][1][0].text, "TEST01")
                    self.assertEqual(out_root[1][1][3].tag, "p")
                    self.assertEqual(out_root[1][1][3].text, "TEST04")
                    self.assertEqual(out_root[1][1][1].tag, "p")
                    self.assertEqual(out_root[1][1][1][0].tag, refname)
                    self.assertEqual(out_root[1][1][1][0].get("href"), "TEST02")
                    self.assertEqual(out_root[1][1][2][0].tag, refname)
                    self.assertEqual(out_root[1][1][2][0].get("href"), "TEST03")


class TestArchdescCNoteInDidMover(ActionTestCase):
    action_class = ArchdescCNoteInDidMover

    def test_mover(self):
        for name, subname in (("note", "p"), ("origination", "name")):
            with self.subTest(element_name=name):
                inp_root = etree.fromstring(DATA)
                dsc_elt = etree.Element("dsc")
                inp_root[1].append(dsc_elt)
                c_elt = etree.Element("c")
                c_elt.append(etree.fromstring(DATA2.format("ID01")))
                dsc_elt.append(c_elt)
                elt = etree.Element(name)
                elt.append(etree.Element(subname))
                elt[0].text = "TEST01"
                inp_root[1].insert(1, elt)
                elt = etree.Element(name)
                elt.append(etree.Element(subname))
                elt[0].text = "TEST02"
                inp_root[1][-1][0].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(len(out_root[1]), 2)
                self.assertEqual(out_root[1][0][-1].tag, name)
                self.assertEqual(out_root[1][0][-1][0].tag, subname)
                self.assertEqual(out_root[1][0][-1][0].text, "TEST01")
                self.assertEqual(len(out_root[1][1][0]), 1)
                self.assertEqual(out_root[1][1][0][0][-1].tag, name)
                self.assertEqual(out_root[1][1][0][0][-1][0].tag, subname)
                self.assertEqual(out_root[1][1][0][0][-1][0].text, "TEST02")


class TestDidAbstractConverter(ActionTestCase):
    action_class = DidAbstractConverter

    def test_converter(self):
        inp_root = etree.fromstring(DATA)
        dsc_elt = etree.Element("dsc")
        inp_root[1].append(dsc_elt)
        c_elt = etree.Element("c")
        c_elt.append(etree.fromstring(DATA2.format("ID01")))
        dsc_elt.append(c_elt)
        elt = etree.Element("abstract")
        elt.text = "TEST01"
        inp_root[1][0].insert(2, elt)
        elt = etree.Element("abstract")
        elt.text = "TEST02"
        inp_root[1][0].append(elt)
        elt = etree.Element("abstract")
        elt.text = "TEST03"
        inp_root[1][1][0][0].insert(0, elt)
        elt = etree.Element("abstract")
        elt.text = "TEST04"
        inp_root[1][1][0][0].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(len(out_root[1][0]), 6)
        for num, idx in enumerate((2, 5)):
            self.assertEqual(out_root[1][0][idx].tag, "note")
            self.assertEqual(out_root[1][0][idx].text or "", "")
            self.assertEqual(out_root[1][0][idx][0].tag, "p")
            self.assertEqual(out_root[1][0][idx][0].text, f"TEST0{num + 1}")
        self.assertEqual(out_root[1][1][0][0].tag, "did")
        self.assertEqual(len(out_root[1][1][0][0]), 6)
        for num, idx in enumerate((0, 5)):
            self.assertEqual(out_root[1][1][0][0][idx].tag, "note")
            self.assertEqual(out_root[1][1][0][0][idx].text or "", "")
            self.assertEqual(out_root[1][1][0][0][idx][0].tag, "p")
            self.assertEqual(out_root[1][1][0][0][idx][0].text, f"TEST0{num + 3}")


class TestUnittitleUnitdateInDidCopier(ActionTestCase):
    action_class = UnittitleUnitdateInDidCopier

    def test_no_copy_with_did_unitdate(self):
        inp_root = etree.fromstring(DATA)
        dsc_elt = etree.Element("dsc")
        inp_root[1].append(dsc_elt)
        c_elt = etree.Element("c")
        c_elt.append(etree.fromstring(DATA2.format("ID01")))
        dsc_elt.append(c_elt)
        elt = etree.Element("unitdate")
        elt.text = "2022-07-31"
        elt.tail = " XX"
        inp_root[1][0][1].text += " "
        inp_root[1][0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(len(out_root[1][0]), 4)
        self.assertEqual(out_root[1][0][2].tag, "unitdate")
        self.assertEqual(out_root[1][0][2].text, "2016-2022")
        self.assertEqual((out_root[1][0][2].tail or "").strip(), "")

    def test_copy_without_did_unitdate(self):
        inp_root = etree.fromstring(DATA)
        dsc_elt = etree.Element("dsc")
        inp_root[1].append(dsc_elt)
        c_elt = etree.Element("c")
        c_elt.append(etree.fromstring(DATA2.format("ID01")))
        dsc_elt.append(c_elt)
        inp_root[1][0].remove(inp_root[1][0][2])  # remove unitdate
        elt = etree.Element("unitdate")
        elt.text = "2022-07-31"
        elt.tail = " XX"
        inp_root[1][0][1].text += " "
        inp_root[1][0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(len(out_root[1][0]), 4)
        self.assertEqual(out_root[1][0][-1].tag, "unitdate")
        self.assertEqual(out_root[1][0][-1].text, "2022-07-31")
        self.assertEqual((out_root[1][0][-1].tail or "").strip(), "")


class TestIncorrectNormalDateEraser(ActionTestCase):
    action_class = IncorrectNormalDateEraser

    def test_no_delete_with_correct_simple_date(self):
        values = (
            "20220731",
            "2022-07-31",
            "2022-07",
            "2022",
            "-01560731",
            "-0156-07-31",
            "-0156-07",
            "-0156",
        )
        for val in values:
            with self.subTest(date_value=val):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][2].set("normal", val)
                inp_root[1][0][2].text = val
                elt = etree.Element("publicationstmt")
                elt.append(etree.Element("date"))
                elt[0].set("normal", val)
                elt[0].text = val
                inp_root[0][1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][2].tag, "unitdate")
                self.assertEqual(out_root[1][0][2].text, val)
                self.assertEqual(out_root[1][0][2].get("normal"), val)
                self.assertEqual(out_root[0][1][1][0].tag, "date")
                self.assertEqual(out_root[0][1][1][0].text, val)
                self.assertEqual(out_root[0][1][1][0].get("normal"), val)

    def test_no_delete_with_correct_double_dates(self):
        values_1 = (
            "20220731",
            "2022-07-31",
            "2022-07",
            "2022",
            "-01560731",
            "-0156-07-31",
            "-0156-07",
            "-0156",
        )
        values_2 = (
            "20220831",
            "2022-08-31",
            "2022-08",
            "2022",
            "-00540731",
            "-0054-07-31",
            "-0054-07",
            "-0054",
        )
        for val1, val2 in product(values_1, values_2):
            with self.subTest(date_value_1=val1, date_value_é=val2):
                val = f"{val1}/{val2}"
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][2].set("normal", val)
                inp_root[1][0][2].text = val
                elt = etree.Element("publicationstmt")
                elt.append(etree.Element("date"))
                elt[0].set("normal", val)
                elt[0].text = val
                inp_root[0][1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][2].tag, "unitdate")
                self.assertEqual(out_root[1][0][2].text, val)
                self.assertEqual(out_root[1][0][2].get("normal"), val)
                self.assertEqual(out_root[0][1][1][0].tag, "date")
                self.assertEqual(out_root[0][1][1][0].text, val)
                self.assertEqual(out_root[0][1][1][0].get("normal"), val)

    def test_delete_with_incorrect_dates(self):
        values = (
            "220731",
            "31-07-2022",
            "07/2022",
            "-56-07",
            "31/07/2022",
            "2021 / 2022",
            "-56-07-31",
            "-56",
            "142",
            "2022-07 / 2022-08",
        )
        for val in values:
            with self.subTest(date_value=val):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][2].set("normal", val)
                inp_root[1][0][2].text = val
                elt = etree.Element("publicationstmt")
                elt.append(etree.Element("date"))
                elt[0].set("normal", val)
                elt[0].text = val
                inp_root[0][1].append(elt)
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][2].tag, "unitdate")
                self.assertEqual(out_root[1][0][2].text, val)
                self.assertEqual(out_root[1][0][2].get("normal"), None)
                self.assertEqual(out_root[0][1][1][0].tag, "date")
                self.assertEqual(out_root[0][1][1][0].text, val)
                self.assertEqual(out_root[0][1][1][0].get("normal"), None)


if __name__ == "__main__":
    unittest.main()
