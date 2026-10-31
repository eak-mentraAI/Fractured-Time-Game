# Texas: Fractured Time — Build TODO

Source assets: [spec v0.3](docs/design/Texas_Fractured_Time_Game_Spec_v0.3.docx), [branching graph v0.3](docs/design/Texas_Fractured_Time_Branching_Graph_v0.3.pdf), and the concept boards in `art/reference/` (`ref_character_select_board.png`, `ref_style_storyboard.png`).

**Target (spec §16):** 20–30 min complete run, 8–12 min demo path, iPad Safari PWA (landscape), fully offline, gamepad + touch. 8–12 decisions, 4–6 QTEs, 3 playable girls (Rowan / Morgan / Ellis), 4 ending families × 3 character epilogues.

**Stack (spec §8):** TypeScript + Vite + Phaser 3, DOM/CSS overlay for dialogue/menus, service worker precache, IndexedDB saves. Narrative engine must not import Phaser.

---

## 0. Decisions

**Resolved (31 Oct 2026)**
- [x] Spec v0.3 is authoritative. `art/reference/ref_style_storyboard.png` is an art-style reference only.
- [x] Chapter flow follows spec v0.3, with the Declaration shown as a dated flashback card in the Spring 1836 montage.
- [x] Ending rules and every state variable are locked in [docs/GAME_STATE.md](docs/GAME_STATE.md), the gameplay rules contract. Paradox = Time Ripples ≥ 70.
- [x] Art direction, AI prompts and the full art list are in [ART_GUIDE.md](ART_GUIDE.md) (45 MVP + 36 optional images).
- [x] Controller: a standard Bluetooth **Xbox Wireless** or **PlayStation DualShock 4 / DualSense** controller instead of an arcade encoder. Safari maps both to the Gamepad API "standard" layout. Show Xbox A/B/X/Y glyphs by default, and PlayStation shapes when `gamepad.id` matches DualShock/DualSense. Touch stays as the fallback.

**Still open**
- [ ] Target iPad model and iPadOS version; pair the controller and test it in Safari **and** as an installed home-screen app (M0).
- [ ] Who runs the AI art generation, and which tool (affects reference-image support and image sizes).
- [ ] Voiceover vs. text-only (assuming text + captions).
- [ ] Teacher / historian who reviews history anchors and the PG tone.

## 1. Project setup

- [x] `git init`, `.gitignore`, folder layout (see README), concept files moved to `docs/design/` and `art/reference/`
- [ ] Vite + TypeScript (strict) + Phaser 3 scaffold, ESLint/Prettier, Vitest
- [ ] Folder layout per spec §8: `src/content`, `src/core`, `src/systems/input`, `src/systems/qte`, `src/presentation`, `src/storage`, `src/offline`, `tests/`
- [ ] Lint rule / test that blocks `core/` from importing `phaser` or the DOM
- [ ] Landscape-first layout with a fixed design resolution (e.g. 2048×1536 / 4:3 iPad), letterboxing, safe-area insets
- [ ] Bundle local fonts: one hand-lettered display face + one highly legible face for timed prompts (no Google Fonts at runtime)
- [ ] Debug overlay: current node, state values, jump-to-node, set-state (dev builds only)

## 2. Narrative core (`core/`, pure TS, fully unit-tested)

- [ ] Content schemas (zod or TS types + JSON Schema): Node, Choice, QTE, HistoricalAnchor, Character, Ending, per spec §9
- [ ] `GameState` type + initial state (all vars from §6 plus `characterId`, `tutorialCompleted`, `visitedNodes`, `choiceLog`)
- [ ] Condition/predicate language (e.g. `{ var: "suspicion", gte: 70 }`, `{ characterId: "rowan" }`, `all/any/not`)
- [ ] Effect language (add/set/clamp/addToSet), with clamping to declared ranges
- [ ] Pure reducer: `(state, event) → state` for choice / timeout / QTE success / fail
- [ ] Transition resolver + deterministic outcomes (same state + input = same result)
- [ ] `CharacterCatalog` (immutable data) + `CharacterAdvantageResolver` (timing multipliers, extra recovery, detection window, all data-driven)
- [ ] `EndingResolver` + `EndingEpilogueResolver` (4 families × 3 characters)
- [ ] **Build-time content validator + graph tests:** implement all 8 checks in [GAME_STATE.md §11](docs/GAME_STATE.md). Reachability is proved by walking legal choice and QTE sequences, never by setting state by hand.
- [ ] Demo mode: `run_mode`, bridge cards, demo snapshot (GAME_STATE.md, Demo section)
- [ ] Generate the story graph (`.dot`/`.svg`) from content data on every build. It replaces the hand-made PDF as the living graph.

## 3. Input system (`systems/input/`)

- [ ] Standard-mapping defaults: A/Cross=CONFIRM (0), B/Circle=EVADE (1), X/Square=INTERACT (2), Y/Triangle=DEVICE (3), Menu/Options=PAUSE (9), D-pad 12–15 + left stick=NAV. Choice slots A/B/X/Y = buttons 0/1/2/3.
- [ ] "Press any button to connect" prompt (Safari only exposes a gamepad after a button press)
- [ ] Gamepad API polling loop → semantic actions `NAV_UP/DOWN/LEFT/RIGHT, CONFIRM, EVADE, INTERACT, DEVICE, PAUSE`
- [ ] Edge-triggered presses, deadzone for sticks/D-pad, monotonic `performance.now()` timing
- [ ] Calibration screen ("press the button you want for CONFIRM…") + remapping, persisted
- [ ] Keyboard mapping (desktop) and on-screen touch controls with parity
- [ ] Connect/disconnect handling; auto-pause on disconnect
- [ ] Glyph component that shows the right label for the current device

## 4. QTE system (`systems/qte/`)

- [ ] Frame-independent scheduler + timer bar (the red bar in the storyboard)
- [ ] Patterns: directional sequence, timed single press, alternating rhythm (mash), stealth move/freeze, timed decision
- [ ] Difficulty params + character modifiers (Morgan wider physical window, Rowan longer detection window, Ellis extra recovery)
- [ ] Accessibility: timer multiplier, timers off, hold-to-confirm alternative, auto-succeed option
- [ ] Success/fail dispatch to the reducer; failure leads to story outcomes, never a hard game over

## 5. Presentation (`presentation/`)

- [ ] Phaser scenes: Boot/Preload, Title, CharacterSelect, Confirm, Tutorial, StoryScene (generic node player), MontageCard, Ending, Archive/Journal
- [ ] Layered 2.5D tableau renderer: bg/mid/fg layers, slow authored camera pans, parallax, ambient loops (smoke, wind, lantern flicker)
- [ ] Paper texture + vignette post-pass; ink-wipe or page-turn transitions between panels
- [ ] DOM overlay: dialogue box, speaker name, timed choice list (4 options A/B/X/Y style), skip/fast-forward seen text
- [ ] Character portraits with expression swaps (neutral / smile / concerned, as in the selection board)
- [ ] Chapter title cards with date and place (hand-lettered style)
- [ ] Journal/"field notes" UI: historical records collected, fact vs. dramatization labels
- [ ] Pause menu, settings (volume categories, text size, contrast, reduced motion, timers), save/load
- [ ] Recap screen at the end: key choices made + ending + character epilogue

## 6. Persistence (`storage/`)

- [ ] IndexedDB save slots with `schemaVersion`, `contentVersion`, `currentNodeId`, `state`, `visitedNodes`, `choiceLog`, `timestamp`
- [ ] Atomic write + last-good backup; autosave at node boundaries, chapter exits, `visibilitychange`
- [ ] Save migrations scaffold
- [ ] JSON export/import (iPad can evict storage)

## 7. Offline / PWA (`offline/`)

- [ ] Web app manifest (landscape, standalone, icons, splash)
- [ ] Service worker precaching a versioned asset manifest generated at build time (Workbox or hand-rolled)
- [ ] "Ready to play offline" only after verifying every mandatory asset is in cache
- [ ] Controlled update flow (never swap assets mid-scene)
- [ ] Audio unlock after first user gesture (Safari)
- [ ] Static HTTPS hosting for install (GitHub Pages / Netlify / Cloudflare Pages)

## 8. Content authoring (one data file per beat)

Follow the v0.3 flow: Title → Select → Tutorial → Fracture → Gonzales → Béxar → Alamo → Montage → San Jacinto → Ending.

- [ ] **Tutorial** (≤90 s, skippable on replay): move, choose, one practice QTE
- [ ] **P0 Fracture:** cover-identity choice (Louisiana / confused / run / truth), detection-escape QTE
- [ ] **C1 Gonzales, Oct 2 1835:** help cannon / supplies / hide & observe / approach Mexican troops; cannon or escape QTE
- [ ] **C2 Béxar, Dec 1835:** escort family / warn soldiers / give supplies / refuse; street-stealth QTE; sets `family_trust`, `shelter_available`
- [ ] **C3 Alamo, Feb 23–Mar 6 1836:** courier choice (emotional centerpiece); Rowan-specific empathy option; siege escape QTE; sets `courier_fate`
- [ ] **Historical montage, Mar 1836:** Declaration (dated flashback card), Goliad (aftermath), Runaway Scrape; one pivotal civilian choice + river-crossing QTE; Morgan-specific wagon option
- [ ] **C5 Road to San Jacinto:** knowledge claim (credible / doubted / exposed); recon stealth QTE; Ellis-specific talk-past-guard option
- [ ] **C6 Eighteen Minutes, Apr 21 1836:** companion choice (help / leave / hide & activate / give device); multi-stage extraction QTE
- [ ] **Endings:** Observer / Protector / Stranded / Paradox illustrated cards + 12 character epilogue lines
- [ ] Delayed callbacks: saved courier or helped family reappears later (at least 2)
- [ ] Each character: ≥2 visibly different dialogue/interaction moments (acceptance gate #3)
- [ ] Historical anchor entries: date, place, summary, sources, review status, "fictionalized" flag
- [ ] Mark a short 8–12 min demo path through the graph

## 9. Art & audio production

- [x] Style guide, character descriptions and AI prompts → [ART_GUIDE.md](ART_GUIDE.md)
- [ ] Generate the 45 MVP images in ART_GUIDE.md §8A (characters first, using the locked references in `art/reference/`); the 36 optional images come after
- [ ] Asset spec: resolution, layer naming, export format (WebP/AVIF + PNG fallback), texture-memory budget per scene
- [ ] UI kit: stamped field-note panels, choice cards, timer bar, button glyphs, chapter cards
- [ ] Audio: sparse score cues, ambient beds per location, UI confirm/tension SFX, all local (AAC/MP3 for Safari)

## 10. QA & acceptance (spec §13 / §19)

- [ ] Full run ≤30 min in normal mode; all 3 characters start to finish
- [ ] All 4 endings reachable for each character (automated + manual)
- [ ] Offline test: install → Airplane Mode → cold launch → play → save → relaunch → restore
- [ ] Controller + touch tested on the target iPad in standalone mode
- [ ] Accessibility: every timed event completable with accessible settings
- [ ] Performance: steady frame pacing during QTEs, memory within budget on the target iPad
- [ ] Historical review sign-off; archive clearly separates fact from dramatization
- [ ] Classroom playtest + tuning (suspicion and risk thresholds, QTE difficulty)

---

## Suggested build order (maps to spec milestones)

1. **M0:** Setup (§1) → input prototype on the real iPad + controller (§3) → offline install proof with one placeholder scene (§7)
2. **M1 vertical slice:** core engine (§2) + QTE (§4) + StoryScene/dialogue (§5) + saves (§6) → polished Character Select + Tutorial + Fracture + Gonzales (~5 min, 2 branches, 3 QTE types)
3. **M2 narrative alpha:** author all remaining beats with placeholder art; endings and graph tests green
4. **M3 art & history beta:** real art and audio, historical review, accessibility pass
5. **M4 release candidate:** offline regression, controller matrix, performance on device, classroom playtest
