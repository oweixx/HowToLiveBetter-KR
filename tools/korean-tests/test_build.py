"""Validate source traceability and safe rendering rather than clinical content."""
import importlib.util
import json
import re
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('build_ko', Path(__file__).resolve().parents[1]/'build-korean.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class KoreanBuildTests(unittest.TestCase):
    def test_markup_is_escaped_and_unsafe_links_are_not_links(self):
        rendered = build.inline('<script>alert(1)</script> [위험](javascript:alert(1)) [출처](https://example.org/?a=1&b=2)')
        self.assertNotIn('<script>', rendered)
        self.assertNotIn('href="javascript:', rendered)
        self.assertIn('href="https://example.org/?a=1&amp;b=2"', rendered)

    def test_missing_fields_fail_instead_of_silently_losing_content(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'01.md'
            path.write_text('### 1. 제목\n- 비용: 시간\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                build.entries(path)

    def test_original_inventory_is_complete(self):
        inventory = build.source_inventory()
        self.assertEqual(641, len(inventory))
        self.assertEqual(34, len({row['file'] for row in inventory}))
        self.assertEqual(641, len({row['id'] for row in inventory}))
        for row in inventory:
            self.assertEqual('pending', row['status'])
            self.assertEqual(64, len(row['sha256']))

    def test_generated_page_has_all_entries_and_no_original_ads(self):
        page = build.read(build.ROOT/'index.html')
        cards = [card for path in (build.ROOT/'ko/book').glob('*.md') for card in build.entries(path)]
        corpus=json.loads(re.search(r'window\.__CORPUS__=(.*?);</script>',page,re.S)[1])
        self.assertEqual(34,len(corpus['parts']))
        self.assertEqual(len(cards),sum(len(re.findall(r'^### \d+\.',part,re.M)) for part in corpus['parts'].values()))
        self.assertIn('class="sidebar"',page)
        self.assertIn('id="theme"',page)
        for dimension in ('ratio','lens','grade','money','time','will'):
            self.assertIn('data-dim="'+dimension+'"',page)
        self.assertIn('<html lang="ko">', page)
        self.assertNotIn('wechat-reward', page)
        self.assertNotIn('mcyyy', page)
        self.assertNotIn('{{', page)
        self.assertNotIn('人民币', page)

    def test_review_links_are_valid(self):
        ids = {card['id'] for path in (build.ROOT/'ko/book').glob('*.md') for card in build.entries(path)}
        mapping = json.loads(build.read(build.ROOT/'ko/source-map.json'))
        for row in mapping['entries']:
            self.assertFalse(set(row['korean_entries']) - ids)
            if row['status'] == 'reviewed':
                self.assertTrue(row['decision'])


if __name__ == '__main__':
    unittest.main()
