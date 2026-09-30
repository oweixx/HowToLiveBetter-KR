"""Restore the upstream reader's layout, changing only localization/integration."""
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'ko/upstream-index.html').read_text(encoding='utf-8')
s=re.sub(r'<!-- ga:start.*?<!-- ga:end -->','',s,flags=re.S)
s=re.sub(r'<noscript>.*?</noscript>','<noscript><p>검색과 필터에는 JavaScript가 필요합니다. <a href="https://github.com/oweixx/HowToLiveBetter-KR/tree/korean-edition/ko/full-book">한국어 본문 파일</a>에서도 읽을 수 있습니다.</p></noscript>',s,flags=re.S)
s=re.sub(r'  <div class="group ad">.*?</div>\s*</aside>','</aside>',s,flags=re.S)
s=re.sub(r'<div id="tip-mask".*?(?=<div id="xref-pop")','',s,flags=re.S)
s=re.sub(r'/\* ---------- 赞赏码弹窗 ---------- \*/.*?(?=\(async function init\(\))','',s,flags=re.S)
s=s.replace('eternity4719.github.io/HowToLiveBetter','oweixx.github.io/HowToLiveBetter-KR')
s=s.replace('github.com/eternity4719/HowToLiveBetter','github.com/oweixx/HowToLiveBetter-KR')
s=s.replace('/blob/main/','/blob/korean-edition/').replace('/tree/main/','/tree/korean-edition/')
s=s.replace('zh-CN','ko').replace('zh_CN','ko_KR').replace('deed.zh-hans','deed.ko')
s=s.replace('"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC"','"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR"')
s=re.sub(r'<div class="doc-head">.*?<details class="gloss"', '''<div class="doc-head">
      <h1>가성비 높은 삶을 위한 안내서</h1>
      <p>각 항목에서 무엇을 들이고, 무엇을 얻는지 살펴봅니다.</p>
      <p>모두 실천할 필요는 없습니다. 필요한 내용을 골라 읽고, 왼쪽에서 돈·시간·노력과 근거 등급으로 찾아보세요. 항목 번호와 출처는 원문과 대조할 수 있도록 유지합니다.</p>
      <p><strong>비공식 한국판 · 번역 및 한국 제도 대조 진행 중.</strong> 중국 제도·금액·기관을 한국 기준으로 받아들이지 마세요. 각 장의 한국 안내와 검토 표시를 함께 확인하세요.</p>
      <div class="stat" aria-live="polite">현재 <b id="cnt">–</b>개 표시 · 전체 <span id="tot">–</span>개</div>
      <div class="doc-links"><a href="https://github.com/oweixx/HowToLiveBetter-KR">한국판 저장소</a> · <a href="https://github.com/eternity4719/HowToLiveBetter">원작 eternity4719</a> · <a href="https://github.com/oweixx/HowToLiveBetter-KR/blob/korean-edition/ko/REVIEW-NOTES.md">현지화 검토 기록</a></div>
      <details class="gloss"''',s,flags=re.S)
s=re.sub(r'<div class="foot">.*?</div>', '<div class="foot">건강·돈·시간·권리의 효과는 서로 다른 기준입니다. 해외 연구 결과는 한국인에게 같은 효과를 보장하지 않습니다. 원작 eternity4719, 한국어판 oweixx. 본문 <a href="https://creativecommons.org/licenses/by/4.0/deed.ko">CC BY 4.0</a> · 코드 MIT. 원작 출처와 변경 사실을 표시해 재배포할 수 있습니다.</div>',s,flags=re.S)
description='한국 생활에 맞춰 번역·대조하는 삶의 안내서. 원문의 34장과 항목별 비용·효과·근거·출처, 검색과 필터 형식을 유지합니다. 현지화 검토 진행 중.'
s=re.sub(r'按性价比排序的人生指南：641 条建议[^"\n]+',description,s)
s=s.replace('"numberOfPages":641,','')
s=re.sub(r'<meta name="keywords"[^>]+>','<meta name="keywords" content="건강,생활,시간,금융,주거,복지,근거,한국판">',s)
s=s.replace('"about":["健康","长寿","个人理财","急救","法律常识","消费者保护"]','"about":["건강","수명","금융","응급처치","법률","소비자 보호"]')
phrases={
 '高性价比人生指南':'가성비 높은 삶을 위한 안내서','用最少的钱、时间和精力换回寿命、金钱和人身自由':'돈·시간·노력으로 건강과 생활을 지키는 선택',
 '打开筛选':'필터 열기','搜索条目':'항목 검색','查看 README.md':'README 보기','在 GitHub 上查看源仓库':'GitHub 저장소 보기','GitHub 仓库':'GitHub 저장소','切换深色模式':'밝은·어두운 화면 전환',
 '作者判断，同口径内可比':'원문 평가 · 같은 효과 기준끼리 비교','口径，不跨口径比较':'서로 다른 효과는 직접 비교하지 않음','荟萃/RCT · 有研究 · 共识':'통합분석·실험 / 개별 연구 / 경험·합의',
 '只看标了争议的':'논쟁이 있는 항목만','只看有待核实的':'확인이 필요한 항목만','清空筛选':'필터 초기화',
 '章节一次只看一个，成本和等级可多选。同一组多选是「或」，不同组之间是「且」。':'장은 하나씩 선택합니다. 비용과 등급은 여러 개를 선택할 수 있습니다. 같은 필터 안에서는 하나라도 맞으면, 다른 필터끼리는 모두 맞아야 표시됩니다.',
 '每节内按性价比从高到低排，检索不改变顺序。':'검색해도 각 장의 원래 항목 순서를 유지합니다.',
 '正文与标签来自仓库 <a href="book/">book/</a> 下的 34 个文件，改正文即改这里。':'본문은 한국판의 34개 장 파일에서 불러옵니다.',
 '看不懂的缩写和名词':'통계와 근거 용어 설명','正文里带虚线的词，点一下或把鼠标放上去就有解释。全表如下。':'점선 밑줄이 있는 용어를 누르거나 가리키면 설명을 볼 수 있습니다.',
 '正在读取正文 …':'본문을 불러오는 중…','没有匹配的条目。去掉一个筛选条件，或换个更短的关键词。':'조건에 맞는 항목이 없습니다. 필터를 줄이거나 다른 검색어를 입력하세요.',
 '在 GitHub 打开':'GitHub에서 열기','跳过去':'해당 항목으로 이동','关闭':'닫기','全部章节':'전체 목차','展开或收起本节目录':'이 장의 항목 목차 펼치기·접기','没有符合当前筛选的条目':'필터에 맞는 항목이 없습니다','本条链接':'이 항목 링크',
 '花少量钱':'돈이 조금 듦','花不少钱':'돈이 많이 듦','每天占时间':'매일 시간 필요','花几小时':'몇 시간 필요','不用毅力':'지속적인 노력 적음','要一点毅力':'꾸준한 노력 조금','要很多毅力':'꾸준한 노력 많이',
 '不花钱':'돈이 들지 않음','每天占用':'매일 필요','几小时':'몇 시간','顺手':'잠깐','不用':'거의 없음','一点':'조금','很多':'많이',
 '换寿命':'건강·수명','换时间精力':'시간·에너지','换人身自由':'권리·자유','换钱':'돈',
 '含待核实':'검토 필요','性价比':'비용 대비 효과','换回什么':'기대하는 효과','证据等级':'근거 등급','花时间':'드는 시간','要毅力':'꾸준한 노력','花钱':'드는 돈','章节':'목차',
 'A 级':'A 등급','B 级':'B 등급','C 级':'C 등급','寿命':'건강·수명','时间精力':'시간·에너지',
 '`证据 ${e.grade} 级`':'`원문 근거 ${e.grade} 등급`','` · ${nSrc} 条`':'` · ${nSrc}개`',
 '`整节，共 ${sec.entries.length} 条`':'`이 장 전체 · ${sec.entries.length}개`','`第 ${e.sec} 节第 ${e.n} 条`':'`제${e.sec}장 ${e.n}번`',
 '成本':'비용','收益':'효과','备注':'참고','来源':'출처','争议':'논쟁','极高':'매우 높음','一般':'보통',
 '读懂数字':'숫자 읽기','术语':'용어',
}
for a,b in sorted(phrases.items(),key=lambda x:-len(x[0])):s=s.replace(a,b)
# Short tokens are machine values too; the builder applies the same vocabulary
# to the cost metadata, keeping the original filter calculations intact.
tokens={'死亡率':'건강','金钱':'금전','时间':'시간','自由':'자유','毅力':'노력','钱':'돈','少':'적음','多':'많음','否':'없음','些':'조금','是':'있음','大':'큼','中':'중간','小':'작음','高':'높음'}
for a,b in tokens.items():s=s.replace(a,b)
s=s.replace('^- 비용：','^- 비용:').replace('^- 说人话：','^- 쉽게 말하면:').replace('^- 효과：','^- 기대 효과:').replace('^- 근거 등급：','^- 근거 등급:').replace('^- 출처：','^- 출처:').replace('^- 참고：','^- 참고:')
s=s.replace('待核实|TODO','검토 필요|확인 필요|TODO')
s=s.replace("localeCompare(b.term, 'zh')","localeCompare(b.term, 'ko')")
s=s.replace("throw new Error('离线副本里缺 '+f)","throw new Error('본문 파일 누락: '+f)")
s=s.replace('正在读取正文 ${done}/${total}','본문 로딩 ${done}/${total}')
s=s.replace("t.title = '作者判断：", "t.title = '원문 평가: ")
s=re.sub(r"t.title = '원문 평가: .*?;", "t.title = '원문의 비용·효과 평가이며 한국 제도 검수 등급과는 다릅니다.';",s)
s=s.replace('href="README.md"','href="https://github.com/oweixx/HowToLiveBetter-KR/blob/korean-edition/README.md"')
s=s.replace('<script>\n/* ---------- 调试', '<script>\n/* ---------- 调试')
s=s.replace('<script>\n/* ---------- 调试','{{CORPUS}}\n<script>\n/* ---------- 调试',1)
# Korean cross-references use chapter/entry wording, with the same five captures.
s=re.sub(r'const XREF_RE = .*?;',r"const XREF_RE = /제?\\s*(\\d+)\\s*장\\s*제?\\s*(\\d+)\\s*(?:항|번)|이 장\\s*제?\\s*(\\d+)\\s*(?:항|번)|제\\s*(\\d+)\\s*항|제\\s*(\\d+)\\s*장/g;",s,count=1)
s=s.replace('人身자유','권리·자유')
s=s.replace('([ABC])','([ABCK])')
s=s.replace("e.ratio = e.level === '큼'", "e.ratio = e.level === '미정' ? '' : e.level === '큼'")
s=s.replace("add(e.grade, `원문 근거 ${e.grade} 등급`)","add(e.grade, e.grade === 'K' ? '한국판 편집 초안' : `원문 근거 ${e.grade} 등급`)")
s=s.replace("if (e.lens) add", "if (e.lens && e.lens !== '미정') add")
s=s.replace("if (e[d]) add", "if (e[d] && e[d] !== '미정') add")
s=s.replace('>C 등급</button>','>C 등급</button>\n      <button class="chip" data-v="K" aria-pressed="false">한국판 초안</button>')
s=s.replace("b.innerHTML = `<span>${s.n}. ${esc(s.title)}</span><i>${s.entries.length}</i>","b.innerHTML = `<span>${s.n}. ${esc(s.title)}</span><i>${s.entries.length || '대기'}</i>")
s=s.replace("if (b.el.hidden !== (n === 0)) b.el.hidden = n === 0;", "const hide = n === 0 && !(state.sec.has(b.n) && !ITEMS.has(b.n+'-1')); if (b.el.hidden !== hide) b.el.hidden = hide;")
s=s.replace("status.innerHTML = `读取正文失败（${esc(String(err.message))}）。确认 README.md 和 book/ 目录都在 index.html 旁边。`;", "status.innerHTML = `본문 로딩 실패: ${esc(String(err.message))}`;")
s=s.replace('加载失败：','로딩 실패: ').replace('继续加载','다시 불러오기').replace('正在读取 …','불러오는 중…').replace('读不到这篇长文（','문서를 읽지 못했습니다 (')
s=s.replace('</style>','\n.sec-link i{white-space:nowrap;flex-shrink:0}.sec-link span{word-break:keep-all;overflow-wrap:anywhere}\n</style>',1)
(ROOT/'ko/site-template.html').write_text(s,encoding='utf-8',newline='\n')
print('Restored upstream layout with Korean UI')
