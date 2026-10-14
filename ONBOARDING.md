# Onboarding — workspace de Paid Ads da TSD

Passo a passo pra deixar o seu Mac com o mesmo setup do Edu: Claude Code + skills + memória do time + acesso por API ao Google Ads, GTM, GA4 e CallRail, e Meta/Agency Titan pelos conectores do Claude.

Leva umas 1 a 2 horas, a maior parte esperando acesso. Faça na ordem.

---

## 1. Peça pro Edu (antes de tudo)

Sem isso os passos seguintes travam:

- [ ] Convite pro **repositório no GitHub** (você precisa de uma conta GitHub).
- [ ] Acesso ao **MCC do Google Ads** `4155514468` com o seu e-mail da TSD.
- [ ] Usuário nos **containers do GTM** e nas **propriedades do GA4** dos clientes que você vai tocar.
- [ ] Acesso às **contas de anúncio no Meta Business Manager**.
- [ ] Usuário na **CallRail** (conta da agência `792265907`).
- [ ] Usuário no **Agency Titan**.
- [ ] Os 3 valores da agência pelo **Bitwarden**: `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`.
- [ ] Acesso de edição ao **Command Center** (artefato no claude.ai).

## 2. Claude

1. Conta no Claude com Claude Code (plano Pro/Max, ou um assento do time se houver).
2. Instale o **VS Code** e a extensão **Claude Code** (ou o CLI `claude`).
3. Em **claude.ai → Settings → Connectors**, conecte com as **suas** contas:
   - **Meta** (Ads)
   - **Agency Titan**
   - **Slack**
   - **Google Drive**

   Os conectores valem no Claude Code quando você está logado na mesma conta.

## 3. Git e o workspace

1. Instale as ferramentas de linha de comando do Mac (trazem `git` e `python3`):
   ```bash
   xcode-select --install
   ```
2. Clone o repositório. O jeito mais fácil é o **GitHub Desktop** (cuida do login): *File → Clone repository*. Ou pelo terminal com a URL que o Edu mandar.
3. **O caminho importa.** O workspace tem que ficar exatamente em:
   ```
   ~/Documents/GitHub/topserv-workspace
   ```
   O GitHub Desktop sugere uma pasta com o nome do repo; troque pra `topserv-workspace`. Scripts e configs contam com esse caminho.
4. Configure seu nome no git (é assim que o Claude sabe quem está na sessão):
   ```bash
   cd ~/Documents/GitHub/topserv-workspace
   git config user.name "Gui"
   git config user.email "<seu e-mail da TSD>"
   ```

## 4. Dependências Python

```bash
cd ~/Documents/GitHub/topserv-workspace
pip3 install --user -r .claude/skills/google-ads-ratos/requirements.txt
python3 -m playwright install chromium
```

Vão aparecer avisos (`FutureWarning`, `NotOpenSSLWarning`) sobre a versão do Python. Pode ignorar: o `tsd.sh` filtra esses avisos.

## 5. Google Ads (credencial sua)

```bash
cd ~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos
cp .env.topserv.example .env.topserv
```

Abra o `.env.topserv` e cole os 3 valores do Bitwarden (developer token, client id, client secret). Depois:

```bash
cd scripts
./tsd.sh setup.py oauth    # abre o navegador: entre com a SUA conta Google da TSD (a que tem acesso ao MCC)
./tsd.sh setup.py test     # tem que listar as contas do MCC
```

O `oauth` grava o seu `GOOGLE_ADS_REFRESH_TOKEN` no `.env.topserv` sozinho.

## 6. GTM e GA4 (mesma credencial, tokens separados)

Ainda em `scripts/`:

```bash
./gtm.sh gtm_setup.py oauth    # grava GTM_REFRESH_TOKEN
./gtm.sh gtm_setup.py test     # lista as contas GTM que você enxerga
./gtm.sh ga4_setup.py oauth    # grava GA4_REFRESH_TOKEN
./gtm.sh ga4_setup.py test     # lista as contas GA4
```

## 7. CallRail

1. Na CallRail: seu perfil → **API Keys** → crie uma chave **sua**.
2. Na raiz do workspace:
   ```bash
   cd ~/Documents/GitHub/topserv-workspace
   cp .env.callrail.example .env.callrail
   ```
   Cole a chave em `CALLRAIL_API_KEY`.
3. Teste:
   ```bash
   cd .claude/skills/google-ads-ratos/scripts
   ./tsd.sh callrail.py /companies.json per_page=5
   ```

## 8. Regra do auto mode (opcional, recomendado)

No auto mode do Claude Code, esta regra deixa o Claude **pausar/ativar** campanhas, ad groups, keywords e anúncios sem pedir confirmação, mas continua pedindo pra **mudança de budget** e **criação** de qualquer coisa. Abra `~/.claude/settings.json` e acrescente (se o arquivo já tiver conteúdo, junte, não substitua):

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

## 9. Teste final

1. Abra a pasta `~/Documents/GitHub/topserv-workspace` no VS Code e inicie o Claude Code **nessa pasta** (é o que carrega o `CLAUDE.md` e a memória do time).
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
| Funcionava e parou depois de ~7 dias | OAuth consent screen em modo "Testing" (token expira em 7 dias) | Pedir pro Edu conferir o consent screen (Internal) ou te adicionar como test user; depois rodar o `oauth` de novo |
| `Error 400: redirect_uri_mismatch` no navegador | OAuth client não é do tipo "Desktop app" | Confirmar com o Edu qual client ID usar |
| `PERMISSION_DENIED` ou conta não aparece | Rodou sem o `tsd.sh` ou ainda não tem acesso ao MCC | Sempre `./tsd.sh ...`; conferir o acesso ao MCC |
| `ERRO: perfil nao encontrado` | Falta o `.env.topserv` | Passo 5 |
| GTM publish dá 403 | Token sem escopo de publicação | Rodar `./gtm.sh gtm_setup.py oauth` de novo |
| `git` abre aviso do Xcode | Faltam as Command Line Tools | `xcode-select --install` (ou usar o GitHub Desktop) |
