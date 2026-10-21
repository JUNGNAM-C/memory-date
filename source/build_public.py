import re,sys
s=open('source/date-memory.html',encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s,a[:60]
    s=s.replace(a,b,1)
# 1) SEED 제거 (기록은 data/YYYY-MM.json에서 읽음)
i=s.index('var SEED={'); j=s.index('function dayCls') if False else None
lines=s.split('\n')
a=next(n for n,l in enumerate(lines) if l.startswith('var SEED={'))
b=next(n for n,l in enumerate(lines) if n>a and l=='};')
lines[a:b+1]=['var SEED={};']
s='\n'.join(lines)
# 2) 데이터 접근
rep("""  if(SEED[k])return SEED[k];
  if(S.gen[k])return S.gen[k];
  try{
    var raw=localStorage.getItem('gen3-'+k);
    if(raw){var v=normalize(JSON.parse(raw));if(v){S.gen[k]=v;return v}}
  }catch(e){}
  return null;""","  return S.gen[k]||null;")
# 3) 빈 화면 문구
a=s.index("function renderEmpty(list){"); b=s.index("function renderRecords") if "function renderRecords" in s[a:] else None
e=s.index("  list.appendChild(box);\n}",a)
s=s[:a]+"""function renderEmpty(list){
  var box=el('div','empty');
  var title=S.m+'월 '+S.d+'일의 기억';
  if(S.loading){
    box.appendChild(el('strong',null,title+'을 불러오는 중입니다'));
  }else{
    box.appendChild(el('strong',null,title+'은 아직 준비되지 않았습니다'));
    box.appendChild(el('p',null,'기억은 매달 초에 한 달 분량을 새로 올립니다. 잠시 뒤에 다시 열어 주세요.'));
  }
"""+s[e:]
# 4) load/go/monthShift 등 제거 후 새 로더
a=s.index("function load(){"); b=s.index("function go(y,m,d){")
s=s[:a]+"""function loadMonth(){
  S.loading=true;show();
  var mm=(S.m<10?'0':'')+S.m;
  fetch('data/'+S.y+'-'+mm+'.json',{cache:'no-cache'}).then(function(r){
    if(!r.ok)throw 0;return r.json();
  }).then(function(j){
    Object.keys(j).forEach(function(k){var n=normalize(j[k]);if(n)S.gen[k]=n});
  }).catch(function(){}).then(function(){S.loading=false;show()});
}

"""+s[b:]
# 5) show(): 타이머 제거
a=s.index("function show(){"); b=s.index("$('prevM').addEventListener")
s=s[:a]+"""function show(){
  var k=keyOf(S.m,S.d);
  var data=dataFor(k);
  renderCover();renderCal();renderScene(data);renderRecords(data);renderNotes(data);renderFoot(data);
}

"""+s[b:]
# 6) 이벤트 핸들러와 시작부
a=s.index("$('prevM').addEventListener"); b=s.index("})();",a)
s=s[:a]+"loadMonth();\n"+s[b:]
# 7) 푸터 문구
a=s.index("  f.textContent=(SEED[keyOf(S.m,S.d)]"); b=s.index("+base;",a)
s=s[:a]+"  f.textContent='이 날의 기억은 널리 알려진 역사 지식과 공개된 자료를 바탕으로 정리했습니다. 자료마다 날짜가 다른 항목은 본문에 적어 두었습니다. '"+s[b:]
rep("S.loading?'기억을 정리하는 중입니다':'이 날의 기억을 기다리고 있습니다'","S.loading?'기억을 불러오는 중입니다':'이 날의 기억은 아직 준비되지 않았습니다'")
rep("'기억이 준비되면 가장 이야기할 만한 장면이 이곳에 실립니다.'","'기억은 매달 초에 한 달 분량을 새로 올립니다.'")
# 8) 날짜 이동 UI 제거
rep(".tools{",".tools{display:none!important}\n.tools-x{")
rep(".st{",".st{pointer-events:none;")
s=s.replace("<title>기억의 날짜</title>","<title>기억의 날짜</title>",1)
if '<meta charset' not in s:
    s=s.replace('<title>','<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<title>',1)

# 홈 화면 아이콘과 매니페스트
s=s.replace('<title>','<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#E5501B">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="기억의 날짜">\n<title>',1)
open('index.html','w',encoding='utf-8').write(s)
