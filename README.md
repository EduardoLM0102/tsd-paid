# topserv-workspace

Workspace da divisão de **Paid Ads** da **TopServ Digital**. Só TopServ.

Usado pelo time de paid (Edu e Gui), cada um no próprio Mac, sincronizado por este repositório.

## Primeira vez aqui?
Siga o [`ONBOARDING.md`](ONBOARDING.md).

## Estrutura
- `CLAUDE.md` — instruções pro Claude Code operar neste workspace (carrega a memória do time sozinho)
- `_contexto/` — base de conhecimento (empresa, preferências, estratégia) + `fontes/` (playbooks originais)
- `_contexto/memoria/` — memória compartilhada do time (clientes, regras, receitas)
- `clients/<slug>/` — logs, planos e relatórios por cliente
- `paid/` — SOPs, relatórios, funis, Command Center, ads próprios da TSD
- `.claude/skills/` — `google-ads-ratos` (Google Ads, GTM, GA4, CallRail), `schwartz-copy`, `ogilvy-copy`
- `.claude/commands/syncar.md` — `/syncar` pra salvar no GitHub
- `tarefas.md` — tarefas correntes
- `_pessoal/` — gitignored, nunca sobe

## Como usar
Abrir esta pasta no VS Code e iniciar o Claude Code nela. Começo da sessão: `git pull --rebase`. Fim: `/syncar`. Entregáveis em inglês.
