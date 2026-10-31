# Game State & Branching Rules

**Status:** design lock v1 (31 Oct 2026). This doc defines every variable the story engine tracks, every choice and QTE that changes them, and how the ending is picked. Where it differs from the variable table in spec §6, this doc wins. Everything else in spec v0.3 stays authoritative.

**Three sources of truth (keep them separate):**

| Document | Owns |
|---|---|
| Game Spec v0.3 ([`design/Texas_Fractured_Time_Game_Spec_v0.3.docx`](design/Texas_Fractured_Time_Game_Spec_v0.3.docx)) | Vision, architecture, art direction, overall experience |
| **This doc**: Game State & Branching Rules | Variables, conditions, effects, QTE rules, ending resolution. The gameplay rules contract. |
| Branching Story Graph | Visual picture of the playable narrative. **Generated from the same content data the engine runs**, never drawn by hand, so it can't drift. (The v0.3 PDF in `docs/design/` is the design-intent reference until then.) |

Audience: middle-school players. Rules are kept simple enough that a player can understand *why* they got their ending.

---

## 0. Decisions locked here

| Topic | Decision |
|---|---|
| Source of truth | Spec v0.3 is authoritative. `art/reference/ref_style_storyboard.png` is an art-style reference only. |
| Chapter flow | Spec v0.3: Title → Select → Tutorial → Fracture → Gonzales → Béxar → Alamo → Spring 1836 Montage (Declaration *as a dated flashback*, Goliad, Runaway Scrape) → San Jacinto (camp + Eighteen Minutes) → Ending. |
| Paradox rule | One visible meter, **Time Ripples** (`timeline_risk`). It measures **how much future knowledge or technology influences people and events in the past**, not how often you use the device. If it's 70 or more when you get home → Paradox. Plain rule for players: "you changed too much." See §4 for what counts. |
| Ending priority | Stranded > Paradox > Protector > Observer |
| Choice timer | 12 s by default (the longest the spec allows, picked for younger players). Can be stretched or turned off in Settings. |
| QTE failure | Never a game over. A failed QTE changes the story or the meters. |
| Choice buttons | Four options map to face buttons A / B / X / Y (Cross / Circle / Square / Triangle on PlayStation). A character-only option *replaces* one slot. |

## 1. Cast & key names

| ID | Name | Who | Notes |
|---|---|---|---|
| `rowan` | Rowan | Playable, 13, the Observer (deer) | |
| `morgan` | Morgan | Playable, 14, the Protector (horse) | |
| `ellis` | Ellis | Playable, 13, the Strategist (fox) | |
| `courier` | Jonah Pryor | Fictional 16-year-old Alamo courier | Emotional centerpiece. Possible final companion. |
| `josefa` | Josefa Treviño | Fictional Tejana mother, Béxar | "The family" in `family_trust` |
| `tomas` | Tomás Treviño | Josefa's 11-year-old son | Possible final companion |
| `will` | Will Carter | Fictional 17-year-old Texian volunteer | Fallback final companion |
| `reed` | Captain Reed | Fictional Texian officer, San Jacinto camp | Asks the knowledge question |
| `ortiz` | Teniente Ortiz | Fictional Mexican army lieutenant, Gonzales | Mexican viewpoint at Gonzales |
| — | The Chrono-Compass | The damaged time device | What the spec calls "the device" |

Real historical figures (Houston, Santa Anna, Travis, delegates) are seen only at a distance or in archive notes. They are never playable conversation partners.

---

## 2. Variables

### 2a. Run state (saved per save slot)

| Variable | Type / range | Start | Player sees it as | What it does |
|---|---|---|---|---|
| `character_id` | `rowan \| morgan \| ellis` | set at select | Portrait | Unlocks character options; sets advantages; picks the epilogue |
| `run_mode` | `full \| demo` | set at new game | — | `demo` follows the short path and applies the demo snapshot (§5, Demo) |
| **Meters** | | | | |
| `suspicion` | int 0–100 | 10 | 👁 **Eyes on You** | At 70+, San Jacinto opens with an interrogation and the knowledge claim gets harder. At 50+, Jonah is wary of you. |
| `timeline_risk` | int 0–100 | 0 | 🌀 **Time Ripples** | At 70+ when you return home, you get the Paradox ending |
| `device_integrity` | int 0–100 | 80 | 🔋 **Device Power** | Under 40 makes extraction harder. At 0 the return window can't open (Stranded). |
| **Relationships** | | | | |
| `family_trust` | int −2..+2 | 0 | Trust in the Treviño family (journal) | ≥1 → shelter, their wagon in the Scrape, Josefa vouches for you, Tomás can be your companion |
| `courier_trust` | int −2..+2 | 0 | Trust in Jonah (journal) | Changes his dialogue; flavors the Protector epilogue |
| **Resources** | | | | |
| `supplies` | int 0–3 | 1 | 🎒 icons | Spend to help people or repair the device |
| `recoveries_left` | int 0–1 | from character (Ellis 1, others 0) | "Second chance" badge | Retry one failed sneak, trick or escape QTE |
| **Story choices** | | | | |
| `cover_identity` | `unset \| louisiana \| confused \| fled \| truth` | `unset` | — | Gonzales dialogue; whether the San Jacinto knowledge claim is believed |
| `device_exposed` | bool | false | — | Someone saw the device glow. Dialogue callbacks. |
| `gonzales_choice` | `unset \| cannon \| supplies \| observe \| approach` | `unset` | — | Béxar and Alamo entry callbacks |
| `bexar_choice` | `unset \| escort \| warn \| misdirect \| supplies \| refuse` | `unset` | — | Journal and epilogue text |
| `shelter_available` | bool | false | Journal note | Set at the end of Béxar: `family_trust ≥ 1` |
| `courier_plan` | `unset \| leave_alone \| stay \| leave_together` | `unset` | — | What Jonah **agrees** to do. Set by the C3 choice. |
| `courier_fate` | `unknown \| safe \| injured \| lost` | `unknown` | Journal note / memorial | What **actually happens** to Jonah. Resolved only at C3 exit, after the escape QTE (rule in C3). safe or injured → he can be your companion. `lost` = stayed for the final assault (off-screen, memorial entry). |
| `montage_choice` | `unset \| wagon \| wounded \| crossing \| leave` | `unset` | — | Epilogue text |
| `knowledge_claim` | `unset \| credible \| doubted \| exposed` | `unset` | — | Captain Reed's attitude |
| `intel` | bool | false | Journal note | Makes extraction easier |
| **Finale** | | | | |
| `companion` | `none \| courier \| tomas \| will` | `none` | — | Who is beside you at San Jacinto (rule in §5, S2) |
| `final_choice` | `unset \| help \| leave \| hide \| give_device` | `unset` | — | Extraction difficulty and the ending |
| `companion_saved` | bool | false | — | Protector gate |
| `return_window` | bool | false | — | Opens at San Jacinto if `device_integrity > 0`. Closed by `give_device`. |
| `extraction_result` | `unset \| success \| fail` | `unset` | — | Stranded gate |
| `ending` | `unset \| observer \| protector \| stranded \| paradox` | `unset` | Ending card | Computed once (§7) |
| **Archive** | | | | |
| `historical_records` | set of record IDs | ∅ | Journal "Archive x / 9" | Archive entries, recap, Observer epilogue |

Record IDs (9): `gonzales`, `gonzales_mexican_view`, `bexar`, `alamo`, `declaration`, `goliad`, `goliad_testimony`, `runaway_scrape`, `san_jacinto`.

### 2b. Engine bookkeeping (saved, not gameplay)

`schemaVersion`, `contentVersion`, `currentNodeId`, `visitedNodes[]`, `choiceLog[] {choiceId, optionId, timedOut, atMs}`, `qteLog[] {qteId, result, usedRecovery}`, `timestamp`.

### 2c. Profile (shared across save slots)

`tutorialCompleted`, `settings {timerMultiplier, timersOff, holdToConfirm, autoSucceedQte, textSize, highContrast, reducedMotion, volumes{music,sfx,ambience}}`, `controllerMapping`, `seenDialogueIds` (for skip and fast-forward).

---

## 3. Character advantages (data, not code)

| Character | Advantage | Numbers | Character-only options |
|---|---|---|---|
| Rowan | Observation | Stealth/detection QTE windows ×1.25 | C3 "Notice his fear" (replaces **A**); Goliad "Listen to the hidden survivor" |
| Morgan | Resilience | Physical QTE windows ×1.25 | Scrape "Lift the wheel yourself" (A variant, no device damage on fail); San Jacinto "Shield them" (A variant) |
| Ellis | Ingenuity | `recoveries_left = 1` | Béxar "Send the patrol the wrong way" (replaces **B**); camp "Talk your way past the sentry" (replaces **B**) |

Every girl gets an early and a late moment where her ability visibly changes the story, not just a timing bonus:

| Character | Early payoff | Late payoff |
|---|---|---|
| Rowan | Recognizes Jonah's fear (C3) | Hears the Goliad survivor's testimony (Montage) |
| Morgan | Frees the wagon at the Runaway Scrape with less risk (Montage) | Shields her companion at San Jacinto (S2) |
| Ellis | Misdirects the patrol in Béxar (C2) | Talks past the sentry near San Jacinto (S1) |

The timing multipliers and the recovery are passive extras on top of these moments. Each payoff shows a small character emblem (deer / horseshoe / fox) so the player notices it.

QTE categories: **stealth** (P0_HIDE, C1_SNEAK, C2_STREETS, S_RECON), **physical** (C1_CANNON, C4_WAGON, C4_CROSSING, S_HELP), **trick** (C2_TRICK, S_TRICK), **escape** (C3_ESCAPE, S_EXTRACT). A recovery can be used on stealth, trick or escape QTEs.

## 4. Shared rules

- **Clamp:** after every effect, clamp each meter to its range.
- **What raises Time Ripples:** future knowledge or technology *influencing people or events*.
  - Counts: telling someone the future (truth +25, warn Jonah +20, reveal plans +25), someone seeing the device work (`exposeDevice` +15), leading others along a route you only know from the device (+10; smaller because nobody learns where it came from).
  - Doesn't count: using the device privately (checking it, repairing it, reading your own records), or helping people with ordinary skills and supplies.
  - The device screen shows this rule the first time the meter moves.
- **`exposeDevice` macro:** `timeline_risk +15`, `suspicion +10`, `device_exposed = true`.
- **Feedback:** every effect that changes a relationship or meter shows a short toast, e.g. "Jonah will remember that." or "🌀 Time ripples."
- **Determinism:** same state + same inputs = same result. No random rolls.
- **Accessibility:** `autoSucceedQte` treats every QTE as a success. `timersOff` removes choice timers, so the timeout edges never fire.

---

## 5. Beat-by-beat: what reads and writes what

Format: **Button · Option → effects → next**. "QTE ✓ / ✗" = success / fail.

### P0 — The Fracture (modern San Antonio → 1835)

Riders find you in the brush with the Chrono-Compass glowing.

**Choice `P0_COVER`** "Where did you come from?" (timeout → B)

| Btn | Option | Effects |
|---|---|---|
| A | "I'm traveling from Louisiana." | `cover_identity=louisiana`, suspicion +5 |
| B | "I… don't understand." | `cover_identity=confused`, suspicion +10 |
| X | "Run!" | `cover_identity=fled`, suspicion +15 |
| Y | "Tell the truth." | `cover_identity=truth`, suspicion +15, timeline_risk +25 |

**QTE `P0_HIDE`**: stealth, directional sequence, 4 inputs. ✓ nothing · ✗ `exposeDevice`.

### C1 — Come and Take It (Gonzales, Oct 2 1835)

**Entry:** if `cover_identity=truth`, townsfolk call you "the strange girl." If `fled`, one of the riders recognizes you. If `device_exposed`, there's a rumor about "a girl with a glowing watch" (all dialogue only).

**Choice `C1_HELP`** "How will you help?" (timeout → X)

| Btn | Option | Effects | QTE |
|---|---|---|---|
| A | Help move the cannon | `gonzales_choice=cannon` | C1_CANNON |
| B | Assist with supplies | `gonzales_choice=supplies`, supplies +1, suspicion −5 | C1_SNEAK |
| X | Stay hidden and observe | `gonzales_choice=observe`, suspicion −5 | C1_SNEAK |
| Y | Approach the Mexican soldiers | `gonzales_choice=approach`, suspicion +10, records += `gonzales_mexican_view` (talk with Teniente Ortiz) | C1_SNEAK |

- **QTE `C1_CANNON`**: physical, alternating rhythm, 10 s. ✓ suspicion −5 ("one of us") · ✗ device_integrity −10.
- **QTE `C1_SNEAK`**: stealth, move/freeze, 15 s. ✓ nothing · ✗ suspicion +10.

**Exit:** records += `gonzales`.

### C2 — Road to Béxar (Dec 1835)

**Entry callbacks:** `gonzales_choice=approach` → Josefa saw you speak respectfully with the soldiers, family_trust +1. `gonzales_choice=cannon` → Texian volunteers recognize you, suspicion −5.

**Choice `C2_FAMILY`** "What will you do?" (timeout → Y)

| Btn | Option | Effects | QTE |
|---|---|---|---|
| A | Escort the family | `bexar_choice=escort`, family_trust +2, suspicion +5 | C2_STREETS (✗ also family_trust −1) |
| B | Warn the soldiers | `bexar_choice=warn`, family_trust +1, suspicion +5 | C2_STREETS |
| B *(Ellis)* | Send the patrol the wrong way | `bexar_choice=misdirect`, family_trust +2 | C2_TRICK |
| X | Give supplies and leave *(needs supplies ≥1)* | `bexar_choice=supplies`, supplies −1, family_trust +1 | C2_STREETS |
| Y | Refuse | `bexar_choice=refuse`, family_trust −1 | C2_STREETS |

- **QTE `C2_STREETS`**: stealth, move/freeze, 15 s. ✓ nothing · ✗ suspicion +10, device_integrity −10.
- **QTE `C2_TRICK`**: trick, timed decision, 8 s. ✓ nothing · ✗ suspicion +15.

**Exit:** `shelter_available = family_trust ≥ 1`; records += `bexar`.

### C3 — The Alamo (Feb 23 – Mar 6 1836)

You're inside when the siege begins and must get out before the final assault. You never see the assault itself.

**Entry callbacks:** `gonzales_choice=cannon` → Jonah was at Gonzales too, courier_trust +1. `suspicion ≥ 50` → he's heard rumors about you, courier_trust −1.

**Choice `C3_COURIER`** "Warn the courier?" (timeout → X)

The choice sets only what Jonah **agrees** to (`courier_plan`). His real fate is resolved at chapter exit.

| Btn | Option | Effects |
|---|---|---|
| A | Tell him to leave | `courier_plan=leave_alone`, courier_trust +1, suspicion +5 |
| A *(Rowan)* | Notice his fear | `courier_plan=leave_alone`, courier_trust +2 |
| B | Warn him of the outcome | `courier_plan=leave_alone`, courier_trust +2, suspicion +15, timeline_risk +20 |
| X | Say nothing | `courier_plan=stay` |
| Y | Offer to carry a message together | `courier_plan=leave_together`, courier_trust +1 |

`leave_alone`: Jonah rides out with a dispatch **before** your escape. A short scene shows him leaving, so his fate doesn't depend on your QTE.

**QTE `C3_ESCAPE`**: escape, 3-stage directional sequence. ✓ nothing · ✗ device_integrity −20, suspicion +10.

**Exit: resolve `courier_fate`**

| `courier_plan` | QTE ✓ | QTE ✗ |
|---|---|---|
| `leave_alone` | `safe` | `safe` (he was already gone) |
| `leave_together` | `safe` | `injured` (he's hurt covering your escape) |
| `stay` | `lost` | `lost` |

Then: records += `alamo`. If `courier_fate=lost`, add a memorial entry to the journal.

### M — Spring 1836 Montage

**M1 Declaration, card only, shown as a dated flashback:** "Meanwhile — March 2, 1836, Washington-on-the-Brazos." It plays *after* the Alamo chapter, but the card clearly says it happened **four days before** the Alamo fell, while the siege was still going on. Nobody in the scene treats it as fresh news. records += `declaration`. Then come Goliad (Mar 27) and the Runaway Scrape, in date order.

**M2 Goliad (Mar 27), card only, PG-level aftermath:** records += `goliad`. **Rowan only:** "Listen to the hidden survivor" (Yes/No): Yes → records += `goliad_testimony`.

**M3 Runaway Scrape: Choice `C4_AID`** "Who do you help?" (timeout → Y). If `shelter_available`, the stuck wagon belongs to the Treviños.

| Btn | Option | Effects | QTE |
|---|---|---|---|
| A | Free the stuck wagon | `montage_choice=wagon` | C4_WAGON, then C4_CROSSING |
| A *(Morgan)* | Lift the wheel yourself | same as A, but ✗ causes no device damage | C4_WAGON, then C4_CROSSING |
| B | Help the wounded | `montage_choice=wounded`, supplies −1 (if any), suspicion −5. If `courier_fate=injured`: Jonah is among the wounded, courier_trust +1 | C4_CROSSING |
| X | Find another crossing (use the device's map) | `montage_choice=crossing`, timeline_risk +10. Everyone crosses safely. | none |
| Y | Continue on | `montage_choice=leave`; if `shelter_available`, family_trust −1 | C4_CROSSING |

**Jonah callback:** if `courier_fate=safe`, he's among the people on the road and greets you (dialogue only). If `injured`, he's among the wounded (see B).

- **QTE `C4_WAGON`**: physical, alternating rhythm, 10 s. ✓ supplies +1, suspicion −5, family_trust +1 if `shelter_available` · ✗ supplies −1, device_integrity −10.
- **QTE `C4_CROSSING`**: physical, alternating rhythm, 12 s. ✓ nothing · ✗ supplies −1, device_integrity −15.

**Exit:** records += `runaway_scrape`.

### S1 — Houston's Army (camp, mid-April 1836)

**Entry:** `suspicion ≥ 70` → **interrogation variant** (Captain Reed questions you before anything else). If `device_exposed`, Reed has heard about the glowing watch (dialogue only).

**Repair moment** (shown only if supplies ≥1 and device_integrity < 60): "Use supplies to fix the Chrono-Compass?" Yes → supplies −1, device_integrity +25.

**Choice `C5_CLAIM`** "You seem to know a lot about their movements." (timeout → B)

| Btn | Option | Effects |
|---|---|---|
| A | Claim local knowledge | **Credible** if `family_trust ≥ 1` (Josefa vouches) **or** (`cover_identity=louisiana` and suspicion < 70): `knowledge_claim=credible`, suspicion −10, intel=true. Otherwise `doubted`, suspicion +10. |
| B | Admit it's a guess | `knowledge_claim=doubted`, suspicion +5 |
| B *(Ellis)* | Talk your way past the sentry | QTE S_TRICK: ✓ `credible`, intel=true · ✗ `doubted`, suspicion +15 |
| X | Ask about their plans | `knowledge_claim=doubted` |
| Y | Reveal what you know | `knowledge_claim=exposed`, suspicion +20, timeline_risk +25, intel=true |

**QTE `S_RECON`** (everyone): stealth, move/freeze, 15 s. ✓ intel=true · ✗ suspicion +10, device_integrity −10.

### S2 — Eighteen Minutes (San Jacinto, Apr 21 1836)

**Entry:**
- `companion` = `courier` if `courier_fate ∈ {safe, injured}`; else `tomas` if `family_trust ≥ 1`; else `will`.
- `return_window = device_integrity > 0`
- Battle card: records += `san_jacinto`

**Choice `C6_FINAL`** "What will you do?" (the window opens just as your companion is in danger) (timeout → B)

| Btn | Option | Effects |
|---|---|---|
| A | Help your companion | QTE S_HELP: ✓ companion_saved=true · ✗ companion_saved=false (others pull them to safety). Extraction +1 difficulty either way. |
| A *(Morgan)* | Shield them | same as A, wider window |
| B | Leave immediately | companion_saved=false. Extraction −1 difficulty. |
| X | Hide them and activate | companion_saved=true, `exposeDevice` |
| Y | Give them the device | companion_saved=true, return_window=false, `extraction_result=fail` (skip the QTE) |

**QTE `S_EXTRACT`** (if `return_window`): escape, multi-stage directional + timed press.
Difficulty = 2, +1 if `final_choice=help`, −1 if `leave`, −1 if `intel`, +1 if device_integrity < 40, clamped to 1–4. Stages = difficulty + 1.
✓ `extraction_result=success` · ✗ use a recovery if one is left (retry at −1 difficulty); otherwise `fail`.
If `return_window=false` → `extraction_result=fail`.

---

### Demo — bridge and snapshot

In demo mode, after C3 the player sees three short bridge cards: "Béxar, Dec 1835" (shown *before* the Alamo by date, as a flashback), "Spring 1836" (Declaration flashback, Goliad, Runaway Scrape) and "Houston's Army". Then the engine applies this **snapshot** before entering S2. It overwrites only these values; everything the player actually earned (P0, C1, C3) is kept.

| Variable | Demo value | Why |
|---|---|---|
| `family_trust` | 0 | The player never met the Treviños |
| `shelter_available` | false | " |
| `bexar_choice` | `unset` | Epilogues fall back to companion-based lines |
| `montage_choice` | `unset` | " |
| `knowledge_claim` | `unset` | S2 doesn't read it; only `intel` matters |
| `intel` | false | No recon in demo |
| `supplies` | unchanged | |
| `device_integrity` | max(current, 40) | Keeps demo extraction fair |
| `historical_records` | += `bexar`, `declaration`, `goliad`, `runaway_scrape` | Bridge cards count as witnessed |

Result: the companion can only be `courier` (if Jonah left) or `will` (met for the first time in S2). **Never Tomás**, because the player never met him. No scene in the demo refers to Béxar, the Scrape or the camp, except through the bridge cards.

## 6. Read / write matrix (the at-a-glance view)

W = written, R = read (condition or callback), — = untouched

| Variable | P0 | C1 | C2 | C3 | Montage | S1 Camp | S2 Final | Ending |
|---|---|---|---|---|---|---|---|---|
| `run_mode` | — | — | — | — | — | — | R W | — |
| `character_id` | R | R | R | R | R | R | R | R |
| `suspicion` | W | W | W | R W | W | R W | W | — |
| `timeline_risk` | W | — | — | W | W | W | W | **R** |
| `device_integrity` | — | W | W | W | W | R W | R | — |
| `family_trust` | — | — | R W | — | R W | R | R | — |
| `courier_trust` | — | — | — | W | W | — | — | R |
| `supplies` | — | W | R W | — | R W | R W | — | — |
| `recoveries_left` | R W | R W | R W | R W | — | R W | R W | — |
| `cover_identity` | W | R | — | — | — | R | — | — |
| `device_exposed` | W | R | — | — | — | R | W | R |
| `gonzales_choice` | — | W | R | R | — | — | — | — |
| `bexar_choice` | — | — | W | — | — | — | — | R |
| `shelter_available` | — | — | W | — | R | — | — | — |
| `courier_plan` | — | — | — | W R | — | — | — | — |
| `courier_fate` | — | — | — | W | R | — | R | R |
| `montage_choice` | — | — | — | — | W | — | — | R |
| `knowledge_claim` | — | — | — | — | — | W | — | R |
| `intel` | — | — | — | — | — | W | R | — |
| `companion` | — | — | — | — | — | — | W | R |
| `final_choice` | — | — | — | — | — | — | W | R |
| `companion_saved` | — | — | — | — | — | — | W | **R** |
| `return_window` | — | — | — | — | — | — | W R | R |
| `extraction_result` | — | — | — | — | — | — | W | **R** |
| `historical_records` | — | W | W | W | W | — | W | R |

Delayed callbacks (spec: "every decision has a traceable consequence"):

| Decision | Paid off in |
|---|---|
| P0 cover story | Gonzales dialogue; San Jacinto credibility |
| Gonzales role | Béxar entry; Jonah at the Alamo |
| Béxar family | Scrape wagon; Josefa vouches; Tomás as companion |
| Alamo courier | Seen on the Scrape road or among the wounded; companion; memorial |
| Scrape aid | Supplies for the repair; family trust |
| Knowledge claim | Intel → easier extraction; Time Ripples |
| Final choice | Ending family |

---

## 7. Endings

Checked in this order (first match wins):

1. **Stranded**: `extraction_result ≠ success`
2. **Paradox**: `timeline_risk ≥ 70`
3. **Protector**: `companion_saved = true`
4. **Observer**: otherwise

Recap screen explains it in kid language, e.g. Paradox: "You told people about the future too many times. Time noticed."

**Character epilogue** (one line or card per character × ending = 12):
- Rowan: what she noticed (uses `goliad_testimony`, `courier_trust`)
- Morgan: whom she protected (uses `companion`, `bexar_choice`, `montage_choice`)
- Ellis: what she outsmarted (uses `bexar_choice=misdirect`, S_TRICK result, recovery used)

## 8. Balance check (current numbers)

| Meter | How high / low it can go | Notes |
|---|---|---|
| Time Ripples | max 110 → clamped 100 | Paradox takes about 3 "future" actions (e.g. truth 25 + warn 20 + reveal 25 = 70). It can't happen by accident. |
| Eyes on You | 0 – 100 | 70+ needs several risky choices plus failed sneaks |
| Device Power | 80 → 0 only if almost every QTE fails and you skip the repair | So Stranded-by-damage is rare; Stranded mostly comes from a failed extraction or Give Device |
| Endings per character | All 4 reachable for all 3 | Must be confirmed by automated graph tests |

Decisions per run: 7 main + repair + Rowan's Goliad prompt = 8–9 (spec target 8–12). QTEs per run: 6–8. Optional: add 1–2 small-talk choices per chapter that only change trust by ±1.

**8–12 min demo path:** `run_mode=demo`. Skip the tutorial → P0 → C1 → C3 → *bridge cards* → S2. See the Demo snapshot below.

## 9. What the player sees (HUD & journal)

- **During play:** no meters on screen, only toasts after effects ("🌀 Time ripples", "Josefa will remember that.").
- **DEVICE button → Chrono-Compass screen:**
  - 👁 Eyes on You: Unnoticed (0–39) · Watched (40–69) · Suspected (70+)
  - 🌀 Time Ripples: Calm (0–39) · Rippling (40–69) · Breaking (70+)
  - 🔋 Device Power: %
  - 🎒 Supplies: 0–3 icons
- **Journal (field notes):** People page (Josefa & Tomás, Jonah: Distrusts / Wary / Neutral / Friendly / Trusts), Archive x / 9 with **Fact** / **Dramatized** labels, memorial entry if needed.
- **End recap:** ending card, character epilogue, your key choices, archive count.

## 10. Initial state (copy into `src/core/state.ts` later)

```ts
export const initialRunState = (characterId: CharacterId, runMode: RunMode = 'full'): RunState => ({
  character_id: characterId,
  run_mode: runMode,
  suspicion: 10,
  timeline_risk: 0,
  device_integrity: 80,
  family_trust: 0,
  courier_trust: 0,
  supplies: 1,
  recoveries_left: CHARACTERS[characterId].extraRecoveries, // ellis: 1, others: 0
  cover_identity: 'unset',
  device_exposed: false,
  gonzales_choice: 'unset',
  bexar_choice: 'unset',
  shelter_available: false,
  courier_plan: 'unset',
  courier_fate: 'unknown',
  montage_choice: 'unset',
  knowledge_claim: 'unset',
  intel: false,
  companion: 'none',
  final_choice: 'unset',
  companion_saved: false,
  return_window: false,
  extraction_result: 'unset',
  ending: 'unset',
  historical_records: [],
});
```

## 11. Automated narrative validation (must pass before content is "done")

Run on every build against the real content data. **Reachability is proved by playing legal sequences of choices and QTE results**, never by setting variables by hand.

1. Every choice, timeout and QTE result points at a node that exists.
2. Every character (Rowan, Morgan, Ellis) can reach all four endings.
3. Every ending can be explained from `choiceLog` and `qteLog` (the recap generator produces a reason for each).
4. No scene references a character or event the player hasn't met, in both full and demo mode (e.g. no Tomás in demo, no Jonah dialogue when `courier_fate=lost`).
5. No branch produces an impossible state (meters in range, `courier_fate` consistent with `courier_plan`, `companion_saved` only if a companion exists, `ending` set exactly once).
6. Every QTE failure leads to a node that lets the story continue.
7. The full path and the demo path both complete for every character, within the time budget.
8. The story graph (`.dot` / `.svg`) is generated from the same data and attached to the build.
