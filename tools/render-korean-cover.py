"""Keep the original cover layout while localizing all visible text."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/og.html').read_text(encoding='utf-8')
source=re.sub(r'<!--.*?-->','<!-- Korean cover; preserve upstream layout. -->',source,flags=re.S)
source=source.replace('<!doctype html>','<!doctype html><html lang="ko">')
source=source.replace('"Microsoft YaHei","PingFang SC"','"Malgun Gothic","Apple SD Gothic Neo"')
source=source.replace('高性价比人生指南','가성비 높은 삶을 위한 안내서')
source=source.replace('用最少的钱、时间和精力，<br>换回<em>寿命、金钱和自由</em>','돈과 시간, 노력을 아껴<br><em>더 나은 삶을 위한 선택</em>')
source=source.replace('长寿防病 · 急救 · 省钱理财 · 法律红线 · 失业兜底 · 恋爱婚育 · 出国 · 技能','건강 · 응급처치 · 생활비 · 주거 · 일과 복지 · 가족 · 배움')
source=source.replace('<b>641</b> 条建议','원문 <b>34장 · 641개 항목</b>')
source=source.replace('A 级证据 <b>425</b> 条','<b>비공식 한국판</b>')
source=source.replace('<b>1443</b> 条原始文献链接','한국 현지화 진행 중')
source=source.replace('可按性价比筛选','oweixx')
source=source.replace('font-size:82px','font-size:72px')
source+='\n</html>\n'
(ROOT/'ko/cover.html').write_text(source,encoding='utf-8',newline='\n')
chrome=shutil.which('google-chrome') or shutil.which('chromium') or 'C:/Program Files/Google/Chrome/Application/chrome.exe'
with tempfile.TemporaryDirectory(prefix='korean-cover-') as profile:
    result=subprocess.run([chrome,'--headless=new','--disable-gpu','--hide-scrollbars',
                           '--force-device-scale-factor=1','--window-size=1200,630',
                           '--user-data-dir='+profile,'--screenshot='+str(ROOT/'og.png'),
                           (ROOT/'ko/cover.html').as_uri()],capture_output=True,timeout=60)
    if result.returncode:raise SystemExit(result.stderr.decode(errors='replace'))
shutil.copyfile(ROOT/'og.png',ROOT/'ko/og.png')
print('Korean original-layout cover rendered')
