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
