# READ-ONLY: 7d spend + enabled campaign count per channel type, per TSD Google account
import os
import sys, json, collections
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CIDS = sys.argv[1].split(",")
out = {}
for cid in CIDS:
    rec = {"spend7": collections.defaultdict(float), "enabled": collections.defaultdict(int)}
    try:
        for r in run_query(cid, "SELECT campaign.advertising_channel_type, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_7_DAYS"):
            t = r["campaign"].get("advertising_channel_type") or r["campaign"].get("advertisingChannelType")
            rec["spend7"][str(t)] += int(r["metrics"].get("cost_micros") or 0) / 1e6
        for r in run_query(cid, "SELECT campaign.advertising_channel_type, campaign.status FROM campaign WHERE campaign.status = 'ENABLED'"):
            t = r["campaign"].get("advertising_channel_type") or r["campaign"].get("advertisingChannelType")
            rec["enabled"][str(t)] += 1
    except SystemExit as ex:
        rec["error"] = f"SystemExit {ex}"
    except Exception as ex:
        rec["error"] = str(ex)[:200]
    out[cid] = rec
    print(cid, dict(rec["spend7"]), dict(rec["enabled"]), rec.get("error", ""), flush=True)
json.dump(out, open("/private/tmp/claude-501/-Users-eduardolarangeirasmarinho/715c702a-049e-427e-a580-f1c760b49680/scratchpad/ops/google_channels.json", "w"), indent=1)
