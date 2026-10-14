"""All Heart — Phase 2 ramp monitor + flip go/no-go.
Run anytime after the 2026-07-10 tCPA change ($29->$65) to see if the ramp is working
and whether it's safe to run phase2_cutover.py.

Run:  GADS_ENV_PATH=.../.env.topserv python3 phase2_monitor.py
"""
import os
import sys, json
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID="9205826499"
NONBRAND="23685938569"
NEW_ADGROUPS=["199017381820","203964394691","196979638774","198469621179","198469621619"]
BRAND_ADGROUP="198469690939"
BASELINE_IS=0.28   # ~28% pre-change (Jul 9)

def cost(m):
    v=float(m.get("cost_micros",0)); return v/1e6 if v>100000 else v

print("="*66)
print("ALL HEART — PHASE 2 RAMP MONITOR")
print("="*66)

print("\n[1] Daily IS / rank-lost / spend / CPL (since the tCPA change):")
rows=run_query(CID, f"""
SELECT segments.date, metrics.search_impression_share,
 metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share,
 metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM campaign WHERE campaign.id={NONBRAND}
 AND segments.date BETWEEN '2026-07-08' AND '2026-07-20' ORDER BY segments.date""")
print(f"  {'date':11}{'IS%':>7}{'rankLost%':>10}{'budgLost%':>10}{'spend':>8}{'conv':>6}{'CPL':>8}")
last_is=None
for r in rows:
    m=r["metrics"]; d=r["segments"]["date"]
    isv=float(m.get("search_impression_share",0)); last_is=isv
    conv=float(m.get("conversions",0)); c=cost(m)
    cpl=(c/conv) if conv>0 else 0
    print(f"  {d:11}{isv*100:6.1f}{float(m.get('search_rank_lost_impression_share',0))*100:9.1f}"
          f"{float(m.get('search_budget_lost_impression_share',0))*100:9.1f}{c:8.2f}{conv:6.1f}{cpl:8.2f}")

print("\n[2] New RSAs — approval + ad strength (must be APPROVED before flip):")
ads=run_query(CID, f"""
SELECT ad_group.name, ad_group_ad.policy_summary.approval_status,
 ad_group_ad.ad_strength, ad_group_ad.status
FROM ad_group_ad
WHERE ad_group.id IN ({','.join(NEW_ADGROUPS+[BRAND_ADGROUP])})""")
all_ok=True
for a in ads:
    ap=a.get("ad_group_ad",{}).get("policy_summary",{}).get("approval_status","?")
    st=a.get("ad_group_ad",{}).get("ad_strength","?")
    if ap not in ("APPROVED","APPROVED_LIMITED"): all_ok=False
    print(f"  {a['ad_group']['name']:20} approval={ap:18} strength={st}")

print("\n[3] VERDICT:")
if last_is is not None and last_is > BASELINE_IS*1.25:
    print(f"  IS climbing ({last_is*100:.0f}% vs ~28% baseline) — ramp is working.")
else:
    print(f"  IS not clearly up yet (latest {last_is*100:.0f}% vs ~28%). Give it another day or nudge tCPA.")
print("  RSAs all approved: " + ("YES — safe to flip." if all_ok else "NO — do NOT flip until fixed."))
print("  Flip = run phase2_cutover.py (DRY_RUN=True first).")
