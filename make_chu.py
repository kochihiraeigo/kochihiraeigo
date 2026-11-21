# -*- coding: utf-8 -*-
"""中1〜中3の音声ページ(tc1-3 単語 / gc1-3 文法)を g5.html をひな形に生成する"""
import json,re,sys,html
sys.path.insert(0,'/home/claude/work'); sys.path.insert(0,'/home/claude')
from pool import load
W='/home/claude/work/'
tpl=open('g5.html',encoding='utf-8').read()
head=tpl[:tpl.find('<body')]
tail=tpl[tpl.find('const RATE'):]
tail=tail[:tail.find('</script>')]
k=tpl.rfind('<style'); late=tpl[k:tpl.find('</style>',k)+8]
extra=late+"<style>.page{height:auto!important;min-height:297mm;padding-bottom:22mm}.foot{position:static!important;margin-top:10px}.gtoc .tch{font-size:11pt}</style>"
head=head.replace('</head>',extra+'</head>')
EMO=re.compile('[\U0001F000-\U0001FFFF☀-➿️‍]')
def strip(s): return EMO.sub('',s).strip()
E=html.escape
def build(fname,kind,title,chlabel,pages):
    n=len(pages); labels=[f"{i+1:02d}" for i in range(n)]
    tabs=''.join(f'<button class="gtab" data-i="{i}">{l}</button>' for i,l in enumerate(labels))
    gbar=f'<div class="gbar"><a class="yzhome" href="index.html" title="英語やるぞ！ホーム"><b>英</b>ホーム</a><button class="gbtn ghost" id="tocbtn">☰ 目次</button><button class="gbtn" id="from0">▶ この回をはじめから</button><button class="gbtn ghost" id="pz" disabled>⏸ 一時停止</button><span class="gnow" id="gnow"></span><span class="ghint">{"単語" if kind=="t" else "文"}をタップすると、それだけ流れます</span><span class="gtabs">{tabs}</span></div>'
    rows=''.join(f'<button class="tocrow" data-i="{i}"><span class="tnum">{labels[i]}</span><span class="tbody"><div class="tch">{E(p["ch"])}</div><div class="ttl">{E(p["title"])}</div></span><span class="tgo">▶</span></button>' for i,p in enumerate(pages))
    toc=f'<div class="gtoc" id="toc"><div class="toch">{E(title)}</div><div class="tocsub">やりたい単元をえらんでね。えらんだ単元を3回くりかえしたら、自動でつぎの単元にすすみます。</div><button class="tocall" id="playall">▶ はじめから　ぜんぶ流す</button><div class="toclist">{rows}</div><div class="tocnote">とちゅうでやめたいときは「⏸ 一時停止」。目次にもどるときは左上の「☰ 目次」をおしてください。</div></div>'
    body=''
    for i,p in enumerate(pages):
        its=''.join(f'<div class="exrow"><span class="exnum">{k+1}</span><span class="exen"><span class="en">{E(en)}</span></span><span class="exlead"></span><span class="exja">{E(jp)}</span></div>' for k,(jp,en) in enumerate(p['items']))
        body+=f'<div class="gwrap" data-i="{i}"><div class="gscale"><section class="page"><div class="hdr"><div class="hdr-left"><span class="bignum">{labels[i]}</span><div><div class="chlabel">{E(chlabel)}</div><div class="htitle">{E(p["title"])}</div></div></div></div><div class="hdr-rule"></div>{its}<div class="foot">{E(title)}　{labels[i]}　{E(p["title"])}</div></section></div></div>'
    lab=json.dumps(labels)
    t=re.sub(r'LABELS=\[[^\]]*\]','LABELS='+lab,tail)
    out=head+'<body>'+gbar+toc+body+'<script>'+t+'</script><script>if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}</script></body></html>'
    open(fname,'w',encoding='utf-8').write(out); print(fname,n,len(out)//1024,'KB')
# ---- words
def wpages(fn):
    return json.load(open(W+fn))
w1=[]
for i,p in enumerate(wpages('w1_pages.json')):
    items=[(jp,en) for r in p for jp,en in r['pairs']]
    w1.append({'ch':'中1','title':'・'.join(dict.fromkeys(r['label'] for r in p))+f'（{len(items)}語）','items':[(strip(a),b) for a,b in items]})
w2=[]
for p in wpages('w2.json'):
    items=[]
    for it in p['items']:
        if it[0]=='w': items.append((strip(it[1]),it[2]))
        else: items.append((strip(it[1]),f'{it[2]}, {it[3]}, {it[4]}'))
    w2.append({'ch':'中2','title':f"{p['label']}（{len(items)}語）",'items':items})
w3=[{'ch':'中3','title':p['label'],'items':[tuple(x) for x in p['items']]} for p in wpages('w3_pages.json')]
build('tc1.html','t','中1　単語プリント','中1',w1)
build('tc2.html','t','中2　単語プリント','中2',w2)
build('tc3.html','t','中3　単語プリント','中3',w3)
# ---- grammar
P=load(); g1=[];g2=[];g3=[]
by={}
for g,u,sub,jp,en in P: by.setdefault((g,u),[]).append((jp,en))
for (g,u),v in by.items():
    pass
# 中1: units in order, chunks of <=10
seen=[]
for g,u,_,_,_ in P:
    if g=='中1' and u not in seen: seen.append(u)
for u in seen:
    v=by[('中1',u)]; ch=[v[i:i+10] for i in range(0,len(v),10)]
    for j,c in enumerate(ch): g1.append({'ch':'中1','title':u+(f'（{j+1}/{len(ch)}）' if len(ch)>1 else ''),'items':c})
for p in json.load(open(W+'s2.json')):
    g2.append({'ch':'中2','title':p['label'],'items':[(r[2],r[3]) for r in p['rows']]})
idx=json.load(open('/home/claude/chu3_index.json'))
flat=[(jp,en) for g,u,_,jp,en in P if g=='中3']
pos=0
for i,l,n in idx:
    g3.append({'ch':'中3','title':l.lstrip('◆'),'items':flat[pos:pos+n]}); pos+=n
assert pos==len(flat),(pos,len(flat))
build('gc1.html','g','中1　文法プリント（暗唱例文）','中1',g1)
build('gc2.html','g','中2　文法プリント（暗唱例文）','中2',g2)
build('gc3.html','g','中3　文法プリント（暗唱例文）','中3',g3)
