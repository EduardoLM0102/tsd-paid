# Napps Cooling, Heating & Plumbing — Google Ads log

Customer ID `9509605037` (PPC). Longview, TX (HVAC + Plumbing). LSA fora de escopo deste log.
MCC: não confirmado ainda em qual MCC do book está (fora do padrão Topservdigital `4155514468`
usado nos outros clientes deste workspace — a verificar).

**Nota de propriedade (2026-08-03):** antes da entrada de hoje, esta conta não tinha nenhum registro
de mudanças no book do Edu (sem pasta `clients/napps/`, sem `historico.md`, sem commit além da
auditoria original). Mudanças na conta entre a auditoria (07-06) e hoje (novo build
`Leads_Search_Nonbranded_Plumbing` criado e pausado, `TSD_07.21_Search_Nonbranded_AC_Summer`
lançada, budget do PMax subiu $100→$130/dia) não têm autoria confirmada — não foram feitas
via este workspace. Ownership formal ainda não confirmado no Agency Titan.

Ver auditoria original: `paid/relatorios/napps/napps-google-ads-audit_2026-07-06.md`.

---

## 2026-07-06 — Auditoria inicial

P0 identificado: conversion tracking quebrado — só `Calls from ads` (AD_CALL) contava; formulários
do site, ligações do site e o import offline do GHL (`GHL Form Fill`) estavam todos invisíveis pro
Smart Bidding. Detalhe completo no relatório linkado acima.

---

## 2026-08-03 — Realocação de budget + rebuild de tracking

**Executado por Edu** diretamente na UI (fora deste workspace), reportado depois e confirmado via
API pelo Claude.

### 1. Budget: $20/dia do PMax pra Search Nonbranded AC Summer

| Campanha | ID | Antes | Depois |
|---|---|---|---|
| PMax `TSD_02.20_PMAX_Plumbing_CoreServices` | 23590336249 | $130/dia | **$110/dia** |
| Search `TSD_07.21_Search_Nonbranded_AC_Summer` | 24049055193 | $35/dia | **$55/dia** |

Confirmado via API (`read.py campaigns`). Risco baixo: PMax vinha gastando só ~$9/dia de média nos
últimos 30 dias (media real ~$273 de $130/dia de budget) — não era budget-constrained, é
Ad Rank/asset-constrained (mesmo diagnóstico da auditoria de 07-06). AC Summer é a campanha viva que
está de fato convertendo (4 conv / $473 / 30d antes da mudança).

### 2. Rebuild de conversion tracking — duas ações novas criadas

| Conversion action | ID | Tipo | Categoria | Status |
|---|---|---|---|---|
| `Click to call` | 7707737498 | CLICK_TO_CALL | PHONE_CALL_LEAD | ENABLED, primary |
| `TSD - Lead form` | 7707721901 | WEBPAGE | SUBMIT_LEAD_FORM | ENABLED, primary |

- **Click to call** — clique no link de telefone do site (`tel:` link), diferente do `Calls from ads`
  (que é ligação pelo Call Asset do próprio anúncio, sem passar pelo site).
- **TSD - Lead form** — via listener de evento (GTM), dispara na submissão do formulário de lead.

Confirmado via GAQL que ambas estão ENABLED e `primary_for_goal = true`. Ainda sem conversões
registradas (esperado — criadas hoje). `Calls from ads` continua a única fonte com volume real até
aqui; `GHL Form Fill` segue ENABLED/primary mas com 0 conversões nos últimos 30 dias — **não foi
mexido nesta rodada**.

### Aberto

- [ ] Confirmar que `Click to call` e `TSD - Lead form` começam a registrar conversões (checar em
  alguns dias).
- [ ] `GHL Form Fill` continua zerado — pipeline offline do GHL ainda não investigado/consertado.
- [ ] Confirmar ownership formal da conta no Agency Titan.
- [ ] Ticket do AM pra registrar por escrito a mudança de budget (mesma exigência do MasterOps v6
  aplicada nos outros clientes deste book).
- [ ] Negativas seguem ausentes nas campanhas de search ativas relevantes (Branded não tem nenhuma);
  campanha nova que queimou $977/0 conv antes de pausar não tinha negativas.

---

## 2026-08-31 — AC Summer: negativas, split de ad group, fix de landing page

**Executado pelo Claude** (direcionado pelo Edu via chat, nesta sessão).

### 1. Diagnóstico

- Snapshot 30d: $3.779 spend, 117 clicks, ~21 conv, ~$180 CPL, IS de conta 23,9%.
- Só 2 de 18 campanhas ativas: `TSD_07.21_Search_Nonbranded_AC_Summer` ($100/d) e
  `TSD_03.22_Search_Branded_Evergreen` ($60/d). `TSD_02.20_PMAX_Plumbing_CoreServices` achada
  **PAUSADA** (estava ativa a $110/d na entrada de 08-03) — mudança não documentada, sem autoria
  confirmada.
- Branded: 85,5% IS, QS 8, saudável.
- AC Summer: 25,5% IS (49% perdido pra rank, 25% pra budget), QS 1-5. Os 3 ad groups (AC Repair,
  AC Tune-Up, AC Replace Install) mandavam 100% do tráfego pra homepage (nappsac.com/) em vez das
  páginas de serviço dedicadas que o site já tem.
- Search terms mostrou a AC Summer absorvendo bastante impressão (0 clique) em busca de marca/produto
  (Goodman, Lennox, Carrier, Daikin, Amana etc.) — diluindo o histórico de CTR agregado, provável
  contribuinte pro QS baixo. Confirmado que a Napps vende/instala mini-split (fetch em
  nappsac.com/hvac-services/) — "mini split" **não** foi negativado.
- Branded já tinha ~15 keywords BROAD de marca habilitadas (não só as 2 vistas antes) com QS 8 e
  zero vazamento nos search terms — rebuild pra Phrase não se justificava; só entraram negativas de
  proteção pros concorrentes locais vistos nos search terms com 0 clique (All Seasons Professionals,
  A US Air Conditioning of Texas, Ben Maines Air Conditioning, Mack and Hansen).

### 2. Negativas adicionadas (campaign-level, PHRASE)

| Campanha | Negativas | Total depois |
|---|---|---|
| `TSD_07.21_Search_Nonbranded_AC_Summer` (24049055193) | 27 — marcas de fabricante (goodman, lennox, carrier, daikin, amana, bryant, american standard, comfortmaker, friedrich, ducane, heil, bard, ruud, mirage, cooper and hunter, della, hessaire, pioneer, mr cool, comfort aire, guardian, evcon, nfm, premaire, aaron's, lowe's, midea) | 21 → 48 |
| `TSD_03.22_Search_Branded_Evergreen` (23685615826) | 4 — concorrentes locais (all seasons professionals, a us air conditioning of texas, ben maines air conditioning, mack and hansen) | 0 → 4 |

### 3. Split de ad group: AC Replace Install → AC Replacement + AC Installation

- Ad group `198093421826` renomeado "AC Replace Install" → **"AC Replacement"** (ficou com as
  keywords de troca: ac replacement x2, new air conditioner, air conditioner replacement, hvac
  replacement, ac unit replacement, new ac unit, new ac unit cost).
- Criado ad group novo `203482277207` **"AC Installation"** (keywords de instalação movidas pra cá:
  hvac installation, ac installation, ac installation near me) com RSA novo (15 headlines / 4
  descriptions, ad id `822815883987`). Criado PAUSED por padrão da skill, ativado depois de confirmar
  geo-targeting da campanha (11 criterios LOCATION via GAQL) e revisar o copy.

### 4. Fix de landing page (4 ad groups da AC Summer)

nappsac.com tem páginas de serviço dedicadas em `/hvac-services/residential/ac-services/` (repair,
installation, replacement, maintenance) que nenhum ad group usava. Final URLs trocadas:

| Ad group | ad id | Nova final URL |
|---|---|---|
| AC Repair | 817739789235 | `.../ac-services/repair/` |
| AC Tune-Up | 817739789646 | `.../ac-services/maintenance/` |
| AC Replacement | 817849043516 | `.../ac-services/replacement/` |
| AC Installation | 822815883987 | `.../ac-services/installation/` |

**Checagem de tracking antes da troca**: baixado HTML bruto das 4 páginas-alvo + homepage.

- **Calls from ads** — dispara pelo call extension do próprio anúncio, não depende da landing page.
  Zero risco.
- **Click to call** — link `tel:903-758-6482` idêntico (mesmo markup) nas 5 páginas. Tracker é
  sitewide, não por página. Zero risco.
- **TSD - Lead form** — o formulário do site não é um `<form>` nativo, é um widget GoHighLevel embutido
  (iframe, form-id `Y0T8AuvseKBX6itJAZju`, "Schedule Service - Activate"). Confirmado embed
  byte-idêntico nas 4 páginas-alvo + homepage (um único widget compartilhado, não uma variante por
  página). Evidência forte de que o listener do GTM (normalmente escopado no widget/form, não na URL
  do pai) continua disparando.
- **Gap**: sem acesso ao container GTM deste cliente (Napps não aparece na MCC GTM da TopServ —
  consistente com a nota acima de ownership ainda não confirmado no Agency Titan), então não deu pra
  inspecionar a configuração literal do trigger. Isso é verificação a nível de markup, não o teste
  formal Verified-Live de integração GHL.

### Aberto (atualizado)

- [ ] Reconferir volume de conversão de Click to call / TSD - Lead form por ad group em alguns dias
  pra confirmar que o tracking sobreviveu à troca de URL (verificação real, já que não tem acesso
  direto ao GTM).
- [ ] `GHL Form Fill` continua zerado — pipeline offline do GHL ainda não investigado/consertado.
- [ ] Confirmar ownership formal da conta no Agency Titan — também bloqueia acesso GTM pra este cliente.
- [ ] Ticket do AM pra registrar por escrito quem pausou `TSD_02.20_PMAX_Plumbing_CoreServices` entre
  08-03 e hoje (mudança não documentada, achada em 08-31) — e decidir se reativa ou mantém pausada.

---

## 2026-09-15 — Snapshot semanal (leitura, sem mudança na conta)

**Executado pelo Claude** (pedido do Edu via chat).

Pull padrão de 7 dias (`insights.py account` + `read.py campaigns` via `tsd.sh`), com trust check de
conversion actions e de network settings antes de reportar.

### Números (últimos 7 dias)

| Métrica | Valor |
|---|---|
| Spend | $1.079,54 |
| CPL | $120,11 |
| CPC | $29,18 |
| Total Conversions | 8,99 |
| Conv Rate | 24,29% |
| Branded Conversions | 8,99 |
| Unbranded Conversions | 0 |
| Branded CPL | $40,53 |
| Unbranded CPL | N/A (0 leads em $715,27 de spend) |
| Impression Share (Search) | 33,02% |

Só as mesmas 2 campanhas ativas de sempre com tráfego: `TSD_03.22_Search_Branded_Evergreen` (11
clicks, $364,27, 8,99 conv) e `TSD_07.21_Search_Nonbranded_AC_Summer` (26 clicks, $715,27, 0 conv).
Resto da conta segue pausado.

### Trust check
- Conversion actions com volume: `Calls from ads` (6,99) e `Click to call` (2,0), ambas
  PHONE_CALL_LEAD — legítimas, sem junk.
- Network settings das 2 campanhas ativas: `target_search_network=False`,
  `target_content_network=False` em ambas, e `ad_network_type` 100% `SEARCH` nos 7 dias — sem
  vazamento pra Search Partners/Display (diferente do padrão sistêmico achado em 08-24 em outras
  contas do book).
- Sem LSA na conta (nenhuma campanha `LOCAL_SERVICES`) — nada a excluir.

### Aberto
- [ ] AC Summer gastou $715,27 sem nenhuma conversão registrada nesta janela de 7 dias — confirmar
  se é só ruído de semana curta ou se o tracking pós-troca de landing page (08-31) parou de
  registrar. Cruza com o item já aberto acima de reconferir Click to call / TSD - Lead form por ad
  group.

---

## 2026-09-15 — Pull de 20 dias: conversões por ação + CPL blended/por campanha (leitura, sem mudança na conta)

**Executado pelo Claude** (pedido do Edu via chat, mesma sessão do snapshot acima).

Janela: 2026-08-26 a 2026-09-14 (20 dias fechados). Query GAQL direta (`segments.conversion_action_name`
e `metrics.cost_micros`/`conversions` por campanha), script `napps_conv_by_action_20d.py` criado nesta
sessão em `scripts/`.

### Conversões por ação (20 dias)

| Conversion action | Categoria | Conversions | All conversions |
|---|---|---|---|
| Calls from ads | PHONE_CALL_LEAD | 12,99 | 12,99 |
| Click to call | PHONE_CALL_LEAD | 4,00 | 6,00 |
| **Total** | | **16,99** | **18,99** |

100% das conversões no período vieram de ligação. `TSD - Lead form` e `GHL Form Fill` seguem em
zero — mesmo padrão já registrado no snapshot de 7 dias acima, agora confirmado também na janela de
20 dias.

### CPL — blended e por campanha (20 dias)

| Campanha | Spend | Conversions | CPL |
|---|---|---|---|
| `TSD_03.22_Search_Branded_Evergreen` | $1.265,08 | 13,99 | $90,44 |
| `TSD_07.21_Search_Nonbranded_AC_Summer` | $2.136,38 | 3,00 | $712,13 |
| **Blended (conta)** | **$3.401,46** | **16,99** | **$200,23** |

AC Summer consumiu ~62% do spend do período por ~18% dos leads — consistente com o diagnóstico de
08-31 (25,5% IS, QS 1-5) e com o item aberto acima sobre o tracking pós-troca de landing page.

### Aberto
- [ ] CPL de $712 na AC Summer nos últimos 20 dias — decidir entre cortar budget da campanha,
  revisitar QS/negativas de novo, ou tratar como sintoma de tracking quebrado (form fill zerado)
  até confirmar qual das duas coisas é.

---

## 2026-09-15 — Rebuild de tracking + troca de URL no Google Ads

**Reportado pelo Edu via chat, não executado pelo Claude nesta sessão.**

Tracking reconstruído e corrigido. Tags antigas desativadas para garantir que não causem disrupção
ou interferência com a configuração nova.

URL dos anúncios no Google Ads também foi trocada.

---

## 2026-09-15 — Split de budget HVAC/Plumbing 50/50 (pedido do cliente)

**Executado pelo Claude** (pedido do Edu via chat, repassando pedido do cliente).

### Contexto

Change history da conta (`change_event`, últimos 30 dias) mostrou só uma mudança de budget: hoje às
08:03, `eduardo@topservdigital.com` cortou `TSD_07.21_Search_Nonbranded_AC_Summer` de $100/dia pra
$1/dia (sem registro anterior neste log — presumivelmente parte do trabalho de rebuild de tracking
reportado acima, não documentado como corte de budget na hora). Nenhuma outra campanha teve budget
ou status alterado nos últimos 30 dias — não havia campanha de Plumbing viva com $50/dia como o Edu
lembrava; o total nonbranded real pré-corte era só os $100/dia da AC Summer (HVAC), sem contrapartida
de Plumbing rodando.

Cliente pediu pra dividir o budget igualmente entre HVAC e Plumbing. Interpretação confirmada com o
Edu: restaurar o total de $100/dia de antes do corte de hoje e split 50/50.

### Mudanças

| Campanha | Categoria | Antes | Depois |
|---|---|---|---|
| `TSD_07.21_Search_Nonbranded_AC_Summer` (24049055193) | HVAC | $1/dia (cortado hoje 08:03) | **$50/dia** |
| `TSD_06.05_Leads_Search_Nonbranded_Plumbing` (23819717682) | Plumbing | PAUSED, $58,40/dia | **ENABLED, $50/dia** |

Escolhida `TSD_06.05_Leads_Search_Nonbranded_Plumbing` como campanha de Plumbing (não uma das outras
~6 pausadas/duplicadas na conta) por ser o par TSD-quality construído no mesmo dia
(`TSD_06.05_Leads_Search_Nonbranded_HVAC` é a equivalente de HVAC, também pausada) — confirmado com
o Edu antes de reativar.

Verificado antes de reativar: 3 ad groups (Drain and Sewer, Leak Detection, Emergency Plumber), todos
ENABLED com ads ENABLED. Bidding strategy das 3 campanhas ativas (Branded, AC Summer, Plumbing) =
Maximize Conversions — confirma que o budget novo vai de fato ser gasto, não fica parado por CPC
manual travado.

`TSD_03.22_Search_Branded_Evergreen` ($60/dia) não foi tocada — branded, não é HVAC nem Plumbing.

Total nonbranded HVAC+Plumbing agora: $100/dia ($50 + $50), igual ao total pré-corte de hoje.

### Aberto
- [ ] Confirmar com o Edu se o corte de AC Summer pra $1/dia hoje de manhã foi intencional (parte do
  trabalho de tracking) ou acidental — ficou sem registro até esta investigação.
- [ ] `TSD_06.05_Leads_Search_Nonbranded_Plumbing` estava pausada há semanas; acompanhar CTR/QS/IS
  nos próximos dias pra confirmar que reativar não trouxe surpresa (keywords/negativas desatualizadas,
  etc.) — não auditado a fundo nesta sessão, só verificado que tem ads live.
- [ ] Segue aberto: CPL de $712/20d na AC Summer (item da entrada de 09-15 acima) — vale reavaliar
  agora que o budget voltou a $50/dia.

---

## 2026-09-24 — Investigação de 6 meses: "gastou mais, receita caiu" (leitura, sem mudança em nenhuma conta)

**Executado pelo Claude** (pedido do Edu via chat, a partir do pedido da AM após a reunião mensal com o cliente).

Cliente disse na reunião que gastou mais em marketing este ano e viu queda de receita, e reconheceu que recusou leads de HVAC nos meses de calor por falta de equipe. Janela: 2026-03-24 a 2026-09-23 vs mesma janela de 2025.

### O que foi lido (só leitura)
- Google Ads PPC `9509605037` (campanhas, ações de conversão por mês, redes, search terms, call_view, change_status, config atual)
- LSA `9239407401` (conta separada, fora do `contas.yaml`): gasto diário, `local_services_lead`, conversas
- Meta `438790276573563` (gasto mensal, campanhas, activity log)
- GA4 `383876275` (sessões por canal, eventos)
- Keyword Planner (Longview TX), Slack, Drive (Media Plan Q3, Fix Plan de call tracking de 09-08)

### Achados principais
- Gasto total (Google + LSA + Meta) $51.948 vs $39.476 (+32%). Meta +$13,4k, Google PPC +$5,8k, LSA −$6,7k.
- PMax Plumbing: gasto foi de $551/semana para $17/semana em 07-05 (impressões −98%) com a campanha ainda ENABLED. Mesmo dia: lista de negativas "TSD - Master Negatives NonBranded (Jul 2026)" (142 termos) anexada a 5 campanhas e 11 critérios da PMax alterados. PMax tem target CPA de $80. Causa não confirmada.
- Custo por conversão contada no não-branded: $107 (04-08 a 07-05) → $380 (07-06 a 09-23).
- Cliente pediu só plumbing em 07-03 e parar anúncios de AC tune-up em 07-22 (Slack). Meta AC tune-up foi desligado em 07-23. Na Google, `TSD_07.21_Search_Nonbranded_AC_Summer` segue ENABLED: $5.024 desde 07-21, ad group AC Tune-Up $1.683 / 8 conv. Não achei reautorização do cliente.
- LSA: leads 499 → 366 (−27%). 62 de 118 leads desde 08-01 com status DECLINED (44/81 em agosto, 29 deles de plumbing). Semana de 08-17 sozinha teve 21.
- CPC da campanha Branded: $13,4 (abr–jul) → $33,7 (ago–set). "napps ac": $3,19 → $54,78. Causa não confirmada.
- Call tracking: CallRail do Napps desmontado (9 números liberados, audit de 09-08), GBP publica a linha do cliente, LSA sem número rastreado. `phone_link_click` no GA4 caiu para 2 em ago e 0 em set (substituído por `phone_click`).
- Tráfego pago no GA4 (Paid Search + Cross-network) −80% em jul–set vs 2025. Orgânico estável (~200/mês).
- Feb–Mar/2026: tráfego lixo da PMax (193k cliques, 4.005 conversões, $665) contaminou o histórico de conversão.

### Não verificado
Receita e jobs (não temos dado). Se as 106 conversões "Calls from ads" da PMax eram ligações reais (call_view não tem linhas de PMax). Causa do colapso da PMax em 07-05 e quem pausou a PMax em agosto. Causa do salto de CPC no Branded. Motivo da queda de volume da LSA e dos leads DECLINED. Qualidade dos leads da Meta. Desvio de conversões para a conta da Supreme (só consta no audit de 09-08).

### Arquivos criados
- `paid/relatorios/napps/napps-6mo-investigation_2026-09-24.md` (relatório completo, com timeline e apêndice mensal)
- `paid/relatorios/napps/napps-investigation-2026-09-24_scripts/` (queries usadas; `h.py` tem o path de saída do scratchpad antigo, ajustar `OUT` antes de rodar de novo)

### Aberto
- [x] Decisão do Edu: pausar ou manter `TSD_07.21_Search_Nonbranded_AC_Summer` enquanto o cliente não confirmar se quer HVAC. **Resolvido 09-30:** o cliente confirmou por escrito que pediu divisão igual HVAC/plumbing em 9/8, então a AC Summer fica ligada (ver entrada de 09-30).
- [ ] Change history na UI do Google Ads: PMax Plumbing de 06-28 a 07-10 e de 08-03 a 08-12 (a API só guarda 30 dias).
- [ ] Auction Insights da campanha Branded, ago–set vs abr–jul.
- [ ] Ticket 07-03 no Agency Titan (confirmação "só plumbing" ao cliente) e qualquer resposta do cliente depois.
- [ ] Via Angela: receita e jobs por mês (HVAC vs plumbing, com fonte do lead) desde jan/2025, e o que "Declined" significa no app da LSA para o cliente.
- [ ] Confirmar se `903-289-7073` (call asset da Google) é uma linha viva e rastreada.
- [ ] Data em que os números do CallRail foram liberados.

---

## 2026-09-30 — Comentários do cliente no relatório de 6 meses (leitura, sem mudança em nenhuma conta)

**Executado pelo Claude** (pedido do Edu via chat, a partir do ticket da AM: "please review comments from the client, highlighted in yellow, please share your feedback").

### Contexto: o cliente comentou numa versão editada, não na nossa
A versão que o cliente comentou é diferente da nossa (`paid/relatorios/napps/Napps - 6-month Review.pdf`, 09-25). Alguém editou antes de enviar. As diferenças são justamente as linhas que o cliente questionou:

| Linha | Nossa versão | Versão que o cliente viu |
|---|---|---|
| 31/08 | "Tightened the **AC** search campaign" | "Tightened the **plumbing** search campaign" |
| 15/09 | "Split **evenly** between HVAC and plumbing" | "Focused **entirely on plumbing**" |
| Next 90 days | "highest intent **AC and plumbing** searches" | "highest-intent **plumbing** searches" |

### Comentários do cliente e o que a checagem mostrou

**1. "Não perdemos ligações"** (3 toques no dispatch, depois todos os telefones do prédio tocam; fora do horário tem answering service).
`call_view` de 2025-03-24 a 09-23: as 41 ligações MISSED têm **todas 0 segundos** e vêm em rajadas de segundos: 06-04, 3 em 13s; 06-17, 5 em 6 min; 06-26, 9 em 15 min às 19h. 25 das 41 são de junho/2025. Todas estão em campanhas antigas, não TSD (Search_HVAC_Repair 17, Search_AC_Maintenance 12, Search_Plumbing 6, Search_Plumbing_GEO 6). Conclusão: são ligações que nunca conectaram (problema de linha/roteamento ou discagem automática), não ligações que a equipe deixou de atender. O cliente tem razão.

**2. Campanha de hiring: "confirmar que foi cancelada, não estamos contratando".**
Meta `438790276573563`: `TSD_Jun04_Hiring_HVAC_Refrigerator` e `TOFU_Hiring_HVAC_Refrigerator_Maintenance_Tech` estão PAUSED. Último gasto em 07-02.

**3. HVAC vs plumbing: "pedimos só plumbing em 6/30 e divisão igual em 9/8, garantam que está igual".**
Conta hoje (GAQL): só 3 campanhas ENABLED, que são `TSD_03.22_Search_Branded_Evergreen` $60/d, `TSD_07.21_Search_Nonbranded_AC_Summer` $50/d e `TSD_06.05_Leads_Search_Nonbranded_Plumbing` $50/d. Gasto de 09-15 a 09-28: HVAC $801 (21 cliques, 1 conv), plumbing $720 (34 cliques, 1 conv), branded $649 (16 cliques, 9 conv). A divisão 50/50 de 09-15 continua valendo e o gasto está equilibrado.

### Achados extras

- **Correção da investigação de 09-24:** `call_view` TEM linhas de PMax. A query antiga selecionava `ad_group.name`, e a PMax (que não tem ad group) caía do resultado sem aviso. PMax de 2026-03-24 a 09-23: 760 ligações, 18 missed, mediana de 24s, 458 com menos de 30s, **124 com 60s ou mais** (abr 51, mai 24, jun 39, jul 10, ago 0). O volume sumiu junto com o colapso da PMax em julho (F2). Os números só de Search no relatório (90 ligações, 2 missed, 55 com 60s ou mais) continuam valendo. Nota de correção adicionada na investigação.
- **De onde vêm as 55 ligações com 60s ou mais (2026):** Branded 31, AC Summer 15, Nonbranded HVAC 5, Nonbranded Evergreen 4, Leads Plumbing 0. Em 2025 foram 25, todas não-branded (14 de plumbing). O Edu decidiu que vale como ganho, porque são ligações reais independente da campanha. Contexto interno: plumbing search foi de 14 para 0.

### Decisões do Edu
- A linha de 31/08 (trabalho na AC Summer) sai do relatório corrigido, sem trocar "plumbing" por "AC". Assim o relatório não fala da campanha de AC que rodou no período só-plumbing (07-21 a 09-08).
- A linha de unanswered sai, e fica "calls over a minute 25 → 55".
- A linha de trazer o hiring de volta sai.
- Os próximos 90 dias foram reescritos para HVAC = plumbing, com LSA como fonte de lead mais barata para os dois.

### Resposta entregue ao Edu para postar no ticket da AM (Angela)

```
Hi Angela, here's my feedback on each comment:

1. Unanswered calls: the 41 calls from last year show up in Google as 0 seconds long, several placed seconds apart. Those calls never connected, so they never reached their phones. It had nothing to do with their team. I rewrote that part of the report without the unanswered numbers (below).

2. Hiring campaign: confirmed, it has been off since July 2. I removed the line about bringing it back.

3. HVAC and plumbing: we are already split equally. Since September 15, HVAC and plumbing search each get $50/day, and spend has been even since then ($801 HVAC, $720 plumbing).

Here is the corrected text for the report:

Calls are lasting longer
Calls from Google search ads lasting over a minute more than doubled, from 25 to 55.

What we've done since July
- Rebuilt conversion tracking on your website and in Google Ads (September 15), so every lead is counted the same way from here on
- Split the search budget equally between HVAC and plumbing (September 15)

Next 90 days
- Connect leads to booked jobs, so we can report cost per booked job by channel each month
- Keep Local Services Ads as the lowest-cost lead source for both HVAC and plumbing
- Keep Google search split equally between HVAC and plumbing, focused on the highest-intent searches for each
- Add cost controls to branded search so more budget goes toward new customers
- Run HVAC and plumbing search steadily for 30 days at equal budgets, for a clean comparison with Local Services Ads

Also, for the next report, can you send me the final version before it goes out? A few lines were changed from my draft, and those were the ones they commented on.
```

### Arquivos
- Queries: `paid/relatorios/napps/napps-review-feedback-2026-09-30_scripts/` (rodar via `./tsd.sh`, o README tem o gotcha do `ad_group`)

### Aberto
- [ ] Edu posta a resposta no ticket da AM.
- [ ] Ter uma resposta pronta caso o cliente pergunte por que teve anúncio de AC em julho–agosto (07-21 a 09-08). Não achei reautorização.
- [ ] Acompanhar HVAC vs plumbing search nos 30 dias de divisão igual (desde 09-15: 1 conv cada, em torno de $750 cada). Plumbing search trouxe 0 ligações com 60s ou mais no ano, contra 14 em 2025.
- [ ] Próximos relatórios: pedir à AM a versão final antes de enviar ao cliente.

---

## 2026-10-05 — Otimização semanal 7 dias (task do Agency Titan): keyword QS 1 pausada + 3 negativas

**Aprovado pelo Edu no chat.** Sem mudança de budget: a divisão igual HVAC / plumbing pedida pelo cliente continua
$50 / $50 (Branded $60 à parte). Script `napps_apply_1005.py` (nesta pasta), tudo conferido por read-back.

**Últimos 7 dias (09-28 → 10-04), só PPC (LSA é conta separada):**

| Campanha | Gasto | Cliques | Conv | CPL |
|---|---|---|---|---|
| TSD_03.22_Search_Branded_Evergreen | $413,18 | 8 | 4 | $103 |
| TSD_06.05_Leads_Search_Nonbranded_Plumbing | $349,93 | 11 | 2 | $175 |
| TSD_07.21_Search_Nonbranded_AC_Summer | $325,80 | 12 | 0 | – |
| **Total** | **$1.088,91** | **31** | **6** | **$181** |

Entrada anterior (09-28): CPL $137, 6 leads. IS da conta 32,4% (52,4% perdido por rank, 15,1% por budget). Conversões:
5 `Calls from ads` + 1 `Click to call`. HVAC $326 vs plumbing $350 na semana, a divisão segue equilibrada.

**Achados:**
1. **Branded ficou caro:** CPC médio $51,65 (semana anterior $25,92). "napps ac" $184,60 em 3 cliques, "napps longview tx"
   $156,19 em 2. As keywords de marca são BROAD em Max Conversions sem teto. O relatório de 6 meses prometeu "cost
   controls to branded search".
2. **AC Summer:** $2.017 em 30 dias para 1 conversão. "ac repair" PHRASE sozinha gastou $1.285 (QS 3, ~$46 por clique).
   E a campanha ainda é de AC de verão em outubro.
3. **Concorrentes:** "benjamin franklin plumbing tyler tx" $72,76 em 2 cliques, sem conv. Holt, Hester, Peter Paul,
   Jack's AC com impressões. Mas "ledbetter plumbing longview texas" converteu 1. Sem regra definida pra Napps, então
   nada bloqueado.

**Feito:**
- Keyword "new air conditioner" (PHRASE, ad group AC Replacement `198093421826`, AC Summer) ENABLED → PAUSED: QS 1,
  $224 / 14 cliques / 0 conv em 30d.
- Negativas PHRASE: AC Summer `24049055193` "store", "scratch and dent"; Plumbing `23819717682` "store" (busca de
  comprar equipamento em loja, "home ac store near me" $23,15).

### Aberto (decisão do Edu)
- [ ] Branded: trocar pra Target Impression Share com teto de CPC (~$8–10), como Zen Air e Watt's Right. Cumpre o
  "cost controls to branded search" do relatório.
- [ ] AC Summer: reconstruir como HVAC de aquecimento (furnace / heater repair) mantendo os $50/d, e decidir o
  "ac repair" PHRASE ($1.285 / 1 conv em 30d).
- [ ] Concorrentes: bloquear os de plumbing que não convertem (Benjamin Franklin etc.) ou manter.

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers (PPC only):** $937.73, 34 clicks, 3 conv, $313 CPL (prior $158.72/7). All 3 = Branded Calls from ads (5 calls, 3 ≥60s); Branded $171.15/5 clicks, $34.23 CPC ('napps ac' $127 for 3 clicks). AC Summer $398.87/12 clicks/0 conv. Plumbing $367.71/17 clicks/0 conv; 'plumber available now' (phrase) $231 matched competitors, 'the mink tyler tx', Tyler/Marshall. KPI Health = Poor.

**Staged, not applied (same as 10-05):** Branded → Target IS with $8–10 cap; AC Summer → heating rebuild at $50/d; plumbing phrase negatives 'the mink', 'detector'; competitor block/keep + is Tyler in the service area.
AT task 93b7ccd8 closed, KPI record e92de0ce.

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-19 — Weekly 7-day pass (Google + LSA + Meta) + 14-day review (Agency Titan tasks, Gui): read-only, all staged

**PPC 10-12..10-18:** $816.13, 1 conv (Branded call). Branded $292.54 / 5 clicks ($58.51 CPC; 'napps longview tx' broad $76/click), overspent 10-14 and 10-16. Plumbing $277.22 / 0 ('plumber available now' phrase $251, matched Benjamin Franklin). AC Summer $246.37 / 0. NB = $1,345 / 0 conv in 2 weeks. HVAC/plumbing split still even. KPI Health Poor.
**LSA 9239407401:** $144.55, 4 message leads, $36.14, 90.5% top / 14.9% abs top.
**Meta 438790276573563:** awareness only $34.62, ARL no cap, ad set = ZIP 75605 only (reach 3,355) → propose expanding geo at same budget.
**14-day (10-05..10-18):** biggest finding = **all plumbing ad groups land on the homepage**, AC on /schedule-now/, while the site has /plumbing/emergency/, /plumbing/leak-detection/, /plumbing/slab-leaks/, /sewer-drain/clogged-drains/, /air-conditioning/repair/, /heating/ (checked 10-19) → point each ad group to its page (likely cause of QS 1–3). Plus the 3-week-old staged items: Branded → Target IS + $8–10 cap; AC Summer → heating; pause 'plumber available now' + 'hvac maintenance' until LPs fixed.
AT tasks eeab3f31 / c2ba367c / 5511cbb3 / 8e9a8687 left open for Gui's review.

## 2026-10-20 — APPLIED the 10-05/10-13 staged changes (Edu: "the staged changes, they are ALL approved")

Script `paid/weekly-7day/staged_1013_apply_2026-10-20.py` (validate first, then live, read-back confirmed). Budgets unchanged (Branded $60, Plumbing $50, HVAC $50).
1. **Branded 23685615826:** Maximize Conversions → **Target Impression Share, 95% absolute top, $10 CPC cap** (was $34 avg CPC).
2. **Plumbing 23819717682:** PHRASE negatives **the mink** ('the mink tyler tx' $36.30) and **detector** (leak-detector tool
   searches $60.97). 0 conv blocked, no keyword conflicts. Tyler IS in the service area (nappsac.com lists Tyler + Lindale), so
   no geo change.
3. **AC Summer 24049055193 → heating**, renamed **TSD_07.21_Search_Nonbranded_HVAC_Heating**, $50/d unchanged:
   - NEW ad groups + 1 RSA each (claims only from nappsac.com, checked 10-20: 24/7 emergency heating, TACLA 72668C, family owned
     since 1957, Bryant factory authorized, upfront flat-rate pricing, financing on replacements):
     Furnace Repair → /heating/furnaces/ (9 kw: furnace repair P+E, heater repair, heating repair, heat pump repair, furnace/heater
     not working, emergency heating repair, furnace repair near me) · ad 828663394462;
     Furnace Replacement → /heating/furnaces/replacement/ (6 kw) · ad 828741722618;
     Heating Maintenance → /heating/maintenance/ (6 kw) · ad 828615169809. All 3 ads in review.
   - PAUSED ad groups AC Tune-Up, AC Replacement, AC Installation; PAUSED 'ac repair' PHRASE ($914 / 1 conv in 30d).
     **AC Repair ad group stays live** (its other keywords + ad), so the campaign keeps serving while heating ads are reviewed.
**Note:** the live AC ads still say "Free Estimates Available"; the site doesn't mention free estimates. Worth fixing later.
⚑ Check heating ad approval 10-21/22, recheck results 10-27 (fu-074).

## 2026-10-20 (later) — Tracking check for the new heating ad groups (read-only)

**Works:** call asset 903-289-7073 APPROVED on TSD_07.21_Search_Nonbranded_HVAC_Heating (Calls from ads, 60s, 27 in 60d).
Headless test on /heating/furnaces/?gclid=TSDtest1020b: gtag loads G-Q9KC7NXEWY + AW-16542555435 (conversion linker, gclid
captured in ccm/collect), and a tel: tap fires 'Click to call' (label ZnW2CJr7qtscEKu6jdA9) via the Google tag's own
link-click rule. Fake gclid, so no real conversion recorded.
**Broken: form fills are not counted in Google Ads, site-wide.** The heating pages (and /schedule-now/) embed the GoHighLevel
form 'Schedule Service - Activate' (iframe link.leadnurturemachine.com/widget/form/Y0T8AuvseKBX6itJAZju, lazy-loaded). Nothing on
the page fires a conversion on submit. 'TSD - Lead form' (WEBPAGE, AW-16542555435/Qxp-CK2BqtscEKu6jdA9) fired once in 60d
(08-25, /contact/); 'GHL Form Fill' (upload) 0.
**GA4 (383876275, linked to this Ads account):** last 60d ghl_schedule_service 7 + ghl_contact_us 1 + ghl_career_form 1 (all
pagePath/source '(not set)', so not attributable), 'lead' 5 (has page + source; 2 of 5 = /careers/). Key events include
ghl_contact_us and ghl_career_form (and page_view) but not ghl_schedule_service; no GA4 import exists in Ads.
**No GTM container on nappsac.com** and no Napps account in TSD's GTM. Podium chat not tracked in Ads.
**Plan (Edu, 10-21, first thing):** create/install a GTM container, add a GHL form listener → 'TSD - Lead form' conversion,
excluding careers; test on /heating/furnaces/. Command Center fu-076.

---

## 2026-10-21 — Correction: form tracking was already in GTM (Edu tested, working)

Edu: the form-fill tracking was already implemented in GTM, and he tested it today; it fires. **The 10-20 entry's "No GTM container on nappsac.com" was wrong:** /heating/furnaces/ loads **GTM-KH7RS4V** (seen in the page source 10-21). The container isn't in TSD's GTM account (same access gap as the 08-03 entry), which is why the 10-20 check found no Napps account. fu-076 closed, nothing to build.
Still worth watching: 'TSD - Lead form' recorded 1 conversion in 60d while GA4 saw 7 schedule-form submits. That may just be few ad-click visitors submitting, but confirm the next real form lead from an ad shows up in Ads (with fu-074, 10-22).

## 2026-10-22 — Heating ads approved + conversion check (fu-074), read-only

**Heating ads:** all 3 (828663394462 Furnace Repair, 828741722618 Furnace Replacement, 828615169809 Heating Maintenance) APPROVED / REVIEWED, ELIGIBLE. First clicks 10-21: Furnace Repair 1 click $20.12, Heating Maintenance 1 click $37.42, 0 conv. Furnace Replacement no impressions yet. Heating and Plumbing campaigns show LIMITED (reason UNKNOWN in the API); Branded LEARNING (new Target IS strategy).
**No counted conversions since 10-12.** Google `call_view` has 5 ad calls after 10-12: 10-14 52s (Heating), 10-15 55s, 10-17 46s, 10-19 7s, 10-21 3s (Plumbing). `Calls from ads` counts 60s+ only, so none counted. CallRail ('Google Ads' source) shows the same 10-14/15/17 calls at 47–56s, all answered, first-time. So tracking works; the calls are just short. `TSD - Lead form`: 0 in the last 30 days.
**Watch:** whether 46–56s ad calls are real bookings (listen in CallRail before changing the 60s rule). Recheck 10-27 (fu-074).

## 2026-10-22 (later) — Non-branded diagnosis, read-only (30d 09-22..10-21)

**⚠ Both non-branded campaigns PAUSED this morning, not by TSD API:** HVAC_Heating 24049055193 at 08:55:48, Plumbing 23819717682 at 08:55:52 (change_status; change_event not showing it yet, so who is unknown). Also Branded keyword edits at 08:02 and a Branded ad added 10-21 19:53. Budgets unchanged ($60/$50/$50). Both spent normally on 10-21. Confirm who paused before doing anything.

**Why non-branded conversions are expensive:**
- Plumbing $1,453 / 55 clk / 3 conv ($484). 'plumber available now' PHRASE = $1,115 (77%), matching competitor names via near-phrase: Benjamin Franklin (~$170), Ledbetter ($120, 1 conv), Holt ($91), Eschberger, Jason's, Roy, Fountain. Matches the CallRail wrong-number calls (Benjamin Franklin, "Lead Better" = Ledbetter).
- Heating/AC $1,509 / 52 clk / 1 conv. 'ac repair' $740 (paused 10-20), 'hvac maintenance' $441 / 0 conv. Competitor terms ~$335 (Chaffin Smith, A C Pros, Wood AC, Veterans Pride, Jack's, Servpro), plus duct cleaning, Athens/Mt Pleasant.
- Competitor terms ≈ $846 of ~$2,960 visible NB spend.
- QS 1–3 on most keywords; landing page experience BELOW AVERAGE almost everywhere, expected CTR below. CPC $26–37.
- Max Conversions, no tCPA, no CPC cap, ~1 conv/month and form fills 0 + ad calls under 60s not counted → bidding has no signal.
- IS 27–28%: lost to rank 39–46%, budget 27–33%.
No changes made.
**Open question:** who paused NB this morning (Edu, teammate, client)? Don't re-enable until known.
**Recommended once the pause is explained (not applied, needs Edu's OK):**
- Competitor brand names as negatives in both NB campaigns (closes the 10-05 block-or-keep question: block; wrong-number calls prove the cost).
- 'plumber available now' PHRASE → EXACT or pause, so Plumbing spreads across real service keywords.
- Both NB → Maximize Clicks with ~$15 CPC cap until there's conversion signal.
- Listen to the 46–56s ad calls in CallRail; if real leads, lower the Calls-from-ads threshold.
- Investigate landing page experience (BELOW AVERAGE): speed + relevance.
**PPC CPA context (Oct 1–20):** $2,709.55 spend / 3 CallRail PPC wins = ~$903; all 3 wins were existing customers, likely Branded ($650), so NB ~$2,060 for 0 wins (unverified per call).

## 2026-10-22 (night) — Who paused the two non-branded campaigns (fu-079)

Change history (change_event 10-21..10-22) answers it: both pauses came from **eduardo@topservdigital.com in the Google Ads web UI** (GOOGLE_ADS_WEB_CLIENT), Heating 24049055193 at 08:55:48 and Plumbing 23819717682 at 08:55:52. Not an outside user. No other changes in that window (the 08:02 branded keyword edit mentioned earlier does not show up in change_event). Only Branded 23685615826 is live (LEARNING). Edu to confirm it was him (or a browser session on his login) and why, before re-enabling.

**Edu (10-22 night):** "I paused those campaigns because they're too expensive and I'll request a couple new landing pages to use in those campaigns." Nonbranded Heating + Plumbing stay paused until the new pages exist; relaunch on the new pages with the 10-22 diagnosis fixes (competitor negatives, 'plumber available now' to exact or paused, Max Clicks ~$15 cap). fu-079 closed.

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

Read-only on all accounts; everything below is staged. 7 AT tasks completed, notes in the task fields + KPI rows (Google 9622f9d5, Meta 2d469ad9, LSA 0b628d2f).

**7-day Google (10-19..10-25):** $510.05 / 19 clicks / 1 conv (CPL $510.05, CPC $26.84; prior $816.13 / 1). Branded $35.40 / 5 clicks / 1 conv, CPC $7.08 (prior $58.51) after the 10-20 Target IS 95% abs top + $10 cap, IS 95.2%, still Learning. NB $474.65 / 0 conv on 10-19..10-21, then paused by Edu 10-22. The 1 conv = 213s Branded call 10-23; 2 NB Plumbing calls 7s/3s. Competitor terms $162 (holt plumbing, wood air conditioning). KPI lead quality Mixed.
**30-day Google (09-26..10-25):** $3,627.92 / 12.98 conv / CPL $279.45 (prior 30d $4,734.45 / 24.01 / $197.22). RSA asset labels all NOT_APPLICABLE (no best/worst). NB LP experience BELOW AVERAGE on most keywords, QS 1-3; /schedule-now/ $1,179 / 0 conv, homepage $843 / 1. NB Heating has no campaign-level sitelinks. NB geo: Tyler $604 + Henderson County towns $543 = 44% of NB spend, 0 conv.
**90-day Google (07-28..10-25):** $11,726.75 / 56.98 conv / CPL $205.79. TSD - Lead form 0 since 08-25, GHL Form Fill 0 in 90d (stalled, tracking test staged for Gui); Click to call last 10-05. Tyler + Henderson County $3,223 / 1 conv in 90d. No ad schedule; 00-05h $365 / 0 conv, Sun $964 / 2. Age 18-34 $592 / 0. No audiences attached.
**LSA 9239407401:** 7d $461.65, 7 charged (6 calls, 1 msg), $65.95 CPL, 43% of 7 x $154.29 = Underspending, top 92.89%. 30d $1,132.67, 34 leads / 18 charged, $62.93, 0 disputes, 17 booked (50%); 19 of 34 leads under bathroom remodeling (mostly existing customers). 10-14 10:26 duplicate septic message charged, not disputed.
- LSA staged: dispute the 10-14 10:26 duplicate; ask AM if bathroom remodeling category should stay on.

**Staged, not applied:**
- NB stays paused until Edu's new LPs (fu-084). On relaunch: 65/35 HVAC/plumbing from 11-01 (fu-092), competitor phrase negatives (holt, wood air conditioning, benjamin franklin, a c pros, the mink), 'plumber available now' to exact/pause, Max Clicks with CPC cap, decide Tyler/Henderson County with the AM, heating sitelinks on the Heating campaign, Heating Maintenance RSA (POOR) fix, NB schedule ~6am-9pm, observation audiences.
- Tracking task for forms (test submit with gclid -> TSD - Lead form; GHL upload).
- Branded: no change; recheck 10-27.

Tasks: [7d Google](https://app.agencytitan.com/tasks/instance/ddc33400-a23c-47b3-871b-05d7abcc4981) · [30d Google](https://app.agencytitan.com/tasks/instance/dc942476-b624-43d9-adba-9698042aa974) · [90d Google](https://app.agencytitan.com/tasks/instance/c5d38c0c-80ff-4076-8f19-a5a0534c41cd) · [7d LSA](https://app.agencytitan.com/tasks/instance/d3ecdf40-d9cf-4f45-ada1-83212681972b) · [30d LSA](https://app.agencytitan.com/tasks/instance/0180df26-e2cb-4542-a328-5e70a37156aa). Meta in meta-ads-log.md.

## 2026-10-27 — fu-074 recheck (read-only, nothing changed)

Script `napps_recheck_1027.py`. Only Branded is live since 10-22 (NB Heating + Plumbing paused by Edu, still paused; no changes since).
So the heating search-term / CPL part of fu-074 moves to the relaunch (fu-084), and the 50/50 spend check is moot.

**Branded on Target IS (95% abs-top, $10 cap, since 10-20), POST 10-20 → 10-26 vs PRE 10-06 → 10-19:**

| | Spend | $/day | Clicks | CPC | Conv | IS / abs-top |
|---|---:|---:|---:|---:|---:|---|
| PRE (Max Conv) | $445.41 | $32 | 12 | $37.12 | 3 | 93 / 93 |
| POST (Target IS) | $11.37 | $2 | 4 | **$2.84** | 2 (1 ad call, 1 click-to-call) | 94 / 56 |

- CPC fell ~93% with brand IS held at 94%. Abs-top 56% (cap $10 loses the very top on a few auctions); brand volume is tiny (1–18 impr/day),
  so not worth raising the cap. Still LEARNING. Budget $60/d mostly unused, by design.
- Search terms all brand (napps ac, napps ac longview tx, napps cooling heating & plumbing). 'mink plumbing tyler tx' 1 impr, 0 clicks.
- The one real call (10-23 15:56, 214s, CallRail "first-time") was an **existing customer** chasing a pending repair (waiting on a blower
  motor). Not a new lead. Same pattern as Oct 1–20 (all 3 PPC wins were existing customers). See call-wins-log 10-23.

**Short ad calls question (from 10-22) closed:** the 46–56s ad calls on 10-14 / 10-15 / 10-17 were 2 wrong numbers (another Athens HVAC co,
Benjamin Franklin) + 1 Saturday answering-service "are you open". The 60s Calls-from-ads rule loses nothing; keep it.

**Account is effectively dark:** PPC spent **$289 in 7 days, $278 of it on 10-20/21 before the NB pause**; since 10-22 it's ~$2/day vs
$160/day budgeted. No new-customer lead from Google PPC since at least 10-01. Relaunch depends on the new landing pages (fu-084, 10-29),
and the client's 65/35 split starts 11-01 (fu-092). If NB is still paused on 11-01, the AM should know the split has nothing to apply to yet.

## 2026-10-27 (later) — Non-branded RELAUNCHED on the 2 new landing pages (Edu's go, fu-084)

Edu: "We have these two landing pages... implement them in the campaigns we paused and turn them on again", then "Move forward with your
additions and then go ahead and publish the campaigns". Script `napps_relaunch_1027.py` (validate-only, then `--apply`, read-back confirmed).

**Pages checked before launch (10-27):** https://nappsac.com/furnace-heating-repair-in-longview/ and
https://nappsac.com/emergency-plumber-in-longview/ both HTTP 200, noindex (fine for ads), load GTM-KH7RS4V + gtag AW-16542555435 +
G-Q9KC7NXEWY, tel: = 903-758-6482 (main line; taps counted by the gtag link-click rule). New GHL forms 41itmOgyyvmnwOP5aBfa (heating) and
9mZSVwSVyFxgDqp4cR0V (plumbing), both on link.leadnurturemachine.com. The GTM listener (public gtm.js) catches any GHL form from that origin
with an email ('set-sticky-contacts' → `ghl_form_submit` → 'TSD - Lead form' Qxp-CK2BqtscEKu6jdA9), so the new forms should count.
**Not tested with a real submit** (would create a fake GHL lead): one test + Mo's Verified Live before telling the client the pages are live.

**Applied (NB total $100/d unchanged, now 65/35 per the client's 10-23 request; Branded untouched):**
| | Heating 24049055193 | Plumbing 23819717682 |
|---|---|---|
| Budget | $50 → **$65** | $50 → **$35** |
| Bidding | Max Conv → **Max Clicks, $15 CPC cap** | same |
| Live ad group | **Furnace Repair** only (ad 828663394462 → new heating page) | **Emergency Plumber** only (ad 807944988879 → new plumbing page) |
| Paused ad groups | AC Repair, Heating Maintenance, Furnace Replacement (page is repair-only, no AC page) | Drain and Sewer, Leak Detection (page is emergency-only) |
| Keywords | — | 'plumber available now' PHRASE PAUSED (77% of spend, matched competitors); EXACT stays |
| New PHRASE negatives | chaffin smith, a c pros, wood air conditioning, alford pace, veterans pride, servpro, jack's ac, walker heating | benjamin franklin, ledbetter, holt plumbing, eschberger, jason's plumbing, roy the plumber, fountain plumbing |

**Eagle Point Roofing cleanup (Edu: old TSD client, exclude not just pause):** the account had 5 Eagle Point sitelink assets. 2 were live-linked
('Our Locations' 346848030215, 'About Us' 346848030218, both → eaglepointroofingtx.com) on Plumbing AND on the old paused
TSD_06.05_Leads_Search_Nonbranded_HVAC 23819634471. All 4 links REMOVED; 0 at ad group / account level. The other 3 (Fence Repair, Fence
Installation, Roof Repair) were already unlinked. Assets can't be deleted via the API, so the 5 sit orphaned and serve nowhere.

**After launch:** both campaigns ENABLED (Heating LEARNING, Plumbing LIMITED), both ads back in review after the URL change.
**Expect** underspend at first (one ad group each, $15 cap vs $26–39 CPCs before) and fewer clicks; that's the trade for cutting waste.
**Next:** ad approval 10-28; first-week read 11-03 (fu-099); actual HVAC/plumbing spend split vs 65/35 (fu-092).

## 2026-11-03 — fu-099 + fu-092: first week of the relaunched Nonbranded (read-only, nothing changed)

**Window:** 10-28 → 11-02 (6 days). Script `napps_recheck_1103.py` + CallRail pull (company COM4cd8…, 5 calls 10-28 → 11-03).
No account changes since Edu's 10-27 relaunch batch.

| | Budget | Spent (per day) | Clicks | CPC | IS / rank-lost | Leads |
|---|---:|---:|---:|---:|---|---:|
| NB Heating | $65 | $62.46 ($10) | 5 | $12.49 | 30 / 70 | 0 |
| NB Plumbing | $35 | $14.39 ($2) | 1 | $14.39 | 33 / 67 | 0 |
| Branded | $60 | $26.54 ($4) | 3 | $8.85 | 95 / 5 | 0 new |

- **Ads approved** (828663394462 heating, 807944988879 plumbing), both on the new pages.
- **Underspend: NB spent $77 of $600 (13%).** Rank-lost ~70% on both. The $15 cap sits under the market (CPCs were $26–39 before) and
  quality scores are low: core keywords QS 1–5, landing page experience still BELOW AVERAGE on every rated keyword (Google's rating lags a new page,
  so this can still move). Search volume is there: heating got 260 impressions, mostly real furnace-repair intent ("furnace not turning on",
  "furnace running but no heat", "furnace not igniting"), but we win few auctions.
- **65/35 split (fu-092):** budgets are set 65/35, actual spend 81/19. Meaningless while neither campaign spends its budget.
- **Clicks:** "how much for hvac service call" $14.81, "heater repair" x2, "heating repair" x3, "plumber near me" $14.39. All 6 clicks came from
  Tyler (2), Daingerfield (2), Frankston (1), Gun Barrel City (1): none from Longview. Tyler is in the service area (site lists it); the other three are fringe.
- Competitor impressions, no clicks: chris cooling tyler tx, coy dodd air conditioning tyler texas, c woods ac, e d miller service company.
- **Leads: 0 from Nonbranded** (no forms, no ad calls). Branded's 3 ad calls (10-29 513s, 10-30 65s, 11-02 289s) are one repeat caller from
  Fort Collins CO (970), CallRail "repeat" = existing contact, not a new lead; Google didn't count them either.
- Forms on the new pages are still untested with a real submit, and Mo's Verified Live is still owed before telling the client the pages are live.
- Account total ~$17/day vs $160/day budgeted.

**Proposed (needs Edu's go; budgets unchanged, so no client approval):**
1. Max CPC cap $15 → $25 on both NB campaigns (still under the old $26–39 CPCs), recheck in a week.
2. One test submit on each new page (heating + plumbing) to confirm 'TSD - Lead form' fires, then Mo's Verified Live.
3. Tell the AM: the 65/35 split is set, but Google is barely spending (~$17/day of $160) while the new pages earn quality score.

## 2026-11-03 (later) — APPLIED cap $15 → $25; ⚠ new-page forms can't be counted (GTM listener needs an email)

Edu: "Yes, work on the three topics you brought up."

**1. Applied:** `napps_cap_1103.py`, validate-only first, then `--apply`. Max Clicks CPC cap $15 → **$25** on NB Heating 24049055193 and
NB Plumbing 23819717682. Read-back: both $25, budgets $65 / $35 unchanged, both ENABLED.

**2. Test submit: NOT done, because the tracking can't work yet.** Checked before submitting (headless, no submit):
- The new GHL forms (41itmOgyyvmnwOP5aBfa heating, 9mZSVwSVyFxgDqp4cR0V plumbing) ask only **full name, phone, ZIP**. No email field.
  Both have Cloudflare Turnstile (a headless submit would likely be blocked anyway).
- The live GTM-KH7RS4V listener (public gtm.js, read 11-03) only pushes `ghl_form_submit` when the GHL payload has an email:
  `a&&a.email&&(window.dataLayer.push({event:"ghl_form_submit",...}))`. So a form fill on either new page never reaches 'TSD - Lead form'
  (Qxp-CK2BqtscEKu6jdA9). The 10-27 entry assumed "with an email" was fine; it isn't for these forms.
- **Fix (UI only):** GTM-KH7RS4V is not reachable with TSD's GTM API token (no Napps account among the 82 it sees). In the Custom HTML listener
  tag change `a&&a.email&&(` to `a&&(a.email||a.phone)&&(`, publish, then one test submit per page in GTM Preview (GPC + ad blocker off)
  and confirm 'TSD - Lead form' fires. Then Mo's Verified Live (lead lands in GHL).
- Side check: raw HTML of both pages still loads GTM-KH7RS4V + AW-16542555435 + G-Q9KC7NXEWY. Headless Chromium gets a page without them
  (bot variant), so headless tag tests on nappsac.com aren't reliable; use a real browser.

**3. AM note:** drafted for Edu (spend barely moving, cap raised, form tracking fix this week). No AM name on file in the workspace.

## 2026-11-04 — Quick check after the $25 cap (read-only)

- Cap change landed 11-03 10:41 (account time). NB 11-03: Heating $52.60 / 4 clicks, Plumbing $22.61 / 1 click = **$75.21**, vs ~$13/day in week 1.
  The plumbing click ($22.61, "plumbers near me") cleared the old $15 cap. Rank-lost Heating 78% (11-02) → 60%. 11-04 has no spend yet (early hours).
- Clicked terms: plumbers near me, heat pump compressor replacement cost (price research), hvac near me. 0 leads; Branded ad call 11-03 58s (under the 60s rule).
- **GTM-KH7RS4V still v20, listener still requires an email** (gtm.js size changed only from Google's library). New-page form leads still can't count (fu-121).

## 2026-11-04 — Cowork first-visitor test (Edu): new-page form leads do NOT count in Google Ads (confirmed)

Edu tested 11-04 ("tracking is working fine"), likely in a browser with an older GHL sticky contact. Cowork re-ran it as a first-time visitor
(nappsac.com + link.leadnurturemachine.com storage empty), Tag Assistant on GTM-KH7RS4V, page 1 only (furnace-heating-repair-in-longview):
- Submit 11-04 09:19:17 BRT (12:19:17 UTC), GHL contact **bHJnE5kJ0IQxAqQK4U5r** "TSD TEST - please ignore", source "Heating Landing Page" (delete in GHL).
- set-sticky-contacts payload: full_name, first/last, phone +19035550100, postal_code, source, location_id. **No email key.**
- '00 | cHTML - GHL Form Listener' was loaded, but **no ghl_form_submit**, **'TSD - Lead form' (Qxp-CK2BqtscEKu6jdA9) did not fire**, no conversion request.
- Inline thank-you, no redirect, no captcha.
- Side flag: Cowork typing (903) 555-0100 into the phone field left 35550100 (leading "90" dropped); only +19035550100 entered correctly. May be an automation
  artifact; check by hand on mobile, since 903 is Longview's area code.
- Page 2 (emergency plumber) skipped: same listener, same field set, same result expected; test both after the fix.

**Fix still owed (Edu, GTM UI):** listener `a&&a.email&&(` → `a&&(a.email||a.phone)&&(`, publish, re-test first-visitor on both pages (fu-121).

## 2026-11-04 (later) — Listener fix PASSES in GTM Preview (not yet published)

Edu edited '00 | cHTML - GHL Form Listener' in GTM-KH7RS4V: `if (!contactData || !contactData.email) return;` →
`if (!contactData || !(contactData.email || contactData.phone)) return;`. Cowork re-test on the heating page in Preview (09:25:22 BRT, same contact
bHJnE5kJ0IQxAqQK4U5r, payload still no email): ghl_form_submit fired (#33), '03 | G.Ads - Lead Form' (label Qxp-CK2BqtscEKu6jdA9) sent to
googleadservices, plus '03 | G.Ads - User-Provided Data' and '03 | GA4 - Lead Form'. Plumbing page not tested (same listener).
- **Live is still v20 until Edu publishes.**
- Test hit had no gclid, so Google Ads won't attribute it; GA4 may show 1 test lead.
- ⚠ Cowork: the site's WP Rocket delays GTM until the first scroll/click on the page. Clicks inside the GHL iframe don't count as page interactions,
  so a visitor who lands, clicks straight into the form and submits may never load GTM: lead lost AND gclid not stored. Fix = web dev excludes
  GTM (googletagmanager.com / GTM-KH7RS4V inline snippet) from WP Rocket "Delay JavaScript execution". Not tested yet.
- 11-04: AT Internal Request **fa6ddeb9-7a1b-4600-a87e-8393e3356134** "Napps: Google Ads update on the new landing pages" created as a DRAFT (Intake, not submitted)
  for Edu to review: Intake + Review & Close = Edu, Execution = Angela (Napps' assigned AM in AT). FYI only (pages live since 10-27, 65/35, week-1 spend, cap raise, phone-only form fix).

---

## 2026-11-06 — LSA → Pay-per-lead PMax migration: exposure check (read-only, NOT migrated yet)

Napps LSA `9239407401` is still classic LSA (Max Conversions). It's multi-trade (leads 08-08..11-06: plumber 80 / HVAC 40 / bath remodel 24),
but NO per-trade target is set (target_cpa_bid_micros = 0 on all three; manual bids $50/$22/$23 are leftovers ignored under Max Conv).
So the "one campaign-level target" change shouldn't move anything here when it switches.

**Context:**
Google (not TSD) is moving LSA into a new campaign type, "Pay-per-lead PMax". It creates a PERFORMANCE_MAX campaign
(`Pay-per-lead-PMax-<business>`, Max Conversions, same daily budget as the old LSA, one asset group `xcat:service_area_business_<trade>`)
and pauses the old `LocalServicesCampaign:SystemGenerated`. Still billed per valid lead, still Search + Maps only, badge carries over.
What changes: no manual bidding, one campaign-level target instead of one per trade, weekly budget becomes a daily average, old LSA
dashboard reports don't migrate (lead history does). Sweep of all 57 enabled MCC accounts on 11-06: 7 switched on 11-03/11-04
(Watt's Right, Amazing Morrow, Golden, Gray Duct, King's Window, Nick's, Spencer). Full write-up: `_contexto/memoria/tsd-lsa-ppl-pmax-migration.md`.

Data notes: `local_services_lead` still returns leads after the switch (lsa_report.py lead data OK). Spend/metrics now sit on the
PMax campaign, so anything filtering on channel LOCAL_SERVICES (google_channels.py) misses them. **$0 spend ≠ dark**: only charged
leads cost money, clicks are free. Judge delivery by impressions + leads per day.

## 2026-11-10 — fu-120: week 2 of the relaunched Nonbranded after the $15 → $25 cap (read-only, nothing changed)

**Window:** 11-03 → 11-09 (7 days; the cap went live 11-03 10:41, so ~all of it at $25). Scripts `napps_recheck_1110.py` (+ `b`/`c`/`d` follow-ups)
and CallRail company COM4cd8 (30 calls 10-28 → 11-10). Leads judged on calls + CallRail only (Edu: form tracking treated as broken until fu-121 closes).
No account changes since 11-03 10:41 (change_event).

| | Budget/day | Week 2 spent (per day) | % of budget | Clicks | CPC | IS | Rank-lost | Week 1 (6d) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| NB Heating | $65 | $410.85 ($59) | 90% | 20 | $20.54 | 37 | 63 | $62 / 5 clk / IS 30 / rank-lost 70 |
| NB Plumbing | $35 | $221.97 ($32) | 91% | 10 | $22.20 | 40 | 51 (+10 budget-lost) | $14 / 1 clk / IS 33 / rank-lost 67 |
| Branded | $60 | $38.95 ($6) | — | 7 | $5.56 | 85 | 15 | $27 / 3 clk |

- **Spend fixed:** NB $633 vs $77 in week 1. Split **65/35 exactly** (fu-092 OK now that both spend). Daily is lumpy (Heating $0 on 11-06, $139 on 11-04).
- **Rank-lost still high:** 63% / 51%, abs-top 18% / 16%. Better than week 1 (~70%), not solved. Raising the cap again won't fix it cheaply: QS is the lever.
- **Landing page experience: still BELOW AVERAGE on every rated keyword** (emergency plumber QS 5, plumber near me QS 1, emergency plumber near me QS 2,
  furnace repair / heater repair / heat pump repair QS 3, furnace repair near me QS 2). Ad relevance is ABOVE AVERAGE on the core terms, eCTR mostly below.
  Only 'plumbing repair near me' shows LP AVERAGE (0 impressions). Two weeks in, Google's rating of the new pages hasn't moved.
- **Leads (calls + CallRail): 0 verified from Nonbranded.** Cumulative since the 10-27 relaunch: $710, 36 clicks, 0.
  - call_view week 2: only Branded (11-03 58s from the Fort Collins repeat caller, 11-05 missed). No NB ad call.
  - CallRail "Google Ads" number 903-289-7073: 4 calls in 14 days, all the same Fort Collins repeat caller (Gilbert, Sabina). 0 new.
  - Google counted **1 'Click to call' conversion on NB Plumbing** (11-04, 2 pm, mobile, "plumbers near me" via 'plumber available now' EXACT).
    That action is type CLICK_TO_CALL = a TAP on the call button, not a call. No matching call_view row and nothing on 289-7073 that day → **tap, no call. Not a lead.**
    It is primary + biddable in the PHONE_CALL_LEAD/CALL_FROM_ADS goal, so Max Clicks ignores it but the account's conversion column overstates NB.
  - The other 26 CallRail calls are all GBP (903-522-5601), not ads.
- ⚠ **Measurement blind spot (new):** both new pages show the main line **903-758-6482** (tel: links + text, raw HTML) = CallRail's destination number,
  not a tracking number. CallRail's website-session tracker "Paid Search (Google Ads)" is **DISABLED** and GTM v21 loads no CallRail script, so a visitor
  who lands on the new page and taps the phone number calls the shop directly: **no CallRail record, no Google Ads conversion.** "Calls + CallRail" only
  sees the ad's call button (asset 343446389771 = 903-289-7073). So 0 measured NB calls ≠ 0 calls. The old "Homepage Calls" session tracker is disabled too.
- **fu-121 status:** live GTM-KH7RS4V is **v21** and its listener reads `email||a.phone` → the fix is published (matches fu-121 note 11-04).
  0 'TSD - Lead form' conversions on NB in week 2. Not proof of 0 forms: no first-visitor LIVE test on record yet, WP Rocket still delays GTM, Mo's Verified Live still owed.
- **Search terms (visible ≈ $162 of $633; Google hides the rest):**
  - Plumbing: **"streety plumbing marshall texas/tx" (competitor) $69.86 / 3 clicks via 'emergency plumber' PHRASE** = 31% of visible plumbing spend.
    'plumbers near me' $69.51 / 3 clicks (1 = the tap). 'plumber available now' EXACT $80 / 4 clicks, matching "plumbers near me".
  - Heating: **water-heater queries on the furnace page** ("gas hot water heater not working" $24.97, "water heater pilot light not lighting" $24.12) via 'heater not working' PHRASE.
    'hvac near me' $28.97 via 'heating repair' PHRASE; "heat pump compressor replacement cost" $14.73 (price research). Competitor impressions with no clicks (2 amigos, c&r, chris cooling, adams air).
- **Geo (clicks, location of presence):** Heating: Tyler 6 ($106), Gilmer 3, Big Sandy 3, Marshall 3, Kilgore 2, Longview 2, Seven Points 1.
  Plumbing: Longview 4 ($93), Athens 2, Marshall 1, Tyler 1, Hallsville 1, Gun Barrel City 1. **Longview now 6 of 30 clicks** (0 of 6 in week 1).
  Far southwest fringe (Athens, Gun Barrel City, Seven Points) = $83 / 4 clicks.
- Side note: GBP calls are busy (26 in 14 days, 1 tagged "Schedule booked" 11-09). Not an ads result.

**Read:** the cap raise did its job on delivery (13% → 90% of budget, exact 65/35), but $633 bought 30 clicks and 0 measurable leads, and the landing page is still
rated BELOW AVERAGE. 30 clicks is too few to call it a fail, and calls from the page itself can't be seen. Fix the measurement before judging week 3.

**Proposed (needs Edu's go; budgets unchanged, so no client approval):**
1. Put a CallRail tracking number on the 2 new pages (enable a website-session/DNI tracker for Google Ads visitors, or at least a static source number
   on these 2 pages), so page calls count. CallRail UI only (API is GET-only for us).
2. Negatives: 'streety' PHRASE on Plumbing; 'water heater' PHRASE on Heating (furnace page doesn't sell it; plumbing page is emergency-only).
3. 'Click to call' (7707737498, taps) → secondary, same fix as Integrate Comfort 11-04, so taps stop showing as conversions.
4. Geo: confirm whether Athens / Gun Barrel City / Seven Points are in Napps' service area; if not, exclude them.
5. Hold the $25 cap and budgets for week 3. LP experience is the QS lever: page speed (WP Rocket) + message match, ask web dev.
Next read: fu-144 (11-17).

## 2026-11-10 (later) — APPLIED recs 2-5 (Edu: "Apply 2-5"); rec 1 (CallRail on the pages) → Cowork recon first

`napps_apply_1110.py`, validate-only first, then `--apply`, read-back confirmed:
2. PHRASE negatives: **'streety'** on NB Plumbing (blocks the 2 "streety plumbing marshall" terms, $69.86, 0 conv in 30d) and **'water heater'** on NB Heating
   (blocks 24 terms in 30d, $49.09, 0 conv). No keyword conflicts.
3. **'Click to call' 7707737498 (CLICK_TO_CALL taps) → Secondary**, account-wide (primary False, include_in_conversions False). 90d taps: Branded 15, NB 8.
   No enabled campaign bids on conversions (Branded Target IS, NB Max Clicks), so this only cleans reporting. Use all_conversions across this date.
4. **Geo: the "fringe towns" were a county target.** Both NB campaigns targeted **Henderson County TX** (9059512), which holds Athens, Gun Barrel City, Seven Points,
   Chandler and Eustace; none are on nappsac.com/service-area/. Henderson the town (Rusk County), which IS on the service-area page, wasn't targeted on NB
   (Branded has it). Swapped on both NB: county **removed**, **Henderson city 1026468 added**. Still 11 locations each, PRESENCE only.
5. Cap $25 and budgets $65 / $35 held (asserted by the script, not written). Landing-page experience fix = web dev via AM, not sent.

**Rec 1, CallRail on the new pages (fu-146), API facts gathered:** company script `//cdn.calltrk.com/companies/336278805/1286f50050a4f3ac8e79/12/swap.js`,
dni_active false; "Paid Search (Google Ads)" session tracker disabled since 2023-05-15, 0 numbers; **CallRail Google Ads integration for Napps = 'pending' with
no customer selected** (so even gclid calls can't upload to 9509605037). Active trackers: GBP 522-5601, LSA 289-6340, Google Ads call asset 289-7073, Organic Social 320-4458.
Cowork recon prompt (read-only: plan/cost, old tracker, 903 availability, integration, GTM CallRail tags, live page swap test, WP Rocket delay):
`clients/napps/cowork-callrail-recon-1110.md`. Decision after recon (Edu): session pool (gclid → uploads) vs one source tracker.

## 2026-11-10 (later 2) — Cowork CallRail recon results (read-only, nothing created; fu-146)

- **Plan:** Call Tracking Intelligence Advanced $185/mo, 20 numbers included, account at **172 numbers** → extra local number **$2.50/mo**. 2,500 min included,
  2,275 used (near the cap), $0.05/extra min. Toll-free +$5/mo.
- **Old "Paid Search (Google Ads)" session tracker:** can't be re-enabled (greyed out, "Unavailable"). A new one is needed.
- **903 numbers:** available (wizard offered 903-708-8425 for a single Google Paid tracker; NOT bought, wizard left unconfirmed). Pool not checked.
- **CallRail → Google Ads integration:** Pending, no account selected. **Requires an active website (session) pool first.** 9509605037 "Napps Cooling, Heating & Plumbing"
  is in the dropdown. Finish = pool → select account → call conversion settings → Activate. So a single source tracker would show page calls but could never upload them.
- **GTM-KH7RS4V:** not visible to eduardo@topservdigital.com (only G-Q9KC7NXEWY and AW-16542555435 show). The 11-04 listener edit was made under another login; retry as that one.
- **Live pages:** 903-758-6482 everywhere (8 tel: links per page), no calltrk/callrail request, no CallRail script in the source. First-visitor state not proven, but the script is absent from the HTML.
- **Site:** WordPress + Elementor 4.3.6 + WP Rocket 3.24, delay-JS markup on both pages; no WP admin access; web contact not identifiable from the site.

**Rec (Edu decides):** new session tracker, Google paid visitors only, smallest pool CallRail allows (~4 numbers ≈ $10/mo on TSD's CallRail bill), swap target 903-758-6482;
swap.js via a GTM-KH7RS4V Custom HTML tag (no WP access); then finish the Google Ads integration on 9509605037 (count first-time calls 60s+). Caveat: WP Rocket delays
GTM until the first interaction, so a visitor who taps the number before scrolling dials the unswapped main line. Ask the web dev (via Angela) to exclude GTM from the delay.

## 2026-11-10 (later 3) — Decision: reuse 903-289-7073 on the new pages (no new CallRail numbers); AT task for the web dev

Edu: no extra CallRail charge. The web dev swaps 903-758-6482 → **903-289-7073** (existing "Google Ads" CallRail number) on both new pages, text + all tel: links,
only on those 2 pages. Visibility only (no Google Ads upload without a session pool; fine while NB is on Max Clicks). Page calls = CallRail "Google Ads" calls
minus Google call_view (call-button) calls. Also asked: exclude googletagmanager.com from WP Rocket "Delay JavaScript execution".
AT Internal Request created via the AT web UI (connector was signed out), left in **Intake, not submitted**; Edu assigns the web dev himself (not Angela):
https://app.agencytitan.com/tasks/instance/33c671b4-ea17-450c-8c13-9c254e531475
- 2026-11-10: Edu **submitted** the AT task 33c671b4 and assigned it to the web dev. Next: when it's done, check both pages show 903-289-7073 (text + tel: links), then count page calls in the fu-144 read.

## 2026-11-11 — Landing-page number swap VERIFIED LIVE (AT 33c671b4, Sha)

Checked both pages by curl 11-11 ~13:00 BRT:
- /furnace-heating-repair-in-longview/ and /emergency-plumber-in-longview/: **903-289-7073** appears 7x in visible text and in all **8 tel: links** per page; **0** tel:9037586482 left.
- The only remaining "(903) 758-6482" is the site-wide JSON-LD schema `telephone` (HVACBusiness/Plumber NAP). Correct, leave it: schema carries the main line, not a tracking number.
- GTM-KH7RS4V snippet now loads as a plain `<script>` (0 `rocketlazyloadscript` tags on the page; WP Rocket still delays 19 other scripts via data-rocket-src). So the GTM delay ask is done too.
- Sha's execution note: "The phone number has been updated, and GTM has been excluded from JS delay." Review notes written; AT close pending Edu (classifier blocked the write).
- Next: confirm in CallRail that 903-289-7073 is reporting calls from these pages (fu-144 read 11-17), and that CallRail's Google Ads integration can now attribute them.

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

Read-only on all accounts; everything below is staged. 4 AT tasks completed (7d Google, 14d Google, 7d LSA, 7d Meta), notes in task fields + KPI rows (Google ce40864e, LSA d80f4e3f, Meta 189d2e21).

**Edu relaunched NB 10-27 09:38 (API, not logged here before):** both NB campaigns enabled, Max Clicks $15 CPC ceiling, budgets HVAC $65/d + Plumbing $35/d (= the client's 65/35 split from 11-01; Branded $60 separate), 15 campaign negatives (holt plumbing, wood air conditioning, a c pros etc.), ad URLs swapped, 4 campaign assets removed. Live NB ad groups: Furnace Repair -> /furnace-heating-repair-in-longview/, Emergency Plumber -> /emergency-plumber-in-longview/; all others paused.

**7-day Google (10-27..11-02):** $103.39 / 9 clicks / 0 counted conv, CPC $11.49, IS 32.42% (prior $289.19 / 2 conv). Branded $26.54 / 3 clicks, IS 91%. **3 Branded ad calls 60s+ (513s 10-29, 65s 10-30, 289s 11-02) recorded 0 conversions** (all_conversions 0 too; last counted Calls from ads 10-23; account call reporting -> Calls from ads 60s). NB HVAC $62.46 / 5 clicks, NB Plumbing $14.39 / 1 click, both 0 conv, rank-lost ~70%, budget-lost 0; actual spend split 81/19. **100% of NB spend outside Longview** (Tyler $27.14, Daingerfield $20.51, Frankston $14.81, Gun Barrel City $14.39). KPI health Mixed.
**14-day (10-20..11-02):** $392.58 / 21 clicks / 2 conv (Branded), prior 14 $1,837.35 / 2.99. QS: plumber near me EXACT 1, furnace repair near me 2, furnace repair 3. Furnace Repair RSA AVERAGE, Emergency Plumber EXCELLENT. No audiences. Open recs: 51 KEYWORD, sitelinks x2, search partners x3, Max Conv, PMax, lead form.
**LSA 9239407401 (7d):** $130.12, 3 charged (1 call, 2 msg), CPL $43.37 (prior $386.65 / 6 / $64.44), 12% of 7 x $154.29 = Underspending, top 92.91%. 10-28 faucet message charged + DECLINED (no dispute), 11-02 water heater message NEW, 10-20 declined call dispute PENDING.

**Staged, not applied:**
- Check the 3 uncounted Branded 60s+ calls in the UI (Calls from ads) before judging NB.
- Ask the AM whether Tyler / Daingerfield / Frankston / Gun Barrel City are served; if not, narrow NB to Longview core.
- Test-submit both new LPs with a gclid (forms 0 since 08-25).
- Heating/plumbing sitelinks on the NB campaigns; heating headlines for the Furnace Repair RSA; observation audiences; reject KEYWORD / partners / Max Conv / PMax / lead form recs.
- After 2 weeks of relaunch data: if still rank-limited with 0 budget-lost, consider a higher CPC ceiling on HVAC only. Budgets stay 65/35.
- LSA: dispute the 10-28 faucet message if not a real job; confirm a human reply on the 11-02 message.
- Revisit 2026-11-10 (7-day) and 2026-11-17 (14-day).

Tasks: [7d Google](https://app.agencytitan.com/tasks/instance/6585c753-cd79-4144-9131-41ede48d1978) · [14d Google](https://app.agencytitan.com/tasks/instance/32222056-c32c-4add-8195-2883a53911f4) · [7d LSA](https://app.agencytitan.com/tasks/instance/bed364a8-9742-4769-90d4-d70f3cbe5dc3). Meta in meta-ads-log.md.

## 2026-11-09 — AT optimization tasks (Gui, via Claude)

Read-only on all accounts; everything below is staged. 3 AT tasks completed (7d Google, 7d LSA, 7d Meta), notes in task fields + KPI rows (Google fef0f465, LSA fc5f758f, Meta 09a4cb0a).

**Edu 11-03 10:41 (API, not logged here before):** Max Clicks CPC ceiling $15 -> $25 on both NB campaigns. Budgets unchanged (HVAC $65, Plumbing $35, Branded $60).

**7-day Google (11-02..11-08 vs 10-26..11-01):** $574.24 / 33 clicks / 1 counted conv (prior $88.53 / 9 / 1), CPC $17.40, IS 37.32%. NB $528.86 / 26 clicks, CPC ~$20 (was $12.49); IS barely moved (HVAC 32.7 -> 35.1%, Plumbing 30.9 -> 39.4%), rank-lost 65% / 51%. The 1 conv = 'Click to call' website tap on the Emergency Plumber LP 11-04 (Longview), no matching Google Ads call in CallRail. Branded $45.38 / 7 clicks, CPC $6.48, IS 86.2%; 3 ad calls (11-02 289s, 11-03 58s, 11-05 missed). CallRail: the 2 answered calls on call-asset number 903-289-7073 are both repeat callers. 0 verified new PPC leads. KPI health Poor.
- Branded 60s+ calls still 0 conv (10-29, 10-30, 11-02). API: asset 903-289-7073 on all 3 campaigns uses the account-level action = 'Calls from ads' (60s, primary); account call reporting on. Cause not visible in API. HVAC Heating's 'calls from ads' goal is not biddable (Branded + Plumbing are).
- Geo: only 21% of NB spend in Longview ($110.52 of $528.86); Tyler $128.99, Gilmer $73.25, Big Sandy $71.26, Kilgore $43.45, Gun Barrel City $39.39, Athens $33.32, Marshall $28.68 (all targeted).
- Search terms: HVAC 'heater not working' / 'heater repair' phrase pulls water heater / tankless / Rinnai / Navien terms onto the furnace page ($49.09 spent on 2), plus fireplace / gas log / RV; 11 competitor names with impressions at $0. NB 9pm-5am $112.59, 0 conv. QS: heater repair 3, plumber near me 1, emergency plumber near me 2; post-click BELOW AVERAGE on all scored NB keywords.

**LSA 9239407401 (7d):** $300.24 (prior $69.03), 8 leads (7 calls, 1 msg), 4 charged (3 calls, 1 msg), CPL $75.06, 28% of 7 x $154.29 = Underspending, top 94.96%. 5 of 8 leads under bathroom remodeling. 11-02 water heater message now BOOKED (11-03 item closed). 10-20 dispute CREDITED. 4 charged DECLINED undisputed: 10-14 10:26 msg, 10-14 12:22 msg, 10-23 07:48 call, 10-28 faucet msg.

**Staged, not applied:**
- HVAC Heating phrase negatives: water heater, tankless, rinnai, navien, fireplace, gas log, hydronic + competitors (loftis air, coy dodd, privette ac, simmons air conditioning, jacks air conditioning, chris cooling, milestone hvac, hamilton hvac, adams ac repair, 2 amigos, cool breeze). Water heater belongs in Plumbing if Edu wants it.
- Hold the $25 ceiling to 11-17 (2 weeks); if NB still has 0 verified calls, lower it and narrow geo rather than buy reach with CPC. Budgets stay 65/35.
- AM: confirm Tyler / Gilmer / Big Sandy / Gun Barrel City / Athens are served (open since 10-26).
- NB ad schedule ~6am-9pm. 'Calls from ads' UI / Google support check; 'calls from ads' biddable on HVAC Heating. LP form test with gclid still open.
- LSA: dispute the 4 charged DECLINED leads if not real jobs (10-14 ones first, window closing); AM on bathroom remodeling category.
- Revisit 2026-11-16 (7-day) and 2026-11-17 ($25 ceiling at 2 weeks).

Tasks: [7d Google](https://app.agencytitan.com/tasks/instance/1f1336e5-c3cd-4049-b4a3-589614e0ba5c) · [7d LSA](https://app.agencytitan.com/tasks/instance/76f54cad-8d86-4ec6-8465-1ee7f8b6a351). Meta in meta-ads-log.md.

## 2026-11-16 — AT optimization tasks (Gui, via Claude)

Read-only on all accounts; everything below is staged. 4 AT tasks completed (7d Google, 14d Google, 7d LSA, 7d Meta), notes in task fields + KPI rows (Google aa5baba3, LSA c8f6e2c7, Meta d33230c5). Extra read-only scripts: `np_extra_1116.py`, `np_extra2_1116.py`, `np_recs_1116.py` (run scratchpad) + CallRail calls 11-09..11-16.

**Changes since last pass (change_event):** only Edu's 11-10 06:31 API changes (negs 'streety' + 'water heater', Henderson County -> Henderson city on both NB; 'Click to call' -> Secondary). Both negs work: no matching terms after 11-10. Geo swap works: 0 spend outside targeted cities after 11-09.

**7-day Google (11-09..11-15 vs 11-02..11-08):** $708.76 / 33 clicks / 0 counted conv (prior $574.24 / 33 / 1 tap), CPC $21.48, IS 44.68% (prior 37.32%). NB Heating $492.15 / 21 clicks, CPC $23.44, IS 42.8%, rank-lost 50.7% (11-14 $144.15 and 11-15 $128.75, ~2x daily); NB Plumbing $197.24 / 9, IS 52.9%, rank-lost 47.1%; Branded $19.37 / 3, IS 100%. NB = 98% of budget, split 71/29 vs 65/35. KPI health Poor.
- **0 verified PPC leads.** 0 ad calls (call_view), 0 calls on CallRail 903-289-7073 11-09..11-15, so 0 calls from the 2 new LPs since the 11-11 number swap.
- ⚠ **Form goal gap:** 1 'TSD - Lead form' submit on 11-14 (NB Plumbing, Emergency Plumber page, desktop) + a desktop 'Click to call' tap the same day, both in all_conversions only. 'TSD - Lead form' (SUBMIT_LEAD_FORM) is in NO campaign's conversion goals (Plumbing goals = Calls from ads + Qualified lead; Heating has none), so new-page forms never reach the Conversions column. Real lead vs test unknown: check GHL.
- **After the window (11-16):** NB Heating ad call 416s from a first-time caller (936 area code, CallRail tag 'Schedule booked') + Branded call 224s from a repeat caller. First possible NB lead since the 10-27 relaunch, for fu-144.
- Search terms: 'jacks air conditioning longview tx' $24.30, 'evans heating and air reviews' $24.74, 'gas fireplace service' $23.29 via 'heating repair' PHRASE; 'streety' $69.86 was 11-09 (pre-neg). Tyler = $330.14 (48%) of NB spend, Longview $70.56. No overnight NB spend.

**14-day (11-02..11-15 vs 10-19..11-01):** $1,283.00 / 66 clicks / 1 counted (the 11-04 tap) vs $598.58 / 28 / 2. NB $1,218.25 / 56 clicks / 0 verified. Rank-lost Heating 56.8%, Plumbing 49.2%. Furnace Repair RSA AVERAGE, others GOOD, all approved. NB Heating has no sitelinks; NB Plumbing carries 'Commercial AC Repair' + 'Commercial Plumbing' sitelinks. No audiences. Auto recs: 66 KEYWORD, sitelink x2, partners x3, display expansion, RSA, lead form x2, PMax opt-in.

**LSA 9239407401 (7d, still classic LSA, not migrated):** $662.26 (prior $300.24), 10 leads (9 calls, 1 msg), 9 charged (8 calls, 1 msg), $73.58 per charged lead, 61% of 7 x $154.29 = On Pace, top 95.59%. 8 plumber / 1 bath remodel / 1 HVAC. Possible duplicate: 2 charged plumber calls 11-13 14:51 + 14:53. Charged + DECLINED + not credited (to rate, fu-161): 10-23 07:48 call, 10-28 msg, 11-03 14:06 call. 30d $1,493.18 / 22 charged / $67.87.

**Staged, not applied:**
- Add the Submit lead form goal (TSD - Lead form) to both NB campaigns (reporting only on Max Clicks; use all_conversions across the change).
- Check GHL for the 11-14 form; if it was a test, still owe the fu-121 first-visitor live test + Mo Verified Live.
- Heating PHRASE negs: fireplace, reviews, jacks, evans (+ the 11-09 competitor list).
- Heating sitelinks to the furnace page; plumbing sitelinks instead of 'Commercial AC Repair' on NB Plumbing; 'Heating/Heater Repair' headlines on the Furnace Repair RSA; observation audiences. Reject KEYWORD / partners / display / PMax / lead form recs.
- Hold the $25 cap + budgets to Edu's fu-144 read (11-17). AM: confirm Tyler is served.
- LSA: rate the possible 11-13 duplicate and the 3 charged DECLINED leads (fu-161).
- Revisit 2026-11-17 (fu-144: count the 11-16 NB call, CallRail page calls) and 2026-11-23 (7-day).

Tasks: [7d Google](https://app.agencytitan.com/tasks/instance/6e4b5453-6fe9-4e03-8b46-357fa6836848) · [14d Google](https://app.agencytitan.com/tasks/instance/e7c1489c-3acf-4666-aafc-65122ae4859e) · [7d LSA](https://app.agencytitan.com/tasks/instance/ee96cc48-85e8-4b2f-84d0-19e684e70e6d). Meta in meta-ads-log.md.

## 2026-11-17 — fu-144: week 3 of the relaunched Nonbranded (read-only, nothing changed)

**Window:** 11-10 → 11-16 (7d) vs week 2 11-03 → 11-09. Script `napps_recheck_1117.py` + CallRail COM4cd8 pulled WITH CallRail transcripts (`_pessoal/call-wins/napps-1117/`, 45 calls 11-03..11-16, 44 transcribed).
Only changes since 11-10: Edu's own 11-10 edits (negs + Henderson county → city). LP number swap live since 11-11 (both pages = 903-289-7073).

| | Budget | Week 3 (per day) | Clicks | CPC | IS | Rank-lost | Week 2 |
|---|---:|---:|---:|---:|---:|---:|---|
| NB Heating | $65 | $566.88 ($81, over budget) | 25 | $22.68 | 45 | 46 (+8 budget-lost) | $411 / 20 clk / IS 37 / rank-lost 63 |
| NB Plumbing | $35 | $197.38 ($28) | 9 | $21.93 | 54 | 46 | $222 / 10 clk / IS 40 / rank-lost 51 |
| Branded | $60 | $24.60 ($4) | 3 | $8.20 | 100 | 0 | $39 / 7 clk |

- **Split 74/26** (target 65/35): Heating overdelivered on the cold weekend (11-14 $144, 11-15 $129, 11-16 $123; impressions 185-254/day vs ~80 before), Plumbing held back by rank.
- **First real Nonbranded lead since the 10-27 relaunch:** 11-16 16:07, 418s, NB Heating ad call (call_view 416s, CallRail 903-289-7073, first-time caller, area code 936). Trailer home, 2-year-old heat/AC unit trips the main breaker
  when the heat runs, mentions Rusk County Electric (Henderson area). **BOOKED** for 11-17 8am-noon, $89 diagnostic quoted. Search term = "alford and pace air conditioning" via 'heating repair' PHRASE
  (he was looking for an old friend whose dad owned that company). Real, but partly luck.
- **Branded 11-16 11:09, 225s** = Huntington Hills (existing commercial customer, boiler + water heater just installed, asking about CO detector / TDLR registration). Existing, not new.
- **Page calls since the 11-11 number swap: 0.** All 3 calls on 903-289-7073 since 11-03 match Google call_view (call-button) calls 1:1 (11-03 Fort Collins repeat caller, the 2 above). So the pages now ARE measured and nobody called from them this week.
- **Form: 1 'TSD - Lead form' on NB Plumbing, 11-14, desktop** (+ 1 'Click to call' tap the same day, desktop, secondary). First form conversion on a new page since the relaunch, so the fu-121 listener fix fires live. Not verified as a real lead (no GHL access): ask Mo/Angela.
- **Geo (clicks, presence): Tyler = 15 of 25 Heating clicks ($328.57) + 5 of 9 Plumbing ($99.57) = $428 / 20 clicks / 0 leads = 56% of NB spend.** Longview 3 clicks ($72), Henderson 4 ($98, the lead's area),
  Marshall 3, Gilmer 2, Kilgore 1, Daingerfield 1. Tyler IS on the service-area page (checked 10-12 and today), but 90d before the relaunch Tyler + Henderson County = $3,223 / 1 conv, and it's 40 mi from the Longview shop with its own local competitors.
- **Quality:** Plumbing 'emergency plumber' LP experience now **AVERAGE** (was BELOW AVERAGE all 3 prior weeks), QS 5. Heating kws still LP BELOW AVERAGE, QS 2-3. Rank-lost dropped 63 → 46 on Heating.
- **Search terms (visible ~$350 of $764):** Heating 'heating repair' PHRASE is the loose one: "hvac longview tx" $47.52/2 (good intent), competitor/review terms "evans heating and air reviews" $24.74, "jacks air conditioning longview tx" $24.30,
  "gas fireplace service" $23.29, plus "alford and pace" (the lead). Plumbing: "i need a plumber" $48.68/2, "plumber" $24.94, "best plumbers near me", "plumbers near me" (the form).
- **Cumulative since 10-27:** $1,473.93 / 70 clicks / **1 booked new customer** (+1 unverified form).

**Proposed (Edu's go):**
1. **Hold budgets and the $25 cap for week 4.** Not the "still 0 with page calls tracked" case: 1 booked lead, page calls now measured, heating demand just jumped with the cold, Plumbing LP rating improved.
2. **Tyler: -50% location bid adjustment on both NB** (keep it targeted, it's in the service area). Week 3 = 56% of NB spend for 0 leads; 90d before relaunch $3.2k / 1 conv.
   Max Clicks honors location bid adjustments. Alternative: ask Angela whether Napps actually wants Tyler jobs before touching it.
3. **AM ask (fold into the 11-19 strategy review, fu-170):** was the 11-14 desktop form from the plumbing page a real lead (GHL)? And confirm the 11-16 caller (trailer, breaker tripping) was seen 11-17.
4. Leave 'heating repair' PHRASE alone this week (it found the lead); revisit competitor/review terms at the next read if they keep costing ~$25 a click.

## 2026-11-17 (later) — SECOND LOOK at the week-3 read (Edu asked) + APPLIED Tyler -50% on Heating only

**What the first pass missed (read-only checks, `_tmp_napps_2.py`, not kept):**
- **Message mismatch for Tyler on Heating:** RSA headline 1 "Furnace Repair in Longview TX", "Serving Longview & East TX"; LP H1 "Furnace & Heating Repair in Longview, TX". Tyler is 40 mi away.
  Since 10-27: Tyler Heating 711 impr / 23 clk (3.2% CTR) / $462 / 0 calls. The Plumbing ad has no city ("Emergency Plumber Near You"); Tyler Plumbing 107 / 6 / $122 / **1 form (the 11-14 one) + 1 tap**.
  So the only Plumbing conversion came from Tyler: the first-pass "-50% on both" would have cut it. Plumbing also has 0% budget-lost, so a Tyler cut there reallocates nothing.
- **Longview barely clicks the Heating ad:** 388 impr / 4 clk / 1.0% CTR (Tyler 3.2%). GBP took 42 calls in 14 days vs 3 on ads. In Longview, Napps' own listing likely absorbs the demand; the paid reach is the outer towns.
- **Heating is budget-limited on cold days** (budget-lost 27% on 11-14, 22% on 11-16), so money cut from Tyler on Heating does flow to the towns the page is written for.
- **"First real lead" framing:** real booked job, but via a legacy company name ("alford and pace air conditioning"), click in Longview. Generic heating/plumbing intent = 0 verified new customers from ~69 clicks / ~$1,450 in 3 weeks.
  The 11-10 trigger ("discuss cutting back or changing the offer") is met in spirit. Signal for an offer: term "$99 plumber special near me today"; the rep quoted the 11-16 caller an $89 diagnostic; neither page shows a price.
- **Nov MTD split 70/30** (Heating $990 / Plumbing $434) vs the client's 65/35: budgets are 65/35, Heating overdelivers in the cold, Plumbing can't buy its $35 at the $25 cap. Say it in the 11-19 review.
- No location bid modifiers existed on either NB campaign. (Unresolved geo 9053151 in the target list, not touched.)

**APPLIED 09:44 -03 (`napps_apply_1117.py`, validate-only then `--apply`):** Tyler 1026855 bid modifier **0.5 (-50%) on NB Heating 24049055193 only**; read-back 0.5, Plumbing Tyler modifier unset (confirmed with the dict query). Budgets $65/$35 and the $25 cap unchanged.
Max Clicks honors location bid adjustments; at ≤$12.50 Tyler Heating clicks will mostly stop (week 1 at a $15 cap delivered 13%).

**For the 11-19 strategy review (fu-170):** (1) does Napps want Tyler jobs; if yes, ask the web dev for Tyler-titled pages (rollout pattern); if no, exclude Tyler. (2) Was the 11-14 Tyler desktop plumbing form a real person (GHL)? Was the 11-16 caller seen 11-17? (3) Diagnostic price / offer on the two pages. (4) Delivery 70/30 vs requested 65/35.
Next read fu-176 11-24: Tyler share on Heating after the modifier, Heating spend on cold days, Plumbing form verification.

**AM note DRAFTED in Agency Titan (Edu asked "shouldn't we send a task to Angela?"; Edu sends):** Internal Request `49583709-e201-4295-9cbc-c724c1728911`,
"Google Ads update: first lead from the new pages, Tyler, and 3 questions before the 11-19 review", client Napps (AM = Angela), requester Edu, Intake/Review = Edu, Execution = Angela,
dept Account Management/Customer Success (confirmed on read-back). Covers: 11-10 negs + geo fix, 11-11 tracking number on the pages, 11-17 Tyler -50% on heating, 3-week results
($1,474 / 70 clk / 1 booked + 1 unverified form, 0 page calls, generic intent 0 confirmed), Nov delivery 70/30 vs 65/35, and the 3 review questions (Tyler pages or exclude, verify the form + the 11-16 caller, price/offer on the pages). Next check 11-24.
https://app.agencytitan.com/tasks/instance/49583709-e201-4295-9cbc-c724c1728911

## 2026-11-20 — Post Client Strategy Review alignment (AT 73c502b8, Gui via Claude)

Read-only. Script `napps_alignment_1120.py` (+ Meta campaign read). Checklist written (6 of 8), Paid Ads Alignment substage set to in_progress, NOT completed.
What was agreed: no call outcome recorded by the AM (review 0de4a6cc, call 11-19 13:42 UTC; `top_marketing_services` empty). Presented = keep every setting, ~$5,300/mo (Google ~$3,200, LSA ~$2,000, Meta ~$150), 65/35 HVAC/plumbing, Tyler -50% on Heating. After the call: a client `ads_budget_marketing` record "2026-11-19" = **$53,000**, 11-19 → 12-22 (almost surely $5,300 typed with an extra zero). AM note 49583709 (Tyler question) went back to Edu 11-20 14:53 UTC ("Sending back to Eduardo", 1 comment, not readable via API).
- **Budgets ✓ (unchanged):** NB Heating 24049055193 $65 + NB Plumbing 23819717682 $35 (Max Clicks, $25 cap) + Branded 23685615826 $60 (Target IS, $10 ceiling, spends ~$4/d). 7d 11-13..11-19: Heating $620.30 / 29 clk, Plumbing $303.57 / 13, Branded $30.52 = $954.39; split 67/33. Nov 1-19 $1,791.10 (67/33). Since the call (11-19..11-20): $98.50. LSA 9239407401 $154.29/d, week of 11-16 $558.04 (11-16..11-20). Meta ARL 120248317976460021 $5/d ACTIVE, $34.16 / 7d, reach 3,304, freq 2.16.
- **Ad groups ✓:** only Furnace Repair + Emergency Plumber live; all AC groups, Drain/Sewer, Leak Detection paused. RSAs APPROVED, final URLs = the 2 new LPs.
- **Geo ✓:** presence, 11 locations on each NB, Tyler 1026855 modifier 0.5 on Heating only (Edu 11-17, only change since). Unresolved 9053151 still in the list.
- **Copy ✗:** no offer anywhere in ads or assets (no promotion asset; 'Free Estimates' callout only). current_specials = $89 Diagnostic / $89 Fall Tune-Up (agreed 09-24, "previously $79"), but Hector's winter statics (AT 334ede71, still in Execution) say $79 Winter Tune-Up through Nov 30 and $79 + 10% off equipment in Dec. Which price is current is an AM question.
- **Tracking ✓ with gap:** Calls from ads primary + biddable (14d 2), LP number = CallRail 903-289-7073; 'TSD - Lead form' fires (14d 1 all-conv) but is in no campaign goal (staged 11-16, still not applied); CallRail → Google Ads integration still pending.
- **LSA since 11-13:** 19 leads (2 messages 11-19 and 11-20 still NEW, charged).
- **To escalate (not yet in an AM note):** (1) budget record $53,000 vs the $5,300 presented; (2) offer price $89 (current_specials) vs $79 (winter statics), and whether to put the offer in the Google ads/pages; (3) Tyler answer (pages or exclude) still open; (4) the 2 new LSA messages.
- Blocks completion: Tyler decision (client) + offer/copy not aligned + budget record typo. Next: fu-176 11-24.

## 2026-11-24 — AT tasks (Gui, via Claude)

Read-only on all accounts; everything below is staged. 3 AT tasks completed (7d Google, 7d LSA, 7d Meta), notes in task fields + KPI rows (Google c992e882, LSA 1b2547ef, Meta 09bba895). Extra read-only scripts in the run scratchpad: `np_recheck_1124.py` (copy of napps_recheck_1117.py on 11-17..11-23), `np_geo_1124.py`. CallRail not checked (agency account HTTP 429).

**Changes since last pass (change_event 11-16..11-24):** only Edu's 11-17 Tyler 0.5 modifier on NB Heating.

**7-day Google (11-17..11-23 vs 11-10..11-16):** $526.84 / 25 clicks / 0 counted conv (prior $767.21 / 36 / 2), CPC $21.07, Search IS 43.22%, 47% of the $160/d budget. KPI health Poor.
- NB Heating $287.32 / 14 clk (~$41/d of $65), IS 42%, rank-lost 58%, budget-lost 0 (prior $566.88 / 25, budget-lost 6%). NB Plumbing $233.60 / 10 (95% of budget, days up to $72.77). Branded $5.92 / 1, IS 95%. NB split 55/45 vs 65/35.
- **Tyler -50% worked on Tyler but the money didn't reflow:** Tyler Heating 193 impr / 3 clk / $35.31 (12% of Heating) vs 15 clk / $328.57 in wk 3. Heating is now rank-limited at the $25 cap, and heating impressions fell after 11-17 (233 → 38-90/day).
- 0 ad calls (call_view 11-17..11-24), 0 'TSD - Lead form', 2 secondary taps (Branded 11-18, Plumbing 11-19). Since 10-27 NB $1,973.20 / 93 clk / 1 booked (11-16).
- Clicks by town: Heating Longview 4 / Kilgore 3 / Tyler 3 / Marshall 2 / Henderson 2; Plumbing Longview 3 / Daingerfield 3 / Kilgore 2 / Marshall 1 / Gladewater 1.
- Terms: Plumbing = generic near-me ('plumbers near me' $74.60/3, '24 hour plumbers in my area' $48.66/2); 'plumber available now' EXACT $147.05/6 via close variants; 'plumber near me' EXACT QS 1 $86.55/4. Heating waste 'rheem tankless heater code e5' $24.82, 'electric heater won t turn on' $18.31, 'how much to replace hvac blower motor' $12.19.

**LSA 9239407401 (7d, classic LSA):** $690.25 (prior $765.26), 11 charged = 6 calls + 5 msgs, $62.75 per charged lead (prior $69.57), 4 uncharged bathroom-remodel calls, On Pace (64% of 7 x $154.29), top 90.76%. 9 of 11 charged = plumbing. Messages 11-19 + 11-20 still NEW status. No credits.

**Staged, not applied (inputs for Edu's fu-176 today):** hold budgets + $25 cap (Heating underspends after the Tyler cut); Heating PHRASE negs tankless + 'how much to replace' (+ the 11-16 fireplace/reviews/jacks/evans, still unapplied); 'TSD - Lead form' goal on both NB (11-16, still unapplied); watch 'plumber near me' EXACT QS 1 one more week; AM items from the 11-20 alignment still open. Revisit 2026-11-30.

Tasks: [7d Google](https://app.agencytitan.com/tasks/instance/5edaba87-a7cb-4ab6-ae5d-f4b15a015fcd) · [7d LSA](https://app.agencytitan.com/tasks/instance/14c666e2-3ba4-405f-9de8-2e1c68ea4f84). Meta in meta-ads-log.md.
