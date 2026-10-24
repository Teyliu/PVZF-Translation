# German localization update

Reference: English files at commit
`a3db1c63e3b4982df57b3ca902653078e849a030` (4.0.5.2 Alpha release period).

## Completed in this update

| File | Text fields checked against English |
| --- | ---: |
| `Almanac/DetailStringsTranslate.json` | 47 |
| `Strings/abyss_buffs.json` | 132 |
| `Strings/translation_regexs.json` | 480 |
| `Strings/customlevel_regexs.json` | 91 |
| `Strings/customlevel_strings.json` | 280 |
| `Strings/custom_level_data.json` | 198 |
| `Strings/tips_fs.json` | 200 |
| `Strings/tips_iz.json` | 92 |
| `Strings/gods_evolved.json` | 0 (empty reference) |
| `Strings/travel_buffs.json` | 1002 |
| `Strings/translation_strings.json` | 3585 |
| `Almanac/ZombieStringsTranslate.json` | 708 |
| `Almanac/LawnStringsTranslate.json` | 2884 |

All thirteen current JSON text files cover 9699 text fields, including all
721 plants and 236 zombies. Reference lookup keys,
placeholders, numeric content, controls and rich-text tags are retained. The
release's `Strings/changelog.txt` is also translated. Existing German text was
reviewed while updating the current source, including correcting shield,
damage-reduction and tutorial descriptions.

The 77 legacy achievements (154 text fields) have also been revised, preserving
their existing keys, IDs and numeric conditions. They have no current English
counterpart, so they are excluded from the 9699-field reference comparison.
Existing textures have been retained. The localization has not been play-tested
in game.

## Translation approach and source limitations

The new text is authored directly from the English reference using ChatGPT.
No output from Google Translate, OPUS-MT or other translation services is used
in these changes. Scripts only apply explicitly authored translations and check
technical invariants; they do not generate translations.

Structural checks cannot prove linguistic accuracy or that text fits the game's
fixed UI elements. German-speaking in-game review is still needed, particularly
for fusion names, terminology and mechanics wording.

The reference itself has gaps. Its `gods_evolved.json` is empty, and the release
notes list missing support for The Gods: Evolved and its almanac, parts of the
Super Level Editor, and custom online levels. Translating available text does
not add missing hooks to the translator DLL. Malformed format tags already in
the English reference are retained rather than silently changed.

Known reference ambiguities retained for upstream review:

- The Abyss Opportunity description says **odd-numbered** levels in English,
  while its Chinese lookup key refers to even-numbered levels. German follows
  the English description.
- One average-damage pattern whose Chinese key uses the hundred-million unit
  has a ten-thousand multiplier in English. German retains the English
  multiplier; correcting that mismatch requires a separate source decision.
- The Last Striker banner description contains incomplete English timing text
  ("every 5s for 5 on the field"). German retains the stated values without
  inventing an absent unit or condition.

Translation files retain the repository's CC BY-NC 4.0 license.

## Validate the completed files

From the repository root, run:

```sh
python "Useful Scripts/Checking/validate_localization.py" German
python "Useful Scripts/Checking/test_validate_localization.py"
```

The checks use only Python's standard library and make no network requests.
They detect missing or extra keys, changed list structure or types, modified
IDs or numbers, placeholder and format-tag changes, lost line breaks, duplicate
JSON keys, and internal translation markers.

The full German reference check reports **13 files, 9699 text fields, 0 errors**.
The validator regression suite passes all 8 tests. `git diff --check` also passes.
Proper names, contributor handles and the reference's Latin placeholder biography
are intentionally retained. English and Chinese prose left in the old German
almanacs was replaced, and plant names were aligned across almanacs and tips.

## In-game review

1. Use a separate installation of the matching PC Multi-language release.
2. Copy `PvZ_Fusion_Translator/Localization/German` into
   `Mods/PvZ_Fusion_Translator/Localization/German` in the game's folder.
3. Select **Deutsch** and the **Local** translation source in the mod's language
   settings. Online mode may load the old upstream files instead.
4. Alternatively, with the game closed, edit the existing translator section
   in `UserData/MelonPreferences.cfg`:

   ```toml
   [PvZ_Fusion_Translator]
   UseLocal = true
   Language = "German"
   ```

   Preserve all other settings and sections.

5. Check menus, mechanics explanations, Abyss modifiers, custom-level messages,
   both almanacs, achievements and Odyssey modifiers. Record the level, displayed
   text, expected correction and any clipping or formatting problems.

The current MelonLoader source includes `German` in `LanguageEnum` and maps it
to `Deutsch`. This update does not change the translator DLL.
