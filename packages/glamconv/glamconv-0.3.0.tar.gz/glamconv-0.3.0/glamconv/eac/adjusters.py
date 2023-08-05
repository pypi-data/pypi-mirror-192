# -*- coding: utf-8 -*-
"""
Module containing actions for changing the values of the vocabulary-controlled
attributes (in order to have a legit value) and for moving some elements
into their new legit parent.
"""

from lxml import etree
from glamconv.eac.utils import log_element
from glamconv.eac.formats import EAC_CPF
from glamconv.transformer.actions import TransformAction


LEGIT_LOCALTYPE_VALUES = {
    "address": (
        ("postal address", "other", "visitors address"),
        "other",
    ),
    "addressLine": (
        (
            "street",
            "other",
            "postalcode",
            "localentity",
            "firstdem",
            "secondem",
            "country",
        ),
        "other",
    ),
    "date": (
        ("unknown", "open", "unknownEnd", "unknownStart"),
        "unknown",
    ),
    "dateRange": (
        ("unknown", "open", "unknownEnd", "unknownStart"),
        "unknown",
    ),
    "nameEntry": (
        ("abbreviation", "other", "authorized", "alternative", "preferred"),
        "other",
    ),
    "nameEntryParallel": (
        ("abbreviation", "other", "authorized", "alternative", "preferred"),
        "other",
    ),
    "part": (
        (
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
        ),
        "title",
    ),
    "placeEntry": (
        (
            "death",
            "birth",
            "other",
            "foundation",
            "private-residence",
            "business-residence",
            "suppression",
        ),
        "other",
    ),
    "relationEntry": (
        ("agencyCode", "agencyName", "title", "id"),
        "title",
    ),
}


class LocalTypeAttributeAdjuster(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "localtype-adjuster"
    name = "Adjusting the values of localType attribute in some elements"
    category = "Cleansing"
    desc = (
        "In Ape-EAC, the values of the localType attribute must be picked in "
        "a vocabulary for the elements: <address>, <addressLine>, <date>, "
        "<dateRange>, <nameEntry>, <nameEntryParallel>, <part>, <placeEntry>, "
        "and <relationEntry>. If the value of localType is not in the legit "
        "vocabulary, this action changes it for a default value such as "
        '"other", "unknown" or "title".'
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        corrected_elts = []
        request = " | ".join(
            f".//{name}[@localType]"
            for name in (
                "address",
                "addressLine",
                "date",
                "dateRange",
                "nameEntry",
                "nameEntryParallel",
                "part",
                "placeEntry",
                "relationEntry",
            )
        )
        for elt in xml_root.xpath(request):
            legit_values, default_value = LEGIT_LOCALTYPE_VALUES[elt.tag]
            value = " ".join(elt.get("localType").lower().split())
            if value in ("unknownend", "unknownstart"):
                value = value[:7] + value[7].upper() + value[8:]
            if value in ("agencycode", "agencyname"):
                value = value[:6] + value[6].upper() + value[7:]
            if value not in legit_values:
                elt.set("localType", default_value)
                count += 1
                if log_details:
                    corrected_elts.append(log_element(elt))
            else:
                elt.set("localType", value)
        if count > 0:
            logger.warning(
                "The value of localType attribute has been changed in "
                f"{count:d} elements in order to have a value taken from the "
                "fixed vocabulary."
            )
            if log_details:
                logger.warning(
                    "The following elements have had their localType attribute "
                    "corrected:\n" + "\n".join(corrected_elts)
                )
        return xml_root


PARENT_ELT = {
    "function": "functions",
    "languageUsed": "languagesUsed",
    "legalStatus": "legalStatuses",
    "localDescription": "localDescriptions",
    "mandate": "mandates",
    "occupation": "occupations",
    "place": "places",
}


class DescriptionChildrenMover(TransformAction):
    applicable_for = (EAC_CPF,)
    uid = "description-children-mover"
    name = "Moving some <description> children into their thematic element"
    category = "Cleansing"
    desc = (
        "In Ape-EAC, the <description> element cannot directly contain "
        "<function>, <languageUsed>, <legalStatus>, <localDescription>, "
        "<mandate>, <occupation> or <place> elements. They must always be "
        "stored in <functions>, <languagesUsed>, <legalStatuses>, "
        "<localDescriptions>, <mandates>, <occupations> or <places> children "
        "of <description>. This action adds the correct regrouping element "
        "and moves such elements into it."
    )

    def _execute(self, xml_root, logger, log_details):
        count = 0
        moved_elts = []
        for elt_name in (
            "function",
            "languageUsed",
            "legalStatus",
            "localDescription",
            "mandate",
            "occupation",
            "place",
        ):
            to_move = []
            for xml_elt in xml_root.xpath(f".//description/{elt_name}"):
                count += 1
                if log_details:
                    moved_elts.append(log_element(xml_elt))
                to_move.append(xml_elt)
            if len(to_move) > 0:
                grp_elt = etree.Element(PARENT_ELT[elt_name])
                idx = to_move[0].getparent().index(to_move[0])
                to_move[0].getparent().insert(idx, grp_elt)
                for elt in to_move:
                    grp_elt.append(elt)
        if count > 0:
            logger.info(
                f"{count:d} children of <description> have been moved into "
                "their regrouping element."
            )
            if log_details:
                logger.info(
                    "The following elements have been moved:\n" + "\n".join(moved_elts)
                )
        return xml_root
