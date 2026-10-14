#!/bin/bash
# Scheduled Command Center funnel refresh. RUNS ON EDU'S MAC ONLY: one machine writes the funnels, never two (launchd: ~/Library/LaunchAgents/com.tsd.funnel-refresh.plist, 08:00 Brasilia, once a day (Edu 10-10)).
# 1) pull: funnel_build.py via tsd.sh (read-only Google Ads + CallRail)  2) push: headless Claude writes the JSON into the
# Command Center db (funnels/<client>) with ArtifactData. Log: ~/Library/Logs/tsd-funnel-refresh.log
export PATH="$HOME/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
WS="$HOME/Documents/GitHub/topserv-workspace"
TSD=$WS/.claude/skills/google-ads-ratos/scripts/tsd.sh
URL=https://claude.ai/artifact/1gah5xuCXDADf4kYVYp95q
# newest Claude Code binary bundled with the VS Code extension (the npm "claude" is too old for ArtifactData)
CLAUDE=$(ls -d "$HOME"/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude 2>/dev/null | sort -V | tail -1)
[ -x "$CLAUDE" ] || CLAUDE=claude
echo "=== $(date '+%Y-%m-%d %H:%M %Z') === using $CLAUDE ($("$CLAUDE" --version 2>/dev/null | head -1))"
for CLIENT in $(python3 -c "import json;print(' '.join(json.load(open('$WS/paid/funnels/clients.json'))['clients']))"); do
  OUT=$("$TSD" "$WS/paid/funnels/funnel_build.py" --client "$CLIENT" 2>&1)
  JSON=$(echo "$OUT" | sed -n 's/^wrote \(.*\.json\).*/\1/p')
  if [ -z "$JSON" ] || [ ! -f "$JSON" ]; then echo "$CLIENT: PULL FAILED"; echo "$OUT" | tail -5; continue; fi
  echo "$CLIENT: pulled $JSON"
  cd "$(dirname "$JSON")" && "$CLAUDE" -p "Use the ArtifactData tool (load it with ToolSearch first if it isn't loaded). Artifact url: $URL.
Step 1: action get, collection funnels, doc_id $CLIENT (no out_dir). Only note the document's version number; ignore its content.
Step 2: action set, collection funnels, doc_id $CLIENT, file_path $JSON, if_version = that version (omit if_version only if step 1 found no document).
Do nothing else. Reply with exactly one line: OK <new version> or FAIL <reason>." \
    --allowedTools "ArtifactData" "ToolSearch" --model sonnet < /dev/null 2>&1 | tail -3
done
