# -*- coding: utf-8 -*-
"""音読ページをアプリ「英語やるぞ！」の一部にする。
   ・ホーム画面に追加できるようにする（manifest / アイコン）
   ・オフラインでも開けるようにする（service worker の登録）
   ・左上に「英 ホーム」ボタンを足す
   何度実行しても二重にならない。
   使い方: python3 add_pwa.py /home/claude/kochihiraeigo/*.html
"""
import re, sys, pathlib

MARK = "<!--yaruzo-pwa-->"

HEAD = (MARK +
        '<link rel="manifest" href="manifest.json">'
        '<meta name="theme-color" content="#D1095A">'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">'
        '<meta name="apple-mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-title" content="英語やるぞ！">'
        '<style>.yzhome{display:inline-flex;align-items:center;gap:5px;'
        'text-decoration:none;color:#fff;background:rgba(255,255,255,.16);'
        'border:1px solid rgba(255,255,255,.42);border-radius:8px;'
        'padding:4px 10px 5px;font-weight:700;font-size:13px;margin-right:4px;}'
        '.yzhome b{font-size:15px;line-height:1;}</style>')

HOME = ('<a class="yzhome" href="index.html" title="英語やるぞ！ホーム">'
        '<b>英</b>ホーム</a>')

FOOT = ('<script>if("serviceWorker" in navigator){window.addEventListener("load",'
        'function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}'
        '</script>')


def patch(p):
    t = p.read_text(encoding="utf-8")
    if MARK in t:
        return "すでに対応ずみ"
    if "<head>" not in t:
        return "head が見つからない"
    t = t.replace("<head>", "<head>" + HEAD, 1)
    m = re.search(r'<div class="gbar">', t)
    if m:
        t = t[:m.end()] + HOME + t[m.end():]
    t = t.replace("</body>", FOOT + "</body>", 1)
    p.write_text(t, encoding="utf-8")
    return "対応しました" + ("" if m else "（ホームボタンは入れられず）")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        p = pathlib.Path(a)
        if p.name == "index.html":
            continue
        print(f"  {p.name}: {patch(p)}")
