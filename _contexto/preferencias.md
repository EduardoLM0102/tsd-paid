# Preferências e modo de trabalho — TopServ Digital

## Idioma
- **Entregáveis, docs internos, tickets, Slack, KPI framework, relatórios → inglês.** A TopServ é americana e tudo circula em inglês.
- **Conversa comigo (Edu) → português** está ok. Só o output que vai pra empresa é em inglês.

## Como o trabalho se move na TSD (MasterOps v6)
Seis princípios acima de qualquer processo (quando processo e princípio conflitam, o princípio ganha):
1. **Cliente primeiro, sempre.** Se o processo trava o cuidado com o cliente, escalar pro COO. Resolve o cliente, depois arruma o processo.
2. **AM é dono da relação com o cliente**, incluindo comunicação. AM não é relay; AM conduz. DH/Mo entram em call só quando realmente necessário (exceção, não default).
3. **Ticket vai pra divisão, não pra pessoa.** O DH garante que foi reconhecido, atribuído e concluído — não é o assignee default de tudo.
4. **AM coordena trabalho cross-division de rotina.** DH não coordena com outro DH pra trabalho de rotina que veio de um AM.
5. **Rotear por quem faz o trabalho, não pela plataforma citada.** Alerta veio do Google mas o fix é no site → Web Dev. Fix é em campanha/plataforma → Paid. Fix é GHL → Mo.
6. **Componente GHL exige Verified Live do Mo** antes de comunicar "live" ao cliente (joint test obrigatório).

## Disciplina operacional (minha divisão)
- **Agency Titan = fonte única.** "Se não está no Titan, não aconteceu." (playbooks ainda citam ClickUp; em transição.)
- **Friday status semanal:** Done / In Progress / Blocked.
- **1:1 semanal com o Ryan** durante o onboarding, depois cadência normal.
- **Atrito vai pro Ryan**, não pros canais do time.
- **Hard rules de paid:**
  1. Nenhuma mudança de budget sem aprovação escrita do cliente (AM submete ticket). Nunca executar primeiro e avisar depois.
  2. Achou problema na otimização semanal → Slack DM pro AM em até 2h (cliente, o que achou, ação, se precisa avisar o cliente). AM nunca é pego de surpresa numa call.
  3. Toda campanha segue a convenção de nomenclatura padrão da TSD (legível por AM e cliente sem explicação).
  4. Verificação end-to-end do fluxo de lead antes de qualquer campanha de geração de lead ir ao ar. Com GHL → joint test com Mo + Verified Live no ticket.

## SLAs (tiered)
- **Standard:** 24–72h por categoria de ticket (builds novos, ajuste de budget, brand/impression, offer launch).
- **Accelerated (Fast-Track):** 4–8h — swap de criativo em campanha ativa com sinal de performance + brief completo + aprovação do cliente.
- **Critical:** acknowledge em 1h / resolver no mesmo dia — overspend, tracking quebrado, conta suspensa, oferta errada no ar.

## SOPs recorrentes da divisão (A1–A5)
- **A1** Weekly Optimization (semanal, todo cliente; checklists por plataforma: Google, Meta, YouTube, TikTok, LSA).
- **A2** Biweekly Review (a cada 14 dias).
- **A3** Monthly Report & Strategy Review (fim do mês).
- **A4** Weekly Paid Ads Pulse (toda sexta até 9h; roll-up único, todos os clientes, health flag Green/Yellow/Red + 5 essenciais por cliente; posta em #paid-ads-pulse). **Red** → AM contata cliente em 48h com plano.
- **A5** Quarterly Strategy Review (dia 10 do novo trimestre; 1 doc por cliente; recomendação de budget sempre com a matemática, nunca "shift more to LSA" vago).

## Estilo de comunicação
- Direto, claro, profissional. Sem enrolação.
- Recomendação de budget = **com números e a conta**, não direção vaga.
- Health flags nunca vazios: todo Yellow/Red tem causa em uma frase + ação em uma frase. "Monitoring" não é ação.

## Metodologia de Meta Ads do Edu (doutrina da divisão)
SOP completo: `paid/sops/meta-ads-launch-buildout.md` (fonte de verdade; PDF/HTML são build a partir dele).

- **CBO sempre.** Budget na campanha, nunca no ad set. O spend é o voto do algoritmo, e é isso que a gente lê.
- **Um ângulo = um ad set DCT.** Cada Dynamic Creative carrega UM ângulo, com 3 criativos (iterações do mesmo ângulo, mesmo formato), 2 headlines e 2 primary texts DAQUELE ângulo. Os ângulos rodam em paralelo na mesma CBO e competem pelo budget. Testa-se **oferta/ângulo**, não layout.
- **Conta sem vencedor prévio → 100% teste.** Conta com post ID isolado → vencedores seguem nos ad sets isolados e o teste roda junto numa fatia menor.
- **Isolamento de vencedor = reusar o POST ID original** (mantém prova social e aprendizado). Nunca recriar o anúncio do zero.
- **Kill rules:** não gastou → morre (o algoritmo achou irrelevante perto dos outros). Gastou pouco → morre. Gastou e trouxe só 1-2 leads (ou poucos leads relativo ao volume total, em conta que já tem post IDs isolados) → morre.
- **Targeting:** Advantage+ em TUDO. **Nunca interesse/comportamento/detailed targeting.** Só geo (people living in), e idade no máximo como *sugestão*. Campanha ruim se conserta na oferta/ângulo/criativo, nunca apertando público.
- **Awareness sempre em paralelo**, objetivo **Ad Recall Lift** (não reach/impressão), com vídeo e artes feitos de propósito pra branding/brand recall — nunca criativo de conversão reciclado. Não se lê por CPL. 5-10% do budget.

## Metodologia de Google Ads (PPC) do Edu
SOP: `paid/sops/google-ads-launch-buildout.md`. Doutrina extraída dos logs reais (All Heart, Hawkins, Mission, Zen Air, auditoria Napps).

- **Consertar a medição antes de gastar.** Nenhuma decisão de lance/scale sobre sinal de conversão sujo.
- **Nunca ler nem reportar número blended.** Brand e non-brand separados ANTES de qualquer CPL sair da boca de alguém.
- **Brand sempre em campanha separada**, com negativação cruzada (brand EXACT como negativa na non-branded).
- **Ad groups temáticos** (8-10 kws, 1 RSA cada, 15 headlines/4 descriptions). Nunca mega ad group. **Phrase + Exact só; broad nunca.**
- **Negativas anexadas ANTES de habilitar** (lista compartilhada). Match type por propósito: PHRASE = padrão, EXACT = gastador conhecido, BROAD = bloquear categoria inteira. Não over-negativar; não cortar bom intento com dado fino.
- **Triagem por IS:** perdido por RANK → dinheiro não é o lever (é relevância/asset/LP); perdido por BUDGET → aí sim pedir aumento (com aprovação escrita).
- **tCPA NUNCA abaixo do CPL real** (target inalcançável = algoritmo se recusa a dar lance = autoestrangulamento). Mudar o *target* não reseta learning; mudar o *tipo* reseta.
- **Launch de campanha nova (sem histórico): Max Clicks com teto de CPC**, migrando pra Max Conversions quando houver dado + sinal limpo.
- **PMax fora do launch.** Quando entrar: brand exclusions, asset groups por serviço, audience signals, Ad Strength ≥ Good, teto 5-10%, PMax-only proibido.
- **Geo:** círculos de proximidade nos hubs, **presence only** (nunca "interested in").
- **Ad schedule:** sem default — vem do horário real de atendimento do cliente (campo obrigatório do intake). Restrição, nunca bid modifier (smart bidding ignora modifier).
- **Auto-assets e auto-apply do Google: OFF.**
- Leitura: bid change lê em 3-7 dias; mudança estrutural leva 2-3 semanas. Uma mudança por vez, ~48h de separação, cada uma atribuível. Nunca ler intraday nem o dia corrente (lag de ligação).

## Metodologia de YouTube e TikTok
SOPs: `paid/sops/youtube-ads-launch-buildout.md` e `paid/sops/tiktok-ads-launch-buildout.md`.

- **YouTube:** duas campanhas — Conversão (Video Action/Demand Gen, Max Conversions **sem target**) + Video Views pra Ad Recall Lift (medido por Brand Lift study quando o budget passa o mínimo; abaixo disso lê CPV/VTR/reach/frequência e diz que não mediu). **View-through NÃO é lead** (Secondary, só reporting, nunca alimenta lance). Targeting = geo + in-market/custom segments. **O vídeo é o caminho crítico:** upload no canal é do time do Vince (48h do Green Light), ativação 48h depois; Paid faz os cutdowns.
- **TikTok:** **não existe objetivo de otimização por ad recall lift** (só Brand Lift Study, mínimo $25k-$100k+ ou 500k impressões — fora do nosso book). Awareness compra o proxy (Reach com frequency cap, ou Video Views/focused view 6s-15s) e é lida em reach/frequência/views. **Nunca reportar número de recall no TikTok.** Conversão = Instant Form (default) ou Call Ads. **Lead de Instant Form some em 90 dias** → integração automática com o CRM é obrigatória e testada antes do launch. Piso da plataforma: $50/dia campanha, $20/dia ad group.

## Preferências adicionais
[Adicionar conforme aparecerem.]
