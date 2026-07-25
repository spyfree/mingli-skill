# Input Normalization

## Minimum Data

- For a full consultation, collect:
  - `date`: `YYYY-MM-DD`, the calendar date as written on the birth record. Never pre-adjust it — see [Day Boundary](#day-boundary-2300-换日).
  - clock time: exact `HH:MM` if possible, otherwise a named 时辰. This feeds the tool parameters `time_index` and, when correcting, `birth_hour` / `birth_minute`. There is no `time` parameter.
  - `gender`: the value the chart engine expects, usually `男` or `女` — see [Gender](#gender).
  - `calendar`: `solar` by default; use `lunar` only when the user explicitly gives 农历
  - `is_leap_month`: ask only when the user explicitly gives a lunar leap month
  - `birthplace` or `longitude`: required for 真太阳时 correction
- If exact birth time is unknown:
  - Ask once if the user knows the hour or approximate 时辰.
  - If still unknown, say that palace placement and fortune timing may change.
  - Offer a reduced-confidence reading instead of pretending certainty.

## Gender

The engine needs a binary value because 大运 direction derives from it (阳男阴女顺行、阴男阳女逆行). It is a computation parameter, not a judgement about identity.

- If the user states 男 or 女, use it.
- If the user has not stated it, ask once. It flips 大运 direction and therefore every timing conclusion.
- Never infer it from a name.
- If the user is non-binary or declines either value, say plainly that the traditional algorithm only branches two ways, and ask which value to use for the calculation. Note the choice in `排盘口径与置信度`.

## Parameter Defaults

- Default `calendar` to `solar`.
- Default `language` to the language the user is writing in; use `zh-CN` when in doubt. Keep 星曜, 宫位, 十神, and 干支 names in Chinese even in a non-Chinese reading, with a translation on first use — translating a 星曜 name loses the referent.
- Default `format` to `json` for internal reasoning.
- If birthplace is unknown, assume:
  - timezone conceptually `Asia/Shanghai`
  - `longitude=120.0`
  - no location-based correction claimed

## Time Mapping

Derive `time_index` from the time you will **actually use for the chart** — the 真太阳时-corrected time when correction is on, the clock time when it is off. Read [Chart Consistency Contract](#chart-consistency-contract) before filling this in.

| time_index | Time range | 时辰 |
| --- | --- | --- |
| 0 | 00:00-00:59 | 早子时 |
| 1 | 01:00-02:59 | 丑时 |
| 2 | 03:00-04:59 | 寅时 |
| 3 | 05:00-06:59 | 卯时 |
| 4 | 07:00-08:59 | 辰时 |
| 5 | 09:00-10:59 | 巳时 |
| 6 | 11:00-12:59 | 午时 |
| 7 | 13:00-14:59 | 未时 |
| 8 | 15:00-16:59 | 申时 |
| 9 | 17:00-18:59 | 酉时 |
| 10 | 19:00-20:59 | 戌时 |
| 11 | 21:00-22:59 | 亥时 |
| 12 | 23:00-23:59 | 晚子时 |

Important rules:

- Treat `23:00-23:59` as `晚子时 (12)` and `00:00-00:59` as `早子时 (0)`.
- If the user only says `子时` and cannot clarify whether it was before or after midnight, say so before reading. The two indices produce different 日柱 and often a different 命宫, so state which conclusions are unaffected; offer to run both charts for comparison only if the user wants that resolved, since it doubles the call count.
- If the user gives only a named 时辰 such as `午时`, map directly to the index and do not fabricate minute-level precision. Do not enable solar-time correction in this case — there is no minute to correct.

## Day Boundary (23:00 换日)

One of the three 排盘事故源 named in `consultation-standards.md` §1.4. The characteristic failure is a **double advance**: the reader advances the date to the next day *and* the engine advances it internally, leaving 日柱 two days off. Nothing errors; the 日主 is simply wrong, and with it every 十神 and 格局 conclusion.

Rule: **pass `date` exactly as it appears on the birth record. Never advance it yourself.** `time_index = 12` is what carries the 晚子时 semantics — let the engine apply its own convention.

Then verify, because conventions differ between 八字 schools as well as between the two systems:

- 八字 has two live conventions. The traditional 子初换日 rule starts the new day at 23:00, so a 23:xx birth gets the 日柱 of `date + 1` — this school does not distinguish 早/晚子时 at all. The 早晚子时 (夜子时) school changes the day at 00:00 instead: a 23:xx birth is 晚子时 of the current day, 日柱 stays on `date`, 时柱 stays 子. An engine exposing a 0-vs-12 split speaks the second school's vocabulary, but that alone does not guarantee its 日柱 handling — hence the check below.
- 紫微 in most schools keeps the calendar day for 命宫 and 身宫 placement and does not advance.

For any 23:00–23:59 birth, check the returned 日柱 against both candidates before interpreting:

- returned 日柱 matches the 干支 of `date` → the engine uses 子正换日 (the 早晚子时/夜子时 convention)
- returned 日柱 matches the 干支 of `date + 1` → the engine uses 子初换日 (the traditional 23:00 changeover, no 早/晚 split)

State which convention applies in `排盘口径与置信度`, and note that 日主, 十神, and 格局 conclusions rest on it. If the returned data does not let you tell, treat every 日柱-based conclusion as low confidence rather than guessing.

Solar-time correction can move the date across this boundary in either direction — see below.

## Chart Consistency Contract

The cross-validation mechanism in `SKILL.md` ("when Ziwei and Bazi agree, raise confidence") is only valid if both charts come from the **same instant under the same conventions**. If Ziwei runs on 真太阳时 while Bazi runs on clock time, the two charts describe different people — and the resulting divergence gets misread as a school-level disagreement, silently lowering confidence for the wrong reason. This failure is invisible in the output.

Fix these three things once, before the first chart call, and reuse them for every call in the consultation:

1. **One time basis.** Decide correction on or off once, and apply that decision to Ziwei *and* Bazi. Never to one only.
2. **One `time_index`.** Derive it from the basis chosen in (1). Do not compute `time_index` from the clock time and also pass `use_solar_time=true` — that combination is self-contradictory, and if the engine honors `time_index` the correction silently no-ops for 命宫 placement, the most consequential field in the Ziwei chart.
3. **One `date`.** The calendar date from the record, unless correction moved it across midnight.

Record the basis in `排盘口径与置信度`: clock time, corrected time, the 时辰 actually used, and whether the two differ.

If a chart tool turns out not to accept the solar-time parameters, do **not** fall back to clock time for that system. Derive `time_index` from the corrected time yourself so both systems land on the same 时辰, and say that the 时柱 and 宫位 rest on a manually corrected 时辰.

## Solar-Time Correction

Enable 真太阳时 correction only when all of the following hold:

- a known birthplace or longitude
- an exact clock time, or at least a reliable hour
- a case where 时辰-boundary precision matters

When enabled, pass to **both** chart tools:

- `longitude`
- `birth_hour`
- `birth_minute`
- `use_solar_time=true`

and set `time_index` from the corrected time, per the consistency contract above.

Approximate the correction as:

```
平太阳时 ≈ 钟表时 − (标准经线经度 − 出生地经度) × 4 分钟
真太阳时 ≈ 平太阳时 + 均时差
```

For China Standard Time the 标准经线 is `120°E`. 均时差 swings roughly ±16 minutes across the year, so a hand estimate is only good to about a quarter hour — never claim exact correction from a manual calculation near a 时辰 boundary.

Handle these cases explicitly:

- **Far-west China** (Xinjiang, Tibet, Gansu, Qinghai): the shift reaches one to two hours and routinely moves the 时辰. Ürümqi (≈87.6°E) is about −130 minutes, so a 15:30 clock birth is ≈13:20 真太阳时 — 未时, not 申时.
- **Correction crossing midnight backwards.** A 00:20 clock birth in Ürümqi corrects to ≈22:10 on the *previous* day: 亥时 of `date − 1`, not 早子时 of `date`. Both `date` and `time_index` change. State this explicitly and re-confirm with the user before continuing.
- **Correction crossing 23:00 forwards** puts the birth into 晚子时. Apply the Day Boundary rules to the corrected time, not the clock time.
- **Boundary inside the 均时差 margin.** If the corrected time lands within about 15 minutes of a 时辰 boundary, treat both adjacent 时辰 as live and report which conclusions are stable across them.
- **Non-China birthplaces**: use that zone's own standard meridian, not 120°E.
- If the user knows only a broad window, do not claim correction at all.
- If correction changes the 时辰, say so in `排盘口径与置信度`. This is the single most consequential normalization step.

## Suggested Base Calls

Read the parameter schema from the server's `tools/list` before the first call of a session and follow it wherever it differs from these examples. Discovery is free and authoritative; a guessed parameter name wastes a metered call.

Correction on. Note that `time_index` comes from the corrected time (15:30 at 100°E ≈ 14:10 → 未时 → `7`), not from the clock time:

```json
{
  "date": "1990-10-21",
  "time_index": 7,
  "gender": "女",
  "calendar": "solar",
  "format": "json",
  "language": "zh-CN",
  "longitude": 100.0,
  "birth_hour": 15,
  "birth_minute": 30,
  "use_solar_time": true
}
```

Correction off — no longitude, no `birth_hour` / `birth_minute`, and `time_index` from the clock time (15:30 → 申时 → `8`):

```json
{
  "date": "1990-10-21",
  "time_index": 8,
  "gender": "女",
  "calendar": "solar",
  "format": "json"
}
```

Pass the same `date`, `time_index`, `gender`, `calendar`, and solar-time basis to `get_ziwei_chart` and `get_bazi_chart`.

For fortune tools (`get_ziwei_fortune`, `get_bazi_fortune`):

- Pass `query_date` when the user asks about a specific year or date.
- Otherwise use the current date and say the fortune reading is anchored to that date.
- Pass the same natal basis as the chart calls.

For the analysis tools (`analyze_bazi_element`, `analyze_ziwei_palace`): the palace and element argument vocabulary is engine-defined. Take it from `tools/list` rather than guessing between `官禄`, `career`, and a numeric index. If the schema is unavailable, say what you could not compute instead of spending calls on guesses.

## Call Budget

Chart calls are metered under a daily quota — take the current figure from the purchase page or the server's limit error, never from this file, for the same reason `SKILL.md` does not hardcode the price. Treat calls as a budget:

- Compute each chart once per consultation and reuse the returned facts for follow-up questions. Re-call only when the birth data, the 时辰 basis, or the requested period changes.
- A full reading is 3 calls; adding both fortune tools makes 5. A two-person comparison doubles it.
- Never re-run a chart to double-check it. Re-read the JSON already in the conversation — including for the Day Boundary verification above, which is an inspection of returned 日柱, not a second call.
