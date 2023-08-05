# -*- coding: utf-8 -*-

import inspect
from glamconv.transformer.libraries import register_format, register_action
from glamconv.transformer.actions import TransformAction
from glamconv.eac.formats import EAC_CPF, EAC_APE
from glamconv.eac import (
    validators,
    adjusters,
    cleaners,
    namespacers,
    required_elts_adders,
    text_data,
    supplementers,
)


def register():
    # Formats
    register_format(EAC_CPF)
    register_format(EAC_APE)
    # Actions
    for module in (
        validators,
        adjusters,
        cleaners,
        namespacers,
        required_elts_adders,
        text_data,
        supplementers,
    ):
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, TransformAction) and cls is not TransformAction:
                for frmt in cls.applicable_for:
                    register_action(cls, frmt.uid)
