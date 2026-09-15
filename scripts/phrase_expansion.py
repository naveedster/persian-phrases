#!/usr/bin/env python3
"""Legacy Persian-only expander. Superseded by ``generate_catalog.py``."""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable

Token = tuple[str, str, str]  # persian, transliteration, english


def _w(fa: str, tr: str, en: str) -> dict[str, str]:
    return {"persian": fa, "transliteration": tr, "english": en}


def _slug(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
    return slug[:72] or "phrase"


def _item(
    category: str,
    persian: str,
    english: str,
    transliteration: str,
    words: list[dict[str, str]],
    formality: str | None = None,
    id_hint: str | None = None,
) -> dict:
    return {
        "id": id_hint or _slug(transliteration),
        "category": category,
        "formality": formality,
        "persian": persian,
        "english": english,
        "transliteration": transliteration,
        "words": words,
    }


MIKHAHAM = _w("می‌خواهم", "mikhāham", "I want")
MIKHAM = _w("می‌خوام", "mikhām", "I want (informal)")
LOTFAN = _w("لطفاً", "lotfan", "please")
YEK = _w("یک", "yek", "one / a")
DARID = _w("دارید", "dārid", "you have (formal)")
DARI = _w("داری", "dāri", "you have (informal)")
KOJAST = _w("کجاست", "kojāst", "where is")
IN = _w("این", "in", "this")
AST = _w("است", "ast", "is")
KHEYLI = _w("خیلی", "kheyli", "very")
BEDUN = _w("بدون", "bedun", "without")
DOOST_DARAM = _w("دوست دارم", "dust dāram", "I like / I love")
NADARAM = _w("ندارم", "nadāram", "I do not have")
HASTAM = _w("هستم", "hastam", "I am")
NISTAM = _w("نیستم", "nistam", "I am not")
BEDEHID = _w("بدهید", "bedahid", "give (formal)")
NESHAN = _w("نشان بدهید", "neshān bedahid", "show (formal)")
BE = _w("به", "be", "to")
AZ = _w("az", "az", "from")
# fix AZ persian
AZ = _w("از", "az", "from")
MIRAVAM = _w("می‌روم", "miravam", "I go")
AMADAM = _w("آمدم", "āmadam", "I came")
NAZDIK = _w("نزدیک است", "nazdik ast", "is near")
DUR = _w("دور است", "dur ast", "is far")
GERAN = _w("گران است", "gerān ast", "is expensive")
ARZAN = _w("ارزان است", "arzān ast", "is cheap")
KHOSHMAZE = _w("خوشمزه است", "khoshmaze ast", "is delicious")
TEND = _w("تند است", "tond ast", "is spicy")
SARD = _w("سرد است", "sard ast", "is cold")
GARM = _w("گرم است", "garm ast", "is hot")
KAMAK = _w("کمک", "komak", "help")
MIKHAM_INF = MIKHAM


FOOD: list[Token] = [
    ("نان", "nān", "bread"),
    ("برنج", "berenj", "rice"),
    ("گوشت", "gusht", "meat"),
    ("مرغ", "morgh", "chicken"),
    ("ماهی", "māhi", "fish"),
    ("تخم‌مرغ", "tokhm-morgh", "egg"),
    ("پنیر", "panir", "cheese"),
    ("ماست", "māst", "yogurt"),
    ("کره", "kare", "butter"),
    ("سالاد", "sālād", "salad"),
    ("سوپ", "sup", "soup"),
    ("پلو", "polo", "pilaf"),
    ("کباب", "kabāb", "kebab"),
    ("خورشت", "khoresh", "stew"),
    ("قورمه‌سبزی", "ghorme-sabzi", "herb stew"),
    ("قیمه", "gheyme", "split-pea stew"),
    ("آش", "āsh", "thick soup"),
    ("ساندویچ", "sāndevich", "sandwich"),
    ("پیتزا", "pitzā", "pizza"),
    ("سیب‌زمینی", "sibzamini", "potato"),
    ("گوجه‌فرنگی", "goje-farangi", "tomato"),
    ("خیار", "khiār", "cucumber"),
    ("پیاز", "piāz", "onion"),
    ("سیر", "sir", "garlic"),
    ("فلفل", "felfel", "pepper"),
    ("نمک", "namak", "salt"),
    ("شکر", "shekar", "sugar"),
    ("روغن", "roghan", "oil"),
    ("میوه", "mive", "fruit"),
    ("سیب", "sib", "apple"),
    ("پرتقال", "porteghāl", "orange"),
    ("موز", "moz", "banana"),
    ("انگور", "angur", "grape"),
    ("هندوانه", "hendvāne", "watermelon"),
    ("هلو", "holu", "peach"),
    ("انار", "anār", "pomegranate"),
    ("خرما", "khormā", "date"),
    ("پسته", "peste", "pistachio"),
    ("بادام", "bādām", "almond"),
    ("گردو", "gerdu", "walnut"),
    ("بستنی", "bastani", "ice cream"),
    ("شیرینی", "shirini", "pastry"),
    ("کیک", "keyk", "cake"),
    ("برنج قهوه‌ای", "berenj-e ghahvei", "brown rice"),
    ("عدس", "adas", "lentils"),
    ("نخود", "nokhod", "chickpeas"),
    ("لوبیا", "lubiā", "beans"),
    ("سبزی", "sabzi", "herbs / greens"),
    ("نعناع", "na'nā", "mint"),
    ("جعفری", "jafari", "parsley"),
]

DRINKS: list[Token] = [
    ("آب", "āb", "water"),
    ("چای", "chāy", "tea"),
    ("قهوه", "qahve", "coffee"),
    ("شیر", "shir", "milk"),
    ("آب‌میوه", "āb-mive", "juice"),
    ("دوغ", "dugh", "savory yogurt drink"),
    ("نوشابه", "nushābe", "soda"),
    ("لیموناد", "limonād", "lemonade"),
    ("آب‌معدنی", "āb-ma'dani", "mineral water"),
    ("شربت", "sharbat", "sweet syrup drink"),
    ("ماءالشعیر", "mā'osh-sha'ir", "malt drink"),
    ("چای سبز", "chāy-e sabz", "green tea"),
    ("چای نبات", "chāy-e nabāt", "rock-candy tea"),
    ("آب گرم", "āb-e garm", "hot water"),
    ("یخ", "yakh", "ice"),
]

PLACES: list[Token] = [
    ("فرودگاه", "forudgāh", "airport"),
    ("ایستگاه", "istgāh", "station"),
    ("هتل", "hotel", "hotel"),
    ("رستوران", "resturān", "restaurant"),
    ("موزه", "muze", "museum"),
    ("بانک", "bānk", "bank"),
    ("داروخانه", "dārukhāne", "pharmacy"),
    ("بیمارستان", "bimārestān", "hospital"),
    ("بازار", "bāzār", "bazaar"),
    ("فروشگاه", "forushgāh", "store"),
    ("سوپرمارکت", "supermarkēt", "supermarket"),
    ("مسجد", "masjed", "mosque"),
    ("پارک", "pārk", "park"),
    ("خیابان", "khiābān", "street"),
    ("میدان", "meydān", "square"),
    ("دانشگاه", "dāneshgāh", "university"),
    ("مدرسه", "madrese", "school"),
    ("کتابخانه", "ketābkhāne", "library"),
    ("سینما", "sinemā", "cinema"),
    ("مترو", "metro", "metro"),
    ("ترمینال", "termināl", "terminal"),
    ("سفارت", "sefārat", "embassy"),
    ("پلیس", "polis", "police"),
    ("پست", "post", "post office"),
    ("نانوایی", "nānvāyi", "bakery"),
    ("کافی‌شاپ", "kāfi-shāp", "cafe"),
    ("ساحل", "sāhel", "beach"),
    ("کوه", "kuh", "mountain"),
    ("روستا", "rustā", "village"),
    ("شهر", "shahr", "city"),
    ("اتاق", "otāgh", "room"),
    ("دستشویی", "dastshuyi", "restroom"),
    ("آسانسور", "āsānsor", "elevator"),
    ("پارکینگ", "pārking", "parking"),
    ("ورودی", "vorudi", "entrance"),
    ("خروجی", "khoruji", "exit"),
    ("پل", "pol", "bridge"),
    ("گمرک", "gomrok", "customs"),
    ("ایستگاه اتوبوس", "istgāh-e otobus", "bus stop"),
    ("تاکسی‌سرویس", "tāksi-servis", "taxi stand"),
]

SHOP_ITEMS: list[Token] = [
    ("پیراهن", "pirāhan", "shirt"),
    ("شلوار", "shalvār", "pants"),
    ("کفش", "kafsh", "shoes"),
    ("کت", "kot", "coat"),
    ("کیف", "kif", "bag"),
    ("کلاه", "kolāh", "hat"),
    ("جوراب", "jurāb", "socks"),
    ("ساعت", "sā'at", "watch"),
    ("انگشتر", "angoshtar", "ring"),
    ("عینک", "eynak", "glasses"),
    ("گوشی", "gushi", "phone"),
    ("شارژر", "shārjer", "charger"),
    ("باتری", "bātri", "battery"),
    ("کتاب", "ketāb", "book"),
    ("مجله", "majale", "magazine"),
    ("نقشه", "naqshe", "map"),
    ("بلیط", "belit", "ticket"),
    ("کارت", "kārt", "card"),
    ("پول", "pul", "money"),
    ("هدیه", "hedye", "gift"),
    ("گل", "gol", "flowers"),
    ("صابون", "sābun", "soap"),
    ("شامپو", "shāmpu", "shampoo"),
    ("خمیردندان", "khamir-e-dandān", "toothpaste"),
    ("حوله", "howle", "towel"),
    ("بالش", "bālesh", "pillow"),
    ("پتو", "patu", "blanket"),
    ("کلید", "kelid", "key"),
    ("چمدان", "chamedān", "suitcase"),
    ("کوله‌پشتی", "kule-poshti", "backpack"),
    ("دوربین", "durbin", "camera"),
    ("لباس", "lebās", "clothes"),
    ("دامن", "dāman", "skirt"),
    ("روسری", "rusari", "scarf"),
    ("کمربند", "kamarband", "belt"),
    ("دستکش", "dastkesh", "gloves"),
]

PEOPLE: list[Token] = [
    ("مادرم", "mādar-am", "my mother"),
    ("پدرم", "pedar-am", "my father"),
    ("برادرم", "barādar-am", "my brother"),
    ("خواهرم", "khāhar-am", "my sister"),
    ("همسرم", "hamsar-am", "my spouse"),
    ("فرزندم", "farzand-am", "my child"),
    ("دخترم", "dokhtar-am", "my daughter"),
    ("پسرم", "pesar-am", "my son"),
    ("دوستم", "dust-am", "my friend"),
    ("همکارم", "hamkār-am", "my colleague"),
    ("استادم", "ostād-am", "my teacher"),
    ("همسایه‌ام", "hamsāye-am", "my neighbor"),
    ("عمویم", "amu-yam", "my uncle (paternal)"),
    ("دایی‌ام", "dāyi-am", "my uncle (maternal)"),
    ("عمه‌ام", "amme-am", "my aunt (paternal)"),
    ("خاله‌ام", "khāle-am", "my aunt (maternal)"),
    ("پدربزرگم", "pedar-bozorg-am", "my grandfather"),
    ("مادربزرگم", "mādar-bozorg-am", "my grandmother"),
    ("فرزندتان", "farzand-etān", "your child (formal)"),
    ("خانواده‌ام", "khānevāde-am", "my family"),
]

FEELING_ADJ: list[Token] = [
    ("خوشحال", "khoshhāl", "happy"),
    ("غمگین", "ghamgin", "sad"),
    ("خسته", "khaste", "tired"),
    ("عصبانی", "asabāni", "angry"),
    ("نگران", "negarān", "worried"),
    ("آرام", "ārām", "calm"),
    ("هیجان‌زده", "hayajān-zade", "excited"),
    ("شرمنده", "sharmande", "embarrassed / sorry"),
    ("تنها", "tanhā", "lonely"),
    ("امیدوار", "omidvār", "hopeful"),
    ("ناامید", "nāomid", "disappointed"),
    ("متعجب", "mota'ajjeb", "surprised"),
    ("ترسیده", "tarside", "afraid"),
    ("مطمئن", "motma'en", "sure"),
    ("مردد", "moraddad", "unsure"),
    ("سپاسگزار", "sepāsgozār", "grateful"),
    ("بی‌حوصله", "bi-hosele", "bored"),
    ("مضطرب", "moztareb", "anxious"),
    ("مغرور", "maghrur", "proud"),
    ("دلتنگ", "deltang", "homesick / longing"),
]

WEATHER_ADJ: list[Token] = [
    ("آفتابی", "āftābi", "sunny"),
    ("ابری", "abri", "cloudy"),
    ("بارانی", "bārāni", "rainy"),
    ("برفی", "barfi", "snowy"),
    ("مه", "meh", "foggy"),
    ("بادی", "bādi", "windy"),
    ("مرطوب", "martaub", "humid"),
    ("خشک", "khoshk", "dry"),
    ("خنک", "khonak", "cool"),
    ("سوزان", "suzān", "scorching"),
    ("طوفانی", "tufāni", "stormy"),
    ("نسیمی", "nasimi", "breezy"),
]

BODY: list[Token] = [
    ("سر", "sar", "head"),
    ("چشم", "cheshm", "eye"),
    ("گوش", "gush", "ear"),
    ("بینی", "bini", "nose"),
    ("دهان", "dahān", "mouth"),
    ("دندان", "dandān", "tooth"),
    ("گلو", "galu", "throat"),
    ("دست", "dast", "hand"),
    ("پا", "pā", "foot / leg"),
    ("شکم", "shekam", "stomach"),
    ("کمر", "kamar", "back / waist"),
    ("قلب", "ghalb", "heart"),
    ("پوست", "pust", "skin"),
    ("گردن", "gardan", "neck"),
    ("شانه", "shāne", "shoulder"),
]

WORK_NOUNS: list[Token] = [
    ("جلسه", "jalase", "meeting"),
    ("پروژه", "proje", "project"),
    ("گزارش", "gozāresh", "report"),
    ("ایمیل", "imeyl", "email"),
    ("تکلیف", "taklif", "homework"),
    ("امتحان", "emtehān", "exam"),
    ("کلاس", "kelās", "class"),
    ("دفتر", "daftar", "office / notebook"),
    ("رئیس", "ra'is", "boss"),
    ("همکار", "hamkār", "colleague"),
    ("دانشجو", "dāneshju", "student"),
    ("معلم", "mo'allem", "teacher"),
    ("قرارداد", "gharārdād", "contract"),
    ("حقوق", "hoghugh", "salary"),
    ("مرخصی", "morkhasi", "time off"),
    ("مهلت", "mohlat", "deadline"),
    ("ارائه", "erā'e", "presentation"),
    ("پژوهش", "pazhuhesh", "research"),
    ("کتاب درسی", "ketāb-e darsi", "textbook"),
    ("جزوه", "jozve", "handout"),
]


def _tok(item: Token) -> dict[str, str]:
    return _w(*item)


def expand_catalog() -> list[dict]:
    out: list[dict] = []

    def add(p: dict) -> None:
        out.append(p)

    # --- Food / drink frames ---
    for fa, tr, en in FOOD + DRINKS:
        tok = _tok((fa, tr, en))
        add(_item("food", f"{fa} می‌خواهم", f"I would like {en}", f"{tr} mikhāham", [tok, MIKHAHAM], "formal", f"want-{_slug(tr)}"))
        add(_item("food", f"{fa} می‌خوام", f"I want {en} (informal)", f"{tr} mikhām", [tok, MIKHAM], "informal", f"want-inf-{_slug(tr)}"))
        add(_item("food", f"یک {fa} لطفاً", f"One {en}, please", f"yek {tr} lotfan", [YEK, tok, LOTFAN], None, f"one-{_slug(tr)}"))
        add(_item("food", f"{fa} دارید؟", f"Do you have {en}? (formal)", f"{tr} dārid?", [tok, DARID], "formal", f"have-{_slug(tr)}"))
        add(_item("food", f"این {fa} است", f"This is {en}", f"in {tr} ast", [IN, tok, AST], None, f"this-is-{_slug(tr)}"))

    for fa, tr, en in FOOD:
        tok = _tok((fa, tr, en))
        add(_item("food", f"{fa} خیلی خوشمزه است", f"The {en} is very delicious", f"{tr} kheyli khoshmaze ast", [tok, KHEYLI, _w("خوشمزه", "khoshmaze", "delicious"), AST], None, f"tasty-{_slug(tr)}"))
        add(_item("food", f"بدون {fa}، لطفاً", f"Without {en}, please", f"bedun-e {tr}, lotfan", [BEDUN, tok, LOTFAN], None, f"without-{_slug(tr)}"))

    # --- Travel / places ---
    for fa, tr, en in PLACES:
        tok = _tok((fa, tr, en))
        add(_item("travel", f"{fa} کجاست؟", f"Where is the {en}?", f"{tr} kojāst?", [tok, KOJAST], None, f"where-{_slug(tr)}"))
        add(_item("travel", f"به {fa} می‌روم", f"I'm going to the {en}", f"be {tr} miravam", [BE, tok, MIRAVAM], None, f"going-{_slug(tr)}"))
        add(_item("travel", f"{fa} نزدیک است", f"The {en} is nearby", f"{tr} nazdik ast", [tok, _w("نزدیک", "nazdik", "near"), AST], None, f"near-{_slug(tr)}"))
        add(_item("travel", f"از {fa} آمدم", f"I came from the {en}", f"az {tr} āmadam", [AZ, tok, AMADAM], None, f"from-{_slug(tr)}"))

    # --- Shopping ---
    for fa, tr, en in SHOP_ITEMS:
        tok = _tok((fa, tr, en))
        add(_item("shopping", f"این {fa} چند است؟", f"How much is this {en}?", f"in {tr} chand ast?", [IN, tok, _w("چند", "chand", "how much"), AST], None, f"price-{_slug(tr)}"))
        add(_item("shopping", f"{fa} می‌خواهم", f"I would like the {en}", f"{tr} mikhāham", [tok, MIKHAHAM], "formal", f"buy-{_slug(tr)}"))
        add(_item("shopping", f"این {fa} گران است", f"This {en} is expensive", f"in {tr} gerān ast", [IN, tok, _w("گران", "gerān", "expensive"), AST], None, f"exp-{_slug(tr)}"))
        add(_item("shopping", f"{fa} کوچک‌تر دارید؟", f"Do you have a smaller {en}?", f"{tr} kuchek-tar dārid?", [tok, _w("کوچک‌تر", "kuchek-tar", "smaller"), DARID], "formal", f"smaller-{_slug(tr)}"))

    # --- Family ---
    for fa, tr, en in PEOPLE:
        tok = _tok((fa, tr, en))
        add(_item("family", f"{fa} کجاست؟", f"Where is {en}?", f"{tr} kojāst?", [tok, KOJAST], None, f"fam-where-{_slug(tr)}"))
        add(_item("family", f"{fa} را دوست دارم", f"I love {en}", f"{tr} rā dust dāram", [tok, _w("را", "rā", "object marker"), _w("دوست", "dust", "friend / love"), _w("دارم", "dāram", "I have")], None, f"fam-love-{_slug(tr)}"))
        add(_item("family", f"این {fa} است", f"This is {en}", f"in {tr} ast", [IN, tok, AST], None, f"fam-this-{_slug(tr)}"))

    # --- Feelings ---
    for fa, tr, en in FEELING_ADJ:
        tok = _tok((fa, tr, en))
        add(_item("feelings", f"{fa} هستم", f"I am {en}", f"{tr} hastam", [tok, HASTAM], None, f"feel-{_slug(tr)}"))
        add(_item("feelings", f"خیلی {fa}‌ام", f"I am very {en}", f"kheyli {tr}-am", [KHEYLI, tok, _w("ـام", "-am", "I am")], "informal", f"feel-very-{_slug(tr)}"))
        add(_item("feelings", f"چرا {fa} هستید؟", f"Why are you {en}? (formal)", f"cherā {tr} hastid?", [_w("چرا", "cherā", "why"), tok, _w("هستید", "hastid", "you are (formal)")], "formal", f"feel-why-{_slug(tr)}"))

    # --- Weather ---
    for fa, tr, en in WEATHER_ADJ:
        tok = _tok((fa, tr, en))
        add(_item("weather", f"هوا {fa} است", f"The weather is {en}", f"havā {tr} ast", [_w("هوا", "havā", "weather"), tok, AST], None, f"wx-{_slug(tr)}"))
        add(_item("weather", f"امروز {fa} است", f"Today is {en}", f"emruz {tr} ast", [_w("امروز", "emruz", "today"), tok, AST], None, f"wx-today-{_slug(tr)}"))

    # --- Health / body ---
    for fa, tr, en in BODY:
        tok = _tok((fa, tr, en))
        add(_item("health", f"{fa}م درد می‌کند", f"My {en} hurts", f"{tr}-am dard mikonad", [tok, _w("ـم", "-am", "my"), _w("درد", "dard", "pain"), _w("می‌کند", "mikonad", "does")], None, f"hurt-{_slug(tr)}"))
        add(_item("health", f"{fa}م خوب نیست", f"My {en} is not well", f"{tr}-am khub nist", [tok, _w("ـم", "-am", "my"), _w("خوب", "khub", "well"), _w("نیست", "nist", "is not")], None, f"unwell-{_slug(tr)}"))

    # --- Work ---
    for fa, tr, en in WORK_NOUNS:
        tok = _tok((fa, tr, en))
        add(_item("work", f"{fa} دارم", f"I have a {en}", f"{tr} dāram", [tok, _w("دارم", "dāram", "I have")], None, f"work-have-{_slug(tr)}"))
        add(_item("work", f"{fa} کی است؟", f"When is the {en}?", f"{tr} key ast?", [tok, _w("کی", "key", "when"), AST], None, f"work-when-{_slug(tr)}"))
        add(_item("work", f"{fa} را تمام کردم", f"I finished the {en}", f"{tr} rā tamām kardam", [tok, _w("را", "rā", "object marker"), _w("تمام", "tamām", "finished"), _w("کردم", "kardam", "I did")], None, f"work-done-{_slug(tr)}"))

    out.extend(_handwritten())
    return out


def _handwritten() -> list[dict]:
    rows: list[dict] = []

    def H(cat: str, fa: str, en: str, tr: str, words: list[tuple[str, str, str]], formality: str | None = None, hid: str | None = None) -> None:
        rows.append(_item(cat, fa, en, tr, [_w(*x) for x in words], formality, hid))

    # Time & numbers
    days = [
        ("شنبه", "shanbe", "Saturday"),
        ("یکشنبه", "yekshanbe", "Sunday"),
        ("دوشنبه", "doshanbe", "Monday"),
        ("سه‌شنبه", "seshanbe", "Tuesday"),
        ("چهارشنبه", "chahārshanbe", "Wednesday"),
        ("پنجشنبه", "panjshanbe", "Thursday"),
        ("جمعه", "jome", "Friday"),
    ]
    for fa, tr, en in days:
        H("time", f"امروز {fa} است", f"Today is {en}", f"emruz {tr} ast",
          [("امروز", "emruz", "today"), (fa, tr, en), ("است", "ast", "is")], hid=f"today-{tr}")
        H("time", f"فردا {fa} است", f"Tomorrow is {en}", f"fardā {tr} ast",
          [("فردا", "fardā", "tomorrow"), (fa, tr, en), ("است", "ast", "is")], hid=f"tomorrow-{tr}")

    months = [
        ("فروردین", "farvardin", "Farvardin (Mar–Apr)"),
        ("اردیبهشت", "ordibehesht", "Ordibehesht (Apr–May)"),
        ("خرداد", "khordād", "Khordād (May–Jun)"),
        ("تیر", "tir", "Tir (Jun–Jul)"),
        ("مرداد", "mordād", "Mordād (Jul–Aug)"),
        ("شهریور", "shahrivar", "Shahrivar (Aug–Sep)"),
        ("مهر", "mehr", "Mehr (Sep–Oct)"),
        ("آبان", "ābān", "Ābān (Oct–Nov)"),
        ("آذر", "āzar", "Āzar (Nov–Dec)"),
        ("دی", "dey", "Dey (Dec–Jan)"),
        ("بهمن", "bahman", "Bahman (Jan–Feb)"),
        ("اسفند", "esfand", "Esfand (Feb–Mar)"),
    ]
    for fa, tr, en in months:
        H("time", f"ماه {fa} است", f"It is {en}", f"māh-e {tr} ast",
          [("ماه", "māh", "month"), (fa, tr, en.split()[0]), ("است", "ast", "is")], hid=f"month-{tr}")

    hours = [
        ("یک", "yek", "one"), ("دو", "do", "two"), ("سه", "se", "three"),
        ("چهار", "chahār", "four"), ("پنج", "panj", "five"), ("شش", "shesh", "six"),
        ("هفت", "haft", "seven"), ("هشت", "hasht", "eight"), ("نه", "noh", "nine"),
        ("ده", "dah", "ten"), ("یازده", "yāzdah", "eleven"), ("دوازده", "davāzdah", "twelve"),
    ]
    for fa, tr, en in hours:
        H("time", f"ساعت {fa} است", f"It is {en} o'clock", f"sā'at {tr} ast",
          [("ساعت", "sā'at", "hour"), (fa, tr, en), ("است", "ast", "is")], hid=f"hour-{tr}")
        H("time", f"{fa} دقیقه صبر کنید", f"Please wait {en} minutes", f"{tr} daqiqe sabr konid",
          [(fa, tr, en), ("دقیقه", "daqiqe", "minute"), ("صبر", "sabr", "wait"), ("کنید", "konid", "do (formal)")], "formal", f"wait-{tr}")

    H("time", "دیروز بود", "It was yesterday", "diruz bud",
      [("دیروز", "diruz", "yesterday"), ("بود", "bud", "was")])
    H("time", "پس‌فردا می‌آیم", "I'll come the day after tomorrow", "pas-fardā miāyam",
      [("پس‌فردا", "pas-fardā", "the day after tomorrow"), ("می‌آیم", "miāyam", "I come")])
    H("time", "هفتهٔ آینده", "Next week", "hafte-ye āyande",
      [("هفته", "hafte", "week"), ("آینده", "āyande", "coming / next")])
    H("time", "ماه گذشته", "Last month", "māh-e gozashte",
      [("ماه", "māh", "month"), ("گذشته", "gozashte", "past")])
    H("time", "سال نو مبارک", "Happy New Year", "sāl-e now mobārak",
      [("سال", "sāl", "year"), ("نو", "now", "new"), ("مبارک", "mobārak", "blessed")])
    H("time", "الان وقت ندارم", "I don't have time now", "alān vaqt nadāram",
      [("الان", "alān", "now"), ("وقت", "vaqt", "time"), ("ندارم", "nadāram", "I do not have")], "informal")
    H("time", "زود باش", "Hurry up (informal)", "zud bāsh",
      [("زود", "zud", "soon / quick"), ("باش", "bāsh", "be")], "informal")
    H("time", "عجله نکنید", "Don't rush (formal)", "ajale nakonid",
      [("عجله", "ajale", "hurry"), ("نکنید", "nakonid", "don't do (formal)")], "formal")

    # Emergency
    emergencies = [
        ("کمک کنید", "Help me / help!", "komak konid",
         [("کمک", "komak", "help"), ("کنید", "konid", "do (formal)")], "formal"),
        ("با پلیس تماس بگیرید", "Call the police", "bā polis tamās begirid",
         [("با", "bā", "with"), ("پلیس", "polis", "police"), ("تماس", "tamās", "contact"), ("بگیرید", "begirid", "take (formal)")], "formal"),
        ("با اورژانس تماس بگیرید", "Call an ambulance", "bā orzhāns tamās begirid",
         [("با", "bā", "with"), ("اورژانس", "orzhāns", "emergency / ambulance"), ("تماس", "tamās", "contact"), ("بگیرید", "begirid", "take")], "formal"),
        ("آتش‌سوزی است", "There is a fire", "ātash-suzi ast",
         [("آتش‌سوزی", "ātash-suzi", "fire (incident)"), ("است", "ast", "is")], None),
        ("دزدیده شدم", "I've been robbed", "dozdide shodam",
         [("دزدیده", "dozdide", "stolen"), ("شدم", "shodam", "I became")], None),
        ("کیفم را دزدیدند", "They stole my bag", "kif-am rā dozdidand",
         [("کیفم", "kif-am", "my bag"), ("را", "rā", "object marker"), ("دزدیدند", "dozdidand", "they stole")], None),
        ("گم شده‌ام", "I'm lost", "gom shode-am",
         [("گم", "gom", "lost"), ("شده‌ام", "shode-am", "I have become")], None),
        ("نفس نمی‌توانم بکشم", "I can't breathe", "nafas nemitavānam bekasham",
         [("نفس", "nafas", "breath"), ("نمی‌توانم", "nemitavānam", "I cannot"), ("بکشم", "bekasham", "I draw")], None),
        ("خونریزی دارد", "It's bleeding", "khunrizi dārad",
         [("خونریزی", "khunrizi", "bleeding"), ("دارد", "dārad", "it has")], None),
        ("لطفاً آمبولانس خبر کنید", "Please call an ambulance", "lotfan āmbolāns khabar konid",
         [("لطفاً", "lotfan", "please"), ("آمبولانس", "āmbolāns", "ambulance"), ("خبر", "khabar", "news / notify"), ("کنید", "konid", "do")], "formal"),
        ("اینجا خطرناک است", "It's dangerous here", "injā khatarnāk ast",
         [("اینجا", "injā", "here"), ("خطرناک", "khatarnāk", "dangerous"), ("است", "ast", "is")], None),
        ("من را دنبال نکنید", "Don't follow me", "man rā donbāl nakonid",
         [("من", "man", "me"), ("را", "rā", "object marker"), ("دنبال", "donbāl", "follow"), ("نکنید", "nakonid", "don't")], "formal"),
        ("پاسپورت گم کرده‌ام", "I've lost my passport", "pāsport gom karde-am",
         [("پاسپورت", "pāsport", "passport"), ("گم", "gom", "lost"), ("کرده‌ام", "karde-am", "I have done")], None),
        ("کیف پولم نیست", "My wallet is missing", "kif-pul-am nist",
         [("کیف پولم", "kif-pul-am", "my wallet"), ("نیست", "nist", "is not")], None),
        ("آتش گرفته", "It's on fire", "ātash gerefte",
         [("آتش", "ātash", "fire"), ("گرفته", "gerefte", "has caught")], None),
        ("زخمی شده‌ام", "I'm injured", "zakhmi shode-am",
         [("زخمی", "zakhmi", "injured"), ("شده‌ام", "shode-am", "I have become")], None),
        ("کسی را صدا کنید", "Call someone", "kasi rā sedā konid",
         [("کسی", "kasi", "someone"), ("را", "rā", "object marker"), ("صدا", "sedā", "voice / call"), ("کنید", "konid", "do")], "formal"),
        ("لطفاً سریع باشید", "Please be quick", "lotfan sari' bāshid",
         [("لطفاً", "lotfan", "please"), ("سریع", "sari'", "quick"), ("باشید", "bāshid", "be (formal)")], "formal"),
        ("شماره اضطراری چیست؟", "What is the emergency number?", "shomāre-ye ezterāri chist?",
         [("شماره", "shomāre", "number"), ("اضطراری", "ezterāri", "emergency"), ("چیست", "chist", "what is")], "formal"),
        ("اینجا بمانید", "Stay here", "injā bemānid",
         [("اینجا", "injā", "here"), ("بمانید", "bemānid", "stay (formal)")], "formal"),
        ("فرار کنید", "Run / flee", "farār konid",
         [("فرار", "farār", "escape"), ("کنید", "konid", "do")], "formal"),
        ("من گم کرده‌ام", "I've lost (it)", "man gom karde-am",
         [("من", "man", "I"), ("گم", "gom", "lost"), ("کرده‌ام", "karde-am", "I have done")], None),
        ("دستم می‌سوزد", "My hand is burning", "dast-am misuzad",
         [("دستم", "dast-am", "my hand"), ("می‌سوزد", "misuzad", "it burns")], None),
        ("او بیهوش است", "He/she is unconscious", "u bihush ast",
         [("او", "u", "he/she"), ("بیهوش", "bihush", "unconscious"), ("است", "ast", "is")], None),
        ("لطفاً ترجمه کنید", "Please translate", "lotfan tarjome konid",
         [("لطفاً", "lotfan", "please"), ("ترجمه", "tarjome", "translation"), ("کنید", "konid", "do")], "formal"),
        ("سفارت کجاست؟", "Where is the embassy?", "sefārat kojāst?",
         [("سفارت", "sefārat", "embassy"), ("کجاست", "kojāst", "where is")], None),
        ("دزدی شد", "There was a theft", "dozdi shod",
         [("دزدی", "dozdi", "theft"), ("شد", "shod", "happened")], None),
        ("آژیر می‌زند", "The alarm is sounding", "āzhir mizanad",
         [("آژیر", "āzhir", "siren"), ("می‌زند", "mizanad", "it hits / sounds")], None),
        ("خروج اضطراری کجاست؟", "Where is the emergency exit?", "khoruj-e ezterāri kojāst?",
         [("خروج", "khoruj", "exit"), ("اضطراری", "ezterāri", "emergency"), ("کجاست", "kojāst", "where is")], None),
        ("من را به بیمارستان ببرید", "Take me to the hospital", "man rā be bimārestān bebarid",
         [("من", "man", "me"), ("را", "rā", "object marker"), ("به", "be", "to"), ("بیمارستان", "bimārestān", "hospital"), ("ببرید", "bebarid", "take (formal)")], "formal"),
    ]
    for i, row in enumerate(emergencies):
        fa, en, tr, words, form = row
        H("emergency", fa, en, tr, words, form, hid=f"emg-{i+1}")

    # Extra greetings / polite / daily that aren't in the seed
    extras = [
        ("greetings", "روز بخیر", "Good day", "ruz bekheyr",
         [("روز", "ruz", "day"), ("بخیر", "bekheyr", "well")], None),
        ("greetings", "وقت بخیر", "Good time of day", "vaqt bekheyr",
         [("وقت", "vaqt", "time"), ("بخیر", "bekheyr", "well")], None),
        ("greetings", "در پناه خدا", "Go with God / take care", "dar panāh-e khodā",
         [("در", "dar", "in"), ("پناه", "panāh", "protection"), ("خدا", "khodā", "God")], None),
        ("greetings", "به امید دیدار", "Hope to see you", "be omid-e didār",
         [("به", "be", "to"), ("امید", "omid", "hope"), ("دیدار", "didār", "meeting")], None),
        ("greetings", "فعلاً خداحافظ", "Bye for now", "fe'lan khodāhāfez",
         [("فعلاً", "fe'lan", "for now"), ("خداحافظ", "khodāhāfez", "goodbye")], "informal"),
        ("greetings", "از کجا هستید؟", "Where are you from? (formal)", "az kojā hastid?",
         [("از", "az", "from"), ("کجا", "kojā", "where"), ("هستید", "hastid", "you are")], "formal"),
        ("greetings", "اهل کجایی؟", "Where are you from? (informal)", "ahl-e kojāyi?",
         [("اهل", "ahl", "native of"), ("کجایی", "kojāyi", "where")], "informal"),
        ("greetings", "خوش گذشت", "It was nice / I had a good time", "khosh gozasht",
         [("خوش", "khosh", "pleasant"), ("گذشت", "gozasht", "passed")], None),
    ]
    polite_extra = [
        ("قابل نداشت", "Don't mention it (informal)", "ghābel nadāsht",
         [("قابل", "ghābel", "worth"), ("نداشت", "nadāsht", "did not have")], "informal"),
        ("خیلی لطف کردید", "That's very kind of you", "kheyli lotf kardid",
         [("خیلی", "kheyli", "very"), ("لطف", "lotf", "kindness"), ("کردید", "kardid", "you did (formal)")], "formal"),
        ("ببخشید دیر کردم", "Sorry I'm late", "bebakhshid dir kardam",
         [("ببخشید", "bebakhshid", "forgive"), ("دیر", "dir", "late"), ("کردم", "kardam", "I did")], None),
        ("اجازه هست؟", "May I? / Is it allowed?", "ejāze hast?",
         [("اجازه", "ejāze", "permission"), ("هست", "hast", "is there")], None),
        ("مزاحم نمی‌شوم", "I won't bother you", "mozāhem nemishavam",
         [("مزاحم", "mozāhem", "bother"), ("نمی‌شوم", "nemishavam", "I do not become")], "formal"),
        ("بعد از شما", "After you", "ba'd az shomā",
         [("بعد", "ba'd", "after"), ("از", "az", "from"), ("شما", "shomā", "you (formal)")], "formal"),
        ("قابل شما را ندارد", "It's nothing / not worthy of you", "ghābel-e shomā rā nadārad",
         [("قابل", "ghābel", "worth"), ("شما", "shomā", "you"), ("را", "rā", "object marker"), ("ندارد", "nadārad", "does not have")], "formal"),
        ("قربونت", "Thanks / I adore you (very informal)", "ghorbunet",
         [("قربونت", "ghorbunet", "may I be your sacrifice")], "informal"),
        ("خواهش می‌کنم بفرمایید", "Please, go ahead", "khāhesh mikonam befarmāyid",
         [("خواهش", "khāhesh", "request"), ("می‌کنم", "mikonam", "I do"), ("بفرمایید", "befarmāyid", "please do")], "formal"),
        ("شرمنده کردید", "You're too kind / you've embarrassed me", "sharmande kardid",
         [("شرمنده", "sharmande", "embarrassed"), ("کردید", "kardid", "you made (formal)")], "formal"),
        ("لطف دارید", "That's kind of you", "lotf dārid",
         [("لطف", "lotf", "kindness"), ("دارید", "dārid", "you have")], "formal"),
        ("با کمال میل", "With pleasure", "bā kamāl-e meyl",
         [("با", "bā", "with"), ("کمال", "kamāl", "perfection"), ("میل", "meyl", "desire")], "formal"),
        ("حتماً", "Certainly", "hatman",
         [("حتماً", "hatman", "certainly")], None),
        ("البته", "Of course", "albatte",
         [("البته", "albatte", "of course")], None),
        ("بعید می‌دانم", "I doubt it", "ba'id midānam",
         [("بعید", "ba'id", "unlikely"), ("می‌دانم", "midānam", "I know / consider")], None),
    ]
    for i, (fa, en, tr, words, form) in enumerate(polite_extra):
        H("polite", fa, en, tr, words, form, hid=f"polite-x-{i+1}")
    for i, row in enumerate(extras):
        cat, fa, en, tr, words, form = row
        H(cat, fa, en, tr, words, form, hid=f"extra-{cat}-{i+1}")

    daily_extra = [
        ("روشن است", "It's on / it's clear", "rowshan ast",
         [("روشن", "rowshan", "on / bright"), ("است", "ast", "is")]),
        ("خاموش کنید", "Turn it off", "khāmush konid",
         [("خاموش", "khāmush", "off"), ("کنید", "konid", "do")], "formal"),
        ("در را ببند", "Close the door (informal)", "dar rā beband",
         [("در", "dar", "door"), ("را", "rā", "object marker"), ("ببند", "beband", "close")], "informal"),
        ("پنجره را باز کنید", "Open the window", "panjere rā bāz konid",
         [("پنجره", "panjere", "window"), ("را", "rā", "object marker"), ("باز", "bāz", "open"), ("کنید", "konid", "do")], "formal"),
        ("چراغ را روشن کن", "Turn on the light (informal)", "cherāgh rā rowshan kon",
         [("چراغ", "cherāgh", "lamp"), ("را", "rā", "object marker"), ("روشن", "rowshan", "on"), ("کن", "kon", "do")], "informal"),
        ("شارژ تمام شد", "The battery died", "shārj tamām shod",
         [("شارژ", "shārj", "charge"), ("تمام", "tamām", "finished"), ("شد", "shod", "became")]),
        ("وای‌فای رمز دارد", "The Wi‑Fi has a password", "vāy-fāy ramz dārad",
         [("وای‌فای", "vāy-fāy", "Wi‑Fi"), ("رمز", "ramz", "password"), ("دارد", "dārad", "has")]),
        ("رمز را می‌گویید؟", "Will you tell me the password?", "ramz rā miguyid?",
         [("رمز", "ramz", "password"), ("را", "rā", "object marker"), ("می‌گویید", "miguyid", "you say (formal)")], "formal"),
        ("پیامک بفرست", "Send a text (informal)", "payāmak beferest",
         [("پیامک", "payāmak", "SMS"), ("بفرست", "beferest", "send")], "informal"),
        ("زنگ می‌زنم", "I'll call", "zang mizanam",
         [("زنگ", "zang", "ring / call"), ("می‌زنم", "mizanam", "I hit")]),
        ("مشغولم", "I'm busy", "mashghulam",
         [("مشغول", "mashghul", "busy"), ("ـم", "-am", "I am")]),
        ("بعداً حرف می‌زنیم", "We'll talk later", "ba'dan harf mizanim",
         [("بعداً", "ba'dan", "later"), ("حرف", "harf", "talk"), ("می‌زنیم", "mizanim", "we hit / we talk")], "informal"),
        ("عکس بگیرم؟", "Shall I take a photo?", "aks begiram?",
         [("عکس", "aks", "photo"), ("بگیرم", "begiram", "I take")]),
        ("صبر کن", "Wait (informal)", "sabr kon",
         [("صبر", "sabr", "wait"), ("کن", "kon", "do")], "informal"),
        ("نمی‌دانم", "I don't know", "nemidānam",
         [("نمی‌دانم", "nemidānam", "I do not know")]),
        ("یادم رفت", "I forgot", "yād-am raft",
         [("یادم", "yād-am", "my memory"), ("رفت", "raft", "went")]),
        ("درست است", "That's right", "dorost ast",
         [("درست", "dorost", "correct"), ("است", "ast", "is")]),
        ("اشتباه کردم", "I made a mistake", "eshtebāh kardam",
         [("اشتباه", "eshtebāh", "mistake"), ("کردم", "kardam", "I did")]),
        ("ممکن است؟", "Is it possible?", "momken ast?",
         [("ممکن", "momken", "possible"), ("است", "ast", "is")]),
        ("حتماً می‌آیم", "I'll definitely come", "hatman miāyam",
         [("حتماً", "hatman", "certainly"), ("می‌آیم", "miāyam", "I come")]),
        ("شاید بیایم", "I might come", "shāyad biāyam",
         [("شاید", "shāyad", "maybe"), ("بیایم", "biāyam", "I come (subjunctive)")]),
        ("نمی‌توانم بیایم", "I can't come", "nemitavānam biāyam",
         [("نمی‌توانم", "nemitavānam", "I cannot"), ("بیایم", "biāyam", "I come")]),
        ("خانه هستم", "I'm at home", "khāne hastam",
         [("خانه", "khāne", "home"), ("هستم", "hastam", "I am")]),
        ("بیرون هستم", "I'm out", "birun hastam",
         [("بیرون", "birun", "outside"), ("هستم", "hastam", "I am")]),
        ("کی برمی‌گردی؟", "When are you coming back? (informal)", "key barmigardi?",
         [("کی", "key", "when"), ("برمی‌گردی", "barmigardi", "you return")], "informal"),
        ("زود برمی‌گردم", "I'll be back soon", "zud barmigardam",
         [("زود", "zud", "soon"), ("برمی‌گردم", "barmigardam", "I return")]),
        ("دیر شده", "It's gotten late", "dir shode",
         [("دیر", "dir", "late"), ("شده", "shode", "has become")]),
        ("صبر کن برسم", "Wait till I get there (informal)", "sabr kon beresam",
         [("صبر", "sabr", "wait"), ("کن", "kon", "do"), ("برسم", "beresam", "I arrive")], "informal"),
        ("راه را بلد نیستم", "I don't know the way", "rāh rā balad nistam",
         [("راه", "rāh", "way"), ("را", "rā", "object marker"), ("بلد", "balad", "knowing how"), ("نیستم", "nistam", "I am not")]),
        ("آدرس را بنویسید", "Please write the address", "ādrés rā benevisid",
         [("آدرس", "ādres", "address"), ("را", "rā", "object marker"), ("بنویسید", "benevisid", "write (formal)")], "formal"),
    ]
    for i, row in enumerate(daily_extra):
        if len(row) == 5:
            fa, en, tr, words, form = row
        else:
            fa, en, tr, words = row
            form = None
        H("daily", fa, en, tr, words, form, hid=f"daily-x-{i+1}")

    health_extra = [
        ("سرما خورده‌ام", "I have a cold", "sarmā khorde-am",
         [("سرما", "sarmā", "cold"), ("خورده‌ام", "khorde-am", "I have caught")]),
        ("تب دارم", "I have a fever", "tab dāram",
         [("تب", "tab", "fever"), ("دارم", "dāram", "I have")]),
        ("سرفه می‌کنم", "I'm coughing", "sorfe mikonam",
         [("سرفه", "sorfe", "cough"), ("می‌کنم", "mikonam", "I do")]),
        ("حساسیت دارم", "I have allergies", "hassāsiyat dāram",
         [("حساسیت", "hassāsiyat", "allergy"), ("دارم", "dāram", "I have")]),
        ("به بادام حساسیت دارم", "I'm allergic to almonds", "be bādām hassāsiyat dāram",
         [("به", "be", "to"), ("بادام", "bādām", "almond"), ("حساسیت", "hassāsiyat", "allergy"), ("دارم", "dāram", "I have")]),
        ("دارو می‌خواهم", "I would like medicine", "dāru mikhāham",
         [("دارو", "dāru", "medicine"), ("می‌خواهم", "mikhāham", "I want")], "formal"),
        ("نسخه دارم", "I have a prescription", "noskhe dāram",
         [("نسخه", "noskhe", "prescription"), ("دارم", "dāram", "I have")]),
        ("دکتر می‌خواهم", "I need a doctor", "doktor mikhāham",
         [("دکتر", "doktor", "doctor"), ("می‌خواهم", "mikhāham", "I want")]),
        ("نوبت می‌خواهم", "I'd like an appointment", "nobat mikhāham",
         [("نوبت", "nobat", "turn / appointment"), ("می‌خواهم", "mikhāham", "I want")]),
        ("بیمه دارید؟", "Do you take insurance?", "bime dārid?",
         [("بیمه", "bime", "insurance"), ("دارید", "dārid", "you have")], "formal"),
        ("حالم بد است", "I feel unwell", "hāl-am bad ast",
         [("حالم", "hāl-am", "my condition"), ("بد", "bad", "bad"), ("است", "ast", "is")]),
        ("سرگیجه دارم", "I feel dizzy", "sargije dāram",
         [("سرگیجه", "sargije", "dizziness"), ("دارم", "dāram", "I have")]),
        ("تهوع دارم", "I feel nauseous", "tehavvo' dāram",
         [("تهوع", "tehavvo'", "nausea"), ("دارم", "dāram", "I have")]),
        ("خوابم نمی‌برد", "I can't sleep", "khāb-am nemibarad",
         [("خوابم", "khāb-am", "my sleep"), ("نمی‌برد", "nemibarad", "does not take")]),
        ("قرص مسکن دارید؟", "Do you have a painkiller?", "ghors-e mosakken dārid?",
         [("قرص", "ghors", "pill"), ("مسکن", "mosakken", "painkiller"), ("دارید", "dārid", "you have")], "formal"),
        ("زخم شده", "It's a cut / it's wounded", "zakhm shode",
         [("زخم", "zakhm", "wound"), ("شده", "shode", "has become")]),
        ("باندپیچی کنید", "Please bandage it", "bānd-pichi konid",
         [("باندپیچی", "bānd-pichi", "bandaging"), ("کنید", "konid", "do")], "formal"),
        ("فشار خونم بالاست", "My blood pressure is high", "feshār-khun-am bālāst",
         [("فشار خونم", "feshār-khun-am", "my blood pressure"), ("بالاست", "bālāst", "is high")]),
        ("دیابت دارم", "I have diabetes", "diābet dāram",
         [("دیابت", "diābet", "diabetes"), ("دارم", "dāram", "I have")]),
        ("گیاهی است؟", "Is it herbal?", "giyāhi ast?",
         [("گیاهی", "giyāhi", "herbal"), ("است", "ast", "is")]),
    ]
    for i, row in enumerate(health_extra):
        if len(row) == 5:
            fa, en, tr, words, form = row
        else:
            fa, en, tr, words = row[:4]
            form = None
        H("health", fa, en, tr, words, form, hid=f"health-x-{i+1}")

    work_extra = [
        ("دیر به جلسه رسیدم", "I arrived late to the meeting", "dir be jalase residam",
         [("دیر", "dir", "late"), ("به", "be", "to"), ("جلسه", "jalase", "meeting"), ("رسیدم", "residam", "I arrived")]),
        ("می‌توانیم فردا حرف بزنیم؟", "Can we talk tomorrow?", "mitavānim fardā harf bezanim?",
         [("می‌توانیم", "mitavānim", "we can"), ("فردا", "fardā", "tomorrow"), ("حرف", "harf", "talk"), ("بزنیم", "bezanim", "we do")], "formal"),
        ("ایمیل را فرستادم", "I sent the email", "imeyl rā ferestādam",
         [("ایمیل", "imeyl", "email"), ("را", "rā", "object marker"), ("فرستادم", "ferestādam", "I sent")]),
        ("لطفاً این را امضا کنید", "Please sign this", "lotfan in rā emzā konid",
         [("لطفاً", "lotfan", "please"), ("این", "in", "this"), ("را", "rā", "object marker"), ("امضا", "emzā", "signature"), ("کنید", "konid", "do")], "formal"),
        ("از کلاس جا ماندم", "I missed class", "az kelās jā māndam",
         [("از", "az", "from"), ("کلاس", "kelās", "class"), ("جا", "jā", "place"), ("ماندم", "māndam", "I stayed")]),
        ("نمره خوب گرفتم", "I got a good grade", "nomre-ye khub gereftam",
         [("نمره", "nomre", "grade"), ("خوب", "khub", "good"), ("گرفتم", "gereftam", "I got")]),
        ("باید درس بخوانم", "I have to study", "bāyad dars bekhānam",
         [("باید", "bāyad", "must"), ("درس", "dars", "lesson"), ("بخوانم", "bekhānam", "I read")]),
        ("کارمند هستم", "I'm an employee", "kārmand hastam",
         [("کارمند", "kārmand", "employee"), ("هستم", "hastam", "I am")]),
        ("آزادکار هستم", "I'm a freelancer", "āzād-kār hastam",
         [("آزادکار", "āzād-kār", "freelancer"), ("هستم", "hastam", "I am")]),
        ("دورکاری می‌کنم", "I work remotely", "durkāri mikonam",
         [("دورکاری", "durkāri", "remote work"), ("می‌کنم", "mikonam", "I do")]),
        ("لطفاً تکرار کنید", "Please repeat that", "lotfan tekrār konid",
         [("لطفاً", "lotfan", "please"), ("تکرار", "tekrār", "repeat"), ("کنید", "konid", "do")], "formal"),
        ("اسلاید بعدی", "Next slide", "slāyd-e ba'di",
         [("اسلاید", "slāyd", "slide"), ("بعدی", "ba'di", "next")]),
        ("سوالی دارید؟", "Any questions?", "so'āli dārid?",
         [("سوالی", "so'āli", "a question"), ("دارید", "dārid", "you have")], "formal"),
        ("موافقم", "I agree", "movāfeqam",
         [("موافق", "movāfeq", "agreeing"), ("ـم", "-am", "I am")]),
        ("موافق نیستم", "I disagree", "movāfeq nistam",
         [("موافق", "movāfeq", "agreeing"), ("نیستم", "nistam", "I am not")]),
        ("باید فکر کنم", "I need to think", "bāyad fekr konam",
         [("باید", "bāyad", "must"), ("فکر", "fekr", "thought"), ("کنم", "konam", "I do")]),
        ("فردا تحویل می‌دهم", "I'll turn it in tomorrow", "fardā tahvil midaham",
         [("فردا", "fardā", "tomorrow"), ("تحویل", "tahvil", "delivery"), ("می‌دهم", "midaham", "I give")]),
        ("این را چاپ کنید", "Please print this", "in rā chāp konid",
         [("این", "in", "this"), ("را", "rā", "object marker"), ("چاپ", "chāp", "print"), ("کنید", "konid", "do")], "formal"),
        ("اینترنت قطع شد", "The internet went out", "internet qat' shod",
         [("اینترنت", "internet", "internet"), ("قطع", "qat'", "cut"), ("شد", "shod", "became")]),
        ("فایل را فرستادم", "I sent the file", "fāyl rā ferestādam",
         [("فایل", "fāyl", "file"), ("را", "rā", "object marker"), ("فرستادم", "ferestādam", "I sent")]),
    ]
    for i, row in enumerate(work_extra):
        if len(row) == 5:
            fa, en, tr, words, form = row
        else:
            fa, en, tr, words = row
            form = None
        H("work", fa, en, tr, words, form, hid=f"work-x-{i+1}")

    weather_extra = [
        ("هوا سرد شده", "It's gotten cold", "havā sard shode",
         [("هوا", "havā", "weather"), ("سرد", "sard", "cold"), ("شده", "shode", "has become")]),
        ("هوا گرم شده", "It's gotten hot", "havā garm shode",
         [("هوا", "havā", "weather"), ("گرم", "garm", "hot"), ("شده", "shode", "has become")]),
        ("برف می‌آید", "It's snowing", "barf miāyad",
         [("برف", "barf", "snow"), ("می‌آید", "miāyad", "it comes")]),
        ("باد می‌آید", "The wind is blowing", "bād miāyad",
         [("باد", "bād", "wind"), ("می‌آید", "miāyad", "it comes")]),
        ("رعد و برق است", "There's thunder and lightning", "ra'd o bargh ast",
         [("رعد", "ra'd", "thunder"), ("و", "o", "and"), ("برق", "bargh", "lightning"), ("است", "ast", "is")]),
        ("چتر لازم است", "You need an umbrella", "chatr lāzem ast",
         [("چتر", "chatr", "umbrella"), ("لازم", "lāzem", "necessary"), ("است", "ast", "is")]),
        ("کت بردار", "Take a coat (informal)", "kot bardār",
         [("کت", "kot", "coat"), ("بردار", "bardār", "pick up")], "informal"),
        ("آسمان صاف است", "The sky is clear", "āsemān sāf ast",
         [("آسمان", "āsemān", "sky"), ("صاف", "sāf", "clear"), ("است", "ast", "is")]),
        ("غبارآلود است", "It's dusty / hazy", "ghobār-ālud ast",
         [("غبارآلود", "ghobār-ālud", "dusty"), ("است", "ast", "is")]),
        ("دمای هوا چند است؟", "What's the temperature?", "damā-ye havā chand ast?",
         [("دمای", "damā-ye", "temperature of"), ("هوا", "havā", "air"), ("چند", "chand", "how much"), ("است", "ast", "is")]),
    ]
    for i, row in enumerate(weather_extra):
        if len(row) == 5:
            fa, en, tr, words, form = row
        else:
            fa, en, tr, words = row
            form = None
        H("weather", fa, en, tr, words, form, hid=f"wx-x-{i+1}")

    shopping_extra = [
        ("می‌توانم پرو کنم؟", "Can I try this on?", "mitavānam paro konam?",
         [("می‌توانم", "mitavānam", "I can"), ("پرو", "paro", "fitting"), ("کنم", "konam", "I do")]),
        ("سایز بزرگ‌تر دارید؟", "Do you have a larger size?", "sāyz-e bozorg-tar dārid?",
         [("سایز", "sāyz", "size"), ("بزرگ‌تر", "bozorg-tar", "larger"), ("دارید", "dārid", "you have")], "formal"),
        ("تخفیف دارد؟", "Is it on sale?", "takhfif dārad?",
         [("تخفیف", "takhfif", "discount"), ("دارد", "dārad", "it has")]),
        ("کارت می‌گیرید؟", "Do you take cards?", "kārt migirid?",
         [("کارت", "kārt", "card"), ("می‌گیرید", "migirid", "you take")], "formal"),
        ("فقط نقد است؟", "Is it cash only?", "faghat naghd ast?",
         [("فقط", "faghat", "only"), ("نقد", "naghd", "cash"), ("است", "ast", "is")]),
        ("فاکتور می‌خواهم", "I would like a receipt", "fāktur mikhāham",
         [("فاکتور", "fāktur", "receipt"), ("می‌خواهم", "mikhāham", "I want")], "formal"),
        ("بسته‌بندی کنید", "Please wrap it", "baste-bandi konid",
         [("بسته‌بندی", "baste-bandi", "wrapping"), ("کنید", "konid", "do")], "formal"),
        ("عوض می‌کنید؟", "Can I exchange this?", "avaz mikonid?",
         [("عوض", "avaz", "exchange"), ("می‌کنید", "mikonid", "you do")], "formal"),
        ("مرجوع می‌کنم", "I'm returning this", "marju' mikonam",
         [("مرجوع", "marju'", "return"), ("می‌کنم", "mikonam", "I do")]),
        ("رنگ دیگر دارید؟", "Do you have another color?", "rang-e digar dārid?",
         [("رنگ", "rang", "color"), ("دیگر", "digar", "other"), ("دارید", "dārid", "you have")], "formal"),
        ("این را جدا کنید", "Please weigh / separate this", "in rā jodā konid",
         [("این", "in", "this"), ("را", "rā", "object marker"), ("جدا", "jodā", "separate"), ("کنید", "konid", "do")], "formal"),
        ("نیم کیلو بدهید", "Give me half a kilo", "nim kilo bedahid",
         [("نیم", "nim", "half"), ("کیلو", "kilo", "kilo"), ("بدهید", "bedahid", "give")], "formal"),
        ("تازه است؟", "Is it fresh?", "tāze ast?",
         [("تازه", "tāze", "fresh"), ("است", "ast", "is")]),
        ("گران‌تر از این نمی‌دهم", "I won't pay more than this", "gerān-tar az in nemidaham",
         [("گران‌تر", "gerān-tar", "more expensive"), ("از", "az", "than"), ("این", "in", "this"), ("نمی‌دهم", "nemidaham", "I do not give")]),
        ("چانه می‌زنم", "I'm haggling", "chāne mizanam",
         [("چانه", "chāne", "chin / bargain"), ("می‌زنم", "mizanam", "I hit")]),
    ]
    for i, row in enumerate(shopping_extra):
        if len(row) == 5:
            fa, en, tr, words, form = row
        else:
            fa, en, tr, words = row
            form = None
        H("shopping", fa, en, tr, words, form, hid=f"shop-x-{i+1}")

    return rows
