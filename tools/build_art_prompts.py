#!/usr/bin/env python3
"""Build ART_PROMPTS.md: one fully assembled, copy-paste prompt per picture.

The reusable blocks (style spine, avoid list, character blocks, select-panel
compositions, format blocks) are read from ART_GUIDE.md, so editing a block
there and re-running this script updates every prompt:

    python3 tools/build_art_prompts.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "ART_GUIDE.md"
OUT = ROOT / "ART_PROMPTS.md"

# ---------------------------------------------------------------------------
# 1. Pull the reusable blocks out of ART_GUIDE.md
# ---------------------------------------------------------------------------

def load_blocks():
    text = GUIDE.read_text(encoding="utf-8")
    blocks, formats = {}, {}
    last_label = None
    for m in re.finditer(r"(\*\*(F\d):[^\n]*\*\*\n)?```[a-z]*\n(.*?)\n```", text, re.S):
        fmt, body = m.group(2), m.group(3).strip()
        if fmt:
            formats[fmt] = body
            continue
        starts = {
            "spine": "Cinematic storybook illustration",
            "avoid": "Do not include:",
            "rowan": "ROWAN (", "morgan": "MORGAN (", "ellis": "ELLIS (",
            "jonah": "JONAH:", "josefa": "JOSEFA:", "tomas": "TOMÁS:",
            "will": "WILL:", "reed": "CAPTAIN REED:", "ortiz": "TENIENTE ORTIZ:",
            "compass": "THE CHRONO-COMPASS:", "window": "THE RETURN WINDOW:",
        }
        for key, prefix in starts.items():
            if body.startswith(prefix):
                blocks[key] = body
        if body.startswith("COMPOSITION"):
            for who in ("Rowan", "Morgan", "Ellis"):
                if f"): {who}," in body or f"): {who} " in body:
                    blocks[f"comp_{who.lower()}"] = body
    needed = ["spine", "avoid", "rowan", "morgan", "ellis", "jonah", "josefa", "tomas",
              "will", "reed", "ortiz", "compass", "window",
              "comp_rowan", "comp_morgan", "comp_ellis"]
    missing = [k for k in needed if k not in blocks] + [f"F{i}" for i in range(1, 9) if f"F{i}" not in formats]
    if missing:
        raise SystemExit(f"Could not find these blocks in ART_GUIDE.md: {missing}")
    return blocks, formats


def fill(block, *values):
    """Replace each [bracketed blank] in order with the given values."""
    blanks = re.findall(r"\[[^\]]*\]", block)
    if len(blanks) != len(values):
        raise ValueError(f"Block has {len(blanks)} blanks, got {len(values)} values:\n{block}")
    for blank, value in zip(blanks, values):
        block = block.replace(blank, value, 1)
    return block


# ---------------------------------------------------------------------------
# 2. Picture definitions
# ---------------------------------------------------------------------------

SHAPES = {
    "F1": "Landscape 3:2", "F2": "Portrait 2:3", "F3": "Square 1:1", "F4": "Square 1:1",
    "F5": "Landscape 3:2", "F6": "Landscape 3:2", "F7": "Square 1:1", "F8": "Portrait 4:5 (or 2:3)",
}

REF = {
    "rowan": "art/reference/ref_rowan.png",
    "morgan": "art/reference/ref_morgan.png",
    "ellis": "art/reference/ref_ellis.png",
    "board": "art/reference/ref_character_select_board.png",
    "story": "art/reference/ref_style_storyboard.png",
}

EXPRESSIONS = {
    "rowan": ["neutral (soft, listening)", "happy (shy, gentle smile)",
              "worried (eyes wide, hand at her pendant)", "determined (quiet, firm gaze)"],
    "morgan": ["neutral (calm, steady)", "happy (big open grin)",
               "worried (jaw tight, brows down)", "determined (fierce, chin up)"],
    "ellis": ["neutral (thinking, one eyebrow slightly up)", "happy (sly half-smile)",
              "worried (biting her lip, glancing away)", "determined (narrowed eyes, small smirk)"],
    "jonah": ["neutral", "hopeful", "scared", "sad"],
    "josefa": ["neutral", "grateful", "worried", "stern"],
    "tomas": ["neutral", "happy", "scared", "brave"],
    "will": ["neutral", "nervous", "relieved", "brave"],
    "reed": ["stern", "doubtful", "suspicious", "impressed"],
}

# Location blocks from ART_GUIDE.md §7
LOC = {
    "modern": "a quiet research site at night near old Spanish mission ruins, portable lights and equipment cases, the modern San Antonio skyline glowing far away",
    "gonzales": "the small frontier town of Gonzales on the Guadalupe River, log cabins and simple wooden houses, dirt roads, autumn grass",
    "bexar": "the streets of San Antonio de Béxar in December 1835, flat-roofed stone and adobe houses, a dusty plaza, the stone church of San Fernando with its dome",
    "alamo": "the old Alamo mission in winter 1836, a roofless weathered stone church with a flat broken top edge, long adobe walls around a big dusty courtyard, wooden cannon platforms",
    "washington": "an unfinished wooden building with cloth covering the window holes, cold and drafty, men in frock coats around rough wooden tables with papers and ink",
    "goliad": "the old stone fort Presidio La Bahía at Goliad with its small stone chapel and bell tower",
    "scrape": "muddy roads in heavy rain, families fleeing east on foot, in ox carts and covered wagons, swollen brown rivers",
    "sanjacinto": "open prairie beside Buffalo Bayou with live oak trees and marshy grass, spring wildflowers, a Mexican army camp behind a low barricade of packs and saddles",
}

NO_HUMP = "The top of the church front is flat and broken, no curved parapet."

# Each picture:
#   id, title, mvp, file, fmt, fmt_fill (values for the format's blanks) or fmt_text (custom),
#   chars: [(key, action)], refs: [paths], scene: dict or subject: str, extra: str,
#   modern: allow modern objects, note: shown under the prompt
P = []

def pic(**kw):
    kw.setdefault("chars", [])
    kw.setdefault("refs", [])
    kw.setdefault("fmt_fill", ())
    P.append(kw)


def scene(where, who, before, now, after, focal, camera, mood):
    return dict(where=where, who=who, story=f"{before} → {now} → {after}", focal=focal, camera=camera, mood=mood)


# --- A1 Main characters (MVP) ----------------------------------------------
pic(id="R-01", title="Rowan + deer select panel", mvp=True, file="art/characters/r01_rowan_select.png",
    fmt="F8", chars=[("rowan", "looking up and off to the side with quiet curiosity, one hand near her pendant")],
    refs=[REF["rowan"]], comp="comp_rowan",
    extra="A white-tailed deer doe is clearly visible beside her.")
pic(id="R-02", title="Rowan full body", mvp=True, file="art/characters/r02_rowan_body.png",
    fmt="F2", fmt_fill=("full body, standing", "left"),
    chars=[("rowan", "standing still and at ease, slightly turned, one hand holding her pendant, head tilted as if listening to something far away")],
    refs=[REF["rowan"]])
pic(id="R-03", title="Rowan expressions", mvp=True, file="art/characters/r03_rowan_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["rowan"]),
    chars=[("rowan", "shown head and shoulders in four different expressions")],
    refs=[REF["rowan"]], expr=True)
pic(id="M-01", title="Morgan + horse select panel", mvp=True, file="art/characters/m01_morgan_select.png",
    fmt="F8", chars=[("morgan", "her gloved hand resting gently on her horse's cheek, looking off into the distance with calm confidence")],
    refs=[REF["morgan"]], comp="comp_morgan",
    extra="A chestnut horse with a white blaze is clearly visible beside her.")
pic(id="M-02", title="Morgan full body", mvp=True, file="art/characters/m02_morgan_body.png",
    fmt="F2", fmt_fill=("full body, standing", "right"),
    chars=[("morgan", "standing with her feet planted wide and shoulders square, chin up, thumbs hooked in her belt, ready to step in and help")],
    refs=[REF["morgan"]])
pic(id="M-03", title="Morgan expressions", mvp=True, file="art/characters/m03_morgan_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["morgan"]),
    chars=[("morgan", "shown head and shoulders in four different expressions")],
    refs=[REF["morgan"]], expr=True)
pic(id="E-01", title="Ellis + fox select panel", mvp=True, file="art/characters/e01_ellis_select.png",
    fmt="F8", chars=[("ellis", "sitting on old stone ruins, forearm resting on her knee, glancing sideways with a thoughtful look")],
    refs=[REF["ellis"]], comp="comp_ellis",
    extra="A gray fox is clearly visible beside her.")
pic(id="E-02", title="Ellis full body", mvp=True, file="art/characters/e02_ellis_body.png",
    fmt="F2", fmt_fill=("full body, crouching low on one knee", "left"),
    chars=[("ellis", "crouched low on one knee, glancing sideways with a sly half-smile, one hand pointing off to the side as if she just spotted another way out")],
    refs=[REF["ellis"]])
pic(id="E-03", title="Ellis expressions", mvp=True, file="art/characters/e03_ellis_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["ellis"]),
    chars=[("ellis", "shown head and shoulders in four different expressions")],
    refs=[REF["ellis"]], expr=True)

# --- A2 Supporting characters (MVP) ----------------------------------------
pic(id="C-01", title="Jonah full body", mvp=True, file="art/characters/c01_jonah_body.png",
    fmt="F2", fmt_fill=("full body, standing", "left"), pronoun="his",
    chars=[("jonah", "standing with both hands clutching his bag strap, glancing nervously over his shoulder")],
    refs=[REF["story"] + " (style only)"])
pic(id="C-02", title="Jonah expressions", mvp=True, file="art/characters/c02_jonah_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["jonah"]),
    chars=[("jonah", "shown head and shoulders in four different expressions")],
    refs=["art/characters/c01_jonah_body.png"], expr=True)
pic(id="C-03", title="Josefa full body", mvp=True, file="art/characters/c03_josefa_body.png",
    fmt="F2", fmt_fill=("full body, standing", "right"),
    chars=[("josefa", "standing protectively with one arm held out to the side as if keeping a child behind her, looking toward danger with calm determination")],
    refs=[REF["story"] + " (style only)"])
pic(id="C-05", title="Tomás full body", mvp=True, file="art/characters/c05_tomas_body.png",
    fmt="F2", fmt_fill=("full body, standing", "left"), pronoun="his",
    chars=[("tomas", "standing with his chin up and fists at his sides, trying hard to look brave, hat tipped back")],
    refs=[REF["story"] + " (style only)"])
pic(id="C-07", title="Will full body", mvp=True, file="art/characters/c07_will_body.png",
    fmt="F2", fmt_fill=("full body, standing", "right"), pronoun="his",
    chars=[("will", "standing as tall as he can, holding his too-big rifle awkwardly across his body, with a nervous smile")],
    refs=[REF["story"] + " (style only)"])
pic(id="C-09", title="Captain Reed full body", mvp=True, file="art/characters/c09_reed_body.png",
    fmt="F2", fmt_fill=("full body, standing", "left"), pronoun="his",
    chars=[("reed", "standing with arms crossed, looking down with narrowed eyes as if questioning someone")],
    refs=[REF["story"] + " (style only)"])
pic(id="C-11", title="Teniente Ortiz full body", mvp=True, file="art/characters/c11_ortiz_body.png",
    fmt="F2", fmt_fill=("full body, standing", "right"), pronoun="his",
    chars=[("ortiz", "standing straight and formal, one gloved hand resting on his sword hilt, with a serious but polite expression")],
    refs=[REF["story"] + " (style only)"])

# --- A3 Props & icons (MVP) ------------------------------------------------
pic(id="D-02", title="Chrono-Compass, cracked", mvp=True, file="art/props/d02_compass_cracked.png",
    fmt="F4", compass="cracked",
    subject="The Chrono-Compass lying open on its side, a crack running across the glass face, its blue glow flickering weakly over the tiny gears. No people.")
pic(id="D-03", title="Chrono-Compass in two hands", mvp=True, file="art/props/d03_compass_hands.png",
    fmt="F4", compass="cracked",
    subject="Close-up of two young hands in worn sleeves holding the Chrono-Compass, which is blazing with bright blue-white light, streaks of light spiraling out between the fingers. Only the hands and the device; no faces.")
pic(id="U-01", title="Paper texture", mvp=True, file="art/ui/u01_paper.png",
    fmt="F7", fmt_fill=("warm cream rag paper",),
    subject="Just the paper surface: soft fibers, gentle grain and faint uneven tone. No people, no drawings.")
pic(id="U-06", title="Deer icon", mvp=True, file="art/ui/u06_icon_deer.png",
    fmt="F4", refs=[REF["board"]],
    subject="A small, simple ink-and-wash emblem of a deer's head with antlers, facing forward, like the little emblem next to Rowan's name on the reference board. Bold, clear shape that reads well when tiny. No people.")
pic(id="U-07", title="Horseshoe icon", mvp=True, file="art/ui/u07_icon_horseshoe.png",
    fmt="F4", refs=[REF["board"]],
    subject="A small, simple ink-and-wash emblem of a horseshoe, open end up, like the little emblem next to Morgan's name on the reference board. Bold, clear shape that reads well when tiny. No people.")
pic(id="U-08", title="Fox icon", mvp=True, file="art/ui/u08_icon_fox.png",
    fmt="F4", refs=[REF["board"]],
    subject="A small, simple ink-and-wash emblem of a gray fox's head, facing forward, like the little emblem next to Ellis's name on the reference board. Bold, clear shape that reads well when tiny. No people.")

# --- A4 Scenes (MVP) -------------------------------------------------------
pic(id="S-01", title="Title screen", mvp=True, file="art/scenes/s01_title.png", fmt="F1", refs=[REF["board"]],
    fmt_text="FORMAT: a wide title-screen background with no characters, keeping the left third as calm, open sky where the game's logo will go. Wide landscape composition.",
    scene=scene("the Texas Hill Country in spring, late golden sunset",
                "no people",
                "a long journey is about to begin",
                "the sun sets over rolling hills and old stone mission ruins in the distance",
                "a faint blue shimmer in the sky hints that time is about to crack open",
                "the distant mission ruins glowing in the last sunlight",
                "wide establishing shot, framed by a live oak branch along the top right, a carpet of bluebonnets in the foreground leading the eye toward the ruins",
                "warm golden sunset, hopeful and mysterious"))
pic(id="P-01", title="Modern research site", mvp=True, file="art/scenes/p01_research_site.png", fmt="F1", modern=True,
    scene=scene(f"modern-day San Antonio, Texas, late at night, clear and still: {LOC['modern']}",
                "no main characters; equipment only",
                "a research team has set up a secret experiment",
                "portable lights and equipment cases sit among the old stone mission ruins",
                "a small brass device on a tripod is starting to glow blue",
                "the small glowing brass device on its tripod in the middle of the ruins",
                "wide establishing shot, framed by a crumbling stone archway in the foreground",
                "tense moonlit night, cool indigo shadows and the warm glow of work lights"))
pic(id="P-02", title="The time vortex", mvp=True, file="art/scenes/p02_vortex.png", fmt="F1",
    scene=scene("inside the moment time breaks apart, no place and no time",
                "no people",
                "the experiment has gone wrong",
                "a huge swirling tunnel of blue-white light tears open, pulling in leaves and pieces of stone",
                "everything is about to be pulled through into 1835",
                "the blazing white center of the swirling tunnel",
                "looking straight into the tunnel, ink and watercolor strokes spiraling toward the center",
                "blazing blue-white light against deep indigo darkness, awe and danger"))
pic(id="P-03", title="1835 woods, riders approaching", mvp=True, file="art/scenes/p03_woods_riders.png", fmt="F1",
    scene=scene("thick oak and cedar woods near San Antonio de Béxar, autumn 1835, dawn with mist",
                "no main characters; three riders on horseback in 1830s frontier clothes, slouch hats and long rifles, in the middle distance",
                "a stranger has just appeared out of nowhere, leaving crushed leaves and a fading blue glow in the brush",
                "the riders have spotted something and slow their horses",
                "they are about to search the brush",
                "the lead rider peering through the trees toward the viewer",
                "low hidden view from inside the brush, framed by dark foreground leaves, sunbeams slanting through the mist",
                "cold blue dawn fog with warm shafts of sunlight, tense"))
pic(id="G-01", title="Gonzales town by the river", mvp=True, file="art/scenes/g01_gonzales_town.png", fmt="F1",
    scene=scene(f"early October 1835, late afternoon with a dusty golden sky: {LOC['gonzales']}",
                "no main characters; small groups of settlers in the middle distance",
                "riders have just brought news that Mexican soldiers are coming",
                "settlers gather around a small brass cannon in an ox cart",
                "a white flag with a black cannon and a black star is about to be raised",
                "the little cannon in the ox cart, lit by a beam of low sun",
                "wide establishing shot, framed by a dark cabin corner in the foreground, a dirt road leading toward the cannon",
                "warm golden sunset, tense and quiet"))
pic(id="G-02", title="Cannon close-up", mvp=True, file="art/scenes/g02_cannon_closeup.png", fmt="F1",
    scene=scene("Gonzales, early October 1835, late afternoon",
                "no main characters; only the strong hands and homespun sleeves of settlers gripping the wooden cart wheel",
                "Mexican soldiers have come to take the town's cannon back",
                "settlers strain to push the small bronze cannon on its ox cart out of a deep rut",
                "the cart is about to roll free",
                "the small bronze cannon barrel and the big wooden wheel stuck in the rut",
                "low close-up from beside the wheel, dust kicking up, log cabins soft and blurred behind",
                "warm golden late light, urgent"))
pic(id="B-01", title="Béxar street", mvp=True, file="art/scenes/b01_bexar_street.png", fmt="F1",
    scene=scene(f"a cold gray December afternoon: {LOC['bexar']}",
                "no main characters; Mexican army soldiers in dark blue coats and tall black shakos marching across the far end of the street, Tejano families with bundles hurrying close to the walls",
                "fighting has broken out in the town",
                "families rush to find shelter as soldiers pass",
                "a wooden door is about to close",
                "a half-open wooden door spilling warm light into the gray street",
                "street-level shot, the flat-roofed houses leading the eye toward the dome of San Fernando church, smoke drifting across",
                "gray winter light, worried and hurried"))
pic(id="B-03", title="Night alley in Béxar", mvp=True, file="art/scenes/b03_night_alley.png", fmt="F1",
    scene=scene("a narrow alley between stone and adobe walls in San Antonio de Béxar, December 1835, night",
                "no main characters; the long shadows of a patrol stretching across the far end of the alley",
                "a patrol has just turned the corner",
                "a single hanging lantern lights the alley, with crates and barrels to hide behind",
                "someone is about to sneak past",
                "the pool of lantern light in the middle of the alley",
                "low view from behind a stack of crates, the alley leading the eye toward the patrol's shadows",
                "tense night, deep indigo shadows and warm lantern light"))
pic(id="A-01", title="The Alamo from outside", mvp=True, file="art/scenes/a01_alamo_outside.png", fmt="F1",
    extra=NO_HUMP,
    scene=scene(f"late February 1836, cold pale late afternoon: {LOC['alamo']}",
                "no main characters; tiny figures of defenders in everyday frontier clothes working on the walls",
                "the defenders know an army is coming",
                "they hurry to strengthen the walls",
                "on the far horizon, smoke rises from the campfires of a huge army",
                "the roofless stone church front with its flat, broken top edge",
                "wide shot from a low rise outside the walls, framed by bare winter mesquite branches, tiny figures against huge walls",
                "cold, pale winter light, gray-brown grass, uneasy"))
pic(id="A-02", title="Inside the Alamo courtyard", mvp=True, file="art/scenes/a02_alamo_courtyard.png", fmt="F1",
    extra=NO_HUMP,
    scene=scene(f"inside the walls, late February 1836, gray afternoon: {LOC['alamo']}",
                "no main characters; defenders in mixed frontier clothes hauling cannonballs and stacking sandbags in the background",
                "the siege has begun",
                "the defenders prepare inside the big dusty courtyard",
                "a messenger's saddled horse waits by the gate",
                "a quiet spot by a small campfire near the wall, with open space where two people could sit and talk",
                "medium-wide shot, framed by a wooden cannon platform in the foreground, the old church front in the background",
                "gray winter light with a warm glow from the campfire, tense but human"))
pic(id="A-03", title="Night escape from the Alamo", mvp=True, file="art/scenes/a03_alamo_escape.png", fmt="F1",
    scene=scene("outside the Alamo walls, early March 1836, night",
                "no people",
                "cannon fire has broken part of the old adobe wall",
                "a gap in the wall opens onto dark fields and an irrigation ditch",
                "someone is about to slip out into the night",
                "the jagged gap in the wall with moonlight beyond it",
                "low view from inside the wall looking out through the gap, broken adobe bricks in the foreground",
                "tense moonlit night, distant orange cannon flashes on the horizon, smoke drifting"))
pic(id="N-02", title="Washington-on-the-Brazos", mvp=True, file="art/scenes/n02_declaration_hall.png", fmt="F1",
    scene=scene(f"Washington-on-the-Brazos, March 2, 1836, a freezing morning: {LOC['washington']}",
                "no main characters; delegates in frock coats seen from behind and at a distance, one man standing and reading from a paper",
                "desperate news has arrived from the Alamo",
                "the delegates gather in the cold, unfinished hall",
                "they are about to declare independence",
                "the standing man and his paper, lit by a candle",
                "medium-wide shot from the back of the room, framed by a rough wooden doorway, cold daylight through the cloth-covered windows",
                "cold gray daylight and warm candlelight, serious and historic"))
pic(id="N-04", title="Goliad chapel at dusk", mvp=True, file="art/scenes/n04_goliad_chapel.png", fmt="F1",
    scene=scene(f"late March 1836, dusk: {LOC['goliad']}",
                "no people",
                "something terrible happened here a few days ago",
                "the stone chapel stands silent with its doors open and a dropped hat on the steps",
                "a single candle left on the step will burn into the night in remembrance",
                "the chapel bell tower against the dusk sky",
                "wide shot from outside the fort wall, framed by a broken wooden gate",
                "quiet, sad, still evening, thin smoke far away; no bodies, no violence"))
pic(id="N-05", title="Runaway Scrape road", mvp=True, file="art/scenes/n05_runaway_road.png", fmt="F1",
    scene=scene(f"late March 1836, heavy cold rain: {LOC['scrape']}",
                "no main characters; many kinds of families fleeing east together: Anglo settlers, Tejano families and enslaved Black families, on foot, in ox carts and covered wagons",
                "news has come that Santa Anna's army is advancing",
                "families flee down a muddy road, leaving belongings behind",
                "one covered wagon ahead is stuck deep in the mud",
                "the stuck covered wagon with its wheel sunk in mud",
                "wide shot with the road leading into the rain, a dropped chair and an open trunk in the mud in the foreground",
                "gray rainy afternoon, desperate but determined"))
pic(id="N-07", title="River crossing", mvp=True, file="art/scenes/n07_river_crossing.png", fmt="F1",
    scene=scene("a flooded brown river in East Texas, early April 1836, rain",
                "no main characters; people wading waist-deep across the river, holding on to a rope stretched between the banks, a wagon waiting on the far side",
                "the river has flooded from days of rain",
                "families cross by holding a rope against the strong current",
                "the water is still rising",
                "the rope stretched tight across the swirling brown water",
                "high angle looking down from the near bank, the rope leading the eye across the river",
                "gray rainy afternoon, dangerous and urgent"))
pic(id="J-01", title="Texian army camp", mvp=True, file="art/scenes/j01_army_camp.png", fmt="F1",
    scene=scene("the Texian army camp under live oaks, mid-April 1836, rain",
                "no main characters; volunteers in mixed frontier clothes around smoky fires, tents made of canvas and blankets, horses, a tall officer seen from behind at a distance",
                "the army has been retreating for weeks",
                "tired volunteers dry their rifles by the fires",
                "a decision to fight is coming",
                "the officers' tent with a lantern glowing inside",
                "wide shot framed by dripping oak branches in the foreground",
                "gray rainy afternoon, weary but tense"))
pic(id="J-02", title="Recon through tall grass", mvp=True, file="art/scenes/j02_recon_grass.png", fmt="F1",
    scene=scene(f"April 20, 1836, late afternoon: {LOC['sanjacinto']}",
                "no main characters; Mexican army soldiers in dark blue coats resting and working behind their barricade, tents behind them",
                "a scout has crept close to the enemy camp",
                "soldiers rest behind a low barricade of packs, saddles and brush",
                "a sentry is about to turn and look this way",
                "the low barricade and the sentry beside it",
                "hidden low view through tall grass, blades of grass blurred in the foreground",
                "warm late-afternoon light, quiet and tense"))
pic(id="J-03", title="San Jacinto battlefield", mvp=True, file="art/scenes/j03_battlefield.png", fmt="F1",
    scene=scene(f"April 21, 1836, mid-afternoon: {LOC['sanjacinto']}",
                "no main characters; tiny distant lines of Texian volunteers charging across the open prairie toward the Mexican camp, small flags, everything far away",
                "the Texian army has suddenly attacked",
                "the charge sweeps across the prairie through clouds of smoke",
                "the battle will be over in eighteen minutes",
                "a gap of golden light breaking through the smoke above the prairie",
                "wide shot from the edge of a live oak grove, dark oak trunks framing the view, tiny figures against a huge smoky sky",
                "hazy smoky battlefield light, dramatic; no gore, everything distant"))
pic(id="X-01", title="Ending: Observer", mvp=True, file="art/scenes/x01_end_observer.png", fmt="F1", modern=True,
    scene=scene("the edge between 1836 and the present day, twilight",
                "one small figure seen from far behind, just a dark silhouette with a backpack, face not visible",
                "the journey through history is over",
                "the figure steps into a glowing ring of blue light in an oak grove",
                "beyond the light, the soft glow of modern San Antonio is waiting",
                "the glowing ring of blue light",
                "wide shot from behind, the oak trees framing the light, the figure tiny against it",
                "deep indigo twilight with blazing blue-white light, peaceful and bittersweet"))
pic(id="X-02", title="Ending: Protector", mvp=True, file="art/scenes/x02_end_protector.png", fmt="F1",
    scene=scene("the Texas prairie in late spring, sunset",
                "no people",
                "someone was saved",
                "a weathered wooden fence stands among wildflowers, a hat hanging on one post",
                "two friends are about to sit on the fence and watch the sunset",
                "the empty fence rail with room for two, glowing in the sunset",
                "wide shot, the fence line leading the eye toward the setting sun",
                "warm golden sunset, peaceful and hopeful"))
pic(id="X-03", title="Ending: Stranded", mvp=True, file="art/scenes/x03_end_stranded.png", fmt="F1",
    scene=scene("a small homestead in 1836 Texas, sunset",
                "no people",
                "the way home has closed",
                "a log cabin with smoke curling from the chimney, a small garden and a split-rail fence",
                "a new life in the past is beginning",
                "the warm glowing window of the cabin",
                "wide shot from a low hill, a path leading down to the cabin, framed by a live oak",
                "warm golden sunset, bittersweet but hopeful"))
pic(id="X-04", title="Ending: Paradox", mvp=True, file="art/scenes/x04_end_paradox.png", fmt="F1", modern=True,
    scene=scene("modern-day San Antonio, Texas, dusk",
                "no people",
                "history was changed too much",
                "the city skyline looks familiar but subtly wrong: strange unfamiliar towers, odd colors in the lights, buildings that shouldn't be there",
                "a faint blue crack in the sky shows that time is still unsettled",
                "an unfamiliar tall spire at the center of the skyline",
                "wide shot from across the river, the river leading the eye toward the skyline",
                "eerie dusk with slightly wrong colors, mysterious and uneasy"))

# --- A5 Foreground (MVP) ---------------------------------------------------
pic(id="F-01", title="Tall grass layer", mvp=True, file="art/foreground/f01_grass.png",
    fmt="F6", fmt_fill=("tall prairie grass", "bottom"),
    subject="Tall, golden-green Texas prairie grass with a few seed heads, drawn with loose ink and watercolor. No people.")

# --- B Optional ------------------------------------------------------------
pic(id="C-13", title="Mexican army soldiers (group)", mvp=False, file="art/characters/c13_mexican_soldiers.png",
    fmt="F2", refs=[REF["story"] + " (style only)"],
    fmt_text="FORMAT: a full-body group of three figures standing together, on a plain flat cream background with nothing else, so it can be cut out easily.",
    subject="Three Mexican army soldiers of 1836 standing together: dark blue coats with red collars and cuffs, white crossbelts, light trousers, tall black shako hats, muskets with bayonets. One young and nervous, one older and tired, one looking off to the side. Ordinary people, not villains.")
pic(id="C-12", title="Texian volunteers (group)", mvp=False, file="art/characters/c12_texian_group.png",
    fmt="F2", refs=[REF["story"] + " (style only)"],
    fmt_text="FORMAT: a full-body group of three figures standing together, on a plain flat cream background with nothing else, so it can be cut out easily.",
    subject="Three Texian volunteers of 1836 standing together in everyday frontier clothes: homespun shirts, a frock coat, slouch hats, long rifles, no uniforms. One young, one bearded and older, one Tejano volunteer in a wide-brimmed hat and serape.")
pic(id="J-04", title="Return Window in the oak grove", mvp=False, file="art/scenes/j04_return_window.png", fmt="F1",
    window=True,
    scene=scene(f"April 21, 1836, late afternoon: {LOC['sanjacinto']}",
                "no people",
                "the battle is ending and smoke drifts through the trees",
                "the Return Window opens in a quiet grove of live oaks",
                "it is already starting to shrink",
                "the swirling Return Window",
                "medium-wide shot, dark oak trunks framing the window, smoke and golden light behind",
                "hazy golden light and glowing blue-white magic, urgent and wondrous"))
pic(id="R-04", title="Rowan epilogue", mvp=False, file="art/characters/r04_rowan_epilogue.png", fmt="F5",
    chars=[("rowan", "sitting on a wooden fence, reading her journal with a thoughtful, peaceful expression")],
    refs=[REF["rowan"]],
    scene=scene("the Texas prairie at sunset", "Rowan (described above)",
                "the adventure is over", "Rowan reads back through everything she noticed", "she is about to close the journal and smile",
                "Rowan's face, softly lit by the sunset", "medium shot, waist-up, wildflowers in the foreground", "warm golden sunset, quiet and reflective"))
pic(id="M-04", title="Morgan epilogue", mvp=False, file="art/characters/m04_morgan_epilogue.png", fmt="F5",
    chars=[("morgan", "standing at a wooden fence with her arms resting on the top rail, looking out over the prairie with a proud, tired smile")],
    refs=[REF["morgan"]],
    scene=scene("the Texas prairie at sunset", "Morgan (described above)",
                "the adventure is over", "Morgan thinks about the people she protected", "she is about to turn and wave to someone",
                "Morgan's face, softly lit by the sunset", "medium shot, waist-up, a horse grazing far in the background", "warm golden sunset, proud and reflective"))
pic(id="E-04", title="Ellis epilogue", mvp=False, file="art/characters/e04_ellis_epilogue.png", fmt="F5",
    chars=[("ellis", "perched on a low stone wall, turning a small brass compass in her fingers with a satisfied half-smile")],
    refs=[REF["ellis"]],
    scene=scene("old stone ruins on a Texas hill at sunset", "Ellis (described above)",
                "the adventure is over", "Ellis remembers every clever escape", "she is already planning the next one",
                "Ellis's face and the compass, softly lit by the sunset", "medium shot, waist-up, ruins framing her", "warm golden sunset, clever and reflective"))
pic(id="N-01", title="Map of Texas, 1836", mvp=False, file="art/scenes/n01_texas_map.png", fmt="F4",
    subject="A hand-drawn map of Texas in 1836 on old, slightly stained paper: the Gulf of Mexico coastline, rivers drawn as wavy ink lines flowing to the coast, small ink dots for towns, a simple compass rose in one corner. No words, no labels, no letters anywhere. No people.")
pic(id="C-04", title="Josefa expressions", mvp=False, file="art/characters/c04_josefa_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["josefa"]),
    chars=[("josefa", "shown head and shoulders in four different expressions")],
    refs=["art/characters/c03_josefa_body.png"], expr=True)
pic(id="C-10", title="Captain Reed expressions", mvp=False, file="art/characters/c10_reed_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["reed"]),
    chars=[("reed", "shown head and shoulders in four different expressions")],
    refs=["art/characters/c09_reed_body.png"], expr=True)
pic(id="C-06", title="Tomás expressions", mvp=False, file="art/characters/c06_tomas_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["tomas"]),
    chars=[("tomas", "shown head and shoulders in four different expressions")],
    refs=["art/characters/c05_tomas_body.png"], expr=True)
pic(id="C-08", title="Will expressions", mvp=False, file="art/characters/c08_will_expressions.png",
    fmt="F3", fmt_fill=tuple(EXPRESSIONS["will"]),
    chars=[("will", "shown head and shoulders in four different expressions")],
    refs=["art/characters/c07_will_body.png"], expr=True)
pic(id="A-04", title="Smoke over the Alamo at dawn", mvp=False, file="art/scenes/a04_alamo_dawn.png", fmt="F1",
    extra=NO_HUMP,
    scene=scene("a quiet hill far from the Alamo, March 6, 1836, dawn",
                "no people",
                "the battle is over",
                "thin smoke rises over the distant Alamo",
                "the sun is about to rise on a changed world",
                "the far-off Alamo under a column of smoke",
                "wide shot from the hilltop, framed by bare mesquite branches, the Alamo tiny in the distance",
                "quiet, sad, still dawn, pale pink and gray light; nothing violent shown"))
pic(id="B-02", title="Inside the Treviño home", mvp=False, file="art/scenes/b02_trevino_home.png", fmt="F1",
    scene=scene("inside a small adobe home in San Antonio de Béxar, December 1835, night",
                "no people",
                "the family has barred the door against the fighting outside",
                "a candle burns on a wooden table beside clay pots, a folded blanket and a small wooden cross on the wall",
                "someone is about to peek through the shutter",
                "the candle flame and the crack of light at the shutter",
                "medium-wide shot, framed by a rough wooden doorway in the foreground",
                "candlelit night, deep indigo shadows, warm and safe but worried"))
pic(id="G-03", title="Soldiers across the river", mvp=False, file="art/scenes/g03_soldiers_river.png", fmt="F1",
    scene=scene("the banks of the Guadalupe River near Gonzales, early October 1835, early morning",
                "no main characters; a line of Mexican army cavalry soldiers in dark blue coats with red trim, waiting on horseback on the far bank",
                "soldiers have arrived to demand the town's cannon",
                "they wait across the misty river",
                "the settlers are about to give their answer",
                "an officer on a pale horse at the water's edge",
                "wide shot from behind tall reeds on the near bank, the river leading the eye across",
                "cold blue dawn fog, quiet and tense"))
pic(id="G-04", title="Sneaking path in Gonzales", mvp=False, file="art/scenes/g04_sneak_path.png", fmt="F1",
    scene=scene("behind the log cabins of Gonzales, early October 1835, late afternoon",
                "no main characters; settlers' shadows far off near the cabins",
                "everyone's attention is on the cannon",
                "a narrow path runs between a split-rail fence and a field of dry cornstalks",
                "someone is about to slip past unseen",
                "the gap in the fence leading into the cornfield",
                "low hidden view from among the cornstalks, the path leading the eye forward",
                "warm golden late light with long shadows, sneaky"))
pic(id="P-04", title="Hiding in the brush", mvp=False, file="art/scenes/p04_brush_hide.png", fmt="F1",
    scene=scene("dense brush near San Antonio de Béxar, autumn 1835, dawn",
                "no main characters; horses' legs visible far off between the branches",
                "riders are searching the woods",
                "a hollow under a fallen tree and a narrow path through thorny brush and prickly pear offer a way out",
                "the riders are about to come closer",
                "the narrow escape path through the brush",
                "low hidden view from under the fallen tree, branches framing every edge",
                "cold blue dawn fog, tense"))
pic(id="N-06", title="Stuck wagon wheel", mvp=False, file="art/scenes/n06_stuck_wagon.png", fmt="F1",
    scene=scene("a muddy road in East Texas, late March 1836, heavy rain",
                "no main characters; only boots and hands pushing at the edges of the picture",
                "the wagon slid into a deep rut",
                "its big wooden wheel is sunk to the hub in thick mud",
                "it is about to come free, or break",
                "the wagon wheel and the splashing mud",
                "low close-up beside the wheel, rain streaking down",
                "gray rainy afternoon, straining and urgent"))
pic(id="N-03", title="The Declaration on the table", mvp=False, file="art/scenes/n03_declaration_paper.png", fmt="F4",
    subject="A handwritten document on a rough wooden table beside a quill, an ink pot and a burning candle, March 1836. The handwriting is only blurry, unreadable ink squiggles, with no real letters or words. No people.")
pic(id="S-02", title="Character select background", mvp=False, file="art/scenes/s02_select_bg.png", fmt="F1",
    refs=[REF["board"]],
    fmt_text="FORMAT: a wide, soft background with no characters that fades into plain cream paper toward the edges, quiet and simple so three character panels can sit on top. Wide landscape composition.",
    scene=scene("the Texas Hill Country in spring, golden afternoon",
                "no people",
                "three different paths are about to cross",
                "soft watercolor hills, oaks and a few bluebonnets blend gently into the paper",
                "a journey through history is about to begin",
                "a soft glow of light in the center",
                "wide, simple composition with lots of calm space",
                "warm golden afternoon, gentle and inviting"))
pic(id="F-02", title="Oak branches layer", mvp=False, file="art/foreground/f02_oak_branches.png",
    fmt="F6", fmt_fill=("oak branches and leaves", "top and the left and right edges"),
    subject="Dark live oak branches with small leaves and a little Spanish moss, drawn with loose ink and watercolor. No people.")
pic(id="F-03", title="Smoke layer", mvp=False, file="art/foreground/f03_smoke.png",
    fmt="F6", fmt_fill=("smoke wisps", "bottom and the left and right edges"),
    subject="Soft gray watercolor smoke drifting in wisps. No people.")
pic(id="F-04", title="Brush layer", mvp=False, file="art/foreground/f04_brush.png",
    fmt="F6", fmt_fill=("brush and bushes", "bottom"),
    subject="Low Texas brush, small bushes and a prickly pear cactus, drawn with loose ink and watercolor. No people.")
pic(id="F-05", title="Wall edge layer", mvp=False, file="art/foreground/f05_wall_edge.png",
    fmt="F6", fmt_fill=("a broken adobe wall edge", "left side"),
    subject="The crumbling edge of an old adobe wall with a few loose bricks. No people.")
pic(id="C-14", title="Fleeing family (group)", mvp=False, file="art/characters/c14_refugee_family.png",
    fmt="F2", refs=[REF["story"] + " (style only)"],
    fmt_text="FORMAT: a full-body group of figures walking together, on a plain flat cream background with nothing else, so it can be cut out easily.",
    subject="A family fleeing in 1836, walking together and carrying bundles: a father with a heavy pack, a mother holding a small child, an older girl carrying a chicken basket. Tired but determined, wearing simple homespun clothes and shawls.")
pic(id="D-07", title="Come and Take It flag", mvp=False, file="art/props/d07_gonzales_flag.png",
    fmt="F4", extra="The flag has NO words or letters on it.",
    subject="A homemade white cloth flag from 1835 hanging from a wooden pole, with a simple black cannon shape and a single black five-pointed star above it. No people.")
pic(id="D-01", title="Chrono-Compass, unbroken", mvp=False, file="art/props/d01_compass_whole.png",
    fmt="F4", compass="unbroken",
    subject="The Chrono-Compass, shiny and new, lid open, glowing a steady calm blue. No people.")
pic(id="D-04", title="Rowan's deer pendant", mvp=False, file="art/props/d04_deer_pendant.png",
    fmt="F4", refs=[REF["rowan"]],
    subject="Rowan's round brass pendant engraved with deer antlers, on a thin leather cord, slightly worn. No people.")
pic(id="D-05", title="Morgan's horseshoe charm", mvp=False, file="art/props/d05_horseshoe.png",
    fmt="F4", refs=[REF["morgan"]],
    subject="Morgan's small iron horseshoe charm on a braided leather bracelet. No people.")
pic(id="D-06", title="Ellis's fox pendant", mvp=False, file="art/props/d06_fox_pendant.png",
    fmt="F4", refs=[REF["ellis"]],
    subject="Ellis's small silver fox-head pendant on a thin dark chain. No people.")
pic(id="D-08", title="Field journal", mvp=False, file="art/props/d08_journal.png",
    fmt="F4",
    subject="An open leather-bound field journal with blank cream pages, a ribbon bookmark and a pencil tucked in the binding. The pages are completely blank. No people.")
pic(id="D-09", title="Jonah's letter", mvp=False, file="art/props/d09_letter.png",
    fmt="F4",
    subject="A folded, creased letter sealed with red wax, a little smudged with dirt, tied with string. No readable writing. No people.")
pic(id="D-10", title="Supply satchel", mvp=False, file="art/props/d10_satchel.png",
    fmt="F4",
    subject="A worn brown leather satchel with a buckled flap, a bread loaf and a rolled bandage peeking out. No people.")
pic(id="U-02", title="Watercolor wash stains", mvp=False, file="art/ui/u02_wash_stains.png",
    fmt="F7", fmt_fill=("watercolor wash stains",),
    subject="Soft overlapping ochre and gray watercolor stains on cream paper. No people.")
pic(id="U-03", title="Torn paper edges", mvp=False, file="art/ui/u03_torn_edges.png",
    fmt="F7", fmt_fill=("torn paper edges",),
    subject="Rough torn edges of cream paper with soft fibers along the tear. No people.")
pic(id="U-04", title="Ink brush banner", mvp=False, file="art/ui/u04_brush_banner.png",
    fmt="F4", refs=[REF["board"]],
    subject="One wide, rough, horizontal black ink brush stroke with dry-brush edges, like the black banner behind the game title on the reference board. No people.")
pic(id="U-05", title="Ink stamp marks", mvp=False, file="art/ui/u05_stamps.png",
    fmt="F4",
    subject="Three faded, uneven ink rubber-stamp marks on cream paper in a row: a circle, a five-pointed star and an X. No people.")


# ---------------------------------------------------------------------------
# 3. Assemble
# ---------------------------------------------------------------------------

def assemble(p, B, F):
    parts = [B["spine"]]
    for key, action in p["chars"]:
        parts.append(fill(B[key], f"In this picture: {action}."))
    if p.get("compass"):
        parts.append(fill(B["compass"], p["compass"]))
    if p.get("window"):
        parts.append(B["window"])
    if p.get("comp"):
        parts.append(B[p["comp"]])
    if p.get("scene"):
        s = p["scene"]
        parts.append("\n".join([
            f"SCENE: {s['where']}.",
            f"WHO: {s['who']}.",
            f"STORY MOMENT: {s['story']}.",
            f"FOCAL POINT: {s['focal']}.",
            f"CAMERA: {s['camera']}.",
            f"MOOD & LIGHT: {s['mood']}.",
        ]))
    if p.get("subject"):
        parts.append(f"SUBJECT: {p['subject']}")
    if p.get("extra"):
        parts.append(p["extra"])
    fmt = p.get("fmt_text") or fill(F[p["fmt"]], *p["fmt_fill"])
    if p.get("pronoun"):
        fmt = fmt.replace("her own", f"{p['pronoun']} own")
    parts.append(fmt)
    avoid = B["avoid"]
    if p.get("modern"):
        avoid = avoid.replace("modern objects, ", "")
    if p["fmt"] in ("F2", "F3", "F4", "F6", "F7", "F8"):
        # These pictures need a plain background, so don't forbid one.
        avoid = avoid.replace("empty generic backgrounds, ", "")
    parts.append(avoid)
    prompt = "\n\n".join(parts)
    leftover = re.findall(r"\[[^\]]*\]", prompt)
    if leftover:
        raise ValueError(f"{p['id']} still has blanks: {leftover}")
    return prompt


SECTIONS = [
    ("⭐ A1. Main characters", lambda p: p["mvp"] and p["id"][0] in "RME"),
    ("⭐ A2. Supporting characters", lambda p: p["mvp"] and p["id"][0] == "C"),
    ("⭐ A3. Props & icons", lambda p: p["mvp"] and p["id"][0] in "DU"),
    ("⭐ A4. Scenes", lambda p: p["mvp"] and p["id"][0] in "SPGBANJX"),
    ("⭐ A5. Foreground", lambda p: p["mvp"] and p["id"][0] == "F"),
    ("➕ B. Optional (most useful first)", lambda p: not p["mvp"]),
]

HEADER = """# 📋 Texas: Fractured Time — Ready-to-Paste Prompts

Every picture we need, with its prompt **already put together**. No assembling needed.

> 🤖 This file is made automatically from [ART_GUIDE.md](ART_GUIDE.md) by `tools/build_art_prompts.py`. To change a prompt, change the block in ART_GUIDE.md (or the picture's details in the script) and run `python3 tools/build_art_prompts.py`. Don't edit this file by hand, or your changes will be overwritten next time.

## How to use it

1. **Find the next picture.** Start at the top and go in order: ⭐ MVP first, then ➕ Optional.
2. **Set up your AI tool** using the little table above each prompt:
   - 📎 **Upload**: attach the reference picture(s) listed, if your tool allows it.
   - 📐 **Shape**: pick this shape or aspect ratio.
3. **Copy the whole grey box** (there's a copy button in its top-right corner on GitHub) and paste it into the AI tool.
4. **Make 3–4 versions.** Put them all in `art/drafts/`.
5. **Pick the best**, check it against the list at the end of ART_GUIDE.md, and save it exactly where **💾 Save as** says.
6. **Tick the box** ☐ → ✅ in this file and in ART_GUIDE.md §8.

> 💡 If a picture comes out wrong, look at **Part 9: Fixing Problems** in ART_GUIDE.md and add the fix sentence to the end of the prompt.

"""


def main():
    B, F = load_blocks()
    ids = [p["id"] for p in P]
    assert len(ids) == len(set(ids)), "duplicate IDs"
    mvp = sum(p["mvp"] for p in P)
    out = [HEADER, f"**{len(P)} pictures: ⭐ {mvp} MVP + ➕ {len(P) - mvp} optional.**\n\n## Contents\n"]
    for title, pred in SECTIONS:
        items = [p for p in P if pred(p)]
        out.append(f"- **{title}** ({len(items)}): " + ", ".join(p["id"] for p in items))
    out.append("")
    for title, pred in SECTIONS:
        items = [p for p in P if pred(p)]
        out.append(f"\n---\n\n## {title} ({len(items)})\n")
        for p in items:
            refs = "<br>".join(f"`{r.split(' (')[0]}`" + (" (style only)" if "style only" in r else "") for r in p["refs"]) or "nothing"
            out.append(f"### ☐ {p['id']} · {p['title']}\n")
            out.append("| 📎 Upload | 📐 Shape | 💾 Save as |\n|---|---|---|")
            out.append(f"| {refs} | {SHAPES[p['fmt']]} | `{p['file']}` |\n")
            if any(r.startswith("art/characters/") for r in p["refs"]):
                out.append("> ⚠️ Make the picture in the 📎 Upload column **first**, so you can use it as the reference here.\n")
            out.append("```text\n" + assemble(p, B, F) + "\n```\n")
            if p.get("expr"):
                stem = p["file"].rsplit("/", 1)[1].rsplit(".", 1)[0]
                names = [v.split(" (")[0] for v in p["fmt_fill"]]
                out.append(f"> ✂️ Then crop it into 4 squares (top-left, top-right, bottom-left, bottom-right) and save them next to it as "
                           + ", ".join(f"`{stem}_{n}.png`" for n in names) + ".\n")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(P)} prompts ({mvp} MVP)")


if __name__ == "__main__":
    main()
