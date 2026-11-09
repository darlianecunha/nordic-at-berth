# Nordic At-Berth CO2

At-berth CO2 emissions from the auxiliary engines of cargo ships in **all Finnish ports** and **19 Norwegian ports**, 2019 to 2025, estimated call by call from open national port-call registers. Preliminary results, November 2026.

Live page: https://nordic-at-berth.vercel.app

## What the page shows

- At-berth CO2 by year, with the change 2019 to 2025
- LMDI decomposition of that change into number of calls, time at berth and vessel power
- Concentration by port and, for Finland, by berth (the Finnish register records a berth code on every call)
- Shore-power ceiling by year, using each year's national grid emission factor
- Segment shares (general cargo and ro-ro, container, liquid bulk, dry bulk)

## Method

The inventory follows Cunha, D. R., Oliveira, C. B. M., Santos, V. R. P., & Pinheiro, R. E. P. (2026). At-berth CO2 emissions at a Brazilian bulk-heavy multi-cargo port: drivers, shore power potential and implications for port decarbonisation management. *Case Studies on Transport Policy*, 26, 102005. https://doi.org/10.1016/j.cstp.2026.102005

CO2 = auxiliary power at berth (Fourth IMO GHG Study, by segment and DWT class) × hours alongside × SFOC (185 g/kWh, MGO) × 3.206 g CO2 per g fuel.

Limits: auxiliary boilers are excluded, so totals are a lower bound for tankers; stays shorter than 1 h or longer than 240 h are removed as AIS artefacts or lay-ups; passenger ships, ferries, offshore and fishing vessels are outside the inventory; Finnish DWT missing in the register (about 15% of calls) was imputed from gross tonnage by segment. Shore-power scenarios assume full uptake and 97% transmission efficiency; they are a technical ceiling, not a forecast.

## Data sources

| Country | Source | Licence | Content |
|---|---|---|---|
| Finland | [Fintraffic Digitraffic port-call API](https://www.digitraffic.fi/en/marine-traffic/) | CC BY 4.0 | 219,410 calls with IMO, berth, ATA, ATD; vessel register with GT, DWT, engine power |
| Norway | [Kystverket Kystdatahuset API](https://kystdatahuset.no) | Open | 211,965 calls in 19 ports with GT and DWT |
| Grid factors | [Statistics Finland, table 14qt](https://pxdata.stat.fi/PxWeb/pxweb/en/StatFin/StatFin__ehk/statfin_ehk_pxt_14qt.px); NVE climate declaration (Norway) | Open | g CO2/kWh by year |
| Engine parameters | IMO (2020), Fourth IMO GHG Study | | Auxiliary power by segment and size class |

Data downloaded on 9 November 2026. The page embeds aggregated results only; call-level tables are available on request.

## Files

- `index.html`: the page, a single self-contained file (no external dependencies)
- `template.html`: page template with a `/*__DATA__*/` placeholder
- `build_site.py`: reads the result tables of the inventory and writes `index.html`

## Licence and citation

Analysis and charts: CC BY 4.0, Darliane Ribeiro Cunha, PhD, https://orcid.org/0000-0003-2548-1237

Cite as: Cunha, D. R. (2026). Nordic At-Berth CO2: at-berth emissions of cargo ships in Finnish and Norwegian ports, 2019-2025, from open port-call registers. https://nordic-at-berth.vercel.app
