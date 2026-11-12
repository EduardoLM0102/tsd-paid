# C&S Air — LSA Call Wins Log (Oct 1–15, 2026)

Scope: Google Local Services Ads calls only. These calls don't go through CallRail. Lead list, status, and recordings were pulled from the Google Ads LSA API (account 5563867754, `local_services_lead` + `local_services_lead_conversation`) and transcribed locally.

**Caveat:** names and spelled details come from an auto-generated transcript on phone-quality audio. "Google status" is what the business marked in the LSA dashboard, and the outcome tag is what the call itself shows. They can differ.

**Outcome legend:** ✅ Booked · ⏳ Open/follow-up needed · ❌ No contact / not a lead

---

## 2026-10-01

- **10:47 · 209s · LSA · Mansfield** — Existing customer (Amanda). Upstairs unit hums loudly outside but the fan won't spin, so she shut it off. No home warranty anymore. Booked for Monday (Oct 5), 10am–1pm, with an offer to move it up if it becomes urgent. Google status: Booked (not charged). ✅ Booked.

## 2026-10-05

- **16:01 · 93s · LSA · Joshua** — New customer. Indoor unit runs, outdoor unit is dead, house at 79°F with the thermostat set to 73. Told about the $89 trip charge; she said she'd make a few calls and call back. Google status: Booked (charged). ⏳ Open — the call ends without a booking. Check whether she called back and booked.

## 2026-10-14

- **12:26 · 268s · LSA · (existing customer)** — Tina, existing customer. AC temperature climbing after an overnight power outage. Her six-month maintenance plan has lapsed, and she's leaving town this weekend, so she wants someone out before then. The call ends without a clear booking. Google status: Active (not charged). ⏳ Open — confirm a visit was scheduled before the weekend.

---

## Running tally (Oct 1–15, 3 calls)

| Outcome | Count | Detail |
|---|---|---|
| ✅ Booked | 1 | Mansfield repair, Mon Oct 5, 10am–1pm |
| ⏳ Open | 2 | Joshua new customer (price-shopping, Google says booked), Tina (lapsed maintenance plan) |
| ❌ Not a lead | 0 | |

*Google's dashboard shows 2 booked. Only 1 booking is audible on the calls. The Joshua lead may have been booked on a later call.*

---

# Added 2026-11-09: Sep 15–30 and Oct 19–Nov 5

Pulled with `pull_lsa.py` (account 5563867754, 2026-09-15 → 2026-11-09): 23 leads, 21 with a recording, transcribed locally with faster-whisper (small.en). Names and details can carry transcription errors. Oct 1–15 is above; the 10-19 call is in `call-wins-log.md`. Why this pull: C&S marked 25 of 49 LSA leads DECLINED since Aug 1 and 11 of those were charged, so the question was whether real jobs are being turned away.

**Outcome legend:** ✅ Booked · ⏳ Open/follow-up needed · ❌ Not a lead

## 2026-09-15
- **08:17 · 0s** — No connection, no recording. Google status: Declined (not charged). ❌ No contact.
- **17:45 · 319s · Alvarado** — Longtime customer, system replaced this summer, house at 83°F. Taken through the after-hours agent, details collected. Google status: Booked (not charged). ✅ Booked, existing customer.

## 2026-09-16
- **16:13 · 73s** — Existing customer (Linda), house warming up, put in the 4–7pm window. Google status: Booked (not charged). ✅ Booked, existing customer.

## 2026-09-17
- **12:46 · 79s** — Gerardo, following up on a proposal for a commercial office AC job: he sent the plans the week before and never got a price. Office says it went to the owner, "we've been super busy", owner will call. Google status: **Declined (charged)**. ⏳ Open — a commercial prospect waiting on a quote, not a decline.

## 2026-09-21
- **15:46 · 293s** — Job seeker (recent HVAC school graduate). Told there are no entry-level openings. Google status: Declined (not charged). ❌ Not a lead.

## 2026-09-25
- **15:23 · 71s** — Job seeker (2 years as an install apprentice). Invited to come by and apply. Google status: Declined (not charged). ❌ Not a lead.

## 2026-09-29
- **08:42 · 287s** — A C&S employee calling the office about a minor road incident with the company trailer. Google status: **Declined (charged)**. ❌ Not a lead — an internal call that Google charged for. Dispute candidate.
- **15:36 · 270s · Mansfield** — Existing customer (Fatima), drain line running a stream of water after a recent service. Google status: Booked (not charged). ✅ Booked, existing customer.

## 2026-10-20
- **08:59 · 347s, then 10-21 07:44 · 42s · Colleyville** — Existing customer (Justin), system blowing hard with no cold air. Phil walked him through the likely cause on the phone; he fixed it himself, called back to cancel the visit and promised a five-star review. Google status: Declined (not charged). ❌ No job (solved by phone).

## 2026-10-21
- **18:57 · message · install_ac** — Message lead, no recording. Google status: Booked (charged). Not verifiable from audio.

## 2026-10-22
- **12:05 · 258s, then 10-26 12:23 · 420s · Fort Worth** — New customer (Bailey), referred by a friend, AC repair. Visit and quote done; on the second call she has a cheaper second opinion and follow-up questions, part on order. Google status: **Active (charged)**, never marked. ⏳ Open — a real new customer mid-decision.

## 2026-10-23
- **14:24 · 281s** — A general contractor asking for warranty work on a commercial job C&S did in Midland, TX (one room gets no cold air). Message passed on. Google status: Declined (not charged). ⏳ Open — existing commercial client waiting on a callback.

## 2026-10-27
- **09:17 · 67s** — Existing customer moving a two-system tune-up from Nov 5 to Mon Nov 9. Google status: Declined (not charged). ❌ Not a new lead (reschedule).

## 2026-10-29
- **09:17 · 53s** — The same contractor calling back about the Midland warranty work, six days after the first call. Message "run up the ladder". Google status: Declined (not charged). ⏳ Open — second ask, still no callback.

## 2026-10-30
- **13:16 · 94s** — Existing customer (new unit this summer) asking what filter size to buy. Google status: **Booked (charged)**. ❌ Not a job — a filter-size question that Google charged for. Dispute candidate.
- **16:02 · 216s · Mansfield** — Existing customer booking the winter check-up; offered the $165/year membership (two visits). Google status: Active (not charged). ✅ Booked, existing customer.

## 2026-11-02
- **10:12 · 170s · Burleson** — Existing commercial customer (a boutique) with a unit down; says an earlier service call was never completed. New service call put in. Google status: Booked (not charged). ✅ Booked, existing customer.

## 2026-11-04
- **15:23 · 522s** — Job seeker (HVAC/refrigeration tech) asking about openings and pay. Google status: Active (not charged). ❌ Not a lead.

## 2026-11-05
- **14:35 · 57s** — Owner of a hotel C&S has worked on, asking for the owner: a room has been offline about two months waiting on a part. Message taken. Google status: Active (not charged). ⏳ Open — existing commercial client chasing a callback.

## Running tally (Sep 15 – Nov 5, 19 leads not already logged above)

| Outcome | Count | Detail |
|---|---|---|
| ✅ Booked | 5 | All existing customers (2 on 09-15/16, 09-29, 10-30 check-up, 11-02) |
| ⏳ Open | 5 | 1 new customer mid-decision (10-22), 1 commercial quote never sent (09-17), 3 calls from 2 commercial clients waiting on a callback (10-23, 10-29, 11-05) |
| ❌ Not a lead | 9 | 3 job seekers, 1 C&S employee, 1 filter question, 1 reschedule, 1 solved by phone, 1 no connection, 1 message lead with no audio (not verifiable) |

**Flag for Edu:**
- **C&S is not turning away real jobs.** "Declined" is how the office marks calls that aren't a new job (job seekers, staff, reschedules, existing customers). The marking is mostly right.
- **LSA brings almost no new customers.** In 8 weeks (Sep 15–Nov 9, incl. the Oct 1–15 calls above) the only new-customer leads are 10-05 (Joshua, price-shopping), 10-21 (message, install) and 10-22 (Fort Worth, came by referral), plus the 09-17 commercial prospect. The rest are existing customers using the ad as the phone number. Google's "Booked" count overstates ad-driven jobs.
- **Two charged leads to dispute:** 09-29 (C&S employee) and 10-30 (filter-size question). The 9 declined + charged leads from Aug 1–Sep 9 were not pulled; same check is worth doing if the dispute window allows.
- **Callbacks owed to commercial clients:** the 09-17 proposal, the Midland warranty job (called twice, 10-23 and 10-29), and the hotel room (11-05). Not an ads issue, but it is revenue and worth passing to the AM.
