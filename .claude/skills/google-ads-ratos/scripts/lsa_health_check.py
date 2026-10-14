#!/usr/bin/env python3
"""LSA health check across all TSD accounts: verification artifacts
(license/insurance/background check/business registration) + campaign
primary_status, reduced to CURRENT state (not full history) and flagged
for anything that looks like it's blocking delivery."""
import sys
from datetime import datetime, date
sys.path.insert(0, ".")
from lib import init_client

LSA_ACCOUNTS = [
    {"client": "Cool Hand Electric", "customer_id": "9865206319"},
    {"client": "Mission Accomplished", "customer_id": "4904262993"},
    {"client": "Hawkins Siding and Exterior", "customer_id": "2198608170"},
    {"client": "Neon Monkey Services", "customer_id": "1219885876"},
    {"client": "Golden Plumbing", "customer_id": "4193142570"},
    {"client": "Zen Air Heating and Cooling", "customer_id": "3740502923"},
    {"client": "C&S Air", "customer_id": "5563867754"},
    {"client": "Gillespie's Heating and Cooling", "customer_id": "7410489772"},
    {"client": "Watt's Right Electric", "customer_id": "3651667805"},
    {"client": "Watt's Right - Broken Arrow (sister)", "customer_id": "9261944882"},
    {"client": "Proud Pops Plumbing, Air & Electric", "customer_id": "1051843378"},
    {"client": "Proud Pops - LSA San Antonio [1]", "customer_id": "7261668241"},
    {"client": "Proud Pops - LSA San Antonio [2]", "customer_id": "6621969129"},
    {"client": "My Favorite Service Company - LSA New Braunfels", "customer_id": "4127524472"},
    {"client": "My Favorite Service Company - LSA San Antonio", "customer_id": "4905286019"},
    {"client": "All Seasons AC (LSA)", "customer_id": "8655979348"},
]

VERIF_QUERY = """
    SELECT
        local_services_verification_artifact.id,
        local_services_verification_artifact.status,
        local_services_verification_artifact.artifact_type,
        local_services_verification_artifact.creation_date_time,
        local_services_verification_artifact.license_verification_artifact.license_type,
        local_services_verification_artifact.license_verification_artifact.rejection_reason,
        local_services_verification_artifact.license_verification_artifact.expiration_date_time,
        local_services_verification_artifact.insurance_verification_artifact.rejection_reason,
        local_services_verification_artifact.insurance_verification_artifact.expiration_date_time,
        local_services_verification_artifact.business_registration_check_verification_artifact.rejection_reason
    FROM local_services_verification_artifact
"""

CAMPAIGN_QUERY = """
    SELECT
        campaign.id, campaign.name, campaign.status,
        campaign.primary_status, campaign.primary_status_reasons,
        campaign.serving_status,
        metrics.impressions, metrics.clicks
    FROM campaign
    WHERE campaign.advertising_channel_type = 'LOCAL_SERVICES'
        AND campaign.status != 'REMOVED'
        AND segments.date DURING LAST_30_DAYS
"""

TODAY = date(2026, 8, 27)

def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.strptime(s.split(".")[0], "%Y-%m-%d %H:%M:%S").date()
    except Exception:
        return None

def main():
    client = init_client()
    service = client.get_service("GoogleAdsService")

    all_flags = []

    for acc in LSA_ACCOUNTS:
        name, cid = acc["client"], acc["customer_id"]
        flags = []

        # --- campaign status ---
        try:
            rows = list(service.search(customer_id=cid, query=CAMPAIGN_QUERY))
        except Exception as e:
            flags.append(f"CAMPAIGN QUERY ERROR: {str(e).splitlines()[0][:180]}")
            rows = []
        for row in rows:
            c = row.campaign
            reasons = [r.name for r in c.primary_status_reasons] if c.primary_status_reasons else []
            if c.status.name == "PAUSED":
                flags.append(f"Campaign PAUSED (reasons={reasons})")
            elif c.primary_status.name not in ("ELIGIBLE",):
                flags.append(f"Campaign primary_status={c.primary_status.name} reasons={reasons}")

        # --- verification artifacts ---
        try:
            vrows = list(service.search(customer_id=cid, query=VERIF_QUERY))
        except Exception as e:
            flags.append(f"VERIFICATION QUERY ERROR: {str(e).splitlines()[0][:180]}")
            vrows = []

        by_type = {}
        for row in vrows:
            a = row.local_services_verification_artifact
            t = a.artifact_type.name
            by_type.setdefault(t, []).append(a)

        for t in ("LICENSE", "INSURANCE", "BUSINESS_REGISTRATION_CHECK", "BACKGROUND_CHECK"):
            arts = by_type.get(t, [])
            if not arts:
                continue
            # latest PASSED artifact by expiration date (the credential currently on file)
            passed = [a for a in arts if a.status.name == "PASSED"]
            latest_created = max(arts, key=lambda a: a.creation_date_time)

            if t == "LICENSE":
                exp = lambda a: parse_dt(a.license_verification_artifact.expiration_date_time)
            elif t == "INSURANCE":
                exp = lambda a: parse_dt(a.insurance_verification_artifact.expiration_date_time)
            else:
                exp = lambda a: None

            if not passed:
                flags.append(f"{t}: NO PASSED artifact on record — latest attempt status={latest_created.status.name}")
                continue

            best_passed = max(passed, key=lambda a: exp(a) or date.min)
            best_exp = exp(best_passed)
            if best_exp and best_exp < TODAY:
                flags.append(f"{t}: current on-file credential EXPIRED on {best_exp} (no newer PASSED replacement)")
            elif best_exp and (best_exp - TODAY).days <= 30:
                flags.append(f"{t}: current on-file credential expires SOON, {best_exp} ({(best_exp - TODAY).days}d) — no newer PASSED renewal on file yet")
            # latest submission overall is not passed and is newer than the best passed one -> stuck renewal
            if latest_created.status.name not in ("PASSED",) and latest_created.creation_date_time > best_passed.creation_date_time:
                lt = ""
                if t == "LICENSE":
                    lt = latest_created.license_verification_artifact.rejection_reason.name
                elif t == "INSURANCE":
                    lt = latest_created.insurance_verification_artifact.rejection_reason.name
                flags.append(f"{t}: latest renewal attempt ({latest_created.creation_date_time[:10]}) status={latest_created.status.name} rejection={lt} — valid credential still on file until {best_exp}, but renewal is stuck")

        if flags:
            all_flags.append((name, cid, flags))

    print("="*100)
    print(f"LSA HEALTH CHECK — {len(LSA_ACCOUNTS)} contas, hoje={TODAY}")
    print("="*100)
    if not all_flags:
        print("Nenhum problema encontrado.")
    for name, cid, flags in all_flags:
        print(f"\n{name}  ({cid})")
        for f in flags:
            print(f"  - {f}")
    print("\n" + "="*100)

if __name__ == "__main__":
    main()
