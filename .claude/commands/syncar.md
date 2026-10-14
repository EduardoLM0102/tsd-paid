---
name: syncar
description: >
  Salva o estado atual do workspace TopServ no GitHub (commit + pull + push) com UM comando.
  Use quando alguém disser "salva no github", "synca", "syncar", "faz commit",
  "sobe pro github", "backup", "salva tudo", "manda pro repo".
  O TopServ NÃO tem auto-sync — só sobe quando este comando roda.
---

# /syncar — Salvar o workspace TopServ no GitHub

Workspace do empregador (TSD), usado por mais de uma pessoa (Edu e Gui). Nada sobe sozinho: este comando é o único jeito de sincronizar.
O push é deliberado — sempre liste o que vai subir antes de commitar.

## Se o `git` não funcionar (Mac sem Xcode Command Line Tools)

Se `git` cair no shim do Xcode, use o git embutido do GitHub Desktop exportando as variáveis antes de qualquer comando git:

```bash
BASE="/Applications/GitHub Desktop.app/Contents/Resources/app/git"
export GIT_EXEC_PATH="$BASE/libexec/git-core"
export GIT_TEMPLATE_DIR="$BASE/share/git-core/templates"
export PATH="$GIT_EXEC_PATH:$PATH"
```

## Verificação inicial

```bash
git status --short
git remote get-url origin 2>/dev/null
```

Antes de listar, confira que nada de segredo ou pessoal entrou: nenhum `.env*` (fora `*.example`), nada de `_pessoal/`, nenhum `contas.local.yaml`. Se aparecer, parar e avisar.

## Fluxo A: tem mudanças

Liste pra pessoa o que vai ser salvo, depois:

```bash
git add -A
git commit -m "sync: [descrição curta do que foi feito]"
git pull --rebase
git push
```

O `git pull --rebase` traz o que a outra pessoa subiu antes de empurrar o seu. Se der **conflito**, parar, mostrar quais arquivos conflitaram e resolver junto com a pessoa (nunca descartar o trabalho do outro, nunca `--force`).

Descrição do commit em inglês (repo do empregador), refletindo o trabalho da sessão
(ex: "sync: tracking audit findings", "sync: KPI framework draft", "sync: weekly report").
Sem descrição clara, use `sync: workspace updates`.

Depois do push, confirme:

> "Salvo. Trabalho da TopServ seguro no GitHub."

## Fluxo B: sem mudanças locais

Rodar `git pull --rebase` mesmo assim (pode ter coisa nova da outra pessoa) e avisar:

> "Nada novo pra salvar. Puxei as atualizações do repo."

## Fluxo C: erro no push

Mostre o erro de forma simples e o próximo passo:

> "Não consegui enviar pro GitHub. Erro: [mensagem]
> Causas comuns: sem internet, autenticação do GitHub, ou a outra pessoa subiu algo no meio (rodar de novo resolve). Me diz que eu te ajudo."

## Regras

- Nunca commitar `.env`, chaves, segredos, `_pessoal/` ou `contas.local.yaml`.
- Nunca `git push --force`.
- Tom direto — não explicar git a não ser que perguntem.
- Em erro, sempre dizer o que fazer a seguir.
- Este repo é só TopServ — nunca misturar contexto, voz ou clientes de fora.
