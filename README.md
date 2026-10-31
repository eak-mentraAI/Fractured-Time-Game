# Texas: Fractured Time

A hand-illustrated, choice-driven adventure through the Texas Revolution (1835–1836). You play Rowan, Morgan or Ellis, three girls stranded in the past who have to witness history, stay hidden and find a way home.

- **Platform:** offline iPad Safari PWA (landscape), plus desktop browsers
- **Controls:** Xbox or PlayStation Bluetooth controller, keyboard or touch
- **Length:** 20–30 minute full run, 8–12 minute demo
- **Stack (planned):** TypeScript, Vite, Phaser 3, with a DOM overlay for dialogue and menus

## Where things live

```
├── README.md            ← you are here
├── TODO.md              ← build checklist and open decisions
├── ART_GUIDE.md         ← how to make the art with AI (prompts + checklist)
├── docs/
│   ├── GAME_STATE.md    ← gameplay rules contract: variables, choices, QTEs, endings
│   └── design/          ← original spec (v0.3) and branching graph PDF
└── art/                 ← all artwork (see art/README.md)
    ├── reference/       ← 🔒 locked, approved references; don't edit
    ├── drafts/          ← scratch space for AI tries (not saved to git)
    ├── characters/      ← finished character art
    ├── props/
    ├── scenes/
    ├── foreground/
    └── ui/
```

Game code (`src/`, `tests/`, `public/`) will be added when development starts. See TODO.md §1.

## Which document wins?

| Document | Owns |
|---|---|
| `docs/design/…Game_Spec_v0.3.docx` | Vision, architecture, art direction, overall experience |
| `docs/GAME_STATE.md` | Variables, conditions, effects, QTE rules, ending resolution |
| Story graph | Will be generated from the game's content data (the v0.3 PDF is the design reference until then) |
| `ART_GUIDE.md` + `art/reference/` | How everything looks |
