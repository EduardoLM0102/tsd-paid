#!/usr/bin/env python3
"""
GA4 Setup — gera o refresh token do Google Analytics 4 (somente leitura).

Reaproveita o MESMO OAuth client Desktop do Google Ads (GOOGLE_ADS_CLIENT_ID/SECRET),
com escopo analytics.readonly e refresh token SEPARADO (GA4_REFRESH_TOKEN).

Usa duas APIs (ambas precisam estar habilitadas no Google Cloud):
  - Google Analytics Admin API   (analyticsadmin v1beta)  -> listar contas/properties
  - Google Analytics Data API    (analyticsdata v1beta)   -> rodar relatorios

Uso:
  ./gtm.sh ga4_setup.py oauth   # gera GA4_REFRESH_TOKEN
  ./gtm.sh ga4_setup.py test    # lista contas e properties acessiveis
  ./gtm.sh ga4_setup.py check
"""

import hashlib
import os
import re
import socket
import sys
import webbrowser
from urllib.parse import unquote

# Mesmo motivo do GTM: o client ja tem outros escopos concedidos, e o Google
# devolve a uniao deles. Sem isso o oauthlib trata "scope mudou" como erro.
os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "1")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
ENV_PATH = os.environ.get("GADS_ENV_PATH") or os.path.join(SKILL_DIR, ".env")
SERVER = "127.0.0.1"

# Somente leitura: cobre Admin API (read) e Data API.
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

sys.path.insert(0, SCRIPT_DIR)
from lib import _load_env_file, mask_token


def ga4_credentials():
    """Credenciais do GA4 (client do Ads + GA4_REFRESH_TOKEN)."""
    from google.oauth2.credentials import Credentials

    _load_env_file()
    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "").strip()
    refresh_token = os.environ.get("GA4_REFRESH_TOKEN", "").strip()

    missing = [n for n, v in [
        ("GOOGLE_ADS_CLIENT_ID", client_id),
        ("GOOGLE_ADS_CLIENT_SECRET", client_secret),
        ("GA4_REFRESH_TOKEN", refresh_token),
    ] if not v]
    if missing:
        print(f"ERRO: falta no .env ({ENV_PATH}): {', '.join(missing)}", file=sys.stderr)
        if missing == ["GA4_REFRESH_TOKEN"]:
            print("  Rode: ./gtm.sh ga4_setup.py oauth", file=sys.stderr)
        sys.exit(1)

    return Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )


def admin_service():
    from googleapiclient.discovery import build
    return build("analyticsadmin", "v1beta", credentials=ga4_credentials(), cache_discovery=False)


def data_service():
    from googleapiclient.discovery import build
    return build("analyticsdata", "v1beta", credentials=ga4_credentials(), cache_discovery=False)


# ---------------------------------------------------------------------------

def cmd_check():
    print("=== Dependencias ===")
    try:
        import googleapiclient  # noqa: F401
        print("OK: google-api-python-client")
    except ImportError:
        print("FALTA: pip3 install --user google-api-python-client")
    print()
    print("=== .env ===")
    _load_env_file()
    for key in ["GOOGLE_ADS_CLIENT_ID", "GOOGLE_ADS_CLIENT_SECRET", "GA4_REFRESH_TOKEN"]:
        val = os.environ.get(key)
        present = bool(val and val.strip())
        display = mask_token(val) if present and "TOKEN" in key else ("OK" if present else "")
        print(f"  {'OK' if present else 'FALTA'}: {key} {display}")
    if not (os.environ.get("GA4_REFRESH_TOKEN") or "").strip():
        print("\nPROXIMO PASSO: ./gtm.sh ga4_setup.py oauth")


def find_free_port(start=8080, end=8090):
    for port in range(start, end + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((SERVER, port)); s.close(); return port
        except OSError:
            continue
    return None


def run_oauth():
    from google_auth_oauthlib.flow import Flow

    _load_env_file()
    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        print(f"ERRO: CLIENT_ID/SECRET faltando em {ENV_PATH}")
        sys.exit(1)

    port = find_free_port()
    if not port:
        print("ERRO: nenhuma porta livre 8080-8090."); sys.exit(1)
    redirect_uri = f"http://{SERVER}:{port}"

    flow = Flow.from_client_config({
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }, scopes=SCOPES)
    flow.redirect_uri = redirect_uri

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        state=hashlib.sha256(os.urandom(1024)).hexdigest(),
        prompt="consent",
        include_granted_scopes="true",
    )

    print("\n" + "=" * 60)
    print("  AUTORIZACAO GOOGLE ANALYTICS 4")
    print("=" * 60 + "\n")
    print("Abre esta URL no browser (ou ela vai abrir sozinha):\n")
    print(f"  {authorization_url}\n")
    print(f"Aguardando callback em {redirect_uri} ...\n")
    webbrowser.open(authorization_url)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER, port)); sock.listen(1)
    connection, _ = sock.accept()
    data = connection.recv(4096).decode("utf-8")

    match = re.search(r"GET\s\/\?(.*?)\s", data)
    if not match:
        print("ERRO: callback invalido."); connection.close(); sock.close(); sys.exit(1)
    params = {}
    for pair in match.group(1).split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1); params[k] = unquote(v)
    if "error" in params:
        print(f"ERRO do Google: {params['error']}"); connection.close(); sock.close(); sys.exit(1)
    code = params.get("code", "")

    html = ("<html><head><meta charset='utf-8'></head><body style='font-family:sans-serif;"
            "display:flex;align-items:center;justify-content:center;height:100vh;background:#FAF7F2;'>"
            "<div style='text-align:center;'><h1 style='color:#4CAF50;'>Pronto!</h1>"
            "<p style='color:#57534E;font-size:1.2rem;'>GA4 autorizado. Pode fechar esta aba.</p>"
            "</div></body></html>")
    connection.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html}".encode())
    connection.close(); sock.close()

    flow.fetch_token(code=code)
    token = flow.credentials.refresh_token
    if not token:
        print("ERRO: Google nao retornou refresh token.")
        print("  Revogue em https://myaccount.google.com/permissions e tente de novo.")
        sys.exit(1)
    print(f"Refresh token gerado: {mask_token(token)}")
    return token


def save_token(token):
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    if "GA4_REFRESH_TOKEN=" in content:
        content = re.sub(r'GA4_REFRESH_TOKEN=.*', f'GA4_REFRESH_TOKEN="{token}"', content)
    else:
        content = content.rstrip("\n") + f'\nGA4_REFRESH_TOKEN="{token}"\n'
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Salvo em {ENV_PATH}")


def cmd_oauth():
    save_token(run_oauth())
    print("\nProximo passo: ./gtm.sh ga4_setup.py test")


def cmd_test():
    print("Testando conexao com o GA4...")
    svc = admin_service()
    try:
        accounts = svc.accounts().list().execute().get("accounts", [])
    except Exception as e:
        print(f"ERRO: {e}")
        print("\nSe disser 'API has not been used', habilite no Google Cloud:")
        print("  - Google Analytics Admin API")
        print("  - Google Analytics Data API")
        sys.exit(1)
    print(f"\nConexao OK! {len(accounts)} conta(s) GA4:")
    for a in accounts:
        print(f"  {a.get('displayName')}  ({a.get('name')})")


COMMANDS = {"check": cmd_check, "oauth": cmd_oauth, "test": cmd_test}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Uso: python3 ga4_setup.py <check|oauth|test>")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()
