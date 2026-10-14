#!/usr/bin/env bash
# Roda os scripts de GTM no perfil TopServ (.env.topserv), sem tocar no .env default da skill.
#
#   ./gtm.sh gtm_setup.py oauth
#   ./gtm.sh gtm_setup.py test
#   ./gtm.sh gtm.py accounts
#   ./gtm.sh gtm.py list --account 123456 --container 7654321
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export GADS_ENV_PATH="$(dirname "$SCRIPT_DIR")/.env.topserv"
export PYTHONUNBUFFERED=1

if [[ ! -f "$GADS_ENV_PATH" ]]; then
  echo "ERRO: perfil nao encontrado em $GADS_ENV_PATH" >&2
  exit 1
fi

cd "$SCRIPT_DIR"

# *_setup.py (oauth) e interativo (browser): nao filtrar stdout.
if [[ "${1:-}" == *_setup.py ]]; then
  exec python3 "$@"
fi

python3 "$@" 2>&1 \
  | grep -v "Warning\|warnings.warn\|site-packages\|eol_message\|file_cache\|oauth2client" \
  || true
