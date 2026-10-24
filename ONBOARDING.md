# Onboarding — workspace de Paid Ads da TSD

Passo a passo pra deixar o seu computador com o mesmo setup do Edu: Claude Code + skills + memória do time + acesso por API ao Google Ads, GTM, GA4 e CallRail, e Meta/Agency Titan pelos conectores do Claude.

Escrito pra **Windows**. No Mac, veja as notas "**Mac:**" em cada passo. Leva umas 1 a 2 horas, a maior parte esperando acesso. Faça na ordem.

---

## 1. Peça pro Edu (antes de tudo)

Sem isso os passos seguintes travam:

- [ ] Convite pro repositório **tsd-paid** no GitHub (você precisa de uma conta GitHub). Aceite pelo e-mail.
- [ ] Acesso ao **MCC do Google Ads** `4155514468` com o seu e-mail da TSD.
- [ ] Usuário nos **containers do GTM** e nas **propriedades do GA4** dos clientes que você vai tocar.
- [ ] Acesso às **contas de anúncio no Meta Business Manager**.
- [ ] O conteúdo do arquivo **`.env.callrail`** pelo **Bitwarden** (item "CallRail API (.env.callrail)"). É a chave da CallRail do Edu, que enxerga a conta da agência e as contas próprias dos clientes. Usuário seu na CallRail é opcional, só pra abrir a interface.
- [ ] Usuário no **Agency Titan**.
- [ ] Os 3 valores da agência pelo **Bitwarden**: `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`.
- [ ] Acesso de edição ao **Command Center** (artefato no claude.ai).

## 2. Programas

1. **Git for Windows** — git-scm.com/download/win (pode aceitar as opções padrão). Instala também o **Git Bash**, que o Claude Code usa pra rodar comandos.
2. **Python 3.12** — python.org/downloads (versão 3.12.x). Na primeira tela do instalador, **marque "Add python.exe to PATH"**.
3. **Desligue o atalho do Python da Microsoft Store:** Configurações → Aplicativos → Configurações avançadas de aplicativos → **Aliases de execução de aplicativo** → desligue os dois "Instalador de Aplicativo" de `python.exe` e `python3.exe`.
4. **GitHub CLI** — cli.github.com (instalador do Windows).
5. **UTF-8 pro Python** (evita erro com acento e emoji). Abra o PowerShell e rode uma vez:
   ```powershell
   setx PYTHONUTF8 1
   ```
6. **Feche e abra o VS Code de novo** (pra ele enxergar os programas novos).

**Mac:** em vez disso, rode `xcode-select --install` (traz git e python3) e instale o GitHub CLI com `brew install gh` ou pelo cli.github.com.

## 3. Claude

1. Conta no Claude com Claude Code (plano Pro/Max, ou um assento do time se houver).
2. No VS Code, instale a extensão **Claude Code** e faça login.
3. Em **claude.ai → Settings → Connectors**, conecte com as **suas** contas:
   - **Meta** (Ads)
   - **Agency Titan**
   - **Slack**
   - **Google Drive**

   Os conectores valem no Claude Code quando você está logado na mesma conta.

## 4. GitHub e o workspace

Abra o **Git Bash** (menu Iniciar) e rode:

```bash
gh auth login
```

Escolha **GitHub.com** → **HTTPS** → responda **Yes** em "Authenticate Git with your GitHub credentials" → login pelo navegador. Isso deixa o `git` (e o `/syncar`) autenticado.

Depois clone o repositório. **O caminho importa**, use exatamente este:

```bash
gh repo clone EduardoLM0102/tsd-paid ~/Documents/GitHub/topserv-workspace
cd ~/Documents/GitHub/topserv-workspace
git config user.name "Gui"
git config user.email "<seu e-mail da TSD>"
```

No Windows isso vira `C:\Users\<você>\Documents\GitHub\topserv-workspace`. O `user.name` é como o Claude sabe quem está na sessão.

**Daqui em diante dá pra deixar o Claude te guiar:** abra essa pasta no VS Code (File → Open Folder), inicie o Claude Code nela e peça *"Leia o ONBOARDING.md e me guie no setup a partir do passo 5"*.

## 5. Dependências Python

No terminal do VS Code (Git Bash), na pasta do workspace:

```bash
python -m pip install -r .claude/skills/google-ads-ratos/requirements.txt
python -m playwright install chromium
```

**Mac:** `pip3 install --user -r ...` e `python3 -m playwright install chromium`.

Avisos de versão (`FutureWarning` etc.) podem ser ignorados.

## 6. Google Ads (credencial sua)

```bash
cd ~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos
cp .env.topserv.example .env.topserv
code .env.topserv
```

Cole os 3 valores do Bitwarden no arquivo e salve. **Você mesmo cola no arquivo, não mande no chat do Claude.** Depois:

```bash
cd scripts
./tsd.sh setup.py oauth    # abre o navegador: entre com a SUA conta Google da TSD (a que tem acesso ao MCC)
./tsd.sh setup.py test     # tem que listar as contas do MCC
```

O `oauth` grava o seu `GOOGLE_ADS_REFRESH_TOKEN` no `.env.topserv` sozinho.

## 7. GTM e GA4 (mesma credencial, tokens separados)

Ainda em `scripts/`:

```bash
./gtm.sh gtm_setup.py oauth    # grava GTM_REFRESH_TOKEN
./gtm.sh gtm_setup.py test     # lista as contas GTM que você enxerga
./gtm.sh ga4_setup.py oauth    # grava GA4_REFRESH_TOKEN
./gtm.sh ga4_setup.py test     # lista as contas GA4
```

## 8. CallRail + transcrição de ligações (call wins)

Usa a **mesma chave da CallRail do Edu**. Ela enxerga a conta da agência (`792265907`) e também as contas próprias dos clientes (Watt's Right, Cool Hand, King's, Hawkins, Lilypad, Neon Monkey, Potomac). Com uma chave sua, você só veria as contas em que foi convidado.

1. Na raiz do workspace:
   ```bash
   cd ~/Documents/GitHub/topserv-workspace
   cp .env.callrail.example .env.callrail
   code .env.callrail
   ```
   Abra o item **"CallRail API (.env.callrail)"** no Bitwarden, copie o conteúdo inteiro por cima do que está no arquivo e salve. **Você mesmo cola no arquivo, não mande no chat do Claude.** O arquivo é gitignored, nunca sobe.
2. Teste a chave:
   ```bash
   cd .claude/skills/google-ads-ratos/scripts
   ./tsd.sh callrail.py /companies.json per_page=5
   ```
   Tem que listar empresas da CallRail.
3. Instale o transcritor (roda local, não precisa de chave nenhuma):
   ```bash
   cd ~/Documents/GitHub/topserv-workspace
   python -m pip install -r .claude/skills/call-wins/requirements.txt
   ```
   **Mac:** `pip3 install --user -r ...`
4. Teste o fluxo completo (puxa 2 dias de ligações da King's, transcreve, apaga no fim):
   ```bash
   python .claude/skills/call-wins/scripts/pull_calls.py kings-window 2026-10-21 2026-10-22
   python .claude/skills/call-wins/scripts/transcribe.py _pessoal/call-wins/kings-window
   rm -rf _pessoal/call-wins/kings-window
   ```
   A primeira transcrição baixa o modelo (~500 MB, uma vez só). Deu certo se apareceu `DONE`.

Pronto. No dia a dia é só pedir pro Claude: *"monta o call wins log da Hawkins de 10-16 a 10-22"*. Ele usa a skill `call-wins` (`.claude/skills/call-wins/SKILL.md`), que puxa as ligações, transcreve no seu computador e escreve o log em `clients/<cliente>/`. O LSA que não passa pela CallRail ele puxa direto do Google Ads, com o acesso do passo 6.

**Regras:** áudio e transcrição ficam em `_pessoal/call-wins/` (têm dados pessoais de clientes, nunca sobem). A chave é só pra leitura: nada de criar, editar ou apagar coisa na CallRail pela API.

## 9. Regra do auto mode (opcional, recomendado)

No auto mode do Claude Code, esta regra deixa o Claude **pausar/ativar** campanhas, ad groups, keywords e anúncios sem pedir confirmação, mas continua pedindo pra **mudança de budget** e **criação** de qualquer coisa. Abra o arquivo de settings do Claude (`C:\Users\<você>\.claude\settings.json` no Windows, `~/.claude/settings.json` no Mac) e acrescente (se já tiver conteúdo, junte, não substitua):

```json
{
  "autoMode": {
    "allow": [
      "$defaults",
      "Bash calls to google-ads-ratos/scripts/tsd.sh update.py that pass --status (ENABLED/PAUSED/REMOVED) to change a Google Ads campaign, keyword, ad group, or ad on a TopServ client account. Does NOT cover --budget (dollar-amount changes) or create.py (new campaign/ad-group/keyword creation) via this same script — those still require confirmation."
    ]
  }
}
```

## 10. Teste final

1. Com a pasta do workspace aberta no VS Code, inicie o Claude Code **nessa pasta** (é o que carrega o `CLAUDE.md` e a memória do time).
2. Peça: *"weekly PPC snapshot da Zen Air"*.
3. Deu certo se o Claude puxou os números pelo `tsd.sh` sem erro de credencial.

---

## Dia a dia

- **Começo:** `git pull --rebase` (o Claude faz isso sozinho ao abrir a sessão).
- **Fim:** `/syncar`. Nada sobe pro GitHub sozinho.
- **Cada cliente tem um dono** (o mesmo do Agency Titan). Vai mexer numa conta de outra pessoa? Avise antes.
- **Aprendizado novo** (cliente, regra, armadilha) vai pra `_contexto/memoria/`, não pra memória pessoal do Claude. Assim chega no resto do time.
- **Coisa pessoal** (anotações suas, arquivos que não são do time) vai em `_pessoal/`, que nunca sobe.
- **Nunca** commitar `.env*`, tokens ou senhas. O `.gitignore` já bloqueia, mas confira o que o `/syncar` lista.
- **Não agende** o refresh diário dos funis (`funnel_refresh_daily.sh`): ele roda só no Mac do Edu.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Python was not found; run without arguments to install from the Microsoft Store` | Atalho da Store ainda ligado ou Python fora do PATH | Passo 2.3; reinstalar o Python marcando "Add python.exe to PATH"; reabrir o VS Code |
| `$'\r': command not found` ao rodar `tsd.sh` | Arquivo `.sh` com fim de linha do Windows | No Git Bash, na pasta do workspace: `sed -i 's/\r$//' .claude/skills/google-ads-ratos/scripts/*.sh` |
| `UnicodeEncodeError` / caractere estranho | Python sem UTF-8 | Passo 2.5 e reabrir o VS Code |
| `gh` ou `python` "não reconhecido" | Programa instalado com o VS Code aberto | Fechar e abrir o VS Code |
| `git push` pede usuário/senha | Git não autenticado | `gh auth login` de novo, respondendo **Yes** pra autenticar o Git |
| Funcionava e parou depois de ~7 dias | OAuth consent screen em modo "Testing" (token expira em 7 dias) | Pedir pro Edu conferir o consent screen (Internal) ou te adicionar como test user; depois rodar o `oauth` de novo |
| `Error 400: redirect_uri_mismatch` no navegador | OAuth client não é do tipo "Desktop app" | Confirmar com o Edu qual client ID usar |
| `PERMISSION_DENIED` ou conta não aparece | Rodou sem o `tsd.sh` ou ainda não tem acesso ao MCC | Sempre `./tsd.sh ...`; conferir o acesso ao MCC |
| `ERRO: perfil nao encontrado` | Falta o `.env.topserv` | Passo 6 |
| GTM publish dá 403 | Token sem escopo de publicação | Rodar `./gtm.sh gtm_setup.py oauth` de novo |
| CallRail dá `401` | `.env.callrail` vazio ou colado errado | Passo 8.1: colar de novo o conteúdo do Bitwarden, sem espaço antes/depois da chave |
| CallRail dá `429` | Limite de requisições da conta | O script espera e tenta de novo sozinho. Se continuar por mais de 1h numa conta só, avisar o Edu |
| `faster-whisper missing` ou erro de DLL / `ctranslate2` ao transcrever | Transcritor não instalado, ou falta o Visual C++ do Windows | Passo 8.3; se for DLL, instalar o "Microsoft Visual C++ Redistributable" (x64) e reabrir o VS Code |
