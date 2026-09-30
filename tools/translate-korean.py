"""Prepare a resumable Korean translation draft of the public upstream corpus.

Uses Google's public translation endpoint without credentials. This is a draft
translation aid, not a medical/legal verifier. URLs, numbering, evidence grades
and machine-readable cost tags are preserved. No local private files are sent.
"""
import concurrent.futures
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT/'.translation-work'
CACHE.mkdir(exist_ok=True)
FIELDS = {'成本':'비용','说人话':'쉽게 말하면','收益':'기대 효과','证据等级':'근거 등급','来源':'출처','备注':'참고'}


def translate(values):
    digest = hashlib.sha256(json.dumps(values,ensure_ascii=False).encode()).hexdigest()
    cached = CACHE/(digest+'.json')
    if cached.exists():
        return json.loads(cached.read_text(encoding='utf-8'))
    if sum(len(v) for v in values)>1600:
        if len(values)>1:
            result=[translate([v])[0] for v in values]
        else:
            pieces=re.split(r'(?<=[。；！？])',values[0])
            chunks=[]
            current=''
            for piece in pieces:
                if len(current)+len(piece)>1200 and current:
                    chunks.append(current);current=''
                current+=piece
            if current:chunks.append(current)
            if len(chunks)==1:
                chunks=[values[0][i:i+1000] for i in range(0,len(values[0]),1000)]
            result=[' '.join(translate([chunk])[0] for chunk in chunks)]
        cached.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
        return result
    urls = {}
    def protect(m):
        key = f'URLKEEP{len(urls):05}END'
        urls[key] = m[0]
        return key
    protected = [re.sub(r'https?://[^\s<>）)]+',protect,v) for v in values]
    payload = '\n\n'.join(f'[{i:04}]\n{v}' for i,v in enumerate(protected))
    endpoint = 'https://translate.googleapis.com/translate_a/single?'+urllib.parse.urlencode(
        {'client':'gtx','sl':'zh-CN','tl':'ko','dt':'t','q':payload})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(endpoint,timeout=50) as response:
                data=json.load(response)
            translated=''.join(x[0] for x in data[0] if x[0])
            marks=list(re.finditer(r'\[\s*(\d{4})\s*\]',translated))
            if [int(m[1]) for m in marks] != list(range(len(values))):
                raise ValueError('translation separators changed')
            result=[]
            for i,m in enumerate(marks):
                value=translated[m.end():marks[i+1].start() if i+1<len(marks) else len(translated)].strip()
                for key,url in urls.items():
                    value=re.sub(r'\s*'.join(re.escape(ch) for ch in key),lambda _:url,value,flags=re.I)
                if 'URLKEEP' in value.upper():
                    raise ValueError('unrestored URL marker')
                expected=re.findall(r'https?://[^\s<>）)]+',values[i])
                if any(url not in value for url in expected):
                    raise ValueError('source URL lost in translation')
                result.append(re.sub(r'\s*\n\s*',' ',value))
            cached.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
            return result
        except Exception as exc:
            if attempt==4:
                if len(values)>1:
                    result=[translate([v])[0] for v in values]
                    cached.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
                    return result
                raise RuntimeError(f'translation failed: {digest}: {type(exc).__name__}') from exc
            time.sleep(min(2**attempt,16))


def chapter(path):
    raw=path.read_text(encoding='utf-8')
    n=int(path.name[:2])
    meta=json.loads((ROOT/'ko/editorial.json').read_text(encoding='utf-8'))
    title=next(x[1] for x in meta['chapters'] if x[0]==n)
    headings=list(re.finditer(r'^### (\d+)\. (.+)$',raw,re.M))
    out=[f'[전체 목차](../../README.md)\n\n# {n}. {title}\n',
         '원문의 항목 번호·근거·출처를 보존한 한국어 번역 초안입니다. 중국 제도와 통계는 대한민국에 그대로 적용되지 않습니다. 한국 제도와의 대조 및 문장 검수는 진행 중입니다.\n']
    for i,m in enumerate(headings):
        body=raw[m.end():headings[i+1].start() if i+1<len(headings) else len(raw)]
        fields=re.findall(r'^- (成本|说人话|收益|证据等级|来源|备注)：(.*)$',body,re.M)
        values=[m[2]]+[value for key,value in fields if key not in ('证据等级','来源')]
        trans=translate(values)
        cursor=1
        out.append(f'### {m[1]}. {trans[0]}')
        tag=re.search(r'^<!-- 成本标签:.*?-->',body,re.M)
        if tag:out.append(tag[0])
        for key,value in fields:
            if key not in ('证据等级','来源'):value=trans[cursor];cursor+=1
            out.append(f'- {FIELDS[key]}: {value.strip()}')
        out.append('')
    # Quarantine machine drafts; they must never be deployed as reviewed advice.
    dest=CACHE/'full-book'/f'{n:02}.md'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
    print(f'chapter {n:02}: {len(headings)} entries translated',flush=True)
    return len(headings)


if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(chapter,p):p for p in sorted((ROOT/'book').glob('*.md'))}
        total=0
        failures=[]
        for job in concurrent.futures.as_completed(jobs):
            try:total+=job.result()
            except Exception as exc:
                failures.append(jobs[job].name)
                print(f'FAILED {jobs[job].name[:2]}: {exc}',flush=True)
    print(f'Translation draft ready: {total} entries',flush=True)
    if failures:raise SystemExit(f'{len(failures)} chapters need retry')
