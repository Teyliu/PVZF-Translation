# 🌱 PVZ Fuzion Console Manager

A small companion tool for **Plants vs Zombies: Fusion** translators.
It scans every locale in `PvZ_Fusion_Translator/` against the English source
and tells you exactly **what's still missing**, then generates ready-to-use
Markdown reports and Trello CSVs.

> **Heads up — the tool moved.**
> The old `pvzf_console.pyz` Python archive that used to sit in this folder is
> gone. The Console Manager is now a Node CLI published on npm, so you always
> get the latest version instead of a stale copy checked into this repo.
> No Python, no `pip`, no runtime dependencies — just Node.

---

## 🚀 First run in 30 seconds

1. Make sure **Node.js 20 or newer** is installed.
   Download: [nodejs.org](https://nodejs.org/).
2. Open a terminal **in this `ConsolManager/` folder** — the tool then finds
   `../PvZ_Fusion_Translator/` on its own:

   ```
   PVZF-Translation/
   ├── ConsolManager/        ← run the CLI from here
   └── PvZ_Fusion_Translator/
       ├── Localization/
       ├── Dumps/
       └── …
   ```
3. Run:

   ```bash
   npx @charles_lindecker/pvzf-console
   ```

   That's it — the interactive menu opens.

Running it often? Install it once and get the `pvzf-console` command directly:

```bash
npm install -g @charles_lindecker/pvzf-console
pvzf-console
```

Generated reports and exports land in `ConsolManager/reports/` and
`ConsolManager/exports/`, which are git-ignored — nothing you produce here will
end up in a commit by accident.

> Launched it somewhere else? No problem. Go to
> **[3] Settings → Change PvZ_Fusion_Translator folder** and paste the
> absolute path to the folder. The setting is remembered across runs.

---

## 🧭 How to use it

The main menu always looks like this:

```
  MAIN MENU
  ─────────
    [1]  Show what's missing
    [2]  Translator tools
    [3]  Settings
    [0]  Exit
```

### [1] Show what's missing

Pick a locale (or `*` for all), then pick what to check:

| Option       | What it compares                                                          |
| ------------ | ------------------------------------------------------------------------- |
| Plants       | Plant almanac (`Almanac/LawnStringsTranslate.json`)                       |
| Zombies      | Zombie almanac (`Almanac/ZombieStringsTranslate.json`)                    |
| Achievements | Achievements (`Almanac/AchievementsTextTranslate.json`)                   |
| Strings      | UI strings (`Strings/translation_strings.json`)                           |
| Regex        | Regex translations (`Strings/translation_regexs.json`)                    |
| Tips         | Both `tips_iz.json` and `tips_fs.json`                                    |
| Abyss buffs  | `Strings/abyss_buffs.json`                                                |
| Travel buffs | `Strings/travel_buffs.json`                                               |
| All types    | Runs every check back-to-back                                             |

You get one Markdown report per type under **`reports/<Locale>/`**. Each
report shows the exact JSON block to copy/translate/paste into the locale
file. The tool also offers to write `*_diff.json` files alongside the reports —
say yes if you want the missing entries in re-injectable JSON form.

### [2] Translator tools

**Migrate tips** — rebuilds `tips_iz.json` / `tips_fs.json` from the legacy
`translation_strings.json`. All-or-nothing: if any source tip is missing from
`translation_strings.json`, the tool refuses to write a half-filled file and
tells you how many entries are still unmapped.

**Export Trello CSV** — turns a full locale's backlog into a Trello-ready
import. You'll get one CSV per category under `exports/<Locale>/`:

```
exports/French/
├── trello_Plants.csv
├── trello_Zombies.csv
├── trello_Strings.csv
├── trello_Regex.csv
├── trello_Tips_IZ.csv
├── trello_Tips_FS.csv
├── trello_Abyss_Buffs.csv
├── trello_Travel_Buffs.csv
└── trello_README.md      # full Blue Cat Power-Up import walkthrough
```

Every card description is a `json` code block so Trello renders it as a
monospace snippet — escape sequences like `\n` stay exactly as they appear in
the source files.

Follow the generated `trello_README.md` for the one-time board setup
(labels, lists, the Blue Cat plugin).

**Check duplicates** — scans every string file for duplicate JSON keys and for
values reused across multiple keys. Any locale with matches gets a
`duplicates.md` report under `reports/<Locale>/`.

### [3] Settings

Everything here is optional — defaults are sensible.

| Setting         | Default            | Notes                                          |
| --------------- | ------------------ | ---------------------------------------------- |
| Project folder  | auto-detected      | Absolute path to `PvZ_Fusion_Translator/`      |
| Source locale   | `English`          | The reference used for diffs (`Dumps` for raw dumps) |
| Text color      | `default`          | Color of ordinary text                         |
| Accent color    | `cyan`             | Color of headers, prompts, option keys         |
| Spacing density | `comfortable`      | `compact` · `comfortable` · `spacious`         |
| Show emoji      | `true`             | Swap emojis for `[OK] / [!] / [X]` if `false`  |
| Show banner     | `true`             | ASCII title shown at launch                    |
| Trello label    | `To be translated` | Label written on every exported card           |

Your settings file lives in your own account, not in this repo:

| Platform    | Path                                                        |
| ----------- | ----------------------------------------------------------- |
| macOS       | `~/Library/Application Support/pvzf-console/settings.json`   |
| Linux / BSD | `$XDG_CONFIG_HOME/pvzf-console/settings.json`, else `~/.config/pvzf-console/settings.json` |
| Windows     | `%APPDATA%\pvzf-console\settings.json`                       |

`[3] Settings` shows the exact path under *Settings file*. To keep it elsewhere,
set `PVZF_CONSOLE_SETTINGS` to the full path you want. Coming from the old
`pvzf_console.pyz` and its `settings.json` in this folder? It is picked up
automatically on first launch — nothing to redo.

---

## ⚡ Power-user mode

Skip the menus and run a single locale from the command line:

```bash
pvzf-console diff --lang French
pvzf-console diff --lang German --out ./out/german
pvzf-console diff --lang French --with-diff      # also write *_diff.json
```

Without a global install, prefix each command with
`npx @charles_lindecker/pvzf-console` instead of `pvzf-console`.

- Exits `0` on success.
- Exits `2` on an invalid or unknown locale (name lookup is case-sensitive).

Use it from batch scripts or CI to flag regressions automatically.

---

## 🛟 Troubleshooting

**"command not found: pvzf-console"**
Install Node 20+ from [nodejs.org](https://nodejs.org/), then either
`npm install -g @charles_lindecker/pvzf-console` or run it with `npx`.

**"Directory does not exist: …"**
The configured project folder is wrong. Open `[3] Settings` → *Change
PvZ_Fusion_Translator folder* and paste the right absolute path.

**The banner is a scrambled wall of `?` characters**
Your terminal isn't UTF-8 / VT100. The tool enables VT100 on Windows consoles,
but if that fails, go to `[3] Settings` → *Toggle ASCII banner* / *Toggle emoji*
for a plain-text fallback.

**A generated CSV is huge**
That's expected on day-one locales (thousands of strings). Import one CSV at
a time using the Blue Cat plugin — the instructions in
`trello_README.md` walk you through each step.

---

## 📦 What's in the package

- The translation-diff engine (plants, zombies, achievements, strings,
  regex, tips IZ / FS, abyss buffs, travel buffs).
- The tips-migration tool.
- The duplicate checker.
- The Trello CSV exporter + import guide generator.
- A configurable interactive TUI and a headless CLI.

No telemetry, no network calls, no data leaves your machine.

---

## 🔗 Source, issues, contributing

npm package:
<https://www.npmjs.com/package/@charles_lindecker/pvzf-console>

Open source on GitHub:
<https://github.com/LINDECKER-Charles/PVZ-Fuzion-ConsolManager>

If you hit a bug or want a new feature, open an issue or a pull request
there. The repo README explains how to set up a dev environment and how to
add new translation types.

---

## 👤 Author

**Charles Lindecker**
[charles.lindecker@outlook.fr](mailto:charles.lindecker@outlook.fr)
