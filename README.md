# Piloto AIS Europa (inventário por escala em um porto europeu)

Objetivo: aplicar o método Itaqui/Paranaguá (escalas, fases, maritimeco2) a um porto europeu com AIS aberto,
para o CV do Vici (evidência de transferência) e para a Proposta B.

## Fontes abertas testadas em 07/11/2026

| Fonte | Cobertura | Histórico | Acesso | Situação |
|---|---|---|---|---|
| Danish Maritime Authority, aisdata.ais.dk (novo endereco; o antigo web.ais.dk saiu do ar) | Águas dinamarquesas (Aarhus, Copenhague, Fredericia, Esbjerg, Kalundborg...) | Diário desde 2006, CSV em .zip (centenas de MB/dia) | Sem login | Funciona por http; download direto do bucket S3 |
| Kystdatahuset (Kystverket, Noruega) | Águas norueguesas | Histórico via API | Cadastro gratuito em kystdatahuset.no/api-access | Aberta sem login; usada |
| Digitraffic (Fintraffic, Finlândia) | Águas finlandesas | Só posições atuais (API aberta, funciona); histórico não | Sem login | Útil só com coletor contínuo |
| Global Fishing Watch API | Global, eventos de escala em porto (port visits) derivados de AIS | Desde 2012 | Token gratuito | Pendente de cadastro; dá escalas, não fases |
| NOAA MarineCadastre (EUA) | Costa dos EUA | Diário, aberto | Sem login | Funciona; fora da Europa |

## Resultados em 07/11/2026

**Noruega (Kystdatahuset, API aberta sem login)**: `noruega/dados/` tem 211.965 escalas em 19 portos (2019-2025), com navio, tipo, GT, DWT, chegada, saida e horas atracado, mais 43.075 escalas em cais com shore power (`escalas_osps_2019_2025.csv`). Script: `noruega/baixar_kystdatahuset.py`.

`noruega/inventario_atberth.py` aplica o metodo do inventario Itaqui/Paranagua (IMO GHG4, Tabela 17; MDO por ser SECA) aos quatro segmentos de carga: 100.080 escalas no escopo, **971 mil t de CO2 at-berth em 2019-2025** (75% granel liquido, puxado por Mongstad e Karsto; carga geral 12%, conteiner 8%, granel solido 5%). Saidas em `noruega/inventario/`: `inventario_porto_ano.csv`, `inventario_porto_ano_segmento.csv`, `escalas_com_co2.csv` (linha a linha) e `fora_do_escopo_horas.csv` (passageiros, ro-pax, cruzeiros, pesca, offshore, rebocadores: 9,8 milhoes de horas sem CO2 calculado, por falta de tabela de potencia nesses segmentos).

Ressalvas: 2024 tem o dobro de escalas dos outros anos (provavel mudanca de cobertura da Kystverket; confirmar antes de usar em serie); 478 escalas tiveram DWT imputado por GT; a caldeira de navios-tanque atracados segue a hipotese do modelo brasileiro (1.350 kW nas faixas maiores) e e o que faz Mongstad dominar.

**Dinamarca (aisdata.ais.dk, bucket S3 aberto, AIS bruto diario desde 2006, 550-750 MB/dia)**: 1 a 3 de outubro de 2026 baixados e filtrados para Aarhus, Copenhague e Fredericia (`dinamarca/*.csv`, so Class A, sem pesca/lazer/rebocador). Proximo passo: reconstruir escalas e fases (fundeio, manobra, atracacao) por MMSI.

## Fluxo

1. Baixar os dias desejados de `https://web.ais.dk/aisdata/` (ex.: `aisdk-2026-10-01.zip`) para `brutos/`.
2. `python3 filtrar_aisdk.py --porto aarhus --entrada brutos --saida filtrado --apagar`
   (mantém só Class A, dentro da caixa do porto, sem pesca/lazer/rebocador; alguns MB por dia).
3. Próximo passo (a escrever): `escalas.py` para reconstruir escalas por MMSI (fundeio, manobra, atracação)
   a partir de SOG, status de navegação e polígonos de cais; depois `maritimeco2` para o CO2 por fase.

## Caixas dos portos (lat_min, lat_max, lon_min, lon_max)

Ver `PORTOS` em `filtrar_aisdk.py`; ajustar quando os polígonos de cais estiverem definidos.
