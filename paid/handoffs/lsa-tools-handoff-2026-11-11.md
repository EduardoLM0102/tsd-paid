# Handoff: TopServ Digital LSA tooling (lead pull, call recordings, local transcription, call outcome rating)

**From:** Eduardo Marinho (Paid, TopServ Digital) · **To:** Alex Castro, for the coding agent building the TopServ Portal LSA feature · **Date:** 2026-11-11
**Source repo:** `topserv-workspace` (GitHub `EduardoLM0102/tsd-paid`). Every path below is relative to the repo root.

## 0. How to read this document

- This is a **handoff, not a summary**. Every script that touches LSA lead data is pasted **verbatim** in section 7 (Appendix). Nothing was rewritten, refactored or fixed.
- **No secrets are included.** `.env` values are replaced by `<redacted>`. Variable *names* are kept so you know what to provide. Google Ads customer IDs and client names are included (they are not secrets).
- Issues found while preparing this are listed in **section 6 (Known issues)**, marked `⚠ FLAG`. They are **not fixed**. Some come with a suggestion for the receiving agent; the suggestion is optional.
- Where something is not known, it says **UNVERIFIED**. Do not treat those as facts.
- Comments and docstrings in some scripts and in `SKILL.md` are in Portuguese. They are kept as-is.

## 1. What exists today (and what does not)

| Step | What it does | Implemented as | Status |
|---|---|---|---|
| 1. Pull LSA leads + conversations | GAQL on `local_services_lead` and `local_services_lead_conversation` per Google Ads account | `.claude/skills/call-wins/scripts/pull_lsa.py` | Working, read-only |
| 2. Download LSA call recordings | GET `call_recording_url` with the Google Ads OAuth bearer token | same file, `pull_lsa.py` | Working |
| 3. (Alt source) Pull CallRail calls + recordings | CallRail API v3, for clients whose LSA calls go through CallRail | `.claude/skills/call-wins/scripts/pull_calls.py` | Working, read-only (GET only) |
| 4. Transcribe recordings | Local `faster-whisper` (`small.en`, CPU, int8). Nothing goes to the cloud | `.claude/skills/call-wins/scripts/transcribe.py` | Working |
| 5. Rate each call / lead | Read transcript + Google status, tag each lead ✅ Booked / ⏳ Open / ❌ Not a lead / ⚠️ IVR-only, write a markdown log per client | **No script.** Done by Claude Code following the rules in `.claude/skills/call-wins/SKILL.md` (pasted verbatim, section 7.1) | Manual, agent-driven |
| 6. Cross-account lead report | Counts per account: total / charged / credited, by type and by status | `.claude/skills/google-ads-ratos/scripts/lsa_report.py` | Working, account list is stale (see 6) |
| 7. Cross-account health check | Verification artifacts (license, insurance, background, business registration) + LSA campaign status | `.claude/skills/google-ads-ratos/scripts/lsa_health_check.py` | Runs, has a hardcoded date (see 6) |
| 8. Lead-handling audit (one client) | Per lead: status, charged, credit state, call length bucket, did business reply to messages, feedback submitted | `.claude/skills/google-ads-ratos/scripts/proud_pops_lsa_lead_handling.py` | Client-specific (Proud Pops), kept as a pattern reference |
| 9. **Write back to LSA** (mark booked / archive / rate lead / dispute) | What Angela described in the 2026-11-10 meeting | **Not implemented anywhere.** No script calls a mutate/feedback endpoint. Every LSA tool in the repo is read-only | Does not exist |

**What Angela asked for in the 2026-11-10 meeting (the target behavior), quoted from the transcript:** for each LSA lead, "listen to the call, generate a name and reason for the call", leave the charge field as is, "then book it or archive it". She also mentioned the agent should "rate the call" and "dispute the call". She wants it tested on a smaller client before Watt's Right ("LSA generates 40% of the income for Watt's Right") and wants updates at least daily. Jonathan's concern: cost of running it for ~32 clients twice a day.

## 2. Architecture and data flow

```
Google Ads API (MCC 4155514468, OAuth user creds from .env.topserv)
   │  GAQL: local_services_lead (+ local_services_lead_conversation)
   ▼
pull_lsa.py ──► _pessoal/call-wins/<slug>/lsa.json         (leads, each with its conversations)
          └──► _pessoal/call-wins/<slug>/audio/lsa_<conversation_id>.mp3
                         (GET call_recording_url with "Authorization: Bearer <oauth access token>")

CallRail API v3 (for clients whose LSA calls show up in CallRail)
pull_calls.py ─► _pessoal/call-wins/<slug>/calls.json
           └──► _pessoal/call-wins/<slug>/audio/<callrail_call_id>.mp3

transcribe.py <dir> ─► <dir>/transcripts.json   {"<audio file basename>": "[m:ss] text\n[m:ss] text ..."}

Claude Code (agent, in the IDE) reads lsa.json + transcripts.json, applies SKILL.md rules
   ─► clients/<slug>/lsa-call-wins-log.md   (committed to the repo; PII-light summary)
```

- `_pessoal/` is gitignored. Audio, `lsa.json`, `calls.json` and `transcripts.json` never get committed (they hold customer PII).
- Only the summarized log (`clients/<slug>/lsa-call-wins-log.md`) is committed.
- Join key between `lsa.json` and `transcripts.json` for LSA: `transcripts["lsa_" + conversation.id]`, where `conversation` is an item in `lead["conversations"]`. It is **not** the lead id (see FLAG 6.5).

### Frameworks / dependencies

| Package | Version pin | Used by |
|---|---|---|
| Python | 3.9 on Edu's Mac, 3.12 on Windows | all |
| `google-ads` | `==31.1.0` | `lib/__init__.py`, all GAQL scripts |
| `google-auth-oauthlib` | `==1.3.1` | OAuth setup (`setup.py`, not pasted) |
| `google-api-python-client` | `==2.198.0` | not used by LSA scripts |
| `playwright` | `==1.60.0` | not used by LSA scripts |
| `requests` | unpinned (comes with google-ads deps) | `pull_lsa.py` audio download |
| `faster-whisper` | `>=1.0` | `transcribe.py` |
| stdlib `urllib` | n/a | `pull_calls.py` (no `requests`) |

Model: `faster-whisper` `small.en`, `device="cpu"`, `compute_type="int8"`, `beam_size=5`, `vad_filter=True`. First run downloads ~500 MB into `~/.cache/huggingface`. Measured speed: roughly 2–4x faster than real time on CPU. Two parallel runs share the CPU and each gets ~3x slower.

### Credentials (names only, values redacted)

`.claude/skills/google-ads-ratos/.env.topserv` (gitignored):
```
GOOGLE_ADS_DEVELOPER_TOKEN=<redacted>
GOOGLE_ADS_CLIENT_ID=<redacted>          # OAuth "Desktop app" client in TopServ's Google Cloud project
GOOGLE_ADS_CLIENT_SECRET=<redacted>
GOOGLE_ADS_REFRESH_TOKEN=<redacted>      # per person; user OAuth, not a service account
GOOGLE_ADS_LOGIN_CUSTOMER_ID=<redacted>  # MCC Topservdigital 4155514468
GOOGLE_ADS_CUSTOMER_ID=<redacted>        # default account when --customer-id is omitted
GTM_REFRESH_TOKEN=<redacted>             # not used by LSA tools
GA4_REFRESH_TOKEN=<redacted>             # not used by LSA tools
CALLRAIL_API_KEY=<redacted>
CALLRAIL_ACCOUNT_ID=<redacted>
```
`.env.callrail` at repo root (gitignored): `CALLRAIL_API_KEY=<redacted>` (read by `pull_calls.py`). The CallRail key is the agency key, read-only by team rule.

The LSA recording download reuses the Google Ads OAuth credentials: `init_client().credentials` → `creds.refresh(Request())` → `Authorization: Bearer <creds.token>`. Without the bearer header the recording URL (ads.google.com/localservicesads/attachment/...) returns a 302 to a login page.

## 3. Account map (client → Google Ads customer ID holding LSA)

Two hardcoded copies of this list exist (`LSA_ACCOUNTS` in `lsa_report.py` and in `lsa_health_check.py`), both shown verbatim in the appendix. Known additions not in either list (from team notes, see FLAG 6.2):

| Client | LSA customer_id | Note |
|---|---|---|
| Napps | 9239407401 | multi-trade (plumber / HVAC / bath remodel) |
| Spencer Air | 2524618054 | migrated to Pay-per-lead PMax 2026-11-04 |
| King's Window | 6769493219 | migrated 2026-11-04 |
| Amazing Morrow | 9677746935 | migrated 2026-11-03 |
| Concrete Adventures | 2898153501 | new client |
| Integrate Comfort (Belleville / Englewood) | 3 LSA accounts, IDs not in the LSA scripts | UNVERIFIED IDs, check `contas.yaml` |

Client lifecycle (affects which accounts a portal should poll): Golden Plumbing is on freeze; Gillespie's is offboarded; Hawkins Siding was terminated 2026-11-02 (30-day countdown to ~12-02); Cool Hand Electric's LSA is managed by another agency (Relentless Digital), read-only for TSD.

CallRail mapping: `paid/funnels/clients.json` → `{"_doc": ..., "clients": {"<slug>": {"cid", "callrailAccount", "callrailCompany", "callrailName"}}}`. Slugs present: watts-right, spencer-air, napps, integrate-comfort, cs-air, all-seasons-ac, neon-monkey, lilypad-septic, kings-window, hawkins-siding, cool-hand-electric.

Where LSA calls show up: on King's Window and Neon Monkey, LSA calls appear in CallRail (source "Google Local Services Ads"). On C&S Air, Napps, All Seasons and Cool Hand they do **not**, so `pull_lsa.py` is the source there. For any other client this is UNVERIFIED.

## 4. LSA API facts learned the hard way

- `local_services_lead` fields used: `resource_name, id, lead_type, lead_status, lead_charged, category_id, service_id, creation_date_time, credit_details.credit_state, lead_feedback_submitted`. Also available (used in `clients/zen-air/2026-10-14-lsa-review.md`, not in a script): `note.description`, `note.edit_date_time` (notes the client's team typed in LSA), and `contact_details` (select the whole message; `contact_details.consumer_name` and `contact_details.phone_number` return UNRECOGNIZED_FIELD).
- `local_services_lead_conversation` fields used: `id, lead, event_date_time, conversation_channel (PHONE_CALL / MESSAGE), participant_type (ADVERTISER / consumer), phone_call_details.call_duration_millis, phone_call_details.call_recording_url, message_details.text`.
- Conversations can be dated days after the lead was created, so `pull_lsa.py` puts no upper date bound on the conversation query.
- `lead_charged` absent in the JSON = not charged (protobuf default omitted by `MessageToDict`).
- **Google "BOOKED" is whatever the business tapped in the LSA app.** Watt's Right marks ~97% of leads booked. Treat it as a claim, report it next to the transcript outcome, never instead of it.
- **Pay-per-lead PMax migration (Nov 2026).** Google is auto-converting LSA into a `PERFORMANCE_MAX` campaign named `Pay-per-lead-PMax-<business>` with one asset group named `xcat:service_area_business_<category>`, and pausing the old `LocalServicesCampaign:SystemGenerated`. Accounts switched 11-03/11-04: Watt's Right, Amazing Morrow, Golden, Gray Duct, King's Window, Nick's Heating, Spencer Air. More will flip. After the switch, `local_services_lead` **still returns leads** (verified on Watt's Right 11-05/11-06). What breaks is anything filtered on `advertising_channel_type = 'LOCAL_SERVICES'` for spend/metrics/status. Detect migrated campaigns with: `SELECT campaign.id, asset_group.name FROM asset_group WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX' AND asset_group.name LIKE 'xcat:%'` (don't match on campaign name; it can be renamed). `campaign.start_date` is gone in this API version; use `campaign.start_date_time`. Manual per-category bidding goes away (one campaign-level tCPA).
- `$0 spend` on an LSA / pay-per-lead campaign does not mean dark. Spend = charged leads only. Judge delivery by impressions + leads per day.
- CallRail: the call's `recording` field is a pointer JSON `{"url": ...}`, not audio. Building the URL with `urlencode` turns commas in `fields` into `%2C`, which CallRail rejects (400), so `pull_calls.py` builds it by hand. 429 rate limit: one account at a time; repeated 429 for over an hour on one account usually means the account was cancelled. CallRail's own transcription needs the paid Conversation Intelligence add-on; only Proud Pops' own CallRail account (533681324) has it (`fields=transcription` returns a speaker-labeled transcript, no whisper needed).
- Splitting LSA calls out of CallRail data: match `\bLSA\b|Local Services` on the source/header only. A plain case-insensitive `lsa` matches "Tulsa".

## 5. The rating step (how Claude classifies each call today)

There is no code for this. The rules live in `SKILL.md` (verbatim in 7.1). Condensed here for convenience, in English; SKILL.md is the source of truth if they differ:

- Outcome is decided **only from what the transcript shows**: visit/estimate/service scheduled = ✅ Booked. Asked for a quote, sent a photo, left a message with a real need = ⏳ Open. Vendor, wrong number, other company, cancellation, job seeker = ❌ Not a lead. Greeting/voicemail only, no message = ⚠️ IVR-only. Existing customer confirming a time = ✅ but noted as not new pipeline. When unsure, ⏳ and say why.
- One line per LSA lead (merge multiple calls of the same lead). Show Google status (`BOOKED`, `ACTIVE`, ...) and charged / not charged **next to** the transcript outcome.
- Never repeat card numbers, CVV or payment data from a transcript; write "gave card details over the phone".
- Each log ends with a `Running tally` table (Outcome | Count | Detail) and a "Flag for Edu" paragraph (real new-job rate, voicemail drops, lost hot leads, wrong tracking number, metadata that doesn't match the transcript).
- Caveat always included: small local ASR model on phone audio misspells names/streets.

Example of the output (from `clients/cs-air/lsa-call-wins-log.md`, end-customer names removed):

```markdown
## 2026-10-05

- **16:01 · 93s · LSA · <city>** — New customer. Indoor unit runs, outdoor unit is dead, house at 79°F with the thermostat set to 73. Told about the $89 trip charge; she said she'd make a few calls and call back. Google status: Booked (charged). ⏳ Open — the call ends without a booking. Check whether she called back and booked.

## Running tally (Oct 1–15, 3 calls)

| Outcome | Count | Detail |
|---|---|---|
| ✅ Booked | 1 | <city> repair, Mon Oct 5, 10am–1pm |
| ⏳ Open | 2 | new customer (price-shopping, Google says booked), existing customer (lapsed maintenance plan) |
| ❌ Not a lead | 0 | |
```

Findings this process produced (why it matters for the portal): C&S Air "Declined" = non-jobs and about half of LSA leads are existing customers; Neon Monkey 18 ad calls → 5 real leads, 7 IVR-only; All Seasons 7 of 13 calls were callers who wanted a different company. Google's "Booked" count overstated ad-driven new jobs in every account checked.

## 6. Known issues (marked, NOT fixed)

> ⚠ FLAG 6.1 — `lsa_health_check.py`: `TODAY = date(2026, 8, 27)` is hardcoded. All "expired" / "expires soon" checks compare against Aug 27, 2026, not the run date. Suggestion for the receiving agent: use `date.today()` (not applied).

> ⚠ FLAG 6.2 — Account lists are duplicated and stale. `LSA_ACCOUNTS` exists twice (`lsa_report.py`, `lsa_health_check.py`) with slightly different labels ("All Seasons AC" vs "All Seasons AC (LSA)"). Both miss Napps 9239407401, Spencer 2524618054, King's 6769493219, Amazing Morrow 9677746935, Concrete Adventures 2898153501, the Integrate Comfort LSA accounts and others listed in section 4's migration note. Both still include offboarded/frozen clients (Gillespie's, Golden, Hawkins). The docstring of `pull_lsa.py` already notes the first three missing IDs. Suggestion: single source of truth (e.g. discover via `customer_client` under the MCC + a has-LSA check) — not applied.

> ⚠ FLAG 6.3 — Pay-per-lead PMax migration breaks `lsa_health_check.py` campaign check. `CAMPAIGN_QUERY` filters `advertising_channel_type = 'LOCAL_SERVICES'`. On migrated accounts the old LSA campaign is PAUSED by Google, so the script will flag "Campaign PAUSED" (false alarm) and never inspects the new `PERFORMANCE_MAX` pay-per-lead campaign. Same risk for any portal logic that filters on `LOCAL_SERVICES` for spend/status.

> ⚠ FLAG 6.4 — `lsa_health_check.py` `CAMPAIGN_QUERY` has `segments.date DURING LAST_30_DAYS` in WHERE. UNVERIFIED: a campaign with no metric rows in the last 30 days may not be returned at all, so a fully dark campaign could produce no flag.

> ⚠ FLAG 6.5 — Doc vs behavior mismatch in `transcribe.py`. Docstring says keys are `"<call or lead id>"`. Actual key is the audio file basename: CallRail → `<callrail call id>`, LSA → `lsa_<conversation id>` (from `pull_lsa.py`). A lead with several calls has several transcript entries. Joining by lead id will miss everything.

> ⚠ FLAG 6.6 — Error handling is inconsistent around `lib.run_query`. `run_query` calls `handle_google_error`, which prints and calls `sys.exit(1)`. So in `pull_lsa.py` one failing account/query kills the whole process. `proud_pops_lsa_lead_handling.py` works around it with `except SystemExit`. `lsa_report.py` / `lsa_health_check.py` avoid it by calling `service.search` directly with their own try/except. A portal loop over many accounts needs to account for this.

> ⚠ FLAG 6.7 — `lsa_report.py` and `lsa_health_check.py` use `sys.path.insert(0, ".")` before `from lib import ...`. They only work when the working directory is `.claude/skills/google-ads-ratos/scripts/` (which `tsd.sh` guarantees with `cd "$SCRIPT_DIR"`). Run from anywhere else → `ModuleNotFoundError: lib`. `pull_lsa.py` and `proud_pops_lsa_lead_handling.py` use absolute paths and don't have this problem.

> ⚠ FLAG 6.8 — `pull_calls.py` parses `.env.callrail` with `dict(l.strip().split("=", 1) ...)` and checks `l.startswith("#")` on the unstripped line. Quoted values (`KEY="abc"`) keep their quotes and auth fails; an indented comment line containing `=` would be parsed as a key. `lib._load_env_file` does strip quotes, so the two loaders behave differently.

> ⚠ FLAG 6.9 — `lsa_report.py` labels the count "credited/disputed" but counts every `credit_state` that is not UNSPECIFIED/UNKNOWN, which UNVERIFIED-ly includes pending credit requests, not only granted credits.

> ⚠ FLAG 6.10 — `pull_lsa.py` interpolates CLI dates straight into GAQL f-strings without validation. Low risk on a CLI, worth noting if the portal passes user input.

> ⚠ FLAG 6.11 — `proud_pops_lsa_lead_handling.py` is client-specific: hardcoded `SURFACES` (3 Proud Pops accounts), `SINCE = "2026-06-01"`, and "SEPTEMBER" sections hardcoded to `2026-09`. It is here as a pattern for per-lead handling metrics (call length buckets, business-replied-to-message, `lead_feedback_submitted`), not as reusable code.

> ⚠ FLAG 6.12 — **Policy conflict to decide, not a code bug.** Current team rule (SKILL.md + ONBOARDING): recordings and transcripts carry customer PII (names, addresses, sometimes card numbers spoken aloud) and must stay local; transcription is local on purpose, and nothing goes to a cloud service. A portal that sends audio or transcripts to a hosted model/API (for transcription or for the rating step) conflicts with that rule. This needs a decision from Jonathan/Ryan before building, not a workaround in code.

> ⚠ FLAG 6.13 — Write-back does not exist (see section 1, row 9). UNVERIFIED pointers for the receiving agent to check against current Google Ads API docs, nothing here was tested: `LocalServicesLeadService` has `ProvideLeadFeedback` (consumer-style satisfaction survey on a lead) and `AppendLeadConversation` (append a note/message). It is UNVERIFIED whether the API can set a lead to BOOKED/ARCHIVED or file a dispute; in the team's experience those were done in the LSA dashboard UI. With leads moving into the Google Ads UI after the PMax migration, the available actions may change.

> ⚠ FLAG 6.14 — Volume/cost context for Jonathan's question, measured on Edu's Mac: transcription is local CPU (no per-call API cost), ~2–4x faster than real time. Calls per client per week were never measured across all clients (example: C&S Air had 3 LSA calls in Oct 1–15). The rating step today is a Claude Code session (subscription), not a metered API. Twice-daily runs for ~32 clients were never tested.

## 7. Appendix: source files, verbatim

### 7.1 `.claude/skills/call-wins/SKILL.md`

~~~~markdown
---
name: call-wins
description: Transcreve e analisa ligações de clientes TSD (gravações da CallRail e do LSA) e monta o "call wins log" do cliente, dia a dia, com o resultado de cada ligação (✅ Booked / ⏳ Open / ❌ Not a lead / ⚠️ IVR-only). Transcrição 100% local (faster-whisper), nada vai pra nuvem. Use quando alguém pedir "call wins", "log de ligações", "transcrever ligações", "analisar as ligações", "o que as ligações estão gerando", "quantas ligações viraram job", "ouvir as gravações da CallRail", ou atualizar o call-wins-log.md / lsa-call-wins-log.md de um cliente.
---

# Call Wins: ligações → transcrição local → log de resultados

Pega as ligações de um cliente num período, baixa as gravações, transcreve no próprio computador e escreve um log honesto do que cada ligação gerou. Serve pra provar, ligação por ligação, o que o investimento em ads está virando em job fechado (ou não). Processo completo e histórico: `_contexto/memoria/tsd-call-wins-log-process.md`. Contas e armadilhas da CallRail: `_contexto/memoria/tsd-callrail-api-access.md`.

Setup (uma vez por máquina): seção 8 do `ONBOARDING.md`. Se `.env.callrail` não existir na raiz ou o `faster-whisper` não estiver instalado, mandar a pessoa pra lá antes de seguir.

## Regras que não mudam

- **Transcrição só local.** As gravações têm PII real de clientes (nomes, endereços, às vezes número de cartão falado). Nunca mandar áudio ou transcrição pra serviço de nuvem. A transcrição da própria CallRail exige um add-on pago que a conta não tem.
- **Áudio, `calls.json`, `lsa.json` e `transcripts.json` ficam em `_pessoal/call-wins/<slug>/`** (gitignored). Nunca copiar pra `clients/` nem commitar.
- **No log, nunca repetir números de cartão, CVV ou dados de pagamento**, mesmo que apareçam na transcrição. Escrever só "gave card details over the phone".
- **CallRail e Google Ads: só leitura.** Os scripts só fazem GET/search.
- **Rate limit da CallRail:** uma conta por vez, sem varrer as 122 empresas. Se der 429 repetido por mais de 1h numa conta só, ela provavelmente foi cancelada, não é limite normal.

## Passo a passo

Rodar da raiz do workspace. No Windows é `python`, no Mac `python3`.

### 1. Descobrir as contas do cliente

- **CallRail:** o slug precisa estar em `paid/funnels/clients.json` (11 clientes mapeados, cada um com `callrailAccount` + `callrailCompany`). Se não estiver, ver `tsd-callrail-api-access.md` e rodar com `--account ACC... --company COM... --out _pessoal/call-wins/<slug>`.
- **LSA:** o customer_id está em `LSA_ACCOUNTS` em `.claude/skills/google-ads-ratos/scripts/lsa_report.py`. Faltam lá: Napps `9239407401`, Spencer `2524618054`, King's `6769493219`.
- Na CallRail de King's e Neon Monkey as ligações de LSA **aparecem** (source "Google Local Services Ads"). Em C&S, Napps, All Seasons e Cool Hand **não aparecem**, então puxar pelo `pull_lsa.py`.

### 2. Puxar ligações e gravações

```bash
python .claude/skills/call-wins/scripts/pull_calls.py <slug> <início YYYY-MM-DD> <fim YYYY-MM-DD>
python .claude/skills/call-wins/scripts/pull_lsa.py <slug> <customer_id LSA> <início> <fim>   # quando o LSA não passa pela CallRail
```

Rodar de novo não baixa de novo o que já está lá. `--no-audio` puxa só a lista.

### 3. Transcrever

```bash
python .claude/skills/call-wins/scripts/transcribe.py _pessoal/call-wins/<slug>
```

Leva uns segundos por ligação (CPU). A primeira vez baixa o modelo (~500 MB). Pode interromper e rodar de novo, ele continua de onde parou. Se for muita ligação, rodar em background.

### 4. Analisar e escrever o log

Ler `calls.json` / `lsa.json` + `transcripts.json` e escrever:

- `clients/<slug>/call-wins-log.md`: ligações da CallRail atribuídas a ads.
- `clients/<slug>/lsa-call-wins-log.md`: só LSA (vindas do `pull_lsa.py` ou com source LSA na CallRail).

**O que entra como "ads":** ligação com `gclid`, ou source de Google Ads / Google Ads Extension / Local Services Ads / Meta / Facebook, ou do Website pool quando o número do pool só recebe tráfego pago (dizer no cabeçalho qual regra foi usada). Ligação orgânica (GMB/GBP sem gclid, direta) fica de fora, a não ser que peçam todas. Pra separar LSA, procurar `\bLSA\b|Local Services` **só no source/cabeçalho**: um `lsa` sem fronteira de palavra pega "Tulsa".

**Formato** (seguir os logs que já existem, ex. `clients/kings-window/call-wins-log.md`). Log em inglês:

1. Título `# <Client> — Call Wins Log` + 1 parágrafo de escopo: período, quantas ligações, regra de "ads", "transcribed locally with faster-whisper (small.en)", e o aviso de que nomes/ruas podem sair com erro de transcrição.
2. Legenda: `✅ Booked · ⏳ Open/follow-up needed · ❌ Not a lead · ⚠️ IVR-only`.
3. Uma seção `## YYYY-MM-DD` por dia. Cada ligação = 1 bullet: `**HH:MM · <dur>s · <source> · <city> (<name>)**`, depois 1 ou 2 frases do que aconteceu, depois o resultado com o motivo. Ligações repetidas do mesmo número seguidas podem virar 1 bullet.
4. LSA: 1 linha por lead (juntar as várias ligações do mesmo lead). Mostrar o status do Google (`BOOKED`, `ACTIVE`...) e se foi cobrado (`lead_charged` ausente = não cobrado) **ao lado** do resultado da transcrição, nunca no lugar. O "BOOKED" do Google é o que o cliente marcou no app, não prova nada.
5. Fechar com a tabela `## Running tally` (Outcome | Count | Detail) e um parágrafo **Flag for Edu** com o que importa: taxa real de job novo, ligações que caíram na caixa postal, leads quentes perdidos, número de rastreamento errado, metadata da CallRail que não bate com a transcrição.

**Como decidir o resultado:** só pelo que a transcrição mostra. Agendou visita/estimativa/serviço = ✅. Pediu orçamento, mandou foto, deixou recado com uma necessidade real = ⏳. Vendedor, engano, outra empresa, cancelamento, emprego = ❌. Só saudação/caixa postal sem recado = ⚠️. Ligação de cliente existente confirmando horário conta como ✅, mas dizer que não é pipeline novo. Na dúvida, ⏳ e dizer por quê.

Se o log já existe, acrescentar os dias novos e atualizar o tally (ou anotar no rodapé até que data o tally vai). Não reescrever o que já está lá.

### 5. Depois

- O que for acionável (lead quente parado, número quebrado, IVR demais) → doc em `followups` no Command Center (regras no `CLAUDE.md`).
- `/syncar` no fim. Confere que nada de `_pessoal/` entrou.

~~~~

### 7.2 `.claude/skills/call-wins/requirements.txt`

~~~~text
faster-whisper>=1.0

~~~~

### 7.3 `.claude/skills/call-wins/scripts/pull_lsa.py`

~~~~python
"""Pull one LSA account's leads + call recordings straight from Google Ads. Read-only.
For clients whose LSA calls never touch CallRail (C&S, Napps, All Seasons, Cool Hand...).

  python pull_lsa.py <client-slug> <customer_id> <start YYYY-MM-DD> <end YYYY-MM-DD> [--no-audio]

<customer_id> = the account holding LSA (see LSA_ACCOUNTS in google-ads-ratos/scripts/lsa_report.py;
missing there: Napps 9239407401, Spencer 2524618054, King's 6769493219).
Uses the person's own Google Ads login (.env.topserv), no tsd.sh needed.
Writes into _pessoal/call-wins/<slug>/ (gitignored):
  lsa.json                  leads (type, status, charged) each with its conversations (calls + messages)
  audio/lsa_<conv id>.mp3   one file per recorded call
Google "BOOKED" = whatever the business tapped in the LSA app: report it beside the transcript outcome, never instead."""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
RATOS = os.path.join(ROOT, ".claude", "skills", "google-ads-ratos")
os.environ.setdefault("GADS_ENV_PATH", os.path.join(RATOS, ".env.topserv"))
sys.path.insert(0, os.path.join(RATOS, "scripts"))
from lib import init_client, run_query  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("slug"); ap.add_argument("customer_id"); ap.add_argument("start"); ap.add_argument("end")
ap.add_argument("--no-audio", action="store_true")
a = ap.parse_args()
cid = a.customer_id.replace("-", "")
out = os.path.join(ROOT, "_pessoal", "call-wins", a.slug)
os.makedirs(os.path.join(out, "audio"), exist_ok=True)

leads = {}
for r in run_query(cid, f"""
    SELECT local_services_lead.resource_name, local_services_lead.id, local_services_lead.lead_type,
      local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.category_id,
      local_services_lead.service_id, local_services_lead.creation_date_time
    FROM local_services_lead
    WHERE local_services_lead.creation_date_time >= '{a.start} 00:00:00'
      AND local_services_lead.creation_date_time <= '{a.end} 23:59:59'"""):
    l = r["local_services_lead"]
    leads[l["resource_name"]] = {**l, "conversations": []}

# Conversations can come days after the lead was created, so no upper date bound here
for r in run_query(cid, f"""
    SELECT local_services_lead_conversation.id, local_services_lead_conversation.lead,
      local_services_lead_conversation.event_date_time, local_services_lead_conversation.conversation_channel,
      local_services_lead_conversation.participant_type,
      local_services_lead_conversation.phone_call_details.call_duration_millis,
      local_services_lead_conversation.phone_call_details.call_recording_url,
      local_services_lead_conversation.message_details.text
    FROM local_services_lead_conversation
    WHERE local_services_lead_conversation.event_date_time >= '{a.start} 00:00:00'"""):
    c = r["local_services_lead_conversation"]
    if c["lead"] in leads:
        leads[c["lead"]]["conversations"].append(c)

json.dump(list(leads.values()), open(os.path.join(out, "lsa.json"), "w", encoding="utf-8"), indent=1)
calls = [c for l in leads.values() for c in l["conversations"] if c.get("phone_call_details", {}).get("call_recording_url")]
print(f"{len(leads)} LSA leads, {len(calls)} recorded calls -> {out}")
if a.no_audio or not calls:
    sys.exit()

# Recording URLs 302 to a login page without auth; with the Ads OAuth bearer token they return audio/mpeg
import requests  # noqa: E402
from google.auth.transport.requests import Request  # noqa: E402
creds = init_client().credentials
creds.refresh(Request())
new = 0
for c in calls:
    fn = os.path.join(out, "audio", f"lsa_{c['id']}.mp3")
    if os.path.exists(fn):
        continue
    resp = requests.get(c["phone_call_details"]["call_recording_url"],
                        headers={"Authorization": f"Bearer {creds.token}"}, timeout=120)
    if resp.ok and "audio" in (resp.headers.get("content-type") or ""):
        open(fn, "wb").write(resp.content)
        new += 1
        print(f"  lsa_{c['id']}  {c['event_date_time'][:16]}", flush=True)
    else:
        print(f"  lsa_{c['id']} FAILED: HTTP {resp.status_code} {resp.headers.get('content-type')}", flush=True)
    time.sleep(0.3)
print(f"{new} new recordings downloaded")

~~~~

### 7.4 `.claude/skills/call-wins/scripts/pull_calls.py`

~~~~python
"""Pull one client's CallRail calls + recordings for a date range. Read-only (GET only).

  python pull_calls.py <client-slug> <start YYYY-MM-DD> <end YYYY-MM-DD> [--no-audio]
  python pull_calls.py --account ACC... --company COM... --out <dir> <start> <end>

<client-slug> = a key in paid/funnels/clients.json (holds each client's CallRail account + company id).
Writes into _pessoal/call-wins/<slug>/ (gitignored: recordings carry customer PII):
  calls.json          every call in the range, with source/gclid/recording metadata
  audio/<call id>.mp3 one file per call that has a recording
Re-running skips recordings already downloaded.
Builds the URL by hand: urlencode turns the commas in `fields` into %2C, which CallRail rejects (400)."""
import argparse, json, os, sys, time, urllib.error, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
FIELDS = ("source,source_name,medium,campaign,keywords,gclid,first_call,answered,duration,start_time,"
          "landing_page_url,utm_source,utm_medium,utm_campaign,recording,recording_duration,"
          "customer_name,customer_city,customer_state,tracking_phone_number,business_phone_number,lead_status,tags")

env = dict(l.strip().split("=", 1) for l in open(os.path.join(ROOT, ".env.callrail"), encoding="utf-8")
           if "=" in l and not l.startswith("#"))
KEY = env["CALLRAIL_API_KEY"]


def get(url, auth=True, raw=False, tries=6):
    headers = {"Authorization": f'Token token="{KEY}"'} if auth else {}
    for i in range(tries):
        try:
            resp = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120)
            return resp.read() if raw else json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                wait = 30 * (i + 1)
                print(f"  CallRail rate limit (429), waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            raise


ap = argparse.ArgumentParser()
ap.add_argument("args", nargs="+", help="<slug> <start> <end>, or <start> <end> with --account/--company/--out")
ap.add_argument("--account"); ap.add_argument("--company"); ap.add_argument("--out")
ap.add_argument("--no-audio", action="store_true", help="only calls.json, skip recordings")
a = ap.parse_args()

if a.account:
    start, end = a.args
    acc, comp, out = a.account, a.company, a.out
else:
    slug, start, end = a.args
    clients = json.load(open(os.path.join(ROOT, "paid", "funnels", "clients.json"), encoding="utf-8"))["clients"]
    if slug not in clients:
        sys.exit(f"'{slug}' not in paid/funnels/clients.json. Known: {', '.join(clients)}")
    acc, comp = clients[slug]["callrailAccount"], clients[slug]["callrailCompany"]
    out = os.path.join(ROOT, "_pessoal", "call-wins", slug)

os.makedirs(os.path.join(out, "audio"), exist_ok=True)

calls, page = [], 1
while True:
    d = get(f"https://api.callrail.com/v3/a/{acc}/calls.json?company_id={comp}&start_date={start}&end_date={end}"
            f"&per_page=250&page={page}&fields={FIELDS}")
    calls += d["calls"]
    if page >= d.get("total_pages", 1):
        break
    page += 1
    time.sleep(0.5)
json.dump(calls, open(os.path.join(out, "calls.json"), "w", encoding="utf-8"), indent=1)

recorded = [c for c in calls if c.get("recording") and (c.get("recording_duration") or 0)]
print(f"{len(calls)} calls, {len(recorded)} with a recording -> {out}")
if a.no_audio:
    sys.exit()

new = 0
for c in recorded:
    fn = os.path.join(out, "audio", f"{c['id']}.mp3")
    if os.path.exists(fn):
        continue
    try:
        link = get(c["recording"])["url"]  # API returns a pointer {"url": ...}, not the audio
        open(fn, "wb").write(get(link, auth=False, raw=True))
        new += 1
        print(f"  {c['id']}  {c.get('start_time', '')[:16]}  {c.get('source_name') or c.get('source')}", flush=True)
    except Exception as e:
        print(f"  {c['id']} FAILED: {e}", flush=True)
    time.sleep(0.3)
print(f"{new} new recordings downloaded")

~~~~

### 7.5 `.claude/skills/call-wins/scripts/transcribe.py`

~~~~python
"""Transcribe every recording in <dir>/audio/ locally with faster-whisper. Nothing leaves the machine.

  python transcribe.py <dir> [--model small.en]

<dir> = the client folder pull_calls.py / pull_lsa.py wrote (e.g. _pessoal/call-wins/kings-window).
Writes <dir>/transcripts.json  {"<call or lead id>": "[0:03] text\n[0:09] text ..."}
Saves after every file and skips ids already transcribed, so it can be stopped and re-run.
First run downloads the model (~500 MB, cached in ~/.cache/huggingface). CPU only, roughly 2-4x faster than real time."""
import argparse, glob, json, os, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--model", default="small.en", help="small.en (default) / medium.en (better names, ~3x slower)")
a = ap.parse_args()

try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit("faster-whisper missing: python -m pip install -r .claude/skills/call-wins/requirements.txt")

out_fn = os.path.join(a.dir, "transcripts.json")
done = json.load(open(out_fn, encoding="utf-8")) if os.path.exists(out_fn) else {}
todo = [f for f in sorted(glob.glob(os.path.join(a.dir, "audio", "*.mp3")))
        if os.path.splitext(os.path.basename(f))[0] not in done]
print(f"{len(done)} already transcribed, {len(todo)} to go", flush=True)
if not todo:
    sys.exit()

model = WhisperModel(a.model, device="cpu", compute_type="int8")
for i, fn in enumerate(todo, 1):
    cid = os.path.splitext(os.path.basename(fn))[0]
    t0 = time.time()
    try:
        segs, _ = model.transcribe(fn, beam_size=5, vad_filter=True)
        done[cid] = "\n".join(f"[{int(s.start) // 60}:{int(s.start) % 60:02d}] {s.text.strip()}" for s in segs)
    except Exception as e:
        print(f"  {cid} FAILED: {e}", flush=True)
        continue
    json.dump(done, open(out_fn, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  [{i}/{len(todo)}] {cid}  {time.time() - t0:.0f}s", flush=True)
print(f"DONE -> {out_fn}")

~~~~

### 7.6 `.claude/skills/google-ads-ratos/scripts/lib/__init__.py`

~~~~python
#!/usr/bin/env python3
"""
Google Ads Ratos - Biblioteca compartilhada
Auth (google-ads SDK), .env loader, GAQL runner, output helpers, error handling
"""

import json
import os
import sys
import time

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

def ensure_sdk():
    """Verifica se o google-ads SDK esta instalado."""
    try:
        import google.ads.googleads
        return True
    except ImportError:
        print("ERRO: SDK 'google-ads' nao instalado.", file=sys.stderr)
        print("  Instale com: pip3 install google-ads protobuf", file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------------------------
# .env loader (sem depender de python-dotenv)
# ---------------------------------------------------------------------------

_ENV_SEARCH_PATHS = [
    p for p in [
        # GADS_ENV_PATH escolhe o perfil (ex.: .env.topserv). Vence os padroes.
        os.environ.get("GADS_ENV_PATH"),
        os.path.expanduser("~/.claude/skills/google-ads-ratos/.env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
    ] if p
]

_YAML_SEARCH_PATHS = [
    os.path.expanduser("~/.claude/skills/google-ads-ratos/google-ads.yaml"),
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "google-ads.yaml"),
]


def _load_env_file():
    """Carrega variaveis de um .env sem precisar de source no zshrc."""
    for env_path in _ENV_SEARCH_PATHS:
        if os.path.isfile(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("export "):
                        line = line[7:]
                    if "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value and not os.environ.get(key):
                        os.environ[key] = value
            return env_path
    return None


def _find_yaml_path():
    """Encontra google-ads.yaml para fallback do SDK."""
    for yaml_path in _YAML_SEARCH_PATHS:
        if os.path.isfile(yaml_path):
            return yaml_path
    return None


def mask_token(token):
    """Mascara token pra nao vazar em logs/output. Mostra so os 6 primeiros chars."""
    if not token or len(token) < 10:
        return "***"
    return f"{token[:6]}...{token[-4:]}"


# ---------------------------------------------------------------------------
# Auth & SDK init
# ---------------------------------------------------------------------------

_client = None


def init_client():
    """Inicializa o GoogleAdsClient com .env ou google-ads.yaml."""
    global _client
    if _client is not None:
        return _client

    ensure_sdk()
    from google.ads.googleads.client import GoogleAdsClient

    # Tenta carregar do .env primeiro
    env_file = _load_env_file()

    dev_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_ADS_REFRESH_TOKEN")
    login_customer_id = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")

    if dev_token and client_id and client_secret and refresh_token:
        # Build from env vars
        config = {
            "developer_token": dev_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "use_proto_plus": True,
        }
        if login_customer_id:
            config["login_customer_id"] = login_customer_id.replace("-", "")

        _client = GoogleAdsClient.load_from_dict(config)
        source = env_file or "env vars"
        print(f"Client inicializado via {source} (token: {mask_token(dev_token)})", file=sys.stderr)
        return _client

    # Fallback: google-ads.yaml
    yaml_path = _find_yaml_path()
    if yaml_path:
        _client = GoogleAdsClient.load_from_storage(yaml_path)
        print(f"Client inicializado via {yaml_path}", file=sys.stderr)
        return _client

    print("ERRO: Credenciais Google Ads nao encontradas.", file=sys.stderr)
    print("  Crie o arquivo ~/.claude/skills/google-ads-ratos/.env com:", file=sys.stderr)
    print('  GOOGLE_ADS_DEVELOPER_TOKEN="seu-token"', file=sys.stderr)
    print('  GOOGLE_ADS_CLIENT_ID="seu-client-id"', file=sys.stderr)
    print('  GOOGLE_ADS_CLIENT_SECRET="seu-secret"', file=sys.stderr)
    print('  GOOGLE_ADS_REFRESH_TOKEN="seu-refresh-token"', file=sys.stderr)
    print('  GOOGLE_ADS_LOGIN_CUSTOMER_ID="1234567890"', file=sys.stderr)
    print("", file=sys.stderr)
    print("  Ou crie um google-ads.yaml na mesma pasta.", file=sys.stderr)
    print("  Ou rode: /google-ads-ratos setup", file=sys.stderr)
    sys.exit(1)


def get_default_customer_id():
    """Retorna o customer ID padrao da env var GOOGLE_ADS_CUSTOMER_ID."""
    _load_env_file()
    customer_id = os.environ.get("GOOGLE_ADS_CUSTOMER_ID")
    if not customer_id:
        print("ERRO: Nenhuma conta informada.", file=sys.stderr)
        print("  Use --customer-id 1234567890 ou defina GOOGLE_ADS_CUSTOMER_ID.", file=sys.stderr)
        sys.exit(1)
    return customer_id.replace("-", "")


def resolve_customer_id(args_customer_id=None):
    """Resolve customer ID: argumento CLI > env var."""
    if args_customer_id:
        return args_customer_id.replace("-", "")
    return get_default_customer_id()


# ---------------------------------------------------------------------------
# GAQL query runner
# ---------------------------------------------------------------------------

def run_query(customer_id, query):
    """Executa uma query GAQL e retorna lista de rows como dicts."""
    client = init_client()
    service = client.get_service("GoogleAdsService")

    results = []
    try:
        response = service.search(customer_id=customer_id, query=query)
        for row in response:
            results.append(_row_to_dict(row))
    except Exception as e:
        handle_google_error(e)

    return results


def _row_to_dict(row):
    """Converte uma row protobuf para dict legivel."""
    from google.protobuf.json_format import MessageToDict
    return MessageToDict(row._pb, preserving_proto_field_name=True)


# ---------------------------------------------------------------------------
# Cost conversion
# ---------------------------------------------------------------------------

def micros_to_currency(micros):
    """Converte cost_micros para valor monetario (/ 1_000_000)."""
    if micros is None:
        return 0.0
    try:
        return int(micros) / 1_000_000
    except (ValueError, TypeError):
        return 0.0


def format_cost(micros):
    """Formata cost_micros como string com 2 casas decimais."""
    return f"{micros_to_currency(micros):.2f}"


def convert_costs_in_row(row):
    """Converte todos os campos cost_micros de uma row para reais."""
    if not isinstance(row, dict):
        return row
    for key, value in list(row.items()):
        if isinstance(value, dict):
            convert_costs_in_row(value)
        elif key.endswith("_micros") or key == "amount_micros":
            row[key] = micros_to_currency(value)
            # Add a friendly key without _micros suffix
            friendly_key = key.replace("_micros", "")
            if friendly_key not in row:
                row[friendly_key] = row[key]
    return row


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def print_json(obj):
    """Serializa e printa qualquer objeto para stdout."""
    if isinstance(obj, list):
        obj = [convert_costs_in_row(row) for row in obj]
    elif isinstance(obj, dict):
        obj = convert_costs_in_row(obj)
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def print_error(msg):
    """Printa erro formatado para stderr."""
    print(f"ERRO: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def handle_google_error(error):
    """Trata erros do Google Ads API e exibe mensagem util."""
    ensure_sdk()
    from google.ads.googleads.errors import GoogleAdsException

    if isinstance(error, GoogleAdsException):
        error_data = {
            "error": True,
            "message": str(error),
            "errors": [],
        }
        for ga_error in error.failure.errors:
            err = {
                "error_code": str(ga_error.error_code),
                "message": ga_error.message,
            }
            if ga_error.location:
                err["field_path"] = str(ga_error.location)
            error_data["errors"].append(err)

        # Rate limiting
        if "RESOURCE_EXHAUSTED" in str(error):
            error_data["hint"] = "Rate limit atingido. Aguarde alguns minutos antes de tentar novamente."

        # Auth errors
        if "AUTHENTICATION_ERROR" in str(error) or "AUTHORIZATION_ERROR" in str(error):
            error_data["hint"] = "Erro de autenticacao. Verifique developer_token, refresh_token e permissoes."

        # Permission
        if "PERMISSION_DENIED" in str(error):
            error_data["hint"] = "Sem permissao. Verifique se o login_customer_id (MCC) tem acesso a esta conta."

        print(json.dumps(error_data, indent=2, ensure_ascii=False, default=str))
        sys.exit(1)
    else:
        print_error(str(error))
        sys.exit(1)


def handle_google_error_decorator(func):
    """Decorator que trata erros do Google Ads API."""
    def wrapper(*args, **kwargs):
        ensure_sdk()
        from google.ads.googleads.errors import GoogleAdsException
        try:
            return func(*args, **kwargs)
        except GoogleAdsException as e:
            handle_google_error(e)
        except Exception as e:
            print_error(str(e))
            sys.exit(1)
    return wrapper


# ---------------------------------------------------------------------------
# Rate limiting helpers
# ---------------------------------------------------------------------------

def safe_delay(seconds=1):
    """Delay entre operacoes de escrita para evitar rate limiting."""
    time.sleep(seconds)


# ---------------------------------------------------------------------------
# Common argparse helpers
# ---------------------------------------------------------------------------

def add_customer_arg(parser, required=False):
    """Adiciona argumento --customer-id ao parser."""
    parser.add_argument(
        "--customer-id",
        required=required,
        help="Google Ads customer ID (sem hifens). Padrao: GOOGLE_ADS_CUSTOMER_ID"
    )


def add_date_args(parser):
    """Adiciona argumentos de data ao parser."""
    parser.add_argument(
        "--date-range",
        default="LAST_30_DAYS",
        help="Periodo: LAST_7_DAYS, LAST_14_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH, etc (default: LAST_30_DAYS)"
    )
    parser.add_argument("--since", help="Data inicio (YYYY-MM-DD)")
    parser.add_argument("--until", help="Data fim (YYYY-MM-DD)")


def add_limit_arg(parser, default=None):
    """Adiciona argumento --limit ao parser."""
    parser.add_argument("--limit", type=int, default=default, help="Limite de resultados")


def add_campaign_filter(parser):
    """Adiciona argumento --campaign-id ao parser."""
    parser.add_argument("--campaign-id", help="Filtrar por campaign ID")


def build_date_clause(args):
    """Constroi clausula WHERE de data a partir dos argumentos."""
    if hasattr(args, "since") and args.since and hasattr(args, "until") and args.until:
        return f"segments.date BETWEEN '{args.since}' AND '{args.until}'"
    # Map friendly names to GAQL date ranges
    date_range = getattr(args, "date_range", "LAST_30_DAYS")
    return f"segments.date DURING {date_range}"


def parse_json_arg(json_str, arg_name="argumento"):
    """Faz parse de um argumento JSON string."""
    if not json_str:
        return None
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print_error(f"JSON invalido no argumento {arg_name}: {e}")
        sys.exit(1)

~~~~

### 7.7 `.claude/skills/google-ads-ratos/scripts/tsd.sh`

~~~~bash
#!/usr/bin/env bash
# Roda qualquer script da skill no perfil TopServ (MCC 4155514468),
# sem tocar no .env default da skill.
#
#   ./tsd.sh setup.py oauth
#   ./tsd.sh setup.py test
#   ./tsd.sh read.py campaigns --customer-id 9205826499 --date-range LAST_30_DAYS
#   ./tsd.sh insights.py account --customer-id 8634274092 --date-range LAST_7_DAYS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export GADS_ENV_PATH="$(dirname "$SCRIPT_DIR")/.env.topserv"
export PYTHONUNBUFFERED=1
export PYTHONUTF8=1   # Windows: UTF-8 em arquivos e no terminal (acentos/emoji)

# Mac: python3. Windows: python (o "python3" de lá costuma ser o atalho da Microsoft Store)
PY=python3
"$PY" -c "import sys" >/dev/null 2>&1 || PY=python

if [[ ! -f "$GADS_ENV_PATH" ]]; then
  echo "ERRO: perfil nao encontrado em $GADS_ENV_PATH" >&2
  exit 1
fi

cd "$SCRIPT_DIR"

# setup.py e interativo (browser + prompts): nao filtrar, nao mexer no stdout.
if [[ "${1:-}" == "setup.py" ]]; then
  exec "$PY" "$@"
fi

"$PY" "$@" 2>&1 \
  | grep -v "Warning\|warnings.warn\|site-packages\|eol_message\|Request made\|Client inicializado" \
  || true

~~~~

### 7.8 `.claude/skills/google-ads-ratos/requirements.txt`

~~~~text
# Versões que rodam no Mac do Edu (Python 3.9). No Windows, usar Python 3.12. Instalar com:
#   Windows: python -m pip install -r .claude/skills/google-ads-ratos/requirements.txt && python -m playwright install chromium
#   Mac:     pip3 install --user -r .claude/skills/google-ads-ratos/requirements.txt && python3 -m playwright install chromium
google-ads==31.1.0
google-auth-oauthlib==1.3.1
google-api-python-client==2.198.0
playwright==1.60.0

~~~~

### 7.9 `.claude/skills/google-ads-ratos/scripts/lsa_report.py`

~~~~python
#!/usr/bin/env python3
"""
LSA lead report — todos os clientes TSD com presenca em Local Services Ads.

Roda local_services_lead.* (nao e metrics de PPC) em cada conta que carrega
LSA, seja dentro da mesma conta de PPC (campanha LOCAL_SERVICES) ou em uma
conta LSA dedicada. Lista vem de contas.yaml, curada manualmente abaixo —
atualizar aqui quando um cliente novo ligar LSA ou uma conta LSA fechar.

Uso:
    ./tsd.sh lsa_report.py                     # ultimos 30 dias, todas as contas
    ./tsd.sh lsa_report.py --days 7
    ./tsd.sh lsa_report.py --since 2026-08-01 --until 2026-08-25
    ./tsd.sh lsa_report.py --client "Watt's Right"   # filtra por nome (substring)
"""

import argparse
import sys
from datetime import date, timedelta

sys.path.insert(0, ".")
from lib import init_client

# ---------------------------------------------------------------------------
# Registro de contas com LSA (curado a partir de contas.yaml, 2026-08-25)
# ---------------------------------------------------------------------------
# mode: "same_account"  -> campanha LOCAL_SERVICES vive dentro da conta de PPC
#       "dedicated"      -> customer_id e uma conta so de LSA

LSA_ACCOUNTS = [
    {"client": "Cool Hand Electric", "customer_id": "9865206319", "mode": "same_account",
     "note": "LSA existe mas fora do escopo TSD (decisao do Edu) — leitura de dados ok."},
    {"client": "Mission Accomplished", "customer_id": "4904262993", "mode": "dedicated",
     "note": "PPC: 8634274092"},
    {"client": "Hawkins Siding and Exterior", "customer_id": "2198608170", "mode": "same_account",
     "note": "Campanha LSA 21211420266"},
    {"client": "Neon Monkey Services", "customer_id": "1219885876", "mode": "dedicated",
     "note": "PPC: 7953905280"},
    {"client": "Golden Plumbing", "customer_id": "4193142570", "mode": "same_account",
     "note": "Campanha LSA 21051260085, LSA ATIVA mesmo com PPC pausado"},
    {"client": "Zen Air Heating and Cooling", "customer_id": "3740502923", "mode": "dedicated",
     "note": "PPC: 4360840956"},
    {"client": "C&S Air", "customer_id": "5563867754", "mode": "same_account",
     "note": "Conta se chama '(LSA) C&S Air' mas tem PPC completo dentro"},
    {"client": "Gillespie's Heating and Cooling", "customer_id": "7410489772", "mode": "same_account",
     "note": "Campanha LSA 23940351598, near-zero volume, fora do escopo PPC"},
    {"client": "Watt's Right Electric", "customer_id": "3651667805", "mode": "same_account",
     "note": "~86% do spend/leads da conta"},
    {"client": "Watt's Right - Broken Arrow (sister)", "customer_id": "9261944882", "mode": "dedicated",
     "note": "Dormant, zero spend historicamente — checar mesmo assim"},
    {"client": "Proud Pops Plumbing, Air & Electric", "customer_id": "1051843378", "mode": "same_account",
     "note": "Campanha LOCAL_SERVICES:SystemGenerated dentro da conta PPC"},
    {"client": "Proud Pops - LSA San Antonio [1]", "customer_id": "7261668241", "mode": "dedicated",
     "note": "Eletricista, Boerne/Helotes/Seguin TX"},
    {"client": "Proud Pops - LSA San Antonio [2]", "customer_id": "6621969129", "mode": "dedicated",
     "note": "HVAC, Bandera/Converse/Kerrville TX"},
    {"client": "My Favorite Service Company - LSA New Braunfels", "customer_id": "4127524472", "mode": "dedicated",
     "note": "Sem spend desde fev/2026 — checar mesmo assim"},
    {"client": "My Favorite Service Company - LSA San Antonio", "customer_id": "4905286019", "mode": "dedicated",
     "note": "Sem spend desde fev/2026 — checar mesmo assim"},
    {"client": "All Seasons AC", "customer_id": "8655979348", "mode": "dedicated",
     "note": "PPC: 4467722415. LSA live sob o MCC desde 2026-10-14 (faltavam docs de verificacao)"},
]


def build_query(since, until):
    return f"""
        SELECT
            local_services_lead.id,
            local_services_lead.lead_type,
            local_services_lead.lead_status,
            local_services_lead.lead_charged,
            local_services_lead.credit_details.credit_state
        FROM local_services_lead
        WHERE local_services_lead.creation_date_time >= '{since} 00:00:00'
            AND local_services_lead.creation_date_time <= '{until} 23:59:59'
    """


def fetch_leads(client, customer_id, query):
    """Roda a query numa conta, sem derrubar o loop se a conta der erro."""
    service = client.get_service("GoogleAdsService")
    try:
        response = service.search(customer_id=customer_id, query=query)
        rows = []
        for row in response:
            lead = row.local_services_lead
            rows.append({
                "lead_type": lead.lead_type.name if lead.lead_type else "UNSPECIFIED",
                "lead_status": lead.lead_status.name if lead.lead_status else "UNSPECIFIED",
                "lead_charged": bool(lead.lead_charged),
                "credit_state": lead.credit_details.credit_state.name if lead.credit_details.credit_state else None,
            })
        return rows, None
    except Exception as e:
        return None, str(e).splitlines()[0][:180]


def summarize(rows):
    total = len(rows)
    charged = sum(1 for r in rows if r["lead_charged"])
    by_type = {}
    by_status = {}
    credited = 0
    for r in rows:
        by_type[r["lead_type"]] = by_type.get(r["lead_type"], 0) + 1
        by_status[r["lead_status"]] = by_status.get(r["lead_status"], 0) + 1
        if r["credit_state"] and r["credit_state"] not in ("UNSPECIFIED", "UNKNOWN", None):
            credited += 1
    return total, charged, by_type, by_status, credited


def main():
    ap = argparse.ArgumentParser(description="Relatorio global de leads LSA — todas as contas TSD")
    ap.add_argument("--days", type=int, default=30, help="Janela em dias a partir de hoje (default: 30)")
    ap.add_argument("--since", help="Data inicio (YYYY-MM-DD)")
    ap.add_argument("--until", help="Data fim (YYYY-MM-DD)")
    ap.add_argument("--client", help="Filtra por nome do cliente (substring, case-insensitive)")
    args = ap.parse_args()

    if args.since and args.until:
        since, until = args.since, args.until
    else:
        until_d = date.today()
        since_d = until_d - timedelta(days=args.days)
        since, until = since_d.isoformat(), until_d.isoformat()

    accounts = LSA_ACCOUNTS
    if args.client:
        needle = args.client.lower()
        accounts = [a for a in accounts if needle in a["client"].lower()]
        if not accounts:
            print(f"Nenhuma conta LSA cadastrada bate com '{args.client}'.")
            sys.exit(1)

    client = init_client()
    query = build_query(since, until)

    print("=" * 100)
    print(f"LSA LEAD REPORT — {since} a {until}  ({len(accounts)} conta(s))")
    print("=" * 100)

    grand_total = 0
    grand_charged = 0
    grand_credited = 0
    errors = []

    for acc in accounts:
        rows, err = fetch_leads(client, acc["customer_id"], query)
        print(f"\n{acc['client']}  (customer_id {acc['customer_id']}, {acc['mode']})")
        if acc.get("note"):
            print(f"  note: {acc['note']}")
        if err:
            print(f"  ERRO: {err}")
            errors.append((acc["client"], err))
            continue

        total, charged, by_type, by_status, credited = summarize(rows)
        grand_total += total
        grand_charged += charged
        grand_credited += credited

        if total == 0:
            print("  0 leads no periodo.")
            continue

        type_str = ", ".join(f"{k}={v}" for k, v in sorted(by_type.items(), key=lambda x: -x[1]))
        status_str = ", ".join(f"{k}={v}" for k, v in sorted(by_status.items(), key=lambda x: -x[1]))
        print(f"  total={total}  charged={charged} ({charged/total:.0%})  credited/disputed={credited}")
        print(f"  by_type: {type_str}")
        print(f"  by_status: {status_str}")

    print("\n" + "=" * 100)
    print(f"TOTAL (todas as contas listadas): {grand_total} leads, {grand_charged} charged, {grand_credited} credited/disputed")
    if errors:
        print(f"\n{len(errors)} conta(s) com erro (ver acima) — provavel CUSTOMER_NOT_ENABLED ou sem campanha LOCAL_SERVICES ativa.")
    print("=" * 100)


if __name__ == "__main__":
    main()

~~~~

### 7.10 `.claude/skills/google-ads-ratos/scripts/lsa_health_check.py`

~~~~python
#!/usr/bin/env python3
"""LSA health check across all TSD accounts: verification artifacts
(license/insurance/background check/business registration) + campaign
primary_status, reduced to CURRENT state (not full history) and flagged
for anything that looks like it's blocking delivery."""
import sys
from datetime import datetime, date
sys.path.insert(0, ".")
from lib import init_client

LSA_ACCOUNTS = [
    {"client": "Cool Hand Electric", "customer_id": "9865206319"},
    {"client": "Mission Accomplished", "customer_id": "4904262993"},
    {"client": "Hawkins Siding and Exterior", "customer_id": "2198608170"},
    {"client": "Neon Monkey Services", "customer_id": "1219885876"},
    {"client": "Golden Plumbing", "customer_id": "4193142570"},
    {"client": "Zen Air Heating and Cooling", "customer_id": "3740502923"},
    {"client": "C&S Air", "customer_id": "5563867754"},
    {"client": "Gillespie's Heating and Cooling", "customer_id": "7410489772"},
    {"client": "Watt's Right Electric", "customer_id": "3651667805"},
    {"client": "Watt's Right - Broken Arrow (sister)", "customer_id": "9261944882"},
    {"client": "Proud Pops Plumbing, Air & Electric", "customer_id": "1051843378"},
    {"client": "Proud Pops - LSA San Antonio [1]", "customer_id": "7261668241"},
    {"client": "Proud Pops - LSA San Antonio [2]", "customer_id": "6621969129"},
    {"client": "My Favorite Service Company - LSA New Braunfels", "customer_id": "4127524472"},
    {"client": "My Favorite Service Company - LSA San Antonio", "customer_id": "4905286019"},
    {"client": "All Seasons AC (LSA)", "customer_id": "8655979348"},
]

VERIF_QUERY = """
    SELECT
        local_services_verification_artifact.id,
        local_services_verification_artifact.status,
        local_services_verification_artifact.artifact_type,
        local_services_verification_artifact.creation_date_time,
        local_services_verification_artifact.license_verification_artifact.license_type,
        local_services_verification_artifact.license_verification_artifact.rejection_reason,
        local_services_verification_artifact.license_verification_artifact.expiration_date_time,
        local_services_verification_artifact.insurance_verification_artifact.rejection_reason,
        local_services_verification_artifact.insurance_verification_artifact.expiration_date_time,
        local_services_verification_artifact.business_registration_check_verification_artifact.rejection_reason
    FROM local_services_verification_artifact
"""

CAMPAIGN_QUERY = """
    SELECT
        campaign.id, campaign.name, campaign.status,
        campaign.primary_status, campaign.primary_status_reasons,
        campaign.serving_status,
        metrics.impressions, metrics.clicks
    FROM campaign
    WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES'
        AND campaign.status != 'REMOVED'
        AND segments.date DURING LAST_30_DAYS
"""

TODAY = date(2026, 8, 27)

def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.strptime(s.split(".")[0], "%Y-%m-%d %H:%M:%S").date()
    except Exception:
        return None

def main():
    client = init_client()
    service = client.get_service("GoogleAdsService")

    all_flags = []

    for acc in LSA_ACCOUNTS:
        name, cid = acc["client"], acc["customer_id"]
        flags = []

        # --- campaign status ---
        try:
            rows = list(service.search(customer_id=cid, query=CAMPAIGN_QUERY))
        except Exception as e:
            flags.append(f"CAMPAIGN QUERY ERROR: {str(e).splitlines()[0][:180]}")
            rows = []
        for row in rows:
            c = row.campaign
            reasons = [r.name for r in c.primary_status_reasons] if c.primary_status_reasons else []
            if c.status.name == "PAUSED":
                flags.append(f"Campaign PAUSED (reasons={reasons})")
            elif c.primary_status.name not in ("ELIGIBLE",):
                flags.append(f"Campaign primary_status={c.primary_status.name} reasons={reasons}")

        # --- verification artifacts ---
        try:
            vrows = list(service.search(customer_id=cid, query=VERIF_QUERY))
        except Exception as e:
            flags.append(f"VERIFICATION QUERY ERROR: {str(e).splitlines()[0][:180]}")
            vrows = []

        by_type = {}
        for row in vrows:
            a = row.local_services_verification_artifact
            t = a.artifact_type.name
            by_type.setdefault(t, []).append(a)

        for t in ("LICENSE", "INSURANCE", "BUSINESS_REGISTRATION_CHECK", "BACKGROUND_CHECK"):
            arts = by_type.get(t, [])
            if not arts:
                continue
            # latest PASSED artifact by expiration date (the credential currently on file)
            passed = [a for a in arts if a.status.name == "PASSED"]
            latest_created = max(arts, key=lambda a: a.creation_date_time)

            if t == "LICENSE":
                exp = lambda a: parse_dt(a.license_verification_artifact.expiration_date_time)
            elif t == "INSURANCE":
                exp = lambda a: parse_dt(a.insurance_verification_artifact.expiration_date_time)
            else:
                exp = lambda a: None

            if not passed:
                flags.append(f"{t}: NO PASSED artifact on record — latest attempt status={latest_created.status.name}")
                continue

            best_passed = max(passed, key=lambda a: exp(a) or date.min)
            best_exp = exp(best_passed)
            if best_exp and best_exp < TODAY:
                flags.append(f"{t}: current on-file credential EXPIRED on {best_exp} (no newer PASSED replacement)")
            elif best_exp and (best_exp - TODAY).days <= 30:
                flags.append(f"{t}: current on-file credential expires SOON, {best_exp} ({(best_exp - TODAY).days}d) — no newer PASSED renewal on file yet")
            # latest submission overall is not passed and is newer than the best passed one -> stuck renewal
            if latest_created.status.name not in ("PASSED",) and latest_created.creation_date_time > best_passed.creation_date_time:
                lt = ""
                if t == "LICENSE":
                    lt = latest_created.license_verification_artifact.rejection_reason.name
                elif t == "INSURANCE":
                    lt = latest_created.insurance_verification_artifact.rejection_reason.name
                flags.append(f"{t}: latest renewal attempt ({latest_created.creation_date_time[:10]}) status={latest_created.status.name} rejection={lt} — valid credential still on file until {best_exp}, but renewal is stuck")

        if flags:
            all_flags.append((name, cid, flags))

    print("="*100)
    print(f"LSA HEALTH CHECK — {len(LSA_ACCOUNTS)} contas, hoje={TODAY}")
    print("="*100)
    if not all_flags:
        print("Nenhum problema encontrado.")
    for name, cid, flags in all_flags:
        print(f"\n{name}  ({cid})")
        for f in flags:
            print(f"  - {f}")
    print("\n" + "="*100)

if __name__ == "__main__":
    main()

~~~~

### 7.11 `.claude/skills/google-ads-ratos/scripts/proud_pops_lsa_lead_handling.py`

~~~~python
"""
Proud Pops — LSA lead handling (checklist D3 / AM item P-6). Read-only.
Lead-level detail for the 3 live LSA surfaces, Jun 1 → today. NO consumer contact details, recordings or message text
are selected (PII stays out). Per lead: date, type, status, charged, credit/dispute state, job type, and from the
conversation log: call duration (0s = likely missed) and whether the business replied to messages.

Run: ./tsd.sh proud_pops_lsa_lead_handling.py
"""
import sys, os, datetime
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query

SURFACES = {"1051843378": "in-account (PPC acct)", "7261668241": "LSA [1] Electrician", "6621969129": "LSA [2] HVAC"}
SINCE = "2026-06-01 00:00:00"


def leads_for(cid):
    rows = run_query(cid, f"""SELECT local_services_lead.resource_name, local_services_lead.id, local_services_lead.creation_date_time,
local_services_lead.lead_type, local_services_lead.lead_status, local_services_lead.lead_charged, local_services_lead.category_id,
local_services_lead.service_id, local_services_lead.credit_details.credit_state, local_services_lead.lead_feedback_submitted
FROM local_services_lead WHERE local_services_lead.creation_date_time >= '{SINCE}'""")
    return [r["local_services_lead"] for r in rows]


def convs_for(cid):
    try:
        rows = run_query(cid, f"""SELECT local_services_lead_conversation.lead, local_services_lead_conversation.conversation_channel,
local_services_lead_conversation.participant_type, local_services_lead_conversation.event_date_time,
local_services_lead_conversation.phone_call_details.call_duration_millis
FROM local_services_lead_conversation WHERE local_services_lead_conversation.event_date_time >= '{SINCE}'""")
    except SystemExit:
        return None
    by = defaultdict(list)
    for r in rows:
        c = r["local_services_lead_conversation"]; by[c.get("lead")].append(c)
    return by


def bucket(ms):
    if ms is None: return "n/a"
    s = int(ms) / 1000
    return "0s" if s == 0 else "<30s" if s < 30 else "30-60s" if s < 60 else "60s+"


all_rows = []
for cid, name in SURFACES.items():
    leads = leads_for(cid); convs = convs_for(cid)
    print(f"\n######## {cid} {name}: {len(leads)} leads since Jun 1  (conversation data: {'yes' if convs is not None else 'NOT AVAILABLE'})")
    for l in leads:
        conv = (convs or {}).get(l["resource_name"], [])
        calls = [c for c in conv if str(c.get("conversation_channel")) == "PHONE_CALL"]
        durs = [c.get("phone_call_details", {}).get("call_duration_millis") for c in calls]
        maxdur = max((int(d) for d in durs if d is not None), default=None)
        msgs = [c for c in conv if str(c.get("conversation_channel")) == "MESSAGE"]
        replied = any(str(c.get("participant_type")) == "ADVERTISER" for c in msgs) if msgs else None
        row = dict(cid=cid, surface=name, date=l["creation_date_time"][:16], month=l["creation_date_time"][:7], type=str(l.get("lead_type")),
                   status=str(l.get("lead_status")), charged=bool(l.get("lead_charged")),
                   credit=str(l.get("credit_details", {}).get("credit_state", "")), cat=str(l.get("category_id", "")).replace("xcat:service_area_business_", ""),
                   svc=str(l.get("service_id", "")), call=bucket(maxdur) if calls else "", n_calls=len(calls), replied=replied,
                   feedback=bool(l.get("lead_feedback_submitted")))
        all_rows.append(row)

print("\n\n==================== MONTHLY SUMMARY (all 3 surfaces) ====================")
by_m = defaultdict(list)
for r in all_rows: by_m[r["month"]].append(r)
for m in sorted(by_m):
    rs = by_m[m]
    calls = [r for r in rs if r["type"] == "PHONE_CALL"]
    print(f"{m}: leads {len(rs):3d} | calls {len(calls):3d} (call length: {dict(Counter(r['call'] for r in calls))}) "
          f"| status {dict(Counter(r['status'] for r in rs))} | charged {sum(r['charged'] for r in rs)} "
          f"| credit {dict(Counter(r['credit'] for r in rs if r['credit']))}")

print("\n==================== SEPTEMBER + OCTOBER, lead by lead (no contact details) ====================")
for r in sorted((r for r in all_rows if r["month"] >= "2026-09"), key=lambda r: r["date"]):
    extra = f"call {r['call']} ({r['n_calls']} call event(s))" if r["type"] == "PHONE_CALL" else (f"business replied: {r['replied']}" if r["type"] == "MESSAGE" else "")
    print(f"  {r['date']}  {r['surface']:22s} {r['type']:11s} {r['status']:10s} {'charged' if r['charged'] else 'not charged':11s} "
          f"credit={r['credit'] or '-':10s} job={r['cat']}/{r['svc']}  {extra}")

print("\n==================== SEPTEMBER: what needs explaining ====================")
sep = [r for r in all_rows if r["month"] == "2026-09"]
for label, cond in (("declined", lambda r: r["status"] == "DECLINED"),
                    ("not charged", lambda r: not r["charged"]),
                    ("calls 0s (likely missed)", lambda r: r["type"] == "PHONE_CALL" and r["call"] == "0s"),
                    ("calls under 30s", lambda r: r["type"] == "PHONE_CALL" and r["call"] == "<30s"),
                    ("messages with no business reply", lambda r: r["type"] == "MESSAGE" and r["replied"] is False)):
    hit = [r for r in sep if cond(r)]
    print(f"  {label:32s} {len(hit):2d}  " + ", ".join(f"{r['date'][5:10]} {r['surface'].split()[1] if ' ' in r['surface'] else r['surface']}" for r in hit))

~~~~

*End of handoff. Nothing in section 7 was modified from the repo state on 2026-11-11.*
