import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
AT = "Agency Titan 7-day task (client log)"
def ch(state, spend=None, accounts=None, last=None, src=None, note=None):
    d = {"state": state, "spend7": spend, "accounts": accounts, "lastChecked": last, "checkSource": src, "note": note}
    return {k: v for k, v in d.items() if v is not None or k in ("spend7", "lastChecked")}

clients = {
 "proud-pops": {"name": "Proud Pops", "market": "San Antonio, TX", "status": "active", "channels": {
   "google": ch("live", 12406, "1051843378 (PPC) · 9815330464 (My Favorite Service)", "2026-10-08", "google-ads-log 10-08 (search-term sweeps + 30-day report)", "Active checklist: clients/proud-pops/internal-checklist-2026-10.md"),
   "lsa": ch("live", 151, "7261668241 · 6621969129 · MFSC 4127524472 / 4905286019", "2026-10-08", "google-ads-log 10-08 (LSA lead-handling review)", "Only LSA San Antonio [1] spent in the last 7 days. Legacy roofing LSA paused 10-08."),
   "youtube": ch("live", 1417, "Video campaigns inside 1051843378", "2026-10-07", "30-day report (YouTube reported as awareness)")}},
 "watts-right": {"name": "Watt's Right Electric", "market": "Tulsa, OK", "status": "active", "channels": {
   "google": ch("live", 1716, "3651667805", "2026-10-05", AT),
   "lsa": ch("live", 3097, "Inside 3651667805", "2026-10-05", AT),
   "meta": ch("live", 1765, "588638883283311", "2026-10-05", "meta-ads-log 10-05", "Live TOF/MOF/BOF funnel with video-viewer retargeting.")}},
 "hawkins-siding": {"name": "Hawkins Siding & Exterior", "market": "Dallas metro, TX", "status": "active", "channels": {
   "google": ch("live", 688, "2198608170", "2026-10-05", AT, "Siding/exterior only. No window or door ads."),
   "lsa": ch("live", 432, "Inside 2198608170", "2026-10-05", AT),
   "meta": ch("missing", 0, "10086442468052740", None, None, "$0 in the last 7 days. Meta has been dark since 08-20.")}},
 "neon-monkey": {"name": "Neon Monkey Services", "market": "West Fort Worth, TX", "status": "active", "channels": {
   "google": ch("live", 1941, "7953905280", "2026-09-28", "google-ads-log 09-28 (lawn care ticket)", "No weekly AT task for this client."),
   "lsa": ch("live", 65, "1219885876", "2026-08-10", "google-ads-log 08-10"),
   "meta": ch("confirm", 0, "705877631084699", None, None, "Ad account exists with $0 in the last 7 days. Is Meta part of the scope?")}},
 "all-seasons-ac": {"name": "All Seasons AC", "status": "active", "channels": {
   "google": ch("live", 1367, "4467722415", "2026-10-08", "google-ads-log 10-08 (mid-week check)", "Heating ad groups dark (redirected URL). PMax spend is Display taps."),
   "lsa": ch("confirm", None, None, "2026-10-08", "google-ads-log 10-08 (operation rating)", "LSA has a weekly AT task, but there's no LSA campaign in 4467722415. Add the LSA account ID so its spend can be tracked."),
   "meta": ch("live", 135, "2405306059725517", "2026-10-05", "meta-ads-log 10-05", "Awareness setup needs fixing (see follow-up).")}},
 "kings-window": {"name": "King's Window Services", "status": "active", "channels": {
   "google": ch("live", 380, "6769493219", "2026-10-05", AT, "PMax paused 08-31 (second strike)."),
   "lsa": ch("live", 293, "Inside 6769493219", "2026-10-05", AT),
   "meta": ch("live", 381, "483679897962388", None, None, "No Meta check in the workspace logs.")}},
 "zen-air": {"name": "Zen Air Heating & Cooling", "status": "active", "channels": {
   "google": ch("live", 1075, "4360840956", "2026-10-08", "google-ads-log 10-08", "Nonbranded PAUSED 10-08 after $1,050/week with 0 real leads. Only branded is live."),
   "lsa": ch("missing", 0, "3740502923", "2026-10-05", AT, "$0 in the last 7 days ($107 in the last 30)."),
   "meta": ch("live", 1479, "381256660973192", None, None, "No Meta check in the workspace logs.")}},
 "napps": {"name": "Napps Cooling, Heating & Plumbing", "status": "active", "channels": {
   "google": ch("live", 939, "9509605037", "2026-10-05", AT, "Client wants HVAC and plumbing 50/50 (live since 09-15)."),
   "lsa": ch("live", 275, "9239407401", "2026-10-05", AT),
   "meta": ch("live", 35, "438790276573563", None, None, "No Meta check in the workspace logs.")}},
 "spencer-air": {"name": "Spencer Air", "status": "active", "channels": {
   "google": ch("live", 337, "2524618054", "2026-10-06", AT),
   "lsa": ch("live", 507, "Inside 2524618054", "2026-10-06", AT),
   "meta": ch("live", 269, "1845825982372184", "2026-10-06", "meta-ads-log 10-06 (AT task)")}},
 "cs-air": {"name": "C&S Air", "status": "active", "channels": {
   "google": ch("live", 1071, "5563867754", "2026-10-06", AT, "Smart campaign $553 + Search $517 in the last 7 days."),
   "lsa": ch("live", 110, "Inside 5563867754", "2026-10-06", AT),
   "meta": ch("missing", None, None, "2026-10-06", "meta-ads-log 10-06 (AT task)", "There's a weekly Meta task in Agency Titan, but no ad account is shared with TSD. Build Meta or switch off the task.")}},
 "mission-accomplished": {"name": "Mission Accomplished", "market": "Lake Havasu, AZ", "status": "active", "channels": {
   "google": ch("missing", 0, "8634274092", "2026-10-05", AT, "No enabled campaigns and $0 in the last 30 days. Confirm this is on purpose."),
   "lsa": ch("live", 307, "4904262993", "2026-10-05", AT),
   "meta": ch("live", 207, "79203382", "2026-09-29", "meta-ads-log 09-29 (FB report)", "Awareness only since 09-03.")}},
 "lilypad-septic": {"name": "Lilypad Septic", "market": "Salina & Hutchinson, KS", "status": "active", "channels": {
   "google": ch("live", 199, "3797438623", "2026-10-05", AT, "Real conversion test still owed."),
   "meta": ch("confirm", 0, "123589321338300 (client's)", None, None, "Client's ad account exists, no delivery. Is Meta part of the scope?")}},
 "cool-hand-electric": {"name": "Cool Hand Electric", "market": "Mansfield, TX", "status": "active", "channels": {
   "google": ch("live", 917, "9865206319", "2026-10-08", "google-ads-log 10-08", "LSA is excluded from TSD scope."),
   "youtube": ch("live", 178, "Demand Gen inside 9865206319", None, None, "Demand Gen taps inflate conversions. Report Search only."),
   "meta": ch("live", 139, "1517373248873821", None, None, "No Meta check in the workspace logs.")}},
 "integrate-comfort": {"name": "Integrate Comfort Systems", "market": "New Jersey", "status": "active", "channels": {
   "google": ch("live", 543, "4571881760", "2026-10-08", "google-ads-log 10-08", "Checkpoint on the 10-08 changes around 10-28."),
   "lsa": ch("missing", 0, "Belleville 2895702982 · Carlstadt 2175964343 · Englewood Cliffs 8323145223", "2026-09-11", "google-ads-log 09-11", "All three LSA accounts spent $0 in the last 7 days."),
   "youtube": ch("live", 144, "2895702982 (Mitsubishi YouTube)", "2026-09-11", "google-ads-log 09-11"),
   "meta": ch("noaccess", None, "2070047533283360 (ICS)", None, None, "The Meta connector can't read this account (Ads MCP not enabled for it).")}},
 "nicks-heating": {"name": "Nick's Heating & Air", "market": "Hammond, LA", "status": "active", "channels": {
   "google": ch("live", 702, "1854100356", "2026-10-08", "google-ads-log 10-08 (first full check)"),
   "lsa": ch("live", 649, "Inside 1854100356", "2026-10-08", "google-ads-log 10-08"),
   "meta": ch("live", 137, "710350517676765", None, None, "No Meta check in the workspace logs.")}},
 "live-wire": {"name": "Live Wire Electric", "market": "Lynnwood, WA", "status": "confirm",
   "statusNote": "Trade Vulcan (brandon@tradevulcan.com) cloned our Search campaigns on 09-16 and paused ours on 10-05/06. AT tasks stopped after 09-21. Confirm Live Wire is still a client.",
   "channels": {
   "google": ch("live", 1015, "1056617442", "2026-09-21", "Last AT 7-day task", "Spend is on Trade Vulcan's copies."),
   "lsa": ch("live", 36, "Inside 1056617442", "2026-09-21", "Last AT 7-day task")}},
 "strickland": {"name": "Strickland Heating & Air", "status": "confirm",
   "statusNote": "Only On Purpose Media makes changes in this account and every TSD_ campaign is paused. Not in AT or the audit sheet. Confirm whether it's ours.",
   "channels": {"google": ch("live", 916, "9049508615", None, None, "Run by On Purpose Media.")}},
 "eaglepoint": {"name": "Eaglepoint Roofing & Exterior", "status": "confirm",
   "statusNote": "Account is in contas.yaml but nothing is built and it has $0 spend. Confirm whether this is a client.",
   "channels": {"google": ch("missing", 0, "9005488539", "2026-08-31", "google-ads-log 08-31", "Nothing built.")}},
 "carey-walsh": {"name": "Carey & Walsh", "market": "Westchester County, NY", "status": "onboarding",
   "statusNote": "Media plan Nov 2026 to Jan 2027 is ready (clients/carey-walsh/). No ad accounts exist yet.",
   "channels": {
   "google": ch("missing", None, None, None, None, "No Google Ads account yet. Create it under MCC 4155514468."),
   "lsa": ch("missing", None, None, None, None, "LSA verification not started (takes 2 to 5 weeks)."),
   "meta": ch("missing", None, None, None, None, "No ad account, pixel or Page access yet.")}},
 "on-the-way": {"name": "On The Way", "market": "Santa Fe, TX", "status": "offboarding",
   "statusNote": "Contract ends 11/2/2026.",
   "channels": {
   "google": ch("noaccess", None, "3454686129", "2026-10-05", AT, "The client revoked TSD's Google Ads access on 10-05."),
   "meta": ch("live", 169, "1428068256022895", "2026-10-01", "meta-ads-log 10-01", "Spent $169 in the last 7 days, but our notes say the awareness ad stopped 09-11. Check what's running.")}},
 "on-time": {"name": "On Time Service Pros", "market": "Rosemount, MN", "status": "offboarding",
   "statusNote": "Ends 10/16/2026. Meta only.",
   "channels": {"meta": ch("noaccess", None, "1846637992293356", "2026-09-29", "meta-ads-log 09-29", "The Meta connector can no longer open this account.")}},
 "golden-plumbing": {"name": "Golden Plumbing", "status": "frozen",
   "statusNote": "On freeze since 10-08. PPC paused since 07-17.",
   "channels": {
   "google": ch("paused", 0, "4193142570", None, None, "PPC paused since 07-17 at the client's request."),
   "lsa": ch("paused", 0, "Inside 4193142570", None, None, "$0 in the last 7 days ($2,193 in the last 30).")}},
 "gc-home-service": {"name": "GC Home Service", "status": "offboarded", "statusNote": "Offboarded 10-08.",
   "channels": {"google": ch("paused", 0, "2375064049 · LSA 2974002658"), "meta": ch("paused", None, "1434273655098937")}},
 "gillespies": {"name": "Gillespie's Heating & Cooling", "status": "offboarded", "statusNote": "Offboarded 10-08. Campaigns removed.",
   "channels": {"google": ch("paused", 101, "7410489772", None, None, "$101 in the last 7 days, before the removal."), "meta": ch("noaccess", None, "2014320269203822", None, None, "Access lost by 10-07.")}},
 "all-heart": {"name": "All Heart Heating & Cooling", "status": "offboarded",
   "statusNote": "Offboarded. As of 09-29, 4 LSA accounts were still spending under the MCC ($17,582 in 4 weeks). Confirm who pays or unlink them.",
   "channels": {"google": ch("paused", None, "9205826499"), "lsa": ch("paused", None, "9976029542 · 8199337860 · 5064174352 · 7662998005"), "meta": ch("paused", None, "1664197513868366", None, None, "All campaigns paused 08-20.")}},
}

F = []
def fu(client, title, due=None, note=None):
    F.append({"client": client, "title": title, "due": due, "note": note, "status": "open", "createdAt": "2026-10-08", "createdBy": "Claude"})
fu("cs-air", "Revisit the 10-05 recommendations: fix tracking, swap Smart for PMax, trim Nonbranded", "2026-10-06", "clients/cs-air/google-ads-log.md, entry 10-05 (cont.)")
fu("all-seasons-ac", "Fix the Meta awareness setup: Reach to Ad Recall Lift, frequency cap, geo", "2026-10-06", "Meta account 2405306059725517")
fu(None, "Send JB the 'CPC too low' answer (promised EOD 10-08)", "2026-10-08")
fu("watts-right", "Recheck after the 09-29 overhaul (EV paused, PMax job/brand fix, $235/day)", "2026-10-09", "Checklist in clients/watts-right/google-ads-log.md, entry 09-29")
fu("nicks-heating", "Work the 10-08 checklist: pause the AC phrase keyword and Branded broad keyword, PMax geo to Presence, AM ticket", "2026-10-09", "tarefas.md, Nick's section")
fu("cool-hand-electric", "Owner meeting. The 09-24 geo and negatives fixes were still not done at the 10-05 check", "2026-10-09")
fu("on-the-way", "Find out what's spending on Meta ($169 in the last 7 days after the 09-11 stop)", "2026-10-09", "Meta 1428068256022895")
fu("mission-accomplished", "PPC has no enabled campaigns and $0 in 30 days. Confirm it's on purpose", "2026-10-09", "Google 8634274092")
fu("hawkins-siding", "Recheck the 10-05 shift: PMax $13 to $18/day, Nonbranded $80 to $75/day", "2026-10-12")
fu("proud-pops", "JB check-in on Proud Pops. Re-read the active checklist first", "2026-10-12", "clients/proud-pops/internal-checklist-2026-10.md")
fu("all-seasons-ac", "Weekly AT task created 10-05", "2026-10-12")
fu("integrate-comfort", "Checkpoint on the 10-08 changes: PMax $50, Nonbranded $15 heating-only, negatives fixed", "2026-10-28")
fu("live-wire", "Confirm Live Wire is still a client")
fu("strickland", "Confirm whether Strickland is ours")
fu("zen-air", "Rebuild Nonbranded as service phrase/exact keywords and file the AM ticket")
fu("lilypad-septic", "Run the real conversion test")
fu("neon-monkey", "Geo re-targeting ticket is blocked on the location list")
fu("cs-air", "Decide: build Meta for C&S or switch off the weekly Meta task")
fu("proud-pops", "My Favorite Service Co (9815330464): pause it or manage it")
fu("carey-walsh", "Send the media plan to the AM and get written approval of the monthly amount")
fu(None, "Ask AT for 7-day tasks: Proud Pops, Neon Monkey, Cool Hand, ICS, Nick's")

followups = {f"fu-{i+1:03d}": f for i, f in enumerate(F)}
sync = {"channelsAsOf": "2026-10-08", "window": "Oct 1 to 7", "source": "Google Ads API (all accounts under MCC 4155514468) and the Meta connector."}
for i, (k, v) in enumerate(clients.items()):
    v["order"] = i
json.dump({"clients": clients, "followups": followups, "sync": sync}, open(os.path.join(OUT, "seed.json"), "w"), indent=1)
# batch files for ArtifactData (<=50 writes each)
writes = [{"op": "set", "collection": "clients", "doc_id": k, "data": v} for k, v in clients.items()]
writes += [{"op": "set", "collection": "followups", "doc_id": k, "data": v} for k, v in followups.items()]
writes += [{"op": "set", "collection": "meta", "doc_id": "sync", "data": sync}]
json.dump(writes, open(os.path.join(OUT, "writes.json"), "w"))
print(len(clients), "clients,", len(followups), "follow-ups,", len(writes), "writes")
