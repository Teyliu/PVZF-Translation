#!/usr/bin/env python3
"""Assemble final Vietnamese 4.0.5 localization files.

Inputs:
  - merged_*.json (old VI 3.7 base + EN 4.0.5 appends, comparer semantics)
  - chunks/out/*.json (agent translations of EN-only entries)
  - detail_vi_final.json (47 DetailStrings keys)

Outputs (overwrite Vietnamese/):
  Almanac/LawnStringsTranslate.json, Almanac/ZombieStringsTranslate.json,
  Almanac/DetailStringsTranslate.json
  Strings/{translation_strings,translation_regexs,customlevel_regexs,
           tips_fs,tips_iz,custom_level_data,travel_buffs,
           customlevel_strings,abyss_buffs,gods_evolved}.json
Deletes legacy: Almanac/{ModdedPlants,Melon_ModdedPlants,Bepinex_ModdedPlants,ModdedZombies}Translate.json
Keeps: Almanac/AchievementsTextTranslate.json (mod still reads it; no EN 4.0.5 reference)
"""
import json, os, re, sys, collections

ROOT = "/home/ducts/Project/PVZF-Translation/PvZ_Fusion_Translator/Localization"
W = f"{ROOT}/Vietnamese/_work"
VI = f"{ROOT}/Vietnamese"
EN = f"{ROOT}/English"

def L(p):
    with open(p, encoding="utf-8-sig") as f: return json.load(f)
def D(p, o):
    with open(p, "w", encoding="utf-8") as f: json.dump(o, f, ensure_ascii=False, indent=2)

# ---------- 1. idempotent rename pass (hallucinated-name fixes) ----------
RENAME = [
 ("Zombie Hộp Quà Hắc Ngọc Bí Ẩn", "Mỏm Tuyết (Giặc)"),
 ("Zombie Hộp Quà Hồng Ngọc", "Zombie Cua Tuyết"),
 ("Zombie Hộp Quà Hắc Ngọc", "Người Máy Đầu Súng"),
 ("<color=#4B0082><u>Placeholder</u>", "Zombie Đòn Cuối Cùng"),
 ("Zombie Đại Pháo Hạng Nặng", "Zombie Jackson Vũ Trụ"),
 ("<u>Máy Khoan Netherite<u>", "Zombie Giáo Băng Đầu Óc Chó Cao"),
 ("<u>Thiên Cổ Quan Long<u>", "Voi Bóng Đêm"),
 ("<u>Dottore<u>", "Voi Sợ Hãi"),
 ("Lá Bèo Lớn Nước", "Nấm Gươm Nước"),
 ("Bồng Khiên Nước", "Nấm Khiên Nước"),
 ("Lá Bèo Lớn", "Nấm Gươm"),
 ("Dương Đại Thủy", "Nấm Khiên"),
 ("Chậu Hoa Lớn", "Đá Mù"),
 ("Sao Cơ Khí", "Nấm Biển Nướng"),
 ("Thủy Quái Đại Cơ Khí", "Đậu Pháp Sư Băng"),
 ("Nữ Hoàng Ác Ma", "Cỏ Ba Lá Quetzalcoatl"),
 ("Thiên Long Đại Đế", "Óc Chó Hắc Thạch"),
 ("Hắc Long Đại Đế", "SP Hoả Bộc Phượng Lan"),
 ("Bí Đè Thôi Miên", "Mỏm Tuyết (Bạn)"),
]
def sub(s):
    for old, new in RENAME:
        if old in s: s = s.replace(old, new)
    return s
def walk(o):
    if isinstance(o, str): return sub(o)
    if isinstance(o, list): return [walk(x) for x in o]
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    return o

def load_chunk(name):
    p = f"{W}/chunks/out/{name}.json"
    if not os.path.exists(p):
        sys.exit(f"MISSING chunk output: {p}")
    return walk(L(p))

# ---------- 2. almanac ----------
en_lawn = L(f"{EN}/Almanac/LawnStringsTranslate.json")
en_zomb = L(f"{EN}/Almanac/ZombieStringsTranslate.json")
ml = walk(L(f"{W}/merged_lawn.json"))["plants"]
mz = walk(L(f"{W}/merged_zombie.json"))["zombies"]

by_id_l = {e["seedType"]: e for e in ml if isinstance(e, dict) and e.get("seedType") is not None}
by_id_z = {e["theZombieType"]: e for e in mz if isinstance(e, dict) and e.get("theZombieType") is not None}

n_plant_applied = 0
for a in ("A1", "A2", "A3", "A4"):
    for key, vals in load_chunk(a).items():
        st = vals.get("seedType", int(key))
        e = by_id_l.get(st)
        if e is None:
            sys.exit(f"A chunk: seedType {st} not in merged lawn")
        for fld in ("name", "introduce", "info", "cost"):
            if vals.get(fld): e[fld] = vals[fld]
        n_plant_applied += 1
n_zomb_applied = 0
for key, vals in load_chunk("B").items():
    tz = vals.get("theZombieType", int(key))
    e = by_id_z.get(tz)
    if e is None:
        sys.exit(f"B chunk: theZombieType {tz} not in merged zombies")
    for fld in ("name", "introduce", "info"):
        if vals.get(fld): e[fld] = vals[fld]
    n_zomb_applied += 1
D(f"{VI}/Almanac/LawnStringsTranslate.json", {"plants": ml})
D(f"{VI}/Almanac/ZombieStringsTranslate.json", {"zombies": mz})

def apply_flat(final, out, source, what):
    for k, v in out.items():
        if k.startswith("__"):
            sys.exit(f"unexpected special key {k} in {what}")
        if k not in source:
            sys.exit(f"{what}: key {k!r} not in EN source ({len(source)} keys)")
        final[k] = v
en_ts   = L(f"{EN}/Strings/translation_strings.json")
en_tr   = L(f"{EN}/Strings/translation_regexs.json")
en_clr  = L(f"{EN}/Strings/customlevel_regexs.json")
en_tfs  = L(f"{EN}/Strings/tips_fs.json")
en_tiz  = L(f"{EN}/Strings/tips_iz.json")
en_cld  = L(f"{EN}/Strings/custom_level_data.json")
en_tb   = L(f"{EN}/Strings/travel_buffs.json")
en_cls  = L(f"{EN}/Strings/customlevel_strings.json")
en_ab   = L(f"{EN}/Strings/abyss_buffs.json")
en_ge   = L(f"{EN}/Strings/gods_evolved.json")

def base(name): return walk(L(f"{W}/merged_{name}.json"))

def apply_flat(final, out, source, what):
    for k, v in out.items():
        if k.startswith("__"):
            sys.exit(f"unexpected special key {k} in {what}")
        if k not in source:
            sys.exit(f"{what}: key {k!r} not in EN {source_name}")
        final[k] = v

# translation_strings (C1..C6)
ts = base("translation_strings")
for c in ("C1", "C2", "C3", "C4", "C5", "C6"):
    apply_flat(ts, load_chunk(c), en_ts, f"chunk {c}")
D(f"{VI}/Strings/translation_strings.json", ts)
# detail strings: G1 chunk (41 fresh descriptions) + old VI shared keys + fresh translation of 生存模式
en_d = L(f"{EN}/Almanac/DetailStringsTranslate.json")
detail = {}
for k, v in load_chunk("G1").items():
    if k not in en_d: sys.exit(f"G1 chunk: key {k!r} not in EN detail")
    detail[k] = v
old_detail = L(f"{W}/old_detail_vi.json")  # git-restored 3.7 file
for k in en_d:
    if k not in detail and k in old_detail:
        detail[k] = walk(old_detail[k])
detail["生存模式"] = ("Trong chế độ Sinh Tồn, bạn phải trụ vững qua nhiều đợt tấn công của Zombie "
    "(số đợt tấn công vô hạn ở chế độ Sinh Tồn: Vô Tận).\n"
    "\n"
    "Các tùy chọn sau có thể được bật trong Cài Đặt:\n"
    "[Bỏ Qua Lựa Chọn Cây Ở Chế Độ Vô Tận]: Bỏ qua màn hình chọn thẻ cây ở chế độ Vô Tận, "
    "cho phép bạn xem trước Zombie một cách ngắn gọn.\n"
    "[Chế Độ Vô Tận Thực Sự]: Sau khi hoàn thành mỗi đợt tấn công trong chế độ Sinh Tồn, "
    "tự động chuyển sang đợt tiếp theo. Bạn sẽ có 7.5 giây để dùng Almanac (chọn thẻ cây), "
    "trong khi giữ nguyên trạng thái của các cây bạn.")
missing_d = [k for k in en_d if k not in detail]
if missing_d: sys.exit(f"detail keys without translation: {missing_d}")
D(f"{VI}/Almanac/DetailStringsTranslate.json", detail)

# regexs: classify D keys by membership
tr, clr = base("translation_regexs"), base("customlevel_regexs")
for d in ("D1", "D2", "D3"):
    for k, v in load_chunk(d).items():
        if k in en_tr: tr[k] = v
        elif k in en_clr: clr[k] = v
        else: sys.exit(f"D chunk: key {k!r} in neither translation_regexs nor customlevel_regexs")
D(f"{VI}/Strings/translation_regexs.json", tr)
D(f"{VI}/Strings/customlevel_regexs.json", clr)

# tips + custom level data + travel buffs (E1..E3)
tfs, tiz, cld = base("tips_fs"), base("tips_iz"), base("custom_level_data")
tb = base("travel_buffs")
for e in ("E1", "E2", "E3"):
    for k, v in load_chunk(e).items():
        if k == "__travel_buffs__":
            for bk, bv in v.items(): tb[bk] = bv
        elif k in en_tfs: tfs[k] = v
        elif k in en_tiz: tiz[k] = v
        elif k in en_cld: cld[k] = v
        else: sys.exit(f"E chunk: key {k!r} not classified")
D(f"{VI}/Strings/tips_fs.json", tfs)
D(f"{VI}/Strings/tips_iz.json", tiz)
D(f"{VI}/Strings/custom_level_data.json", cld)
D(f"{VI}/Strings/travel_buffs.json", tb)

# customlevel_strings (F1..F3)
cls = base("customlevel_strings")
for f in ("F1", "F2", "F3"):
    apply_flat(cls, load_chunk(f), en_cls, f"chunk {f}")
D(f"{VI}/Strings/customlevel_strings.json", cls)

# abyss_buffs: no chunks expected (no new keys)
ab = base("abyss_buffs")
new_ab = [k for k in ab if k not in L(f"{VI}/Strings/abyss_buffs.json")]
if new_ab:
    print(f"WARNING: abyss_buffs has {len(new_ab)} EN-only keys with no chunk translation: {new_ab[:5]}")
D(f"{VI}/Strings/abyss_buffs.json", ab)
D(f"{VI}/Strings/gods_evolved.json", en_ge)

# ---------- 4. delete legacy superseded files ----------
for f in ("ModdedPlantsTranslate.json", "Melon_ModdedPlantsTranslate.json",
          "Bepinex_ModdedPlantsTranslate.json", "ModdedZombiesTranslate.json"):
    p = f"{VI}/Almanac/{f}"
    if os.path.exists(p): os.remove(p); print("deleted legacy:", f)
# ---------- 4b. old-VI shared entries still in English (3.7-era leftovers) ----------
OLD_FIXES = {
    "translation_strings": {
        "水草, 海蘑菇, 水草": "Rong Biển, Nấm Biển, Rong Biển",
        "购买成功\t\t\t\t\t\t\t\t\t\t购买成功": "Mua Thành Công!",
        "彩色卡牌": "Cây Độc Nhất",
        "木头": "Đồng", "白银": "Bạc", "黄金": "Vàng", "钻石": "Kim Cương", "棱彩": "Lăng Cầu",
        "返回\n(ESC)": "<size=90%>Quay Lại\n(ESC)",
        "ZOMBIE_MODIFIER_TAG": "Chỉnh Sửa Zombie",
        "UNLOCK_MODIFIER_TAG": "Chỉnh Sửa Mở Khóa",
        "INVEST_MODIFIER_TAG": "Chỉnh Sửa Đầu Tư",
        "确定_RG": "Tốt", "优秀": "Giỏi", "完美": "Hoàn Hảo",
        "小队": "Đội Drone",
    },
    "translation_regexs": {
        "旅行：守护 (\\d+)轮已经完成": "Du Lịch: Phòng Tuyến | Đã Hoàn Thành {0} Vòng",
        "^旅行：轮回 (\\d+)轮已经完成": "Du Lịch: Luân Hồi | Đã Hoàn Thành {0} Vòng",
        "^旅行：炼狱 (\\d+)轮已经完成": "Du Lịch: Luyện Ngục | Đã Hoàn Thành {0} Vòng",
        "^坚果台球(\\d+)?": "Billiard Óc Chó {0}",
        "^连击数：(\\d+)": "Combo: {0}",
        "^最大连击数：(\\d+)": "Combo Tối Đa: {0}",
        "未找到节点ID: ([^\\s：]+)": "Không Tìm Thấy Node Có ID: {0}",
        "^([\\s\\S]+)\n\n<b>节点ID:</b> ([\\s\\S]+)": "{0}\n\n<b>ID Node:</b> {1}",
        "\n(\\d+)%\n剩余(\\d+)\n还需(\\d+)": "\n{0}%\nCòn {1} Lớp\nCần {2} Cuộc Tấn Công",
    },
}
for fname, fixes in OLD_FIXES.items():
    p = f"{VI}/Strings/{fname}.json"
    d = L(p)
    n = 0
    for k, v in fixes.items():
        if k in d and d[k] != v:
            d[k] = v; n += 1
    if n: D(p, d); print(f"old-VI fixes applied to {fname}: {n}")

# ---------- 5. verification ----------
report = []
ok = True

def check(name, cond, extra=""):
    global ok
    if not cond: ok = False
    report.append(f"{'PASS' if cond else 'FAIL'}  {name} {extra}")

def ids(lst, key):
    return {e[key] for e in lst if isinstance(e, dict) and e.get(key) is not None}

check("lawn id-set == EN", ids(ml, "seedType") == ids(en_lawn["plants"], "seedType"),
      f"({len(ids(ml,'seedType'))} plants)")
check("zombie id-set == EN", ids(mz, "theZombieType") == ids(en_zomb["zombies"], "theZombieType"),
      f"({len(ids(mz,'theZombieType'))} zombies)")
check("detail keys == EN", set(detail) == set(en_d), f"({len(detail)} keys)")

pairs = [("translation_strings", ts, en_ts), ("translation_regexs", tr, en_tr),
         ("customlevel_regexs", clr, en_clr), ("tips_fs", tfs, en_tfs),
         ("tips_iz", tiz, en_tiz), ("custom_level_data", cld, en_cld),
         ("abyss_buffs", ab, en_ab), ("DetailStringsTranslate", detail, en_d)]
for name, fin, en in pairs:
    check(f"{name} keys == EN", set(fin) == set(en), f"({len(fin)} keys, "
          f"missing={len(set(en)-set(fin))} extra={len(set(fin)-set(en))})")

# ---------- checks scope: only freshly translated entries (old-VI shared text kept by design) ----------
def load_keys(*names):
    s = set()
    for n in names: s |= set(load_chunk(n))
    return s

fresh = {
    "translation_strings": load_keys("C1", "C2", "C3", "C4", "C5", "C6"),
    "tips_fs": set(), "tips_iz": set(), "custom_level_data": set(),
    "travel_buffs": set(),
    "customlevel_strings": load_keys("F1", "F2", "F3"),
    "abyss_buffs": set(),
    "DetailStringsTranslate": load_keys("G1") | {"生存模式"},
}
for e in ("E1", "E2", "E3"):
    for k, v in load_chunk(e).items():
        if k == "__travel_buffs__":
            for bk, bv in v.items():
                for bid in bv: fresh["travel_buffs"].add(f"{bk}/{bid}")
        elif k in en_tfs: fresh["tips_fs"].add(k)
        elif k in en_tiz: fresh["tips_iz"].add(k)
        elif k in en_cld: fresh["custom_level_data"].add(k)
fresh_plants = set()
for a in ("A1", "A2", "A3", "A4"):
    for key, vals in load_chunk(a).items():
        fresh_plants.add(vals.get("seedType", int(key)))
fresh_zombies = {v.get("theZombieType", int(k)) for k, v in load_chunk("B").items()}

TAG = re.compile(r"</?[a-zA-Z][^>]*>")
# deliberately kept verbatim: loanwords/proper nouns/placeholders (see PLAN.md)
LOAN = {"Streamer", "ZomBoogie"}
KEEP_AS_EN = {("custom_level_data", "level_1788007800778_u5mqsl3b2", "name")}
def translatable(s):
    if not isinstance(s, str): return False
    t = TAG.sub("", s).strip()
    if not t or t in ("N/A", "HERE"): return False
    if t.startswith("-------") or t in LOAN: return False
    if re.search(r"Lorem ipsum", t): return False  # EN placeholder text
    if re.fullmatch(r"[\d\s.,%×+\-*/(){}\[\]{value}]+", t): return False
    if re.fullmatch(r"(?:[A-Z]\.)*[A-Z]+\.?", t): return False  # acronym e.g. A.L.E.C.
    if re.search(r"[A-Za-zÀ-ÿ\u00C0-\u02AF]", t): return True  # latin
    return bool(re.search(r"[\u4e00-\u9fff]", t))  # CJK
def tags(s):
    return collections.Counter(TAG.findall(s or ""))

left, tagbad = [], []
def scan(v, e, where):
    if v == e and translatable(e): left.append(where)
    if isinstance(v, str) and tags(v) != tags(e if isinstance(e, str) else ""): tagbad.append(where)

for name, fin, en in pairs:
    if name in ("translation_regexs", "customlevel_regexs", "abyss_buffs"):
        continue  # functional patterns / no fresh content
    if name == "travel_buffs":
        for cat, entries in fin.items():
            for bid, e in entries.items():
                if f"{cat}/{bid}" not in fresh["travel_buffs"]: continue
                ref = en.get(cat, {}).get(bid)
                if not isinstance(ref, dict): sys.exit(f"travel_buffs {cat}/{bid} not in EN")
                for fld in ("name", "desc"):
                    scan(e.get(fld), ref.get(fld), f"travel_buffs {cat}/{bid}.{fld}")
        continue
    for k in fin:
        if k not in fresh[name] or k not in en: continue
        v, ev = fin[k], en[k]
        if name == "translation_strings" and k.startswith("-"):
            continue  # section headers kept verbatim
        if isinstance(v, dict) and isinstance(ev, dict):
            for fld in v:
                if (name, k, fld) in KEEP_AS_EN: continue
                scan(v[fld], ev.get(fld), f"{name}:{k[:40]}.{fld}")
        else:
            scan(v, ev, f"{name}:{k[:50]!r}")

# almanac: fresh entries only
en_pl = {e["seedType"]: e for e in en_lawn["plants"] if isinstance(e, dict)}
en_zl = {e["theZombieType"]: e for e in en_zomb["zombies"] if isinstance(e, dict)}
old_pl_tagdiff = old_z_tagdiff = 0
for e in ml:
    st = e.get("seedType")
    ref = en_pl.get(st)
    if not ref: continue
    for fld in ("name", "introduce", "info", "cost"):
        if st in fresh_plants: scan(e.get(fld), ref.get(fld), f"plant[{st}].{fld}")
        elif isinstance(e.get(fld), str) and tags(e.get(fld)) != tags(ref.get(fld)):
            old_pl_tagdiff += 1
for e in mz:
    tz = e.get("theZombieType")
    ref = en_zl.get(tz)
    if not ref: continue
    for fld in ("name", "introduce", "info"):
        if tz in fresh_zombies: scan(e.get(fld), ref.get(fld), f"zombie[{tz}].{fld}")
        elif isinstance(e.get(fld), str) and tags(e.get(fld)) != tags(ref.get(fld)):
            old_z_tagdiff += 1

check("no untranslated leftovers (fresh entries)", not left, f"({len(left)} found)" if left else "")
if left:
    for x in left[:40]: print("   leftover:", x)
check("rich-text tag multisets == EN (fresh entries)", not tagbad, f"({len(tagbad)} mismatches)" if tagbad else "")
if tagbad:
    for x in tagbad[:40]: print("   tagdiff:", x)
report.append(f"INFO  old-VI shared almanac tag drift (EN balance changes, kept by design): "
              f"plants={old_pl_tagdiff} fields, zombies={old_z_tagdiff} fields")

# all final files parse (they were just dumped, but re-read to be sure)
for sub, files in (("Almanac", ["LawnStringsTranslate.json", "ZombieStringsTranslate.json",
                                "DetailStringsTranslate.json"]),
                   ("Strings", ["translation_strings.json", "translation_regexs.json",
                                "customlevel_regexs.json", "tips_fs.json", "tips_iz.json",
                                "custom_level_data.json", "travel_buffs.json",
                                "customlevel_strings.json", "abyss_buffs.json", "gods_evolved.json"])):
    for f in files:
        L(f"{VI}/{sub}/{f}")
report.append("PASS  all final files re-parse as JSON")

print(f"\nplants applied: {n_plant_applied}, zombies applied: {n_zomb_applied}")
print("\n".join(report))
print("\nASSEMBLY", "OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
