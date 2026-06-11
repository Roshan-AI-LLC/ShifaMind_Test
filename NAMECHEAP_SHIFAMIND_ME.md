# shifamind.me — disable auto-renew + redirect to the platform

Goal: stop ever being charged for `shifamind.me` again, but while it's still
active, send all its traffic to the ShifaMind platform on roshan-ai.com.

> Important ordering: **set the redirect target first** (the platform must be live
> at `https://platform.roshan-ai.com/shifamind`), otherwise the redirect lands on
> a 404. If the platform isn't on roshan-ai.com yet, point the redirect at the
> ShifaMind product page on the marketing site (`https://roshan-ai.com/products/shifamind`
> — adjust to the real path) until the platform migration is done.

## A. Turn off auto-renew (stops future charges, keeps your account)
1. Log in to Namecheap → **Domain List**.
2. Find `shifamind.me` → click **Manage**.
3. On the **Domain** tab, find **AUTO-RENEW** and toggle it **OFF**.
   - You will **not** be charged again. The domain stays fully active until its
     current paid term ends (the expiry date shown on that page), then expires.
   - You can re-enable any time before expiry if you change your mind.
4. (Optional) Turn off any add-ons billing the same way (e.g. PremiumDNS) so
   nothing else renews.

> Do **not** delete the whole Namecheap account — it doesn't stop charges any
> sooner than turning off auto-renew, and you'd lose the ability to redirect or
> reclaim the name while it's still yours.

## B. 301-redirect shifamind.me → the platform (works until expiry)
Namecheap has built-in URL forwarding (only works while using Namecheap BasicDNS —
which is the default).

1. Domain List → `shifamind.me` → **Manage** → **Advanced DNS** (or the
   **Redirect Domain** section on the Domain tab).
2. Under **Redirect Domain**, add:
   - Source: `@`  →  Destination: `https://platform.roshan-ai.com/shifamind`  →  Type: **Permanent (301)**
   - Source: `www` → Destination: `https://platform.roshan-ai.com/shifamind` → Type: **Permanent (301)**
3. Save. Allow a few minutes (up to ~30) for it to take effect, then test:
   `curl -I https://shifamind.me` → expect `301` with
   `Location: https://platform.roshan-ai.com/shifamind`.

> Note: Namecheap's free URL redirect needs their nameservers/BasicDNS. If you've
> moved shifamind.me's DNS elsewhere (e.g. Cloudflare), do the redirect there
> instead (Cloudflare: a Redirect Rule, 301, preserving path if you want).

## C. What happens at expiry
When the paid term ends, `shifamind.me` expires and the redirect stops working.
If you want the redirect to live on long-term, the alternative is to **keep**
the domain (leave auto-renew on) purely as brand insurance — it's only a few
dollars a year. Your call; this runbook follows your choice to let it lapse.

## Optional: I can do steps A & B with you in the browser
If you want, I can drive these in your logged-in Namecheap tab (Claude in Chrome)
so you don't have to hunt through the UI — just say the word and have Namecheap
open and signed in.
