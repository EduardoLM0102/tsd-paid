# Zen Air Heating and Cooling — Google Ads log

Customer ID `4360840956` (PPC). LSA é conta separada: `3740502923`. MCC Topservdigital `4155514468`.
Cliente: Eddie (eddie@callzenair.com). AM/analista: Andrea.

---

## 2026-07-31 — PMax desligado, budget do Search para $200/dia

**Executado** por Edu (autoridade verbal do Head of Paid), via `change_pmax_off_search_up.sh`.

### Mudanças

| # | Objeto | ID | Antes | Depois |
|---|---|---|---|---|
| 1 | PMax `TSD_03.23_PMAX_HVAC_Calls` | 22959264938 | ENABLED, $100/dia | **PAUSED** |
| 2 | Search `TSD_05.13_Search_Branded_Evergreen` | 23675783172 | $150/dia | **$200/dia** |

Budget diário da conta (PPC): $250 → $200. Os outros $50/dia do PMax saíram da mesa.

### Métricas antes (últimos 30 dias, na data da mudança)

| Campanha | Spend | Conv | CPA | Cliques | Impressões |
|---|---|---|---|---|---|
| PMax `TSD_03.23_PMAX_HVAC_Calls` | $2.478,28 | 1 | **$2.478,28** | 4.702 | 143.266 |
| Search `TSD_05.13_Search_Branded_Evergreen` | $4.551,22 | 14 | $325,09 | 152 | 4.338 |

Motivo: 4.702 cliques e 143 mil impressões pra uma única conversão. Confirma o levantamento do
`2026-07-31-spend-reduction-plan.md` (grosso do delivery em YouTube/Display).

### Hipótese

Realocar metade do budget do PMax pro Search converte a $325 em vez de $2.478. Ganho esperado
~$50/dia de spend que sai do desperdício + ~$50/dia que passa a rodar num canal com CPA 7,6x melhor.

### RESSALVA — o Search "Branded" não é branded

Keywords de `23675783172`, mesmos 30 dias:

| Keyword | Match | Spend | Conv | CPA |
|---|---|---|---|---|
| hvac contractors near me | BROAD | $3.425,62 | 6 | **$570,94** |
| emergency heating service ga | BROAD | $507,91 | 2 | $253,96 |
| zen air heating and cooling | EXACT | $455,14 | 6 | **$75,86** |
| zen air hvac | EXACT | $66,10 | 0 | — |
| zen air | EXACT | $42,81 | 0 | — |

75% do spend está numa broad de $571 de CPA. **Os +$50/dia vão majoritariamente pra ela, não pros
termos de marca a $76.** Foi decisão consciente do Edu manter a broad rodando por ora (escopo mínimo
na mudança de hoje). O CPA blended do Search deve piorar antes de melhorar.

**Próximo passo natural:** separar o não-branded (`hvac contractors near me`,
`emergency heating service ga`, `commercial air conditioning ga`) numa campanha própria, e aí o
"Branded" vira branded de verdade.

### Aberto

- [ ] **Abrir ticket do AM (Andrea)** pra registrar por escrito a mudança de budget — MasterOps v6
  exige aprovação escrita do cliente; foi feito na autoridade verbal do Edu. Mesma dívida da
  GC Home Service.
- [x] Reler CPA do Search: confirmado em 2026-08-03, broad ainda domina (87% do spend, ~$427 CPA
  vs ~$105 CPA do branded puro) → split de campanha feito (ver 2026-08-03 abaixo).
- [ ] Decidir o destino dos outros $50/dia do PMax (hoje fora da conta).

---

## 2026-08-03 — Split non-branded: build + cutover completos, live

**Executado** por Edu (autoridade verbal do Head of Paid), via
`change2_split_nonbranded_campaign.sh` (build) + cutover manual do Edu (budget/status) + pausa das
keywords via Claude.

### O que foi criado

| Objeto | ID | Status |
|---|---|---|
| Campanha `TSD_08.03_Search_NonBranded_Evergreen` | 24100030790 | PAUSED, $100/dia |
| Ad group `Zen Air HVAC Nonbranded` | 205687909824 | PAUSED |
| 30 keywords não-branded (movidas logicamente de 193305460463) | — | PAUSED |
| 1 RSA (headlines/descriptions não-branded já aprovadas, sem menção a "Zen Air") | 819594645969 | PAUSED |

### Motivo

CPL blended da campanha "Branded" ($306,99, 16 conv / $4.911,81) escondia dois perfis bem diferentes:

| Segmento | Spend (30d) | Conv | CPL |
|---|---|---|---|
| Termos de marca ("zen air ...") | ~$630 | 6 | ~$105 |
| Broad não-branded ("hvac contractors near me" etc.) | ~$4.271 | 10 | ~$427 |

### CUTOVER executado

1. Campanha `23675783172` (branded): $200/dia → **$100/dia** (feito pelo Edu na UI)
2. Campanha `24100030790` (non-branded): **ENABLED** (feito pelo Edu na UI)
3. As 30 keywords não-branded **pausadas** no ad group antigo `193305460463` (feito via Claude,
   confirmado via API — ad group antigo agora só tem os 28 termos de marca ENABLED)

Budget total da conta continua $200/dia — foi split, não aumento.

Estado final confirmado via API: `TSD_05.13_Search_Branded_Evergreen` ENABLED/$100/dia com 28
keywords branded ativas; `TSD_08.03_Search_NonBranded_Evergreen` ENABLED/$100/dia com 30 keywords
não-branded e o RSA novo.

### BUG encontrado e corrigido no mesmo dia — bidding strategy errada

`create.py campaign` default pra `MANUAL_CPC` quando `--maximize-conversions`/`--target-cpa` não são
passados (o build não passou nenhum dos dois). Resultado: campanha nova nasceu em Manual CPC com
`ad_group.cpc_bid_micros` não setado → Google zerou pro piso de **$0.01 max CPC**, efetivamente
inerte pra essas keywords (CPC real histórico delas era $29-40). A campanha branded original usa
`MAXIMIZE_CONVERSIONS`, então o `$0.01` que aparece nela é um campo vestigial, não um teto ativo —
por isso não tinha o mesmo problema.

**Corrigido** via mutate direto (`maximize_conversions.target_cpa_micros = 0`) na campanha
24100030790, autorizado pelo Edu. Confirmado via GAQL: as duas campanhas agora estão em
`MAXIMIZE_CONVERSIONS`.

### Aberto

- [ ] **Ticket do AM (Andrea)** — registrar por escrito a mudança (mesma dívida de 07-31, ainda não
  fechada).
- [ ] Revisar bids das keywords/ad group novo na UI (criadas sem bid explícito).
- [ ] Revisar copy do RSA novo (819594645969) — está live agora, dar uma conferida.
- [ ] Acompanhar CPL de cada campanha separadamente em ~14 dias pra confirmar a tese ($105 branded
  vs $427 non-branded).

---

## 2026-08-24 — Bug de network settings corrigido (Search Partners/Display) + branded migrada pra Target Impression Share

**Executado** por Edu (autoridade verbal do Head of Paid), via mutate direto autorizado em conversa.

### O que foi achado

Review completa da conta encontrou que `TSD_08.03_Search_NonBranded_Evergreen` (24100030790) nasceu
com `target_search_network=true` (Search Partners) e `target_content_network=true` (Display) — ao
contrário da branded, que sempre rodou só em Google Search. Breakdown por rede desde o lançamento
(03/08 a 24/08, 21 dias):

| Rede | Cliques | Spend | Conversões | CPL |
|---|---|---|---|---|
| Google Search (real) | 422 | $341,14 | 10 | $34,11 |
| Search Partners | 9.286 | $1.771,04 | 494 | $3,59 |
| Content (Display) | 2.525 | $102,19 | 3 | $34,06 |

80% do spend e 97% das "conversões" vinham de Search Partners — e convertiam MELHOR que o Google
Search de verdade (5,3% vs 2,4%), o que é o padrão clássico de form-fill de baixa qualidade/bot, não
demanda real. 494 leads em 3 semanas não bate com o histórico da conta (14 leads reais/mês em julho).
As ações de conversão contadas são categorias legítimas (`SUBMIT_LEAD_FORM`) — não é problema de meta
de conversão errada, é 100% problema de rede/placement. ClickCease está ativo na conta mas não pega
esse tipo de erro (ele bloqueia por IP, não por network setting).

**Números reais vs reportados no período (03/08–24/08):** reportado (blended) = 510 leads / $8,27
CPL. Real (Search-only) = 13 leads / $180,46 CPL (sendo a branded sozinha: 3 leads / $668 CPL).

**Causa raiz**: `create.py` (skill google-ads-ratos) fixava `target_search_network = True` em toda
campanha SEARCH criada, sem flag pra desligar. Auditoria no resto da carteira TSD encontrou o mesmo
padrão em outras 9 contas (Cool Hand Electric, All Heart, Lilypad Septic, Gillespie's, Watt's Right,
All Seasons AC, Proud Pops, King's Window) — não corrigidas ainda, decisão de rollout por conta fica
pro Edu.

### Correções aplicadas

1. **24100030790**: `target_search_network` e `target_content_network` setados pra `false`.
   Confirmado via GAQL — campanha agora só serve em Google Search, igual a branded.
2. **`create.py`**: Search agora nasce Search-only por padrão (`target_content_network=False`,
   `target_search_network` atrás de flag opcional `--include-search-partners`). Vale pra toda
   campanha nova criada pela skill daqui pra frente, em qualquer conta.

### Branded (23675783172): MAXIMIZE_CONVERSIONS → TARGET_IMPRESSION_SHARE

**Motivo:** a campanha "Branded" nunca teve volume de conversão suficiente pro Maximize Conversions
otimizar de verdade — 1 a 3 conversões reais por semana/3 semanas é sinal demais fraco. Sem teto de
CPA, o Smart Bidding simplesmente gastava o budget no CPC que fosse preciso pra ganhar o leilão, e
o CPC do próprio nome da empresa subiu pra $37–39 (era $18–22 em julho). O trabalho real dessa
campanha não é gerar lead barato, é defender presença no nome da marca — então trocamos a estratégia
pra bater com o objetivo real, em vez de forçar uma estratégia de otimização por conversão numa
campanha que estruturalmente não tem dado pra alimentá-la.

**Configuração aplicada:**

| Campo | Valor |
|---|---|
| Estratégia | `TARGET_IMPRESSION_SHARE` |
| Location | `TOP_OF_PAGE` |
| Target IS | 90% |
| CPC bid ceiling | $4,00 |

O teto de $4 é bem abaixo do CPC atual ($37–39) e do baseline de julho ($18–22) — a hipótese é que boa
parte desse preço era o Smart Bidding perseguindo sinal fraco sem teto, não competição real de leilão
pelo termo de marca. Confirmado ao vivo via GAQL: `bidding_strategy_type: TARGET_IMPRESSION_SHARE`,
`location: TOP_OF_PAGE`, `location_fraction_micros: 900000`, `cpc_bid_ceiling_micros: 4000000`.

**Trade-off assumido:** a campanha para de "tentar achar leads" e passa a garantir presença a um custo
travado — se o CPC ceiling de $4 for baixo demais pra ganhar leilão no Gwinnett/North Atlanta GA, a
Target IS real vai ficar abaixo dos 90% e o teto precisa subir. Não confirmado ainda com dados
ao vivo pós-mudança.

Não mexemos na non-branded (24100030790) — continua em `MAXIMIZE_CONVERSIONS`. Ela tem sinal real
agora (10 conversões reais em 21 dias, $34 CPL) mas ainda é pouco volume pra Target CPA; plano é
deixar rodar 3-4 semanas pós-fix de network e aí sim considerar Target CPA perto do CPL que estiver
mostrando.

### Aberto

- [ ] **Ticket do AM (Andrea)** — essa é a terceira mudança sem registro escrito nessa conta (07-31 e
  08-03 seguem em aberto também). Vale mandar as três juntas numa nota só pra ela.
- [ ] Confirmar com Eddie/GHL se os ~500 "leads" de 03/08–23/08 (majoritariamente Search Partners)
  viraram job de verdade ou eram spam — fecha o loop sobre o que já foi reportado pro cliente nesse
  período.
- [ ] Reconferir Target Impression Share real atingida na branded em ~7-10 dias — se ficar bem abaixo
  de 90%, subir o CPC ceiling.
- [ ] Reconferir CPL da non-branded pós-fix em ~3-4 semanas e decidir sobre Target CPA.
- [ ] Rollout do fix de network settings nas outras 9 contas afetadas (Cool Hand Electric, All Heart,
  Lilypad Septic, Gillespie's, Watt's Right, All Seasons AC, Proud Pops, King's Window) — não feito,
  decisão por conta.

---

## 2026-08-24 (cont.) — Auditoria do GTM: "Submit lead form" é real, "ghl_*" é suspeito

**Investigação, nada mutado ainda.** GTM da Zen Air: conta `6069423387` ("Zen Air Heating & Cooling -
active" — tem uma decoy "Zen air 1" 6366481766, ignorar), container `100567467` (`GTM-KCZ2GTP`,
callzenair.com), workspace 29 ("Zen Air Landing Page Events").

### O que é verificado e confiável

Tag `cHTML - GHL Form Listener` [84] escuta `postMessage` da origem
`https://link.leadnurturemachine.com` (domínio do form embutido do GoHighLevel), só dispara se o
payload tiver um `email` real capturado, e só então empurra `form_submitted` pro dataLayer. O trigger
`cEvent - Lead` [54] escuta exatamente esse evento e dispara as tags de Lead (Google Ads `awct` [55],
GA4 `generate_lead` [70], Meta Lead [88]) — junto com dois outros gatilhos legítimos: `Booked
Appointment` [96] (`_event == 'BookingBooked'`) e `Quote Lead` [95] (usuário navega pra
`/systems/results`, a página de resultado da calculadora de sistema). **"Submit lead form - web" é
tracking de verdade, gated em dado real de contato — não é o problema.**

### A anomalia

Os eventos GA4 custom `ghl_contact_us`, `ghl_service_area`, `ghl_city_page`,
`ghl_schedule_services`, `ghl_request_estimate` (e o já suspeito `book_now_link_click`) **não existem
em nenhuma tag ou trigger desse container GTM.** Nada que a TSD gerencia cria esses nomes. Padrão de
nome (um evento por PÁGINA/etapa do funil) + ausência total no GTM = quase certamente um push nativo
do próprio GoHighLevel direto pro GA4, por fora do GTM, provavelmente disparando por PAGE VIEW de cada
etapa — não por submissão. Mesma espécie de bug do `book_now_link_click` da All Seasons AC (achado e
corrigido em agosto). **Não confirmado 100%** — é inferência por ausência de evidência + padrão de
nome, não uma captura direta do evento disparando. Não afirmar como fato pro cliente/Andrea sem
confirmar com o GHL ou o Eddie.

### Por que isso afeta bidding, não só relatório

Google Ads agrupa conversion actions num "goal" único por categoria+origem, não por ação individual.
`Submit lead form - web` e `ghl_contact_us` caem no MESMO balde (`SUBMIT_LEAD_FORM`/`WEBSITE`) — não
dá pra dizer ao Smart Bidding pra confiar só num e ignorar o outro sem separar as categorias. Volume
de `ghl_contact_us` (82/semana) é MAIOR que o do form verificado sozinho, misturado no mesmo sinal.
`ghl_service_area` cai no balde `PURCHASE`/`WEBSITE`, que está biddable na non-branded.

### Aberto

- [ ] Confirmar com GHL/Eddie o que `ghl_contact_us` e os outros 4 `ghl_*` realmente medem (page view
  vs. submit) antes de mexer em categorização de conversão nessa conta.
- [ ] Se confirmado page-view: recategorizar essas ações pra fora do balde `SUBMIT_LEAD_FORM`/
  `PURCHASE` (ação por ação, `conversion_action.category`) pra isolar o sinal real do form verificado.
  Não tentado ainda — mudança mais sensível que as de hoje porque afeta como lead é contado/reportado
  numa conta viva.
- [ ] Somar ao ticket do AM (Andrea) já pendente — mais um item de tracking a registrar por escrito.

---

## 2026-08-26 — Non-branded sem geo targeting nenhum desde a criação: achado e corrigido

**Achado.** Edu pediu pra checar o targeting da conta. `TSD_08.03_Search_NonBranded_Evergreen`
(24100030790) nunca recebeu location targeting desde que foi criada em 08-03. Confirmado via GAQL:
das 78 `campaign_criterion` na campanha, só `DEVICE` (3) e `IP_BLOCK` do ClickCease (75) — zero
`LOCATION`/`PROXIMITY`/`LOCATION_GROUP`.

**Impacto real**, medido via `geographic_view` (últimos 30 dias): Índia lidera em cliques (7.326
cliques / 185 "conversões"), seguida de Egito, Bangladesh, Paquistão, Indonésia, Iraque, Marrocos,
Arábia Saudita e mais 10 países. Estados Unidos — onde fica a área de serviço real (Gwinnett/North
Atlanta GA) — teve apenas 108 cliques / 2 conversões no mesmo período, ~1% do volume da campanha.
Explica o "516 conversões" que parecia bom demais — mesmo padrão de sintoma do bug de Search
Partners achado em 08-24, mas causa diferente: ali era mix de rede, aqui é ausência total de geo
targeting.

**Causa raiz:** `create.py campaign` nunca setou geo/idioma (já documentado em `aprendizados.md` da
skill), e o build de 08-03 (`change2_split_nonbranded_campaign.sh`) não incluiu nenhum passo manual
pra adicionar location depois. A campanha branded original nunca teve esse problema por ter sido
criada via UI, que força location antes de salvar.

**Corrigido 2026-08-26**, autorizado pelo Edu ("Copy the targeting from Branded to NonBranded
ASAP"), mutate direto (script ad-hoc, fora do `create.py`/`update.py` porque nenhum dos dois expõe
proximity ou `geo_target_type_setting`):

- 5 critérios `PROXIMITY`, raio de 7 milhas, mesmas coordenadas da branded (23675783172)
- `geo_target_type_setting`: `PRESENCE`/`PRESENCE` (igual à branded — mais estrito que o
  `PRESENCE_OR_INTEREST` que a non-branded tinha antes, mesmo sem nenhum location criterion setado)

Confirmado via read-back GAQL pós-mutate, não só a resposta do mutate.

### Aberto

- [ ] **Ticket do AM (Andrea)** — agora são 4 mudanças sem registro escrito nessa conta (07-31,
  08-03, 08-24, e essa). Bundle numa nota só.
- [ ] Não há retroativo: leads/spend já contabilizados no período pré-fix continuam como estão. O
  próximo pull de performance deve mostrar volume total caindo (menos cliques, mas os que sobram são
  reais).
- [ ] Mesma checagem rodada no resto da carteira ao mesmo tempo: achado um caso latente na Cool Hand
  Electric (`TSD_DemandGen_YouTube`, 24184775476) — sem geo, mas `NOT_ELIGIBLE`/$0 spend, ainda não
  ativa. Corrigir antes dela começar a servir.
- [x] Verificação de location targeting virou passo obrigatório em todo lançamento de campanha, pra
  qualquer cliente — ver `aprendizados.md` e `SKILL.md` da skill google-ads-ratos.

---

## 2026-09-07 — Weekly check: branded rank-limited (não é QS), ceiling subiu $4→$8, call assets pausados por ambiguidade de telefone

**Contexto:** checagem semanal de rotina (últimos 7 dias). Conta: 51 cliques, $772,61, 6 conversões
reais (100% `PHONE_CALL_LEAD` "Calls from ads", sem ruído GHL essa semana), $128,77 CPL, 15,2% IS
total. Non-branded ainda budget-constrained ($100/dia), branded gastando pouco ($68,61/semana, 21
cliques). Fix de rede do 08-24 (Search Partners/Display off) segue firme nas duas campanhas —
`target_search_network`/`target_content_network` = false confirmado via GAQL.

### Achado 1 — Branded rank-limited, não é problema de Quality Score

Branded (`TSD_05.13_Search_Branded_Evergreen`, 23675783172) está em Target Impression Share (90%
Top of Page, ceiling $4 setado em 08-24) mas só atingiu 10–17% de IS real nos últimos 7 dias, com
83–90% perdido pra **Ad Rank**, não budget (`primary_status_reasons: BIDDING_STRATEGY_LIMITED`).

Checado se era landing page: **não é**. Quality Score das keywords que servem ("zen air", "zen air
heating and cooling", "zen air hvac") está em 7–8/10, com `post_click_quality_score` (landing page)
e `creative_quality_score` (relevância do anúncio) **Above Average** em todas. O único componente
não-"above average" é `search_predicted_ctr` (Average). CPC médio pago nas vitórias ($2,20–3,92)
fica abaixo do ceiling de $4 — ou seja, é pura disputa de lance: mesmo bidando até o teto, não dá
pra vencer a maioria dos leilões do nome da marca.

**Ação:** ceiling do Target Impression Share subiu de **$4,00 para $8,00** (autorizado pelo Edu),
confirmado via read-back GAQL. Volume de branded é baixo (~$70/semana), então o teste é barato.
Recheck em alguns dias pra ver se o rank-lost realmente cai; se continuar travado perto de 85-90%
mesmo a $8, o teto não é o problema e vale olhar Auction Insights (não exposto pela API, só UI) pra
ver se tem concorrente disputando o nome da marca.

### Achado 2 — Auditoria de ad assets: cobertura já está completa, achou ambiguidade de telefone

Checado sitelink/callout/structured snippet/call/lead form/imagem em conta, campanha (branded) e
ad group. Cobertura já é ampla — 6 sitelinks + 4 herdados de conta + ~27 no ad group, 13 callouts,
2 structured snippets (Types, Neighborhoods), lead form, business name/logo, 15+ imagens. Esse não
é o gargalo do rank-lost.

**Mas achou ambiguidade de telefone**: três números diferentes em CALL assets pela conta —
- `(770) 282-1481` — customer_asset (nível conta), ENABLED, serviria em toda campanha sem override
- `(678)-853-7440` — campaign_asset só na branded, ENABLED, sobrepõe o da conta ali
- `678-329-9929` — linkado em 7 campanhas (a maioria pausada), um vínculo ENABLED numa campanha
  ENABLED mas dormente (`Lead Gen Campaign (2024)`, 0 impressões)

Edu pediu pra não usar extensão de telefone enquanto não tiver clareza de qual número é o certo.
**Pausados** (status PAUSED, não removidos — reversível):
- customer_asset `191832132074~CALL` ((770) 282-1481)
- campaign_asset `23675783172~342557558784~CALL` (branded, (678)-853-7440)
- campaign_asset `21453417561~72720578522~CALL` (Lead Gen Campaign 2024, 678-329-9929)

Confirmado via read-back GAQL. Os outros vínculos do 678-329-9929 (em campanhas já pausadas) não
foram tocados — não servem de qualquer forma.

### Aberto

- [ ] Confirmar com Eddie qual é o número de telefone correto antes de reativar qualquer call asset.
- [ ] Recheck do rank-lost impression share da branded em ~1 semana (ceiling $8).
- [ ] Auction Insights da branded (via UI, não API) pra ver se é concorrência genérica ou alguém
  disputando o nome "zen air" especificamente.
- [ ] Item do proximity/geo da non-branded (flagged 08-31) segue parado — Edu pediu pra deixar de
  lado por enquanto, ainda esperando resposta sobre se as 5 circles de 7 milhas foram intencionais.
- Nenhuma dessas mudanças de hoje mexeu no budget total da conta (ceiling de CPC e status de asset,
  não `campaign_budget`), então não entra no gate de aprovação escrita do MasterOps — mas ainda vale
  registrar no ticket do AM (Andrea) junto com o lote pendente de 07-31/08-03/08-24/08-26.

---

## 2026-09-08 — Novo call asset criado (678-606-8817), habilitado direto na conta

**Executado** por Edu (pedido direto em conversa), via script ad-hoc (`create_call_asset.py`, fora do
`create.py` porque a skill ainda não tem subcomando de CALL asset).

### O que foi feito

Criado 1 asset CALL novo + vínculo `customer_asset` (nível conta — mesmo padrão dos sitelinks/
callouts já existentes na conta):

| Campo | Valor |
|---|---|
| Asset | `customers/4360840956/assets/419084813112` |
| Telefone | 678-606-8817 |
| País | US |
| Vínculo | `customerAssets/419084813112~CALL`, status **ENABLED** |
| Call conversion reporting | `USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION` |

Confirmado via read-back GAQL (não só a resposta do mutate).

### RESSALVA — contradiz a pausa de 09-07

No check semanal de 09-07 (entrada acima), foram achados 3 números diferentes em CALL assets pela
conta — `(770) 282-1481`, `(678)-853-7440`, `678-329-9929` — e Edu pediu explicitamente pra **não
usar nenhuma extensão de telefone até ter clareza de qual número é o certo**. Os 3 foram pausados
por isso.

Esse asset novo (`678-606-8817`) é um **quarto número**, diferente dos três anteriores, criado já
**ENABLED** a pedido direto do Edu nesta conversa. Não ficou claro se esse é o número "certo" que
resolve a ambiguidade de 09-07, ou se é mais um número que precisa da mesma checagem antes de ficar
ativo — não pausei por conta própria porque foi pedido explícito, mas fica registrado o choque com a
decisão do dia anterior.

### Aberto

- [ ] Confirmar com Edu/Eddie se `678-606-8817` é o número definitivo. Se sim, decidir o destino dos
  outros 3 (deletar vs. deixar pausado). Se não, considerar pausar este também até resolver.
- [ ] Ticket do AM (Andrea) segue pendente — agora 5 mudanças sem registro escrito nessa conta
  (07-31, 08-03, 08-24, 08-26, 09-08).

---

## 2026-09-10 — Checagem: dá pra colocar mais budget agora? (só leitura, sem mudança)

**Contexto:** Edu perguntou se o PPC (conta 4360840956) aguentaria mais budget agora. Puxado GAQL
direto (`search_impression_share`, `search_budget_lost_impression_share`,
`search_rank_lost_impression_share`) nas duas campanhas Search ativas, últimos 7 dias.

| Campanha | Budget/dia | Gasto real/dia | IS | Perdido p/ budget | Perdido p/ rank |
|---|---|---|---|---|---|
| Branded (23675783172) | $50 | ~$20 | 17,5% | 0% | 82,5% |
| Non-branded (24100030790) | $150 | ~$115 | 20,1% | 14,5% | 65,4% |

Conta (7d, PPC only): $943,68 gastos, 66 cliques, 4 conversões, $235,92 CPL.

**Conclusão: não, o gargalo continua sendo Ad Rank, não budget.** As duas campanhas gastam abaixo do
teto diário (branded usa só 40% do budget, non-branded ~76%) — se fosse budget-capped, esperaria
gasto batendo no teto antes de perder IS por budget. Branded perde 0% de IS pra budget (100% rank).
Non-branded perde 14,5% pra budget em picos de tráfego, mas ainda é secundário frente ao 65,4%
perdido pra rank. Bate com o padrão histórico da conta (63,3% rank vs 22,6% budget em 07-31; recheck
de 09-07 que subiu o ceiling da branded de $4→$8 por causa exatamente desse rank-lost).

Nenhuma mudança feita — resposta ficou só no chat com o Edu.

### Aberto

- [ ] Se quiser capturar o 14,5% de budget-lost da non-branded, um bump pequeno ali é justificável —
  mas é ajuste marginal, não a resposta pro "precisa de mais budget geral".
- [ ] Recheck do ceiling $8 da branded (setado 09-07) segue pendente, ainda dentro da janela de
  ~1 semana.

---

## 2026-09-10 — Blended CPL 7 dias: chamadas nativas do call extension + conversões normais (só leitura, sem mudança)

**Contexto:** Edu perguntou o CPL blended da conta (4360840956) juntando conversões de call extension
nativo com conversões normais, últimos 7 dias. Puxado via `insights.py account` + GAQL segmentado por
`conversion_action_name`/`conversion_action_category` (`FROM customer`) e por campanha.

**Conta, 7d:** $943,68 gasto, 66 cliques, 4 conversões (métrica oficial de Conversions), CPL $235,92.

Split por ação:

| Ação | Categoria | Campanha | Conversões |
|---|---|---|---|
| Calls from ads | PHONE_CALL_LEAD | Branded (23675783172) | 1 |
| Calls from ads | PHONE_CALL_LEAD | Non-branded (24100030790) | 2 |
| Submit lead form - web | SUBMIT_LEAD_FORM | Non-branded (24100030790) | 1 |

**Edu notou divergência com a coluna "Phone calls" do UI** (5 non-branded + 1 branded = 6, vs. só 3
contando como conversão). Investigado e explicado: "Phone calls" é métrica bruta de toda ligação que
conectou pelo call asset, qualquer duração. "Calls from ads" (a conversion action ativa, categoria
PHONE_CALL_LEAD) só conta ligação **conectada por 60s+** (`phone_call_duration_seconds=60`,
confirmado via GAQL em `conversion_action`). Ou seja, das 6 ligações brutas, 3 não bateram o piso de
60s (queda, caixa postal, engano) e não entram como conversão nem no CPL oficial.

A pedido do Edu, recalculado um segundo número contando **toda ligação bruta como conversão** (sem
filtro de 60s) + o form: 6 ligações + 1 form = **7 "conversões"**, CPL = **$134,81** ($943,68 / 7).
Esse número é maior que o oficial do Google Ads porque ignora o threshold de qualificação da call
conversion action — é uma leitura alternativa pedida pelo Edu, não o CPL que a conta reporta.

Nenhuma mudança feita na conta — só leitura/cálculo, resposta ficou no chat.

### Aberto

- [ ] Ainda não fechado com Edu se ele quer os 60s como piso oficial de "lead" nos relatórios dessa
  conta daqui pra frente, ou se o $134,81 (toda ligação) foi só uma checagem pontual.
- [ ] Segue sem resolver a ambiguidade dos 4 números de telefone nos CALL assets (flag de 09-07/09-08
  acima) — os 3 "conversões brutas que não viraram lead oficial" podem incluir ligações em números
  que nem deveriam estar ativos.

---

## 2026-09-15 — Snapshot padrão 7d + investigação GA4 (clique no telefone vs. lead) + Peach AI

**Contexto:** Edu pediu o pacote padrão de métricas 7d (ver [[tsd-weekly-ppc-snapshot]]), depois pediu
pra cruzar com GA4 pra ver se tem gente clicando no número de telefone e não virando lead, depois
pediu o mesmo corte de conversões olhando só tráfego que veio do Google Ads, e por fim perguntou pelo
Peach AI. Só leitura, nenhuma mudança na conta.

### Snapshot padrão, 4360840956, LAST_7_DAYS (LSA 3740502923 excluído, é conta separada)

| Métrica | Valor |
|---|---|
| Spend | $1.524,71 |
| CPL | $1.524,71 |
| CPC | $17,33 |
| Total Conversions | 1 |
| Conv Rate | 1,14% |
| Impression Share (Search) | 17,73% |

Branded vs. Non-branded:

| Campanha | Spend | Conversões | CPL |
|---|---|---|---|
| Branded (23675783172) | $366,53 | 0 | N/A |
| Non-branded (24100030790) | $1.158,18 | 1 | $1.158,18 |

A única conversão da semana foi confirmada como `Calls from ads` (PHONE_CALL_LEAD) real, não ruído.
Ambas campanhas seguem 100% Google Search puro (`target_search_network`/`target_content_network` =
false nas duas) — o fix de rede de 08-24 segue de pé.

### GA4 (property 350001559, "Zen Air Heating & Cooling - GA4") — clique no telefone vs. lead real

`generate_lead` é o evento confiável (gated no listener real do form GHL, ver auditoria GTM de
08-24 acima). `phone_click` é só o tap no link tel:, sem sinal de conexão/duração (diferente do
"Calls from ads" do Google Ads, que exige 60s+ conectado).

**Últimos 30 dias:** 203 `phone_click`, mas 137 (109 usuários) caem no channel "Display" do GA4 e
aterrissam quase todos em **23/08 (87) e 24/08 (46)** — a cauda exata do vazamento de Search
Partners/Display na non-branded, corrigido em 24/08. Desses 137, só **3** viraram `generate_lead` em
toda a janela de 30 dias — ~98% não foi a lugar nenhum. Desde 25/08 esse volume "Display" caiu pra
quase zero (0-1/dia), confirmando que o fix segurou.

No tráfego limpo (google/cpc "Paid Search"): 49 `phone_click` vs. 223 `generate_lead` em 30 dias — o
form é que carrega o peso real, telefone não é ponto de vazamento no tráfego legítimo.

**Checado de brinde:** `Submit lead form - web` no Google Ads mostra 160 conversões em LAST_30_DAYS,
bate em ordem de grandeza com o `generate_lead` do GA4 — não tem gap de importação GA4→Google Ads
nessa conta. `ghl_contact_us` (ainda suspeito de ser page-view e não submit, flag de 08-24) somou mais
113 no mesmo período.

### Conversões olhando só tráfego Google Ads (GA4 filtrado por sessionSourceMedium = "google / cpc"), LAST_7_DAYS

| Métrica | Valor |
|---|---|
| Sessions | 58 |
| Users | 55 |
| Conversões (key events) | **1** |

A única conversão da semana no tráfego Google Ads foi um `phone_click` (marcado como key event no
GA4). Nenhum `generate_lead` saiu de tráfego Google Ads essa semana — bate com a semana fraca já
vista no snapshot padrão.

### Peach AI — zero na semana, mas por motivo estrutural

`Peach AI — Booked Call` e `Peach AI — Online Booking` são `UPLOAD_CLICKS`/`UPLOAD_CALLS` (origin
WEBSITE/CALL_FROM_ADS) — conversões importadas direto pro Google Ads via API, **não passam pelo
GA4**, então nunca apareceriam no corte acima independente de tráfego. Últimos 30 dias: 08/16, 08/17,
08/22, 08/23, 08/28 (Online Booking, 1 cada), 09/02 (Booked Call, 1), 09/05 e 09/07 (Online Booking,
0,5 cada). **Nada depois de 09/07** — confirma zero Peach AI nos últimos 7 dias, mesma história de
semana fraca em geral, não é problema específico de tráfego ou de fonte.

### Aberto

- [ ] Volume geral despencou logo depois de 24-25/08 e segue baixo (14d: 6 conversões/$1.806 vs. só 1
  nos últimos 7d) — bate na data com o bug de geo-targeting/círculos de proximidade da non-branded
  flagado ao Edu em 08-31 e nunca confirmado se foi resolvido. Vale reabrir essa pergunta com ele,
  pode estar limitando volume mais que Ad Rank ou budget agora.
- [ ] `ghl_contact_us` ainda sem confirmação com GHL/Eddie se é submit real ou page view (mesmo item
  aberto desde 08-24).

---

## 2026-09-15 — Tracking rebuild + URL change to landing page

**Reported by Edu via chat, not executed by Claude this session.**

Tracking rebuilt and fixed. Old tags deactivated to make sure they don't disrupt or interfere with
the new setup. Andrea had put hands on the account and broke some things.

URL changed in Google Ads — traffic is now directed to the landing page.

---

## 2026-09-30 — Deep dive de custo por conversão (só leitura, sem mudança)

**Contexto:** Edu: "absurdly expensive to get conversions, do a deep dive". Documento completo em
`2026-09-30-ppc-cost-deep-dive.md`. Janela limpa 08-31..09-29.

- Conta: $5.038, 20 conversões reportadas ($252), mas só ~13-14 leads reais (12 ligações 60s+ via
  `call_view` + 1-2 forms) = **~$360-390 por lead real**. Non-branded = 84% do gasto, CPC $28,15.
- **87% do gasto visível da non-branded foi em nome de concorrente** (Shumate, Coolray, Bardi, Goodman,
  Lennox help line, e dennis plumbing, ed's supply...). Causa: 4 keywords BROAD num ad group só, zero
  negativas, Max Conversions sem tCPA. `hvac contractors near me` BROAD = 60% do gasto da conta, QS 3.
- **Branded: `zen air` BROAD gastou $1.625 desde 08-17 com 0 conversão.** O diagnóstico de 09-07
  ("rank-limited no próprio nome") estava errado: o IS perdido vinha da broad entrando em leilão
  genérico. O ceiling $4→$8 deixou ela ganhar esses leilões (impr 256→1.183 na semana da mudança).
- LP `/book-hvac-service/` desde 09-15: 41 sessões pagas, 0 form, 1 tap no telefone (GA4).
- `[TSD] Click to call` (criado 09-15) é CLICK_TO_CALL = tap, não ligação; primary e biddable.
- LSA religado 09-10 (access@topservdigital.com), ~15 impr/dia, 1 lead cobrado em setembro.

### Aberto

- [ ] Edu decidir quais das 7 recomendações do doc executar (ordem sugerida lá).
- [ ] Redução de budget explícita (se escolhida) precisa de ticket do AM (Andrea) com aprovação escrita.
- [ ] Eddie/CSR checar se as ligações vindas de busca por concorrente viraram serviço de verdade.

---

## 2026-09-30 (cont.) — EXECUTADO: negativas de concorrente, broads da branded pausadas, bid cap na non-branded

**Aprovado pelo Edu no chat.** Script `zenair_change_0930.py` (dry run `validate_only` antes), verificado por
read-back. Snapshot pra rollback: `snapshot-2026-09-30-pre-negatives-bidcap.json`.

| Mudança | Antes | Depois |
|---|---|---|
| Non-branded (24100030790) bidding | Max Conversions sem tCPA | **Max Clicks, CPC máx $18** |
| Non-branded ad group 205687909824 | 0 negativas | **202** (178 phrase, 24 exact) |
| Branded (23675783172) broads | 8 BROAD de marca ativas | **8 pausadas** (ficam 10 exact + 10 phrase) |
| Branded negativas de campanha | 4 | **210** |
| Branded ceiling TIS | $8 | $8 (mantido, ver doc) |
| Budgets | $150 / $50 | sem mudança |

Negativas: ~170 concorrentes locais (phrase), supply houses + tech support/help line (phrase), fabricantes
só EXACT (carrier, goodman, lennox, daikin, rheem, trane...), marca Zen Air na non-branded (phrase), jobs/
careers/hiring na branded (phrase).

**Achado depois de aplicar:** as ligações vindas de busca por concorrente duraram 65–367s (7 das ~10 ligações
reais da non-branded). Não parecem engano. Horários no doc pro Eddie conferir. Non-branded vai perder a maior
parte das conversões até o rebuild por serviço ou uma campanha de concorrente dedicada.

### Aberto

- [ ] Recheck de search terms da non-branded em 3–4 dias (Max Clicks + 20 broads pode comprar clique barato e ruim).
- [ ] Eddie conferir as 7 ligações de concorrente (horários no doc) → decide campanha de concorrente dedicada.
- [ ] Ticket do AM (Andrea): somar essas mudanças ao lote pendente (sem mudança de budget total).

---

## 2026-10-05 — Otimização semanal 7 dias (task do Agency Titan): 11 negativas na non-branded

**Aprovado pelo Edu no chat.** Só negativas. Sem mudança de budget, lance ou anúncio. Script `zen_apply_1005.py`
(nesta pasta), as 11 conferidas por read-back na campanha.

**Últimos 7 dias (09-28 → 10-04), só PPC (LSA é conta separada):**

| Campanha | Gasto | Cliques | Conv | CPL |
|---|---|---|---|---|
| TSD_08.03_Search_NonBranded_Evergreen | $994,04 | 57 | 3 | $331 |
| TSD_05.13_Search_Branded_Evergreen | $83,01 | 11 | 0 | – |
| **Total** | **$1.077,05** | **68** | **3** | **$359** |

IS da conta 19,9% (50,4% perdido por rank, 29,8% por budget). As 3 conversões caíram 09-28 a 09-30, antes das mudanças
de 09-30: 2 `[TSD] Click to call` (tap) + 1 `Calls from ads`. **Desde o Max Clicks com teto $18 (09-30): CPC caiu de
$29,50 pra $17,44, mas 10-01 a 10-04 = 0 conversão em ~$590.** Branded quase parou de servir depois das broads
pausadas ($5 desde 10-01), esperado com o volume de marca baixo.

**Search terms desde 10-01 (recheck que estava devido ~10-03):** gasto em concorrente praticamente sumiu. O que vazou:
concorrentes novos (metus suwanee, top notch buford, jc lane, omega heating, res air), johnson controls, pesquisa de
produto/preço (hvac system cost, air conditioning prices, lennox hvac systems prices, hvac 4 ton unit), números de
modelo (ttb024c100a2, fb4cnp042, carrier fj5a) e informacional ("what does hvac stand for").

**Feito:** campanha 24100030790, nível campanha.
- PHRASE: metus, jc lane, omega heating, res air, johnson controls, stand for.
- EXACT: top notch buford (phrase "top notch" bloquearia busca genérica tipo "top notch ac repair"), what is hvac,
  ttb024c100a2, fb4cnp042, carrier fj5a.
- Replay nos search terms de 30d: nenhuma bloqueia keyword ativa nem termo que converteu.

**Deixado aberto de propósito:** duct cleaning (o site lista "Ventilation & Duct Cleaning"), buscas de preço/custo
(quem pesquisa custo de sistema novo pode virar troca de equipamento).

**Tentado e não deu:** pausar as 2 campanhas antigas ENABLED com status ENDED (`20525621445`, `21453417561`, Display
ligado). A API recusa: "Cannot modify dates, budget or status of a trial campaign" (são campanhas de experimento).
Gastam $0, inofensivas, só pela UI se quiser limpar.

### Aberto

- [ ] Dar mais 1 semana pro Max Clicks. Se a conversão não voltar, próximo passo é quebrar a non-branded em ad groups
  phrase/exact por serviço (rec. 4 do deep dive de 09-30).
- [ ] Segue aberto do 09-30: Eddie conferir as ligações de concorrente; ticket do AM (Andrea).

---

## 2026-10-08 — PAUSADA a non-branded (pedido do Edu no chat)

`TSD_08.03_Search_NonBranded_Evergreen` (24100030790): ENABLED → **PAUSED**, via `update.py campaign`, conferido por
read-back. Budget ($150/dia) e Max Clicks com teto $18 ficam como estão, pra reativar é só mudar o status.

**Por quê (checagem de 10-01 a 10-07):** $1.050, 81 cliques, 0 conversão. Nenhuma ligação no call_view desde 09-28. GA4
google/cpc: 65 sessões, 0 generate_lead, duração média 59s → 36s. 98% do gasto em 2 BROAD (`hvac contractors near me`
QS 3 $872, `hvac contractors ga` $178) comprando busca informacional (código de erro, DIY, "what is hvac"), pesquisa de
preço e concorrentes novos.

**Fica rodando:** só a branded (23675783172, $50/dia, Target IS). Budget diário da conta no PPC: $200 → $50.

### Aberto

- [ ] Rebuild da non-branded em ad groups phrase/exact por serviço (heating primeiro, é outubro). Começar como campanha
  nova ou reaproveitar esta, decidir no rebuild.
- [ ] Ticket do AM (Andrea): somar ao lote pendente. Esse pause muda o gasto total da conta.

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers (PPC only):** $453.91, 45 clicks, 0 primary conversions, $10.09 CPC. Nonbranded $383.14 on 10-06/07 (32 clicks, 0 conv) before the 10-08 pause. Branded $70.77, 13 clicks, $5.44 CPC, 95% IS, 0 primary conv (1 secondary 'Peach AI — Booked Call'). No call_view calls since 09-28. KPI Health = Poor.

**Changed:** nothing. **Still owed:** Nonbranded rebuild as phrase/exact service ad groups (heating first) + AM ticket for the 10-08 pause (fu-015).
AT task c98a00c9 closed, KPI record 081ab079.

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-14 — LSA review (account 3740502923): wins for the CS call, reach diagnosis, the $12 tCPL (read-only, nothing changed)

Full detail, tables and recipes: `clients/zen-air/2026-10-14-lsa-review.md`.

**Results since the 09-10 restart (to 10-14):** 13 phone leads, 6 BOOKED (1 is an existing customer, maintenance), 4 declined (3 were calls under 30s), 3 not yet marked by Zen. $169.01 spend, Google charged only 2 of 13 ($106.61 on a declined 25s call, $62.40 on a booked lead). About $28 per booked job, $13.00 blended per lead, $84.50 per charged lead. Best week 10-05..10-11: 4 calls, 3 booked. No caller PII in the repo.

**Reach:** budget is not the limit ($642.86/day cap, spending ~$5/day). Limits are the service area (15 cities, city limits only, missing Flowery Branch, Hoschton, Peachtree Corners and all county/unincorporated area), schedule (Sunday off, weekdays to 8 PM, Sat to 5 PM), and season. Impressions down YoY since ~May 2026, but fall lead count is on par with 2025.

**$12 tCPL:** API `category_bids` on HVAC has `target_cpa_bid_micros` = $12 (plus a dormant $350 manual max). Dashboard: "Set a target cost per lead (optional)" box is UNTICKED, but ticking it shows "$12 (current)". Forecast 3 leads/week at both $24 and $80 (none shown for $12). Whether Google applies the $12 is UNCONFIRMED. When it was set is unknowable: API change_event keeps 30 days (no changes since 09-15), UI change history only shows account/user events (not even the 07-03 pause), our 09-30 pull didn't read this field. Field exists since Sep 2024, so set then or later. Charged leads above $12 prove nothing (tCPL is an average). Blended $13 is close to $12 but slow months always land $12-18. Next: Google LSA support to confirm and clear, then a 4-week before/after read vs the same weeks of 2025.

**Access:** SearchLight Digital MCC 6263403407 still has an ACTIVE manager link (since 2024-11-21), and localservicesteam@gmail.com is an ADMIN (since 2024-01-29, owner unknown). Nothing removed.

**New script:** `./tsd.sh zenair_lsa_bids.py` (prints strategy, target per lead, manual max). Command Center: LSA channel updated, follow-up fu-051.

### Open

- [ ] Google LSA support: confirm/clear the $12 tCPL, then 4-week before/after read.
- [ ] LSA service area → 131 service-area ZIPs (heads-up to Andrea; AM ticket if total spend changes).
- [ ] Via Andrea → Eddie: Sunday/evening hours, owner of localservicesteam@gmail.com, mark 3 unmarked leads, which lead was the "won" + value.
- [ ] Ryan: SearchLight Digital link, vendor or leftover?
- [ ] Check LSA messaging is on; check if lead 339121110 ($106.61, declined) can still be disputed.

## 2026-10-16 — Weekly 7-day pass, Google Search + LSA (Agency Titan tasks, Gui): read-only, KPI entries logged

**PPC (10-09..10-15, LSA excluded):** $71.27, 13 clicks, 1 primary conv (a [TSD] Click to call tap, not a recorded call), $5.48 CPC. Only Branded live: 89% IS (11% rank-lost), QS 7-10, terms all brand variants, no negatives. Still 0 call_view calls since 09-28. KPI Health = Poor (no real leads while Nonbranded is paused). Window overlaps the 10-13 pass on 10-09..10-12 (that pass ran late).

**LSA 3740502923:** $62.40, 1 phone lead counted by Google (charged 10-10, also in the 10-13 entry), lead report shows 3 phone leads created 10-09..10-15 (1 BOOKED, 2 unmarked). 51 impr, 100% top / 97.5% abs top. Budget field $642.86/d vs ~$9/d = Underspending (not the limiter). Change event: Edu, 10-14, campaign criterion (service type) via web UI.

**Changed:** nothing. Still owed: Nonbranded phrase/exact rebuild (heating first) + AM ticket for the 10-08 pause.
AT tasks 539f28ea (Google), fd47eaff (LSA), left open for Gui's review. Pull: `weekly_pull.py` 10-09..10-15 vs 10-02..10-08.

## 2026-10-19 — 14-day review (Agency Titan task cd7bdcd7, Gui): read-only

10-05..10-18: $655.19 / 65 clk / 4 conv. NB paused since 10-08 ($531 / 0 on 10-05..07). Branded healthy (QS 7–10, CTR 21.9%, 89% IS). Recommended: NB phrase/exact rebuild (heating first) pointed at the 2 planned LPs; clean up the 2 ENDED trial campaigns in the UI (API can't pause them). Left open for Gui's review.

## 2026-10-23 — Weekly 7-day pass, Google Search + LSA (Agency Titan tasks, Gui): read-only, KPI entries logged

**PPC (10-16..10-22, LSA excluded):** $54.49, 9 clicks, 3 conv ($18.16 CPL, $6.05 CPC), 93% IS. Only Branded live (Target IS, $8 cap).
**2 Calls from ads (call_view: 2 calls, both 60s+) = first recorded ad calls since 09-28**, + 1 [TSD] Click to call tap. Terms all brand.
Changes: Edu set AI Max/asset automation off on legacy campaigns 10-16 (API); eddie@callzenair.com created an asset 10-19 (check). KPI Health = Mixed.
**LSA 3740502923:** $0, 52 impr, 100% top / 89% abs top; lead report 5 phone leads (1 BOOKED, 4 DECLINED), none charged. Underspending (reach-limited).
**Changed:** nothing. Still owed: Nonbranded phrase/exact rebuild (heating first) + AM ticket for the 10-08 pause.
AT tasks `54ce2840` (Google, KPI `7e79b7c1`), `7f983d3f` (LSA, KPI `1cd8910d`), completed.

## 2026-10-18 — LSA $12 tCPL recheck (read-only, Edu asked)

API pull (`zenair_lsa_bids.py` + `zenair_lsa_cap_check_1018.py`): **state identical to 10-14**. `category_bids` HVAC still has `target_cpa_bid_micros` = $12 (manual $350 dormant), strategy MAXIMIZE_CONVERSIONS, `bidding_strategy_system_status` ENABLED, campaign-level `maximize_conversions.target_cpa_micros` still empty. `change_event` 09-19..10-18: zero bidding changes by anyone — the only event is Edu's 10-14 12:00 CAMPAIGN_CRITERION CREATE (localServiceId, web UI). So nobody ticked, cleared or edited the target since the 10-14 review, and the API still can't show the box state; "active or not" remains a Google LSA support question (fu-051 still open). Flow since 10-14: 3 phone leads (10-15 x2, 10-16), 1 BOOKED, none charged; only Oct charge so far = $62.40 on 10-10. Command Center lsa.lastChecked + fu-051 note updated.

## 2026-10-23 — Non-branded rebuilt onto the 2 new landing pages and turned back ON (Edu's go in chat)

**Pages (live 200, noindex, GTM-KCZ2GTP, GHL form via link.leadnurturemachine.com, phone 678-853-7440):**
- Heating: https://callzenair.com/heating-repair-replacement-duluth-ga/ (form "Heating Oct 2026")
- AC: https://callzenair.com/ac-repair-replacement-duluth-ga/
Live GTM container has the GHL listener (`form_submitted` → Ads lead + GA4 `generate_lead`), so form fills on these pages count.
The stray 661/760 numbers in the page source are a site-wide leftover script that only fires on "ridgecrest"/"antelope-valley" URLs. Harmless here.

**Applied** with `clients/zen-air/zen_lp_rebuild_1023.py` (one atomic mutate, 270 ops, validate_only first, read back):

| Change | Before | After |
|---|---|---|
| `TSD_08.03_Search_NonBranded_Evergreen` (24100030790) status | PAUSED (since 10-08) | **ENABLED** |
| Budget | $150/day | **$100/day** (Edu's pick) |
| Bidding | Max Clicks, $18 ceiling | unchanged |
| Old ad group `Zen Air HVAC Nonbranded` (205687909824, 30 kws incl. `hvac contractors near me` BROAD) | ENABLED | **PAUSED** |
| New ad group `Heating Repair & Replacement` (201482056277) | – | 13 phrase + 7 exact, 1 RSA → heating page |
| New ad group `AC Repair & Replacement` (201482056557) | – | 9 phrase + 4 exact, 1 RSA → AC page |
| Campaign negatives | 11 | **241**: the old ad group's 202 copied to campaign level + 28 new phrase (water heater/hot water/space heater/pool, car/auto/truck/vehicle/rv, window unit/portable, DIY/how to/parts/manual/youtube/reddit, jobs/salary/careers/hiring/school/training/certification/course) |

Heating phrase: furnace repair, heating repair, heat pump repair, furnace replacement, heat pump replacement, furnace installation,
new furnace, furnace tune up, furnace service, heating service, heater repair, emergency furnace repair, furnace not working.
Heating exact: furnace repair near me, heating repair near me, heat pump repair near me, furnace repair, heating repair, furnace repair duluth ga, heating repair duluth ga.
AC phrase: ac repair, air conditioning repair, air conditioner repair, ac replacement, ac installation, new ac unit, ac tune up, ac service, emergency ac repair.
AC exact: ac repair near me, ac repair, air conditioning repair near me, ac repair duluth ga.
Conflict replay: no negative blocks a new keyword.

RSAs (15 H / 4 D each, no pins) use only claims on the pages (same-day + 24/7 emergency, free estimates, financing, NATE-certified, since 2016, family-owned, BBB A+) and approved brand lines (Stress Free HVAC, Your Neighborhood HVAC, Inhale Zen Exhale Comfort). No $49 offer (not confirmed, not on the pages). Ads 829433767919 (heating) / 829310581395 (AC) were in review at apply time.

Dropped for now (no matching page): commercial HVAC, IAQ, smart thermostat, generic "hvac contractors" terms.
Branded (23675783172, $50/day) untouched. PPC daily total $50 → **$150** (was $200 before the 10-08 pause).

### Open

- [ ] Confirm both RSAs APPROVED (should clear within a day).
- [ ] Search terms + spend recheck ~10-27 (phrase "heater repair"/"ac service" are the leak risks), first conversion read ~10-30.
- [ ] GHL gate: don't tell Eddie/Andrea the pages are "live" for leads until Mo marks Verified Live (joint test of the form).
- [ ] AM ticket (Andrea): bundle the 10-08 pause + this relaunch at $100/day (PPC total $150 vs $200 approved).
- [ ] Optional: sitelinks pointing at the 2 new pages; account sitelinks still go to the old service pages.

## 2026-10-23 — Lead outcomes since the 10-18 check (read-only, Edu asked)

Pull: `zenair_leads_1023.py` (LSA leads since 09-20 with status/notes/call length + PPC call_view since 10-14). Times America/New_York.

**New LSA leads since 10-18 (4 calls):**
| Created | Call | Status | Client note |
|---|---|---|---|
| 10-19 09:23 | 130s | ACTIVE (unmarked) | none |
| 10-20 11:22 | 106s | DECLINED | sales pitch (auto shop offering fleet services), not a customer |
| 10-21 13:00 | 28 min | **BOOKED** | two addresses, both scheduled for Nov, "both paid for" |
| 10-22 13:32 | 284s | ACTIVE (unmarked) | none |

**Updates on leads already reported:** 10-15 16:16 → BOOKED (returning customer, leaking HVAC). 10-15 09:10 note "hiring??" (job seeker, still ACTIVE). 10-16 08:17 (52s) still unmarked. 09-24 x2 (prepaid maintenance scheduling; "wrong Zen Air, different state") and 10-09 (records lookup) still ACTIVE.

LSA charged spend 10-14..10-23 = $0 (last charge $62.40 on 10-10). Since 09-10: 20 calls, 8 BOOKED (2 of them existing/returning customers), 5 DECLINED, 7 unmarked.

**PPC:** 2 real calls on Branded, 10-16 (68s, 118s), the first `call_view` calls since 09-28. Outcome unknown (Zen Air not in CallRail). NB was paused the whole window (relaunched today).

**Meta:** not pulled. Lead outcomes need Edu's lead export (city only); geo recheck stays ~10-27 vs the 10-19 baseline.

Ask via Andrea: mark the 7 unmarked LSA leads, and confirm what the 10-21 two-address booking was (job type / value).

### Same day — transcribed the 2 unmarked new calls (local faster-whisper small.en, audio + full transcripts kept in session scratchpad only)

- **10-19 09:23 (lead 346892854, 2 min):** furnace stopped working the night before, 40 degrees out. Rep (Haley) had no tech that day (several emergency calls, one tech out), scheduled for the next day 12:00–2:30, offered to call back if a slot opened. Caller accepted. **Booked by transcript** (LSA still shows unmarked).
- **10-22 13:32 (lead 347706996, 5 min):** upstairs heating unit stopped working suddenly a few days ago. Rep (Steve, alone in the office) scheduled tech Landon for the next morning ~9:00, text confirmation sent. **Booked by transcript** (LSA still shows unmarked).

Both are new heating repair service calls. Running tally since 09-10 counting transcripts: 20 calls, **10 booked** (2 existing/returning), 5 declined, 5 unmarked. Whisper can misspell names, so treat names as unverified.

## 2026-10-26 — AT optimization tasks (Gui, via Claude): 30-day + 90-day Google Search, 30-day LSA. Read-only, changes staged

**PPC 30d (09-26..10-25, LSA excluded):** $2,377.66, 177 clicks, 10 conv ($237.77), $13.43 CPC (prev 30: $4,366.21 / 19 conv). Branded $274.72 / 5 conv (2 real ad calls 10-16, 3 taps). Nonbranded old broad ad group $1,784.59 (09-26..10-07); relaunch since 10-23: $318.35, 27 clicks, $11.79 CPC, 1 tap, IS 23% (41% budget-lost). 3 days only, not judged.
**90d:** $12,332.06 (Aug junk conversions inflate 90d counts). Bidding = Automated (Target IS $8 / Max Clicks $18).

**Findings:**
- URGENT: **Branded has an ENABLED lead form asset 342506189374 built for Nick's Heating & Cooling** (business name "Nick's Heating & Cooling", nicksac.com URL + privacy policy). 257 impr / 2 clicks / 0 submits in 30d. Staged: remove.
- **'Submit lead form - web' last fired 2026-09-15** (0 in 40 days, incl. 27 clicks on the new LPs); ghl_contact_us also stopped 09-15; ghl_rating_form/city_page/schedule_services/request_estimate, GA4 phone_link_click, book_now_link_click, Lead form - Submit = 0 in 90d. 7 of 10 counted conv in 30d are taps. Staged: tracking test task (Gui to create), dead actions → secondary.
- Call number mismatch: ads use account call asset 678-606-8817, new LPs show 678-853-7440 (Branded's campaign call asset with that number is PAUSED). Open since 09-08.
- Nonbranded has no own sitelinks; inherits 9 account sitelinks to old city pages (/hvac-repair-in-suwanee-ga/ $175.62, /about-us/contact-us/ $150.16 in 30d).
- Geo: 5 x 7-mile circles, PRESENCE, 100% Georgia in 30d. DeKalb cities (Chamblee, Doraville, Tucker, Brookhaven) $261 / 30d, $1,249 / 90d, outside the service area.
- Low QS on new kws (furnace installation 1, ac service 1, several at 3, LP experience below); RSA labels all NOT_APPLICABLE.
- 60s+ ad calls in 90d (22) all between 6:00-17:59; 30d spend 20:00-05:59 $310, 0 conv. No audiences attached.
- Open Google recs: Search Partners x2, Display expansion, Max Conv, lead form asset, RSA. Staged: dismiss.

**Staged, not applied:** remove the Nick's lead form asset; form test on both new LPs; one call number on ads + pages; Nonbranded sitelinks to the new LPs; exclude the 4 DeKalb cities on Nonbranded; headlines for installation/service terms + swap weak Branded assets; verify RSA claims (NATE, 24/7, BBB A+, since 2016) on the site; NB schedule 6:00-20:00 after ~11-09; observation audiences; dismiss recs.

**LSA 3740502923, 30d:** $62.40, 12 phone leads, 0 message, 1 charged (10-07 booked), 0 disputes/credits. Booked 6/12 (50%); 10-19 and 10-22 are DECLINED in LSA but sounded booked on the 10-23 transcripts. 249 impr, 100% top / 92.5% abs top. Budget field $642.86/d, reach-limited. Staged: add Flowery Branch / Hoschton / Peachtree Corners, Sunday/evening hours (ask Eddie), LSA support on the $12 target (fu-051), Zen to fix statuses; access audit still open.

AT tasks completed: 30-day Google https://app.agencytitan.com/tasks/instance/f3678bdc-12fd-4e41-97e1-7b3d7b1b5183, 90-day Google https://app.agencytitan.com/tasks/instance/fffa5fc8-ab9a-4971-aca0-78f2867481d8, 30-day LSA https://app.agencytitan.com/tasks/instance/cae894d1-2bfe-404b-bd35-0ae96d40574c. KPI - LSA `1cd8910d` (10-23 row) updated with 30-day keys.

## 2026-10-26 — Branded + Non-Branded now report on a calls + forms goal only (Edu's go in chat)

**Why:** Edu asked to make sure the campaigns optimize for tap-to-calls and forms. Before: Non-Branded used the account-default goals (incl. `ghl_service_area` + `book_now_link_click` as PURCHASE, `ghl_contact_us` page-view events in SUBMIT_LEAD_FORM, BOOK_APPOINTMENT, CONTACT, app DOWNLOAD). Branded used custom goal "CMSA" (6452365353), which did NOT include `[TSD] Click to call` but did include the dead GA4 `phone_link_click`, Local actions - Directions and 5 `ghl_*` events.

**Checked end to end first (read-only):** GTM-KCZ2GTP live v32 tag `02 | Google Ads - Phone click` [110] → AW-11095585764 / `o-0hCNSG2PgcEOTn5Kop` = Ads action `[TSD] Click to call` (7769293652, type CLICK_TO_CALL, origin CALL_FROM_ADS, 1 per click), trigger [76] = any click on a `tel:` link. Headless test (Ads/GA4 hits aborted, nothing recorded) on both new LPs, desktop + Android: every tel: tap fired the Ads conversion + GA4 `phone_click`. Emulated iPhone got the site's bot check ("Checking your browser...", 403), likely a headless artifact, real iPhone tap test still worth doing. Peach AI DNI (`dni.js`, company 63) swaps the number for gclid visitors (pool like 678-470-xxxx); the tag still fires since it matches any tel:. Correction to my 10-26 chat read: `[TSD] Click to call` is the site tap tag, not an ad call-button tap, so 10-23 = 1 tap (same event as GA4), not 2.

**Applied** with `clients/zen-air/zen_goal_calls_forms_1026.py` (validate_only first, then read back):
- New custom goal **`TSD | Calls + Forms`** (6459645015): `[TSD] Click to call`, `Calls from ads` (60s+), `Submit lead form - web` (GTM, gated on real GHL submit), `Lead form - Submit` (Google lead form asset 342506189374).
- Left out on purpose: `ghl_*` GA4 imports, GA4 `phone_link_click` (never fires, site sends `phone_click`), Peach AI uploads (Edu: would double-count a tap + booking from one click).
- Branded (23675783172): CMSA → new goal. Non-Branded (24100030790): account default → new goal. CMSA itself untouched (old paused campaigns still use it).

**Bidding unchanged (Edu's pick):** NB Max Clicks $18 cap, Branded Target IS. Neither bids on conversions yet, so this changes the Conversions column only. Expect counted conversions to drop vs before on NB (the `ghl_*` events no longer count); use all_conversions when comparing across 10-26.
Switch NB to Max Conversions once it has ~15-20 real taps/calls/forms on the new LPs (fu in Command Center).

### Open
- [ ] Real-iPhone tap test on one LP (bot check blocked headless iPhone).
- [ ] NB → Max Conversions on the new goal at ~15-20 conversions.
- [ ] Optional cleanup: remove/secondary the dead GA4 `phone_link_click` action.

## 2026-10-26 — Lead form da Nick's REMOVIDO do Branded (achado do Gui)
Gui achou no Branded `TSD_05.13_Search_Branded_Evergreen` (23675783172) um lead form asset 342506189374 com business name "Nick's Heating & Cooling", privacy policy e final URL nicksac.com. Servia desde 2026-03-31 (campanha começou 03-23). Lifetime: 4.878 impr, 101 cliques, **9 envios** (05-20, 05-26, 06-08, 06-10, 06-11, 07-13, 07-17, 07-25, 08-02). Destino dos leads (email/webhook) não aparece na API; ver na UI. Downloads do Google só guardam 30 dias.
**18:58 BRT: link campaign_asset REMOVIDO** (validate + live), readback status REMOVED. O asset continua na conta, só não está ligado a nada. Nenhum outro lead form na conta (conta, campanha, ad group).
A auditoria de assets anterior (Achado 2) listou "lead form" mas não conferiu o nome. Conferir business name em lead forms nas auditorias.
Impacto: a ação "Lead form - Submit" (7553021219) da meta "TSD | Calls + Forms" não tem mais fonte nesta conta.

## 2026-10-29 — Recheck after the 10-23 NB relaunch + 10-26 goal (read-only, Edu asked)

**NB 24100030790 PAUSED ~15:00 ET 10-29 by Edu** (Eddie's request via Angela, AT 'Stop PPC - Google' 6ae9c79c; task Execution completed 10-30 with completion notes). Spent every day 10-23..10-29 (last impressions hour 15 ET).

NB 10-23..10-29 (both new ad groups, RSAs APPROVED, 100% SEARCH network): **$673 / 55 clicks / 1,490 impr / CPC $12.24 / 1 conv** (the 10-23 site tap, already known). 0 calls from ads (call_view empty since 10-23, Branded included). Heating $363 / 30 clicks / 1 conv, AC $310 / 25 clicks / 0. Search IS 16–29%, rank-lost 43% → 76% (budget-lost mostly low after 10-24), so the $18 cap + low QS is the limiter, not budget. QS where reported: `ac service` 1 ($65), `furnace installation` 1 ($48), `air conditioning repair` 5, most others 3. Top spenders: `heating service` $146, `new ac unit` $78, `air conditioning repair` $69.
Search terms: Google shows only ~$96 of the $673. Visible paid terms are mostly research/off-service: gas fireplace repair, "hvac furnace cost", 4-zone mini split install cost, in-room wall AC, "what makes furnace blow cold air", TXV valve cost, "best hvac units". Impression-only terms full of model numbers, error codes, competitor names, prices, mini splits, window/wall units.
Branded 10-23..10-29: $19 / 3 clicks / 0 counted conv (1 Peach AI booked call 10-23, all_conv only).

Meta lead ad set 120247339585910711 after the 10-20 home-only change: 10-13..10-19 $1,000 / 81 leads / $12.34 (11.6/day) vs 10-21..10-28 $1,150 / 87 / $13.22 (10.9/day), CPM ~$11.5 → ~$12.6. Volume barely dropped, so the change did not visibly filter much; city mix still needs Edu's lead export. No Meta edits since 10-24 (activity log = billing only).

## 2026-10-31 — AT optimization tasks (Gui, via Claude)

7-day Google Search + 7-day LSA. Read-only, nothing changed in the accounts.

**PPC (10-24..10-30 vs 10-17..10-23, LSA excluded):** $607.47, 53 clicks, **0 conversions** (all_conversions 0 too, 0 call_view calls), $11.46 CPC (prior $148.46 / 2 conv). KPI Health = Poor.
- **NB first full week on the new LPs:** $568.74, 47 clicks, $12.10 CPC, 0 conv / 0 taps / 0 ad calls. Since relaunch 10-23..10-29: $673.45, 55 clicks, 1 tap. IS 21% (58% rank-lost, 21% budget-lost). Heating LP 21 clicks, AC LP 14; 12 clicks came through the inherited account sitelinks.
- ⚠ **NB PAUSED 10-29 15:26 via the UI by the shared login access@topservdigital.com.** Nothing in the logs says who did it or why. Confirm before anyone relaunches it.
- Visible NB terms ($96 of $568) are research/DIY/product terms (gas fireplace repair, mini split cost, wall mounted AC, txv valve, best hvac units, brand/price furnace terms). The spend comes mostly from the keywords heating service ($118.76) and new ac unit ($77.87); QS 1 on ac service and furnace installation.
- Geo: DeKalb (Doraville/Dunwoody/Chamblee) $51.42; Hall Co (Oakwood/Gainesville/Flowery Branch) $81.09, check it against the service area. Spend from 20:00 to 05:59 was $150.01 (26% of NB).
- Branded: $38.73, 6 clicks, 95% IS, healthy. **The Nick's lead form asset is gone from Branded** (Edu removed a campaign asset via API on 10-26; on 10-31 no LEAD_FORM asset is linked).
- The 0 on forms can't be trusted while web form tracking stays dead since 09-15. Gui is investigating (since 10-26).
**Staged, not applied:** keep NB paused until LP form + call tracking is verified (Edu decides the relaunch); NB negatives (fireplace, mini split, wall mounted, window unit, txv, btu, mobile home, furnace brands, "what makes", "best hvac"; cost/price = Edu decision); tighten or pause heating service / new ac unit; schedule 6:00-20:00 + DeKalb exclusion; NB sitelinks to the new LPs; one call number; AM heads-up on the 10-29 pause; clean up the ENDED trial campaigns in the UI.
- **LSA 3740502923:** $62.40, 1 phone lead (10-28, charged, ACTIVE), 0 messages, $62.40 CPL (prior $0 / 4 uncharged leads: 1 booked, 3 declined). 74 impr, 100% top / 96.6% abs top. Underspending (the API budget of $642.86/d isn't the limiter, reach is). Oct 1-30: $124.80, 13 leads, 2 charged.

AT tasks completed: Google https://app.agencytitan.com/tasks/instance/ad08262c-5da0-426a-ac74-2f52472b706c (KPI `f16cc8c4`), LSA https://app.agencytitan.com/tasks/instance/913c1bce-b039-4bd8-9183-9ceefab6a9b5 (KPI `f22b6c10`).


## 2026-11-12 — Client Strategy Review Oct/Nov (AT c29ad0c8) Paid row written (read-only on the accounts)

Cycle 10-10..11-08. KPI row **53ecca81-aee0-4316-b6de-36f2d2196219** created on the client (Client Performance KPIs) + `additional_paid_ads_notes` on the task. Stage Performance Reporting NOT completed. Full detail: `clients/zen-air/strategy-review-octnov-2026.md`.

- Ad spend $7,481.80 = Meta $6,501.59 (lead CBO $4,517.71, awareness $1,957.64, Now Hiring $26.24) + Google Search $855.41 (Branded $181.96, NB $673.45 for its 10-23..10-29 test) + LSA $124.80 (2 charged leads).
- Qualified 207 = Meta 195 (of 328 unique HighLevel contacts, city inside the targeted area incl. Atlanta 107) + LSA 6 (2 new booked, 4 existing per the 11-12 rule) + Branded 6 (2 Calls from ads 10-16 + 4 Peach AI Booked Call). CPL $36.14. Rec budget $7,000/mo hold; +$50/d Meta if bookings confirm.
- PPC in cycle: Branded $181.96 / 30 clk / 181 impr / IS 93% / conv 7 (2 calls 60s+, 5 site taps) / all_conv 11 (+4 Peach AI). NB $673.45 / 55 clk / 1 tap / 0 calls, IS 20%, rank-lost 56%. Terms: Branded all brand; NB research/off-service (fireplace, furnace cost, mini split...).
- LSA in cycle: campaign $124.80, 238 impr, 36 clk. 10 phone leads, all transcribed locally (`_pessoal/call-wins/zen-air/`): see `lsa-call-wins-log.md`. The 10-28 wrong-number call (New York caller) was CHARGED $62.40 → rate bad ourselves (Command Center fu). 10-19 and 10-22 real bookings sit as DECLINED in LSA (office marks), nothing to do.
- HighLevel (via AT integration, location xYzDJzBnMX6dvv4gf8Xr): 340 contacts in cycle (328 Facebook, 2 City Pages Form, 1 Contact Us, 1 Club Zen, 8 no source). All 332 opportunities `open` in the first pipeline stage → GHL pipeline is not worked, outcomes live in ServiceTitan. Website forms are not attributable to paid (Ads form tracking dead since 09-15).
- `call_view` can't take `segments.date` (PROHIBITED_SEGMENT); pull all rows and filter `start_call_date_time` in Python. Script: `clients/zen-air/strategy_review_pull_1112.py`.

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

**14-Day Google (https://app.agencytitan.com/tasks/instance/34004e5e-9c66-4614-a0c7-dda88158a4bc), read-only, completed, all 8 checklist items ticked.** 10-20..11-02: $743.43 / 66 clk / 2 conv (both [TSD] Click to call taps) / $371.72 CPL / $11.26 CPC (prev 14 $504.48 / 53 / 3). 0 ad calls in call_view; 1 Peach AI Booked Call upload 10-23 (Branded, all-conv only). Web forms 0 (dead since 09-15, Gui investigating).
- NB 10-23..10-29 (paused 10-29 by access@ UI, still unknown who): $673.45 / 55 clk / 1 tap, $12.24 CPC, IS 20% (56% rank-lost). Branded $69.98 / 11 / 1 tap, IS 96%, $0 on 10-31..11-02 (quiet days).
- 12 kws with QS ≤4 = $223.77 (33% of NB); ac service + furnace installation QS 1. Visible NB terms $96.22, $83.27 of it research/DIY/product. 20:00-05:59 = $150.01 / 0 conv. Age 65+ $303.34 / 0 conv (small sample). No audiences attached. DeKalb $65.61, Hall Co $81.09 (check). 14 auto-apply subs PAUSED, 109 open recs on NB. eddie@callzenair.com uploaded 3 image assets (10-19, 11-02).
**Staged, not applied:** keep NB paused until the 10-29 pauser is known + tracking verified (Gui); before relaunch: QS-1 kws pause/exact, heating service + new ac unit → exact, negatives (10-31 list), NB sitelinks to new LPs, 6:00-20:00 schedule, DeKalb exclusion, observation audiences; dismiss recs; clean ENDED trial campaigns. Call-number mismatch flagged only (overlaps Gui's investigation).
Toggles to set in UI (14-Day): High-CPC Keywords Reviewed = Yes, Keyword Warnings Reviewed = Yes, Keywords Paused or Fixed = No, Geo Targeting Adjusted = No, Audience added? = No, Blockers to Escalate = Yes (NB paused by unknown user).

## 2026-11-09 — AT optimization tasks (Gui, via Claude)

7-day Google Search + 7-day LSA. Read-only, nothing changed in the accounts.

**PPC (11-02..11-08 vs 10-26..11-01, LSA excluded):** $33.68, 6 clicks, 3 conv, $11.23 CPL, $5.61 CPC, 50% CVR (prior $393.83 / 34 / 0, of which Nonbranded $355.10 before the 10-29 pause). KPI Health = Mixed.
- Branded only: IS 96.3% (3.7% rank-lost, 0 budget-lost), 42 impr, Limited (Target IS $8 ceiling). All 6 terms brand, no waste. Underspending vs $50/d = brand demand is the cap.
- The 3 conv are [TSD] Click to call taps (11-03 x1, 11-04 x2); 0 call_view calls. **Peach AI Booked Call logged 2 (all-conv only) on the same days (11-03, 11-04)**, so the brand taps likely became 2 booked calls.
- Nonbranded still PAUSED since 10-29 (shared access@ UI login, who/why unknown). Web forms 0 since 09-15 (Gui investigating). 11-02: eddie@callzenair.com created 2 assets.
**Staged, not applied:** confirm the 10-29 pauser with Edu, relaunch only after Gui's tracking check + the 11-03 14-day list; report Peach AI booked calls next to taps; AM ticket for the pause; call-number mismatch = Gui investigating.
- **LSA 3740502923:** $0, 2 phone leads (11-04, 11-05, uncharged, unmarked), 0 messages, 57 impr, 100% top / 79.5% abs top (prior $62.40 / 1 lead 10-28, still unmarked). Underspending: API budget $642.86/d isn't the limiter, reach is. 30d $124.80, 10 leads (2 BOOKED, 5 DECLINED, 3 open). Staged: Zen to mark open leads; service area/hours still waiting on Eddie.

AT tasks completed: Google https://app.agencytitan.com/tasks/instance/560989da-e642-46ad-94ed-69c04ade143b (KPI `f393ba8b`), LSA https://app.agencytitan.com/tasks/instance/e9a71b7d-f6f2-49b6-824f-d142a66d3701 (KPI `718b55bd`).
