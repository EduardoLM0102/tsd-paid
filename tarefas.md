# Tarefas — TopServ (Paid Ads)

## Ofertas de fim de ano — doc pra Angela (Edu, 2026-11-05, Command Center fu-130 / fu-131)
- [ ] Revisar o doc "Holiday Offers: Client Talking Points" (https://claude.ai/artifact/BhgrN7NA698kd8412qQCGQ) e mandar pra Angela (Morrow vai pela Marlo).
- [ ] Até 11-13: juntar as aprovações por escrito (oferta, preço, data final) via ticket AT; montar os anúncios pra lançar na semana de 11-16.
- Contexto completo: `_contexto/memoria/tsd-eoy-2026-seasonal-offers.md`.

## Nick's — pedir landing page de aquecimento (Edu, HOJE 2026-11-04, Command Center fu-125)
- [ ] Pedir a landing page de aquecimento da Nick's (Hammond, LA): 1 serviço por página (ex.: Furnace & Heating Repair in Hammond, LA), H1 = keyword do anúncio + cidade, número CallRail do grupo de anúncio em destaque, marca real (padrão do rollout de LPs, `_contexto/memoria/tsd-landing-page-rollout.md`). Hoje o NB da Nick's é só AC e está quase parado; o grupo de aquecimento (+ negativas for sale, in store, deals, evaporator core, why isn't, why won't) só entra quando a página existir. Depois: decidir PMax $50 → $35 e +$15 no NB heating (fu-124, 11-11).

## ICS — ligação de anúncio cai no menu da central (Edu → AM, até 10-30, Command Center fu-110) — AT 5e5dcc2a SUBMETIDO, em Execution com a Angela (visto 11-04)
- [ ] Abrir ticket pro AM: todas as ligações de anúncio (call extension do Google Ads, LSA, números do site) caem no menu da ICS (8 opções + diretório, 45–60s) e não direto num atendente. De 10-01 a 10-28: 31 ligações de anúncio, 3 jobs novos, 24 desligaram no menu sem falar com ninguém. Quem escolhe "service" é atendido em ~10s (Jason/Jerry), então o problema é o menu, não a equipe.
- [ ] Pedido pra ICS: apontar os números de rastreamento dos anúncios direto pra linha de service/sales (sem menu, dá pra mudar o destino na CallRail) ou pôr "press 1 for service or a new system" como primeira opção. Nossa CallRail é só leitura, a ICS decide.
- [ ] Junto: vários ligantes de NYC (Queens, Bronx, Brooklyn), fora da área de NJ. Checar o tipo de localização na PMax/Search e a área do LSA.
- Prova: `clients/integrate-comfort/call-wins-log.md` (update 2026-10-28).

## C&S Air — achar destino pros ~$100/dia que sobraram (Edu, até 10-30, Command Center fu-091)
- [ ] Depois de pausar PMax + Cooling (10-23), a C&S gasta ~$65-75/dia vs ~$170 antes. Branded e LSA não absorvem. Opções: subir o heating depois da 1ª semana, revisar settings do LSA, campanha de Search comercial, Meta, ou avisar o AM e devolver. Detalhe no fu-091.

## ✅ 2026-10-23 FEITO: análise CallRail da C&S Air + All Seasons (fu-085). C&S: PMax 0 ligações → decisão do Edu (fu-088). All Seasons: 2 de 5 empresa errada, 2 agendados (fu-089 em 10-29)
- [x] C&S: ligações no 817-442-6949 de 10-09 a 10-22 (atendidas, 60s+, primeira vez). Os 39 taps da PMax viraram ligação? Depois rodar o plano de ação (`clients/cs-air/google-ads-log.md`, 2026-10-22 later).
- [ ] All Seasons: ligações do Google Ads 10-16 a 10-22, % de empresa errada vs 10 de 20 em Oct 1-15 (transcrição local). Ler contra as mudanças de 10-22 (520 negativas, 898 keywords pausadas).
- Script: `paid/weekly-7day/callrail_calls_pull.py`. API deu 429 a noite toda em 10-22.

## ✅ 2026-10-21 — Napps form tracking: JÁ EXISTIA no GTM (GTM-KH7RS4V), Edu testou e funciona. fu-076 fechado.
Ver `clients/napps/google-ads-log.md`, entrada 2026-10-20 (tracking check). Command Center fu-076.
- [x] nappsac.com NÃO tem container GTM hoje (só gtag com G-Q9KC7NXEWY + AW-16542555435) e não há conta/container da Napps no GTM da TSD: criar container e instalar no WordPress.
- [x] Listener do form GoHighLevel (iframe link.leadnurturemachine.com, form "Schedule Service - Activate" Y0T8AuvseKBX6itJAZju; Contact Us também) → tag de conversão Google Ads "TSD - Lead form" (AW-16542555435 / Qxp-CK2BqtscEKu6jdA9). Excluir o form de careers.
- [x] Testar (preview/headless) numa página de aquecimento (/heating/furnaces/) e conferir a conversão no Ads no dia seguinte.

## Onboarding (primeiras semanas)
- [ ] Ler Day 1 docs: ADS Playbook v3.1, MasterOps v6, BED Calculator, Brandformance/BED doctrine, Program tiers
- [ ] Ler Week 1 docs: SEO Playbook v4.1, Video Playbook v4, OM Playbook v2, AM Playbook v2.1
- [ ] 1:1s com Andrea, Mac e Mo (inventariar o book — sem mudanças ainda)
- [ ] Setup de acessos: Bitwarden + 2FA, Agency Titan, MCC + Meta Business Manager (via Andrea)
- [ ] Definir core overlap hours com o time

## Non-Branded Keyword/Search-Term Rank — em aberto (ver `paid/relatorios/nonbranded-keyword-rank/activity-log.md`, entrada 2026-09-07)
- [ ] **Re-rodar o pull da Zen Air isolando pré/pós 08-26** — os top termos do relatório (264/250/253
      conversões) vêm da campanha non-branded que ficou sem geo targeting de 08-03 a 08-26
      (`clients/zen-air/google-ads-log.md`), então uma fatia real da janela de 90 dias pode ser
      ruído de tráfego mundial, não demanda dos EUA.
- [ ] Checar se outras contas do book têm o mesmo buraco (campanha non-branded sem location
      targeting desde a criação) — o achado da Zen Air já apontou um caso latente na Cool Hand
      Electric.

## Growth Engine pull (Alex) — em aberto (ver `paid/relatorios/growth-engine-pull-2026-09/activity-log.md`, entradas 2026-09-28 e 09-29)
- [ ] **Compartilhar a pasta com o Alex** (Drive ou Slack) e mandar o ping (texto pronto no fim do activity log). Nada commitado ainda.
- [ ] **Item 6: audience size no Ads Manager** — ZIP 30096 + 2 ZIPs de cliente (sugestão: 30097 ou 30043, mercado da Zen Air); preencher `06_meta_audience_size_estimates.csv`.
- [ ] **Meta por região** (`region` ou `comscore_market`) — bloqueado pelo classifier; liberar a chamada ou exportar do Ads Manager.
- [ ] **On The Way Meta** (1428068256022895) e **split por campanha da Cool Hand no Meta** — bloqueados, não puxados.
- [ ] **Integrate "Mitsubishi YouTube"** (conta 2895702982): confirmar se a TSD roda. Se não, pôr data em `client_roster.csv` e rodar `build_outputs.py` (YouTube a 3x+ vira 9 de 28 semanas, 32%).
- [ ] Identificar contas sem registro: Meta 532145676808452 ("Wattenbarger Racing") e 170464733924961 ("Allen Black"); DFW _Unsuspended, Potomac, Supreme AC, Modern Comfort, AC Cornerstone, Ultimate Comfort LSA.
- [ ] Contas Meta com conector desabilitado: ICS (quase certo que é a Integrate), Rhino, Your New Door.
- [ ] Registrar Integrate Comfort e Strickland no `contas.yaml` e no `clients/README.md` (Strickland ainda sem pasta).
- [ ] **All Heart (offboarded): 4 contas LSA ainda gastando sob o MCC** ($17.582 nas últimas 4 semanas) — confirmar quem paga / desvincular. Ver `clients/all-heart-heating-cooling/google-ads-log.md`.
- [ ] Atualizar `clients/on-time-service-pros/README.md`: a conta Meta existe (1846637992293356).

## Carey & Walsh — em aberto (ver `clients/carey-walsh/internal-notes.md`, entrada 2026-10-05)
- [ ] **Mandar o media plan pro AM** (PDF em `clients/carey-walsh/Carey-Walsh-Media-Plan_Nov-2026-Jan-2027.pdf`) e pegar aprovação escrita do cliente com o valor mensal (vale como aprovação de budget).
- [ ] Perguntar ao AM: o contrato já define budget? C&W já tem perfil LSA / Google Guaranteed fora da TSD? Qual número vai nos anúncios (914-762-9600 ou emergência (347) 508-9713)? Querem leads comerciais? Putnam/Rockland entram depois?
- [ ] Criar conta Google Ads sob o MCC 4155514468 (Search Partners/Display OFF, geo Westchester `9058785` PRESENCE), linkar GA4 `G-6J3K34P4W5`, conversões de call/form (phone-click NÃO primário).
- [ ] Iniciar verificação do LSA (licença, seguro, background checks — 2 a 5 semanas). Confirmar qual licença o Google aceita (NY não tem licença estadual de HVAC).
- [ ] Revisar e publicar o build do GTM (workspace 6 do `GTM-M5DW5ZN`) depois de preencher Conversion ID e Meta Pixel ID. Publicar separado da edição.
- [ ] Meta: criar conta de anúncio + pixel + acesso à Page; briefing de criativo de awareness (Ad Recall) com prazo pro designer.
- [ ] Avisar o AM: o site ainda fala em "federal tax credits" pra heat pump (25C acabou depois de 2025, confirmar) — não usar em anúncio.

## Nick's Heating — TRABALHAR 2026-10-09 (ver `clients/nicks-heating/google-ads-log.md`, entradas 2026-10-08)
Conta 1854100356 nunca tinha sido checada (sem pasta, sem task 7-day no AT, 0 mudanças em 30 dias). Leads conferidos 10-08: são reais.
- [x] (10-21 aplicado) **Nonbranded AC (23821497590):** pausar a PHRASE "air conditioner repair Louisiana" ($856 de $1.257, 1 conv), adicionar negativas (concorrentes, supply houses tipo Ferguson/Trane dealers, "auto" ac, Metairie, pesquisa de preço) e trocar pra Max Clicks com teto de CPC (padrão Zen Air).
- [x] (10-21 aplicado) **Branded (23675600637):** pausar a BROAD "hvac contractors near me" (puxa ~100 nomes de concorrente; 4 das 7 conv "branded" vieram dela).
- [x] (10-21 aplicado) **Realocação no total constante:** parte dos $40/d do NB → PMax (perde 31% de IS por budget a $89 de CPL). Sem aprovação do cliente (total não muda).
- [x] (10-21 aplicado) **PMax (23586346547):** geo PRESENCE_OR_INTEREST → PRESENCE.
- [ ] **Ticket pro AM:** COI renovado pro LSA (planilha diz vencido 08-05; API ainda mostra PASSED), Nick's atende à noite/fim de semana? (LSA só seg–sex 7–16), acesso ao GA, 3 ligações de anúncio perdidas em horário comercial (09-10, 09-11 ×2), mensagem LSA de 09-14 sem marcar, 7 leads LSA pra marcar, revisar 3 leads DECLINED cobrados pra disputa.
- [ ] Tracking: ligação vinda do site não é rastreada (sem call tracking). Ver GTM do form + GA.
- [ ] Cobertura de aquecimento no NB (nov–fev).
- [ ] Pedir task 7-Day Google Search + 7-Day LSA no AT pra Nick's.

## Auditoria de cadência Google (2026-10-08) — em aberto (ver `paid/relatorios/google-ads-cadence-audit-2026-10-08/README.md`)
- [ ] **Live Wire:** Trade Vulcan (brandon@tradevulcan.com) clonou as campanhas em 09-16 e pausou as nossas em 10-05/06; tasks AT pararam em 09-21. Confirmar se ainda é cliente.
- [ ] **Strickland:** só On Purpose Media mexe na conta; todas as TSD_ pausadas. Não está no AT nem na planilha de audit. Confirmar.
- [ ] **Pedir tasks 7-Day Google + LSA no AT** pra: Proud Pops (incl. contas My Favorite Service), Neon Monkey, Nick's, Cool Hand, ICS.
- [ ] **My Favorite Service Company (9815330464):** 5 campanhas vivas, $1,8k/30d, ninguém olha desde jul. Domínio sendo redirecionado (req AT 09-28). Decidir: pausar ou gerenciar.
- [ ] **Neon Monkey LSA:** sem checagem desde 08-10. **ICS LSA Belleville / Mitsubishi YouTube:** desde 09-11.
- [ ] Motivo das pausas sem registro no log: Gillespie's (10-02), GC (09-15), Cool Hand HVAC (10-07).
- [ ] Mandar a resposta de cadência (rascunho no README da auditoria) pra quem pediu.

## Tasks semanais 7-Day (Agency Titan) — follow-ups da rodada de 2026-10-05 (ver o log de cada cliente, entrada 10-05)
- [x] ~~**10-06 C&S Air:** decidir as recomendações (`clients/cs-air/google-ads-log.md`, "2026-10-05 (cont.) — Recommendations"): rota do tracking de ligação (CallRail ou import do GA4), trocar a Smart Campaign (100% Display) pela PMax de fev com end date vencida, pausar keywords da Nonbranded + ad groups de aquecimento.~~ → feito: Smart/PMax/Cooling pausados 10-23, heating Search no ar 10-26 (fechado 11-02).
- [ ] **10-06 All Seasons Meta** (task AT `630fe022`, vence 10-06): Reach → Ad Recall Lift, tirar/subir o frequency cap (2 por 7 dias), geo pra Nassau + Suffolk só "living in", pedir 1–2 criativos de brand recall. Ver `clients/all-seasons-ac/meta-ads-log.md`.
- [ ] **All Seasons Google:** apelar os 6 anúncios de aquecimento do LeadGen (STALE_DISAPPROVAL, só pela UI); decidir os outros 21 auto-apply ligados.
- [ ] **KPI - Meta não tem campo de notas:** decidir se adiciona "Lead Quality Notes" no objeto (mudança no Titan inteiro).
- [ ] **10-09 Watt's Right:** recheck completo das mudanças de 09-29 (checklist no log). Incluir: bloquear ou não "quality electric".
- [x] ~~**~10-12 Hawkins:** PMax gastando os $18/d e segurando ~$29 CPL? Se sim, mais um passo; se o CPL subir, voltar pra $13.~~ → Hawkins CANCELADO em 11-02 (30 dias).
- [ ] **~10-12 All Seasons Google** (task AT `6329236a`, ciclo novo): rodar com uma semana cheia depois do fix de Display.
- [ ] **Zen Air:** mais 1 semana de Max Clicks; se a conversão não voltar, quebrar a non-branded em ad groups phrase/exact por serviço.
- [ ] **Napps:** Branded pra Target IS com teto ~$8–10 (prometido no relatório de 6 meses); reconstruir AC Summer pra aquecimento mantendo $50/d.
- [ ] **Gillespie's:** registrar o motivo da pausa de 10-02 no log (Search desligado, Non-Branded removida).
- [ ] **On The Way:** cliente revogou o acesso ao Google Ads (MCC link INACTIVE). As tasks semanais vão continuar vindo (próxima ~10-10): logar $0 / 0 leads + "lost visibility" até o acesso voltar.
- [ ] Decisões de concorrente (bloquear ou manter, convertem nessas contas): All Seasons, King's Window, Napps. (Hawkins saiu: cancelado 11-02.)
- [ ] Recomendações de realocação (total constante): Lilypad $2–3/d Nonbranded → Branded. (Hawkins saiu: cancelado 11-02.)
- [ ] **Spencer Meta** (10-06, mesmo padrão da All Seasons): Reach → Ad Recall Lift em CBO, tirar o frequency cap 2/7d, geo só "living in" na área de serviço (hoje 16 cidades × 25 mi + "recent"). Ver `clients/spencer-air/meta-ads-log.md`.
- [ ] **C&S Meta:** não tem conta de anúncio compartilhada com a TSD. Decidir: montar o Meta (conta, pixel real no GTM, awareness) ou desligar a task semanal recorrente. Ver `clients/cs-air/meta-ads-log.md`.
- [x] **Tasks Google de 10-06 (C&S `e7b4a5bc`, Spencer `d4839f0a`):** rodadas e fechadas em 10-06 (sem mudanças, KPI + notas).

## Tasks semanais 7-Day — rodada de 2026-10-13 (11 de 12 fechadas; detalhe no log de cada cliente, entrada 10-13)
- [x] **(10-14 aplicado; falta só desligar 7 tipos de auto-apply pela UI, fu-049) All Seasons:** aprovar `clients/all-seasons-ac/asac_autoapply_cleanup_1013.py` (pausa as 156 keywords broad que o auto-apply criou em 10-11 + 14 tipos de auto-apply); os 7 tipos UNKNOWN só pela UI. Command Center fu-043.
- [x] **(10-14 feito e fechado) All Seasons LSA** (task AT `363a93f3`): a conta é a 8655979348, sob o MCC TSD (Edu, 10-14). KPI 7e1e2f9c. Ver log do cliente.
- [x] **(10-14 aplicado; recheck ~10-21, fu-050) Hawkins:** aprovar PMax $18→$23 / NB $75→$70 + correção da marca (negativa 'hawkins' na NB + Branded em Manual CPC ~$5). fu-044.
- [ ] **Resto (fu-045):** Lilypad $3/d NB→Branded; Napps (Branded com teto, AC Summer → aquecimento, negativas); C&S negativas 'airlines'/'car' (feito 10-20); Spencer Meta rebuild ARL/CBO.

## Tasks AT — rodada de 2026-11-24 (Gui; 34 de 34 rotinas completas: C&S 3, Spencer 3, Lilypad 6, All Seasons 6, Watt's 3, MA 3, Napps 3, King's 3, Hawkins 4; detalhe e recs staged no log de cada cliente, entrada 11-24)
- [ ] **Ficaram abertos de propósito (7):** reviews Climate 288a15df, Watt's e2239252 (gêmea), Zen e83dc467 (Edu submete); alinhamentos King's 9f657ee7, Spencer 5a7202d9, Watt's df7c0bbf, Napps 73c502b8 (falta o resultado da call do AM). King's: Angela mandou o media plan pro Edu hoje (IR e4dc9880).
- [ ] **C&S (11-26):** créditos dos 7 leads LSA do glitch Lennox de 11-18 ($455); o 353050671 está sem credit state.
- [ ] **Hawkins:** o próprio cliente tirou Tyler TX do LSA em 11-19 (avisar Edu/AM). Negativas de pesquisa + sitelinks de janela/porta ainda staged.
- [ ] **Mensagens LSA sem resposta:** Spencer 7 (NEW desde 10-25), All Seasons 4 cobradas (Angela já tem em 3addac2e), Napps 11-19/11-20, MA 2 de 11-19 dependem do bot.
- [ ] **Rating LSA (fu-161):** C&S 11-15/11-19/11-23, King's, Watt's 11-17..11-23, Hawkins 11-05 + 11-21 51s, All Seasons 351372745.
- [ ] **Staged pra decisão do Edu:** Watt's 8 negativas de concorrente + 'electrical repair' + grupo EV (fu-175); All Seasons 'eagle heating'/'climate pros'/'gas and heating services' + call asset no Branded (fu-182 11-25); King's negativas auto glass (dodge/rear window/vent glass); Lilypad 'cost to'/'how much' + exclusão Sedgwick/KC; Napps 'tankless'/'how much to replace' + goal de lead form no NB; MA confirmar $100/d em dez por escrito.
- [ ] **CallRail 429 o dia todo:** nenhuma ligação transcrita exceto Watt's. Refazer transcrição de C&S 11-17, All Seasons 11-18/11-23, Napps (página 903-289-7073), Spencer.
- [ ] **Toggles na UI (opcionais):** C&S 7-Day Google: Tracking Firing = Yes, Blockers = Yes; C&S LSA: Blockers = No. Spencer 7-Day Google: Tracking Firing = Yes. Lilypad e Watt's 7-Day Google: Tracking Firing = Yes.

## Tasks AT — rodada de 2026-10-26 (Gui; 48 de 48 completas: 7/14/30/90-Day Google, 7/30-Day Meta, 7/30-Day LSA, 7-Day YouTube; detalhe e recs staged no log de cada cliente, entrada 10-26)
Command Center NÃO atualizado: a conta do Gui não acessa o banco do artefato do Edu ("no such artifact or no access"). Follow-ups ficam aqui até o Edu lançar lá ou dar acesso.
- [ ] **King's Meta, confirmar entrega (10-27):** a campanha de lead ficou escura de 10-17 a 10-26 por um **bug da Meta** na criação do anúncio DCT (`GlassReplace_Ads1,2,3_Dynamic_callform_FO`, 120254214546330721): "Unknown Error When Creating Ad", issue code 2465018, travado em "Update Required" sem erro de setup. Gui reenviou em 10-26 17:43 → "Pending Process", mas às 17:51 voltou pra WITH_ISSUES com o mesmo erro (checado 10-27: 0 impressões). **Reenviar não resolve:** criar um anúncio NOVO no ad set DCT (e apagar o quebrado) ou religar o ad set antigo do GlassReplace ($26 CPL) como ponte.
- [ ] **URGENTE Zen Air (10-27):** o Branded tem lead form asset 342506189374 ENABLED com nome/URL da **Nick's** (nicksac.com). Remover (go do Edu/Gui) e checar se a Nick's tem o inverso. Forms do site (Submit lead form - web + ghl_contact_us) zerados desde 09-15: teste de form nas 2 LPs novas.
- [ ] **Zen Air Meta:** ~$6,5k / 30d gasto vs $2k/mês aprovado (AT 3f291790, só awareness); não achei aprovação da campanha de lead. Confirmar com o AM.
- [ ] **Hawkins (até o recheck de 10-29, fu-080):** copy de janela/porta ainda no ar (descrição do Branded, sitelinks Window Replacement / Doors / Doors & More, headline do PMax "Window Replacement"). Typo "Sliding". NB com 0 lead verificado desde o reset.
- [ ] **Napps:** nenhuma conversão de form desde 08-25 (GHL Form Fill nunca registrou) mesmo com o teste do Edu de 10-21. Mensagens de LSA de 10-14 (uma de vazamento de gás) só receberam o auto-reply. Duplicata de lead de septic de 10-14 cobrada 2x → disputar.
- [ ] **Watt's Right (decisão do Edu):** PMax foi pra YouTube/Display comprando taps (10-21..10-25: só $47,75 de $437,50 no Search; 50 de 53 conv = taps; 5 leads reais). Taps → secondary? NB travado pelo tCPA de $80 (~$62/d de $105, IS perdido por rank 41%→61%), staged tCPA ~$95-100. KPI 10-26 gravado SEM taps (22 leads / $65,24), diferente das linhas anteriores: decidir o padrão.
- [ ] **Mission Accomplished LSA:** 6 leads Declined cobrados sem disputa (09-28, 10-01, 10-09, 10-20 x2, 10-21). Disputar via AM, começando pelos mais antigos (a janela de disputa é curta). Meta: Kingman (raio de 40 km) fora da lista de área? Location type inclui "recent".
- [ ] **King's LSA (até ~11-05):** disputar as chamadas fora da área de 10-07 (Golden Valley MN) e 10-08 (Fort Myers FL).
- [ ] **All Seasons:** 2 mensagens de LSA (10-12, 10-14) ainda NEW sem resposta → AM. LSA bateu o teto de outubro em 10-19 (não estava escuro desde 10-15). Volta 11-01.
- [ ] **Spencer (fu-073 em 10-27):** Target IS com teto de $8 sufocou o Branded (10-20..10-25: $10,64 / 3 cliques / 0 calls). Uploads First Time/Repeat do CallRail parados desde 10-14; a chamada de 10-19 foi pra ação "Phone Call" (fu-031).
- [ ] **C&S:** Edu ligou o Search de heating 24383234148 em 10-26 08:08 ($30/d, teto $12) → fu-090 pode fechar; primeira leitura 11-02.
- [ ] **Tasks de tracking a criar (Gui):** Watt's Right (Form Submission [Landing Page] + Directions sem nada em 90d), King's (ghl_request_estimate parado desde 09-23, chamadas contadas 2x no Branded), Zen Air, Napps, Spencer, C&S, Lilypad (nunca teve teste ponta a ponta).
- [ ] **Toggles pra marcar na UI (a API não grava):** principais: 30-Day Google "Landing Page Issues Found" (King's, Napps, Zen, Watt's, Lilypad, All Seasons), 90-Day "Stalled Conversions Found" (King's, Napps, Zen, Watt's, Spencer, C&S), 30-Day Meta "Awareness Reviewed" + "Hook-Rate & Retention Checked".

## Tasks AT — rodada de 2026-10-27 (Gui; 19 de 19 completas: All Seasons 4, C&S 6, Spencer 6, Proud Pops 3; detalhe e recs staged no log de cada cliente, entrada 10-27)
- [ ] **C&S (até ~10-29):** decidir disputa do lead LSA DECLINED cobrado de 09-29 (lead 342890473); AM fazer responder a mensagem LSA de 10-21. Total diário caiu ~$238 → ~$133 depois das pausas de 10-23 e o AM não sabe (fu-088). Heating Search: primeira leitura 11-02.
- [ ] **Spencer:** uploads CallRail parados desde 10-14 (First Time/Repeat); refazer checagem 10-28 (CallRail 429 hoje) + criar task de tracking. Teto $8 do Branded derrubou o gasto 85% e 0 calls na semana: staged subir pra ~$12. LSA: disputar 4 DECLINED cobrados, responder 2 mensagens (10-19, 10-25). Queda de 65% do LSA em 30d = menos leads (fim do pico de AC), não budget nem rank.
- [ ] **Proud Pops (antes do restore de 11-01, fu-053):** linkar o call asset aprovado (210) 225-5767 (o 794-7570 reprovado é o único linkado → 0 calls; Edu confirma o número, fu-052), cutover G2b, HVAC ad groups pra páginas próprias. LSA: 3 DECLINED cobrados sem disputa (10-03, 10-05, 10-08). Meta: nenhuma conta da Proud Pops compartilhada com a TSD (AM).
- [ ] **All Seasons:** 4 nomes de concorrente passaram pelas negativas de 10-22 (universe home services, flynn aire, sweezy's, argo plumbing; staged); [TSD] Lead Form com 0 desde 10-08 (testar form); mensagem LSA de 10-14 ainda sem resposta; LSA volta 11-01 (checar 11-02). CallRail fu-089 em 10-29.
- [ ] **C&S e Proud Pops sem conta Meta** acessível pela TSD: as tasks de Meta foram fechadas como N/A. Confirmar com AM se Meta está no escopo.
- [ ] **Toggles pra marcar na UI:**
  - All Seasons 14-Day: High-CPC Keywords Reviewed + Keyword Warnings Reviewed = Yes.
  - C&S 30-Day Google: Landing Page Issues Found + Blockers to Escalate = Yes.
  - Spencer 30-Day Google: Blockers = Yes. Spencer 7-Day Google: Blockers = Yes. Spencer 30-Day Meta: Awareness Reviewed, Hook-Rate & Retention Checked, Winning Post IDs Found, Older Ads Paused = Yes.
  - Proud Pops 30-Day Google: Landing Page Issues Found + Blockers = Yes.

## Tasks AT — rodada de 2026-10-31 (Gui; 8 de 8 completas: Zen Air 7-Day Google/LSA/Meta, Proud Pops 7-Day Google/LSA/Meta/YouTube, Hawkins 90-Day Google; detalhe e recs staged no log de cada cliente, entrada 10-31)
- [ ] **Proud Pops (URGENTE, antes do restore de 11-01):** call asset sem mudança desde 10-27: só o 794-7570 REPROVADO está linkado (Branded LIMITED / CALL_EXTENSION_DISAPPROVED); o aprovado (210) 225-5767 está REMOVED. Linkar antes do restore senão as campanhas voltam sem número (fu-052/053, Edu). Branded 7d $687 / 7 conv, todas taps, 0 calls. Meta: ainda nenhuma conta compartilhada (N/A de novo, AM). YouTube pausado desde 10-16.
- [ ] **Zen Air:** NB PAUSADO em 10-29 15:26 pela UI com o login compartilhado access@topservdigital.com, sem log de quem/por quê (Gui?). NB 1ª semana nas LPs novas: $569 / 0 conv, termos de pesquisa/DIY, QS 1, $81 em Hall County (confirmar área). Lead form do Nick's não está mais no Branded (resolvido). Meta $1.456/7d, 107 leads $13,61, frequência 2,58 subindo (1 anúncio só desde 09-22); awareness ainda REACH com cap. Ver geo dos leads no export (11-03).
- [ ] **Hawkins:** Edu mexeu em 10-28 (Branded PAUSADO, 13 negs NB, 2 kws pausadas, tracking params) e 10-30 (ad group Vinyl pausado + 13 negs de concorrente). NB 10-23..10-30: $455 / 0 conv. Branded pausado + 'hawkins' negativado no NB = busca de marca sem anúncio pago: Edu confirmar. 11 ações primárias com 0 em 90d + upload CallRail 'First Time Phone Call' parado desde 10-11 + form web só em All conv → criar task de tracking. Recheck 11-04.
- [ ] **Toggles pra marcar na UI:**
  - Proud Pops 7-Day Google: Policy Issues Found + Blockers to Escalate = Yes. Proud Pops 7-Day Meta: Blockers to Escalate = Yes.
  - Hawkins 90-Day: Stalled Conversions Found = Yes (Schedule/Demographics/Audiences/Locations ficam No).

## Tasks AT — rodada de 2026-11-03 (Gui; 38 de 38 completas: Spencer 4, C&S 4, All Seasons 3, Zen 14-Day 1, Watt's 4, Mission Accomplished 4, Napps 4, King's 4, Lilypad 4, Hawkins 6; detalhe e recs staged no log de cada cliente, entrada 11-03)
- [ ] **King's (URGENTE):** anúncio de lead da Meta ainda WITH_ISSUES (code 2465018), lead gen $0 há 17 dias. Criar anúncio NOVO no ad set DCT (e apagar o quebrado) ou religar o GlassReplace antigo.
- [ ] **Mission Accomplished:** Meta awareness (52605605054542) PAUSADA 10-30 por Jonathan Bannister via MCP, sem registro do motivo; cliente só com LSA. Confirmar com Edu/Jonathan. LSA: 8 leads DECLINED cobrados sem disputa (os mais velhos de 09-28, checar janela).
- [ ] **Watt's:** PMax $720/7d e 0 lead real (187 conv = taps, Display/YouTube). Decisão do Edu: tirar tap da meta do PMax ou pausar e passar os $95/d pro Search. Meta: anúncio controle TOF cansando (CPL $40 → $74).
- [ ] **Hawkins:** conta Meta 10086442468052740 sumiu do acesso da TSD (funcionava em 10-26) → checar Business Manager. LSA: 3 DECLINED cobrados sem disputa (o de 10-11 vence esta semana). Negativas do Edu de 11-02 ("lp", "smartside", "smart siding") bloqueiam LP SmartSide, que a Hawkins vende. Calls não contam desde 10-26 (task de tracking). NB check 11-09.
- [ ] **Napps:** Edu relançou os 2 NB em 10-27 (Max Clicks $15, HVAC $65 / Plumbing $35 = 65/35 ok). 3 ligações Branded 60s+ (10-29, 10-30, 11-02) com 0 conversão → checar ação "Calls from ads" na UI. Todo o gasto NB fora de Longview (Tyler, Daingerfield, Frankston, Gun Barrel City): AM confirmar área.
- [ ] **C&S:** heating 1ª semana $241 / 0 calls / 0 taps; formulários não rastreados (task de tracking). Total vivo ~$57/d vs $238 do plano (fu-088, AM não sabe). CallRail: ligação de 10-22 veio de "Facebook Ads" → alguém fora da TSD roda Meta pra C&S (AM perguntar). Heating semana 2 em 11-09.
- [ ] **All Seasons:** LSA voltou 11-01 e gastou $144 só em 11-02 (4x o diário) → teto de novembro deve acabar cedo, avisar AM (11-05). Busca de marca rodando dentro do NB a até $24,92/clique (sem Branded desde 10-15). Negativas staged no MiniSplit.
- [ ] **Spencer:** Edu subiu o teto do Branded $8 → $10 em 10-28, IS 95% (resolvido). Correção: CallRail NÃO está parado; Repeat Phone Call chega; First Time só está sem teste (nenhuma ligação nova com gclid desde 10-19). 2 mensagens LSA sem resposta (10-19, 10-25).
- [ ] **Zen Air 14-Day:** NB segue pausado desde 10-29 (login access@ compartilhado, quem?). Itens de tracking marcados como "Gui investigando".
- [ ] **Lilypad:** 0 forms RYNO na semana (último 10-26); RSA Septic Pumping caiu pra POOR; 63% do gasto fora das cidades-alvo (geo em Presence or interest). Sem LSA e sem Meta (N/A).
- [ ] **Toggles pra marcar na UI:**
  - Spencer 7-Day Google: Tracking Firing = No, Blockers = Yes. Spencer 14-Day: High-CPC Keywords Reviewed + Keyword Warnings Reviewed = Yes.
  - C&S 7-Day Google: Blockers = Yes (Tracking Firing = No). C&S 14-Day: High-CPC + Keyword Warnings = Yes, Blockers = Yes.
  - All Seasons 7-Day Google: Tracking Firing = Yes.
  - Zen 14-Day: High-CPC + Keyword Warnings = Yes, Blockers = Yes.
  - Watt's 7-Day Google: Tracking Firing = Yes. Watt's 14-Day: High-CPC + Keyword Warnings = Yes.
  - Napps 14-Day: High-CPC + Keyword Warnings = Yes.
  - King's 7-Day Google: Tracking Firing. King's e Lilypad 14-Day: High-CPC + Keyword Warnings = Yes.
  - Hawkins 7-Day Google: Blockers = Yes. Hawkins 30-Day Google: Landing Page Issues Found + Blockers = Yes. Hawkins 30-Day LSA, 7/30-Day Meta: Blockers = Yes.
  - Mission Accomplished 7-Day Google: limpar "On Pace" / "On Target" (default do form, conta parada).

## Tasks AT — rodada de 2026-11-09 (Gui; 31 de 31 completas: Proud Pops 5, Zen Air 3, Hawkins 4, King's 3, Lilypad 3, Mission Accomplished 3, Watt's 3, Napps 3, All Seasons 4 (segundo lote, atribuído às 22:55); detalhe e recs staged no log de cada cliente, entrada 11-09)
- [ ] **All Seasons:** LSA gastou $523 na semana (209% do semanal), ~48% do teto de novembro já foi em 11-08 → apaga em meados de novembro como em outubro, avisar o AM (teto do cliente $2,500/mês). Concorrentes subiram pra 32% do gasto Google → **11-10 aplicadas 22 negativas** (log 11-10). Os 3 leads contados = 0 cliente real (transcritos); form 0 desde 10-08. **11-10 task AT `3addac2e` pra Angela** (mensagens LSA de 10-12/10-14 sem resposta + pedir LSA $60/d): falta você marcar o departamento e enviar o Intake na UI. Decidir com o Edu: keywords ativas da LeadGen com nome de concorrente. Reler ~11-16.
- [ ] **Zen Air (URGENTE):** campanha Now Hiring NÃO é rascunho: o Jonathan Bannister ativou em 11-04, gastou $26 na semana e marcou 71 "leads" a $0,37 (provável evento de lead disparando na página de vagas). Confirmar com a Angela se tem aprovação do cliente. Winter Ready foi recriado em 11-09 (IDs novos no log). NB segue pausado desde 10-29.
- [ ] **King's (URGENTE):** lead da Meta sem rodar há 23 dias (anúncio ainda WITH_ISSUES) → criar anúncio NOVO. LSA migrou pra campanha "Pay-per-lead-PMax" (Google, 11-04): conta como LSA.
- [ ] **Watt's:** LSA migrou pra "[LSA] Watt's Right Electric" (tipo PMax, 11-04). Edu subiu NB pra $320/d + tCPA $110 e Branded pra $50 em 11-04: confirmar aprovação escrita do cliente no AT 7b72529c. PMax $700 / 1 lead real. Branded IS caiu 73% → 43%. Meta: Austin Ensz pausou 3 ad sets FourMode em 11-03 (quem é?).
- [ ] **Hawkins:** NB $889 em 14d com 1 lead → decisão do Edu (NB → PMax) depois que o AM confirmar se os 14 forms do PMax são reais. Tracking morto (CallRail desde 10-11, form desde 10-28): criar task de tracking. Disputar LSA DECLINED de 10-21 e 10-22 até ~11-20. Janela/porta ainda nos sitelinks. Meta sem acesso.
- [ ] **Napps:** teto NB $25 desde 11-03 → $529/7d sem lead verificado, 79% fora de Longview. Revisar em 11-17 (manter ou baixar teto + fechar geo). Ligações Branded 60s+ ainda sem conversão (checar na UI / suporte Google). 4 LSA DECLINED pra disputar.
- [ ] **Proud Pops:** Edu resolveu o call asset e os taps em 11-04 (fu-052 feito). Plumbing $768 / 0 lead e HVAC $751 / 1 lead na semana → decisão de Plumbing em 11-16. Branded IS com orçamento de $50 (checar 11-12). Meta: conta ainda não compartilhada com a TSD (AM).
- [ ] **Mission Accomplished:** Meta segue pausada desde 10-30 (Jonathan Bannister, sem motivo). LSA só 1 lead cobrado na semana, sem impressões no fim de semana. 5 DECLINED cobrados sem disputa.
- [ ] **Lilypad:** Edu aplicou a lista de 11-03 em 11-06; reler em 11-16. Geo: 63% do gasto fora das cidades-alvo (AM confirmar área antes de mudar pra Presence).
- [ ] **Toggles pra marcar na UI:**
  - Zen 7-Day Google: Negatives Added / Ads Paused / Policy Issues = No, Tracking Firing = No, Blockers = Yes. Zen 7-Day Meta: Core Results Declined = Yes, Blockers = Yes (o resto No).
  - Hawkins 7-Day Google: Tracking Firing = No, Blockers = Yes. Hawkins 14-Day: High-CPC + Keyword Warnings Reviewed = Yes.
  - Proud Pops 7-Day Google: Tracking Firing = Yes. Proud Pops 14-Day: High-CPC + Keyword Warnings Reviewed = Yes. Proud Pops 7-Day Meta: Blockers = Yes.
  - King's 7-Day Google: Tracking Firing = Yes.
  - Mission Accomplished 7-Day Google: limpar "On Pace" / "On Target" / "None" (default do form, conta parada).
  - Napps 7-Day Google: Tracking Firing é decisão sua (taps disparam, ligações de anúncio não contam).
  - All Seasons 14-Day: High-CPC Keywords Reviewed + Keyword Warnings Reviewed = Yes; Keywords Paused or Fixed / Geo Targeting Adjusted / Audience added / Blockers to Escalate = No.

## Tasks AT — rodada de 2026-11-10 (Gui; 6 de 6 completas: Spencer 3, C&S 3; detalhe e recs staged no log de cada cliente, entrada 11-10)
- [ ] **Spencer:** LSA migrou pra campanha PMax-type (24436741588, desde 11-07), sem gasto 11-04..11-06. Conversões do Branded contadas em dobro (Calls from ads + upload CallRail) + Directions primária → task de tracking. First Time Phone Call funcionando. 2 mensagens LSA ainda sem resposta (10-19, 10-25).
- [ ] **C&S:** Edu 11-09 deixou o heating só com Repair, $15/d, +26 negativas. Heating 2 semanas = $458 / 0 lead → reavaliar ~11-16. Primeiro form rastreado no Branded (checar se é lead real). LSA $0 com $55/d. Meta segue N/A (quem roda o Facebook da C&S?).
- [ ] **Toggles pra marcar na UI:** Spencer 7-Day Google: Tracking Firing = Yes, Blockers = No. C&S 7-Day Google: Tracking Firing = No, Blockers = Yes. C&S 7-Day Meta: Blockers = Yes.

## Strategy Reviews / Post Review — rodada de 2026-11-12 (Gui; rascunhos no AT, NADA completado, Gui revisa antes)
- [ ] **Revisar e dar complete (Performance Reporting):** Mission Accomplished (dbc1b73e), Lilypad (59a4be8c), All Seasons (7be61e95). Calls do AM já passaram (11-09/11-10).
- [ ] **Zen:** "Oct/Nov Review" (c29ad0c8) já tinha relatório pronto, só falta complete; "Oct/Nov Strategy Review" (e83dc467) parece duplicata. Duplicatas também em C&S (03fff3a7 / fd5eb77f) e Watt's (f911c525 / e2239252): confirmar com o AM.
- [ ] **King's Post Review (9f657ee7):** checklist com 3 itens marcados (geo, tracking, escalar). AM precisa dizer TMS + budget combinados na call de 11-10 (nada registrado). Ad set DCT quebrado da Meta segue ACTIVE a $30/d (pausar = escrita, precisa de ok).
- [ ] **Urgente:** MA 5 leads LSA Declined cobrados (~$345) sem disputa, prazo ~11-19. All Seasons: LSA deve acabar ~11-17; msgs LSA 10-12/10-14 sem resposta. Lilypad: 5 de 6 ligações de anúncio caíram no voicemail (out).
- [ ] **Concrete LSA (c702263a):** conta 2898153501 criada, campanha ativa; falta do cliente background check + seguro + billing. Parte de IG = Social. Decidir complete.
- [x] ~~Próximas reviews~~ → 11-13: Edu fez All Seasons (row 1b309436, submetida), C&S (03fff3a7, row 4387c0fc), Spencer (7a4093a1); duplicatas mapeadas na memória tsd-at-client-strategy-review. Ver rodada 11-16 abaixo.
- [ ] (linha antiga) **Próximas reviews (ciclo ainda aberto):** C&S fecha 11-15, Watt's 11-14/11-16, Spencer 11-16, Napps 11-17, Hawkins 11-22: montar relatório logo após o fechamento.

## Tasks AT — rodada de 2026-11-17 (Gui; 8 de 8 completas: C&S 4, Spencer 4; tudo read-only, recs staged no log de cada cliente, entrada 11-17)
- [x] **Spencer 7-Day Meta (0c28fee8): ✅ FEITA 11-17 depois do refresh do conector** (KPI-Meta 25efa238: $277.47, freq 1.87/sem, CPM $4.55, 1,660 recallers a $0.17; sem fadiga, abaixo de 3x/sem = falta de verba).
- [ ] **C&S:** Edu PAUSOU o Heating Search 24383234148 em 11-16 07:50 (fu-141; total desde 10-26 $586.72 / 68 cliques / 0 leads) → só Branded + LSA no ar, gasto bem abaixo dos $5,500/mês. LSA: $219.28 em 11-15 por 2 leads cobrados ($109.64 cada, era ~$65) → se seguir >$100 avisar o Edu (rever 11-24). Staged: neg 'products' no Branded, +2-3 headlines no RSA 800192030388.
- [ ] **Spencer:** 'Local actions - Directions' ainda Primary (staged → Secondary desde 11-10); uma ligação conta 2x (Calls from ads + CallRail First Time) → precisa task de tracking (Gui criar). LSA (PMax-type 24436741588): $530 / 7 leads, 4 de aquecimento; 2 msgs repair_hvac de 11-15 com 20s de diferença, ambas cobradas = provável duplicata, avaliar como ruim (fu-161); 5 msgs da semana em NEW.
- [ ] **Toggles na UI:** C&S 7-Day Google (Negatives Added No, Ads Paused No, Policy Issues No, Tracking Firing Yes, Blockers Yes), C&S 14-Day (High-CPC Reviewed Yes, Kw Warnings Reviewed Yes, Paused/Fixed No, Geo No, Audience No, Blockers Yes), C&S LSA Blockers No, C&S Meta Blockers Yes (N/A, sem conta Meta); Spencer 7-Day Google (Tracking Firing Yes, Blockers No), Spencer 14-Day (High-CPC Yes, Kw Warnings Yes, Paused/Fixed No, Geo No, Audience No, Blockers No).

## Tasks AT — rodada de 2026-11-16 (Gui; 34 de 34 de rotina completas via 9 sub-agentes: Proud Pops 4, Zen 4, Lilypad 4, Hawkins 3, King's 4, Napps 4, All Seasons 3, Watt's 4, Mission Accomplished 4; tudo read-only, recs staged no log de cada cliente, entrada 11-16)
- [ ] **URGENTE MA Meta:** conta nova 2671066020034494 de novo "Payment Needed" (11-16 10:36), só ~$60 entregues desde 11-11. Brian precisa de cartão que funcione/pré-pago via Angela (Edu decide escalar).
- [ ] **URGENTE Zen Meta:** awareness parada desde 11-13 (ad Cold Weather 120248098173470711 segue DISAPPROVED, sem resultado da revisão); CPL do lead CBO triplicou depois da troca de form 11-13 ($11.75 → $33.37) → confirmar Zapier/GHL do form novo; ler fu-163 11-19.
- [ ] **All Seasons LSA: ✅ APLICADO 11-16 $35.71 → $50/d (read-back OK). Falta o Gui marcar 'raise to $350/week' + Review & Close na UI (auto-mode bloqueou a escrita no AT).** Era: aumento JÁ APROVADO (AT 3addac2e, Angela: "client agreed to raise budget $100/week, total weekly LSA $350") → aplicar $35.71 → $50/d e marcar o item "raise to $350/week" + Review & Close. Esperando ok do Gui/Edu pra aplicar. Também: 3 msgs LSA sem resposta (11-13 351972066, 11-14 352158970, 11-16 352353930).
- [ ] **Napps:** NB $709/sem e 0 lead verificado; 'TSD - Lead form' fora das metas de conversão das campanhas NB; form de 11-14 (Emergency Plumber) checar no GHL; ligação NB de 416s em 11-16 → fu-144 do Edu 11-17.
- [ ] **Proud Pops:** Edu 11-16 08:05 baixou Electrical $455→$375 + Plumbing $145→$75 (Search $880→$730/d) + 8 negs; Nov fecha ~$19.5–20k vs $25k (Angela ouviu ~$21k em d2b5e325). HVAC 1 lead/$1,120 no mês → decisão do Edu (ad group de aquecimento ou pausar).
- [ ] **Watt's:** Branded $145/d só gasta ~$45 (IS 95%) → ~$100/d do Push parado; staged mover pro NB no mesmo total (fu-145 do Edu 11-17). Meta: Clay Manus reestruturou FourMode em 11-16 → confirmar quais campanhas Meta são da TSD.
- [ ] **King's:** ✅ ad set DCT quebrado 120254214478390721 PAUSADO 11-16 (ok do Gui, read-back PAUSED); leads LSA caíram 12→6.
- [ ] **Toggles na UI (API não escreve):** Zen 14-Day: High-CPC + Keyword Warnings = Yes. King's 14-Day: High-CPC + Keyword Warnings = Yes; 7-Day Google: Tracking Firing = Yes. Napps 14-Day: High-CPC + Keyword Warnings. Lilypad 14-Day: High-CPC + Keyword Warnings = Yes. Watt's 14-Day: High-CPC + Keyword Warnings; 7-Day: Tracking Firing = Yes. All Seasons 7-Day: Tracking Firing = Yes. Hawkins 7-Day: os outros = No.
- [ ] **Gui apagar na UI do AT (API exige aprovação no app):** reviews duplicadas MA dbc1b73e, Lilypad 59a4be8c, C&S fd5eb77f, Spencer e9d97f93. ⚠ Zen: a review do Edu c29ad0c8 SUMIU (task not found); e83dc467 é a única que sobrou, NÃO apagar, avisar o Edu. Comentário pra Angela postado em 3addac2e (3 msgs LSA sem resposta).
- [ ] **13 tasks que ficaram com o Gui (não completadas):** reviews duplicadas MA dbc1b73e / Lilypad 59a4be8c / Zen e83dc467 / C&S fd5eb77f / Spencer e9d97f93 (gêmeas já feitas pelo Edu); reviews abertas Watt's e2239252 (call 11-18, gêmea f911c525), Napps 0de4a6cc (call 11-19, gêmea 6db957ea), Hawkins eeb41f98 (call 11-24); Post Review King's 9f657ee7, All Seasons b1e7e485, Spencer 5a7202d9 (precisam do TMS/budget do AM); Internal Request Concrete c702263a; All Seasons 3addac2e (acima).

## Tasks AT — rodada de 2026-11-20 (Gui; 16 etapas: 8 de rotina COMPLETAS, 4 reviews com notas/linha SEM submit, 4 alignments checados e ABERTOS; tudo read-only, recs staged no log de cada cliente, entrada 11-20)
- [ ] **Edu decidir / submeter:**
  - Hawkins review eeb41f98 (call **11-24 15:17 UTC**): row a57b3633 ($5,909.07 / 54 = 25 LSA + 1 call + 28 forms não verificados / $109.43). Antes da call: rodar `clients/hawkins-siding/hawkins_review_1120.py` até 11-22 + LSA 11-20..22, atualizar row e notas, submeter. ✅ 11-20 Edu: offboarding, SEM recomendação de budget → recommend_budget limpo na row + linha Budget das notas reescrita (lido de volta).
  - Climate Experts review 288a15df: SEM acesso (MCC/Meta/AT vazios, Leadsie 593c1204 aberto). Só nota pra Angela, sem row. Submeter na UI. (Edu 11-20: ok, a Angela tem uma task dele sobre isso.)
  - Zen review e83dc467: notas do Edu de 11-12 restauradas (task original c29ad0c8 foi apagada; row 53ecca81 segue no cliente). Submeter na UI. (Edu 11-20: talvez ele mesmo apagou e refez, vai olhar.)
- [ ] **Gui apagar na UI:** review duplicada Watt's e2239252 (gêmea f911c525 completa).
- [ ] **Zen Meta → falar com o Mo:** ✅ Edu 11-20: cerca de 1 milha + pausa do R&G foram intencionais. ⚠ GHL 11-14..11-20 tem só **9** contatos do Facebook (0 em 11-14 e 11-15) vs **24** leads de form no Meta → ~15 leads do form novo não chegaram no GHL (o form novo chega, tag `furnace tune-up & heating`, mas não todos). Edu: confirmar com o Mo (Zapier/mapeamento do form novo). Revisit 11-24.
- [ ] **Watt's alignment df7c0bbf (aberto):** RSA 830598421847 (Electrician General) ainda diz "No Extra Fees on Weekends" / "no extra fee" mas o cliente cobra extra (AT 76e1df4a, 11-19) → ✅ TROCADAS 11-20 23:27 UTC (go do Edu, `wr_rsa_fees_1120.py`, aprovado). Falta: `ads_budget_marketing` no AT = "$17,500 June" velho → Angela atualizar pra ~$26.9k (Push).
- [ ] **Napps alignment 73c502b8 (aberto):** budget no AT gravado como **$53,000** (11-19..12-22), provável $5,300 → Angela corrigir. Oferta em conflito: AT $89 Diagnostic/Tune-Up vs estáticos do Hector $79 Winter Tune-Up. Nota do Tyler 49583709 voltou pro Edu 11-20 com comentário (ler na UI). 2 msgs LSA cobradas 11-19/11-20 em NEW (fu-161).
- [ ] **Spencer alignment 5a7202d9 (aberto):** gasto ritmo ~$3.3k nov / ~$4.9k dez vs $2,700 apresentado (LSA de aquecimento) → AM: confirmar budget ou baixar LSA. Oferta (manutenção grátis 1 ano na troca) em nenhum anúncio; ✅ 7 cidades do AT ADICIONADAS no Branded 11-20 (go do Edu, `spencer_branded_geo_1120.py`, 17 locais); budget: Edu acha que está tudo certo (sem mudança). Falta: oferta + 2 textos Meta de verão. Revisit 11-27.
- [ ] **King's alignment 9f657ee7 (aberto):** nada registrado da call. ⚠ As 4 perguntas do Growth Engine (AT 1496977c) ficaram na Execution, que foi completada 11-19; task está em Review & Close com o Edu → talvez a Angela nunca viu. Edu re-rotear (fu-196): Edu 11-20 vai mandar mensagem pra Angela. Revisit 11-23.
- [ ] **Proud Pops:** ✅ 11-20 APLICADO (go do Edu, `pp_apply_1120.py`): sitelink "See Our Pricing" fora do Electrical + Plumbing (trocado por `Electrical Repair` 441525652903 / `Drain Cleaning` 441598912395), RSA 827482059113 PAUSADO. Plumbing: Edu segura por agora. YouTube: Edu ajustou 11-20 e tirou video partners. Nov ≈ $23.5k dentro dos $25k planejados. Falta: neg exata [electrician] no Electrical (Edu não confirmou). Chave CallRail própria da PP não está na máquina do Gui (sem transcrição). Meta segue N/A.
- [ ] **LSA a avaliar (fu-161):** Zen 2 cobradas de 11-16; Hawkins 11-05 09:05 (DIY, DECLINED, não creditado); PP 7 msgs de encanamento em NEW.
- [ ] **Toggles na UI:** PP 7-Day Google: Tracking Firing = Yes; PP 14-Day: High-CPC + Keyword Warnings Reviewed = Yes. Zen 7-Day Google: Tracking Firing = Yes, Negatives Added = No.
- KPIs 11-20: Zen Google ffac5cef / LSA 13c77019 / Meta ae4bfc7e; PP Google f3e895fa / LSA 7b21338e / Meta 62a91857 ($0 N/A).

## Milestones
- [ ] **Auditoria de tracking/atribuição** em todo o book (semanas 1–2) → `paid/auditoria-tracking/`
- [ ] **KPI framework** da divisão + metas + timeline pra aprovação do Ryan (semanas 2–4, primeiro milestone) → `paid/kpi-framework/`

## All Heart — em aberto (ver `clients/all-heart-heating-cooling/google-ads-log.md`, entrada 2026-07-11)
- [ ] **ATRASADO: abrir ticket do AM** pra registrar por escrito o aumento de budget de 07-10 (feito na autoridade verbal do Edu; MasterOps exige registro escrito do cliente)
- [ ] **Segunda-feira (07-13): rodar `clients/all-heart-heating-cooling/ramp_check.py`** — primeira leitura limpa do ramp do tCPA (2 dias cheios, com as ligações já contabilizadas). Se CPC continuar ~$6-7 sem crescer clique, baixar tCPA pra $50-55.
- [ ] **Perguntar ao AM/cliente: All Heart atende telefone no fim de semana?** Sábado converte a 3,6% vs ~17% dia útil. Se não atendem, cortar fim de semana via *restrição* de ad schedule (bid modifier é ignorado em Max Conversions). Responder ANTES do flip da Fase 2.
- [ ] **Fase 2 (brand split + ad groups temáticos): SEGURAR.** RSAs já aprovados; flip só depois do ramp limpo + resposta do fim de semana.
- [ ] Pausar campanha `20250049817` (ENABLED com $300/dia, inerte só porque `serving_status=ENDED` — bomba-relógio)
- [x] ~~Decidir se desliga a geração automática de assets do Google~~ → **DECIDIDO (07-13): OFF.** Auto-assets e auto-apply desligados no build. Virou regra no SOP de Google (7.8). Falta aplicar nas contas que já rodam.

## GC Home Service — em aberto (ver `clients/gc-home-service/google-ads-log.md`, entrada 2026-07-28)
- [ ] **ATRASADO: abrir ticket do AM** pra registrar por escrito o corte de budget do PMax ($155 → $50/dia, feito na autoridade verbal do Edu; MasterOps exige registro escrito do cliente)
- [ ] **Verificar o tag do form da landing page** (`Form Submision [Landing Page]`, QUALIFIED_LEAD): 0 disparos em 90 dias. É o melhor sinal que temos e está morto — consertar é o maior ganho agora. As duas campanhas entraram em learning com sinal fino (só First Time Phone Call ~13/90d) até isso funcionar.
- [ ] **ServiceTitan offline import** — GC tem ZERO conversões de origem ServiceTitan/upload hoje. Confirmar com o AM se GC tem Marketing Pro / acesso a offline conversion + captura de GCLID; é o mesmo play do Mission Accomplished. Esse é o fix de verdade.
- [ ] Se `Repeat Phone Call` se provar baixo valor no relatório, recategorizar `First Time Phone Call` pra categoria de lead própria e desligar DEFAULT/WEBSITE (hoje os dois dividem o mesmo bucket).
- [ ] Cobrir o resto do audit 2026-07-27: rebalancear peso pro Search + qualidade de landing/asset do PMax, arquivar as 10 campanhas mortas, auditar QS dos termos de marca.
- [ ] **Blocker herdado:** o doc *July Campaign Management, Budget Allocation & Lead Quality Review* nunca foi fornecido — pegar antes de qualquer entregável ao cliente. Update escrito ao cliente é toda sexta. (Procurado no Drive e no Gmail em 31/07: não está lá. O update dessa semana foi montado na estrutura que o Edu passou.)

### Semana 2026-08-21 (ver `clients/gc-home-service/weekly-log-2026-08-21.md`)
- [ ] **Mandar o weekly update pra Eve** revisar antes de ir pro cliente — PDF pronto em `clients/gc-home-service/GC-Home-Service-Weekly-Update_2026-08-21.pdf`
- [ ] **Checar status/entrega do `CBO | YETI GIVEAWAY | 20 AUG`** (subida 20/08, $100/dia) — última leitura mostrou ACTIVE com $0 gasto e sem impressão ainda, condizente com lançamento recente, mas confirmar que está servindo de fato.
- [ ] **Verificar mix de rede do PMax** (Search vs Display/Discover/YouTube) — CPC caiu de ~$0,90 pra ~$0,61 (blended) na mesma semana que o clique dobrou; coluna de conversão padrão segue em 0. Confirmar antes de decidir se corta budget do PMax.

### Semana 2026-07-31 (ver `clients/gc-home-service/weekly-log-2026-07-31.md`)
- [ ] **Mandar o weekly update pra Eve** revisar antes de ir pro cliente — PDF pronto em `clients/gc-home-service/GC-Home-Service-Weekly-Update_2026-07-31.pdf`
- [ ] **Aprovação da landing page** pelo cliente — trava a jogada de qualidade no Google (68,5% da impression share do PMax é perdida por Ad Rank, não por budget)
- [ ] **Novo lote de criativos Meta** com a oferta consolidada — pedido, previsto pra hoje. Quando chegar: 1 ad set DCT por ângulo, quote-back lidera (CPL $47,16 vs $432,52 do tune-up $99)
- [ ] Religar lead gen na Meta atrás do criativo novo (campanha `CBO | NEW CREATIVES | 8 JUL` pausada em 30/07 a $174,81 de CPL)
- [ ] Falar sobre o budget do `CBO | NEW CREATIVES` ter subido $185 → $200/dia em 27/07 (Manuel), 3 dias antes da gente pausar

## Gillespie's Heating and Cooling — em aberto (ver `clients/gillespie-heating-cooling/weekly-log-2026-08-21.md`)
- [x] ~~PPC pausado (Non-Branded + Branded) pra construir landing page nova~~ → **RESOLVIDO 09-17.**
      Zero conversões desde 09-08 (funil confirmado morto, não era tracking) → duas LPs novas no ar
      (`/emergency-ac-repair/`, `/emergency-furnace-repair/`, form perto do topo em vez de 5-14 telas
      abaixo) → todos os 5 ad groups repontados → campanhas religadas mesmo dia, budget intacto.
      Ver `clients/gillespie-heating-cooling/google-ads-log.md`, entradas 2026-09-17.
- [x] ~~**Checar em ~2026-10-01: migrar de Manual CPC pra Maximize Conversions?**~~ → **MOOT: migrado 09-26 (rebuild), check-in 10-01 feito, ver google-ads-log.md.** Edu rodou o teste
      end-to-end 09-17 (resultado não confirmado pra mim ainda — logado como "teste feito", não
      "fix confirmado"). Decisão 09-18: SEGURAR Manual CPC até acumular volume real de conversão
      nas páginas novas (meta: 15-30+ conversões, CPL confiável) antes de migrar o non-branded pra
      Maximize Conversions (sem target) e só depois Target CPA. Branded fica em Manual CPC até o
      budget/volume mudar — $1/dia não sustenta bidding automático. Ver entrada 2026-09-18.
- [ ] **Confirmar se o telefone (859-445-6500) está tocando de fato** — conversion action de
      Click to Call zerada nos mesmos 7 dias do funil morto, sem CallRail conectado pra checar
      independente. Pode ser um segundo buraco de tracking separado do problema da landing page.
      Ver `google-ads-log.md`, entrada 2026-09-17 (fork resolvido).
- [ ] **Primeiro weekly report do cliente**, mesmo formato do GC Home Service — PDF em
      `clients/gillespie-heating-cooling/Gillespies-Heating-Cooling-Weekly-Update_2026-08-21.pdf`.
      Mandado direto pro Edu (sem passar por Eve/AM ainda, não tem esse fluxo montado pra esse
      cliente).
- [x] ~~**Negativar HVAC-General-Company (Google)**~~ → **FEITO 10-01: 287 negativas no NB novo, ver google-ads-log.md.** — termo de busca já pegando nome de concorrente
      (Anderson, Reinhart, Logan, Thomas and Galbraith) e busca de pesquisa/atacado
      (Johnstone Supply, "daikin furnace", car AC) antes do ad group escalar.
- [ ] **Levar recomendação de campanha de awareness no Meta** na próxima conversa com o cliente —
      as 5 criativos ativos são todos de resposta direta, frequência já em 2.71 na semana, sem
      nada de topo de funil. Pedido explícito do Edu, 2026-08-21.
- [ ] Confirmar com Edu/AM se a conta Meta (`2014320269203822`, negócio próprio do cliente) é
      pra TSD gerenciar ativamente ou se é legado que precisa de handoff/aprovação de budget por
      escrito.
- [ ] Aprovação por escrito do corte de budget do Google ($80/$80 → $3,62/$32,57), autorizado
      verbalmente pelo Edu em 08-18.

## Zen Air — 2 landing pages (plano de 10-14, ver `clients/zen-air/landing-pages/2026-10-14-lp-plan.md`)
- [ ] Confirmar com o Eddie se o "$49 Furnace Tune-up and Safety Check" ainda está valendo (banner do site se chama "Spring Version").
- [ ] Confirmar que os $1.500 off do AT expiraram e atualizar `current_specials`.
- [ ] Definir o telefone das páginas (call asset ainda indefinido desde 09-08; sem CallRail achado; AT diz ServiceTitan).
- [ ] Puxar nota + número de reviews do GBP certo (Duluth ou Alpharetta).
- [x] (10-23) Páginas no ar e non-branded religada em cima delas ($100/dia, ver google-ads-log 10-23).
- [ ] Zen Air NB: checar aprovação dos 2 RSAs + search terms ~10-27, conversão ~10-30; Verified Live do Mo no form GHL antes de falar com o cliente; ticket do AM (Andrea).
- [ ] AT: preencher o catálogo de serviços (só Commercial AC marcado) e resolver Lennox vs Carrier.

## Zen Air Meta — geo corrigido em 10-12 (ver `clients/zen-air/meta-ads-log.md`, entrada 2026-10-12)
- [ ] **Postar a resposta na task do AT** (rascunho no chat de 10-12): Marietta/Monroe fora, 131 ZIPs da lista de Target Cities no ar nas 2 ad sets.
- [ ] **Recheck ~10-19:** CPL/volume da lead CBO depois da expansão (learning resetou) + perguntar ao AM se os endereços dos leads agora caem dentro da área. Se aparecer lead do sul de Atlanta / South Fulton, cortar Fulton pra North Fulton.
- [ ] **AT:** ver no app se o perfil do cliente tem histórico de edição (quando entrou o "do not target Marietta/Monroe" em Notes - Paid Advertising); se não tiver, pedir ao suporte do AT e reportar o erro interno do GET /v1/activity.

## Zen Air — em aberto (ver `clients/zen-air/google-ads-log.md`, entrada 2026-07-31)
- [ ] **Abrir ticket do AM (Andrea)** pra registrar por escrito a mudança de 07-31: PMax `TSD_03.23_PMAX_HVAC_Calls` pausado ($100/dia) + Search `TSD_05.13_Search_Branded_Evergreen` $150 → $200/dia. Feito na autoridade verbal do Edu; MasterOps exige registro escrito do cliente.
- [ ] **Reler CPA do Search em ~14 dias (por volta de 08-14).** 75% do spend está na broad `hvac contractors near me` a $571 de CPA — os +$50/dia caem nela, não nos termos de marca ($76). Se continuar assim, pausar a broad ou separar o não-branded em campanha própria.
- [ ] Decidir o destino dos outros $50/dia que saíram do PMax (hoje fora da conta — budget do PPC caiu $250 → $200/dia).

## SOPs de launch (entregável do Ryan — call de 07-10)
Feitos em `paid/sops/` (md = fonte; `build_pdfs.py` regera HTML+PDF; PDFs prontos em `paid/sops/PDFs/`):
- [x] Meta, Google (PPC, sem LSA), YouTube, TikTok — 11 stages cada, prontos pro Ryan montar no AT
- [ ] **Mandar os 4 PDFs pro Ryan** (Slack) — ver mensagem-modelo no histórico da sessão
- [ ] Decisões pendentes que os SOPs esperam (lista completa em `paid/sops/README.md`):
  - [ ] Meta: piso concreto de relevância estatística antes de isolar vencedor (dias? spend? conversões?)
  - [ ] Meta: post IDs isolados ficam na MESMA CBO do teste ou em campanha separada?
  - [ ] Meta: mover o teste de lead flow pro Stage 3 (como nos outros 3) ou manter no Stage 8?
  - [ ] TikTok: confirmar targeting amplo (geo only + ML) e Spark Ads como isolamento de vencedor
  - [ ] YouTube: 2 vídeos distintos (conversão + recall) é realista no budget de produção?
- [ ] Re-baselinar os tempos por stage depois dos primeiros builds reais (hoje são estimativa, não cycle time medido)

## Itens em aberto herdados do playbook
- [ ] KPI benchmarks por trade type e tier (CPL/ROAS/CVR) — **os 4 SOPs dependem disso**
- [ ] Requisitos de onboarding de cliente para Paid (checklist de acesso, setup de tracking, formato de brief) — **coberto em boa parte pelos SOPs (Stage 1 de cada)**
- [ ] Convenção de nomenclatura de campanha (todas as plataformas) — **os 4 SOPs dependem disso**; de facto em uso: `TSD_MM.DD_<Type>_<Brand|NonBranded>_<Theme>`

## Infra do workspace
- [ ] Conectar este repo a um GitHub próprio da TopServ (Edu cria o repo vazio e me passa o link)

## Alex / Portal (2026-11-16)
- [ ] Send Alex `paid/handoffs/2026-11-16-reply-to-alex-naming.md` + `alex-naming-audit-2026-11-16.zip` (Slack DM, ready)
- [ ] Give Alex feedback on the portal Ads tab (his ask from 11-11, still open)
- [ ] Identify call-asset numbers: Nick's (985) 999-4785, Zen Air 678-329-9929 / 678-606-8817 (not in our CallRail)
- [ ] King's pool number as call asset (fu-167)
- [ ] When Alex's naming plan lands: rename live campaigns in one pass, update Google + Meta launch SOPs

