# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

from lxml import etree

from test import ActionTestCase
from glamconv.utils import NS
from glamconv.transformer.rw_actions import XmlReader, XmlWriter


DATA_DIR = Path(__file__).parent / "data"


class TestXmlReader(ActionTestCase):
    action_class = XmlReader

    def test_file_reading(self):
        fname = str(DATA_DIR / "simple-ead.xml")
        out_root = self.run_action(fname)
        self.assertIsInstance(out_root, etree._Element)
        self.assertEqual(out_root.tag, f"{{{NS['ead']}}}ead")

    def test_flow_reading(self):
        with open(DATA_DIR / "simple-ead.xml", mode="rb") as flow:
            out_root = self.run_action(flow)
        self.assertIsInstance(out_root, etree._Element)
        self.assertEqual(out_root.tag, f"{{{NS['ead']}}}ead")

    def test_tree_reading(self):
        fname = str(DATA_DIR / "simple-ead.xml")
        tree = etree.parse(fname)
        out_root = self.run_action(tree)
        self.assertIsInstance(out_root, etree._Element)
        self.assertEqual(out_root.tag, f"{{{NS['ead']}}}ead")

    def test_root_elt_reading(self):
        fname = str(DATA_DIR / "simple-ead.xml")
        root = etree.parse(fname).getroot()
        out_root = self.run_action(root)
        self.assertIsInstance(out_root, etree._Element)
        self.assertEqual(out_root.tag, f"{{{NS['ead']}}}ead")


class TestXmlWriter(ActionTestCase):
    action_class = XmlWriter

    def test_ead_writing(self):
        fname = str(DATA_DIR / "simple-ead.xml")
        root = etree.parse(fname).getroot()
        out = self.run_action(root)
        self.assertIsInstance(out, bytes)
        out_root = etree.fromstring(out)
        exp_elts = ("ead", "eadheader", "eadid", "archdesc", "did", "unitid")
        for (_, elt), exp in zip(etree.iterwalk(out_root, events=("start",)), exp_elts):
            self.assertEqual(elt.tag, f"{{{NS['ead']}}}{exp}")

    def test_eac_writing(self):
        fname = str(DATA_DIR / "simple-eac.xml")
        root = etree.parse(fname).getroot()
        out = self.run_action(root)
        self.assertIsInstance(out, bytes)
        out_root = etree.fromstring(out)
        exp_elts = (
            "eac-cpf",
            "control",
            "recordId",
            "maintenanceStatus",
            "maintenanceAgency",
            "agencyCode",
            "agencyName",
            "maintenanceHistory",
            "maintenanceEvent",
            "eventType",
            "eventDateTime",
            "agentType",
            "agent",
            "cpfDescription",
            "identity",
            "entityType",
            "nameEntry",
            "part",
            "description",
            "existDates",
            "date",
        )
        for (_, elt), exp in zip(etree.iterwalk(out_root, events=("start",)), exp_elts):
            self.assertEqual(elt.tag, f"{{{NS['cpf']}}}{exp}")


if __name__ == "__main__":
    unittest.main()
