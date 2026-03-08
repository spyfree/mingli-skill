---
name: mingli
description: Complete Chinese fortune-reading and 命理咨询 skill for Ziwei Doushu and Bazi, backed by the `spyfree/mingli-mcp` Smithery server. Use when users ask for 算命、命理咨询、紫微斗数、八字、四柱、流年、大运、性格、事业、财运、婚恋、婚姻、感情、健康倾向、人生方向, or want a full natal chart reading from birth details. Normalize the birth data, compute the charts accurately, then deliver a structured reading with chart facts, traditional analysis, confidence notes, timing guidance, and practical advice.
---

# Mingli Fortune Consultant

## Overview

Use `spyfree/mingli-mcp` as the authoritative chart engine. Generate the chart first, reason from returned facts second, and present a complete consultation in clear sections.

## Quick Start

- Connect `spyfree/mingli-mcp` before using this skill.
- If the user wants a full reading, collect birth date, birth time, gender, calendar type, and birthplace if known.
- For the best result, combine:
  - `get_ziwei_chart`
  - `get_bazi_chart`
  - `analyze_bazi_element`
- Add fortune tools only when the user asks about `流年`, `大运`, current-year luck, or a specific period.

## Common Requests

- `帮我算命，看看事业、财运和婚姻。`
- `请用紫微斗数和八字一起看我的命盘。`
- `我想看 2026 年流年和未来十年大运。`
- `Give me a full Ziwei and Bazi reading from my birth details.`
- `Compare my natal structure with my current fortune cycle and tell me what to focus on.`

## Required Dependency

Connect the `spyfree/mingli-mcp` MCP server before using this skill. The public Smithery server is `https://mingli-mcp--spyfree.run.tools`. Prefer `json` tool output for internal reasoning; use `markdown` only when the user explicitly wants raw tool-formatted output.

## Workflow

### 1. Normalize Inputs

- For a full reading, collect: birth date, birth time (`HH:MM` if available), gender used by the system, calendar type (`solar` or `lunar`), leap-month flag when relevant, and birthplace or longitude if known.
- If the user asks for a complete reading but does not know the birth time, ask one concise follow-up question. If the time remains unknown, offer a reduced-confidence reading and say palace- and fortune-based conclusions may shift.
- When the user gives a city or longitude and exact clock time, pass `birth_hour`, `birth_minute`, `longitude`, and `use_solar_time=true` for Ziwei. If birthplace is unknown, default to `Asia/Shanghai` and `longitude=120.0`, and state that no location-specific correction was applied.
- Read `references/input-normalization.md` for `time_index` mapping, default assumptions, and ambiguity handling.

### 2. Choose The Tool Set

- For a complete reading, call:
  - `get_ziwei_chart`
  - `get_bazi_chart`
  - `analyze_bazi_element`
- Add `get_ziwei_fortune` and `get_bazi_fortune` when the user asks about timing, current year, a specific year, or period trends.
- Add `analyze_ziwei_palace` when the user asks for a focused deep dive on career, wealth, relationships, health boundaries, migration, family, property, or children.
- For comparative or relationship consultation with two people, generate each chart separately and compare them manually. Do not imply a formal compatibility algorithm unless a dedicated tool exists and is connected.
- Use `format=json` whenever you need to compare fields or merge multiple tool outputs.

### 3. Read The Charts Before Interpreting

- Separate raw chart facts from interpretation.
- In Ziwei, identify the user's core structure from `命宫`, `身宫`, primary stars, key supporting or afflicting stars, `三方四正`, and major `四化`.
- In Bazi, identify `日主`, `月令`, ten-god distribution, five-element balance, and major strength or weakness signals. Treat `喜忌` as an inferred tendency, not an absolute school-specific verdict unless the returned data supports it clearly.
- When Ziwei and Bazi agree, raise confidence. When they differ, explain the tension instead of forcing a fake consensus.
- Read `references/analysis-framework.md` for the interpretation checklist and domain mapping.

### 4. Produce The Consultation

- Structure the answer in this order unless the user asks for something narrower:
  1. `咨询摘要`
  2. `排盘口径与置信度`
  3. `紫微斗数排盘事实`
  4. `八字排盘事实`
  5. `综合命理解读`
  6. `运势与时间窗口` when requested
  7. `建议与边界`
- In `综合命理解读`, cover personality, strengths, blind spots, career or work style, money patterns, relationships, and health or risk boundaries. Mention family, migration, property, children, or study only when the chart clearly supports it or the user asked.
- Keep `排盘事实` factual and attributable to the chart. Put all inference and traditional reasoning under interpretation sections.
- Use probability language such as `更容易`, `倾向于`, `盘面提示`, and `此处置信度较低`. Avoid deterministic fate claims.
- End with 2-5 concrete actions or observation points that the user can actually use.

## Topic Playbooks

- For `事业` or `工作`, emphasize `官禄`, `财帛`, `迁移`, `仆役` plus Bazi work-style and authority signals.
- For `财运`, emphasize `财帛`, `田宅`, `福德`, cashflow temperament, risk appetite, and wealth accumulation style. Do not give investment advice as certainty.
- For `婚恋` or `关系`, emphasize `夫妻`, `福德`, `迁移`, emotional style, attachment patterns, and communication risks.
- For `健康`, discuss tendencies, stress points, and preventive boundaries only. Do not diagnose disease or replace medical advice.
- For `流年` or `大运`, compare natal structure first, then explain what the current cycle amplifies, relieves, or tests.

## Quality Bar

- State all defaults and missing inputs explicitly.
- If the time is approximate or the user only knows a broad时辰范围, say which conclusions are stable and which may shift.
- Prefer one clarifying question over a long speculative reading when a missing input can materially change the chart.
- Never fabricate palace names, stars, ten gods, or fortune periods that were not returned or reasonably inferred from returned data.
- If the user asks for a machine-readable result, keep the same section logic but return a compact JSON with separate `facts`, `interpretation`, `timing`, and `advice` fields.

## Boundaries

- Treat this as traditional metaphysics and reflective guidance, not empirical certainty.
- Refuse manipulative, coercive, gambling, or guaranteed-riches framing.
- Do not replace medical, legal, or emergency guidance.
- If the user asks for an impossible precision level from incomplete birth data, explain the limitation and offer the highest-confidence partial reading instead.

## References

- Read `references/input-normalization.md` when normalizing birth details or deciding whether solar-time correction is appropriate.
- Read `references/analysis-framework.md` when composing the actual interpretation.
