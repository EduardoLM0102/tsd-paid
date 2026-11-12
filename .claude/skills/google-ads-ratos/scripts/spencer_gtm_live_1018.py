"""Spencer Air GTM-KT5RPTP live version dump (direct path, no account scan). Read-only."""
import sys, re
sys.path.insert(0, ".")
from gtm_setup import gtm_service
svc = gtm_service()
path = "accounts/6000941581/containers/31091984"
live = svc.accounts().containers().versions().live(parent=path).execute()
print(f"LIVE version {live.get('containerVersionId')} name={live.get('name')!r}")
print("VARIABLES:")
for v in live.get("variable", []):
    print(f" - {v.get('name')} ({v.get('type')}) = {[(p.get('key'), p.get('value')) for p in v.get('parameter', [])]}")
print("TAGS:")
for t in live.get("tag", []):
    ps = [(p.get('key'), p.get('value')) for p in t.get('parameter', []) if p.get('value') and p.get('key') != 'html']
    html = next((p.get('value') for p in t.get('parameter', []) if p.get('key') == 'html'), '')
    ids = sorted(set(re.findall(r"(?:AW-\d+|G-[A-Z0-9]{6,12}|\b\d{15,16}\b|calltrk\.com/companies/\d+/\w+|hooks?\.[\w./-]+)", html or '')))
    print(f" - [{t.get('tagId')}] {t.get('name')} ({t.get('type')}) paused={t.get('paused', False)} fire={t.get('firingTriggerId')} {ps} html_ids={ids}")
print("TRIGGERS:")
for tr in live.get("trigger", []):
    print(f" - [{tr.get('triggerId')}] {tr.get('name')} ({tr.get('type')}) {tr.get('customEventFilter') or tr.get('filter') or ''}")
