# Project Brief — Ecuador Quantificado: Remittances Visualization

> **For:** Claude Code
> **Goal:** Build a single, polished, fully reproducible data visualization for the *Ecuador Quantificado* data-viz contest (El Quantificador + LIDE).
> **Note on language:** This brief is in English, but ALL text rendered inside the chart (title, axis labels, annotations, source line) MUST be in **Spanish** — the contest and judges are Spanish-speaking.

---

## 1. Context (why this matters)

The contest rewards visualizations that communicate a **relevant, evidence-based story about Ecuadorian society**, are based on **verifiable data**, and ship with **the data + steps to reproduce** the analysis. Deadline: **June 27, 2026**. Prizes: 3 months of DataCamp + publication in El Quantificador. Tagline of the organizer: *"La verdad se cuenta con datos."*

Reproducibility is an explicit requirement and the main differentiator. This project must deliver not just an image, but a clean script + dataset + README that lets a judge regenerate the chart from scratch.

## 2. The single message (one chart, one idea)

> **Las remesas que recibe Ecuador se duplicaron en cinco años y hoy son una de sus mayores fuentes de divisas — el reflejo financiero de la emigración masiva, no una señal de prosperidad.**

The chart should make this idea obvious at a glance. Avoid clutter; this is a single-story graphic, not a dashboard.

## 3. The data (verifiable, with sources)

Primary source: **Banco Central del Ecuador (BCE)**. Cross-check / programmatic source: **World Bank** (indicator `BX.TRF.PWKR.CD.DT`, country `ECU`), available via the World Bank API (fully reproducible).

### 3.1 Recommended approach
1. Pull the full annual remittances-received series for Ecuador programmatically from the **World Bank API** (this guarantees reproducibility and full year coverage). Endpoint pattern:
   `https://api.worldbank.org/v2/country/ECU/indicator/BX.TRF.PWKR.CD.DT?format=json&per_page=100`
2. The World Bank series usually **lags by 1–2 years**, so **append the latest official BCE figures** for the most recent years as a small, clearly-cited CSV. Mark these points in the chart (e.g. a subtle "dato BCE" note) so the provenance is transparent.
3. Store the merged series as `data/remesas_ecuador.csv` with columns: `anio, remesas_millones_usd, fuente`.

### 3.2 Known official figures to validate against (USD millions, remittances received)
These are from BCE reporting (verify against the live source when building; do not hardcode blindly without the source column):

| Año  | Remesas (USD M) | Fuente |
|------|-----------------|--------|
| 2016 | 2,601           | BCE    |
| 2020 | 3,337           | BCE    |
| 2022 | 4,743           | BCE    |
| 2023 | 5,447.5         | BCE    |
| 2024 | 6,539.8         | BCE    |
| 2025 | 7,729           | BCE    |

(Use the World Bank API for the complete year-by-year series; use the table above to sanity-check and to fill the most recent years the WB API may not yet publish.)

### 3.3 Context stats for annotations (cite, don't clutter)
- 2025 remittances ≈ **~6% of GDP**; 2024 ≈ 5.3% of GDP.
- **United States = 77.8%** of remittances received in 2025 (ties the surge to recent emigration).
- Jan–Sep 2025: remittances received (USD 5,737 M) **exceeded** Ecuador's total external financing for the year (USD 4,520 M).
- Source citation line to render on the chart:
  `Fuente: Banco Central del Ecuador y Banco Mundial. Elaboración propia.`

## 4. The visualization spec

- **Type:** Line chart (or area chart) of **annual remittances received, 2007–2025** (use full available range; 2000–2025 is fine if data is clean).
- **X axis:** `Año`. **Y axis:** `Remesas recibidas (millones de USD)`.
- **Highlight the post-2020 surge:** annotate the steep climb from 2020 onward (e.g. shaded region or annotated arrow: `Se duplican en 5 años`).
- **One context callout** on the chart: a small annotation noting `EE. UU. = 77,8% de las remesas (2025)` OR `Superan al financiamiento externo del país`. Pick the single strongest one — do not add both; keep it clean.
- **Title (Spanish, on-chart):** `Récord de remesas: el dinero de la emigración sostiene a Ecuador`
- **Subtitle (Spanish, on-chart):** `Las remesas recibidas se duplicaron entre 2020 y 2025`
- **Number formatting:** thousands separator, USD millions. Spanish decimal/format conventions are a nice touch but not required.

## 5. Design guidance

- Clean, editorial, rigorous — think a serious data-journalism outlet, not a flashy infographic. The organizer values clarity over decoration.
- Minimal gridlines, generous whitespace, one accent color for the remittances line, neutral grays for context.
- Direct-label the final data point (2025 value) instead of relying only on the axis.
- Export at high resolution suitable for social posting (the contest is promoted on Instagram/X). Produce **both** a square-ish (1080×1080 or 1080×1350) version for social and a standard landscape version.

## 6. Tech stack

- **Python** (Carlos's stack). Use `pandas` for data, `requests` for the World Bank API, and **`matplotlib`** (or `plotly` if an interactive HTML version is also wanted) for the chart.
- Keep dependencies minimal and pinned in `requirements.txt`.
- Code should be clean, commented, and runnable end-to-end with a single command.

## 7. Deliverables (file structure)

```
ecuador-remesas/
├── README.md                  # what it is, the message, data sources, how to reproduce
├── requirements.txt
├── fetch_data.py              # pulls World Bank API + merges BCE latest-year figures -> data/remesas_ecuador.csv
├── make_chart.py              # reads the CSV, renders the chart(s) to /output
├── data/
│   └── remesas_ecuador.csv    # the verifiable dataset, with a 'fuente' column
└── output/
    ├── remesas_ecuador.png        # landscape, high-res
    └── remesas_ecuador_social.png # square/portrait for Instagram/X
```

## 8. README must include (for the contest's reproducibility requirement)

1. The single-message headline and a 3–4 sentence explanation of what the chart shows and why it matters.
2. Exact data sources with URLs (BCE remittances reports; World Bank indicator `BX.TRF.PWKR.CD.DT`).
3. Step-by-step reproduction: `pip install -r requirements.txt` → `python fetch_data.py` → `python make_chart.py`.
4. A note on data provenance: which years come from the World Bank API vs. appended from BCE, so the methodology is transparent.
5. Author credit line for Carlos.

## 9. Acceptance criteria

- [ ] Running the two scripts from a clean environment regenerates the exact chart.
- [ ] All on-chart text is in Spanish; the single message is unmistakable.
- [ ] The dataset CSV is present, with a source column, and matches the official BCE figures in §3.2.
- [ ] No invented numbers — every figure traces to BCE or the World Bank.
- [ ] Two export sizes produced (landscape + social).
- [ ] README enables a stranger to reproduce the result.

## 10. Out of scope / cautions

- Do **not** turn this into a multi-panel dashboard. One chart, one message.
- Do **not** editorialize beyond what the data supports; the "emigration, not prosperity" framing should be conveyed through the US-share annotation and an honest caption, not unsupported claims.
- If the World Bank API is unreachable, fall back to building the CSV from the BCE figures in §3.2 and document this in the README.
