# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.adjusters import (
    ArchdescLevelAttribAdjuster,
    DscTypeAttribAdjuster,
    EmphRenderAttribAdjuster,
    LanguageLangcodeAttribAdjuster,
    LanguageScriptcodeAttribAdjuster,
    ListAttribsAdjuster,
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
    <dsc type="othertype">
      <c level="collection">
        <did xmlns:xlink="http://www.w3.org/1999/xlink">
          <unitid>UID2</unitid>
          <unittitle>Exemple 2</unittitle>
          <unitdate>2016-2022</unitdate>
          <dao xlink:href="http://www.logilab.org/EXAMPLE/2"/>
        </did>
      </c>
    </dsc>
  </archdesc>
</ead>
"""


class TestArchdescLevelAttribAdjuster(ActionTestCase):
    action_class = ArchdescLevelAttribAdjuster

    def test_no_level_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].attrib.pop("level")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(out_root[1].get("level"), "fonds")
        self.assertEqual(out_root[1].get("otherlevel"), None)

    def test_correct_level_attribute(self):
        inp_root = etree.fromstring(DATA)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(out_root[1].get("level"), "fonds")
        self.assertEqual(out_root[1].get("otherlevel"), None)

    def test_incorrect_level_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].set("level", "collection")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(out_root[1].get("level"), "fonds")
        self.assertEqual(out_root[1].get("otherlevel"), "collection")

    def test_incorrect_level_attribute_with_otherlevel(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].set("level", "collection")
        inp_root[1].set("otherlevel", "TEST01")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(out_root[1].get("level"), "fonds")
        self.assertEqual(out_root[1].get("otherlevel"), "TEST01")


class TestDscTypeAttribAdjuster(ActionTestCase):
    action_class = DscTypeAttribAdjuster

    def test_no_type_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1][1].attrib.pop("type")
        out_root = self.run_action(inp_root)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "dsc")
        self.assertEqual(out_root[1][1].get("type"), None)

    def test_correct_type_attribute(self):
        inp_root = etree.fromstring(DATA)
        out_root = self.run_action(inp_root)
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "dsc")
        self.assertEqual(out_root[1][1].get("type"), "othertype")

    def test_incorrect_type_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1][1].set("type", "incorrect")
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1].tag, "dsc")
        self.assertEqual(out_root[1][1].get("type"), "othertype")


class TestEmphRenderAttribAdjuster(ActionTestCase):
    action_class = EmphRenderAttribAdjuster

    def test_no_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(etree.fromstring("<emph>TEST</emph>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 ")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail or "", "")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), None)

    def test_bold_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(etree.fromstring('<emph render="bold">TEST</emph>'))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 ")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail or "", "")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), "bold")

    def test_italic_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(
            etree.fromstring('<emph render="italic">TEST</emph>')
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 ")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail or "", "")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), "italic")

    def test_other_bold_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(
            etree.fromstring('<emph render="light-bold">TEST</emph>')
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 ")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail or "", "")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), "bold")

    def test_other_italic_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(
            etree.fromstring('<emph render="reversed-italic">TEST</emph>')
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 ")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail or "", "")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), "italic")

    def test_doublequote_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(
            etree.fromstring('<emph render="doublequote">TEST</emph>')
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 « ")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail, " »")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), None)

    def test_singleequote_render_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0][1][0][0].text += " "
        inp_root[0][1][0][0].append(
            etree.fromstring('<emph render="singlequote">TEST</emph>')
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][1][0][0].tag, "titleproper")
        self.assertEqual(out_root[0][1][0][0].text, "Example 1 \u2018")
        self.assertEqual(out_root[0][1][0][0][0].tag, "emph")
        self.assertEqual(out_root[0][1][0][0][0].text, "TEST")
        self.assertEqual(out_root[0][1][0][0][0].tail, "\u2019")
        self.assertEqual(out_root[0][1][0][0][0].get("render"), None)


class TestLanguageLangcodeAttribAdjuster(ActionTestCase):
    action_class = LanguageLangcodeAttribAdjuster

    def test_correct_langcode_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0].append(
            etree.fromstring(
                '<profiledesc><langusage><language langcode="fra"/></langusage></profiledesc>'
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0][0].tag, "language")
        self.assertEqual(out_root[0][2][0][0].get("langcode"), "fra")

    def test_upcase_correct_langcode_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0].append(
            etree.fromstring(
                '<profiledesc><langusage><language langcode="SPA"/></langusage></profiledesc>'
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0][0].tag, "language")
        self.assertEqual(out_root[0][2][0][0].get("langcode"), "spa")

    def test_incorrect_langcode_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0].append(
            etree.fromstring(
                '<profiledesc><langusage><language langcode="zrg"/></langusage></profiledesc>'
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0][0].tag, "language")
        self.assertEqual(out_root[0][2][0][0].get("langcode"), None)


class TestLanguageScriptcodeAttribAdjuster(ActionTestCase):
    action_class = LanguageScriptcodeAttribAdjuster

    def test_correct_scriptcode_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0].append(
            etree.fromstring(
                '<profiledesc><langusage><language scriptcode="Grek"/></langusage></profiledesc>'
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0][0].tag, "language")
        self.assertEqual(out_root[0][2][0][0].get("scriptcode"), "Grek")

    def test_upcase_correct_scriptcode_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0].append(
            etree.fromstring(
                '<profiledesc><langusage><language scriptcode="tAmL"/></langusage></profiledesc>'
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0][0].tag, "language")
        self.assertEqual(out_root[0][2][0][0].get("scriptcode"), "Taml")

    def test_incorrect_scriptcode_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[0].append(
            etree.fromstring(
                '<profiledesc><langusage><language scriptcode="eurp"/></langusage></profiledesc>'
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[0][2][0][0].tag, "language")
        self.assertEqual(out_root[0][2][0][0].get("scriptcode"), None)


class TestListAttribsAdjuster(ActionTestCase):
    action_class = ListAttribsAdjuster

    def test_no_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].insert(
            1,
            etree.fromstring("<acqinfo><list><item>TEST</item></list></acqinfo>"),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "list")
        self.assertEqual(out_root[1][1][0].get("numeration"), None)
        self.assertEqual(out_root[1][1][0].get("type"), None)

    def test_correct_numeration_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].insert(
            1,
            etree.fromstring(
                '<acqinfo><list numeration="arabic"><item>TEST</item></list></acqinfo>'
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "list")
        self.assertEqual(out_root[1][1][0].get("numeration"), "arabic")
        self.assertEqual(out_root[1][1][0].get("type"), None)

    def test_incorrect_numeration_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].insert(
            1,
            etree.fromstring(
                '<acqinfo><list numeration="upperroman"><item>TEST</item></list></acqinfo>'
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "list")
        self.assertEqual(out_root[1][1][0].get("numeration"), None)
        self.assertEqual(out_root[1][1][0].get("type"), None)

    def test_correct_type_attribute(self):
        for val in ("ordered", "marked"):
            with self.subTest(value=val):
                inp_root = etree.fromstring(DATA)
                inp_root[1].insert(
                    1,
                    etree.fromstring(
                        f'<acqinfo><list type="{val}"><item>TEST</item></list></acqinfo>'
                    ),
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "list")
                self.assertEqual(out_root[1][1][0].get("numeration"), None)
                self.assertEqual(out_root[1][1][0].get("type"), val)

    def test_incorrect_type_attribute(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].insert(
            1,
            etree.fromstring(
                '<acqinfo><list type="simple"><item>TEST</item></list></acqinfo>'
            ),
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "list")
        self.assertEqual(out_root[1][1][0].get("numeration"), None)
        self.assertEqual(out_root[1][1][0].get("type"), None)


if __name__ == "__main__":
    unittest.main()
