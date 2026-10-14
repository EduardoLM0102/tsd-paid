# Setup Google Ads API — TopServ

> **Pessoa nova no time?** Use o `ONBOARDING.md` na raiz do workspace. As credenciais da agência (developer token + OAuth client) já existem: peça ao Edu. Este arquivo é só pra criar credenciais **do zero** (token/projeto novos).

Você já tem acesso ao MCC. Faltam 3 credenciais de API. Ordem:

## 0) Antes de tudo — pergunte ao time
A TopServ é uma agência; **provavelmente já existe um developer token** no MCC. Pergunte à **Andrea / Mo** se já há `developer token` + projeto OAuth da agência. Se sim, pula a etapa 1 (e talvez a 2). Isso evita pedir aprovação nova ao Google.

## 1) Developer token (no MCC da TopServ)
1. Entre no **MCC** em ads.google.com com a conta que tem acesso.
2. **Tools → Setup → API Center** (só aparece em manager account).
3. Pegue/solicite o **developer token**. O token "Test" sai na hora mas só funciona em contas de teste; para contas reais precisa de **Basic access** (preenche um formulário curto; costuma sair rápido).
4. Copie o token → vai em `GOOGLE_ADS_DEVELOPER_TOKEN` no `.env.topserv`.

## 2) OAuth client (Google Cloud Console)
1. console.cloud.google.com → crie/selecione um projeto.
2. **APIs & Services → Library →** ative a **"Google Ads API"**.
3. **OAuth consent screen** → tipo Internal (se for Workspace da TopServ) ou External + se adicione como test user.
4. **Credentials → Create credentials → OAuth client ID → tipo "Desktop app"**.
5. Copie **Client ID** e **Client secret** → `.env.topserv` (`GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`).

## 3) MCC ID
Pegue o número do MCC (canto superior do Google Ads, formato 123-456-7890) → coloque **sem hífens** em `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.

## 4) Refresh token (automático, depois dos itens acima)
Com developer token + client id/secret + MCC já no `.env.topserv`, o próprio script gera o refresh token:
```bash
cd .claude/skills/google-ads-ratos/scripts
./tsd.sh setup.py oauth   # abre o navegador, você autoriza com a conta que tem acesso ao MCC
./tsd.sh setup.py test    # confirma a conexão
```
O `oauth` grava o `GOOGLE_ADS_REFRESH_TOKEN` no `.env.topserv` sozinho.

## Pronto
Depois do `test` passar, dá pra começar (read-only primeiro, alinhado à auditoria):
```bash
./tsd.sh read.py accounts                                   # lista contas sob o MCC
./tsd.sh insights.py account --customer-id XXXX --date-range LAST_30_DAYS
```

Tutorial em vídeo/print das credenciais: ratosdeia.com.br/assets/tutorial-token-google-ads/

**Nota de governança:** é o MCC de um empregador. Gere as credenciais com o ok da Andrea/Mo e comece com leitura. O `.env.topserv` fica só na sua máquina (está no .gitignore, não vai pro GitHub).
