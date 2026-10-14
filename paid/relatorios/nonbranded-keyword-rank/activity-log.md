# Non-Branded Keyword/Search-Term Rank — activity log

## 2026-09-07 — Relatório criado, bug de branded/nonbranded achado e corrigido

**Pedido do Edu:** rank dos termos non-branded mais usados por volume de conversão, entre os
clientes TSD (livro TopServ, MCC 4155514468). Escopo definido com o Edu: só TSD,
últimos 90 dias (2026-06-09 a 2026-09-06).

**v1 (descartada — tinha bug sério).** Puxei `keyword_view` e `search_term_view` via
`google-ads-ratos/scripts/tsd.sh read.py keywords` / `read.py search-terms` das 15 contas PPC
ativas do book, com `--since`/`--until` (o literal `LAST_90_DAYS` não existe em GAQL — só
`LAST_30_DAYS`/`LAST_MONTH`/etc, então usei range explícito). Marquei como "branded" qualquer linha
cuja campaign/ad_group tivesse `"branded"` na string. **Bug:** `"branded"` é substring literal de
`"nonbranded"`, então o filtro excluía quase todas as campanhas non-branded de verdade e sobravam só
campanhas legado/lead-gen que escondiam o nome da marca num ad group (ex.: All Seasons AC tinha um
ad group chamado literalmente `All Seasons AC (BRAND)` dentro da campanha `TSD_Search_LeadGen`, e a
campanha `TSD_07.01_Lead_Search_Mitsubishi-Brand` usa "Brand" sem "Branded"). Total non-branded
reportado na v1: só 173 conversões (keywords) / 107 (search terms) — bem abaixo do real.

**Correção do Edu:** "para o All Seasons, tudo com 'all seasons' é branded. Mesma coisa pro
Mitsubishi." Corrigi o filtro (`is_branded.py`, em `/private/tmp/.../scratchpad/`, não versionado
neste repo):
1. Detecção por nome agora distingue `branded` de `nonbranded`/`unbranded` (e também pega `brand`
   sozinho, tipo "Mitsubishi-Brand").
2. Adicionei uma lista de termos de marca própria/fabricante por conta, aplicada ao texto da
   keyword/search term **independente da campanha** — estendi pra todas as 15 contas (não só All
   Seasons AC), já que o mesmo padrão de vazamento (nome da própria empresa aparecendo como
   "non-branded" por causa de legado/broad match) apareceu em várias: All Heart ("all heart"),
   Watt's Right ("watts right"/"what's right"), Zen Air ("zen air"), Proud Pops ("proud pops",
   "problem solvers"), etc.

**v2 (final).** Non-branded total: **1.287,9 conversões** (keywords) / **1.009,4** (search terms) —
7x maior que a v1, porque agora as campanhas non-branded reais estão sendo contadas.

**Entregável:** dois PDFs plain (Times 12pt, b/w, sem branding TSD) em
`paid/relatorios/nonbranded-keyword-rank/`:
- `Nonbranded Keyword Rank - TSD Book.pdf`
- `Nonbranded Search Terms Rank - TSD Book.pdf`

**Achado que sobrou no relatório, marcado como suspeito:** Zen Air lidera disparado em ambos os
rankings ("local hvac repair company" 264 conv / "hvac contractors near me" 250 conv nos keywords;
"ac technicians" 253 conv nos search terms), todos custando menos de ~$6/conversão — muito fora da
curva do resto do book. Sinalizei no relatório pra cross-check no GA4/CRM antes de confiar no
número.

**Depois de logar isso, achei a explicação provável** (não voltei a mexer nos PDFs ainda): o log de
`clients/zen-air/google-ads-log.md`, entrada 2026-08-26, documenta que a campanha
`TSD_08.03_Search_NonBranded_Evergreen` — a mesma campanha por trás desses top keywords/search terms
— **não teve NENHUM location targeting desde que foi criada em 08-03 até ser corrigida em 08-26**.
Nesse período o tráfego veio majoritariamente de Índia/Egito/Bangladesh/Paquistão/etc, com "516
conversões" relatadas que pareciam boas demais. Ou seja: uma fatia real da janela de 90 dias deste
relatório (03/08 a 26/08, ~23 dias) tem tráfego/"conversões" da Zen Air non-branded contaminado por
ausência de geo targeting, não demanda real dos EUA.

## Aberto
- [ ] **Re-rodar o pull da Zen Air isolando pré/pós 08-26** (ou excluir esse período) pra saber
  quanto das 264/250/253 conversões é ruído do bug de geo vs. volume real pós-fix. Só assim dá pra
  confiar no número dela no ranking.
- [ ] Considerar aplicar a mesma checagem (campanha non-branded sem geo desde a criação) no resto do
  book, já que o achado de Zen Air (08-26) citava um caso latente na Cool Hand Electric — conferir
  se outras contas do book têm o mesmo buraco.
- [ ] Se quiser, decidir com o Edu se os PDFs v2 devem levar uma nota mais forte (não só "vale
  checar") já que agora tem causa raiz documentada, ou se espera o re-pull acima antes de mexer de
  novo no relatório.
