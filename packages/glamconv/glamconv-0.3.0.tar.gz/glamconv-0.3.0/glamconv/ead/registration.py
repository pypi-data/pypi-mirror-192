# -*- coding: utf-8 -*-

import inspect
from glamconv.transformer.libraries import register_format, register_action
from glamconv.transformer.actions import TransformAction
from glamconv.ead.formats import EAD_2002, EAD_APE
from glamconv.ead import (
    ead_2002_correcters,
    cleaners,
    adjusters,
    arch_data,
    header,
    link_managers,
    namespacers,
    text_data,
    supplementers,
)


def register():
    # Formats
    register_format(EAD_2002)
    register_format(EAD_APE)
    # Actions
    for module in (
        ead_2002_correcters,
        cleaners,
        adjusters,
        arch_data,
        header,
        link_managers,
        namespacers,
        text_data,
        supplementers,
    ):
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, TransformAction) and cls is not TransformAction:
                for frmt in cls.applicable_for:
                    register_action(cls, frmt.uid)
