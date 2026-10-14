from h import *
q = """
SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type, shared_set.name
FROM shared_criterion
WHERE shared_set.id = 12141170676
"""
rows=list(run_query(CID,q))
print(len(rows))
t=sorted(((r["shared_criterion"]["keyword"]["text"], r["shared_criterion"]["keyword"]["match_type"]) for r in rows))
print("; ".join(f"{a} [{b[0]}]" for a,b in t))
