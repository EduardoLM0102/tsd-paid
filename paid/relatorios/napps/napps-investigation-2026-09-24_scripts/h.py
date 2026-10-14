import os
import sys, json
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID = "9509605037"
OUT = "/private/tmp/claude-501/-Users-eduardolarangeirasmarinho/aaa1573d-0f6f-4b87-9ebb-d004682e3b36/scratchpad/napps/"
def f(x):
    try: return float(x)
    except: return 0.0
def isv(x):
    try: return float(x)
    except: return None
