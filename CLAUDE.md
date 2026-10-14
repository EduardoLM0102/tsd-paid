# TopServ Digital — workspace de Paid Ads

## O que é esse workspace
Workspace da divisão de **Paid Ads** da **TopServ Digital (TSD)**, agência americana de marketing para *home service contractors*. Mora aqui tudo de paid na TSD: logs por cliente, auditoria de tracking, framework de KPI, relatórios, briefs, SOPs e as skills/scripts de Google Ads, GTM, GA4 e CallRail. **Só TopServ:** nada de outras empresas ou clientes de fora entra aqui.

**Quem usa (cada um no próprio computador, sincronizado pelo GitHub `EduardoLM0102/tsd-paid`):**
- **Edu (Eduardo, Mac)** — Head of Paid Ads. Dono da divisão (playbook, time, sistemas, integridade de atribuição em todo o book). Reporta ao **Ryan (COO)**.
- **Gui (Windows)** — time de Paid Ads (entrou em out/2026).

Se não estiver claro quem está na sessão, olhar `git config user.name` ou perguntar. Nos arquivos de memória e logs, "Edu" é o Eduardo; regra registrada como "Edu quer/disse" vale pro time todo.

**Idioma:** entregáveis, docs e comunicação da TopServ são em **inglês** (empresa americana). Conversa com o Edu ou o Gui pode ser em português.

## Estrutura de pastas
- `_contexto/` — base de conhecimento da TopServ (não apagar): `empresa.md`, `preferencias.md`, `estrategia.md`, `fontes/` (playbooks originais)
- `_contexto/memoria/` — **memória compartilhada do time** (estado de cada cliente, regras, receitas, armadilhas). Índice em `_contexto/memoria/README.md`
- `clients/<slug>/` — tudo de cada cliente (`google-ads-log.md`, planos, relatórios, scripts pontuais)
- `paid/` — trabalho da divisão: `sops/`, `relatorios/`, `funnels/`, `command-center/`, `own-ads/`, `auditoria-tracking/`, `kpi-framework/`
- `.claude/skills/google-ads-ratos/` — skill de Google Ads/GTM/GA4 (scripts em `scripts/`, contas em `contas.yaml`)
- `.claude/commands/syncar.md` — `/syncar` (commit + pull + push)
- `tarefas.md` — lista de tarefas corrente
- `ONBOARDING.md` — setup de uma pessoa nova (credenciais, conectores, dependências)
- `_pessoal/` — **gitignored**, coisas pessoais de cada um na própria máquina. Nunca sobe.

## No início de qualquer conversa
1. Rodar `git pull --rebase` (pode ter coisa nova da outra pessoa). Se houver mudança local não salva, avisar antes.
2. Ler e usar como base: `_contexto/empresa.md` (TopServ, Brandformance, quem é quem, tiers), `_contexto/preferencias.md` (como se trabalha, SLAs, doutrina, metodologias), `_contexto/estrategia.md` (foco e milestones).
3. O índice da memória do time é carregado abaixo. Quando um cliente aparecer, abrir o arquivo de memória dele e o `clients/<slug>/` antes de agir.

Para detalhe profundo de processo, consultar os playbooks em `_contexto/fontes/`. Não listar o que foi lido, só usar o contexto.

@_contexto/memoria/README.md

## Memória: onde salvar
- **Tudo que for de TSD** (estado de cliente, regra, correção, receita, armadilha) vai pra `_contexto/memoria/` + uma linha no `README.md` de lá. **Não** salvar memória de TSD na memória pessoal/automática do Claude, porque ela não chega na outra pessoa.
- Antes de criar arquivo novo, procurar um existente sobre o assunto e atualizar ele. Datas absolutas.
- Regra de comportamento nessa pasta → este `CLAUDE.md`. Sobre a empresa/papéis → `_contexto/empresa.md`. Como trabalhar lá → `_contexto/preferencias.md`. Foco/prioridades → `_contexto/estrategia.md`. Salvar só a linha nova, sem reformatar o arquivo inteiro.
- Quando alguém corrigir algo ou der instrução permanente, perguntar se quer salvar.

## Trabalho em dupla (Git)
- **Começo da sessão:** `git pull --rebase`. **Fim da sessão (ou depois de qualquer mudança importante):** `/syncar`.
- **Cada cliente tem um dono** (o mesmo responsável que está no Agency Titan). Antes de mexer numa conta de outra pessoa, avisar. Duas pessoas mudando a mesma conta de Google/Meta no mesmo dia = mudanças não atribuíveis.
- **Nunca commitar** `.env*` (fora `*.example`), tokens, `_pessoal/` ou `contas.local.yaml`. Credenciais são de cada um, na própria máquina.
- Em conflito de merge, nunca descartar o trabalho do outro nem usar `--force`.

## Ferramentas
- **Google Ads / GTM / GA4:** skill `google-ads-ratos`, sempre via `scripts/tsd.sh` (Ads) e `scripts/gtm.sh` (GTM/GA4), perfil `.env.topserv`, MCC `4155514468`. Nunca o `.env` default. No Windows o Python é `python` (não `python3`): os wrappers escolhem sozinhos, e onde logs/memória dizem `python3 ...`, no Windows é `python ...`. Receitas e armadilhas: `_contexto/memoria/topserv-google-ads-location.md`.
- **CallRail:** `scripts/callrail.py` (lê `.env.callrail` na raiz; só GET).
- **Meta, Agency Titan, Slack, Google Drive:** conectores do claude.ai, cada pessoa logada com a própria conta. (Tickets da TSD vivem no Agency Titan, não no ClickUp.)

## Command Center (https://claude.ai/artifact/1gah5xuCXDADf4kYVYp95q)
Painel de Paid com todos os clientes, canais, relógio de 7 dias e follow-ups (artefato do Edu, compartilhado com o time). Ler e escrever pela tool `ArtifactData` (collections `clients`, `followups`, `checks`, doc `meta/sync`).
- **Todo "revisitar X no dia Y" vira um doc em `followups`** (`client` = slug ou null pra geral, `title`, `due` YYYY-MM-DD, `details` = o que precisa ser feito, em inglês, linhas com "- " viram bullets, terminar com "Source: <arquivo/entrada>", `status: "open"`, `createdBy: "Claude"`). Não basta memória ou `tarefas.md`. O time lê o `details` no pop-up do cliente.
- **Toda checagem semanal de um canal** atualiza `clients/<slug>.channels.<google|lsa|meta|youtube>` (`lastChecked`, `checkSource`, `spend7`, `state`) via `update`.
- Quando um cliente aparecer na conversa, ler os `followups` abertos dele primeiro e citar o que está vencido.
- O refresh automático dos funis (`funnel_refresh_daily.sh`) roda **só numa máquina** (a do Edu). Ninguém mais agenda.

## Doutrina central (Brandformance)
TSD não vende ads/SEO/vídeo soltos. Vende **marca + performance juntos** (sistema "Brandformance"): anúncio não cria autoridade, **amplifica**. Os 6 princípios do MasterOps v6 estão acima de qualquer processo (cliente primeiro; AM é dono da relação; ticket vai pra divisão, não pra pessoa; AM coordena cross-division; rotear por quem faz o trabalho, não pela plataforma citada; GHL exige "Verified Live" do Mo antes de comunicar ao cliente).

## Regras de trabalho na TopServ
- **Agency Titan** é a fonte única de verdade. "Se não está no Titan, não aconteceu." (Os playbooks ainda citam ClickUp como sistema de tickets — em transição para o Titan.)
- **Friday status** toda semana: Done / In Progress / Blocked.
- **Atrito e discordância** vão pro Ryan (COO), não pros canais do time.
- **Mudança de budget** só com aprovação escrita do cliente, via ticket do AM. Paid nunca executa primeiro e avisa depois.
- **GHL gate:** campanha com componente GHL não é comunicada como "live" até o Mo marcar Verified Live (joint test).
- Os playbooks citam o Paid Ads DH como "Manuel" — esse é o **assento que o Edu ocupa**.
