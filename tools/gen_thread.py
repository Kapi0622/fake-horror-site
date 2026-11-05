# 2ch風スレッドページ（2ch/thread.html）を作るスクリプト
#
# 使い方（このフォルダの一つ上で実行）:
#   python3 tools/gen_thread.py
#
# 本文は tools/thread.txt を書き換える。書式:
#   1行目     スレタイ
#   レスの頭  「番号 ：名前：YYYY/MM/DD(曜) hh:mm:ss ID:xxxx」
#   その下    本文（空行はレスの区切りとして扱う）
# 曜日が日付と合っていなければエラーで止まる。
import re, sys, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "thread.txt"
TEMPLATE = ROOT / "tools" / "thread_template.html"
OUT = ROOT / "2ch" / "thread.html"
WD = "月火水木金土日"

HEAD = re.compile(r"^(\d+) ：(.+?)：(\d{4})/(\d\d)/(\d\d)\((.)\) (\d\d:\d\d:\d\d) ID:(\S+)$")

lines = SRC.read_text(encoding="utf-8").splitlines()
title = lines[0].strip()

posts = []
for line in lines[1:]:
    m = HEAD.match(line)
    if m:
        posts.append({"m": m, "body": []})
    elif posts:
        posts[-1]["body"].append(line)

def anchor(text):
    # >>12 や >>30-32 をページ内リンクにする
    return re.sub(r"&gt;&gt;(\d+)(-\d+)?",
                  lambda m: '<a href="#r%s">%s</a>' % (m.group(1), m.group(0)), text)

out = []
for i, p in enumerate(posts, 1):
    num, name, y, mo, d, wd, tm, id_ = p["m"].groups()
    if int(num) != i:
        sys.exit("レス番号が飛んでいます: %s（%d のはず）" % (num, i))
    real = WD[datetime.date(int(y), int(mo), int(d)).weekday()]
    if wd != real:
        sys.exit("曜日が違います: >>%s %s/%s/%s は(%s)" % (num, y, mo, d, real))
    body = p["body"]
    while body and not body[-1].strip():
        body.pop()
    body_html = anchor(" <br> ".join(html.escape(b, quote=False) for b in body))
    out.append('<dt id="r%s">%s ：<font color="#008800"><b>%s</b></font>：%s/%s/%s(%s) %s ID:%s</dt>\n'
               '<dd> %s <br><br></dd>' % (num, num, html.escape(name), y, mo, d, wd, tm, id_, body_html))

page = TEMPLATE.read_text(encoding="utf-8")
page = page.replace("{{TITLE}}", html.escape(title)).replace("{{POSTS}}", "\n".join(out))
OUT.write_text(page, encoding="utf-8")
print("%s: %d レス" % (OUT.relative_to(ROOT), len(posts)))
