"""Shared, conservative extraction of protected manuscript fields.

These recognizers cover common text/LaTeX forms. They are not a parser for all
citation styles, units, or mathematics, and do not establish semantic equivalence.
"""

from __future__ import annotations

import re
from collections import Counter
from decimal import Decimal, localcontext


NUMBER_PATTERN = r"[-+−–—]?(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)(?:%|[eE][-+−]?\d+)?"
NUMBER_RE = re.compile(rf"(?<![A-Za-z]){NUMBER_PATTERN}(?![A-Za-z])")
LATEX_CITATION_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}")
PANDOC_CITATION_RE = re.compile(r"\[([^\]]*@[A-Za-z0-9_:.\-/]+[^\]]*)\]")
PANDOC_KEY_RE = re.compile(r"@([A-Za-z0-9_:.\-/]+)")
AUTHOR = r"(?:[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'\-]+|[\u3400-\u9fff]{2,6})"
AUTHORS = rf"{AUTHOR}(?:\s+(?:et\s+al\.?|(?:and|&)\s+{AUTHOR})|等)?"
YEAR = r"(?:18|19|20)\d{2}[a-z]?"
AUTHOR_YEAR_RE = re.compile(
    rf"(?<!\w){AUTHORS}\s*[（(]\s*{YEAR}\s*[)）]"
    rf"|[（(]\s*{AUTHORS}\s*[,，]\s*{YEAR}(?:\s*;\s*{AUTHORS}\s*,\s*{YEAR})*\s*[)）]"
)
# Quantity scales and common economic/measurement units. New units need both
# changed-unit and safe-copyedit cases; unknown units remain outside this screen.
UNIT = (
    r"(?:trillion|billion|million|thousand|hundred|percentage\s+points?|"
    r"percent|basis\s+points?|dollars?|euros?|yuan|USD|CNY|RMB|"
    r"years?|months?|days?|hours?|minutes?|seconds?|kg|km|cm|mm|"
    r"亿元|万元|亿|万|千|百|元|年|月|天|小时|分钟|秒|百分点|个基点)(?![A-Za-z])"
)
QUANTITY_RE = re.compile(
    rf"(?<![A-Za-z0-9_])(?:[$€£¥]\s*)?{NUMBER_PATTERN}\s*{UNIT}(?:\s*{UNIT})*"
    rf"|[$€£¥]\s*{NUMBER_PATTERN}", re.IGNORECASE
)
EQUATION_RE = re.compile(
    r"\\begin\{(?P<env>equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|displaymath|math)\}"
    r".*?\\end\{(?P=env)\}"
    r"|\\\[.*?\\\]|\\\(.*?\\\)"
    r"|(?<!\\)\$\$.*?(?<!\\)\$\$"
    r"|(?<![\\$])\$(?!\$)[^\n$]+(?<!\\)\$(?!\$)", re.DOTALL
)
PVALUE_RE = re.compile(rf"\bp\s*(?:[<>=≤≥]|\\(?:leq?|geq?))\s*{NUMBER_PATTERN}", re.IGNORECASE)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eq)?ref\{([^}]+)\}")


def normalize_number(value: str) -> str:
    return value.translate(str.maketrans({"−": "-", "–": "-", "—": "-", ",": ""}))


def numeric_tokens(text: str) -> list[str]:
    return [normalize_number(match.group(0)) for match in NUMBER_RE.finditer(text)]


def citation_spans(text: str) -> list[tuple[int, int, list[str]]]:
    spans = []
    for pattern, kind in ((LATEX_CITATION_RE, "latex"), (PANDOC_CITATION_RE, "pandoc"), (AUTHOR_YEAR_RE, "author-year")):
        for match in pattern.finditer(text):
            if kind == "latex":
                keys = [key.strip() for key in match.group(1).split(",") if key.strip()]
            elif kind == "pandoc":
                keys = PANDOC_KEY_RE.findall(match.group(1))
            else:
                keys = ["author-year:" + re.sub(r"\s+", " ", match.group(0)).strip()]
            if not any(match.start() < end and match.end() > start for start, end, _ in spans):
                spans.append((match.start(), match.end(), keys))
    return sorted(spans)


def citation_keys(text: str) -> list[str]:
    return [key for _, _, keys in citation_spans(text) for key in keys]


def mask_citations(text: str, replacement: str = " ") -> str:
    for start, end, _ in reversed(citation_spans(text)):
        text = text[:start] + replacement + text[end:]
    return text


def quantity_tokens(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", normalize_number(match.group(0))).strip().lower() for match in QUANTITY_RE.finditer(text)]


def equation_tokens(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", match.group(0)).strip() for match in EQUATION_RE.finditer(text)]


def protected_counts(text: str, variables: list[str]) -> dict[str, Counter[str]]:
    return {
        "numbers": Counter(numeric_tokens(text)),
        "citations": Counter(citation_keys(text)),
        "variables": Counter({variable: len(re.findall(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", text)) for variable in variables}),
        "quantities": Counter(quantity_tokens(text)),
        "equations": Counter(equation_tokens(text)),
        "pvalue_relations": Counter(re.sub(r"\s+", "", normalize_number(match.group(0))).lower() for match in PVALUE_RE.finditer(text)),
        "latex_labels": Counter(LABEL_RE.findall(text)),
        "latex_refs": Counter(REF_RE.findall(text)),
    }


# Opt-in numeric support for translation, deliberately separate from strict patch
# protection. Only CNY amounts and percent/percentage-point units are normalized.
# No currency conversion, unnamed scales, citation translation, or semantic proof.
ECON_NUMBER = r"[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)"
ECON_SCALE = r"billion|million|thousand|亿|万|千"
ECON_QUANTITY_RE = re.compile(
    rf"(?<![A-Za-z0-9_.])(?:"
    rf"(?P<prefix>CNY|RMB|人民币)\s*(?P<pnum>{ECON_NUMBER})\s*(?P<pscale>{ECON_SCALE})?\s*(?:元|yuan\b)?"
    rf"|(?P<snum>{ECON_NUMBER})\s*(?P<sscale>{ECON_SCALE})?\s*(?P<suffix>元|yuan\b)"
    rf"|(?P<rnum>{ECON_NUMBER})\s*(?P<rate>percentage\s+points?|percent(?:age)?|basis\s+points?|个百分点|百分点|个基点|基点|%)"
    rf")(?![A-Za-z0-9_]|[.]\d|\s*(?:{ECON_SCALE}|元|yuan\b|dollars?\b|euros?\b|USD\b|EUR\b|GBP\b|[$€£]))",
    re.IGNORECASE,
)
ECON_SCALES = {"": 1, "thousand": 1000, "千": 1000, "万": 10000,
               "million": 1000000, "亿": 100000000, "billion": 1000000000}


def economic_numeric_inventory(text: str) -> tuple[Counter[str], list[dict[str, str]]]:
    """Return a limited quantity inventory and visible equivalence records.

    元/yuan denotes CNY only in an explicitly established mainland/RMB context;
    callers must not use this opt-in check for an ambiguous currency manuscript.
    Unconverted numeric/unit forms retain their strict spelling.
    """
    inventory: Counter[str] = Counter()
    records = []
    remaining = []
    previous = 0
    excluded = [(m.start(), m.end()) for m in EQUATION_RE.finditer(text)]
    excluded += [(start, end) for start, end, _ in citation_spans(text)]
    for match in ECON_QUANTITY_RE.finditer(text):
        if any(match.start() < end and match.end() > start for start, end in excluded):
            continue
        number = match["pnum"] or match["snum"] or match["rnum"]
        scale = (match["pscale"] or match["sscale"] or "").lower()
        unit = (match["rate"] or "").lower()
        is_point = "point" in unit or "百分点" in unit or "基点" in unit
        kind = "percentage-point" if is_point else "percent" if unit else "CNY"
        factor = Decimal("0.01") if "basis" in unit or "基点" in unit else Decimal(ECON_SCALES[scale])
        with localcontext() as context:
            context.prec = max(28, len(number) + 16)
            value = (Decimal(normalize_number(number)) * factor).normalize()
        token = kind + ":" + str(value)
        inventory[token] += 1
        records.append({"text": match.group(0).strip(), "equivalent": token})
        remaining.extend([text[previous:match.start()], " "])
        previous = match.end()
    remaining.append(text[previous:])
    remainder = "".join(remaining)
    inventory.update("number:" + value for value in numeric_tokens(remainder))
    inventory.update("unconverted-unit:" + value for value in quantity_tokens(remainder))
    return inventory, records
