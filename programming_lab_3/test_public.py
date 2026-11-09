"""Public examples, not the complete grading suite. Do not edit."""
import copy
import unittest
import inference as student
from models import get_model


class PublicTests(unittest.TestCase):
    def assertVector(self, actual, expected):
        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), len(expected))
        for a, e in zip(actual, expected):
            self.assertAlmostEqual(a, e, delta=1e-9)

    def test_prediction_asymmetric(self):
        self.assertVector(student.predict([.8, .2], [[.9, .1], [.4, .6]]), [.8, .2])

    def test_update_umbrella(self):
        self.assertVector(student.update([.5, .5], 0, [[.9, .1], [.2, .8]]), [9/11, 2/11])

    def test_classroom_filter(self):
        m = get_model()
        result = student.filter_sequence(m.prior, [0, 0, 1], m.transition, m.sensor)
        self.assertEqual(len(result), 3)
        for b, p in zip(result, [9/11, 621/703, 4593/24089]):
            self.assertVector(b, [p, 1-p])

    def test_empty_sequence(self):
        m = get_model()
        self.assertEqual(student.filter_sequence(m.prior, [], m.transition, m.sensor), [])

    def test_three_states(self):
        m = get_model("three_state")
        self.assertVector(student.predict(m.prior, m.transition), [.52, .33, .15])
        # P(U) = .52*.1 + .33*.4 + .15*.85 = .3115.
        self.assertVector(student.update([.52, .33, .15], 0, m.sensor),
                          [.052/.3115, .132/.3115, .1275/.3115])

    def test_zero_evidence(self):
        with self.assertRaises(ValueError):
            student.update([.5, .5], 1, [[1., 0.], [1., 0.]])

    def test_zero_step_is_copy(self):
        m = get_model()
        result = student.predict_steps(m.prior, m.transition, 0)
        self.assertVector(result, m.prior)
        self.assertIsNot(result, m.prior)

    def test_two_steps(self):
        self.assertVector(student.predict_steps([1., 0.], [[.7, .3], [.3, .7]], 2), [.58, .42])

    def test_inputs_and_history_are_independent(self):
        m = get_model()
        before = copy.deepcopy(m)
        obs = [0, 1, 0]
        hist = student.filter_sequence(m.prior, obs, m.transition, m.sensor)
        self.assertEqual(m, before)
        self.assertEqual(obs, [0, 1, 0])
        self.assertEqual(len({id(b) for b in hist}), 3)
        self.assertTrue(all(b is not m.prior for b in hist))


if __name__ == "__main__":
    unittest.main()
