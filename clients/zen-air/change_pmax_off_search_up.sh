#!/usr/bin/env bash
# Zen Air Heating and Cooling — customer 4360840956
# STAGED 2026-07-31. DO NOT RUN until written client approval is on the AM ticket (Andrea / Eddie).
#
# WHAT IT DOES
#   1. Pauses PMax  TSD_03.23_PMAX_HVAC_Calls   (22959264938)  — was $100.00/day
#   2. Raises Search TSD_05.13_Search_Branded_Evergreen (23675783172) $150.00 -> $200.00/day
#
# WHY (last 30 days)
#   PMax:   $2,478.28 /  1 conv  = $2,478.28 CPA  (4,702 clicks, 143,266 impr)
#   Search: $4,551.22 / 14 conv  =   $325.09 CPA
#
# NET EFFECT: account daily budget $250 -> $200 (the other $50/day comes off the table).
#
# READ THIS BEFORE RUNNING — the +$50 does NOT land on branded terms.
#   Inside campaign 23675783172, last 30 days:
#     "hvac contractors near me"   BROAD  $3,425.62 /  6 conv = $570.94 CPA  (75% of spend)
#     "zen air heating and cooling" EXACT   $455.14 /  6 conv =  $75.86 CPA
#   Adding budget to this campaign as-is mostly feeds the $571 CPA broad keyword.
#   Consider pausing/negativing the broad term in the same change, or hold the +$50
#   until the non-branded traffic is split into its own campaign.

set -euo pipefail
cd "$(dirname "$0")/../../.claude/skills/google-ads-ratos"

echo "==> Pausing PMax 22959264938"
./scripts/tsd.sh update.py campaign \
  --customer-id 4360840956 \
  --campaign-id 22959264938 \
  --status PAUSED

echo "==> Raising Search 23675783172 budget to \$200/day"
./scripts/tsd.sh update.py campaign \
  --customer-id 4360840956 \
  --campaign-id 23675783172 \
  --budget 20000   # update.py toma CENTAVOS: 20000 = $200.00/dia

echo "==> Verifying"
./scripts/tsd.sh read.py campaigns --customer-id 4360840956 \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin):
    c=r['campaign']
    if c['id'] in ('22959264938','23675783172'):
        print(c['status'], r.get('campaign_budget',{}).get('amount'), c['name'])
"
