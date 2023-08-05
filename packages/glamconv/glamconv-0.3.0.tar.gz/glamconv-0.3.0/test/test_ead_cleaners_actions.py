# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from test import ActionTestCase
from glamconv.ead.cleaners import (
    AttributesEraser,
    DescgrpRemover,
    ElementsEraser,
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
      <unitid>UID1</unitid>
      <unittitle>Exemple 1</unittitle>
      <unitdate>2016-2022</unitdate>
      <dao xlink:href="http://www.logilab.org/EXAMPLE/1"/>
    </did>
"""


class TestAttributesEraser(ActionTestCase):
    action_class = AttributesEraser

    def test_paragraph_children_erasing(self):
        names = {
            "abbr": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("expan",),
            ),
            "bibref": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "entityref",
                    "id",
                    "linktype",
                ),
                (
                    "actuate",
                    "arcrole",
                    "href",
                    "role",
                    "show",
                    "title",
                    "xpointer",
                ),
            ),
            "corpname": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "normal",
                    "role",
                    "rules",
                    "source",
                ),
                ("authfilenumber",),
            ),
            "emph": (
                (
                    "altrender",
                    "id",
                ),
                ("render",),
            ),
            "expan": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("abbr",),
            ),
            "extref": (
                (
                    "altrender",
                    "audience",
                    "entityref",
                    "id",
                    "linktype",
                ),
                (
                    "actuate",
                    "arcrole",
                    "href",
                    "role",
                    "show",
                    "title",
                    "xpointer",
                ),
            ),
            "famname": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "normal",
                    "role",
                    "rules",
                    "source",
                ),
                ("authfilenumber",),
            ),
            "function": (
                (
                    "altrender",
                    "audience",
                    "authfilenumber",
                    "encodinganalog",
                    "id",
                    "normal",
                    "rules",
                    "source",
                ),
                tuple(),
            ),
            "genreform": (
                (
                    "altrender",
                    "audience",
                    "authfilenumber",
                    "encodinganalog",
                    "id",
                    "normal",
                    "rules",
                    "source",
                    "type",
                ),
                tuple(),
            ),
            "geogname": (
                (
                    "altrender",
                    "audience",
                    "authfilenumber",
                    "encodinganalog",
                    "id",
                    "normal",
                    "role",
                    "rules",
                    "source",
                ),
                tuple(),
            ),
            "name": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "normal",
                    "role",
                    "rules",
                    "source",
                ),
                ("authfilenumber",),
            ),
            "note": (
                (
                    "actuate",
                    "altrender",
                    "audience",
                    "id",
                    "show",
                ),
                (
                    "encodinganalog",
                    "label",
                    "type",
                ),
            ),
            "occupation": (
                (
                    "altrender",
                    "audience",
                    "authfilenumber",
                    "encodinganalog",
                    "id",
                    "normal",
                    "rules",
                    "source",
                ),
                tuple(),
            ),
            "origination": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                (
                    "encodinganalog",
                    "label",
                ),
            ),
            "persname": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "normal",
                    "role",
                    "rules",
                    "source",
                ),
                ("authfilenumber",),
            ),
            "ref": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "linktype",
                ),
                (
                    "actuate",
                    "arcrole",
                    "href",
                    "role",
                    "show",
                    "target",
                    "title",
                    "xpointer",
                ),
            ),
            "subject": (
                (
                    "altrender",
                    "audience",
                    "authfilenumber",
                    "encodinganalog",
                    "id",
                    "normal",
                    "rules",
                    "source",
                ),
                tuple(),
            ),
            "title": (
                (
                    "actuate",
                    "altrender",
                    "arcrole",
                    "audience",
                    "authfilenumber",
                    "encodinganalog",
                    "entityref",
                    "href",
                    "id",
                    "linktype",
                    "normal",
                    "render",
                    "role",
                    "rules",
                    "show",
                    "source",
                    "title",
                    "type",
                    "xpointer",
                ),
                tuple(),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[1].append(
                        etree.fromstring(
                            f"<accruals><p><{eltname}>X</{eltname}></p></accruals>"
                        )
                    )
                    inp_root[1][1][0][0].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0][0].tag, eltname)
                    self.assertEqual(
                        out_root[1][1][0][0].get(name),
                        None if name in attnames else "TEST",
                    )

    def test_paragraph_empty_children_erasing(self):
        names = {
            "extptr": (
                (
                    "altrender",
                    "audience",
                    "entityref",
                    "id",
                    "linktype",
                ),
                (
                    "actuate",
                    "arcrole",
                    "href",
                    "role",
                    "show",
                    "title",
                    "xpointer",
                ),
            ),
            "ptr": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "linktype",
                ),
                (
                    "actuate",
                    "arcrole",
                    "href",
                    "role",
                    "show",
                    "target",
                    "title",
                    "xpointer",
                ),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[1].append(
                        etree.fromstring(f"<accruals><p><{eltname}/></p></accruals>")
                    )
                    inp_root[1][1][0][0].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1][0][0].tag, eltname)
                    self.assertEqual(
                        out_root[1][1][0][0].get(name),
                        None if name in attnames else "TEST",
                    )

    def test_abstract_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
            "langcode",
        )
        kept_attnames = (
            "encodinganalog",
            "label",
            "type",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0].append(etree.fromstring("<abstract>X</abstract>"))
                inp_root[1][0][-1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][-1].tag, "abstract")
                self.assertEqual(
                    out_root[1][0][-1].get(name), None if name in attnames else "TEST"
                )

    def test_archdesc_children_erasing(self):
        names = {
            "accessrestrict": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "accruals": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "acqinfo": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "altformavail": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "appraisal": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "arrangement": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "bibliography": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "bioghist": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "container": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "label",
                ),
                (
                    "parent",
                    "type",
                ),
            ),
            "controlaccess": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                ),
                tuple(),
            ),
            "custodhist": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "fileplan": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                ),
                tuple(),
            ),
            "odd": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "originalsloc": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "otherfindaid": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "physdesc": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "label",
                    "rules",
                    "source",
                ),
                ("encodinganalog",),
            ),
            "phystech": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "prefercite": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "processinfo": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "relatedmaterial": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "scopecontent": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("encodinganalog",),
            ),
            "separatedmaterial": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "type",
                ),
                ("encodinganalog",),
            ),
            "userrestrict": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                (
                    "encodinganalog",
                    "type",
                ),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[1].append(
                        etree.fromstring(f"<{eltname}><p>X</p></{eltname}>")
                    )
                    inp_root[1][1].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][1].tag, eltname)
                    self.assertEqual(
                        out_root[1][1].get(name), None if name in attnames else "TEST"
                    )

    def test_address_addressline_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        "<accruals><p>"
                        + "<address><addressline>X</addressline></address>"
                        + "</p></accruals>"
                    )
                )
                inp_root[1][1][0][0].set(name, "TEST")
                inp_root[1][1][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "address")
                self.assertEqual(out_root[1][1][0][0].get(name), None)
                self.assertEqual(out_root[1][1][0][0][0].tag, "addressline")
                self.assertEqual(out_root[1][1][0][0][0].get(name), None)

    def test_archdesc_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        kept_attnames = (
            "encodinganalog",
            "level",
            "otherlevel",
            "relatedencoding",
            "type",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1].tag, "archdesc")
                self.assertEqual(
                    out_root[1].get(name), None if name in attnames else "TEST"
                )

    def test_titlestmt_children_erasing(self):
        names = {
            "author": (
                (
                    "altrender",
                    "audience",
                    "id",
                ),
                ("expan",),
            ),
            "sponsor": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                ),
                tuple(),
            ),
            "subtitle": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                ),
                tuple(),
            ),
            "titleproper": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "render",
                ),
                (
                    "encodinganalog",
                    "type",
                ),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[0][1][0].append(
                        etree.fromstring(f"<{eltname}>X</{eltname}>")
                    )
                    inp_root[0][1][0][1].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[0][1][0][1].tag, eltname)
                    self.assertEqual(
                        out_root[0][1][0][1].get(name),
                        None if name in attnames else "TEST",
                    )

    def test_blockquote_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        "<accruals><p><blockquote><p>X</p></blockquote></p></accruals>"
                    )
                )
                inp_root[1][1][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "blockquote")
                self.assertEqual(out_root[1][1][0][0].get(name), None)

    def test_c_erasing(self):
        attnames = (
            "altrender",
            "tpattern",
        )
        kept_attnames = (
            "audience",
            "encodinganalog",
            "id",
            "level",
            "otherlevel",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(f"<dsc><c>{DATA2}<c>{DATA2}</c></c></dsc>")
                )
                inp_root[1][1][0].set(name, "TEST")
                inp_root[1][1][0][1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "c")
                self.assertEqual(
                    out_root[1][1][0].get(name), None if name in attnames else "TEST"
                )
                self.assertEqual(out_root[1][1][0][1].tag, "c")
                self.assertEqual(
                    out_root[1][1][0][1].get(name), None if name in attnames else "TEST"
                )

    def test_c01_erasing(self):
        attnames = (
            "altrender",
            "tpattern",
        )
        kept_attnames = (
            "audience",
            "encodinganalog",
            "id",
            "level",
            "otherlevel",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        f"<dsc><c01>{DATA2}<c02>{DATA2}<c03>{DATA2}</c03></c02></c01></dsc>"
                    )
                )
                inp_root[1][1][0].set(name, "TEST")
                inp_root[1][1][0][1].set(name, "TEST")
                inp_root[1][1][0][1][1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "c01")
                self.assertEqual(
                    out_root[1][1][0].get(name), None if name in attnames else "TEST"
                )
                self.assertEqual(out_root[1][1][0][1].tag, "c02")
                self.assertEqual(
                    out_root[1][1][0][1].get(name), None if name in attnames else "TEST"
                )
                self.assertEqual(out_root[1][1][0][1][1].tag, "c03")
                self.assertEqual(
                    out_root[1][1][0][1][1].get(name),
                    None if name in attnames else "TEST",
                )

    def test_change_erasing(self):
        attnames = ("altrender",)
        kept_attnames = (
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0].append(
                    etree.fromstring(
                        "<revisiondesc><change><date>2022-07-31</date></change></revisiondesc>"
                    )
                )
                inp_root[0][2][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][2][0].tag, "change")
                self.assertEqual(
                    out_root[0][2][0].get(name), None if name in attnames else "TEST"
                )

    def test_colspec_erasing(self):
        attnames = (
            "align",
            "char",
            "charoff",
            "colsep",
            "colwidth",
            "rowsep",
        )
        kept_attnames = (
            "colname",
            "colnum",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1">'
                        + "<colspec/><tbody><row><entry>X</entry></row></tbody>"
                        + "</tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "colspec")
                self.assertEqual(
                    out_root[1][1][0][0][0].get(name),
                    None if name in attnames else "TEST",
                )

    def test_profiledesc_children_erasing(self):
        names = {
            "creation": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                ),
                tuple(),
            ),
            "descrules": (
                ("altrender",),
                (
                    "audience",
                    "encodinganalog",
                    "id",
                ),
            ),
            "langusage": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                ),
                tuple(),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[0].append(
                        etree.fromstring(
                            f"<profiledesc><{eltname}>X</{eltname}></profiledesc>"
                        )
                    )
                    inp_root[0][2][0].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[0][2][0].tag, eltname)
                    self.assertEqual(
                        out_root[0][2][0].get(name),
                        None if name in attnames else "TEST",
                    )

    def test_dao_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "entityref",
            "id",
            "linktype",
        )
        kept_attnames = (
            "actuate",
            "arcrole",
            "href",
            "role",
            "show",
            "title",
            "xpointer",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][3].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][3].tag, "dao")
                self.assertEqual(
                    out_root[1][0][3].get(name), None if name in attnames else "TEST"
                )

    def test_daoloc_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "entityref",
            "id",
            "linktype",
        )
        kept_attnames = (
            "href",
            "label",
            "role",
            "title",
            "xpointer",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0].append(etree.fromstring("<daogrp><daoloc/></daogrp>"))
                inp_root[1][0][4][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][4][0].tag, "daoloc")
                self.assertEqual(
                    out_root[1][0][4][0].get(name), None if name in attnames else "TEST"
                )

    def test_date_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "certainty",
            "id",
            "type",
        )
        kept_attnames = (
            "calendar",
            "encodinganalog",
            "era",
            "normal",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0].append(
                    etree.fromstring(
                        "<revisiondesc><change><date>2022-07-31</date></change></revisiondesc>"
                    )
                )
                inp_root[0][2][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][2][0][0].tag, "date")
                self.assertEqual(
                    out_root[0][2][0][0].get(name), None if name in attnames else "TEST"
                )

    def test_did_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0].tag, "did")
                self.assertEqual(out_root[1][0].get(name), None)

    def test_physdesc_children_erasing(self):
        names = {
            "dimensions": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "label",
                ),
                (
                    "type",
                    "unit",
                ),
            ),
            "extent": (
                ("altrender", "audience", "encodinganalog", "id", "label", "type"),
                ("unit",),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[1][0].append(
                        etree.fromstring(
                            f"<physdesc><{eltname}>X</{eltname}></physdesc>"
                        )
                    )
                    inp_root[1][0][-1][0].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][0][-1][0].tag, eltname)
                    self.assertEqual(
                        out_root[1][0][-1][0].get(name),
                        None if name in attnames else "TEST",
                    )

    def test_dsc_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
            "othertype",
            "label",
            "tpattern",
        )
        kept_attnames = ("type",)
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(etree.fromstring(f"<dsc><c>{DATA2}</c></dsc>"))
                inp_root[1][1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1].tag, "dsc")
                self.assertEqual(
                    out_root[1][1].get(name), None if name in attnames else "TEST"
                )

    def test_ead_erasing(self):
        attnames = (
            "altrender",
            "relatedencoding",
        )
        kept_attnames = (
            "audience",
            "id",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root.set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root.tag, "ead")
                self.assertEqual(
                    out_root.get(name), None if name in attnames else "TEST"
                )

    def test_eadheader_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "findaidstatus",
            "id",
        )
        kept_attnames = (
            "countryencoding",
            "dateencoding",
            "langencoding",
            "relatedencoding",
            "repositoryencoding",
            "scriptencoding",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0].tag, "eadheader")
                self.assertEqual(
                    out_root[0].get(name), None if name in attnames else "TEST"
                )

    def test_eadid_erasing(self):
        attnames = (
            "encodinganalog",
            "publicid",
            "urn",
        )
        kept_attnames = (
            "countrycode",
            "identifier",
            "mainagencycode",
            "url",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][0].tag, "eadid")
                self.assertEqual(
                    out_root[0][0].get(name), None if name in attnames else "TEST"
                )

    def test_entry_erasing(self):
        attnames = (
            "align",
            "altrender",
            "audience",
            "char",
            "charoff",
            "colname",
            "colsep",
            "id",
            "morerows",
            "nameend",
            "namest",
            "rowsep",
            "valign",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1">'
                        + "<tbody><row><entry>X</entry></row></tbody>"
                        + "</tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0][0][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0][0][0].tag, "entry")
                self.assertEqual(out_root[1][1][0][0][0][0][0].get(name), None)

    def test_filedesc_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0][1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][1].tag, "filedesc")
                self.assertEqual(out_root[0][0].get(name), None)

    def test_head_erasing(self):
        attnames = (
            "althead",
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(f"<dsc><c><head>X</head>{DATA2}</c></dsc>")
                )
                inp_root[1][1][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "head")
                self.assertEqual(out_root[1][1][0][0].get(name), None)

    def test_imprint_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        "<accruals><p><bibref><imprint>X</imprint></bibref></p></accruals>"
                    )
                )
                inp_root[1][-1][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][-1][0][0][0].tag, "imprint")
                self.assertEqual(out_root[1][-1][0][0][0].get(name), None)

    def test_item_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring("<accruals><list><item>X</item></list></accruals>")
                )
                inp_root[1][-1][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][-1][0][0].tag, "item")
                self.assertEqual(out_root[1][-1][0][0].get(name), None)

    def test_label_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        "<accruals><list><defitem>"
                        + "<label>X</label><item>X</item>"
                        + "</defitem></list></accruals>"
                    )
                )
                inp_root[1][-1][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][-1][0][0][0].tag, "label")
                self.assertEqual(out_root[1][-1][0][0][0].get(name), None)

    def test_did_children_erasing(self):
        names = {
            "langmaterial": (
                (
                    "altrender",
                    "audience",
                    "id",
                    "label",
                ),
                tuple(),
            ),
            "materialspec": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "label",
                    "type",
                ),
                tuple(),
            ),
            "physloc": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "parent",
                    "type",
                ),
                ("label",),
            ),
            "repository": (
                (
                    "altrender",
                    "audience",
                    "encodinganalog",
                    "id",
                    "label",
                ),
                tuple(),
            ),
        }
        for eltname, (attnames, kept_attnames) in names.items():
            for name in attnames + kept_attnames:
                with self.subTest(elt_name=eltname, attribute_name=name):
                    inp_root = etree.fromstring(DATA)
                    inp_root[1][0].append(etree.fromstring(f"<{eltname}>X</{eltname}>"))
                    inp_root[1][0][-1].set(name, "TEST")
                    out_root = self.run_action(inp_root)
                    self.assertEqual(out_root[1][0][-1].tag, eltname)
                    self.assertEqual(
                        out_root[1][0][-1].get(name),
                        None if name in attnames else "TEST",
                    )

    def test_language_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0].append(
                    etree.fromstring(
                        "<langmaterial><language>X</language></langmaterial>"
                    )
                )
                inp_root[1][0][-1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][-1][0].tag, "language")
                self.assertEqual(out_root[1][0][-1][0].get(name), None)

    def test_legalstatus_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
            "type",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        "<accessrestrict><legalstatus>X</legalstatus></accessrestrict>"
                    )
                )
                inp_root[1][1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "legalstatus")
                self.assertEqual(out_root[1][1][0].get(name), None)

    def test_list_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "continuation",
            "id",
            "mark",
        )
        kept_attnames = (
            "numeration",
            "type",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring("<accruals><list><item>X</item></list></accruals>")
                )
                inp_root[1][-1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][-1][0].tag, "list")
                self.assertEqual(
                    out_root[1][-1][0].get(name), None if name in attnames else "TEST"
                )

    def test_p_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(etree.fromstring("<accruals><p>X</p></accruals>"))
                inp_root[1][-1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][-1][0].tag, "p")
                self.assertEqual(out_root[1][-1][0].get(name), None)

    def test_physfacet_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
            "label",
            "rules",
            "source",
            "unit",
        )
        kept_attnames = ("type",)
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring("<physdesc><physfacet>X</physfacet></physdesc>")
                )
                inp_root[1][1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "physfacet")
                self.assertEqual(
                    out_root[1][1][0].get(name), None if name in attnames else "TEST"
                )

    def test_profiledesc_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0].append(
                    etree.fromstring(
                        "<profiledesc><creation>X</creation></profiledesc>"
                    )
                )
                inp_root[0][2].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][2].tag, "profiledesc")
                self.assertEqual(out_root[0][2].get(name), None)

    def test_publicationstmt_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0][1].append(
                    etree.fromstring(
                        "<publicationstmt><date>2022-07-31</date></publicationstmt>"
                    )
                )
                inp_root[0][1][-1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][1][-1].tag, "publicationstmt")
                self.assertEqual(out_root[0][1][-1].get(name), None)

    def test_publisher_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
        )
        kept_attnames = ("encodinganalog",)
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0][1].append(
                    etree.fromstring(
                        "<publicationstmt><publisher>X</publisher></publicationstmt>"
                    )
                )
                inp_root[0][1][-1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][1][-1][0].tag, "publisher")
                self.assertEqual(
                    out_root[0][1][-1][0].get(name),
                    None if name in attnames else "TEST",
                )

    def test_revisiondesc_erasing(self):
        attnames = ("altrender",)
        kept_attnames = (
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0].append(
                    etree.fromstring(
                        "<revisiondesc><change><date>2022-07-31</date></change></revisiondesc>"
                    )
                )
                inp_root[0][2].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][2].tag, "revisiondesc")
                self.assertEqual(
                    out_root[0][2].get(name), None if name in attnames else "TEST"
                )

    def test_row_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
            "rowsep",
            "valign",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1"><tbody>'
                        + "<row><entry>X</entry></row>"
                        + "</tbody></tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0][0].tag, "row")
                self.assertEqual(out_root[1][1][0][0][0][0].get(name), None)

    def test_seriesstmt_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0][1].append(
                    etree.fromstring(
                        "<seriesstmt><titleproper>X</titleproper></seriesstmt>"
                    )
                )
                inp_root[0][1][-1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][1][-1].tag, "seriesstmt")
                self.assertEqual(out_root[0][1][-1].get(name), None)

    def test_table_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "colsep",
            "frame",
            "id",
            "pgwide",
            "rowsep",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1"><tbody>'
                        + "<row><entry>X</entry></row>"
                        + "</tbody></tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "table")
                self.assertEqual(out_root[1][1][0].get(name), None)

    def test_tbody_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
            "valign",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1"><tbody>'
                        + "<row><entry>X</entry></row>"
                        + "</tbody></tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "tbody")
                self.assertEqual(out_root[1][1][0][0][0].get(name), None)

    def test_tgroup_erasing(self):
        attnames = (
            "align",
            "altrender",
            "audience",
            "colsep",
            "id",
            "rowsep",
        )
        kept_attnames = ("cols",)
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1"><tbody>'
                        + "<row><entry>X</entry></row>"
                        + "</tbody></tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0].tag, "tgroup")
                self.assertEqual(
                    out_root[1][1][0][0].get(name), None if name in attnames else "TEST"
                )

    def test_thead_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
            "valign",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        '<accruals><table><tgroup cols="1">'
                        + "<thead><row><entry>X</entry></row></thead>"
                        + "<tbody><row><entry>X</entry></row></tbody>"
                        + "</tgroup></table></accruals>"
                    )
                )
                inp_root[1][1][0][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0][0][0].tag, "thead")
                self.assertEqual(out_root[1][1][0][0][0].get(name), None)

    def test_titlestmt_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "encodinganalog",
            "id",
        )
        for name in attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[0][1][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[0][1][0].tag, "titlestmt")
                self.assertEqual(out_root[0][1][0].get(name), None)

    def test_unitdate_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "certainty",
            "datechar",
            "id",
            "label",
            "type",
        )
        kept_attnames = (
            "calendar",
            "encodinganalog",
            "era",
            "normal",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][2].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][2].tag, "unitdate")
                self.assertEqual(
                    out_root[1][0][2].get(name), None if name in attnames else "TEST"
                )

    def test_unitid_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "countrycode",
            "id",
            "identifier",
            "label",
            "repositorycode",
        )
        kept_attnames = (
            "encodinganalog",
            "type",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][0].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][0].tag, "unitid")
                self.assertEqual(
                    out_root[1][0][0].get(name), None if name in attnames else "TEST"
                )

    def test_unittitle_erasing(self):
        attnames = (
            "altrender",
            "audience",
            "id",
            "label",
        )
        kept_attnames = (
            "encodinganalog",
            "type",
        )
        for name in attnames + kept_attnames:
            with self.subTest(attribute_name=name):
                inp_root = etree.fromstring(DATA)
                inp_root[1][0][1].set(name, "TEST")
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][0][1].tag, "unittitle")
                self.assertEqual(
                    out_root[1][0][1].get(name), None if name in attnames else "TEST"
                )


class TestDescgrpRemover(ActionTestCase):
    action_class = DescgrpRemover

    def test_subelements_and_descgrp_in_archdesc(self):
        names = (
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
            "index",
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
        for eltname in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        f"<descgrp><{eltname}><p>TEST01</p></{eltname}>"
                        + f"<descgrp><{eltname}><p>TEST02</p></{eltname}>"
                        + f"<{eltname}><p>TEST03</p></{eltname}></descgrp>"
                        + f"<{eltname}><p>TEST04</p></{eltname}></descgrp>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1].tag, "archdesc")
                self.assertEqual(len(out_root[1]), 5)
                self.assertEqual(out_root[1][0].tag, "did")
                self.assertEqual(len(out_root[1][0]), 4)
                for idx in range(4):
                    self.assertEqual(out_root[1][idx + 1].tag, eltname)
                    self.assertEqual(out_root[1][idx + 1][0].tag, "p")
                    self.assertEqual(out_root[1][idx + 1][0].text, f"TEST0{idx + 1}")

    def test_subelements_and_descgrp_in_c(self):
        names = (
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
            "index",
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
        for eltname in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(etree.fromstring(f"<dsc><c>{DATA2}</c></dsc>"))
                inp_root[1][1][0].append(
                    etree.fromstring(
                        f"<descgrp><{eltname}><p>TEST01</p></{eltname}>"
                        + f"<descgrp><{eltname}><p>TEST02</p></{eltname}>"
                        + f"<{eltname}><p>TEST03</p></{eltname}></descgrp>"
                        + f"<{eltname}><p>TEST04</p></{eltname}></descgrp>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "c")
                self.assertEqual(len(out_root[1][1][0]), 5)
                self.assertEqual(out_root[1][1][0][0].tag, "did")
                self.assertEqual(len(out_root[1][1][0][0]), 4)
                for idx in range(4):
                    self.assertEqual(out_root[1][1][0][idx + 1].tag, eltname)
                    self.assertEqual(out_root[1][1][0][idx + 1][0].tag, "p")
                    self.assertEqual(
                        out_root[1][1][0][idx + 1][0].text, f"TEST0{idx + 1}"
                    )

    def test_head_and_descgrp_in_archdesc(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].append(
            etree.fromstring(
                "<descgrp><head>TEST01</head><accruals><p>TEST02</p></accruals></descgrp>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(len(out_root[1]), 2)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(len(out_root[1][0]), 4)
        self.assertEqual(out_root[1][1].tag, "accruals")
        self.assertEqual(out_root[1][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0].text, "TEST02")

    def test_head_and_descgrp_in_c(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].append(etree.fromstring(f"<dsc><c>{DATA2}</c></dsc>"))
        inp_root[1][1][0].append(
            etree.fromstring(
                "<descgrp><head>TEST01</head><accruals><p>TEST02</p></accruals></descgrp>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c")
        self.assertEqual(len(out_root[1][1][0]), 2)
        self.assertEqual(out_root[1][1][0][0].tag, "did")
        self.assertEqual(len(out_root[1][1][0][0]), 4)
        self.assertEqual(out_root[1][1][0][1].tag, "accruals")
        self.assertEqual(out_root[1][1][0][1][0].tag, "p")
        self.assertEqual(out_root[1][1][0][1][0].text, "TEST02")

    def test_notes_and_descgrp_in_archdesc(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].append(
            etree.fromstring(
                "<descgrp><note><p>TEST01</p></note>"
                + "<descgrp><note><p>TEST02</p></note>"
                + "<note><p>TEST03</p></note></descgrp>"
                + "<note><p>TEST04</p></note></descgrp>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(len(out_root[1]), 1)
        self.assertEqual(out_root[1][0].tag, "did")
        self.assertEqual(len(out_root[1][0]), 8)
        for idx in range(4):
            self.assertEqual(out_root[1][0][idx + 4].tag, "note")
            self.assertEqual(out_root[1][0][idx + 4][0].tag, "p")
            self.assertEqual(out_root[1][0][idx + 4][0].text, f"TEST0{idx + 1}")

    def test_notes_and_descgrp_in_c(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].append(etree.fromstring(f"<dsc><c>{DATA2}</c></dsc>"))
        inp_root[1][1][0].append(
            etree.fromstring(
                "<descgrp><note><p>TEST01</p></note>"
                + "<descgrp><note><p>TEST02</p></note>"
                + "<note><p>TEST03</p></note></descgrp>"
                + "<note><p>TEST04</p></note></descgrp>"
            )
        )
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1][1][0].tag, "c")
        self.assertEqual(len(out_root[1][1][0]), 1)
        self.assertEqual(out_root[1][1][0][0].tag, "did")
        self.assertEqual(len(out_root[1][1][0][0]), 8)
        for idx in range(4):
            self.assertEqual(out_root[1][1][0][0][idx + 4].tag, "note")
            self.assertEqual(out_root[1][1][0][0][idx + 4][0].tag, "p")
            self.assertEqual(out_root[1][1][0][0][idx + 4][0].text, f"TEST0{idx + 1}")

    def test_paragraph_level_elements_and_descgrp_in_archdesc(self):
        names = (
            ("address", "<address><addressline>{}</addressline></address>"),
            ("blockquote", "<blockquote><p>{}</p></blockquote>"),
            (
                "chronlist",
                "<chronlist><chronitem><date>2022-07-31</date>"
                + "<event>{}</event></chronitem></chronlist>",
            ),
            ("list", "<list><item>{}</item></list>"),
            ("p", "<p>{}</p>"),
            (
                "table",
                '<table><tgroup cols="1"><tbody><row><entry>{}</entry></row>'
                + "</tbody></tgroup></table>",
            ),
        )
        for eltname, eltdecl in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        f"<descgrp>{eltdecl.format('TEST01')}"
                        + f"<descgrp>{eltdecl.format('TEST02')}"
                        + f"{eltdecl.format('TEST03')}</descgrp>"
                        + f"{eltdecl.format('TEST04')}</descgrp>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1].tag, "archdesc")
                self.assertEqual(len(out_root[1]), 1)
                self.assertEqual(out_root[1][0].tag, "did")
                self.assertEqual(len(out_root[1][0]), 7)
                self.assertEqual(out_root[1][0][4].tag, "note")
                self.assertEqual(out_root[1][0][4][0].tag, eltname)
                self.assertEqual(out_root[1][0][5].tag, "note")
                self.assertEqual(out_root[1][0][5][0].tag, eltname)
                self.assertEqual(out_root[1][0][5][1].tag, eltname)
                self.assertEqual(out_root[1][0][6].tag, "note")
                self.assertEqual(out_root[1][0][6][0].tag, eltname)

    def test_paragraph_level_elements_and_descgrp_in_c(self):
        names = (
            ("address", "<address><addressline>{}</addressline></address>"),
            ("blockquote", "<blockquote><p>{}</p></blockquote>"),
            (
                "chronlist",
                "<chronlist><chronitem><date>2022-07-31</date>"
                + "<event>{}</event></chronitem></chronlist>",
            ),
            ("list", "<list><item>{}</item></list>"),
            ("p", "<p>{}</p>"),
            (
                "table",
                '<table><tgroup cols="1"><tbody><row><entry>{}</entry></row>'
                + "</tbody></tgroup></table>",
            ),
        )
        for eltname, eltdecl in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(etree.fromstring(f"<dsc><c>{DATA2}</c></dsc>"))
                inp_root[1][1][0].append(
                    etree.fromstring(
                        f"<descgrp>{eltdecl.format('TEST01')}"
                        + f"<descgrp>{eltdecl.format('TEST02')}"
                        + f"{eltdecl.format('TEST03')}</descgrp>"
                        + f"{eltdecl.format('TEST04')}</descgrp>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "c")
                self.assertEqual(len(out_root[1][1][0]), 1)
                self.assertEqual(out_root[1][1][0][0].tag, "did")
                self.assertEqual(len(out_root[1][1][0][0]), 7)
                self.assertEqual(out_root[1][1][0][0][4].tag, "note")
                self.assertEqual(out_root[1][1][0][0][4][0].tag, eltname)
                self.assertEqual(out_root[1][1][0][0][5].tag, "note")
                self.assertEqual(out_root[1][1][0][0][5][0].tag, eltname)
                self.assertEqual(out_root[1][1][0][0][5][1].tag, eltname)
                self.assertEqual(out_root[1][1][0][0][6].tag, "note")
                self.assertEqual(out_root[1][1][0][0][6][0].tag, eltname)

    def test_paragraph_level_elements_with_note_and_descgrp_in_archdesc(self):
        names = (
            ("address", "<address><addressline>{}</addressline></address>"),
            ("blockquote", "<blockquote><p>{}</p></blockquote>"),
            (
                "chronlist",
                "<chronlist><chronitem><date>2022-07-31</date>"
                + "<event>{}</event></chronitem></chronlist>",
            ),
            ("list", "<list><item>{}</item></list>"),
            ("p", "<p>{}</p>"),
            (
                "table",
                '<table><tgroup cols="1"><tbody><row><entry>{}</entry></row>'
                + "</tbody></tgroup></table>",
            ),
        )
        for eltname, eltdecl in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(
                    etree.fromstring(
                        f"<descgrp>{eltdecl.format('TEST01')}"
                        + "<note><p>TEST10</p></note>"
                        + f"{eltdecl.format('TEST04')}</descgrp>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1].tag, "archdesc")
                self.assertEqual(len(out_root[1]), 1)
                self.assertEqual(out_root[1][0].tag, "did")
                self.assertEqual(len(out_root[1][0]), 7)
                self.assertEqual(out_root[1][0][4].tag, "note")
                self.assertEqual(out_root[1][0][4][0].tag, eltname)
                self.assertEqual(out_root[1][0][5].tag, "note")
                self.assertEqual(out_root[1][0][5][0].tag, "p")
                self.assertEqual(out_root[1][0][5][0].text, "TEST10")
                self.assertEqual(out_root[1][0][6].tag, "note")
                self.assertEqual(out_root[1][0][6][0].tag, eltname)

    def test_paragraph_level_elements_with_note_and_descgrp_in_c(self):
        names = (
            ("address", "<address><addressline>{}</addressline></address>"),
            ("blockquote", "<blockquote><p>{}</p></blockquote>"),
            (
                "chronlist",
                "<chronlist><chronitem><date>2022-07-31</date>"
                + "<event>{}</event></chronitem></chronlist>",
            ),
            ("list", "<list><item>{}</item></list>"),
            ("p", "<p>{}</p>"),
            (
                "table",
                '<table><tgroup cols="1"><tbody><row><entry>{}</entry></row>'
                + "</tbody></tgroup></table>",
            ),
        )
        for eltname, eltdecl in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(etree.fromstring(f"<dsc><c>{DATA2}</c></dsc>"))
                inp_root[1][1][0].append(
                    etree.fromstring(
                        f"<descgrp>{eltdecl.format('TEST01')}"
                        + "<note><p>TEST10</p></note>"
                        + f"{eltdecl.format('TEST04')}</descgrp>"
                    )
                )
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1][1][0].tag, "c")
                self.assertEqual(len(out_root[1][1][0]), 1)
                self.assertEqual(out_root[1][1][0][0].tag, "did")
                self.assertEqual(len(out_root[1][1][0][0]), 7)
                self.assertEqual(out_root[1][1][0][0][4].tag, "note")
                self.assertEqual(out_root[1][1][0][0][4][0].tag, eltname)
                self.assertEqual(out_root[1][1][0][0][5].tag, "note")
                self.assertEqual(out_root[1][1][0][0][5][0].tag, "p")
                self.assertEqual(out_root[1][1][0][0][5][0].text, "TEST10")
                self.assertEqual(out_root[1][1][0][0][6].tag, "note")
                self.assertEqual(out_root[1][1][0][0][6][0].tag, eltname)


class TestElementsEraser(ActionTestCase):
    action_class = ElementsEraser

    def test_archdesc_subelements(self):
        names = ("heritedcontrolaccess", "index", "xmlvalue")
        for eltname in names:
            with self.subTest(element_name=eltname):
                inp_root = etree.fromstring(DATA)
                inp_root[1].append(etree.fromstring(f"<{eltname}><p>X</p></{eltname}>"))
                out_root = self.run_action(inp_root)
                self.assertEqual(out_root[1].tag, "archdesc")
                self.assertEqual(len(out_root[1]), 1)
                self.assertEqual(out_root[1][0].tag, "did")

    def test_runner_subelement(self):
        inp_root = etree.fromstring(DATA)
        inp_root[1].insert(0, etree.fromstring("<runner>X</runner>"))
        out_root = self.run_action(inp_root)
        self.assertEqual(out_root[1].tag, "archdesc")
        self.assertEqual(len(out_root[1]), 1)
        self.assertEqual(out_root[1][0].tag, "did")


if __name__ == "__main__":
    unittest.main()
