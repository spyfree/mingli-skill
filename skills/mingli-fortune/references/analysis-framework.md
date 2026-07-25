# Analysis Framework

## Read Facts First

- Generate the chart before interpreting.
- Keep chart facts and interpretive language separate.
- Use Ziwei for palace structure, star pattern, and cycle emphasis.
- Use Bazi for day-master balance, ten gods, five elements, and structural temperament.

## Ziwei Checklist

Start with the natal structure:

- `命宫`: baseline temperament, motivation, identity style
- `身宫`: how the person acts, responds, and manifests traits
- primary stars and major supporting or afflicting stars
- `三方四正`: whether the surrounding palaces reinforce or weaken the core pattern
- `四化`: what gets activated, pressured, or redirected

Use focused palace analysis by topic:

| Topic | Ziwei palaces to emphasize |
| --- | --- |
| Personality | 命宫, 身宫, 福德 |
| Career | 官禄, 财帛, 迁移, 仆役 |
| Wealth | 财帛, 田宅, 福德 |
| Relationships | 夫妻, 福德, 迁移 |
| Family of origin | 父母, 兄弟, 福德 |
| Home and assets | 田宅, 财帛 |
| Children or creative output | 子女, 福德 |
| Health boundaries | 疾厄, 福德 |

## Bazi Checklist

Read the Bazi structure in this order:

- `日主`: core self and energetic center
- `月令`: seasonal context and strength tendency
- ten-god distribution: authority, output, wealth, support, peer pressure
- five-element balance and missing or excessive elements
- hidden stems and branch support when materially relevant

Treat these as guidance rules:

- If day-master support is strong and output or wealth stars are coordinated, discuss initiative and conversion capacity.
- If authority pressure is strong but support is weak, discuss stress, structure, responsibility, and friction.
- If five-element imbalance is obvious, describe behavioral tendencies and balancing suggestions, not superstitious absolutes.
- Treat `喜忌` as a practical balancing direction unless the data strongly supports a narrower school-specific claim.

## Synthesis Rules

- Before synthesizing, confirm both charts were computed from the same time basis and the same 换日 convention. A normalization mismatch — 真太阳时 applied to one system only, or a date advanced twice — presents exactly like a genuine school-level disagreement, and it will quietly drag confidence down for the wrong reason. See the Chart Consistency Contract in `input-normalization.md`.
- Raise confidence when Ziwei and Bazi point in the same direction.
- Explain divergence when the systems disagree and the basis is confirmed identical.
- Distinguish stable natal traits from current-cycle effects.
- If Ziwei gives the structural picture and Bazi gives the energetic picture, merge them instead of making them compete.
- If the user asks for one topic only, keep the synthesis narrow and relevant.

## Timing Rules

Use fortune tools only after the natal base is clear.

- `get_ziwei_fortune`: explain which palaces or transformations are being activated in the requested period.
- `get_bazi_fortune`: explain how the 大运 or 流年 interacts with the natal balance and ten-god structure.
- Do not describe a cycle as purely good or bad. Explain what it rewards, what it pressures, and what it tests.
- For `流年` questions, anchor the reading to the requested year or the current date.

## Response Contract

Use this structure by default:

1. `咨询摘要`
2. `排盘口径与置信度`
3. `紫微斗数排盘事实`
4. `八字排盘事实`
5. `综合命理解读`
6. `运势与时间窗口` when requested
7. `建议与边界`

Within `综合命理解读`, cover:

- personality and temperament
- strengths and growth edges
- career and work style
- wealth behavior and risk pattern
- relationships and communication pattern
- health or stress boundaries

## Wording Rules

- Use phrases like `盘面提示`, `更容易`, `倾向于`, `这个阶段更适合`, and `这里需要留意`.
- Avoid language that sounds guaranteed, fatalistic, or manipulative.
- If the chart fact is weak or the input is incomplete, say so plainly.
- If the user asks for action guidance, convert chart signals into habits, decisions, or observation points.
