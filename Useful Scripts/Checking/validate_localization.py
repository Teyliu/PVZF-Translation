#!/usr/bin/env python3
"""Check a localization's structure and protected content against English.

Usage: python "Useful Scripts/Checking/validate_localization.py" German
Only the Python standard library is required. No network calls are made.
Textual JSON files under Almanac/ and Strings/ are checked. Texture manifests
are excluded because their paths and hashes are language-specific.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parents[2] / 'PvZ_Fusion_Translator' / 'Localization'
PATTERNS = {
    'format tags': re.compile(r'<(?:/?[A-Za-z][^>\n]*|#[0-9A-Fa-f]{3,8})>'),
    'placeholders': re.compile(r'\{[^{}\r\n]*\}'),
    'numbers': re.compile(r'\d+(?:[.,]\d+)*'),
    'line breaks and tabs': re.compile(r'\\[nrt]|[\x00-\x1f]'),
    'URLs': re.compile(r'https?://[^\s<>]+'),
}
RESIDUE = re.compile(r'ZXQ\s*\d+\s*QXZ|QZXBOUNDARY\d+')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key!r}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_object)


def compare(source, target, path, errors, counts):
    if type(source) is not type(target):
        errors.append(f'{path}: JSON value type changed')
    elif isinstance(source, dict):
        missing = source.keys() - target.keys()
        extra = target.keys() - source.keys()
        if missing:
            errors.append(f'{path}: missing keys: {sorted(missing)!r}')
        if extra:
            errors.append(f'{path}: unexpected keys: {sorted(extra)!r}')
        for key in source.keys() & target.keys():
            # These pseudo-comments are not strings displayed by the game.
            if key.startswith('---'):
                continue
            compare(source[key], target[key], f'{path}/{key}', errors, counts)
    elif isinstance(source, list):
        if len(source) != len(target):
            errors.append(f'{path}: array length changed')
        for index, (left, right) in enumerate(zip(source, target)):
            compare(left, right, f'{path}/{index}', errors, counts)
    elif isinstance(source, str):
        counts['text_fields'] += 1
        if source.strip() and not target.strip():
            errors.append(f'{path}: nonempty text was removed')
        if RESIDUE.search(target):
            errors.append(f'{path}: internal translation marker left in text')
        for label, pattern in PATTERNS.items():
            if Counter(pattern.findall(source)) != Counter(pattern.findall(target)):
                errors.append(f'{path}: {label} changed')
        if PATTERNS['format tags'].findall(source) != PATTERNS['format tags'].findall(target):
            errors.append(f'{path}: format tag order changed')
    elif source != target:
        errors.append(f'{path}: ID, number, boolean or null changed')


def validate(reference, target, files=None):
    errors = []
    counts = Counter()
    selected = set(files) if files else None
    found = set()
    for folder in ('Almanac', 'Strings'):
        for source_path in sorted((reference / folder).glob('*.json')):
            relative = source_path.relative_to(reference)
            if selected is not None and relative.as_posix() not in selected:
                continue
            found.add(relative.as_posix())
            target_path = target / relative
            if not target_path.is_file():
                errors.append(f'{relative}: missing file')
                continue
            try:
                source = read_json(source_path)
                translated = read_json(target_path)
                compare(source, translated, str(relative), errors, counts)
                counts['files'] += 1
            except (OSError, ValueError) as exc:
                errors.append(f'{relative}: {exc}')
    if not counts['files']:
        errors.append('No reference JSON files found')
    if selected:
        for name in sorted(selected - found):
            errors.append(f'{name}: reference JSON file not found')
    return errors, dict(counts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('language', nargs='?', default='German')
    parser.add_argument('--base', type=Path, default=BASE, help='Localization directory')
    parser.add_argument('--report', type=Path, help='Optional JSON report path')
    parser.add_argument('--file', action='append', dest='files',
                        help='Check only this path relative to the language folder; repeatable')
    args = parser.parse_args()
    errors, counts = validate(args.base / 'English', args.base / args.language, args.files)
    report = {'language': args.language, **counts, 'errors': errors}
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{args.language}: {counts.get('files', 0)} files, {counts.get('text_fields', 0)} text fields, {len(errors)} errors")
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
