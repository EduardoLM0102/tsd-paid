---
name: tsd-meta-media-upload-drive-route
description: Edu rule 2026-11-18 — every Meta ad media upload (image or video, Drive or local file) goes through the TSD shared Drive + URL upload, done end to end by Claude without asking Edu to upload anything
metadata:
  type: feedback
---

**Rule (Edu, 2026-11-18):** to save Edu work, ALWAYS use the Drive route to get media into a Meta ad account, and do it end to end. That includes files that are on Edu's Mac (Downloads, scratchpad, edited cuts): upload them to Drive first, then into the ad account. Never hand Edu an "upload this in Ads Manager" step if the Drive route can do it. Automate as much as possible.

**Why:** the Meta MCP's `ads_create_upload_url` is not rolled out on every account, and asking Edu to upload by hand stalled the Zen Air re-cut on 11-18. The Drive route worked on Concrete (11-17) and Zen Air (11-18) with no manual step.

**How to apply:**
1. **Already in Drive** (client folder on the TSD Company shared drive): skip to step 4.
2. **Local file:** check size. Drive `create_file` caps at 10 MB *including base64*, so the file must be under ~7 MB. Videos over that: re-encode with the bundled ffmpeg (`imageio-ffmpeg` in a scratchpad venv; H.264 ~1.6 Mbps + AAC 128k gives ~6 MB for a 28 s 1080p cut). Keep the full-quality master locally/in the log.
3. Upload with `create_file` (`base64Content` = `sha256:<hex>:<abs path>`, `disableConversionToGoogleType: true`) into the **client's folder on the TSD Company shared drive** (find it with `search_files`, e.g. the folder holding their other videos). Name it clearly (client, ad name, version, aspect ratio).
4. `get_file_permissions` → shared-drive files inherit `anyoneWithLink` reader, so no share is needed. **Never call `share_file` to make it public** (the permission check refuses it). If a file lacks link access, ask Edu instead of sharing it.
5. `ads_creative_upload_media` with `upload_source=URL`, `media_type` IMAGE/VIDEO, URL `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t` (the `uc?export=download` form is refused). Poll `ads_get_ad_videos` until `ready` (usually under a minute).
6. Build creative/ad as usual; log the Drive file IDs + Meta video IDs/hashes in the client's meta-ads-log.md.

Fallback only if the Drive route fails: the `curl` + `ads_create_upload_url` path in [[tsd-meta-mcp-write-mechanics]].
