# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.header import (
    IdentifiersDefiner,
    EditionstmtConverter,
    NotestmtConverter,
    FrontmatterConverter,
    SponsorConverter,
    StmtPNumEraser,
)


DATA = """
<ead xmlns:xlink="http://www.w3.org/1999/xlink">
  <eadheader>
    <eadid countrycode="FR" identifier="ID1"
           mainagencycode="LGLB-2022">LGLB-2022-ID1</eadid>
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


class TestIdentifiersDefiner(ActionTestCase):
    action_class = IdentifiersDefiner

    def test_country_code_fr(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(inp_root, params={"country_code": "fr"})
        self.assertEqual(out_root[0][0].get("countrycode"), "FR")

    def test_country_code_other_than_fr(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(inp_root, params={"country_code": "de"})
        self.assertEqual(out_root[0][0].get("countrycode"), "FR")

    def test_agency_code(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(inp_root, params={"agency_code": "LGLB-0001"})
        self.assertEqual(out_root[0][0].get("mainagencycode"), "LGLB-0001")

    def test_document_id_with_no_favour_xml(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(inp_root, params={"document_id": "LGLB-0001"})
        self.assertEqual(out_root[0][0].get("identifier"), "LGLB-0001")

    def test_document_id_with_favour_xml(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(
            inp_root,
            params={
                "document_id": "LGLB-0001",
                "favour_xml_document_id": True,
            },
        )
        self.assertEqual(out_root[0][0].get("identifier"), "LGLB-2022-ID1")

    def test_no_document_id_with_favour_xml(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(
            inp_root,
            params={
                "favour_xml_document_id": True,
            },
        )
        self.assertEqual(out_root[0][0].get("identifier"), "LGLB-2022-ID1")

    def test_no_document_id_with_no_favour_xml(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][0].attrib.clear()
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][0].get("identifier"), None)


class TestEditionstmtConverter(ActionTestCase):
    action_class = EditionstmtConverter

    def test_convert_with_no_odd(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.Element("editionstmt")
        elt.append(etree.fromstring("<edition>TEST01</edition>"))
        elt.append(etree.fromstring("<edition>TEST02</edition>"))
        elt.append(etree.fromstring("<p>TEST03.1</p>"))
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "Editions")
        self.assertEqual(out_root[1][1][1].tag, "list")
        self.assertEqual(out_root[1][1][1][0].tag, "item")
        self.assertEqual(len(out_root[1][1][1][0]), 1)
        self.assertEqual(out_root[1][1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][0][0].text, "TEST01")
        self.assertEqual(out_root[1][1][1][0][0].tail, ": ")
        self.assertEqual(out_root[1][1][1][1].tag, "item")
        self.assertEqual(len(out_root[1][1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][1][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][1][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][1][0].text, "TEST02")
        self.assertEqual(out_root[1][1][1][1][0].tail, ": TEST03.1")

    def test_convert_with_odd(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.Element("editionstmt")
        elt.append(etree.fromstring("<edition>TEST01</edition>"))
        elt.append(etree.fromstring("<edition>TEST02</edition>"))
        elt.append(etree.fromstring("<p>TEST03.1</p>"))
        inp_root[0][1].append(elt)
        inp_root[1].append(etree.fromstring("<odd><p>TEST10</p></odd>"))
        inp_root[1].append(etree.fromstring("<odd><p>TEST11</p></odd>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(len(out_root[1]), 3)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 3)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0].text, "TEST10")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(out_root[1][1][1][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][0].text, "Editions")
        self.assertEqual(out_root[1][1][2].tag, "list")
        self.assertEqual(out_root[1][1][2][0].tag, "item")
        self.assertEqual(len(out_root[1][1][2][0]), 1)
        self.assertEqual(out_root[1][1][2][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][2][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][2][0][0].text, "TEST01")
        self.assertEqual(out_root[1][1][2][0][0].tail, ": ")
        self.assertEqual(out_root[1][1][2][1].tag, "item")
        self.assertEqual(len(out_root[1][1][2][1]), 1)
        self.assertEqual(out_root[1][1][2][1][0].tag, "emph")
        self.assertEqual(out_root[1][1][2][1][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][2][1][0].text, "TEST02")
        self.assertEqual(out_root[1][1][2][1][0].tail, ": TEST03.1")
        self.assertEqual(out_root[1][2].tag, "odd")
        self.assertEqual(len(out_root[1][2]), 1)
        self.assertEqual(out_root[1][2][0].tag, "p")
        self.assertEqual(out_root[1][2][0].text, "TEST11")

    def test_convert_with_title(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.Element("editionstmt")
        elt.append(etree.fromstring("<edition>TEST01</edition>"))
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root, params={"title": "TEST-XX"})
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "TEST-XX")
        self.assertEqual(out_root[1][1][1].tag, "list")
        self.assertEqual(out_root[1][1][1][0].tag, "item")
        self.assertEqual(len(out_root[1][1][1][0]), 1)
        self.assertEqual(out_root[1][1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][0][0].text, "TEST01")
        self.assertEqual(out_root[1][1][1][0][0].tail, ": ")


class TestNotestmtConverter(ActionTestCase):
    action_class = NotestmtConverter

    def test_convert_with_no_odd(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.Element("notestmt")
        elt.append(etree.fromstring("<note><p>TEST01</p></note>"))
        elt.append(etree.fromstring("<note><p>TEST02</p><p>TEST03</p></note>"))
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 3)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "Notes")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "note")
        self.assertEqual(out_root[1][1][1][0][0].tag, "p")
        self.assertEqual(out_root[1][1][1][0][0].text, "TEST01")
        self.assertEqual(out_root[1][1][2].tag, "p")
        self.assertEqual(len(out_root[1][1][2]), 1)
        self.assertEqual(out_root[1][1][2][0].tag, "note")
        self.assertEqual(out_root[1][1][2][0][0].tag, "p")
        self.assertEqual(out_root[1][1][2][0][0].text, "TEST02")
        self.assertEqual(out_root[1][1][2][0][1].tag, "p")
        self.assertEqual(out_root[1][1][2][0][1].text, "TEST03")

    def test_convert_with_odd(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.Element("notestmt")
        elt.append(etree.fromstring("<note><p>TEST01</p></note>"))
        elt.append(etree.fromstring("<note><p>TEST02</p><p>TEST03</p></note>"))
        inp_root[0][1].append(elt)
        inp_root[1].append(etree.fromstring("<odd><p>TEST10</p></odd>"))
        inp_root[1].append(etree.fromstring("<odd><p>TEST11</p></odd>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(len(out_root[1]), 3)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 4)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0].text, "TEST10")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(out_root[1][1][1][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][0].text, "Notes")
        self.assertEqual(out_root[1][1][2].tag, "p")
        self.assertEqual(len(out_root[1][1][2]), 1)
        self.assertEqual(out_root[1][1][2][0].tag, "note")
        self.assertEqual(out_root[1][1][2][0][0].tag, "p")
        self.assertEqual(out_root[1][1][2][0][0].text, "TEST01")
        self.assertEqual(out_root[1][1][3].tag, "p")
        self.assertEqual(len(out_root[1][1][3]), 1)
        self.assertEqual(out_root[1][1][3][0].tag, "note")
        self.assertEqual(out_root[1][1][3][0][0].tag, "p")
        self.assertEqual(out_root[1][1][3][0][0].text, "TEST02")
        self.assertEqual(out_root[1][1][3][0][1].tag, "p")
        self.assertEqual(out_root[1][1][3][0][1].text, "TEST03")

    def test_convert_with_title(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.Element("notestmt")
        elt.append(etree.fromstring("<note><p>TEST01</p></note>"))
        inp_root[0][1].append(elt)
        out_root = self.run_action(inp_root, params={"title": "TEST-XX"})
        self.assertEqual(len(out_root[0]), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "TEST-XX")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(len(out_root[1][1][1]), 1)
        self.assertEqual(out_root[1][1][1][0].tag, "note")
        self.assertEqual(out_root[1][1][1][0][0].tag, "p")
        self.assertEqual(out_root[1][1][1][0][0].text, "TEST01")


class TestFrontmatterConverter(ActionTestCase):
    action_class = FrontmatterConverter

    def test_convert_with_no_odd(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.fromstring(
            "<frontmatter><div><p>TEST01</p><p>TEST02</p></div>"
            + "<div><p>TEST03</p><div><p>TEST04</p></div></div></frontmatter>"
        )
        inp_root.insert(1, elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 5)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "Prolegomena")
        for idx in range(4):
            self.assertEqual(out_root[1][1][idx + 1].tag, "p")
            self.assertEqual(out_root[1][1][idx + 1].text, f"TEST0{idx + 1}")

    def test_convert_with_odd(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.fromstring(
            "<frontmatter><div><p>TEST01</p><div><p>TEST02</p></div></div>"
            + "<div><p>TEST03</p><p>TEST04</p></div></frontmatter>"
        )
        inp_root.insert(1, elt)
        inp_root[2].append(etree.fromstring("<odd><p>TEST10</p></odd>"))
        inp_root[2].append(etree.fromstring("<odd><p>TEST11</p></odd>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root), 2)
        self.assertEqual(len(out_root[1]), 3)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 6)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0].text, "TEST10")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(out_root[1][1][1][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][0].text, "Prolegomena")
        for idx in range(4):
            self.assertEqual(out_root[1][1][idx + 2].tag, "p")
            self.assertEqual(out_root[1][1][idx + 2].text, f"TEST0{idx + 1}")
        self.assertEqual(out_root[1][2].tag, "odd")
        self.assertEqual(len(out_root[1][2]), 1)
        self.assertEqual(out_root[1][2][0].tag, "p")
        self.assertEqual(out_root[1][2][0].text, "TEST11")

    def test_convert_with_title(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.fromstring(
            "<frontmatter><div><p>TEST01</p></div><div><p>TEST02</p></div>"
            "</frontmatter>"
        )
        inp_root.insert(1, elt)
        out_root = self.run_action(inp_root, params={"title": "TEST20"})
        self.assertEqual(len(out_root), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 3)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "TEST20")
        for idx in range(2):
            self.assertEqual(out_root[1][1][idx + 1].tag, "p")
            self.assertEqual(out_root[1][1][idx + 1].text, f"TEST0{idx + 1}")

    def test_convert_titlepage(self):
        inp_root = etree.fromstring(DATA)
        elt = etree.fromstring(
            "<frontmatter><titlepage><p>TEST01</p></titlepage><div>"
            "<p>TEST02</p></div></frontmatter>"
        )
        inp_root.insert(1, elt)
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root), 2)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "Prolegomena")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(out_root[1][1][1].text, "TEST02")


class TestSponsorConverter(ActionTestCase):
    action_class = SponsorConverter

    def test_convert_with_no_odd(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0].append(etree.Element("sponsor"))
        inp_root[0][1][0][1].text = "TEST01"
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0][1][0]), 1)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 1)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "Sponsor:")
        self.assertEqual(out_root[1][1][0][0].tail, " TEST01")

    def test_convert_with_odd(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0].append(etree.Element("sponsor"))
        inp_root[0][1][0][1].text = "TEST01"
        inp_root[1].append(etree.fromstring("<odd><p>TEST10</p></odd>"))
        inp_root[1].append(etree.fromstring("<odd><p>TEST11</p></odd>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0][1][0]), 1)
        self.assertEqual(len(out_root[1]), 3)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 2)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0].text, "TEST10")
        self.assertEqual(out_root[1][1][1].tag, "p")
        self.assertEqual(out_root[1][1][1][0].tag, "emph")
        self.assertEqual(out_root[1][1][1][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][1][0].text, "Sponsor:")
        self.assertEqual(out_root[1][1][1][0].tail, " TEST01")
        self.assertEqual(out_root[1][2].tag, "odd")
        self.assertEqual(len(out_root[1][2]), 1)
        self.assertEqual(out_root[1][2][0].tag, "p")
        self.assertEqual(out_root[1][2][0].text, "TEST11")

    def test_convert_with_title(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0].append(etree.Element("sponsor"))
        inp_root[0][1][0][1].text = "TEST01"
        out_root = self.run_action(inp_root, params={"title": "TEST20"})
        self.assertEqual(len(out_root[0][1][0]), 1)
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][1].tag, "odd")
        self.assertEqual(len(out_root[1][1]), 1)
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][0].tag, "emph")
        self.assertEqual(out_root[1][1][0][0].get("render"), "bold")
        self.assertEqual(out_root[1][1][0][0].text, "TEST20")
        self.assertEqual(out_root[1][1][0][0].tail, " TEST01")


class TestStmtPNumEraser(ActionTestCase):
    action_class = StmtPNumEraser

    def test_erase_in_publicationstmt(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1].append(
            etree.fromstring(
                "<publicationstmt><p>TEST01</p><date>2022-07-31</date>"
                + "<num>TEST02</num></publicationstmt>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0][1]), 2)
        self.assertEqual(out_root[0][1][1].tag, "publicationstmt")
        self.assertEqual(len(out_root[0][1][1]), 1)
        self.assertEqual(out_root[0][1][1][0].tag, "date")
        self.assertEqual(out_root[0][1][1][0].text, "2022-07-31")

    def test_erase_in_seriesstmt(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1].append(
            etree.fromstring(
                "<seriesstmt><p>TEST01</p><titleproper>TEST02</titleproper>"
                + "<num>TEST03</num></seriesstmt>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(len(out_root[0][1]), 2)
        self.assertEqual(out_root[0][1][1].tag, "seriesstmt")
        self.assertEqual(len(out_root[0][1][1]), 1)
        self.assertEqual(out_root[0][1][1][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][1][0].text, "TEST02")


if __name__ == "__main__":
    unittest.main()
