import types
import unittest

from unicode_linebreak import linebreaks, Allowed, Mandatory


class TestPyUnicodeLinebreak(unittest.TestCase):
    def test_linebreaks_returns_generator(self):
        string = "a b\nc\r\nd e\rf end"
        linebreaker = linebreaks(string)
        self.assertIs(hasattr(linebreaker, "__iter__"), True)
        self.assertIs(hasattr(linebreaker, "__next__"), True)

        self.assertEqual(next(linebreaker), (2, Allowed))
        self.assertEqual(next(linebreaker), (4, Mandatory))
        self.assertEqual(next(linebreaker), (7, Mandatory))
        self.assertEqual(next(linebreaker), (9, Allowed))
        self.assertEqual(next(linebreaker), (11, Mandatory))
        self.assertEqual(next(linebreaker), (13, Allowed))
        self.assertEqual(next(linebreaker), (16, Mandatory))

    def test_simple(self):
        string = "a b\nc\r\nd e\rf end"
        expected_result = [
            (2, Allowed),
            (4, Mandatory),
            (7, Mandatory),
            (9, Allowed),
            (11, Mandatory),
            (13, Allowed),
            (16, Mandatory),
        ]
        self.assertListEqual(list(linebreaks(string)), expected_result)

    def test_scriptio_continua_linebreaks(self):
        string = (
            "支持常见的温度传感器（例如，常见的热敏电阻、"
            "AD595、AD597、AD849x、PT100、PT1000、"
            "MAX6675、MAX31855、MAX31856、MAX31865、"
            "BME280、HTU21D和LM75）。"
            "还可以配置自定义热敏电阻和自定义模拟温度传感器。"
        )
        expected_result = [
            (3, Allowed),
            (6, Allowed),
            (9, Allowed),
            (12, Allowed),
            (15, Allowed),
            (18, Allowed),
            (21, Allowed),
            (24, Allowed),
            (27, Allowed),
            (30, Allowed),
            (36, Allowed),
            (42, Allowed),
            (45, Allowed),
            (48, Allowed),
            (51, Allowed),
            (54, Allowed),
            (57, Allowed),
            (60, Allowed),
            (66, Allowed),
            (74, Allowed),
            (82, Allowed),
            (91, Allowed),
            (99, Allowed),
            (108, Allowed),
            (118, Allowed),
            (129, Allowed),
            (140, Allowed),
            (151, Allowed),
            (160, Allowed),
            (166, Allowed),
            (169, Allowed),
            (179, Allowed),
            (182, Allowed),
            (185, Allowed),
            (188, Allowed),
            (191, Allowed),
            (194, Allowed),
            (197, Allowed),
            (200, Allowed),
            (203, Allowed),
            (206, Allowed),
            (209, Allowed),
            (212, Allowed),
            (215, Allowed),
            (218, Allowed),
            (221, Allowed),
            (224, Allowed),
            (227, Allowed),
            (230, Allowed),
            (233, Allowed),
            (236, Allowed),
            (239, Allowed),
            (242, Allowed),
            (245, Allowed),
            (251, Mandatory),
        ]

        self.assertListEqual(list(linebreaks(string)), expected_result)
