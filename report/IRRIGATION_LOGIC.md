# Smart Irrigation — Logic (Bonus Module B)

This module is **rule-based**, not a trained model, by design — it needs to be
transparent and auditable, and there is no labeled "should have irrigated"
dataset available to train against. The exact rules are published below so
the decision is fully reproducible.

## Inputs
| Field | Meaning |
|---|---|
| `crop_type` | Crop name, e.g. `Tomato`, `Potato`, `Corn`, `Apple`, `Grape`, `Pepper` (falls back to a generic `default` profile for any other crop) |
| `growth_stage` | One of `seedling`, `vegetative`, `flowering`, `fruiting` |
| `soil_moisture_percent` | Current soil moisture reading (0–100). Designed to later come from Module F's sensor feed |
| `rain_probability_percent`, `forecast_rain_mm_24h` | Weather forecast for the next 24h. Designed to later come from Module C |
| `temperature_c` | Optional. Used only to flag heat-stress urgency |
| `area_sqm` | Plot area, used to scale the recommended water volume |

## Step 1 — Look up moisture thresholds
Each `(crop, growth_stage)` pair maps to a `(min_moisture, optimal_moisture)`
pair in `MOISTURE_THRESHOLDS` (see `service.py`). Crops not in the table use
the `default` profile. These are heuristic values based on typical published
soil-moisture guidance — flowering/fruiting stages are more water-sensitive
than the seedling stage across common vegetable/fruit crops — not calibrated
against real field sensor data (see Limitations in the README).

## Step 2 — Classify current moisture
```
soil_moisture_percent < min_moisture       -> critical_deficit
soil_moisture_percent < optimal_moisture   -> moderate_deficit
soil_moisture_percent >= optimal_moisture  -> adequate
```

## Step 3 — Decide, with a rain-delay override
| Status | Default decision | Rain override |
|---|---|---|
| `critical_deficit` | Irrigate, urgency = **high** | Only delayed if `forecast_rain_mm_24h ≥ 15mm` (heavy rain expected to cover the deficit). Urgency stays "high" either way, so the farmer keeps monitoring. |
| `moderate_deficit` | Irrigate, urgency = **medium** | Delayed (urgency drops to "low") if `rain_probability_percent ≥ 60%` **or** `forecast_rain_mm_24h ≥ 5mm`. |
| `adequate` | No irrigation, urgency = **none** | — |

If irrigation is required and `temperature_c ≥ 35°C`, an extra heat-stress
reason is added (evapotranspiration rises with heat), without changing the
urgency band itself.

## Step 4 — Recommended water volume
```
moisture_deficit_percent = max(0, optimal_moisture - soil_moisture_percent)
recommended_water_liters = moisture_deficit_percent * 0.5 (L per % deficit per m²) * area_sqm
```
Always `0` when irrigation is not required (including when delayed for rain).

## Why this design
- Every threshold and constant lives in one place (`service.py`'s module-level
  constants), so the logic is auditable and reproducible, as required by the
  evaluation rubric.
- Both a hard-deficit path (irrigate regardless of light rain) and a
  soft-deficit path (delay for likely rain) are modeled, since a farmer
  ignoring a critical shortfall because of a 20% rain chance is a worse
  outcome than slightly over-watering.
- Decoupled from other bonus modules: works today with manually entered
  soil-moisture and weather values, and will work unchanged once Module F
  (IoT sensors) and Module C (live weather) exist. Its `recommended_water_liters`
  output is also designed to flow straight into Module D's
  `water_used_liters` / `water_required_liters` inputs.

## Known limitations
- Thresholds are a generic heuristic table, not calibrated per soil type
  (sandy vs. loamy vs. clay hold moisture very differently) or per local
  climate — a production system would tune these against real sensor +
  yield outcome data.
- No consideration of irrigation method efficiency (drip vs. flood) or of
  how recently the field was last irrigated.
