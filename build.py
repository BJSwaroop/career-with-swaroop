#!/usr/bin/env python3
"""
Career with Swaroop - landing page builder.

Usage:  python3 build.py
Output: dist/  (index.html + one page per keyword)

To add a new opportunity: add an entry to data.json, re-run this script,
re-upload dist/. Nothing else to change.
"""

import json
import os
from datetime import date, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

CSS = """
:root{color-scheme:light;--ink:#101418;--muted:#5b6672;--line:#e4e8ec;--bg:#ffffff;
--soft:#f5f7f9;--accent:#1a56db;--accent-ink:#ffffff;--wa:#25d366;--wa-ink:#04301a;
--ok:#0f7b41;--warn:#8a4b00;--warn-bg:#fff4e5}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
-webkit-font-smoothing:antialiased;padding:0 0 56px}
.wrap{max-width:520px;margin:0 auto;padding:0 20px}
header{padding:22px 0 6px}
.brand{display:flex;align-items:center;gap:9px;font-weight:650;font-size:14px;letter-spacing:.01em}
.dot{width:9px;height:9px;border-radius:50%;background:var(--accent);flex:none}
.brand span{color:var(--muted);font-weight:500}
h1{font-size:29px;line-height:1.18;letter-spacing:-.02em;margin:18px 0 8px;font-weight:700}
.sub{color:var(--muted);font-size:17px;margin-bottom:18px}
.verified{display:inline-flex;align-items:center;gap:6px;background:#e9f6ef;color:var(--ok);
border-radius:999px;padding:5px 11px;font-size:12.5px;font-weight:600;margin-bottom:6px}
.facts{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:20px 0}
.fact{display:flex;justify-content:space-between;gap:14px;padding:12px 15px;border-bottom:1px solid var(--line)}
.fact:last-child{border-bottom:0}
.fact .k{color:var(--muted);font-size:14.5px}
.fact .v{font-weight:650;text-align:right;font-size:14.5px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
font-weight:700;margin:26px 0 10px}
a.btn{display:block;text-decoration:none;color:var(--ink);background:var(--soft);
border:1px solid var(--line);border-radius:13px;padding:14px 16px;margin-bottom:10px;
transition:transform .06s ease}
a.btn:active{transform:scale(.985)}
a.btn .lab{font-weight:650;font-size:16px;display:flex;justify-content:space-between;align-items:center;gap:10px}
a.btn .note{color:var(--muted);font-size:13.5px;margin-top:2px}
a.btn .arrow{color:var(--muted);font-weight:400;flex:none}
a.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
a.btn.primary .note,a.btn.primary .arrow{color:rgba(255,255,255,.82)}
a.wa{display:block;text-decoration:none;background:var(--wa);color:var(--wa-ink);
border-radius:13px;padding:15px 16px;margin-top:8px}
a.wa .lab{font-weight:700;font-size:16.5px}
a.wa .note{font-size:13.5px;opacity:.82;margin-top:2px}
ul.pts{list-style:none;border:1px solid var(--line);border-radius:14px;padding:6px 0}
ul.pts li{padding:10px 15px 10px 34px;position:relative;font-size:15px;border-bottom:1px solid var(--line)}
ul.pts li:last-child{border-bottom:0}
ul.pts li:before{content:"";position:absolute;left:15px;top:18px;width:6px;height:6px;
border-radius:50%;background:var(--accent)}
.foot{color:var(--muted);font-size:14px;margin-top:16px}
.expiry{background:var(--warn-bg);color:var(--warn);border-radius:12px;padding:12px 15px;
font-size:14px;font-weight:600;margin:18px 0}
.gone{border:1px solid var(--line);border-radius:14px;padding:26px 20px;text-align:center;margin:22px 0}
.gone h3{font-size:19px;margin-bottom:8px}
.gone p{color:var(--muted);font-size:15px}
.disc{border-top:1px solid var(--line);margin-top:34px;padding-top:16px;
color:var(--muted);font-size:13px;line-height:1.5}
.idx{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);
border-radius:13px;padding:15px 16px;margin-bottom:10px}
.idx .lab{font-weight:650;font-size:16.5px}
.idx .note{color:var(--muted);font-size:14px;margin-top:3px}
"""

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{canonical}">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<style>{css}</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="brand"><i class="dot"></i>Career with Swaroop <span>{handle}</span></div>
</header>
{body}
<p class="disc">{disclaimer}</p>
</div>
</body>
</html>
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def fmt_date(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d %B %Y")


def render_links(groups):
    out = []
    for g in groups:
        out.append('<h2>%s</h2>' % esc(g["heading"]))
        for l in g["links"]:
            cls = "btn primary" if l.get("primary") else "btn"
            out.append(
                '<a class="%s" href="%s" target="_blank" rel="noopener noreferrer">'
                '<span class="lab">%s<span class="arrow">&rarr;</span></span>'
                '<span class="note">%s</span></a>'
                % (cls, esc(l["url"]), esc(l["label"]), esc(l.get("note", "")))
            )
    return "\n".join(out)


def render_page(site, op, today):
    expired = False
    if op.get("expiresOn"):
        expired = today > datetime.strptime(op["expiresOn"], "%Y-%m-%d").date()

    parts = ['<h1>%s</h1>' % esc(op["title"]),
             '<p class="sub">%s</p>' % esc(op["subtitle"])]

    if expired:
        parts.append(
            '<div class="gone"><h3>Ee link expire ayindi</h3>'
            '<p>Ee page %s varaku matrame open ga undedi. '
            'Kotha opportunities kosam community lo join avvandi.</p></div>'
            % esc(fmt_date(op["expiresOn"]))
        )
        parts.append(
            '<a class="wa" href="%s" target="_blank" rel="noopener noreferrer">'
            '<span class="lab">%s</span><span class="note">%s</span></a>'
            % (esc(site["whatsapp"]), esc(site["whatsappLabel"]), esc(site["whatsappNote"]))
        )
    else:
        parts.append('<span class="verified">&#10003; Verified %s</span>'
                     % esc(fmt_date(site["verifiedOn"])))

        if op.get("expiresOn"):
            parts.append('<div class="expiry">%s</div>' % esc(op["expiryNote"]))

        if op.get("facts"):
            rows = "".join(
                '<div class="fact"><span class="k">%s</span><span class="v">%s</span></div>'
                % (esc(f["k"]), esc(f["v"])) for f in op["facts"]
            )
            parts.append('<div class="facts">%s</div>' % rows)

        parts.append(render_links(op["linkGroups"]))

        if op.get("noc"):
            parts.append('<h2>%s</h2>' % esc(op["noc"]["heading"]))
            parts.append('<ul class="pts">%s</ul>' % "".join(
                "<li>%s</li>" % esc(p) for p in op["noc"]["points"]))

        if op.get("footNote"):
            parts.append('<p class="foot">%s</p>' % esc(op["footNote"]))

        parts.append('<h2>Inka opportunities</h2>')
        parts.append(
            '<a class="wa" href="%s" target="_blank" rel="noopener noreferrer">'
            '<span class="lab">%s</span><span class="note">%s</span></a>'
            % (esc(site["whatsapp"]), esc(site["whatsappLabel"]), esc(site["whatsappNote"]))
        )

    return SHELL.format(
        canonical=esc(site.get("baseUrl", "").rstrip("/") + "/" + op["slug"] + ".html"),
        title=esc(op["title"] + " | Career with Swaroop"),
        desc=esc(op["subtitle"]),
        handle=esc(site["handle"]),
        css=CSS,
        body="\n".join(parts),
        disclaimer=esc(site["disclaimer"]),
    )


def render_index(site, ops, today):
    parts = ['<h1>Opportunities</h1>',
             '<p class="sub">Anni official government links. Verified %s.</p>'
             % esc(fmt_date(site["verifiedOn"]))]
    for op in ops:
        if op.get("expiresOn") and today > datetime.strptime(op["expiresOn"], "%Y-%m-%d").date():
            continue
        parts.append(
            '<a class="idx" href="%s.html"><span class="lab">%s</span>'
            '<span class="note">%s</span></a>'
            % (esc(op["slug"]), esc(op["title"]), esc(op["subtitle"]))
        )
    parts.append('<h2>Community</h2>')
    parts.append(
        '<a class="wa" href="%s" target="_blank" rel="noopener noreferrer">'
        '<span class="lab">%s</span><span class="note">%s</span></a>'
        % (esc(site["whatsapp"]), esc(site["whatsappLabel"]), esc(site["whatsappNote"]))
    )
    return SHELL.format(
        canonical=esc(site.get("baseUrl", "").rstrip("/") + "/"),
        title="Career with Swaroop | Opportunities",
        desc=esc("Verified government internships, scholarships and free courses."),
        handle=esc(site["handle"]),
        css=CSS,
        body="\n".join(parts),
        disclaimer=esc(site["disclaimer"]),
    )


def main():
    with open(os.path.join(ROOT, "data.json"), encoding="utf-8") as f:
        data = json.load(f)

    site, ops = data["site"], data["opportunities"]
    today = date.today()

    os.makedirs(DIST, exist_ok=True)

    for op in ops:
        path = os.path.join(DIST, op["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_page(site, op, today))
        print("  built  /%s.html   (keyword: %s)" % (op["slug"], op["keyword"]))

    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index(site, ops, today))
    print("  built  /index.html")
    print("\nDone. %d pages in dist/" % (len(ops) + 1))


if __name__ == "__main__":
    main()
