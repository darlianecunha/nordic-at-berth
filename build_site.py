#!/usr/bin/env python3
"""Gera index.html (pagina estatica, arquivo unico) do inventario at-berth nordico a partir dos CSVs de resultados.
Uso: python3 build_site.py   ->  site/index.html  (publicar com `npx vercel --prod` nesta pasta)"""
import json, os, pandas as pd
B = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(B, "..")
FI = os.path.join(R, "finlandia", "artigo_atberth", "resultados"); NO = os.path.join(R, "noruega", "artigo_atberth", "resultados")
# nomes conferidos no cadastro de locais do Digitraffic (/api/port-call/v1/ports) em 10/11/2026
PORT_NAMES = {"FIKTK": "Kotka (HaminaKotka)", "FISKV": "Sköldvik (Kilpilahti)", "FIHEL": "Helsinki", "FIRAU": "Rauma", "FIHKO": "Hanko", "FIKOK": "Kokkola", "FITOR": "Tornio", "FIRAA": "Raahe", "FIPOR": "Pori", "FIOUL": "Oulu", "FIKEM": "Kemi", "FIUKI": "Uusikaupunki", "FINLI": "Naantali", "FIPRS": "Pietarsaari", "FIINK": "Inkoo", "FIVAA": "Vaasa", "FITKU": "Turku", "FILAN": "Långnäs", "FIMHQ": "Mariehamn", "FIECK": "Eckerö", "FIKJO": "Kalajoki", "FILOV": "Loviisa", "FIKAS": "Kaskinen", "FIPAR": "Parainen", "FIKNT": "Kantvik", "FITOK": "Tolkkinen", "FIHMN": "Hamina"}
YEARS = [str(y) for y in range(2019, 2026)]
def kt(df, key):
    return [{"name": r[key], "values": [round(float(r[y]), 2) for y in YEARS], "total": round(float(r["total_kt"]), 1), "share": float(r["%"])} for _, r in df.iterrows()]
fi_port = pd.read_csv(os.path.join(FI, "porto_ano_kt.csv")); fi_port["port_name"] = fi_port.locode.map(lambda c: PORT_NAMES.get(c, c))
fi_berth = pd.read_csv(os.path.join(FI, "berco_ano_kt_top30.csv")).head(20)
fi_berth["name"] = fi_berth.berco.map(lambda b: PORT_NAMES.get(b.split(":")[0], b.split(":")[0]) + " · berth " + (b.split(":")[1] if b.split(":")[1] != "unknow" else "n/a"))
no_port = pd.read_csv(os.path.join(NO, "porto_ano_kt.csv"))
fi_t5 = pd.read_csv(os.path.join(FI, "t5_indicadores_anuais.csv"), index_col=0); no_t5 = pd.read_csv(os.path.join(NO, "t5_indicadores_anuais.csv"), index_col=0)
fi_t5.index = fi_t5.index.astype(str); no_t5.index = no_t5.index.astype(str)
fi_t5 = fi_t5[fi_t5.index.isin(YEARS)]; no_t5 = no_t5[no_t5.index.isin(YEARS)]  # remove a linha "var_%" da tabela anual
fi_lm = pd.read_csv(os.path.join(FI, "lmdi.csv")); no_lm = pd.read_csv(os.path.join(NO, "lmdi.csv"))
fi_t7 = pd.read_csv(os.path.join(FI, "t7_ops.csv"), index_col=0); no_t7 = pd.read_csv(os.path.join(NO, "t7_ops.csv"), index_col=0)
fi_seg = pd.read_csv(os.path.join(FI, "t6_segmento.csv")); no_seg = pd.read_csv(os.path.join(NO, "t6_segmento.csv"))
SEG = {"carga_geral": "General cargo and ro-ro", "conteiner": "Container", "granel_liquido": "Liquid bulk", "granel_solido": "Dry bulk"}
def annual(t5, t7):
    yrs = YEARS
    return {"years": [int(y) for y in yrs], "calls": [int(t5.loc[y, "escalas"]) for y in yrs], "co2_kt": [round(t5.loc[y, "co2_t"] / 1e3, 1) for y in yrs],
            "dwt": [round(t5.loc[y, "dwt_medio"]) for y in yrs], "stay_h": [round(t5.loc[y, "estadia_mediana_h"], 1) for y in yrs],
            "grid": [round(float(t7.loc[int(y), "grid_g_kwh"]), 1) for y in yrs], "ops_pct": [round(float(t7.loc[int(y), "reducao_%"]), 1) for y in yrs]}
def lmdi(df):
    r = df[(df.periodo == "2019-2025") & (df.tipo == "direto")].iloc[0]
    return {"calls": int(r["N"]), "stay": int(r["T"]), "power": int(r["P"]), "total": int(r["total_t"])}
def seg(df):
    return [{"name": SEG[r.seg], "share_co2": float(r["%CO2"]), "share_calls": float(r["%escalas"])} for _, r in df.iterrows()]
# bercos identificados e concentracao (a partir das escalas do inventario; nada em nivel de escala vai para a pagina)
_c = pd.read_csv(os.path.join(FI, "escalas_principal.csv"), usecols=["locode", "berthCode", "co2", "dwt_imputado"])
_b = (_c.locode + ":" + _c.berthCode.astype(str)).where(_c.berthCode.notna())
N_BERTHS = int(_b.nunique()); _t = _c.groupby(_b.fillna(_c.locode + ":?")).co2.sum().sort_values(ascending=False)
N_HALF = int(((_t.cumsum() / _t.sum()) < .5).sum()) + 1; IMPUTED = round(float(_c.dwt_imputado.mean()) * 100)
# extensao a navios de passageiros e obrigacao de OPS de 2030 (passageiros_ops.py)
PAX = ["ropax", "cruzeiro", "passageiros"]
def obligation(pais):
    d = os.path.join(R, pais, "artigo_atberth", "resultados_passageiros")
    sg = pd.read_csv(os.path.join(d, "segmentos_carga_e_passageiros.csv"), index_col=0).drop("TOTAL"); px = sg[sg.index.isin(PAX)]; cg = sg[~sg.index.isin(PAX)]
    rp = pd.read_csv(os.path.join(d, "ropax_escalas_curtas.csv"), index_col=0).iloc[:, 0]
    parts = [["Passenger ships, covered", px.co2_kt_obrigado_2030.sum()], ["Container ships, covered", cg.co2_kt_obrigado_2030.sum()],
             ["Passenger ships, not covered", px.co2_kt.sum() - px.co2_kt_obrigado_2030.sum()], ["Cargo ships, not covered", cg.co2_kt.sum() - cg.co2_kt_obrigado_2030.sum()]]
    tot = float(sg.co2_kt.sum())
    return {"total_kt": round(tot, 1), "parts": [{"name": n, "kt": round(float(v), 1), "pct": round(float(v) / tot * 100, 1)} for n, v in parts],
            "covered_pct": round(float(sg.co2_kt_obrigado_2030.sum()) / tot * 100), "pax_pct": round(float(px.co2_kt.sum()) / tot * 100),
            "ropax_under2h_pct": round(100 - float(rp["%acima_2h"])), "ropax_co2_over2h_pct": round(float(rp["%co2_em_escalas_acima_2h"]))}
data = {"years": YEARS, "obl": {"fi": obligation("finlandia"), "no": obligation("noruega")},
        "fi": {"label": "Finland, all ports", "annual": annual(fi_t5, fi_t7), "ports": kt(fi_port.head(15), "port_name"), "berths": kt(fi_berth, "name"), "lmdi": lmdi(fi_lm), "seg": seg(fi_seg),
               "n_calls": int(fi_t5.escalas.sum()), "n_berths": N_BERTHS, "n_berths_half": N_HALF, "dwt_imputed_pct": IMPUTED, "n_ports_total": int(len(fi_port))},
        "no": {"label": "Norway, 19 ports", "annual": annual(no_t5, no_t7), "ports": kt(no_port, "port_name"), "berths": None, "lmdi": lmdi(no_lm), "seg": seg(no_seg), "n_calls": int(no_t5.escalas.sum())}}
html = open(os.path.join(B, "template.html"), encoding="utf-8").read().replace("/*__DATA__*/", "const DATA = " + json.dumps(data) + ";")
open(os.path.join(B, "index.html"), "w", encoding="utf-8").write(html); print("index.html", len(html), "bytes")
