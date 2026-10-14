#!/usr/bin/env bash
# ============================================================================
# ZEN AIR HEATING AND COOLING — Change 2: split non-branded out of "Branded"
# Customer: 4360840956
# STAGED 2026-08-03. BUILD block already RUN and confirmed via API — new
# campaign 24100030790 ("TSD_08.03_Search_NonBranded_Evergreen") + ad group
# 205687909824 ("Zen Air HVAC Nonbranded") + 30 keywords + RSA exist in the
# account, all PAUSED. The BUILD block below is commented out (historical
# record — do not re-run, it would create duplicates).
# DO NOT RUN CUTOVER until written client approval is on the AM ticket
# (Andrea / Eddie).
#
# WHY (last 30 days, campaign 23675783172 "TSD_05.13_Search_Branded_Evergreen")
#   Despite the name, 87% of spend is on generic broad-match HVAC terms, not
#   brand terms. Blended CPL for the whole campaign is $306.99 (16 conv /
#   $4,911.81), but that number is misleading:
#     Branded terms only  ("zen air ..."):            ~$630 spend / 6 conv  = ~$105 CPL
#     Non-branded broad   ("hvac contractors near me",
#                          "emergency heating service ga", etc.):
#                                                       ~$4,271 spend / 10 conv = ~$427 CPL
#   Splitting lets each campaign be judged (and bid) on its own economics
#   instead of the broad-match spend hiding how cheap branded actually is.
#   This is the follow-up flagged in change_pmax_off_search_up.sh's own
#   warning ("hold the +$50 until the non-branded traffic is split into its
#   own campaign").
#
# WHAT IT DOES
#   BUILD (already run, PAUSED, no live impact):
#     1. New campaign "TSD_08.03_Search_NonBranded_Evergreen", $100.00/day, PAUSED
#     2. New ad group "Zen Air HVAC Nonbranded" in that campaign
#     3. The 30 non-branded keywords added to the new ad group (same match
#        types as today), all inheriting PAUSED status from the ad group
#     4. A new RSA in the new ad group, reusing only the already-approved
#        non-branded headlines/descriptions from the existing ad (brand
#        mentions removed/kept out)
#   CUTOVER (changes live serving — commented out at the bottom, pending
#   AM ticket approval):
#     5. Drop old campaign 23675783172 budget $200 -> $100/day (branded-only
#        campaign doesn't need to fund the broad-match spend anymore)
#     6. Enable the new campaign + new ad group
#     7. Pause the 30 non-branded keywords inside the OLD ad group (193305460463)
#        so they stop competing there once the new campaign is live
#
# NET EFFECT: account daily budget stays flat at $200/day (100 branded +
# 100 non-branded) — this is a structural split, not a budget increase.
#
# BEFORE RUNNING CUTOVER: review the new RSA copy and keyword bids in the
# UI. Keywords/ad group were created with no explicit bid (inherits
# create.py defaults) — sanity-check CPC bids before enabling.
# ============================================================================
set -euo pipefail
cd "$(dirname "$0")/../../.claude/skills/google-ads-ratos"

CID=4360840956
OLD_CAMP=23675783172
OLD_AG=193305460463    # "Zen Air Heating and Cooling" ad group (branded, stays)
NEW_CAMP=24100030790   # "TSD_08.03_Search_NonBranded_Evergreen" (created, PAUSED)
NEW_AG=205687909824    # "Zen Air HVAC Nonbranded" (created, PAUSED)

# ============================================================================
# BUILD — already executed 2026-08-03. Left here as a record; do not re-run.
# ============================================================================
# # --- STEP 1: create the new campaign (PAUSED, $100/day) --------------------
# OUT=$(./scripts/tsd.sh create.py campaign --customer-id $CID \
#         --name "TSD_08.03_Search_NonBranded_Evergreen" \
#         --type SEARCH \
#         --budget 10000)   # centavos: 10000 = $100.00/dia
# echo "$OUT"
#
# # --- STEP 2: create the new ad group (PAUSED) ------------------------------
# OUT=$(./scripts/tsd.sh create.py ad-group --customer-id $CID --campaign-id $NEW_CAMP \
#         --name "Zen Air HVAC Nonbranded")
# echo "$OUT"
#
# # --- STEP 3: add the 30 non-branded keywords to the new ad group ----------
# # text|match_type, same set (and match types) that sit in OLD_AG
# NONBRANDED_KEYWORDS=(
#   "hvac contractors near me|BROAD"                 # $3,723.69 / 8 conv in OLD_AG
#   "emergency heating service ga|BROAD"              # $520.39 / 2 conv in OLD_AG
#   "commercial air conditioning ga|BROAD"            # $27.31 / 0 conv in OLD_AG
#   "furnace repair duluth|BROAD"
#   "furnace repair duluth|EXACT"
#   "local hvac repair company|BROAD"
#   "ac repair duluth ga|EXACT"
#   "ac repair duluth ga|BROAD"
#   "commercial hvac duluth|BROAD"
#   "commercial hvac duluth|EXACT"
#   "hvac contractors ga|BROAD"
#   "hvac contractors ga|EXACT"
#   "heating repair duluth ga|EXACT"
#   "heating repair duluth ga|BROAD"
#   "emergency ac repair ga|EXACT"
#   "emergency ac repair ga|BROAD"
#   "indoor air quality services ga|EXACT"
#   "indoor air quality services ga|BROAD"
#   "air flow ventilation pros ga|EXACT"
#   "air flow ventilation pros ga|BROAD"
#   "residential hvac services duluth|BROAD"
#   "air flow and ventilation experts|BROAD"
#   "smart thermostat installation ga|BROAD"
#   "affordable ac repair duluth|BROAD"
#   "smart hvac systems duluth|EXACT"
#   "smart hvac systems duluth|BROAD"
#   "best hvac company duluth ga|EXACT"
#   "best hvac company duluth ga|BROAD"
#   "indoor air quality testing duluth|BROAD"
#   "ac repair duluth georgia|BROAD"
# )
# for entry in "${NONBRANDED_KEYWORDS[@]}"; do
#   IFS='|' read -r kw_text kw_match <<< "$entry"
#   ./scripts/tsd.sh create.py keyword --customer-id $CID --ad-group-id $NEW_AG \
#     --text "$kw_text" --match-type "$kw_match"
# done
#
# # --- STEP 4: create the RSA in the new ad group (PAUSED) -------------------
# # Headlines/descriptions reused verbatim from the existing approved RSA in
# # OLD_AG, minus anything mentioning "Zen Air" / "callzenair" brand terms.
# ./scripts/tsd.sh create.py rsa --customer-id $CID --ad-group-id $NEW_AG \
#   --url "https://callzenair.com/" \
#   --headlines "AC Repair Duluth GA|HVAC Contractors Georgia|Stress-Free HVAC Service|Request Your Free Estimate|Expert AC & Heating Repair|Heating Repair Experts|Licensed, Bonded & Insured|Commercial HVAC Services|Emergency AC Repair|HVAC Contractors Near Me" \
#   --descriptions "Top-rated HVAC experts in GA. From AC repair to smart systems, call for a free estimate.|Licensed and insured contractors. Experience the difference in home comfort."

echo "BUILD already done (all PAUSED). Campaign = $NEW_CAMP, ad group = $NEW_AG"
echo "Review keywords/RSA/bids in the UI, confirm AM ticket approval, then"
echo "uncomment and run the CUTOVER block below."

# ============================================================================
# CUTOVER — run ONLY after client approval is on the AM ticket. This changes
# live serving: old campaign budget drops, new campaign goes live, and the
# non-branded keywords stop serving out of the old branded ad group.
# ============================================================================
# ./scripts/tsd.sh update.py campaign --customer-id $CID --campaign-id $OLD_CAMP --budget 10000   # $200 -> $100/day
# ./scripts/tsd.sh update.py campaign --customer-id $CID --campaign-id $NEW_CAMP --status ENABLED
# ./scripts/tsd.sh update.py ad-group --customer-id $CID --ad-group-id $NEW_AG --status ENABLED
#
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 296788112051    --status PAUSED  # "hvac contractors near me" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 859562546367    --status PAUSED  # "emergency heating service ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 310990134369    --status PAUSED  # "commercial air conditioning ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 302102393203    --status PAUSED  # "furnace repair duluth" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 385015682041    --status PAUSED  # "furnace repair duluth" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 305440965525    --status PAUSED  # "local hvac repair company" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 309440560782    --status PAUSED  # "ac repair duluth ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 330289070777    --status PAUSED  # "ac repair duluth ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 310679090521    --status PAUSED  # "commercial hvac duluth" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 453543712457    --status PAUSED  # "commercial hvac duluth" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 348400405674    --status PAUSED  # "hvac contractors ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 643874264084    --status PAUSED  # "hvac contractors ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 385749122543    --status PAUSED  # "heating repair duluth ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 667296864672    --status PAUSED  # "heating repair duluth ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 628376058206    --status PAUSED  # "emergency ac repair ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 777381230100    --status PAUSED  # "emergency ac repair ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2473698104290   --status PAUSED  # "indoor air quality services ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2493656191803   --status PAUSED  # "indoor air quality services ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2473698104330   --status PAUSED  # "air flow ventilation pros ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2493656191563   --status PAUSED  # "air flow ventilation pros ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263451758   --status PAUSED  # "residential hvac services duluth" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263451918   --status PAUSED  # "air flow and ventilation experts" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263451958   --status PAUSED  # "smart thermostat installation ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263451998   --status PAUSED  # "affordable ac repair duluth" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263604638   --status PAUSED  # "smart hvac systems duluth" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2493656191603   --status PAUSED  # "smart hvac systems duluth" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263604878   --status PAUSED  # "best hvac company duluth ga" EXACT
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2493656191643   --status PAUSED  # "best hvac company duluth ga" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263605078   --status PAUSED  # "indoor air quality testing duluth" BROAD
# ./scripts/tsd.sh update.py keyword --customer-id $CID --ad-group-id $OLD_AG --keyword-id 2474263605318   --status PAUSED  # "ac repair duluth georgia" BROAD
#
# echo "==> Verifying"
# ./scripts/tsd.sh read.py campaigns --customer-id $CID \
#   | python3 -c "
# import json,sys
# for r in json.load(sys.stdin):
#     c=r['campaign']
#     if c['id'] in ('$OLD_CAMP','$NEW_CAMP'):
#         print(c['status'], r.get('campaign_budget',{}).get('amount'), c['name'])
# "
