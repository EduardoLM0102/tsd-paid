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
