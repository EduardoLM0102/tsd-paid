#!/usr/bin/env bash
# Roda qualquer script da skill no perfil TopServ (MCC 4155514468),
# sem tocar no .env default da skill.
#
#   ./tsd.sh setup.py oauth
#   ./tsd.sh setup.py test
#   ./tsd.sh read.py campaigns --customer-id 9205826499 --date-range LAST_30_DAYS
#   ./tsd.sh insights.py account --customer-id 8634274092 --date-range LAST_7_DAYS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export GADS_ENV_PATH="$(dirname "$SCRIPT_DIR")/.env.topserv"
export PYTHONUNBUFFERED=1

if [[ ! -f "$GADS_ENV_PATH" ]]; then
  echo "ERRO: perfil nao encontrado em $GADS_ENV_PATH" >&2
  exit 1
fi

cd "$SCRIPT_DIR"

# setup.py e interativo (browser + prompts): nao filtrar, nao mexer no stdout.
if [[ "${1:-}" == "setup.py" ]]; then
  exec python3 "$@"
fi

python3 "$@" 2>&1 \
  | grep -v "Warning\|warnings.warn\|site-packages\|eol_message\|Request made\|Client inicializado" \
  || true
