# 가성비 높은 삶을 위한 안내서 · 한국판

![한국의 제도와 생활에 맞춰 다시 쓰는 HowToLiveBetter 비공식 한국판. 한국 현지화 초안.](og.png)

**현재 일부 내용을 작성한 현지화 초안입니다. 원문 전체의 번역·검수는 진행 중입니다.**

중국의 제도·가격·사회적 사례를 대한민국에서 사용할 수 있는 안내로 다시 쓰는 프로젝트입니다. 위안화를 원화로 환산하는 데 그치지 않고, 지원 대상·신청 창구·법적 조건·예외를 한국의 공식 자료로 다시 확인합니다. 해외 연구의 대상과 한계를 한국인의 효과로 바꾸지 않습니다.

- 한국판 웹 화면: 저장소를 내려받아 [index.html](index.html)을 브라우저로 열면 됩니다. 별도 설치 없이 검색할 수 있습니다.
- 한국어 본문: [ko/book](ko/book)
- 전체 34장 편집 범위: [ko/editorial.json](ko/editorial.json)
- 원문 641개 항목의 검토 상태: [ko/source-map.json](ko/source-map.json)
- 편집 기준과 이미지 처리: [ko/LOCALIZATION.md](ko/LOCALIZATION.md)

한국판 항목은 여러 원문 항목을 합치거나 한국 제도로 대체할 수 있습니다. 한국판 초안 수는 번역 완료한 원문 항목 수가 아닙니다. `source-map.json`의 `pending`은 아직 전체 대응 검토가 끝나지 않았다는 뜻입니다. 작성된 초안도 내용 검수가 필요합니다.

## 현재 작성한 내용

| 장 | 한국판 초안 | 주요 변경 |
| --- | --- | --- |
| 5 | [돈을 지키는 소비와 금융](ko/book/05.md) | 예금보호, 채무 상담, 원화 계산 예시 |
| 7 | [소득이 끊겼을 때](ko/book/07.md) | 구직급여, 긴급복지, 고용24 |
| 15 | [전세·월세와 내 집 마련](ko/book/15.md) | 등기, 전입신고, 확정일자, 보증금 반환 |
| 19 | [재직·퇴사·산재](ko/book/19.md) | 한국 최저임금, 퇴직금, 임금체불 |
| 24 | [병원 이용과 의료비](ko/book/24.md) | 진료 절차, 응급실, 재난적의료비 |

다른 장의 계획은 웹 화면의 전체 목차에서도 확인할 수 있습니다. 의료·법률·복지 항목은 출처와 적용 조건을 함께 읽어 주세요. 확인일은 자료를 확인한 날짜이며 모든 상황에서 같은 결과를 보장하는 날짜가 아닙니다.

## 원작과 이용 조건

원작은 [eternity4719의 《高性价比人生指南》](https://github.com/eternity4719/HowToLiveBetter)입니다. 한국판 기준 원문은 [`d63794d`](https://github.com/eternity4719/HowToLiveBetter/tree/d63794d5dba477ca42b3309a5ae5b396f330c35f)입니다. 원래 [중국어 README](README.zh-CN.md)와 `book/`, `docs/`는 원문 비교용으로 보존합니다.

한국어 번역·한국 제도에 맞춘 재구성·한국판 디자인은 **oweixx / HowToLiveBetter-KR**에서 관리합니다. 비공식 파생판이며 원작자의 한국판 검수나 보증을 뜻하지 않습니다. 한국판의 오류는 이 저장소의 이슈로 알려 주세요.

- 본문과 한국판 이미지: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ko), [라이선스 전문](LICENSE)
- 코드: [MIT](LICENSE-CODE), 기존 저작권 고지 유지

재배포할 때 원작자와 한국판 출처, 라이선스 링크, 수정 사실을 표시해야 합니다. 원작자의 광고·위챗 후원 QR은 한국판 화면에 사용하지 않습니다.

## 개발과 검증

Python 3으로 외부 패키지 없이 빌드합니다.

```sh
python tools/build-korean.py
python tools/build-korean.py --check
python -m unittest discover -s tools/korean-tests
```

`ko/book/*.md`와 `ko/site-template.html`을 수정한 뒤 빌드하면 `index.html`과 원문 검토 목록을 갱신합니다. 원문이 바뀌면 해당 항목의 검토 상태를 다시 `pending`으로 돌립니다. 사람의 검토 기록은 원문이 같을 때 유지합니다. 검색 화면은 네트워크 연결 없이 읽을 수 있지만 외부 출처 링크에는 인터넷 연결이 필요합니다.

표지 원본은 [ko/cover.html](ko/cover.html)입니다. 1200×630, 배율 1로 캡처해 `og.png`와 `ko/og.png`를 함께 갱신합니다. 중국어 원문의 통계·전자책 스크립트는 한국판 배포에 사용하지 않습니다.
