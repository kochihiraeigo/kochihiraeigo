# 英語やるぞ！

英検の単語プリント・文法プリントの音読ページ（Webアプリ）。

- 公開先: https://kochihiraeigo.github.io/kochihiraeigo/
- ホーム画面に追加すると、アプリとして開きます（PWA）。
- 音声は端末の読み上げ機能を使うので、一度開いたあとはオフラインでも動きます。

## ファイル

| ファイル | 中身 |
|---|---|
| `index.html` | アプリのホーム。名前の登録、級のお気に入り（★）|
| `t5 / t4 / t3 / tp2 / t2 .html` | 単語プリントの音読ページ |
| `g5 / g4 / g3 / gp2 / g2 .html` | 文法プリントの音読ページ |
| `manifest.json` | アプリ名・アイコンの設定 |
| `sw.js` | オフライン用（キャッシュ）。更新したら `VERSION` を上げる |
| `icon-*.png` / `apple-touch-icon.png` | アイコン（「英」） |

## 教材を更新したとき

1. `make_gweb.py` / `make_word.py` で音読ページを作り直す
2. `python3 add_pwa.py *.html` を実行（アプリ用のタグとホームボタンを入れ直す／二重にはならない）
3. `sw.js` の `VERSION` を上げる
4. commit して push。数分で公開先に反映されます

## 中学生版（中1〜中3）
- `tc1/tc2/tc3.html` = 単語、`gc1/gc2/gc3.html` = 文法（暗唱例文）。`make_chu.py` が `g5.html` をひな形に生成（データは /home/claude/work の json から）。
- 印刷プリントのQRは `https://kochihiraeigo.github.io/kochihiraeigo/tc3.html#pN` の形式。
