#!/usr/bin/env python3
"""Convert a BibTeX file into the JSON consumed by the Hugo theme.

Usage:
    python3 scripts/bib2json.py [publications.bib] [data/publications.json]

No third-party dependencies. The parser handles the subset of BibTeX that
publication lists normally use: @type{key, field = {value} | "value" | number,
...}, nested braces, month macros, `@comment`/`@string`/`@preamble` blocks
(ignored) and `%` line comments outside entries.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Fields used only by the website. They are removed from the BibTeX snippet.
SITE_FIELDS = {
    "category", "abbr", "keywords", "equal", "note", "arxiv", "openreview",
    "code", "slides", "pdf", "project", "video", "poster",
}

# Order of links shown under each paper.
LINK_FIELDS = [
    ("url", "paper"), ("doi", "doi"), ("pdf", "pdf"), ("arxiv", "arxiv"),
    ("openreview", "openreview"), ("code", "code"), ("slides", "slides"),
    ("poster", "poster"), ("video", "video"), ("project", "project"),
]

DEFAULT_CATEGORY = {
    "article": "journal",
    "inproceedings": "conference",
    "conference": "conference",
    "incollection": "conference",
    "book": "other",
    "phdthesis": "other",
    "mastersthesis": "other",
}

LATEX_ACCENTS = {
    '"': {"a": "ä", "o": "ö", "u": "ü", "e": "ë", "i": "ï", "A": "Ä", "O": "Ö", "U": "Ü"},
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "c": "ć", "n": "ń", "s": "ś", "z": "ź",
          "E": "É", "A": "Á"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"},
    "~": {"n": "ñ", "a": "ã", "o": "õ"},
    "c": {"c": "ç", "C": "Ç"},
    "v": {"c": "č", "s": "š", "z": "ž", "r": "ř", "e": "ě", "C": "Č", "S": "Š", "Z": "Ž"},
    "k": {"a": "ą", "e": "ę"},
    "l": {"": "ł"},
}


class BibParseError(ValueError):
    pass


def _skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i].isspace():
        i += 1
    return i


def _read_braced(s: str, i: int) -> tuple[str, int]:
    """s[i] == '{' (or '('). Return (inner text, index after the closing char)."""
    open_ch = s[i]
    close_ch = "}" if open_ch == "{" else ")"
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == open_ch or (open_ch == "(" and c == "{"):
            depth += 1
        elif c == close_ch or (open_ch == "(" and c == "}"):
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise BibParseError(f"unbalanced braces starting at offset {i}")


def _read_quoted(s: str, i: int) -> tuple[str, int]:
    j = i + 1
    depth = 0
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == '"' and depth == 0:
            return s[i + 1:j], j + 1
        j += 1
    raise BibParseError(f"unterminated string at offset {i}")


def _parse_fields(body: str) -> tuple[str, dict[str, str], list[tuple[str, str]]]:
    key, _, rest = body.partition(",")
    fields: dict[str, str] = {}
    raw: list[tuple[str, str]] = []
    i = 0
    while True:
        i = _skip_ws(rest, i)
        if i >= len(rest):
            break
        if rest[i] == ",":
            i += 1
            continue
        m = re.match(r"([A-Za-z][\w\-:.]*)\s*=\s*", rest[i:])
        if not m:
            raise BibParseError(f"cannot parse field near: {rest[i:i + 40]!r}")
        name = m.group(1).lower()
        i += m.end()
        parts = []
        raw_parts = []
        while True:
            i = _skip_ws(rest, i)
            if rest[i] == "{":
                val, i = _read_braced(rest, i)
                parts.append(val)
                raw_parts.append("{" + val + "}")
            elif rest[i] == '"':
                val, i = _read_quoted(rest, i)
                parts.append(val)
                raw_parts.append('"' + val + '"')
            else:
                m2 = re.match(r"[^,#\s}]+", rest[i:])
                if not m2:
                    raise BibParseError(f"bad value for {name}")
                tok = m2.group(0)
                i += m2.end()
                parts.append(str(MONTHS.get(tok.lower()[:3], tok)) if name == "month" else tok)
                raw_parts.append(tok)
            i = _skip_ws(rest, i)
            if i < len(rest) and rest[i] == "#":
                i += 1
                continue
            break
        fields[name] = "".join(parts).strip()
        raw.append((name, " # ".join(raw_parts)))
    return key.strip(), fields, raw


def parse_bibtex(text: str) -> list[dict]:
    entries = []
    i = 0
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        # ignore '@' inside % comments
        line_start = text.rfind("\n", 0, at) + 1
        if "%" in text[line_start:at]:
            i = text.find("\n", at) if text.find("\n", at) >= 0 else len(text)
            continue
        m = re.match(r"@\s*(\w+)\s*([{(])", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        brace_at = at + m.end() - 1
        body, i = _read_braced(text, brace_at)
        if etype in {"comment", "string", "preamble"}:
            continue
        key, fields, raw = _parse_fields(body)
        entries.append({"type": etype, "key": key, "fields": fields, "raw": raw, "pos": len(entries)})
    return entries


def latex_to_text(s: str) -> str:
    """Strip BibTeX braces and simple LaTeX accents, keeping $...$ math intact."""
    out = []
    for k, chunk in enumerate(re.split(r"(\$[^$]*\$)", s)):
        if k % 2 == 1:
            out.append(chunk)
            continue

        def accent(m: re.Match) -> str:
            cmd, ch = m.group(1), m.group(2) or ""
            return LATEX_ACCENTS.get(cmd, {}).get(ch, ch)

        chunk = re.sub(r"\{?\\([\"'`^~ckvl])\s*\{?([A-Za-z]?)\}?\}?", accent, chunk)
        chunk = chunk.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
        chunk = chunk.replace("---", "—").replace("--", "–").replace("~", " ")
        chunk = chunk.replace("{", "").replace("}", "")
        out.append(chunk)
    return re.sub(r"\s+", " ", "".join(out)).strip()


def format_author(name: str) -> str:
    name = latex_to_text(name.strip())
    if name.lower() == "others":
        return "others"
    if "," in name:
        parts = [p.strip() for p in name.split(",")]
        if len(parts) == 2:
            return f"{parts[1]} {parts[0]}".strip()
        if len(parts) == 3:  # von Last, Jr, First
            return f"{parts[2]} {parts[0]}, {parts[1]}".strip()
    return name


def split_authors(s: str) -> list[str]:
    # split on " and " at brace depth 0
    out, depth, cur, i = [], 0, [], 0
    while i < len(s):
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0 and re.match(r"\s+and\s+", s[i:], flags=re.I) and (i == 0 or s[i].isspace()):
            m = re.match(r"\s+and\s+", s[i:], flags=re.I)
            out.append("".join(cur))
            cur = []
            i += m.end()
            continue
        cur.append(c)
        i += 1
    if cur:
        out.append("".join(cur))
    return [a for a in (x.strip() for x in out) if a]


def entry_to_json(e: dict) -> dict:
    f = e["fields"]
    category = f.get("category", "").lower() or DEFAULT_CATEGORY.get(e["type"], "preprint")
    keywords = [k.strip().lower() for k in re.split(r"[,;]", f.get("keywords", "")) if k.strip()]
    equal = {int(x) for x in re.findall(r"\d+", f.get("equal", ""))}

    authors = []
    for idx, a in enumerate(split_authors(f.get("author", "")), start=1):
        formatted = format_author(a)
        if formatted == "others":
            authors.append({"name": "et al.", "equal": False})
        else:
            authors.append({"name": formatted, "equal": idx in equal})

    venue = f.get("journal") or f.get("booktitle") or ""
    if not venue and f.get("archiveprefix", "").lower() == "arxiv":
        venue = "arXiv"

    links = []
    for field, label in LINK_FIELDS:
        v = f.get(field)
        if not v:
            continue
        if field == "doi" and not v.startswith("http"):
            v = "https://doi.org/" + v
        if field == "arxiv" and not v.startswith("http"):
            v = "https://arxiv.org/abs/" + v
        links.append({"label": label, "url": v})
    if f.get("eprint") and f.get("archiveprefix", "").lower() == "arxiv" and not f.get("arxiv"):
        links.append({"label": "arxiv", "url": "https://arxiv.org/abs/" + f["eprint"]})

    year = f.get("year", "")
    try:
        month = int(f.get("month", "0"))
    except ValueError:
        month = MONTHS.get(f.get("month", "").lower()[:3], 0)

    raw_lines = [f"@{e['type']}{{{e['key']},"]
    for name, val in e["raw"]:
        if name not in SITE_FIELDS:
            raw_lines.append(f"  {name} = {val},")
    raw_lines.append("}")

    return {
        "key": e["key"],
        "type": e["type"],
        "category": category,
        "selected": "selected" in keywords,
        "title": latex_to_text(f.get("title", "")),
        "authors": authors,
        "venue": latex_to_text(venue),
        "abbr": latex_to_text(f.get("abbr", "")),
        "note": latex_to_text(f.get("note", "")),
        "year": year,
        "month": month,
        "links": links,
        "bibtex": "\n".join(raw_lines),
        "_pos": e["pos"],
    }


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    src = Path(argv[1]) if len(argv) > 1 else root / "publications.bib"
    dst = Path(argv[2]) if len(argv) > 2 else root / "data" / "publications.json"
    entries = [entry_to_json(e) for e in parse_bibtex(src.read_text(encoding="utf-8"))]
    # newest first; keep file order within the same year/month
    entries.sort(key=lambda p: (-int(p["year"] or 0), -p["month"], p["_pos"]))
    for p in entries:
        del p["_pos"]
    dst.write_text(json.dumps(entries, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} entries to {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
