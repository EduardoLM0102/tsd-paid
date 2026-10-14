#!/usr/bin/env bash
# ============================================================================
# PROUD POPS — Change 1: rehome the generic "plumber" head terms
# Campaign: TSD_05.14_Leads_Search_Nonbranded_Plumbing (23853484024)
# Customer: 1051843378  |  Bid strategy: MAXIMIZE_CONVERSIONS (no CPC bids)
#
# WHY: "plumber san antonio tx" (QS 3, $20.66 CPC, 36% of spend, 3.6% CTR) and
# the other generic plumber terms live in AG1_LeakDetection -> query/ad mismatch
# -> Below-Average expected CTR -> low QS -> ~82% of impression share lost to Rank.
# Fix: give them a matched home (General Plumber ad group + on-theme RSA) so CTR
# and QS recover. Nothing is paused/enabled until the CUTOVER block at the bottom.
# ============================================================================
set -euo pipefail
cd "$(dirname "$0")/../../.claude/skills/google-ads-ratos/scripts"

CID=1051843378
CAMP=23853484024
OLD_AG=196726297659   # AG1_Plumbing_LeakDetection (where the generic terms sit now)

# --- STEP 1: create the new ad group (PAUSED) and capture its ID ------------
OUT=$(./tsd.sh create.py ad-group --customer-id $CID --campaign-id $CAMP \
        --name "AG4_Plumbing_General")
echo "$OUT"
AG4=$(echo "$OUT" | python3 -c "import sys,json,re;print(re.search(r'adGroups/(\d+)',sys.stdin.read()).group(1))")
echo ">>> New ad group AG4_Plumbing_General = $AG4"

# --- STEP 2: add the generic plumber keywords to AG4 ------------------------
./tsd.sh create.py keyword --customer-id $CID --ad-group-id $AG4 --text "plumber san antonio"    --match-type EXACT
./tsd.sh create.py keyword --customer-id $CID --ad-group-id $AG4 --text "plumber near me"        --match-type EXACT
./tsd.sh create.py keyword --customer-id $CID --ad-group-id $AG4 --text "plumber san antonio tx" --match-type PHRASE

# --- STEP 3: create the on-theme RSA in AG4 (PAUSED) -----------------------
# Homeowner voice, no AI tells. All headlines <=30, descriptions <=90 chars.
./tsd.sh create.py rsa --customer-id $CID --ad-group-id $AG4 \
  --url "https://proudpops.com/" --path1 "Plumber" --path2 "San-Antonio" \
  --headlines "Plumber in San Antonio|San Antonio Plumbers|Same-Day Plumber Near You|Licensed San Antonio Plumber|Family-Owned & Local|Upfront Pricing, No Surprises|Free Pop-In Visit|5-Star Rated Plumbers|Need a Plumber Today?|Fast, Friendly Plumbing|Call Proud Pops Plumbing|Trusted Local Plumbers|Book Your Plumber Online|Serving San Antonio, TX|Honest Plumbing Done Right" \
  --descriptions "Need a plumber in San Antonio? Proud Pops comes same-day with upfront, honest pricing.|Licensed, family-owned plumbers serving San Antonio and the Hill Country. Book online.|From leaks to water heaters, we fix it right the first time. Free Pop-In, no hidden fees.|Friendly, 5-star plumbers who treat your home right. Call Proud Pops today."

echo ""
echo "=================================================================="
echo "BUILD DONE (all PAUSED). New ad group AG4 = $AG4"
echo "Review the RSA in the UI, then run the CUTOVER block below."
echo "=================================================================="

# ============================================================================
# CUTOVER — run ONLY after the RSA copy is approved. This changes live serving.
# Enables AG4 and pauses the 3 generic terms in AG1 so they don't compete.
# Uncomment to execute (replace $AG4 with the printed ID if running separately).
# ============================================================================
# ./tsd.sh update.py ad-group --customer-id $CID --ad-group-id $AG4 --status ENABLED
# ./tsd.sh update.py keyword  --customer-id $CID --ad-group-id $OLD_AG --keyword-id 354371636767 --status PAUSED  # "plumber san antonio tx" PHRASE
# ./tsd.sh update.py keyword  --customer-id $CID --ad-group-id $OLD_AG --keyword-id 1178376016   --status PAUSED  # "plumber san antonio" EXACT
# ./tsd.sh update.py keyword  --customer-id $CID --ad-group-id $OLD_AG --keyword-id 21810437552  --status PAUSED  # "plumber near me" EXACT
