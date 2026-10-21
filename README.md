# 기억의 날짜

오늘 날짜에 일어난 역사와 인문학 이야기를 1993년 벽걸이 달력 느낌으로 보여주는 모바일 웹 앱입니다.

## 공개 버전 (GitHub Pages)
- `index.html` : 공개 앱. 접속한 날의 기록만 보여 주고 다른 날짜로 이동하는 기능은 없습니다.
- `data/YYYY-MM.json` : 한 달 분량의 기록. 매달 초에 새 달 파일을 올립니다. 형식은 `"MM-DD": {featured, events, notes}`입니다.
- `featured.sig` 는 이날의 한 장면이 가진 역사적 의의, `featured.refs` 는 참고 링크입니다.

## 원본과 글꼴
- `source/date-memory.html` : 날짜 이동과 Claude 호출 기능이 있는 전체 기능판(claude.ai 아티팩트 원본).
- `source/build_public.py` : 원본에서 공개판 `index.html`을 만드는 스크립트 (`python3 source/build_public.py`, 저장소 루트에서 실행).
- `OwnglyphJaegeonsa.ttf` : 타이틀 글꼴 원본(온글잎 재건사). `title-subset.ttf`는 타이틀 글자만 추린 파일이며 index.html에 인라인으로 들어 있습니다.
