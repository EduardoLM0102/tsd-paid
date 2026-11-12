---
name: tsd-gmail-access
description: "TSD Gmail (eduardo@topservdigital.com) has no connector; read it through Claude in Chrome on the browser Edu named 'TSD'"
metadata:
  node_type: memory
  type: reference
---

Edu's TSD mailbox is eduardo@topservdigital.com. There is no Gmail connector in Claude Code (checked 2026-11-09). The Google Drive connector does reach the TSD account (2026-11-09: it returned files owned by eduardo@topservdigital.com and the TSD shared drive), but it only reads Drive, not mail. Vista Social notifications do not land in this mailbox, so it cannot answer "do we post for client X".

The route that works is Claude in Chrome. Edu has two Chrome browsers connected; the one signed in to the TSD Google account was named "TSD" on 2026-11-09. If the browser list shows it, select that one; if it only shows "Browser 1 / Browser 2", ask Edu (AskUserQuestion), do not guess.

Recipe: open `https://mail.google.com/mail/u/0/`, type the query in the search box (a `#search/...` URL alone loads an empty list), open the thread, read it with `get_page_text`. Results default to "most relevant", so add `newer_than:10d` to confirm which message is really the latest.

Angela Moyer (angela@topservdigital.com) is TSD's Client Success Lead. She often forwards client emails with no note of her own, so the ask is inside the forwarded part.

**2026-11-11 sending a reply via Claude in Chrome (worked, with one trap):** the TSD Gmail (eduardo@topservdigital.com) is Browser 1 in Chrome; the claude.ai Gmail connector is Edu's personal account, so replies from the TSD address go through the browser. Open the thread, click "Reply all" **by coordinates** (clicking the `find` ref for "Reply all" hit a label and did NOT open the compose box), screenshot to confirm the compose body has focus, then type. If the compose box is not open, every typed character becomes a Gmail keyboard shortcut (the "?" in the text opened the shortcuts overlay; c/r/a/y/m/s/e would compose/reply/archive/mute/star). Check Drafts afterwards. Gmail appends Edu's own signature; no Claude watermark is added when typing in the browser (the Slack connector does add "Sent using Claude").
