# 🎨 Art Folder

Every picture for the game lives here. Full instructions and prompts are in [`../ART_GUIDE.md`](../ART_GUIDE.md).

## The path of a picture

```
 1. Make it         2. Pick the best        3. Save it here            4. Tick it off
 (AI tool)    →     try in drafts/    →     with the right name   →    in ART_GUIDE.md §8
```

1. **Make it** with your AI tool: copy the prompt from [`../ART_PROMPTS.md`](../ART_PROMPTS.md) and upload the reference it lists.
2. **Drop every try into `drafts/`.** Name it anything. This folder is your messy desk and is **not** uploaded to GitHub.
3. **Pick the best one**, check it with the checklist at the end of ART_GUIDE.md, then **save it into the right folder** with the exact file name from the checklist.
4. **Tick the box** ☐ → ✅ in ART_GUIDE.md §8.

## Which folder?

| Folder | What goes in it | ID starts with | Example |
|---|---|---|---|
| `reference/` | 🔒 **Approved references only.** Don't add, change or delete. | `ref_` | `ref_rowan.png` |
| `drafts/` | All your tries, messy and unfinished | anything | `rowan_try3.png` |
| `characters/` | Girls, supporting characters, select panels, expression sheets | R, M, E, C | `r01_rowan_select.png` |
| `props/` | The Chrono-Compass, pendants, flag, letter… | D | `d02_compass_cracked.png` |
| `scenes/` | Backgrounds and endings | S, P, G, B, A, N, J, X | `g01_gonzales_town.png` |
| `foreground/` | Grass, branches and smoke layers that go in front of scenes | F | `f01_grass.png` |
| `ui/` | Paper textures and small icons | U | `u06_icon_deer.png` |

## File name rules

- **Lowercase only, underscores instead of spaces:** `g01_gonzales_town.png` ✅ · `G-01 Gonzales Town.PNG` ❌
- **Start with the ID** from the checklist (drop the dash: `G-01` → `g01`).
- **PNG**, biggest size your tool makes.
- Expression sheets: also save the 4 cropped squares as `r03_rowan_expressions_neutral.png`, `_happy`, `_worried`, `_determined`.

## Replacing a picture

Made a better version? **Save over the old file with the same name.** Git remembers the old one, so nothing is lost.

## Saving to GitHub

When you've finished a few pictures, ask a grown-up or Claude to commit them, or use GitHub Desktop: write a short note like `Add Rowan select panel and body` and press **Commit**, then **Push**.
