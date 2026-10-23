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
