---
name: topserv-google-ads-location
description: "Where TopServ Google Ads client work lives locally + how account access actually works (\"Ratos\" = a local skill, not an MCP connector)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c824868d-c8a7-4be1-bd2f-b3c0347fc9b2
  modified: 2026-09-03T14:34:51.514Z
---

TopServ (TSD) Google Ads client work lives at `~/Documents/GitHub/topserv-workspace/`.

Google Ads access is NOT via an MCP connector. It's the local skill **`google-ads-ratos`** at `~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/` — Python scripts (`read.py`, `insights.py`, `create.py`, etc.) that hit the Google Ads API against the TopServ MCC (Topservdigital, login-customer-id `4155514468`). When the user says "through Ratos," they mean this skill.

- `contas.yaml` in that skill dir maps client name → customer_id. Registered clients (as of 2026-07): **All Heart Heating & Cooling** (`9205826499`, HVAC+Plumbing, Kern/Antelope Valley CA), **Mission Accomplished** (`8634274092`, HVAC, Mohave County tri-state), and **Hawkins Siding and Exterior** (`2198608170`, siding/windows/doors, Texas Dallas metro/Lewisville).
- Per-client logs: `~/Documents/GitHub/topserv-workspace/clients/<slug>/google-ads-log.md`.
- Edu is Head of Paid Ads at TopServ (employee, started 2026-06-17, reports to Ryan/COO). The workspace is TSD-only and shared with the paid team through GitHub.

## Credenciais — sistema de PERFIS (cada pessoa na própria máquina)
- **Perfil TSD = `.env.topserv`** (MCC `4155514468`, default customer id All Heart `9205826499`). O `.env` default da skill **não é da TSD**: nunca usar pra trabalho TSD.
- **`GADS_ENV_PATH`** (env var) escolhe qual arquivo de credencial usar. Está em `scripts/lib/__init__.py` (`_ENV_SEARCH_PATHS`, primeiro da lista) e em `scripts/setup.py` (`ENV_PATH`). `save_refresh_token()` reescreve o arquivo inteiro e `_load_env_file()` para no primeiro arquivo que existir, então cada perfil precisa ter as 5 vars completas.
- Wrapper: **`scripts/tsd.sh <script.py> <args>`** roda qualquer script no perfil TopServ e filtra os warnings do SDK. Ex.: `./tsd.sh read.py campaigns --customer-id 9205826499 --date-range LAST_30_DAYS`. (Ele faz `exec` sem filtro quando o script é `setup.py`, que é interativo.)
- Os dois `.gitignore` (raiz + skill) cobrem `.env` e `.env.*` (menos `*.example`). Conferir com `git check-ignore` antes de criar perfil novo.
- Dev token + OAuth client (Desktop app) são da agência e iguais pra todo mundo. **O refresh token é de cada pessoa**: cada um roda `./tsd.sh setup.py oauth` com a própria conta TSD (Workspace). Passo a passo em `ONBOARDING.md`. Dev token da TopServ tem Basic/Standard. Testado: 62 contas sob o MCC.

## LSA lead data (adicionado 2026-08-25)
Local Services Ads tem dados que NÃO aparecem em `campaigns`/`insights.py` (que só pegam spend/clicks via a campanha LOCAL_SERVICES agregada). Lead-level detail (tipo call/message/booking, status, charged, credit/dispute) vive no resource separado `local_services_lead`, acessível com as MESMAS credenciais já configuradas (testado e funcionando 2026-08-25, sem approval extra necessário). Requer que a conta tenha uma campanha LOCAL_SERVICES ativa.
- Subcomando ad-hoc: `read.py local-services-leads --customer-id X --days 30`.
- Relatório global (todas as contas TSD com LSA de uma vez): `tsd.sh lsa_report.py` — registro de 15 contas (mesma-conta + dedicadas) hardcoded no topo do script (`LSA_ACCOUNTS`), atualizar lá quando cliente novo ligar LSA. Ver SKILL.md seção "LSA — relatorio global".
- GAQL usa `local_services_lead.creation_date_time` (datetime, não `segments.date`) pra filtro de período.
- Duração de cada ligação LSA: `local_services_lead_conversation.phone_call_details.call_duration_millis` (+ `.lead`, `.event_date_time`), mostra callbacks no mesmo lead. `contact_details.consumer_name` é UNRECOGNIZED_FIELD. `change_event` exige as DUAS datas (BETWEEN), senão CHANGE_DATE_RANGE_INFINITE (2026-10-14, Zen Air).
- **Link de lead LSA:** a API NÃO devolve URL da página do lead (só `call_recording_url` por ligação). Formato real do painel (achado no Slack): `ads.google.com/localservices/inbox?cid=<customer id>&bid=<business id>&pid=9999999999` (+ `mcid=9199434992`, `euid` é por usuário, dispensável). O `bid` NÃO sai da API; só copiando a URL do painel. Formato da URL de um lead específico ainda não confirmado: quando alguém colar uma, registrar aqui (2026-10-14).

## Armadilhas que já custaram tempo (não repetir)
- O OAuth client **tem que ser tipo "Desktop app"**. Um client "Web application" devolve `Error 400: redirect_uri_mismatch`, porque `setup.py:find_free_port()` sorteia uma porta livre entre 8080–8090 e o redirect não é fixo. Desktop app aceita loopback em qualquer porta sem registrar nada.
- Consent screen em modo **"Testing" expira o refresh token em 7 dias**. Com Workspace, marcar **Internal** (não expira, e some o aviso de app não verificado). Se um setup parar de funcionar do nada depois de ~1 semana, é isso.
- `run_query()` devolve as chaves em **snake_case** (`row['customer_client']['descriptive_name']`), NÃO camelCase.
- **Receita GAQL direta:** `from lib import run_query, init_client, resolve_customer_id`; `run_query(customer_id, query)` devolve lista de dicts (MessageToDict). **`run_query` NÃO converte micros**: dividir `cost_micros`, `average_cpc`, `target_cpa_micros` por 1_000_000 na mão (`read.py`/`insights.py` já convertem). Rodar a partir de `scripts/` via `./tsd.sh <script>.py`.
- Geo: não existe breakdown nativo no CLI. Usar GAQL `geographic_view` com `segments.geo_target_city/geo_target_region` + `geographic_view.location_type` (AREA_OF_INTEREST vs LOCATION_OF_PRESENCE), depois resolver nomes com `geo_target_constant` (`WHERE geo_target_constant.resource_name IN (...)`).
- Conversões/bidding: `conversion_action` (config), `campaign_conversion_goal` (o que o bidding persegue), `campaign.bidding_strategy_type` / `maximize_conversions.target_cpa_micros`.
- Se `read.py accounts` falhar (tenta cada conta como login próprio), listar a hierarquia com GAQL `customer_client` usando customer_id = MCC `4155514468`.
- No `contas.yaml`, alguns números nas `notas` são **campaign IDs, não customer IDs** (ex.: Hawkins LSA `21211420266`). Não tentar usar como `--customer-id`.
- **`LAST_90_DAYS` não existe** como literal do operador `DURING` (`LAST_30_DAYS` existe). Pra 90 dias usar `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'`.
- Pra ver conversão por ação, a query tem que sair **`FROM customer`** com `segments.conversion_action_name` (não `FROM campaign`).
- `insights.py campaign` devolve `cost` já dividido, mas **`cost_per_conversion` continua em micros** — dividir por 1e6 na mão.
- Nem todo cliente está no `contas.yaml` (GC Home Service `2375064049` e Spencer Air `2524618054` não estão). Passar `--customer-id` direto.
- **`update.py campaign` sem `--customer-id` explícito falha em SILÊNCIO com "sucesso" falso.** Sem a flag, `resolve_customer_id()` cai no default do perfil (`.env.topserv` = All Heart `9205826499`), não na conta que você acabou de estar lendo. Como o `--budget` faz uma query interna (`SELECT campaign.campaign_budget WHERE campaign.id = X`) pra achar o recurso do budget, e essa campanha não existe na conta errada, a query volta 0 linhas, o bloco de mutação é pulado inteiro — e mesmo assim o script imprime `{"status": "updated", "budget_updated": true}`. Aconteceu 2026-08-10 na Proud Pops (ver [[tsd-proud-pops-aug-budget]]): 2 updates "bem-sucedidos" que não mudaram nada na conta viva. **Sempre passar `--customer-id` explícito em update.py, e sempre reconferir com `read.py campaigns` depois — nunca confiar no JSON de sucesso sozinho.**
- **`campaign.status: ENABLED` does not mean a campaign is serving.** `read.py campaigns` / `insights.py` only surface the plain `status` field. A campaign can be `ENABLED` and still show zero impressions/clicks for weeks because `campaign.primary_status` is `ENDED` (e.g. a past `end_date`) or `NOT_ELIGIBLE` (policy/asset issues) — check `campaign.primary_status` + `campaign.primary_status_reasons` via a raw GAQL `run_query()` call (not exposed through the `read.py`/`insights.py` CLI) whenever a campaign shows activity that doesn't match its budget/history. Found 2026-09-03 on C&S Air's "Leads-Performance Max" campaign — see [[tsd-cs-air]]. Note `campaign.start_date`/`campaign.end_date` themselves are NOT selectable GAQL fields on this account/API version (`UNRECOGNIZED_FIELD`) — read the status/reasons fields instead of trying to read the raw date.
- **`update.py campaign --budget` está em CENTAVOS, não em dólares.** O código faz `amount_micros = int(args.budget) * 10000`. Pra $200/dia usar **`--budget 20000`**. Passar `--budget 200` seta a campanha a **$2,00/dia** — e a API aceita numa boa, sem erro. O `--help` diz "in centavos (5000 = R$50)", mas o exemplo do `SKILL.md` (`--budget 10000`) é ambíguo e induz ao erro. Quase derrubei o Search da Zen Air pra $2/dia assim em 2026-07-31 (ver [[tsd-zen-air]]). **Sempre conferir a unidade antes de mudança de budget em conta viva, e verificar com `read.py campaigns` depois** — o `read.py` já devolve o valor convertido em dólares, então serve de conferência.

## Keyword Planner works on TSD (checked 2026-10-07)
`./tsd.sh keyword_planner.py historical-metrics --customer-id <CID> --keywords "a|b" --location-id 21164 --language-id 1000 --network GOOGLE_SEARCH` returns 12 months of monthly volume + top-of-page bids. Defaults are Brazil/Portuguese, so always pass location (21164 = New Jersey) and language (1000 = English).

## Meta Ads MCP — campos que o conector recusa
O `ads_get_ad_entities` valida campo por nível e erra em vez de ignorar. Já bateu:
- nível `campaign`: **não aceita** `actions`, `link_click`. Usar `lead`, `cost_per_lead`, `results`, `cost_per_result`, `amount_spent`, `landing_page_view`, `post_engagement`.
- nível `ad`: **não aceita** `campaign_name`, `adset_name` (só os `_id`). Resolver nome cruzando com uma chamada de nível campaign.
- A mensagem de erro lista todos os campos válidos daquele nível — ler ela em vez de adivinhar de novo.

## Auto-mode blocks live Ratos writes (2026-09-29)
In auto mode, the classifier blocks writing mutate scripts AND running them via tsd.sh, even after Edu
explicitly says "execute". Retrying counts as "Auto-Mode Bypass", and so does opening Terminal for him.
The project-level allow rules in topserv-workspace/.claude/settings.local.json don't load when the
session starts from ~ (and that file's `Edit(/Users/...)` rule has a single slash, so it's
project-relative and wrong anyway). User-level `autoMode.allow` in ~/.claude/settings.json only covers
`update.py --status`. **What worked:** Edu exited auto mode, then the tsd.sh run got a normal Allow
prompt. **How to apply:** before a live mutation in auto mode, tell Edu up front to switch off auto mode
(or add the allow rules). Don't retry into a block. Write + `--validate` the script first so the live
run is one command. **Not consistent:** later the same day, still in auto mode, `update.py ad --final-urls`
and a scratchpad mutate script (validate + live in one run) went through without a block after Edu's
explicit "all allowed from me". GTM edits and publish also passed. So try once, and stop if blocked.

## Final URL swaps: don't edit the only ad (learned 2026-10-08, Proud Pops)
Updating `final_urls` on an existing RSA via AdService sends it back to review (PENDING / AD_GROUP_AD_UNDER_REVIEW). On
Proud Pops I edited the ONLY enabled ad in 6 ad groups at once, so Electrical + Plumbing Search both went to
primary_status PENDING until review cleared. **How to apply:** when an ad group has a single ad, create a new RSA with the new URL
(copy the assets), let it get approved, then pause the old one. Only edit in place when other approved ads in the same
ad group keep serving. Also check `campaign.primary_status_reasons` after any ad edit.
- **AI Max off via API:** setting `campaign.ai_max_setting.enable_ai_max = False` alone fails with AI_MAX_MUST_BE_ENABLED while
  TEXT_ASSET_AUTOMATION (text customization) is OPTED_IN. Send both in one op: enable_ai_max=False + asset_automation_settings
  [TEXT_ASSET_AUTOMATION OPTED_OUT, FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION OPTED_OUT], mask both fields (2026-10-08, Proud Pops).
- **Video (YouTube) campaigns are read-only for criteria via the API:** campaign_criterion creates on VIDEO campaigns fail
  MUTATE_NOT_ALLOWED, and content label BRAND_SUITABILITY_CONTENT_FOR_FAMILIES is INVALID_EXCLUDED_CATEGORY at campaign level. Use
  ACCOUNT-level `customer_negative_criterion` (youtube_channel.channel_id / content_label) instead; it also covers PMax YouTube
  inventory. MessageToDict returns enum fields as `type_` (not `type`) on these rows (2026-10-08, Proud Pops).
- **Cheap "Video views" CPV on YouTube = kids inventory.** Proud Pops SA VideoViews ($0.011 CPV) ran largely on Disney Jr. / Bluey /
  Ms Rachel; check group_placement_view on any TSD YouTube campaign before trusting view counts.
- **PMax brand exclusions ARE doable via API now (2026-10-08, google-ads 31.x):** `BrandSuggestionService.suggest_brands(brand_prefix=...)`
  → entity ids (/g/…). Create a shared_set type BRANDS + shared_criterion brand.entity_id, then attach to PMax as a **negative
  campaign_criterion brand_list.shared_set** (campaign_shared_set is OPERATION_NOT_PERMITTED_FOR_CONTEXT). PMax also accepts
  campaign-level negative keywords. Check the suggested entity's URL: Proud Pops' old name "The Problem Solvers" matched an unrelated UK company.

