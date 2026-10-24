# Napps (Knapp's) — LSA Call Wins Log (Oct 1–15, 2026)

Scope: Google Local Services Ads leads only. These calls don't go through CallRail. Lead list, status, and recordings were pulled from the Google Ads LSA API (LSA account 9239407401, `local_services_lead` + `local_services_lead_conversation`) and transcribed locally. One line per lead; leads with several calls are merged into one line.

**Caveat:** names and spelled details come from an auto-generated transcript on phone-quality audio. "Google status" is what the business marked in the LSA dashboard, and the outcome tag is what the calls show.

**Patterns to flag:**
- **Existing customers call through LSA.** Property managers, a parks department, and repeat customers use this number for ongoing work. Some of those leads are charged even though they aren't new business.
- **Four message leads on 10-14 got only the after-hours auto-reply.** They are a clogged septic line (sent twice), gas line leaks with the meter pulled, and a broken hose with a large water bill. Nothing after the auto-reply is visible.
- **Dispute candidate:** the septic message came in twice (04:13 and 10:26) and was **charged both times**.
- **The LSA account isn't in the team's LSA report script** (`lsa_report.py` lists no Napps account), so Napps LSA has been invisible in the weekly LSA pull.

**Outcome legend:** ✅ Booked · ⏳ Open/follow-up needed · ❌ No contact / not a lead · 🔁 Duplicate of a lead already counted

---

## 2026-10-01

- **11:09 · 241s · LSA · (commercial kitchen)** — Existing commercial customer complaining that fryer hoses were installed backwards on an earlier job. Lead plumber sent the same afternoon to fix it. Google status: Booked (not charged). ❌ Not a new lead (rework on an earlier job).
- **11:40 · 2 calls (353s, 307s) · LSA** — Customer (Erin) setting up an AC maintenance plan after a recent visit. Booked Wednesday, first slot 8:30–9am. Also asked for help with a water-heater warranty claim through another installer. Google status: Booked (charged). ✅ Booked.

## 2026-10-02

- **10:06 · 3 calls (200s, 528s, 52s) · LSA · Gilmer** — Apartment property manager (existing account) opening no-cool tickets for five units (183, 184, 225, 072, 215). Scheduled for that afternoon and the next day. Google status: Booked (not charged). ✅ Booked (multiple service tickets).
- **11:39 · 597s · LSA** — Existing customer asking for a manager about an ongoing job that had to be redone. The office will move forward once the customer sends specs for a table. Google status: Booked (not charged). ⏳ Open — existing-job issue.
- **17:07 · 33s · LSA** — Reached the after-hours answering service; caller said they'd call back Monday. Google status: Declined. ❌ No contact.

## 2026-10-05

- **13:52 · 226s · LSA · Winona** — New homeowner (moved from Colorado) with a clogged kitchen sink. Wants all the plumbing checked. Booked for the next morning. Google status: Booked (charged). ✅ Booked.
- **14:09 · 123s · LSA** — Parks and Recreation department checking on parts lead time for an existing repair. Google status: Booked (not charged). ❌ Not a new lead (status check).

## 2026-10-06

- **08:30 · 160s · LSA · Longview** — Rehab hospital, patient shower not getting hot water. Plumber will head over as soon as one is free. Google status: Booked (charged). ✅ Booked (same-day dispatch).
- **12:40 · 187s · LSA · Tatum** — Business with a drink fridge in the dining area that isn't cooling. Scheduled for the next day. Google status: Booked (charged). ✅ Booked.
- **13:38 · 88s · LSA** — Job seeker asking about HVAC openings (not certified yet). Google status: Declined (not charged). ❌ Not a lead (job seeker).

## 2026-10-08

- **19:42 · 126s · LSA · Longview** — Apartment complex maintenance asking for an on-call plumber after hours, because another company was tied up. Answering service reached the on-call plumber, who agreed to call right back. Google status: Booked (not charged). ✅ Booked (after-hours dispatch).

## 2026-10-09

- **10:13 · 147s · LSA · Gladewater** — Assisted-living building with sewage backing up into sinks in several rooms. Someone scheduled for that afternoon. Google status: Booked (not charged). ✅ Booked.

## 2026-10-10

- **17:15 · 153s · LSA** — Weekend call: wiring on a water heater, found through Google as "nearest water heater replacement." Answering service tried to reach the on-call tech; the outcome isn't in the recording. Google status: Booked (charged). ⏳ Open — confirm.

## 2026-10-14

- **04:13 · message · LSA · Gilmer** — Septic line clogged; laundry backs up into the tub. Only the after-hours auto-reply was sent. Google status: Active (charged). ⏳ Open — reply owed.
- **10:26 · message · LSA · Gilmer** — Same septic message sent again. Google status: New (charged). 🔁 Duplicate of 04:13. **Dispute the second charge.**
- **12:22 · message · LSA** — Four gas-line leaks; the gas company pulled the meter. Google status: New (charged). ⏳ Open — **urgent**, reply owed.
- **17:17 · message · LSA** — Broken water hose pipe, water bill over $1,000, customer on SSI. Only the auto-reply was sent. Google status: Active (charged). ⏳ Open — reply owed.

## 2026-10-15

- **08:17 · 269s · LSA** — Existing customer; an appliance installer knocked off the ice-maker water connection when installing a new fridge. Ticket scheduled. Google status: Active (not charged). ✅ Booked.


## 2026-10-16

- **07:46 · 90s · LSA · Longview area** — Not a customer: a driver reporting one of Napps' vans (plate ending 9441) tailgating every car on Highway 259 from Kilgore to Longview. No callback wanted. Google status: Active (not charged). ❌ Not a lead. *Pass to the owner as a driver-safety complaint.*

---

## Running tally (Oct 1–15, 18 leads)

| Outcome | Count | Detail |
|---|---|---|
| ✅ Booked | 8 | Maintenance plan, five apartment units, Winona sink, rehab hospital shower, Tatum fridge, after-hours apartment plumber, assisted-living sewage, ice-maker line |
| ⏳ Open | 5 | Existing-job issue, weekend water heater, septic message, gas leaks message, hose leak message |
| 🔁 Duplicate | 1 | Septic message sent twice (charged twice) |
| ❌ Not a lead | 4 | Rework complaint, parts status check, job seeker, after-hours no-contact |

*Google's dashboard shows 11 booked. Several of those are existing-customer calls or rework that this log doesn't count as new wins.*

*Oct 16–17 calls added 2026-10-17 (day sections above); the tally table covers Oct 1–15.*
