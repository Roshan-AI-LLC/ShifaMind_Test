# Roshan-AI Website Rebuild — Spec

This document is the implementation brief for rebuilding the
`Roshan-AI-LLC/Website` repository. It describes **information
architecture, content, and brand structure** — not visual redesign. The
existing font, logo, and theme are kept.

The goal is a Corti-style **platform site**: Roshan-AI is the company
and platform, ShifaMind is the first named product, and the
architecture is built so additional products plug in mechanically.

Reference model: <https://www.corti.ai/> and
<https://www.corti.ai/medical-coding>.

---

## 1. Brand architecture

| Layer | Name | Role | Where it appears |
|---|---|---|---|
| Company / legal | **Roshan-AI LLC** | Legal entity | Footer, privacy policy, contracts |
| Platform brand | **Roshan-AI** | Public-facing parent brand | Everywhere — domain, nav, hero |
| Product brand | **ShifaMind** | First product (clinical coding + reasoning for doctors) | `/products/shifamind`, app chrome, product-strip on homepage |
| Future products | TBD | Each gets its own `/products/<name>` page and entry in product strip | Same slots as ShifaMind |

Rule: nothing above the product layer is named "ShifaMind". The company
is Roshan-AI. ShifaMind is a thing Roshan-AI ships.

### Sub-brand treatment for ShifaMind

- ShifaMind gets its own **accent color** and **wordmark**, both living
  inside the Roshan-AI design system (same font family, same grid, same
  component library).
- On the Roshan-AI homepage and global nav, ShifaMind is referred to by
  name + one-line descriptor ("ShifaMind — clinical coding &
  reasoning for physicians").
- Inside `/products/shifamind` and inside the app itself, the ShifaMind
  wordmark + accent can lead, with a small "by Roshan-AI" lockup in the
  header.
- Mirror Corti/Symphony: Symphony has its own identity but never
  competes with Corti at the top level.

---

## 2. Domain & URL plan

| Now | Target | Notes |
|---|---|---|
| `roshan-ai.com` | `roshan-ai.com` | Primary marketing site |
| `platform.shifamind.me` | `app.roshan-ai.com` | The running app. Keep `platform.shifamind.me` as a 301 for ≥12 months |
| `shifamind.me` | 301 → `roshan-ai.com/products/shifamind` | |
| — | `roshan-ai.com/products/shifamind` | Product marketing page |
| — | `docs.roshan-ai.com` *(later)* | API/integration docs once they exist |

DNS / redirect work happens after the new site is live on
`roshan-ai.com`.

---

## 3. Site map

```
/                         Home — what Roshan-AI is + product strip
/products                 Product index
  /products/shifamind     ShifaMind product page (flagship — build first)
  /products/<future>      Reuses ProductPage template
/platform                 The Roshan-AI platform stack (shared infra story)
/developers               API / integration overview (thin v1 is fine)
/company
  /company/about          Mission, story, Roshan-AI LLC
  /company/team           Founders + team
  /company/careers        Open roles (or "we're hiring" CTA)
/contact                  Book a demo / contact form
/legal/privacy
/legal/terms
```

Navigation (top bar):
**Products ▾**  •  Platform  •  Developers  •  Company  •  Contact  •  **Sign in** (→ `app.roshan-ai.com`)

The Products dropdown is the key piece. It lists each product with a
one-line descriptor — same pattern Corti uses for Symphony, FactsR, etc.

---

## 4. Homepage blueprint (`/`)

Sections, top to bottom:

1. **Hero**
   - Headline: one hard claim about the company. e.g., *"AI infrastructure for clinical reasoning."*
   - Sub-headline: one sentence on what that means in practice.
   - Two CTAs: primary "See ShifaMind" → `/products/shifamind`; secondary "Talk to us" → `/contact`.
   - Background: subtle product visual (note → codes animation, or platform UI fragment), not stock imagery.

2. **Product strip**
   - One card per product. ShifaMind today; second slot can be "Coming soon" if you want to signal portfolio without faking it.
   - Each card: product wordmark, one-line descriptor, "Learn more →".

3. **Why Roshan-AI** *(three to four pillars)*
   - Clinical-grade reasoning, not generic LLM output
   - Built for integration (API-first)
   - Evidence + explainability on every prediction
   - Compliance posture (HIPAA, GDPR — only claim what's true today)

4. **Customer / pilot logos** *(or "trusted by clinicians at" if no logos yet)*
   - Even one or two pilot sites move the needle. If none, replace with a short trust statement and remove later.

5. **Platform diagram**
   - Simple visual: data in → Roshan-AI platform → products out. Same idea as Corti's stack diagram. Establishes that ShifaMind is one consumer of shared infra.

6. **Closing CTA band**
   - "Build with Roshan-AI" / "Book a demo".

7. **Footer**
   - Products • Company • Developers • Legal • Roshan-AI LLC, ©year, address.

---

## 5. ShifaMind product page (`/products/shifamind`)

Modeled directly on `corti.ai/medical-coding`. **Build this first** — it is the highest-leverage page.

1. **Hero**
   - Headline: hard claim. e.g., *"ICD-10 predictions doctors can defend."*
   - Sub: one sentence — "ShifaMind reads a clinical note and returns ranked ICD-10 codes with the concept evidence behind each one."
   - One benchmark number (only if you have it — accuracy on a held-out set, latency, etc.). If you don't have a clean number yet, omit rather than fake.
   - CTAs: "Try ShifaMind" → `app.roshan-ai.com` signup • "Book a demo".

2. **Live example block** *(the centerpiece — Corti does this brilliantly)*
   - Left: a real clinical note (use one of the 10 MIMIC-IV samples).
   - Right: ranked ICD-10 codes with confidence + the activated concepts each code is grounded in.
   - Static is fine for v1; an animated reveal is better; an actual live demo is best. Pick the level you can ship.

3. **What ShifaMind does** *(three columns)*
   - Predict — ranked ICD-10 codes from free-text notes
   - Explain — concept activation showing *why* each code
   - Discuss — grounded chat with the prediction in context

4. **Breadth grid**
   - Code systems supported (ICD-10-CM today; PCS/CPT/UK if/when added).
   - Specialties / note types covered.
   - Mirror Corti's coding-page grid layout — it sells the surface area.

5. **For developers / integrators** *(even thin)*
   - "Integrate ShifaMind via API." Show one curl example or one JSON response. Signals seriousness even if API access is gated.
   - Link to `/developers`.

6. **Security & compliance strip**
   - HIPAA, GDPR, data handling. Bullets, not paragraphs. Only claim what's true.

7. **FAQ** *(5–8 items)*
   - "How is this different from a general LLM?"
   - "Does ShifaMind replace coders?" (No — clinician/coder-in-the-loop.)
   - "What models power it?" (BioClinicalBERT Phase 1 + concept attribution.)
   - "How do you handle PHI?"
   - "Can I try it on my own notes?"

8. **Closing CTA**
   - "Try ShifaMind" / "Book a demo".

---

## 6. Reusable `ProductPage` template

Every product page (`/products/<name>`) uses the same component
skeleton:

```
<ProductHero claim subClaim primaryCta secondaryCta benchmark? />
<LiveExample input output />
<ThreeColumnFeatures items[3] />
<BreadthGrid columns[] rows[] />
<DeveloperBlock codeExample />
<ComplianceStrip items[] />
<FAQ items[] />
<ClosingCta />
```

Adding product #2 = filling in the same slots. No new design work.

---

## 7. Pages beyond the product page

### `/platform`
The shared-infra story. Diagram + a few sentences per layer
(ingestion, models, reasoning, APIs, app surface). Establishes that
Roshan-AI is a platform, not a single product.

### `/developers`
Thin v1: "Roshan-AI APIs power clinical reasoning in your product."
One auth example, one endpoint example, "Request access" CTA.
Grows into real docs at `docs.roshan-ai.com` later.

### `/company/about`
Mission, founding story, what Roshan-AI is building toward. The
ShifaMind story can be one chapter inside this, not the headline.

### `/company/team`
Founders + key team. Photos, one-line bios, LinkedIn.

### `/contact`
Form: name, email, organization, role, message, "I'm a [clinician /
developer / partner / press]". Routes to the right inbox.

---

## 8. Content tone

- Direct, technical, confident. Match Corti.
- No marketing fluff. Every claim is either a number, a screenshot, or
  a concrete capability.
- Doctors and developers are the two audiences. Hospital execs are
  tertiary. Don't write for everyone.

---

## 9. Tech notes for the Website repo

- Keep the current font and logo system.
- The repo should expose a single `ProductPage` component (section 6)
  used by every `/products/<name>` page.
- Sub-brand accents (ShifaMind accent color + wordmark) live as design
  tokens (`brand.shifamind.accent`, `brand.shifamind.wordmark`), so
  future products add a token and a wordmark asset, nothing else.
- Add `/sitemap.xml` and `robots.txt`. Set `<title>` and OG tags per
  page — the current site likely under-does this.
- All external CTAs ("Sign in", "Try ShifaMind") point to
  `app.roshan-ai.com` once the platform move happens; until then, point
  to `platform.shifamind.me`.

---

## 10. Migration sequence

1. Build new site on a staging URL off the Website repo.
2. Ship `/`, `/products/shifamind`, `/contact`, `/company/about`, `/legal/*` first. The rest can come after launch.
3. Cut `roshan-ai.com` over once those pages are live.
4. Set up `app.roshan-ai.com` DNS pointing at the existing platform host. Update Supabase auth allowed redirect URLs to include both old and new domains during the transition.
5. Update the platform repo to use `app.roshan-ai.com` as its canonical URL; keep `platform.shifamind.me` as a 301.
6. Add 301 from `shifamind.me` root to `roshan-ai.com/products/shifamind`.
7. After ≥12 months of stable redirects, decide whether to retire the `shifamind.me` domain.

Step 5 is a small change in the platform repo (this one — `shifamind_test`) and should be done in a separate session once the website is live.

---

## 11. Open decisions for the Website-repo session to make

- Final headline copy for the Roshan-AI homepage hero.
- Final claim line for the ShifaMind product page hero.
- Whether to ship the live-example block as static, animated, or live in v1.
- Exact ShifaMind accent color (within the existing Roshan-AI palette).
- Whether `/developers` ships at launch or after.

Everything else above is settled.
