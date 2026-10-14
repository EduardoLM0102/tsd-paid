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
export PYTHONUTF8=1   # Windows: UTF-8 em arquivos e no terminal (acentos/emoji)

# Mac: python3. Windows: python (o "python3" de lá costuma ser o atalho da Microsoft Store)
PY=python3
"$PY" -c "import sys" >/dev/null 2>&1 || PY=python

if [[ ! -f "$GADS_ENV_PATH" ]]; then
  echo "ERRO: perfil nao encontrado em $GADS_ENV_PATH" >&2
  exit 1
fi

cd "$SCRIPT_DIR"

# setup.py e interativo (browser + prompts): nao filtrar, nao mexer no stdout.
if [[ "${1:-}" == "setup.py" ]]; then
  exec "$PY" "$@"
fi

"$PY" "$@" 2>&1 \
  | grep -v "Warning\|warnings.warn\|site-packages\|eol_message\|Request made\|Client inicializado" \
  || true
