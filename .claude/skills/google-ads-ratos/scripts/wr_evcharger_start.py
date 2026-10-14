import sys, json
sys.path.insert(0, ".")
from lib import run_query
CID = "3651667805"
q = "SELECT campaign.name, campaign.start_date, campaign.status FROM campaign WHERE campaign.id = 24094882200"
for r in run_query(CID, q):
    print(json.dumps(r))
