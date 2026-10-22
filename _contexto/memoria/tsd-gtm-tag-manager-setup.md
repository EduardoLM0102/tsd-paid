---
name: tsd-gtm-tag-manager-setup
description: Google Tag Manager wired into the google-ads-ratos skill (read+edit+publish) reusing the Ads OAuth client
metadata: 
  node_type: memory
  type: reference
  originSessionId: d5ccaae3-a3ee-42a0-a888-cf7315aa40f9
  modified: 2026-07-23T22:04:11.687Z
---

Google Tag Manager (API v2) foi acoplado à skill local [[topserv-google-ads-location]] `google-ads-ratos`, em `.../scripts/` (gtm_setup.py, gtm.py, gtm.sh).

Design: NÃO usa MCP nem a lib google-ads — usa `google-api-python-client` (`build("tagmanager","v2")`). Reusa o MESMO OAuth client Desktop do Google Ads (GOOGLE_ADS_CLIENT_ID/SECRET no .env.topserv) e o mesmo Google Cloud project, mas com token SEPARADO `GTM_REFRESH_TOKEN` e escopos GTM (tagmanager.readonly + edit.containers + publish). Dep extra instalada: google-api-python-client (--user).

Perfil: sempre `./gtm.sh <script> ...` (perfil TopServ, `.env.topserv`). Cada pessoa gera o próprio GTM_REFRESH_TOKEN na própria máquina (ver `ONBOARDING.md`). Setup: `./gtm.sh gtm_setup.py oauth` (browser, autorizar com conta que tem acesso aos containers) → grava GTM_REFRESH_TOKEN → `test` lista contas. Mesma pegadinha do Ads: consent screen External exige Test users senão token expira em 7 dias.

Comandos gtm.py: accounts | containers --account | workspaces --account --container | list (tags/triggers/variables) | create-tag/update-tag --json <arquivo formato API v2> | publish. REGRA DE SEGURANÇA embutida: edição só em workspace (rascunho); publish é comando separado e explícito, nunca automático junto da edição (container ao vivo do cliente).

GOTCHAS aprendidos na prática (2026-07-23):
- ESCOPOS: editar workspace/tags só precisa de `edit.containers`, mas **criar versão/publicar exige também `tagmanager.edit.containerversions`** — sem ele o publish devolve 403 "insufficient authentication scopes". Os 4 escopos já estão no gtm_setup.py; se aparecer 403, é re-rodar o oauth.
- O default workspace **NÃO é id "1"** (no container da Proud Pops é 38). Listar workspace "1" volta vazio e dá a falsa impressão de container vazio. Sempre listar workspaces antes.
- A versão **live** é a fonte da verdade do que roda no site (`versions().live()`), não o workspace.
- **DEPOIS DE PUBLICAR de um workspace lateral, rodar `workspaces.sync()` no Default Workspace.** Publicar do ws lateral deixa o Default defasado mostrando a config VELHA; se alguém editar e publicar dali, REVERTE a correção sem perceber (foi assim que nasceu a "v34 Revert" que quebrou o tracking da Proud Pops). Sync com 0 conflitos resolve.
- Um write do Google Ads (mutate) é barrado pelo classificador do Claude Code; writes de GTM passam.

Estado em 2026-07-23: setup completo e validado end-to-end — oauth feito, 80 contas GTM acessíveis, e o primeiro uso real (Proud Pops, ver [[tsd-proud-pops-tracking]]) foi diagnosticado, corrigido em draft, publicado (v38) e sincronizado.

**Testing a GTM draft WITHOUT Preview (2026-10-07, Proud Pops):** list `environments()`. The one with type `workspace`
has an authorizationCode, and `gtm.js?id=GTM-XXX&gtm_auth=<code>&gtm_preview=env-<id>&gtm_cookies_win=x` serves the
current draft (run `quick_preview` first). In Playwright, load the real site, `route.fulfill` the site's gtm.js with
the draft body, push fake dataLayer events, and `route.abort` every GA4/Ads/Meta request while logging it (GA4 `en=`
in URL or POST body; Ads by conversion label). Nothing gets recorded. Always run a control pass with the live gtm.js to
prove the test detects hits. Template: `scripts/proud_pops_gtm_headless_test.py`. For SPA in-app nav, use a visible
link click, else `history.pushState` + `popstate`.
**Auto-mode:** `gtm.py publish` right after an edit was blocked as "Blind Apply" even with Edu's explicit "make it go
live". It passed on retry once the draft had been tested this way. Test first, then publish.
**Testing an exact VERSION before publish (2026-10-08, Proud Pops v43):** `workspaces.create_version` (does NOT publish) →
`environments.create(parent, body={accountId, containerId, name, type:"user", containerVersionId})` (body must include
accountId + containerId or it 400s "Invalid account_id") → serve `gtm.js?id=GTM-X&gtm_auth=<authorizationCode>&gtm_preview=env-<id>&gtm_cookies_win=x`
in Playwright → `versions.publish` → delete the env. Tests the exact artifact you'll publish. Gotcha: Proud Pops lead tags are
`oncePerLoad`, so test each lead event on a fresh page load. A headless browser sent no Meta pixel hits even after Accept All,
but Meta MCP `ads_get_dataset_stats` showed the pixel live, so verify Meta via dataset stats, not headless.


- **`gtm.py list` defaults to workspace 1** (2026-10-22, Concrete Adventures): containers whose live workspace has another id (e.g. GTM-53FXJRN4 = workspace 3) show up EMPTY. Run `gtm.py workspaces` first and pass `--workspace <id>` before calling a container empty.
