# Mission Accomplished — LSA Call Wins Log

Scope: every Google Local Services lead on the dedicated LSA account 4904262993 from 2026-10-09 to 2026-11-07 (the Oct/Nov strategy review cycle). That's 15 leads: 12 calls (all recorded), 2 messages and 1 online booking. Calls were pulled with `pull_lsa.py` and transcribed locally with faster-whisper (small.en). Names and streets may come out wrong in the transcription, so street addresses and emails are left out on purpose.

The Google status (what the client's team marked in the LSA inbox) and whether the lead was charged are shown next to the transcript outcome, never in place of it.

Legend: ✅ Booked · ⏳ Open/follow-up needed · ❌ Not a lead · ⚠️ IVR-only

## 2026-10-09
- **10:10 · 211s · LSA call · Lake Havasu (Charles)**: AC fan runs outside but no cold air, unit trying to start and failing. Booked same day, Jose 2 to 5 PM. Unit age unknown, maybe ~15 years. ✅ Booked (repair visit). Google: BOOKED, charged. Possible replacement opportunity if the unit is old.
- **10:25 · 55s · LSA call**: Asked if they service portable roll-around AC units. Team said no, replace it instead. ❌ Not a lead (service not offered). Google: DECLINED, **charged**.
- **18:46 · LSA message**: "RV AC not working, pump not working, just motor", quote request. ❌ Not a lead (RV). Google: DECLINED, charged then **credited**.

## 2026-10-20
- **09:39 · 61s · LSA call**: Restaurant "make line" (refrigerated prep table) not holding temperature. Team said they don't do refrigeration. ❌ Not a lead (service not offered). Google: DECLINED, **charged**.
- **11:08 · LSA message**: Quote request for a **new central AC unit**, 1,100 sq ft home, electric AC / gas heat. The client's AI scheduler ("Tina") replied twice asking for a phone number (11:09 and 12:09). No reply from the customer, no human follow-up visible. ⏳ Open, real **replacement** lead that went nowhere. Google: DECLINED, charged.

## 2026-10-21
- **09:55 · 79s · LSA call · apartment complex**: Maintenance person, AC keeps blowing transformers, they can't find the short. Team quoted the $99 diagnostic (waived if repairs are approved). Caller will check with the owner and call back. ⏳ Open, real repair lead (commercial/rental). Google: DECLINED, charged.

## 2026-10-23
- **14:18 · 226s · LSA call · Lake Havasu (John)**: Rental house, outdoor condenser not running, out for 1.5 to 2 months, already swapped the capacitor. Old Goodman, original to the house. Booked Monday 11 AM to 2 PM. ✅ Booked (repair visit). Google: ACTIVE (not marked booked), charged. Strong replacement candidate (old unit, out for months, landlord).

## 2026-10-26
- **09:10 · 78s · LSA call**: Wants a labor-only quote for two houses (5-ton + 4-ton systems, ~600 ft of ductwork), customer supplies the equipment. Team only prices full systems ($7k to $25k range given). ❌ Not a lead under the client's policy (labor-only). Google: DECLINED, **charged**. Note: that's ~9 tons of equipment; worth asking Brian if he'd quote the full systems.
- **12:30 · 14s · LSA call**: Went straight to "Your call has been forwarded to an automated voice messaging system." ⚠️ IVR-only, midday. Google: DECLINED, not charged.

## 2026-10-27
- **09:00 · 139s · LSA call**: Delivery driver (freight company) calling back about a delivery, said nobody answered last time. Put on hold, then "everybody is currently on the phone". ❌ Not a lead. Google: ACTIVE, not charged.

## 2026-10-29
- **11:04 · LSA online booking**: Booked through the LSA booking button, no details in the API. ✅ Booked per Google, can't be verified from here. Google: BOOKED, charged.

## 2026-10-30
- **09:20 · 22s · LSA call**: Only the IVR greeting played twice ("press 1..."), caller hung up before reaching anyone. ⚠️ IVR-only. Google: DECLINED, **charged**.
- **10:17 · 230s · LSA call · Ehrenberg AZ**: Park model RV, heat pump package unit under warranty, heating coil burned out. Team was honest: with the 3-hour round trip it would cost $200 to $400 in labor, so buy the part online. Caller will research and call back if needed. ⏳/❌ Open but unlikely. Google: **BOOKED** (the transcript shows nothing was booked), charged.

## 2026-11-02
- **18:03 · 112s · LSA call · Mohave County (Vince)**: Wanted dryer vent cleaning only. Team doesn't do dryer vents alone, offered a free whole-house duct cleaning estimate. Booked for the next day, 11 AM to 2 PM. ✅ Booked (free estimate, upsell from a small ask). Google: ACTIVE (not marked booked), charged.

## 2026-11-06
- **08:11 · 6s · LSA call**: Hung up during the IVR greeting. ⚠️ IVR-only. Google: ACTIVE, not charged.

## Running tally (2026-10-09 to 2026-11-07)

| Outcome | Count | Detail |
|---|---|---|
| ✅ Booked | 4 | 10-09 AC repair, 10-23 rental AC repair, 11-02 duct cleaning estimate (all three confirmed in the transcript), 10-29 online booking (Google only) |
| ⏳ Open | 3 | 10-20 new AC quote (message, no phone), 10-21 apartment complex (waiting on owner), 10-30 park model RV warranty (unlikely) |
| ❌ Not a lead | 5 | portable AC, RV AC message, commercial refrigeration, labor-only install, delivery driver |
| ⚠️ IVR-only | 3 | 10-26 (voicemail system), 10-30 (hung up at IVR), 11-06 (6s) |

Spend for the period: $790.83, 12 charged leads, 1 credited.

**Flag for Edu**
- **Real leads = 7 (4 booked + 3 open), same count as the AT row, but a different set than the "not declined" count.** The client's LSA statuses don't match what happened: 2 real leads are marked DECLINED (the new-AC quote and the apartment complex), 2 booked calls are still ACTIVE, and the RV call is marked BOOKED though nothing was booked. Their statuses can't be used as the lead-quality signal.
- **Dispute candidates (charged, not a lead):** portable AC (10-09), commercial refrigeration (10-20), IVR hang-up (10-30), maybe labor-only (10-26). The 10-09 one is probably past Google's 30-day dispute window already; the others still have time.
- **One out of three is a service they don't offer.** RVs show up twice (Lake Havasu / Parker / Ehrenberg have lots of RVs and park models), plus portable units and refrigeration. Worth checking the LSA job types and service-area settings, and asking Brian if he wants RV/park model work or not.
- **The only explicit replacement request was lost to the AI texting bot.** "Tina" asked twice for a phone number and nobody followed up by hand. Replacement is 60% of Brian's planned budget, so this is the lead type he cares about most.
- **Replacement signals on repair calls aren't being picked up.** The 10-09 (~15-year-old unit) and 10-23 (old Goodman, out for 2 months, rental) calls are classic replacement candidates. Nobody mentioned financing or replacement on the call; that's for the tech on site, but worth telling Brian.
- **Phone handling:** the person who answers is quick and books well with clear time windows. But every call starts with a ~15 to 20 second "press 1" IVR, and 3 of 12 callers never got past it (one at midday went to the voicemail system). Also, the AI texting bot gives **(928) 517-7775** while the old Meta ads used 928-517-7702: confirm which number goes on the new Meta lead forms.
- **No leads at all from Oct 10 to Oct 19.**

**Sent to the AM (2026-11-10):** AT Internal Request `3de43e31` "LSA lead review and Facebook payment method", submitted by Edu, Execution = Angela. Asked the office to fix the LSA statuses, follow up on the 10-20 replacement quote, say yes/no on RV and park model work, and confirm the phone number for the Meta forms. Told her we're disputing the 10-20 commercial refrigeration and 10-30 IVR hang-up calls (10-26 labor-only left out). Disputes not filed yet (fu-140).

**2026-11-12 dispute attempt (fu-140), via Cowork + API read:** both target leads show "Rating submitted" in the LSA UI (status Archive = API DECLINED) with no dispute option. API `credit_details.credit_state` = UNSPECIFIED for 347255880 (10-20 refrigeration) and 349098042 (10-30 IVR hang-up): a rating was given (likely by the office when they declined it) but NO credit was requested or granted. For comparison the 10-09 RV message 345281710 shows CREDITED (11-06), so that route works when the rating carries a credit-eligible reason. Nothing changed in the account. Windows close ~11-19 (10-20 lead) and ~11-29 (10-30 lead).

**2026-11-12 CLOSED (Edu):** there is no LSA dispute anymore. You rate a lead bad and Google refunds it or not. These two were rated and not refunded, so nothing more to do. fu-140 closed.
