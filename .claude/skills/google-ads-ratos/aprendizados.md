# Aprendizados — Google Ads Ratos

Regras aprendidas durante o uso. O Claude DEVE ler este arquivo antes de criar qualquer objeto.

---

## API v23 (SDK 30.0.0) — campos obrigatórios para criar campanha

- `contains_eu_political_advertising` é **enum** (não boolean). Usar valor `3` (DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING)
- `maximize_clicks` não funciona como atributo direto. Usar `manual_cpc.enhanced_cpc_enabled = False` como fallback
- Budget name deve ser único. Script agora usa timestamp no nome pra evitar colisão com budgets órfãos
- Descriptions do RSA: máximo 90 caracteres. Headlines: máximo 30 caracteres

## Bidding + budget

- **Maximize Conversions / tCPA exige budget NÃO-compartilhado.** Budget criado sem `explicitly_shared=False` vira shared por default → erro `BIDDING_STRATEGY_TYPE_INCOMPATIBLE_WITH_SHARED_BUDGET` ao criar a campanha. Sempre setar `budget.explicitly_shared = False` para campanhas Max Conv.
- `update.py campaign` **não** expõe bidding. Pra ajustar tCPA de uma campanha Max Conversions, mutate direto: `campaign.maximize_conversions.target_cpa_micros` com update_mask `"maximize_conversions.target_cpa_micros"`. Mudar o *target* (não o tipo de estratégia) **não** reseta learning.
- Diagnóstico clássico "IS perdido por RANK alto + budget quase não gasto" numa Max Conv com tCPA = **tCPA baixo demais estrangulando** (o algo se recusa a entrar em leilões acima do alvo). Subir o tCPA destrava volume na hora, sem mexer em budget.
- **`create.py campaign` sem `--maximize-conversions` nem `--target-cpa` cai em `MANUAL_CPC`.** Se a intenção era espelhar uma campanha existente em Max Conversions e o flag for esquecido, a campanha nasce em Manual CPC. Combinado com `create.py ad-group` sem `--cpc-bid` (o campo fica unset), o Google zera o `cpc_bid_micros` pro piso de **$0.01** — a campanha fica ENABLED mas efetivamente inerte (não ganha nenhum leilão). Sempre conferir `bidding_strategy_type` da campanha original antes de criar uma paralela, e checar `campaign.bidding_strategy_type` + `ad_group.effective_cpc_bid_micros` via GAQL direto depois do build (o `read.py` mostra `cpc_bid` mesmo quando o campo é vestigial numa campanha Max Conversions — não confiar nesse número isolado, sempre cruzar com o bidding_strategy_type).

## Auditoria de mudanças (change history)

- **`change_event` = só mudanças de USUÁRIO** (UI/API). **`change_status` = usuário + automações do Google.** Se algo apareceu no `change_status` e não no `change_event`, foi o **Google automático** (auto-assets, auto-apply), não você. Usar os dois pra auditar.
- `change_event` **exige** filtro em `change_event.change_date_time` + `LIMIT` (máx 10000).
- `change_status` **exige range LIMITADO nos DOIS lados** (`>=` E `<=`), senão dá `CHANGE_DATE_RANGE_INFINITE`.
- **Sempre checar o timezone da conta** (`SELECT customer.time_zone FROM customer`) antes de concluir "isso aconteceu depois que fechei". Contas US ficam em `America/Los_Angeles`; a máquina do Edu é BRT (PT+4). Já quase virou falso positivo.

## GAQL — campos e incompatibilidades

- `campaign.start_date` / `campaign.end_date` **não são selecionáveis** nesta versão da API (`UNRECOGNIZED_FIELD`).
- **Métricas de impression share NÃO são compatíveis com `segments.hour`** — IS só existe em granularidade diária.
- **IS intradiário é ruído.** Na mesma tarde o mesmo campo leu 10% e depois 33%. Só ler IS com o dia fechado.
- Pra comparar "hoje vs ontem" com o dia ainda correndo: **segmentar por `segments.hour` e cortar na mesma hora nos dois dias** (hour-matched). Comparar dia parcial com dia cheio é leitura errada.
- Cuidado: `run_query` **aborta o script** quando a query dá erro — uma query ruim no meio mata as seguintes. Isolar queries de risco.

## Armadilhas de conta (checar em toda auditoria)

- **Campanha `ENABLED` com `serving_status = ENDED`** gasta zero (data de fim passou) mas continua ENABLED com o budget preso nela. É bomba-relógio: basta alguém editar a data. Sempre `SELECT campaign.serving_status` junto do status. (Achado na All Heart: `20250049817`, ENABLED, $300/dia, ENDED.)
- **Smart bidding (Max Conv / tCPA) IGNORA bid modifiers de ad schedule** (e de device, exceto -100%). Se o objetivo é cortar fim de semana / horário ruim, o único lever que funciona é **restrição de ad schedule** (limitar quando serve), não ajuste de lance.
- Antes de culpar tracking por "zero conversão hoje", **checar `segments.day_of_week` em 60d**. Conta de home service pode simplesmente não converter no sábado/domingo (All Heart: sábado 3,6% de conv rate vs ~17% dia útil). Conversão de ligação também tem **lag de reporte** → dado do mesmo dia sempre subestima.
- **Campanha de experimento (trial) não aceita mudança de status pela API.** ENABLED + ENDED com orçamento preso, mas o
  mutate volta "Cannot modify dates, budget or status of a trial campaign". Só pela UI. (Zen Air `20525621445` e
  `21453417561`, 2026-10-05.)
- **Auto-apply `DISPLAY_EXPANSION_OPT_IN` religa Display em campanha Search depois que você desliga.** All Seasons: o fix de
  08-31 voltou em 3 campanhas. Desligar Display E pausar a subscription. Pausar funciona pela API:
  `RecommendationSubscriptionService.mutate_recommendation_subscription`, update em
  `customers/{cid}/recommendationSubscriptions/{TYPE}`, `status = PAUSED`, update_mask `status`. Listar as ativas:
  `SELECT recommendation_subscription.type, recommendation_subscription.status FROM recommendation_subscription`
  (alguns tipos voltam como `UNKNOWN`). (2026-10-05)
- **`STALE_DISAPPROVAL`** no `policy_topic_entries` = anúncio reprovado há muito tempo e nunca revisado de novo. Não serve
  até apelar na UI (ou recriar o anúncio). Checar ad groups com 0 anúncios APPROVED. (All Seasons LeadGen, 2026-10-05.)
- **"User doesn't have permission to access customer" numa conta que funcionava** = checar
  `SELECT customer_client_link.status FROM customer_client_link WHERE customer_client_link.client_customer = 'customers/<id>'`
  na MCC. `INACTIVE` = o cliente desvinculou a MCC. O `change_event` da MCC não mostra quando nem quem
  (`CUSTOMER_CLIENT_LINK` nem é filtrável). (On The Way, 2026-10-05.)
- **Budget lost IS = 0% todo dia ⇒ aumentar budget não faz NADA.** Confirmar `metrics.search_budget_lost_impression_share` antes de propor/creditar aumento de budget como solução. O gargalo aí é rank (lance/QS), não budget.

## Criação de campanha (geo)

- `create.py campaign` **não seta geo/idioma** — campanha nova nasce mirando tudo (o mundo inteiro, não só o país da conta). Depois de criar, adicionar `campaign_criterion` de LOCATION/PROXIMITY + LANGUAGE via mutate. Proximity: `proximity.geo_point.latitude_in_micro_degrees` (graus×1e6), `radius` (double) + `radius_units=MILES`.
- **REGRA GERAL, vale pra QUALQUER cliente: nunca ativar uma campanha sem confirmar location targeting via GAQL primeiro.** Não checar visualmente na UI, não assumir que quem fez o build lembrou — rodar a query e ver os critérios de verdade:
  ```
  SELECT campaign.id, campaign_criterion.type, campaign_criterion.criterion_id
  FROM campaign_criterion
  WHERE campaign.id = X AND campaign_criterion.type IN ('LOCATION','PROXIMITY','LOCATION_GROUP')
  ```
  Zero linhas = campanha mirando o planeta inteiro. `read.py locations` **não pega isso sozinho** —
  ele só filtra `type = 'LOCATION'`, então PROXIMITY e LOCATION_GROUP (os tipos que a maioria das
  contas TSD usa) ficam invisíveis nele; sempre rodar a query acima direto, com os três tipos juntos.
  Motivo: achado na Zen Air (`TSD_08.03_Search_NonBranded_Evergreen`, 24100030790) — campanha
  nasceu em 08-03 sem geo nenhum, ninguém verificou antes de ativar, ficou 3+ semanas rodando Google
  Search global. 30 dias de dados: Índia sozinha teve 7.326 cliques / 185 "conversões"; Estados
  Unidos (a área de serviço real) teve 108 cliques / 2 conversões — ~1% do volume da campanha.
  Achado e corrigido 2026-08-26 (ver `clients/zen-air/google-ads-log.md`).

## Local Services Ads (LSA) — leitura de leads (adicionado 2026-08-25)

- Dado de LSA **nao vive em metrics de campanha**. `campaigns`/`insights.py` so pegam spend/clicks agregados da campanha `advertising_channel_type = LOCAL_SERVICES`. Lead-level detail (tipo call/message/booking, status, charged, credit/dispute) vive num resource separado: `local_services_lead`. So retorna dado se a conta tiver campanha LOCAL_SERVICES ativa.
- Testado 2026-08-25: **funciona com as mesmas credenciais ja configuradas** (`.env.topserv`), sem approval extra, sem tier de developer token diferente.
- Filtro de periodo usa `local_services_lead.creation_date_time` (datetime), **nao** `segments.date` — o `build_date_clause()` padrao do `read.py` nao serve aqui.
- Campos validados: `id`, `lead_type`, `lead_status`, `lead_charged`, `creation_date_time`, `category_id`, `service_id`, `locale`, `credit_details.credit_state`, `credit_details.credit_state_last_update_date_time`. `lead_charged=false` e outros defaults ficam **omitidos** no JSON (proto3), nao tratar ausencia como erro.
- Ferramentas novas: `read.py local-services-leads --customer-id X --days N` (uma conta) e `lsa_report.py` (todas as contas TSD com LSA de uma vez — registro `LSA_ACCOUNTS` hardcoded no topo do script, atualizar quando cliente novo ligar LSA). Ver SKILL.md.
- **Nem toda conta PPC tem uma conta-irma de LSA sob a MCC.** Confirmado pra GC Home Service (`2375064049`): sem campanha LOCAL_SERVICES dentro da conta e sem nenhuma conta "GC Home Service - LSA" nos 65 clients da MCC Topservdigital (checado em qualquer status, nao so ENABLED). Antes de investigar "por que o LSA nao performa", confirmar que o LSA **existe** sob nossa MCC — pode ser que o cliente rode um perfil de LSA proprio, fora do nosso acesso.

## Conversion goals (modelo novo) — biddabilidade e writes silenciosos

- **`conversion_action.primary_for_goal` NÃO é o lever** em conta que usa o modelo de *conversion goals*. Quem decide o que entra no lance é `customer_conversion_goal` (conta) e `campaign_conversion_goal` (campanha), uma linha por **(category, origin)**. Mutate em `primary_for_goal` de ação web **retorna sucesso e não muda nada**. (Achado na Mission Accomplished 8634274092.)
- Ações **GOOGLE_HOSTED** (`Local actions - Directions / Menu views / Website visits / Other engagements`) rejeitam o mutate com INVALID_ARGUMENT — mas já são **não-biddable** por padrão. Aparecer como "Primary" na listagem é cosmético, não polui lance. Não confundir isso com problema real.
- **`protobuf_helpers.field_mask(None, pb)` descarta campo cujo valor é igual ao default do proto** → `biddable = False` nunca é enviado, e só os `True` aplicam. Para escrever booleano como False, usar sempre `field_mask_pb2.FieldMask(paths=["biddable"])` explícito.
- **REGRA GERAL: nunca reportar sucesso de escrita sem read-back.** "mutate accepted" mentiu duas vezes na mesma sessão. Depois de qualquer write, reconsultar o recurso e conferir o valor.
- Junk e formulário legítimo costumam dividir a **mesma** linha `DEFAULT / WEBSITE` — não dá pra separar no nível de conta. Para separar: goals por campanha, ou re-categorizar a ação para fora de DEFAULT.
- Em conta de home service com ServiceTitan, `PHONE_CALL_LEAD` = ligação **aconteceu**, não ligação que **valeu**. É esse o sinal que ensina o Smart Bidding a comprar spam call. Preferir `BOOK_APPOINTMENT` (Booked Job/JVP) e `CONVERTED_LEAD` (Completed Jobs) — checando antes se tem volume pra sustentar.

## Relatórios de alcance, CPM e mercado (Growth Engine pull, 2026-09-28/29)

Scripts read-only criados pra isso: `growth_engine_pull.py`, `growth_engine_formats.py`, `growth_engine_weekly.py`, `growth_engine_weekly_network.py` (todos rodam no book inteiro via `tsd.sh`). Log completo em `paid/relatorios/growth-engine-pull-2026-09/activity-log.md`.

- **DMA = `segments.geo_target_metro` em `user_location_view`** (localização física do usuário). Cobriu 99% do spend do book. Nome do metro vem de `geo_target_constant` (`name`, `canonical_name`) consultado por `resource_name IN (...)`. O `user_location_view` devolve várias linhas por metro: sempre agregar.
- **`segments.ad_network_type` funciona em PMax** e separa `YOUTUBE` / `CONTENT` / `SEARCH` / `SEARCH_PARTNERS` / `MAPS` / `DISCOVER` / `GMAIL`. É o único jeito de ver quanto do PMax virou YouTube (no book: $74k, ~4x o spend das campanhas de Vídeo).
- **`segments.ad_format_type`** (`INSTREAM_SKIPPABLE`, `INFEED`, `SHORTS`...) funciona em `FROM campaign` pra `VIDEO` e `DEMAND_GEN`. **Não combina com `segments.ad_network_type`**: a query inteira falha com um `INVALID_ARGUMENT` genérico. Em PMax só devolve `OTHER` (sem split de formato). `ad_group.type` não serve pra isso: as nossas campanhas de vídeo são todas `VIDEO_RESPONSIVE` (multi-formato).
- **Frequência no Google:** `metrics.unique_users` + `metrics.average_impression_frequency_per_user`, uma query por janela de 7 dias, só existe pra `VIDEO` / `DEMAND_GEN` / `DISPLAY`. **PMax e Search não têm frequência.**
- **CTV = `segments.device = CONNECTED_TV`.** No book, 66% do spend de campanhas de Vídeo dos clientes atuais rodou em TV.
- **Quando o erro vier genérico** ("Request contains an invalid argument"), ler `e.failure.errors[i].message` (GoogleAdsException): o `str(e)` do gRPC esconde a mensagem real.
- Segmentar por rede com `metrics.impressions > 0` perde linhas com gasto e zero impressão: ~$22 de diferença em $1,86M no book. Sempre reconciliar o total segmentado contra o total sem segmento.
- CPM de `SEARCH`, `SMART` e `LOCAL_SERVICES` não é preço de mídia (é cobrado por clique/lead). Nunca usar como CPM de marca.
