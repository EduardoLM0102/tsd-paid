# Tarefas — TopServ (Paid Ads)

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
- [ ] **Nonbranded AC (23821497590):** pausar a PHRASE "air conditioner repair Louisiana" ($856 de $1.257, 1 conv), adicionar negativas (concorrentes, supply houses tipo Ferguson/Trane dealers, "auto" ac, Metairie, pesquisa de preço) e trocar pra Max Clicks com teto de CPC (padrão Zen Air).
- [ ] **Branded (23675600637):** pausar a BROAD "hvac contractors near me" (puxa ~100 nomes de concorrente; 4 das 7 conv "branded" vieram dela).
- [ ] **Realocação no total constante:** parte dos $40/d do NB → PMax (perde 31% de IS por budget a $89 de CPL). Sem aprovação do cliente (total não muda).
- [ ] **PMax (23586346547):** geo PRESENCE_OR_INTEREST → PRESENCE.
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
- [ ] **10-06 C&S Air:** decidir as recomendações (`clients/cs-air/google-ads-log.md`, "2026-10-05 (cont.) — Recommendations"): rota do tracking de ligação (CallRail ou import do GA4), trocar a Smart Campaign (100% Display) pela PMax de fev com end date vencida, pausar keywords da Nonbranded + ad groups de aquecimento.
- [ ] **10-06 All Seasons Meta** (task AT `630fe022`, vence 10-06): Reach → Ad Recall Lift, tirar/subir o frequency cap (2 por 7 dias), geo pra Nassau + Suffolk só "living in", pedir 1–2 criativos de brand recall. Ver `clients/all-seasons-ac/meta-ads-log.md`.
- [ ] **All Seasons Google:** apelar os 6 anúncios de aquecimento do LeadGen (STALE_DISAPPROVAL, só pela UI); decidir os outros 21 auto-apply ligados.
- [ ] **KPI - Meta não tem campo de notas:** decidir se adiciona "Lead Quality Notes" no objeto (mudança no Titan inteiro).
- [ ] **10-09 Watt's Right:** recheck completo das mudanças de 09-29 (checklist no log). Incluir: bloquear ou não "quality electric".
- [ ] **~10-12 Hawkins:** PMax gastando os $18/d e segurando ~$29 CPL? Se sim, mais um passo; se o CPL subir, voltar pra $13.
- [ ] **~10-12 All Seasons Google** (task AT `6329236a`, ciclo novo): rodar com uma semana cheia depois do fix de Display.
- [ ] **Zen Air:** mais 1 semana de Max Clicks; se a conversão não voltar, quebrar a non-branded em ad groups phrase/exact por serviço.
- [ ] **Napps:** Branded pra Target IS com teto ~$8–10 (prometido no relatório de 6 meses); reconstruir AC Summer pra aquecimento mantendo $50/d.
- [ ] **Gillespie's:** registrar o motivo da pausa de 10-02 no log (Search desligado, Non-Branded removida).
- [ ] **On The Way:** cliente revogou o acesso ao Google Ads (MCC link INACTIVE). As tasks semanais vão continuar vindo (próxima ~10-10): logar $0 / 0 leads + "lost visibility" até o acesso voltar.
- [ ] Decisões de concorrente (bloquear ou manter, convertem nessas contas): All Seasons, Hawkins, King's Window, Napps.
- [ ] Recomendações de realocação (total constante): Lilypad $2–3/d Nonbranded → Branded; Hawkins próximo passo pra PMax.
- [ ] **Spencer Meta** (10-06, mesmo padrão da All Seasons): Reach → Ad Recall Lift em CBO, tirar o frequency cap 2/7d, geo só "living in" na área de serviço (hoje 16 cidades × 25 mi + "recent"). Ver `clients/spencer-air/meta-ads-log.md`.
- [ ] **C&S Meta:** não tem conta de anúncio compartilhada com a TSD. Decidir: montar o Meta (conta, pixel real no GTM, awareness) ou desligar a task semanal recorrente. Ver `clients/cs-air/meta-ads-log.md`.
- [x] **Tasks Google de 10-06 (C&S `e7b4a5bc`, Spencer `d4839f0a`):** rodadas e fechadas em 10-06 (sem mudanças, KPI + notas).

## Tasks semanais 7-Day — rodada de 2026-10-13 (11 de 12 fechadas; detalhe no log de cada cliente, entrada 10-13)
- [x] **(10-14 aplicado; falta só desligar 7 tipos de auto-apply pela UI, fu-049) All Seasons:** aprovar `clients/all-seasons-ac/asac_autoapply_cleanup_1013.py` (pausa as 156 keywords broad que o auto-apply criou em 10-11 + 14 tipos de auto-apply); os 7 tipos UNKNOWN só pela UI. Command Center fu-043.
- [x] **(10-14 feito e fechado) All Seasons LSA** (task AT `363a93f3`): a conta é a 8655979348, sob o MCC TSD (Edu, 10-14). KPI 7e1e2f9c. Ver log do cliente.
- [x] **(10-14 aplicado; recheck ~10-21, fu-050) Hawkins:** aprovar PMax $18→$23 / NB $75→$70 + correção da marca (negativa 'hawkins' na NB + Branded em Manual CPC ~$5). fu-044.
- [ ] **Resto (fu-045):** Lilypad $3/d NB→Branded; Napps (Branded com teto, AC Summer → aquecimento, negativas); C&S negativas 'airlines'/'car'; Spencer Meta rebuild ARL/CBO.

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
- [ ] Mandar o pedido das 2 páginas (Heating e AC Repair, Replacement & Tune-Ups) pro WebDev depois dos itens acima.
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
