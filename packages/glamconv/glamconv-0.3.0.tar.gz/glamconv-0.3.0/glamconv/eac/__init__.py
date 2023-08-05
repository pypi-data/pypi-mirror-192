# -*- coding: utf-8 -*-
"""
Sub-package containing the formats and the actions related to EAC (Encoded
Archival Context).

EAC exists in two main formats : EAC-CPF and Ape-EAC. The various actions
defined here can be used to convert files in EAC-CPF into Ape-EAC that has
more constraints. Both formats rely on XML files.
"""

import os.path as osp
import json

from .registration import register  # noqa


def eac_cpf_to_ape_default_settings():
    """load default eac-cpf -> ape transformation settings"""
    settings_filepath = osp.join(
        osp.dirname(__file__), "default-eac-cpf-to-ape-settings.json"
    )
    with open(settings_filepath) as inputf:
        return json.load(inputf)
