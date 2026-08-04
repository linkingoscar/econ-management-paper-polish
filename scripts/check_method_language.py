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
            r"\b(?:event[- ]study|event[- ]time plot|pre[- ]trend plot)\b[^.\n]{0,120}"
            r"\b(?:prove|proves|proved|demonstrate|demonstrates|establish|establishes|confirm|confirms)\b"
            r"[^.\n]{0,60}\bparallel trends?\b",
            re.IGNORECASE,
        ),
        "recommendation": "Describe pre-trend evidence as a diagnostic or consistency check; do not call it proof of parallel trends.",
    },
    {
        "code": "event-study-proves-parallel-trends-zh",
        "method": "event-study",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"事件研究[^。\n]{0,100}(?:证明|证实|验证)[^。\n]{0,40}平行趋势", re.IGNORECASE),
        "recommendation": "将事件研究表述为对趋势一致性的诊断证据，并说明剩余假设，不要写成证明平行趋势。",
    },
    {
        "code": "matching-solves-endogeneity",
        "method": "matching",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(
            r"\b(?:psm|propensity[- ]score matching|matching|matched sample)\b[^.\n]{0,100}"
            r"\b(?:solve|solves|solved|eliminate|eliminates|remove|removes|cure|cures|address|addresses)\b"
            r"[^.\n]{0,45}\bendogeneity\b",
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
            r"\b(?:control variables?|fixed effects?|heckman(?: correction)?)\b[^.\n]{0,100}"
            r"\b(?:solve|solves|solved|eliminate|eliminates|remove|removes|cure|cures|address|addresses)\b"
            r"[^.\n]{0,45}\bendogeneity\b",
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
            r"(?:倾向得分匹配|PSM|匹配方法|匹配样本|控制变量|固定效应|Heckman)[^。\n]{0,80}"
            r"(?:解决|消除|克服|完全处理|排除)[^。\n]{0,25}内生性",
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
            r"\b(?:mediation|mediator|mediation analysis)\b[^.\n]{0,100}"
            r"\b(?:prove|proves|proved|demonstrate|demonstrates|establish|establishes|confirm|confirms)\b"
            r"[^.\n]{0,55}\b(?:causal mechanism|causality)\b",
            re.IGNORECASE,
        ),
        "recommendation": "Separate descriptive mediation from causal mediation and state the mediator and identification assumptions.",
    },
    {
        "code": "mediation-proves-causal-mechanism-zh",
        "method": "mediation",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:中介分析|中介效应|中介变量)[^。\n]{0,80}(?:证明|证实|验证)[^。\n]{0,35}(?:因果机制|因果关系)", re.IGNORECASE),
        "recommendation": "区分描述性中介与因果中介，并明确中介变量的时序、外生性和识别假设。",
    },
    {
        "code": "association-overclaim-causality",
        "method": "observational-causality",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(
            r"\b(?:observational|descriptive|correlational|association)\b[^.\n]{0,80}"
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
        "pattern": re.compile(r"(?:相关性|描述性分析|观察性研究)[^。\n]{0,60}(?:因果效应|导致|因果影响)", re.IGNORECASE),
        "recommendation": "如果没有清楚的识别设计和假设，请使用相关性或关联性表述，而不是因果表述。",
    },
    {
        "code": "staggered-did-unbiased-by-default",
        "method": "staggered-did",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(r"\b(?:staggered|multi[- ]period|two[- ]way fixed[- ]effects|TWFE)\b[^.\n]{0,110}\b(?:automatically|by construction|always|unbiased|unambiguously)\b[^.\n]{0,60}\b(?:causal|effect|parallel trends?)\b", re.IGNORECASE),
        "recommendation": "Name the cohort comparison, estimand, support, and heterogeneity assumptions; a staggered specification is not automatically unbiased.",
    },
    {
        "code": "continuous-treatment-identifies-dose-response",
        "method": "continuous-treatment",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:continuous treatment|treatment intensity|dose[- ]response)\b[^.\n]{0,100}\b(?:identif(?:y|ies)|establish(?:es)?|proves?)\b[^.\n]{0,60}\b(?:causal|the causal|the true)\b", re.IGNORECASE),
        "recommendation": "State the support, functional-form, and common-trend assumptions before describing a causal dose response.",
    },
    {
        "code": "bartik-exogenous-by-construction",
        "method": "bartik-iv",
        "language": "en",
        "severity": "blocking",
        "pattern": re.compile(r"\b(?:Bartik|shift[- ]share)\b[^.\n]{0,100}\b(?:exogenous|valid|solves? endogeneity|guarantees? exclusion)\b", re.IGNORECASE),
        "recommendation": "Separate share and shock sources, justify exclusion and shock exogeneity, and state the complier estimand.",
    },
    {
        "code": "cate-discovers-causal-subgroups",
        "method": "cate",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:causal forest|CATE|machine[- ]learning subgroup)\b[^.\n]{0,100}\b(?:discover(?:s|ed)?|reveal(?:s|ed)?|prove(?:s|d)?)\b[^.\n]{0,55}\b(?:causal mechanism|true subgroup|causal subgroup)\b", re.IGNORECASE),
        "recommendation": "Report the target population, overlap, sample splitting, multiplicity, and whether subgroup rules were prespecified.",
    },
    {
        "code": "quantile-oaxaca-causal-interpretation",
        "method": "quantile-oaxaca",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:quantile regression|Oaxaca|unexplained component)\b[^.\n]{0,100}\b(?:causal|discrimination|treatment effect|mechanism)\b", re.IGNORECASE),
        "recommendation": "Label the result as conditional/distributional or decomposition evidence and state the reference structure; causal language needs a separate design.",
    },
    {
        "code": "survey-causality-overclaim",
        "method": "survey",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:survey|questionnaire|self[- ]reported)\b[^.\n]{0,90}\b(?:proves?|establishes?|causes?|causal effect|demonstrates?)\b", re.IGNORECASE),
        "recommendation": "Describe the target population, sampling/nonresponse and measurement limits; reserve causal language for a randomized survey design.",
    },
    {
        "code": "qualitative-generalization-overclaim",
        "method": "qualitative",
        "language": "en",
        "severity": "major",
        "pattern": re.compile(r"\b(?:qualitative|interview|case study|thematic analysis)\b[^.\n]{0,100}\b(?:generaliz(?:e|es|able)|universal|proves?|causal effect|population[- ]wide)\b", re.IGNORECASE),
        "recommendation": "Bound the interpretation to the sampled cases and process evidence, and report transferability rather than population-wide effects.",
    },
    {
        "code": "staggered-did-unbiased-by-default-zh",
        "method": "staggered-did",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"(?:分期实施|分期DID|交错实施|多期DID|双向固定效应|TWFE)[^。\n]{0,80}(?:天然|自动|必然|无偏|不偏|证明|保证)[^。\n]{0,45}(?:因果|平行趋势|处理效应)", re.IGNORECASE),
        "recommendation": "说明队列比较、估计对象、支持范围和异质性假设；分期DID并不会天然无偏。",
    },
    {
        "code": "continuous-treatment-identifies-dose-response-zh",
        "method": "continuous-treatment",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:连续处理|处理强度|剂量反应)[^。\n]{0,70}(?:识别|证明|建立)[^。\n]{0,45}(?:因果|真实)", re.IGNORECASE),
        "recommendation": "说明处理强度的支持范围、函数形式和共同趋势假设，再讨论因果剂量反应。",
    },
    {
        "code": "cate-discovers-causal-subgroups-zh",
        "method": "cate",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:因果森林|CATE|机器学习亚组)[^。\n]{0,70}(?:发现|揭示|证明)[^。\n]{0,45}(?:因果机制|真正因果亚组)", re.IGNORECASE),
        "recommendation": "报告目标总体、重叠、样本切分、多重检验和亚组规则是否预先设定。",
    },
    {
        "code": "bartik-exogenous-by-construction-zh",
        "method": "bartik-iv",
        "language": "zh",
        "severity": "blocking",
        "pattern": re.compile(r"(?:Bartik|移位份额|份额冲击)[^。\n]{0,80}(?:外生|有效|解决内生性|保证排除限制)", re.IGNORECASE),
        "recommendation": "分别说明份额和冲击的来源、排除限制与冲击外生性，并界定服从者估计对象。",
    },
    {
        "code": "quantile-oaxaca-causal-interpretation-zh",
        "method": "quantile-oaxaca",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:分位数回归|Oaxaca分解|不可解释部分)[^。\n]{0,80}(?:因果|歧视|处理效应|机制)", re.IGNORECASE),
        "recommendation": "标明这是条件分布或分解证据，报告参照结构；因果表述需要额外识别设计。",
    },
    {
        "code": "survey-causality-overclaim-zh",
        "method": "survey",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:问卷|调查|自陈)[^。\n]{0,70}(?:证明|证实|导致|因果效应|建立因果)", re.IGNORECASE),
        "recommendation": "说明目标总体、抽样/无应答和测量局限；只有随机化调查设计才可使用因果表述。",
    },
    {
        "code": "qualitative-generalization-overclaim-zh",
        "method": "qualitative",
        "language": "zh",
        "severity": "major",
        "pattern": re.compile(r"(?:质性研究|访谈|案例研究|主题分析)[^。\n]{0,80}(?:普遍|普适|证明|因果效应|总体规律)", re.IGNORECASE),
        "recommendation": "将解释限定在样本案例和过程证据内，报告可迁移性而不是总体效应。",
    },
)


NEGATED_EN = re.compile(
    r"\b(?:not|never|cannot|can't|doesn't|don't|does not|do not|without)\b[^.\n]{0,30}"
    r"\b(?:prove|demonstrate|establish|confirm|solve|eliminate|remove|cure|address|identify|causal)\w*\b",
    re.IGNORECASE,
)
NEGATED_ZH = re.compile(r"(?:不|并非|不能|无法|未能|没有)[^。\n]{0,30}(?:证明|证实|验证|解决|消除|克服|识别|因果)", re.IGNORECASE)


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def check(text: str, path: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    for item in PATTERNS:
        for match in item["pattern"].finditer(text):
            matched_text = match.group(0).strip()
            if (item["language"] == "en" and NEGATED_EN.search(matched_text)) or (
                item["language"] == "zh" and NEGATED_ZH.search(matched_text)
            ):
                continue
            issues.append(
                {
                    "code": item["code"],
                    "method": item["method"],
                    "language": item["language"],
                    "severity": item["severity"],
                    "line": line_number(text, match.start()),
                    "match": matched_text,
                    "recommendation": item["recommendation"],
                }
            )
    issues.sort(key=lambda issue: (issue["line"], issue["code"], issue["match"]))
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
        "decision": "author-required" if issues else "safe-fix",
        "scope": "deterministic-method-language-screen; not a causal-inference proof",
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
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
