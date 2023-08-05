# -*- coding: utf-8 -*-
from unittest import TestCase

from glamconv.transformer.logger import RunLog


class ActionTestCase(TestCase):
    action_class = None

    def run_action(self, input_obj, params=None):
        logger = FakeLog()
        action = self.action_class()
        output_obj = action.run(input_obj, logger, False, params)
        return output_obj


class FakeLog(RunLog):
    def action_start(self, name, param_values):
        pass

    def info(self, message, data=""):
        pass

    def warning(self, message, data=""):
        pass

    def error(self, message, data=""):
        pass
