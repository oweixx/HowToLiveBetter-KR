"""Build the Korean draft with Python's standard library. Code: LICENSE-CODE."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('비용', '핵심', '실행', '기대 효과', '주의', '근거 유형', '출처', '원문 대응', '확인일')


def read(path):
    return path.read_text(encoding='utf-8')


def inline(value):
    """Escape all prose, accepting only explicit HTTP(S) Markdown links."""
    parts, start = [], 0
    for match in re.finditer(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', value):
        parts.extend([html.escape(value[start:match.start()]),
                      '<a href="' + html.escape(match[2], quote=True) +
                      '" rel="noopener noreferrer">' + html.escape(match[1]) + '</a>'])
        start = match.end()
    parts.append(html.escape(value[start:]))
    return ''.join(parts)


def entries(path):
    raw = read(path)
    matches = list(re.finditer(r'^### (\d+)\. (.+)$', raw, re.M))
    result = []
    for i, match in enumerate(matches):
        section = raw[match.end():matches[i+1].start() if i+1 < len(matches) else len(raw)]
        pairs = re.findall(r'^- ([^:]+): (.+)$', section, re.M)
        fields = dict(pairs)
        if len(pairs) != len(REQUIRED) or set(fields) != set(REQUIRED):
            raise ValueError(f'{path.name}:{match[1]}: missing or duplicate fields')
        if int(match[1]) != i+1 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', fields['확인일']):
            raise ValueError(f'{path.name}: numbering/date invalid')
        if not re.search(r'\[[^\]]+\]\(https?://[^\s)]+\)', fields['출처']):
            raise ValueError(f'{path.name}:{match[1]}: source link missing')
        result.append(dict(id=f'kr-{path.stem}-{i+1:02}', chapter=int(path.stem),
                           title=match[2], fields=fields))
    if not result:
        raise ValueError(f'{path.name}: empty chapter')
    return result


def source_inventory():
    result = []
    patterns = {
        'currency': r'元|人民币|万元|公积金',
        'china_policy': r'户口|户籍|社保|医保|民法典|刑法|备案|劳动合同法|公安|中国|我国',
        'phone_number': r'(?<!\d)(?:110|120|119|123\d{2}|123\d{3})(?!\d)',
        'medical_or_safety': r'死亡|药|病|急救|疫苗|孕|婴|中毒',
        'statistics': r'\d+(?:\.\d+)?\s*(?:%|％)|\b(?:HR|RR|OR)\b',
    }
    for path in sorted((ROOT/'book').glob('*.md')):
        raw = read(path)
        matches = list(re.finditer(r'^### (\d+)\. (.+)$', raw, re.M))
        for i, match in enumerate(matches):
            body = raw[match.start():matches[i+1].start() if i+1<len(matches) else len(raw)]
            result.append(dict(id=f'zh-{path.name[:2]}-{int(match[1]):02}',
                               file=path.relative_to(ROOT).as_posix(), number=int(match[1]),
                               title=match[2], sha256=hashlib.sha256(body.encode()).hexdigest(),
                               review_flags=[name for name, pattern in patterns.items() if re.search(pattern, body)],
                               status='pending', korean_entries=[], decision=None))
    return result


def render(meta, cards, inventory):
    completed_chapters = {card['chapter'] for card in cards}
    options = '<option value="">모든 장</option>' + ''.join(
        f'<option value="{n}">{n:02}. {html.escape(title)}</option>'
        for n, title, _ in meta['chapters'] if n in completed_chapters)
    rendered = []
    for card in cards:
        fields = card['fields']
        rendered.append(f'<article id="{card["id"]}" data-chapter="{card["chapter"]}">'
                        f'<div class="eyebrow">{card["chapter"]:02}장 · 한국판 초안</div>'
                        f'<h2><a href="#{card["id"]}">{html.escape(card["title"])}</a></h2>'
                        f'<p class="summary">{inline(fields["핵심"])}</p><dl>' +
                        ''.join(f'<dt>{key}</dt><dd>{inline(fields[key])}</dd>'
                                for key in REQUIRED if key != '핵심') + '</dl></article>')
    roadmap = ''.join(f'<li><strong>{n:02}. {html.escape(title)}</strong>'
                      f'<span class="badge">{"일부 초안 작성" if n in completed_chapters else "작성 대기"}</span>'
                      f'<p>{html.escape(plan)}</p></li>' for n,title,plan in meta['chapters'])
    template = read(ROOT/'ko/site-template.html')
    values = dict(TITLE=html.escape(meta['title']), OPTIONS=options, CARDS='\n'.join(rendered),
                  ROADMAP=roadmap, COUNT=str(len(cards)), CHAPTERS=str(len(completed_chapters)),
                  SOURCE_COUNT=str(len(inventory)), DATE=meta['checked_at'])
    for key, value in values.items():
        template = template.replace('{{'+key+'}}', value)
    if re.search(r'\{\{[A-Z_]+\}\}', template):
        raise ValueError('unresolved template fields')
    return template


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    meta = json.loads(read(ROOT/'ko/editorial.json'))
    cards = [card for path in sorted((ROOT/'ko/book').glob('*.md')) for card in entries(path)]
    inventory = source_inventory()
    if len({item['id'] for item in inventory}) != len(inventory):
        raise ValueError('duplicate original IDs')
    if len({item['id'] for item in cards}) != len(cards):
        raise ValueError('duplicate Korean IDs')
    if any(card['chapter'] not in {chapter[0] for chapter in meta['chapters']} for card in cards):
        raise ValueError('unknown Korean chapter')
    existing_map = ROOT/'ko/source-map.json'
    # Human review decisions persist; an edited source invalidates its prior review.
    if existing_map.exists():
        old = {row['id']:row for row in json.loads(read(existing_map))['entries']}
        for row in inventory:
            previous = old.get(row['id'], {})
            if previous.get('sha256') == row['sha256']:
                for key in ('status','korean_entries','decision'):
                    row[key] = previous.get(key, row[key])
    for row in inventory:
        if row['status'] not in ('pending','reviewed'):
            raise ValueError('invalid source review state')
        if row['status'] == 'reviewed' and not row['decision']:
            raise ValueError('reviewed entry needs an explicit editorial decision')
        if set(row['korean_entries']) - {card['id'] for card in cards}:
            raise ValueError('source map points to missing Korean entry')
    mapping = {'source_commit':meta['source_commit'], 'note':'pending은 미완료. 연결만으로 전체 반영을 뜻하지 않습니다.', 'entries':inventory}
    outputs = {'index.html':render(meta,cards,inventory),
               'ko/source-map.json':json.dumps(mapping,ensure_ascii=False,indent=2)+'\n'}
    for name, value in outputs.items():
        path = ROOT/name
        if args.check:
            if not path.exists() or read(path) != value:
                raise SystemExit(f'Outdated: {name}; run python tools/build-korean.py')
        else:
            path.write_text(value,encoding='utf-8',newline='\n')
    print(f'Korean draft: {len(cards)} entries, {len({c["chapter"] for c in cards})} chapters; source inventory: {len(inventory)} entries.')


if __name__ == '__main__':
    main()
