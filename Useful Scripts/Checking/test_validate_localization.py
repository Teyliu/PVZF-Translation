"""Regression checks for protected localization content; no network required."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).with_name('validate_localization.py')
spec = importlib.util.spec_from_file_location('validator', path)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def compare(self, source, target):
        errors = []
        validator.compare(source, target, 'fixture', errors, validator.Counter())
        return errors

    def test_current_english_reference(self):
        errors, counts = validator.validate(validator.BASE / 'English', validator.BASE / 'English')
        self.assertEqual(errors, [])
        self.assertGreater(counts['text_fields'], 0)

    def test_translation_preserves_game_data(self):
        source = {'plants': [{'seedType': 7, 'info': '<color=red>Damage {value}: 20/1.5s\\n</color>'}]}
        translated = copy.deepcopy(source)
        translated['plants'][0]['info'] = '<color=red>Schaden {value}: 20/1.5s\\n</color>'
        self.assertEqual(self.compare(source, translated), [])
        mutations = {
            'seedType': 8,
            'info': '<color=blue>Schaden {other}: 21/1.5s</color>',
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                broken = copy.deepcopy(translated)
                broken['plants'][0][field] = value
                self.assertTrue(self.compare(source, broken))

    def test_missing_or_extra_lookup_key(self):
        for target in ({}, {'a': 'A', 'unexpected': 'B'}):
            with self.subTest(target=target):
                self.assertTrue(self.compare({'a': 'A'}, target))

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'duplicate.json'
            path.write_text('{"x": "A", "x": "B"}', encoding='utf-8')
            with self.assertRaises(ValueError):
                validator.read_json(path)

    def test_internal_translation_markers_rejected(self):
        self.assertTrue(self.compare('Plant', 'ZXQ00001QXZ'))

    def test_arrow_caption_can_be_translated(self):
        self.assertEqual(self.compare('|<----Range---->|', '|<----Reichweite---->|'), [])

    def test_vertical_tab_preserved(self):
        self.assertTrue(self.compare('Before\vAfter', 'VorherNachher'))
        self.assertEqual(self.compare('Before\vAfter', 'Vorher\vNachher'), [])

    def test_unknown_selected_file_rejected(self):
        errors, _ = validator.validate(validator.BASE / 'English', validator.BASE / 'English', ['Strings/missing.json'])
        self.assertTrue(errors)


if __name__ == '__main__':
    unittest.main()
