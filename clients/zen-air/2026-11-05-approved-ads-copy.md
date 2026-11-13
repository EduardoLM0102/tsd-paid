# Zen Air: build sheet for "Publish Approved Ads" (AT task 2ad75400, requested by Edu 11-03)

Request: publish 3 to 6 ads from Drive folder APPROVED (1zngHomuBS4GySuoCk86Qig0fl8P_WkqM), using Zen Air's taglines and brand guidelines in copy and headline, then send back for review.

**Decisions (Gui, 2026-11-09):**
1. Campaign: the live lead CBO `09/17/26 - CBO | Leads` (120247267872090711). Add 3 new DCT ad sets, one per angle. CBO budget unchanged.
2. Destination: the same instant form the live lead ad uses (`09/22/26 | Ad 02 - Images 07, 11, 13`, ad 120247339585920711).
3. No offer. The $49 tune-up special is out (not confirmed current), so Ad(12), which has "$49" printed on it, is not used and no copy mentions a price.

Structure follows the Meta doctrine: one angle per DCT ad set, up to 3 creatives of that angle, 2 primary texts + 2 headlines written for the angle (any text can pair with any image). That gives 3 DCT ads using 7 of the 11 creatives.

## Sources checked 11-05 (callzenair.com)
- Taglines: "Stress Free HVAC", "We've got the Zen for your den", "Breathe easier with Zen Air Heating & Cooling!", "The art of comfort". The creatives also use "Inhale Zen, Exhale Comfort" and "Your Neighborhood HVAC".
- Claims used: rated 5 out of 5, BBB A+ accredited, 100% satisfaction guarantee (stated on heating work), NATE-certified techs, family-owned and operated since 2016, free estimates on new installations, financing on installs, brands (Lennox, Trane, Carrier, Daikin and others), phone 678-853-7440.
- Nothing below uses a claim that isn't on the site or on the creative.

## Ad set 1: Furnace Tune-Up
Name: `11/09/26 - Furnace Tune-Up (DCT)`
Images: `20261022 Ad(9).png`, `20261022 Ad(11).png`, `20261022 Ad(5).png` (comic). Spares, same message: Ad(1), Ad(10).

**Primary text 1**
Your furnace sat all summer. Give it a once-over before the first cold night.

🔥 Furnace tune-ups before the cold hits
🧰 NATE-certified techs
🏠 Family-owned in Duluth since 2016

**Primary text 2**
Ready for winter? A quick tune-up now beats a cold night later. We've got the Zen for your den.

✅ 100% satisfaction guarantee
⭐ Rated 5 out of 5
📞 Prefer to call? 678-853-7440

**Headline 1:** Ready for Winter? Book a Tune-Up
**Headline 2:** Stress Free HVAC
**Description:** We've got the Zen for your den

## Ad set 2: Proof and trust
Name: `11/09/26 - Rated 5 of 5 (DCT)`
Images: `20261022 Ad(8).png` (real tech photo), `20261022 Ad(3).png` (100% guarantee), `20261022 Ad(2).png` (bear version of Ad 8).

**Primary text 1**
Real techs in real homes around Duluth. That's how we earned a 5 out of 5 rating.

⭐ Rated 5 out of 5
🏅 BBB A+ accredited
🧰 NATE-certified technicians

**Primary text 2**
Stress Free HVAC means you don't have to wonder how the job turns out. Breathe easier this winter.

✅ 100% satisfaction guarantee on heating work
🏠 Family-owned and operated since 2016
📞 Prefer to call? 678-853-7440

**Headline 1:** Rated 5 Out of 5 Near Duluth
**Headline 2:** 100% Satisfaction Guarantee
**Description:** The art of comfort

## Ad set 3: New installations
Name: `11/09/26 - Free Install Estimates (DCT)`
Images: `20261022 Ad(4).png` only. The folder has just one install creative, so this angle runs with 1 image instead of the usual 3.

**Primary text 1**
Thinking about replacing an old furnace or AC? Start with a free estimate and a straight answer.

🏠 Free estimates on new installations
💳 Financing available
🔧 Lennox, Trane, Carrier, Daikin and more

**Primary text 2**
Easy installations, the Zen way. We'll look at your setup and give you options that fit your home.

✅ Free estimates on new installs
🧰 NATE-certified techs
⭐ Rated 5 out of 5

**Headline 1:** Free Estimates on New Installs
**Headline 2:** Easy Installations, Stress Free
**Description:** Financing available

## Not used
- Ad(12): "$49 Furnace Tune Up" is printed on the image. Out with the offer.
- Ad(6), "Your Neighborhood HVAC / CallZenAir.com": brand-only, better for the awareness campaign.
- There is no Ad(7) in the folder.

## How to build (Ads Manager UI)
The Meta MCP can't upload these PNGs (it needs an image already in the ad account or a public URL, and the Drive folder is private) and can't read which instant form the live ad uses. So the build goes in the UI:
1. In `09/17/26 - CBO | Leads`, duplicate the live ad set `09/22/26 - Service Area ZIPs (New Creatives)` (120247339585910711) 3 times. This carries over the 130 ZIPs, the Marietta / Monroe / 30320 exclusions, people living in, Advantage+ audience, placements, Leads goal and instant form destination. Rename per the sheet above.
2. In each copy, delete the duplicated Ad 02 and create one new dynamic creative ad: upload the angle's images from the Drive folder, paste the 2 primary texts + 2 headlines + description, and pick the same instant form and CTA as the live Ad 02.
3. Leave the live ad set and Ad 02 running. Campaign budget stays as is; the CBO splits it across the 4 ad sets.
4. Publish only on Gui's go. Then send back to Edu for review on the AT task, and log the build in `clients/zen-air/meta-ads-log.md`.

Zen Air tracking is under Gui's investigation (10-26). This build doesn't touch targeting, budget or tracking.
