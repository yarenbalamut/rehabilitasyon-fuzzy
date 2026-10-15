"""Regression tests for the educational fuzzy model; require scikit-fuzzy."""
import math
import unittest

from fuzzy_logic import evaluate_patient, INPUT_RANGES, rules


class FuzzyModelTests(unittest.TestCase):
    def test_rule_count(self):
        self.assertEqual(len(rules), 62)

    def test_typical_inputs(self):
        a, b = evaluate_patient(75, 16, 96, 110, 36.8)
        for value in (a, b):
            self.assertTrue(math.isfinite(value))
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)

    def test_previous_membership_boundaries(self):
        scenarios = [
            (75, 16, 100, 110, 36.8),
            (60, 16, 96, 110, 36.8),
            (100, 16, 96, 110, 36.8),
            (75, 12, 96, 110, 36.8),
            (75, 20, 96, 110, 36.8),
            (75, 16, 90, 110, 36.8),
            (75, 16, 96, 90, 36.8),
            (75, 16, 96, 120, 36.8),
            (75, 16, 96, 110, 36.0),
            (75, 16, 96, 110, 37.5),
        ]
        for scenario in scenarios:
            with self.subTest(inputs=scenario):
                a, b = evaluate_patient(*scenario)
                self.assertTrue(all(math.isfinite(v) and 0 <= v <= 100
                                    for v in (a, b)))

    def test_out_of_range_and_nonfinite(self):
        baseline = [75, 16, 96, 110, 36.8]
        for i, (low, high) in enumerate(INPUT_RANGES.values()):
            for bad in (low - 1, high + 1, float('nan'), float('inf')):
                values = baseline.copy()
                values[i] = bad
                with self.subTest(index=i, value=bad):
                    with self.assertRaises(ValueError):
                        evaluate_patient(*values)

    def test_evaluation_independence(self):
        first = evaluate_patient(75, 16, 96, 110, 36.8)
        evaluate_patient(130, 26, 85, 145, 39)
        last = evaluate_patient(75, 16, 96, 110, 36.8)
        self.assertAlmostEqual(first[0], last[0], places=5)
        self.assertAlmostEqual(first[1], last[1], places=5)


if __name__ == '__main__':
    unittest.main()
