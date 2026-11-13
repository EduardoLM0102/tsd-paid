---
name: tsd-meta-mcp-write-mechanics
description: "How Meta Ads MCP writes actually behave (draft mode, publish step, auto-mode allow rules, frequency-cap lock, no county geo) — learned 2026-10-09 on All Seasons"
metadata:
  node_type: memory
  type: reference
  originSessionId: 95bf6dc3-049a-423a-9094-ea958ab31f81
  modified: 2026-10-09T13:24:24.125Z
---

Meta Ads MCP write behavior, learned 2026-10-09 fixing All Seasons awareness ([[tsd-all-seasons-ac]]):

- **Writes land as Ads Manager DRAFTS** (`is_draft: true`), even `ads_update_entity` on a live object and a status PAUSED. Nothing is live until `ads_activate_entity` publishes it. Pass `object_ids` with exactly what to publish, so a broken draft on a sibling object isn't dragged in. PUBLISHING = handed off; re-read live state to confirm.
- **No draft discard tool.** A draft with errors sits in Ads Manager "Review and publish" until Edu discards it in the UI. Re-setting a field to its old value does NOT clear it from the draft.
- **Auto mode blocks Meta writes** unless `~/.claude/settings.json` allows them. Edu added allow rules on 10-09 for ads_update_entity, ads_create_campaign/ad_set/ad, ads_activate_entity, and they worked (unlike the 08-31 Bash create.py case).
- **Frequency controls lock once a campaign has started** (error 3858722). In CBO they're campaign-level, so a new ad set in the same campaign can't fix it. Changing/removing a cap = new campaign.
- **No location search tool**, so county keys can't be looked up. Workaround used: ZIP list from GeoNames US.zip filtered by county (admin_name2), sent as `zips: [{key:"US:xxxxx"}]`.
- Reusing an ad's `creative_id` in a new ad keeps the same post (`effective_object_story_id`), so social proof carries. Check via `ads_get_creatives`.
- Page/post fields aren't in `ads_get_ad_entities`; use `ads_get_creatives` + `ads_get_ad_account_pages`.

- **Image uploads (11-12, Morrow):** `ads_creative_upload_media` with a Drive `uc?export=download` URL is refused ("couldn't be downloaded"). Working path: `curl -L` the Drive file locally → `ads_create_upload_url` (file name, mime, exact byte size) → `curl -X POST` with every returned header + `--data-binary` → `ads_finalize_upload` returns the image hash. ~10 files per batch is fine; the upload URL expires in ~30 min. Every draft ad then reports the account-level `No Payment Method` (1359188) error until the client adds a card; it is the only publish blocker and nothing else needs fixing.

- **Payment methods on client ad accounts (11-12, Morrow):** Edu cannot add a card to a client's ad account from Brazil, even with the card in hand: Meta rejects a payment method when the IP's country doesn't match the account's currency (USD accounts). The client (or someone in the US on their side) adds it via Ads Manager → Billing and payment center, link pattern `https://adsmanager.facebook.com/adsmanager/billing_hub/accounts/details/?business_id=<BM>&asset_id=<acct>&payment_account_id=<acct>`. Ask through the AM, don't promise to do it ourselves.

**How to apply:** any Meta change for TSD clients. Plan for create → verify draft errors → publish → re-read live. See [[tsd-meta-ads-methodology]], [[tsd-weekly-meta-snapshot]].
