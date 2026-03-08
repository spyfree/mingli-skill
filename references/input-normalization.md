# Input Normalization

## Minimum Data

- For a full consultation, collect:
  - `date`: `YYYY-MM-DD`
  - `time`: exact `HH:MM` if possible, otherwise a named 时辰
  - `gender`: map to the tool's expected values, usually `男` or `女`
  - `calendar`: `solar` by default; use `lunar` only when the user explicitly gives 农历
  - `is_leap_month`: ask only when the user explicitly gives a lunar leap month
  - `birthplace` or `longitude`: use for 真太阳时 correction when available
- If exact birth time is unknown:
  - Ask once if the user knows the hour or approximate 时辰.
  - If still unknown, say that palace placement and fortune timing may change.
  - Offer a reduced-confidence reading instead of pretending certainty.

## Parameter Defaults

- Default `calendar` to `solar`.
- Default `language` to `zh-CN`.
- Default `format` to `json` for internal reasoning.
- If birthplace is unknown, assume:
  - timezone conceptually `Asia/Shanghai`
  - `longitude=120.0`
  - no special location-based correction claimed

## Time Mapping

Use these `time_index` values for `get_ziwei_chart`, `get_ziwei_fortune`, `get_bazi_chart`, and `get_bazi_fortune`:

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

- Treat `23:00-23:59` as `晚子时 (12)`.
- Treat `00:00-00:59` as `早子时 (0)`.
- If the user only says `子时` and cannot clarify whether it was before or after midnight, explain the ambiguity before reading.
- If the user gives only a named时辰 such as `午时`, map directly to the corresponding index and do not fabricate minute-level precision.

## Solar-Time Correction

Enable 真太阳时 correction only when all of the following are available:

- a known birthplace or longitude
- an exact clock time or at least a reliable hour
- a use case where time-boundary precision matters

When using correction for Ziwei, pass:

- `longitude`
- `birth_hour`
- `birth_minute`
- `use_solar_time=true`

Use caution in these cases:

- Northwestern China, Tibet, and other far-west locations can shift the 时辰 materially.
- If the user only knows a broad time window, do not claim exact correction.
- If correction changes the时辰, say so explicitly in `排盘口径与置信度`.

## Suggested Base Calls

Use payloads shaped like these:

```json
{
  "date": "1990-10-21",
  "time_index": 8,
  "gender": "女",
  "calendar": "solar",
  "format": "json",
  "language": "zh-CN",
  "longitude": 120.0,
  "birth_hour": 15,
  "birth_minute": 30,
  "use_solar_time": true
}
```

```json
{
  "date": "1990-10-21",
  "time_index": 8,
  "gender": "女",
  "calendar": "solar",
  "format": "json"
}
```

For fortune tools:

- Pass `query_date` when the user asks about a specific year or date.
- Use the user's requested date directly if given.
- Otherwise use the current date and say that the fortune reading is anchored to that date.
