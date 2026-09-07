#!/usr/bin/env python3
"""Detect a small, conservative set of method-language overclaims.

This is a writing gate, not a causal-inference engine.  It flags phrases that
are incompatible with the v3 method-safety red lines and leaves the actual
revision decision to the author.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PATTERNS: tuple[dict[str, Any], ...] = (
    {
        "code": "event-study-proves-parallel-trends",
        "method": "event-study",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:event[- ]study|event[- ]time plot|pre[- ]trend plot)\b[^.\n]{0,120}?"
            r"\b(?:prove|proves|proved|demonstrate|demonstrates|establish|establishes|confirm|confirms)\b"
            r"[^.\n]{0,60}?\bparallel trends?\b",
            re.IGNORECASE,
        ),
        "recommendation": "Describe pre-trend evidence as a diagnostic or consistency check; do not call it proof of parallel trends.",
    },
    {
        "code": "event-study-proves-parallel-trends-zh",
        "method": "event-study",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"事件研究[^。\n]{0,100}?(?:证明|证实|验证)[^。\n]{0,40}?平行趋势", re.IGNORECASE),
        "recommendation": "将事件研究表述为对趋势一致性的诊断证据，并说明剩余假设，不要写成证明平行趋势。",
    },
    {
        "code": "matching-solves-endogeneity",
        "method": "matching",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:psm|propensity[- ]score matching|matching|matched sample)\b[^.\n]{0,100}?"
            r"\b(?:solve|solves|solved|eliminate|eliminates|remove|removes|cure|cures|address|addresses)\b"
            r"[^.\n]{0,45}?\bendogeneity\b",
            re.IGNORECASE,
        ),
        "recommendation": "State which observables are balanced and which unobserved-confounding threats remain; matching alone does not solve endogeneity.",
    },
    {
        "code": "controls-or-heckman-solves-endogeneity",
        "method": "controls-or-heckman",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:control variables?|fixed effects?|heckman(?: correction)?)\b[^.\n]{0,100}?"
            r"\b(?:solve|solves|solved|eliminate|eliminates|remove|removes|cure|cures|address|addresses)\b"
            r"[^.\n]{0,45}?\bendogeneity\b",
            re.IGNORECASE,
        ),
        "recommendation": "Explain the identifying variation and residual confounding; controls or a Heckman correction are not automatic cures for endogeneity.",
    },
    {
        "code": "matching-solves-endogeneity-zh",
        "method": "matching-or-controls",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(
            r"(?:倾向得分匹配|PSM|匹配方法|匹配样本|控制变量|固定效应|Heckman)[^。\n]{0,80}?"
            r"(?:解决|消除|克服|完全处理|排除)[^。\n]{0,25}?内生性",
            re.IGNORECASE,
        ),
        "recommendation": "说明匹配或控制变量实际平衡了什么，以及未观测混淆仍可能存在；不要写成解决内生性。",
    },
    {
        "code": "mediation-proves-causal-mechanism",
        "method": "mediation",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(
            r"\b(?:mediation|mediator|mediation analysis)\b[^.\n]{0,100}?"
            r"\b(?:prove|proves|proved|demonstrate|demonstrates|establish|establishes|confirm|confirms)\b"
            r"[^.\n]{0,55}?\b(?:causal mechanism|causality)\b",
            re.IGNORECASE,
        ),
        "recommendation": "Separate descriptive mediation from causal mediation and state the mediator and identification assumptions.",
    },
    {
        "code": "mediation-proves-causal-mechanism-zh",
        "method": "mediation",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:中介分析|中介效应|中介变量)[^。\n]{0,80}?(?:证明|证实|验证)[^。\n]{0,35}?(?:因果机制|因果关系)", re.IGNORECASE),
        "recommendation": "区分描述性中介与因果中介，并明确中介变量的时序、外生性和识别假设。",
    },
    {
        "code": "association-overclaim-causality",
        "method": "observational-causality",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(
            r"\b(?:observational|descriptive|correlational|association)\b[^.\n]{0,80}?"
            r"\b(?:causal effect|causes?|causally|causal impact)\b",
            re.IGNORECASE,
        ),
        "recommendation": "Use association language unless the manuscript states an identification design and its assumptions.",
    },
    {
        "code": "association-overclaim-causality-zh",
        "method": "observational-causality",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:相关性|描述性分析|观察性研究)[^。\n]{0,60}?(?:因果效应|导致|因果影响)", re.IGNORECASE),
        "recommendation": "如果没有清楚的识别设计和假设，请使用相关性或关联性表述，而不是因果表述。",
    },
    {
        "code": "staggered-did-unbiased-by-default",
        "method": "staggered-did",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(r"\b(?:staggered|multi[- ]period|two[- ]way fixed[- ]effects|TWFE)\b[^.\n]{0,110}?\b(?:automatically|by construction|always|unbiased|unambiguously)\b[^.\n]{0,60}?\b(?:causal|effect|parallel trends?)\b", re.IGNORECASE),
        "recommendation": "Name the cohort comparison, estimand, support, and heterogeneity assumptions; a staggered specification is not automatically unbiased.",
    },
    {
        "code": "continuous-treatment-identifies-dose-response",
        "method": "continuous-treatment",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:continuous treatment|treatment intensity|dose[- ]response)\b[^.\n]{0,100}?\b(?:identif(?:y|ies)|establish(?:es)?|proves?)\b[^.\n]{0,60}?\b(?:causal|the causal|the true)\b", re.IGNORECASE),
        "recommendation": "State the support, functional-form, and common-trend assumptions before describing a causal dose response.",
    },
    {
        "code": "bartik-exogenous-by-construction",
        "method": "bartik-iv",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(r"\b(?:Bartik|shift[- ]share)\b[^.\n]{0,100}?\b(?:exogenous|valid|solves? endogeneity|guarantees? exclusion)\b", re.IGNORECASE),
        "recommendation": "Separate share and shock sources, state which exogeneity argument identifies the estimate, justify exclusion, and define the estimand without assuming a complier interpretation.",
    },
    {
        "code": "cate-discovers-causal-subgroups",
        "method": "cate",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:causal forest|CATE|machine[- ]learning subgroup)\b[^.\n]{0,100}?\b(?:discover(?:s|ed)?|reveal(?:s|ed)?|prove(?:s|d)?)\b[^.\n]{0,55}?\b(?:causal mechanism|true subgroup|causal subgroup)\b", re.IGNORECASE),
        "recommendation": "Report the target population, overlap, sample splitting, multiplicity, and whether subgroup rules were prespecified.",
    },
    {
        "code": "quantile-oaxaca-causal-interpretation",
        "method": "quantile-oaxaca",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:quantile regression|Oaxaca|unexplained component)\b[^.\n]{0,100}?\b(?:causal|discrimination|treatment effect|mechanism)\b", re.IGNORECASE),
        "recommendation": "Label the result as conditional/distributional or decomposition evidence and state the reference structure; causal language needs a separate design.",
    },
    {
        "code": "survey-causality-overclaim",
        "method": "survey",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:survey|questionnaire|self[- ]reported)\b[^.\n]{0,90}?\b(?:causes?|causal effects?|causal mechanism|causality)\b", re.IGNORECASE),
        "recommendation": "Describe the target population, sampling/nonresponse and measurement limits; reserve causal language for a randomized survey design.",
    },
    {
        "code": "qualitative-generalization-overclaim",
        "method": "qualitative",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:qualitative|interview|case study|thematic analysis)\b[^.\n]{0,100}?\b(?:generaliz(?:e|es|able)|universal|causal effect|population[- ]wide)\b", re.IGNORECASE),
        "recommendation": "Bound the interpretation to the sampled cases and process evidence, and report transferability rather than population-wide effects.",
    },
    {
        "code": "staggered-did-unbiased-by-default-zh",
        "method": "staggered-did",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"(?:分期实施|分期DID|交错实施|多期DID|双向固定效应|TWFE)[^。\n]{0,80}?(?:天然|自动|必然|无偏|不偏|证明|保证)[^。\n]{0,45}?(?:因果|平行趋势|处理效应)", re.IGNORECASE),
        "recommendation": "说明队列比较、估计对象、支持范围和异质性假设；分期DID并不会天然无偏。",
    },
    {
        "code": "continuous-treatment-identifies-dose-response-zh",
        "method": "continuous-treatment",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:连续处理|处理强度|剂量反应)[^。\n]{0,70}?(?:识别|证明|建立)[^。\n]{0,45}?(?:因果|真实)", re.IGNORECASE),
        "recommendation": "说明处理强度的支持范围、函数形式和共同趋势假设，再讨论因果剂量反应。",
    },
    {
        "code": "cate-discovers-causal-subgroups-zh",
        "method": "cate",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:因果森林|CATE|机器学习亚组)[^。\n]{0,70}?(?:发现|揭示|证明)[^。\n]{0,45}?(?:因果机制|真正因果亚组)", re.IGNORECASE),
        "recommendation": "报告目标总体、重叠、样本切分、多重检验和亚组规则是否预先设定。",
    },
    {
        "code": "bartik-exogenous-by-construction-zh",
        "method": "bartik-iv",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"(?:Bartik|移位份额|份额冲击)[^。\n]{0,80}?(?:外生|有效|解决内生性|保证排除限制)", re.IGNORECASE),
        "recommendation": "分别说明份额和冲击的来源、识别依赖哪一种外生性论证及排除限制，并界定估计对象；不要自动套用服从者解释。",
    },
    {
        "code": "quantile-oaxaca-causal-interpretation-zh",
        "method": "quantile-oaxaca",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:分位数回归|Oaxaca分解|不可解释部分)[^。\n]{0,80}?(?:因果|歧视|处理效应|机制)", re.IGNORECASE),
        "recommendation": "标明这是条件分布或分解证据，报告参照结构；因果表述需要额外识别设计。",
    },
    {
        "code": "survey-causality-overclaim-zh",
        "method": "survey",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:问卷|调查|自陈)[^。\n]{0,70}?(?:导致|因果效应|因果机制|因果关系|建立因果)", re.IGNORECASE),
        "recommendation": "说明目标总体、抽样/无应答和测量局限；只有随机化调查设计才可使用因果表述。",
    },
    {
        "code": "qualitative-generalization-overclaim-zh",
        "method": "qualitative",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:质性研究|访谈|案例研究|主题分析)[^。\n]{0,80}?(?:普遍|普适|因果效应|总体规律)", re.IGNORECASE),
        "recommendation": "将解释限定在样本案例和过程证据内，报告可迁移性而不是总体效应。",
    },
)


PATTERNS += (
    {
        **PATTERNS[0],
        "code": "parallel-trends-proven-by-event-study",
        "pattern": re.compile(
            r"\bparallel trends?\b[^.;\n]{0,50}?\b(?:proven|proved|established|confirmed|demonstrated)\b"
            r"[^.;\n]{0,35}?\bby\b[^.;\n]{0,45}?\b(?:event[- ]study|event[- ]time plot|pre[- ]trend plot)\b",
            re.IGNORECASE,
        ),
    },
    {
        **PATTERNS[1],
        "code": "parallel-trends-proven-by-event-study-zh",
        "pattern": re.compile(r"平行趋势[^。；\n]{0,20}?(?:被|由)[^。；\n]{0,25}?事件研究[^。；\n]{0,20}?(?:证明|证实|验证)"),
    },
)

# Scope qualification to the current statement. A caveat in a preceding sentence
# or across "but/但" must not hide an affirmative overclaim. This remains a bounded
# lexical screen, not a parser of nested quotations or logical propositions.
CLAUSE_BOUNDARY = re.compile(
    r"[。！？；;\n]|(?<!\d)[.!?](?!\d)|\b(?:but|however|yet)\b|然而|不过|(?<!不)但(?:是)?",
    re.IGNORECASE,
)
NEGATED_EN = re.compile(
    r"\b(?:not(?!\s+(?:only|just|merely)\b)|never|cannot|can't|doesn't|don't|without)\b[^,;\n]{0,35}?"
    r"\b(?:prov|demonstrat|establish|confirm|solv|eliminat|remov|cur|address|identif|causal|"
    r"exogenous|valid|generaliz|universal|population|discrimination)\w*\b",
    re.IGNORECASE,
)
NEGATED_ZH = re.compile(
    r"(?:不(?!仅|但|只)|并非|无法|未能|没有)[^，；\n]{0,30}?"
    r"(?:证明|证实|验证|解决|消除|克服|识别|因果|外生|有效|普适|普遍|总体规律|歧视)",
    re.IGNORECASE,
)
CONDITIONAL = re.compile(
    r"\b(?:only if|only under|conditional on|provided that|requires?|depends? on)\b"
    r"|\bunder\b[^.;\n]{0,50}?\bassumptions?\b|需要|有待|取决于|以.{0,25}为前提|在.{0,25}假设下",
    re.IGNORECASE,
)
AUTOMATIC_VALIDITY = re.compile(
    r"\b(?:by construction|automatically|inherently|always|guarantees?|solves? endogeneity)\b"
    r"|天然|自动|必然|保证|解决内生性", re.IGNORECASE,
)


def statements(text: str):
    start = 0
    for boundary in CLAUSE_BOUNDARY.finditer(text):
        yield start, text[start:boundary.start()]
        start = boundary.end()
    yield start, text[start:]


def needs_context(item: dict[str, Any], statement: str) -> bool:
    # An IV validity discussion is not automatically an unsupported guarantee.
    if item["method"] == "bartik-iv":
        return not AUTOMATIC_VALIDITY.search(statement)
    if item["method"] == "survey" and not re.search(
        r"\b(?:prov(?:e[sd]?|en)|establish(?:es|ed)?|demonstrate[sd]?|confirm(?:s|ed)?|causes?)\b"
        r"|证明|证实|导致|建立因果", statement, re.IGNORECASE,
    ):
        return True
    if item["method"] == "qualitative":
        return not re.search(
            r"\b(?:universal|population)\b|普遍|普适|总体规律"
            r"|\b(?:prov(?:e[sd]?|en)|establish(?:es|ed)?|confirm(?:s|ed)?)\b.{0,45}\bcausal effect\b"
            r"|(?:证明|证实).{0,25}因果效应", statement, re.IGNORECASE,
        )
    # A conditional causal interpretation can be justified by the supplied design.
    # These cues request contextual review, not a failed patch or a design approval.
    if item["method"] in {"continuous-treatment", "observational-causality", "quantile-oaxaca", "survey"}:
        return bool(CONDITIONAL.search(statement) or re.search(
            r"\brandomi[sz]ed\b|随机分配|随机化", statement, re.IGNORECASE,
        ))
    return False


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def check(text: str, path: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    advisories: list[dict[str, Any]] = []
    for offset, statement in statements(text):
        for item in PATTERNS:
            for match in item["pattern"].finditer(statement):
                matched_text = match.group(0).strip()
                if (item["language"] == "en" and NEGATED_EN.search(matched_text)) or (
                    item["language"] == "zh" and NEGATED_ZH.search(matched_text)
                ):
                    continue
                advisory = needs_context(item, statement)
                finding = {
                    "code": item["code"],
                    "method": item["method"],
                    "language": item["language"],
                    "severity": "moderate" if advisory else item["severity"],
                    "line": line_number(text, offset + match.start()),
                    "match": matched_text,
                    "context": statement.strip(),
                    "recommendation": item["recommendation"],
                    "basis": "context-needed" if advisory else "known-overclaim-pattern",
                }
                (advisories if advisory else issues).append(finding)
    issues.sort(key=lambda issue: (issue["line"], issue["code"], issue["match"]))
    advisories.sort(key=lambda issue: (issue["line"], issue["code"], issue["match"]))
    blocking = sum(issue["severity"] == "blocking" for issue in issues)
    major = sum(issue["severity"] == "major" for issue in issues)
    return {
        "schema_version": "1.0",
        "status": "fail" if issues else "pass",
        "file": str(path),
        "issue_count": len(issues),
        "blocking_count": blocking,
        "major_count": major,
        "issues": issues,
        "advisory_count": len(advisories),
        "advisories": advisories,
        "decision": "author-required" if issues else "review-needed" if advisories else "no-known-overclaim",
        "scope": "Known overclaims fail; contextual advisories do not block. Neither result proves identification.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        text = args.manuscript.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result = {"schema_version": "1.0", "status": "fail", "file": str(args.manuscript), "errors": [str(exc)]}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0], file=sys.stderr)
        return 2
    result = check(text, args.manuscript)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"issues: {result['issue_count']}")
        for issue in result["issues"]:
            print(f"- line {issue['line']}: {issue['code']}: {issue['match']}")
        for advisory in result["advisories"]:
            print(f"- review context at line {advisory['line']}: {advisory['match']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
