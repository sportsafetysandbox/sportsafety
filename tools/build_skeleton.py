"""Generate placeholder pages, landing pages, the Site Map page and the mkdocs.yml nav.

Run from the repository root:  python tools/build_skeleton.py
Files containing the marker <!-- handwritten --> are never overwritten.
"""
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from structure import NAV, S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
MARK = "<!-- handwritten -->"


def is_page(item):
    return len(item) == 6


def children(item):
    return item[2] if len(item) == 3 else item[1]


def pages_in(items):
    for it in items:
        if is_page(it):
            yield it
        else:
            yield from pages_in(children(it))


def write(path, text):
    full = os.path.join(DOCS, path)
    if os.path.exists(full):
        with open(full, encoding="utf-8") as f:
            if MARK in f.read():
                return False
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def rel(src, dst):
    return os.path.relpath(dst, os.path.dirname(src)).replace(os.sep, "/")


def placeholder(page):
    path, title, purpose, sections, sources, _ = page
    out = ["---", "status: placeholder", "---", "", f"# {title}", "",
           '!!! note "Page in development"',
           "    This page is part of the portal skeleton. The headings below show its planned content.", ""]
    if purpose:
        out += [purpose, ""]
    for s in sections:
        out += [f"## {s}", "", "*Content to come.*", ""]
    if sources:
        out += ["## Based on (planned sources)", ""]
        out += [f"- {S[k]}" for k in sources]
        out.append("")
    return "\n".join(out)


def landing(page, siblings):
    path, title, purpose, *_ = page
    out = [f"# {title}", ""]
    if purpose:
        out += [purpose, ""]
    out += ['<div class="grid cards" markdown>', ""]
    for it in siblings:
        if is_page(it):
            if it[0] == path:
                continue
            p, t, pur = it[0], it[1], it[2]
            out += [f"-   **[{t}]({rel(path, p)})**", ""]
            if pur:
                out += [f"    {pur}", ""]
        else:
            name = it[0]
            first = next(pages_in(children(it)))
            out += [f"-   **[{name}]({rel(path, first[0])})**", ""]
            subs = ", ".join(p[1] for p in pages_in(children(it)))
            out += [f"    {subs}", ""]
    out += ["</div>", ""]
    return "\n".join(out)


def nav_yaml(items):
    out = []
    for it in items:
        if is_page(it):
            out.append({it[1]: it[0]})
        else:
            out.append({it[0]: nav_yaml(children(it))})
    return out


def sitemap_lines(items, depth=0):
    lines = []
    for it in items:
        ind = "    " * depth
        if is_page(it):
            lines.append(f"{ind}- [{it[1]}]({rel('help/site-map.md', it[0])})")
        else:
            lines.append(f"{ind}- **{it[0]}**")
            lines += sitemap_lines(children(it), depth + 1)
    return lines


def walk(items):
    count = 0
    for it in items:
        if is_page(it):
            if it[5] == "placeholder":
                count += write(it[0], placeholder(it))
            elif it[5] == "landing":
                count += write(it[0], landing(it, items))
        else:
            count += walk(children(it))
    return count


def main():
    n = walk(NAV)
    sm = ["# Site Map", "", "Every page on the portal, in menu order.", "",
          "- [Home](../index.md)"] + sitemap_lines(NAV) + [""]
    write("help/site-map.md", "\n".join(sm))

    with open(os.path.join(ROOT, "mkdocs.base.yml"), encoding="utf-8") as f:
        base = f.read()
    nav = [{"Home": "index.md"}] + nav_yaml(NAV)
    with open(os.path.join(ROOT, "mkdocs.yml"), "w", encoding="utf-8") as f:
        f.write("# GENERATED from mkdocs.base.yml + tools/structure.py by tools/build_skeleton.py.\n")
        f.write("# Edit those files, not this one.\n\n")
        f.write(base.rstrip() + "\n\n")
        f.write(yaml.safe_dump({"nav": nav}, sort_keys=False, allow_unicode=True))
    total = len(list(pages_in(NAV))) + 1
    print(f"{total} pages in nav; {n} generated files written")


if __name__ == "__main__":
    main()
