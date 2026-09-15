#!/usr/bin/env python3
"""Write the bundled phrase catalog used by PersianPhrasesKit."""

from __future__ import annotations

import json
from pathlib import Path

PHRASES = [
    # --- Greetings ---
    {
        "id": "salam",
        "category": "greetings",
        "formality": "informal",
        "persian": "سلام",
        "english": "Hello (informal / everyday)",
        "transliteration": "salām",
        "words": [
            {"persian": "سلام", "transliteration": "salām", "english": "hello / peace"},
        ],
    },
    {
        "id": "salam-aleikom",
        "category": "greetings",
        "formality": "formal",
        "persian": "سلام علیکم",
        "english": "Peace be upon you (formal greeting)",
        "transliteration": "salām aleikom",
        "words": [
            {"persian": "سلام", "transliteration": "salām", "english": "peace / hello"},
            {"persian": "علیکم", "transliteration": "aleikom", "english": "upon you"},
        ],
    },
    {
        "id": "sobh-bekheyr",
        "category": "greetings",
        "formality": None,
        "persian": "صبح بخیر",
        "english": "Good morning",
        "transliteration": "sobh bekheyr",
        "words": [
            {"persian": "صبح", "transliteration": "sobh", "english": "morning"},
            {"persian": "بخیر", "transliteration": "bekheyr", "english": "well / for good"},
        ],
    },
    {
        "id": "asr-bekheyr",
        "category": "greetings",
        "formality": None,
        "persian": "عصر بخیر",
        "english": "Good afternoon",
        "transliteration": "asr bekheyr",
        "words": [
            {"persian": "عصر", "transliteration": "asr", "english": "afternoon"},
            {"persian": "بخیر", "transliteration": "bekheyr", "english": "well / for good"},
        ],
    },
    {
        "id": "shab-bekheyr",
        "category": "greetings",
        "formality": None,
        "persian": "شب بخیر",
        "english": "Good night",
        "transliteration": "shab bekheyr",
        "words": [
            {"persian": "شب", "transliteration": "shab", "english": "night"},
            {"persian": "بخیر", "transliteration": "bekheyr", "english": "well / for good"},
        ],
    },
    {
        "id": "khodahafez",
        "category": "greetings",
        "formality": None,
        "persian": "خداحافظ",
        "english": "Goodbye",
        "transliteration": "khodāhāfez",
        "words": [
            {"persian": "خدا", "transliteration": "khodā", "english": "God"},
            {"persian": "حافظ", "transliteration": "hāfez", "english": "protector"},
        ],
    },
    {
        "id": "halet-chetore",
        "category": "greetings",
        "formality": "informal",
        "persian": "حالت چطوره؟",
        "english": "How are you? (informal)",
        "transliteration": "hālet chetore?",
        "words": [
            {"persian": "حالت", "transliteration": "hālet", "english": "your condition / how you are"},
            {"persian": "چطوره", "transliteration": "chetore", "english": "how is it?"},
        ],
    },
    {
        "id": "hale-shoma-chetor-ast",
        "category": "greetings",
        "formality": "formal",
        "persian": "حال شما چطور است؟",
        "english": "How are you? (formal)",
        "transliteration": "hāl-e shomā chetor ast?",
        "words": [
            {"persian": "حال", "transliteration": "hāl", "english": "condition / health"},
            {"persian": "شما", "transliteration": "shomā", "english": "you (formal/plural)"},
            {"persian": "چطور", "transliteration": "chetor", "english": "how"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "khubam-mamnun",
        "category": "greetings",
        "formality": None,
        "persian": "خوبم، ممنون",
        "english": "I'm fine, thanks",
        "transliteration": "khubam, mamnun",
        "words": [
            {"persian": "خوبم", "transliteration": "khubam", "english": "I am well"},
            {"persian": "ممنون", "transliteration": "mamnun", "english": "thankful / thanks"},
        ],
    },
    {
        "id": "khosh-amadid",
        "category": "greetings",
        "formality": "formal",
        "persian": "خوش آمدید",
        "english": "Welcome",
        "transliteration": "khosh āmadid",
        "words": [
            {"persian": "خوش", "transliteration": "khosh", "english": "happy / well"},
            {"persian": "آمدید", "transliteration": "āmadid", "english": "you came (formal/plural)"},
        ],
    },
    {
        "id": "khoshbakhtam",
        "category": "greetings",
        "formality": None,
        "persian": "خوشبختم",
        "english": "Pleased to meet you",
        "transliteration": "khoshbakhtam",
        "words": [
            {"persian": "خوشبخت", "transliteration": "khoshbakht", "english": "fortunate / happy"},
            {"persian": "ـم", "transliteration": "-am", "english": "I am"},
        ],
    },
    {
        "id": "esm-e-shoma-chist",
        "category": "greetings",
        "formality": "formal",
        "persian": "اسم شما چیست؟",
        "english": "What is your name? (formal)",
        "transliteration": "esm-e shomā chist?",
        "words": [
            {"persian": "اسم", "transliteration": "esm", "english": "name"},
            {"persian": "شما", "transliteration": "shomā", "english": "your (formal)"},
            {"persian": "چیست", "transliteration": "chist", "english": "what is"},
        ],
    },
    {
        "id": "esmam-ast",
        "category": "greetings",
        "formality": None,
        "persian": "اسم من … است",
        "english": "My name is…",
        "transliteration": "esm-e man … ast",
        "words": [
            {"persian": "اسم", "transliteration": "esm", "english": "name"},
            {"persian": "من", "transliteration": "man", "english": "my / I"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "che-khabar",
        "category": "greetings",
        "formality": "informal",
        "persian": "چه خبر؟",
        "english": "What's up? / What's new? (informal)",
        "transliteration": "che khabar?",
        "words": [
            {"persian": "چه", "transliteration": "che", "english": "what"},
            {"persian": "خبر", "transliteration": "khabar", "english": "news"},
        ],
    },
    # --- Polite ---
    {
        "id": "lotfan",
        "category": "polite",
        "formality": None,
        "persian": "لطفاً",
        "english": "Please",
        "transliteration": "lotfan",
        "words": [
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
        ],
    },
    {
        "id": "moteshakkeram",
        "category": "polite",
        "formality": "formal",
        "persian": "متشکرم",
        "english": "Thank you (formal)",
        "transliteration": "moteshakkeram",
        "words": [
            {"persian": "متشکر", "transliteration": "moteshakker", "english": "grateful"},
            {"persian": "ـم", "transliteration": "-am", "english": "I am"},
        ],
    },
    {
        "id": "mersi",
        "category": "polite",
        "formality": "informal",
        "persian": "مرسی",
        "english": "Thanks (informal, from French merci)",
        "transliteration": "mersi",
        "words": [
            {"persian": "مرسی", "transliteration": "mersi", "english": "thanks"},
        ],
    },
    {
        "id": "mamnun",
        "category": "polite",
        "formality": None,
        "persian": "ممنون",
        "english": "Thanks",
        "transliteration": "mamnun",
        "words": [
            {"persian": "ممنون", "transliteration": "mamnun", "english": "thankful / thanks"},
        ],
    },
    {
        "id": "khahesh-mikonam",
        "category": "polite",
        "formality": None,
        "persian": "خواهش می‌کنم",
        "english": "You're welcome / please (do)",
        "transliteration": "khāhesh mikonam",
        "words": [
            {"persian": "خواهش", "transliteration": "khāhesh", "english": "request / plea"},
            {"persian": "می‌کنم", "transliteration": "mikonam", "english": "I do"},
        ],
    },
    {
        "id": "bebakhshid",
        "category": "polite",
        "formality": None,
        "persian": "ببخشید",
        "english": "Excuse me / sorry",
        "transliteration": "bebakhshid",
        "words": [
            {"persian": "ببخشید", "transliteration": "bebakhshid", "english": "forgive (formal/plural)"},
        ],
    },
    {
        "id": "motaassefam",
        "category": "polite",
        "formality": None,
        "persian": "متأسفم",
        "english": "I'm sorry",
        "transliteration": "mota'assefam",
        "words": [
            {"persian": "متأسف", "transliteration": "mota'assef", "english": "sorry / regretful"},
            {"persian": "ـم", "transliteration": "-am", "english": "I am"},
        ],
    },
    {
        "id": "befarmayid",
        "category": "polite",
        "formality": "formal",
        "persian": "بفرمایید",
        "english": "Please come in / go ahead / after you (formal)",
        "transliteration": "befarmāyid",
        "words": [
            {"persian": "بفرمایید", "transliteration": "befarmāyid", "english": "please (do / enter / speak)"},
        ],
    },
    {
        "id": "khaste-nabashid",
        "category": "polite",
        "formality": None,
        "persian": "خسته نباشید",
        "english": "Well done / thank you for your effort (lit. may you not be tired)",
        "transliteration": "khaste nabāshid",
        "words": [
            {"persian": "خسته", "transliteration": "khaste", "english": "tired"},
            {"persian": "نباشید", "transliteration": "nabāshid", "english": "may you not be (formal)"},
        ],
    },
    {
        "id": "dastetan-dard-nakonad",
        "category": "polite",
        "formality": "formal",
        "persian": "دستتان درد نکند",
        "english": "Thank you for the work (lit. may your hand not hurt)",
        "transliteration": "dastetān dard nakonad",
        "words": [
            {"persian": "دستتان", "transliteration": "dastetān", "english": "your hand (formal)"},
            {"persian": "درد", "transliteration": "dard", "english": "pain"},
            {"persian": "نکند", "transliteration": "nakonad", "english": "may it not do"},
        ],
    },
    {
        "id": "ghabeli-nadarad",
        "category": "polite",
        "formality": None,
        "persian": "قابلی ندارد",
        "english": "Don't mention it / it's nothing",
        "transliteration": "ghābeli nadārad",
        "words": [
            {"persian": "قابلی", "transliteration": "ghābeli", "english": "worth / value"},
            {"persian": "ندارد", "transliteration": "nadārad", "english": "it does not have"},
        ],
    },
    {
        "id": "salamat-bashid",
        "category": "polite",
        "formality": "formal",
        "persian": "سلامت باشید",
        "english": "Take care / stay well",
        "transliteration": "salāmat bāshid",
        "words": [
            {"persian": "سلامت", "transliteration": "salāmat", "english": "health / well-being"},
            {"persian": "باشید", "transliteration": "bāshid", "english": "be (formal/plural)"},
        ],
    },
    {
        "id": "ba-ejaze",
        "category": "polite",
        "formality": None,
        "persian": "با اجازه",
        "english": "Excuse me (to pass / leave)",
        "transliteration": "bā ejāze",
        "words": [
            {"persian": "با", "transliteration": "bā", "english": "with"},
            {"persian": "اجازه", "transliteration": "ejāze", "english": "permission"},
        ],
    },
    {
        "id": "cheshm",
        "category": "polite",
        "formality": "informal",
        "persian": "چشم",
        "english": "Sure / of course (informal; lit. “eye”)",
        "transliteration": "cheshm",
        "words": [
            {"persian": "چشم", "transliteration": "cheshm", "english": "eye; used as “of course”"},
        ],
    },
    # --- Food ---
    {
        "id": "gorosne-am",
        "category": "food",
        "formality": "informal",
        "persian": "گرسنه‌ام",
        "english": "I'm hungry",
        "transliteration": "gorosne-am",
        "words": [
            {"persian": "گرسنه", "transliteration": "gorosne", "english": "hungry"},
            {"persian": "ـام", "transliteration": "-am", "english": "I am"},
        ],
    },
    {
        "id": "teshne-am",
        "category": "food",
        "formality": "informal",
        "persian": "تشنه‌ام",
        "english": "I'm thirsty",
        "transliteration": "teshne-am",
        "words": [
            {"persian": "تشنه", "transliteration": "teshne", "english": "thirsty"},
            {"persian": "ـام", "transliteration": "-am", "english": "I am"},
        ],
    },
    {
        "id": "yek-chay-lotfan",
        "category": "food",
        "formality": None,
        "persian": "یک چای لطفاً",
        "english": "One tea, please",
        "transliteration": "yek chāy lotfan",
        "words": [
            {"persian": "یک", "transliteration": "yek", "english": "one / a"},
            {"persian": "چای", "transliteration": "chāy", "english": "tea"},
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
        ],
    },
    {
        "id": "ab-mikhaham",
        "category": "food",
        "formality": "formal",
        "persian": "آب می‌خواهم",
        "english": "I would like water",
        "transliteration": "āb mikhāham",
        "words": [
            {"persian": "آب", "transliteration": "āb", "english": "water"},
            {"persian": "می‌خواهم", "transliteration": "mikhāham", "english": "I want"},
        ],
    },
    {
        "id": "hesab-lotfan",
        "category": "food",
        "formality": None,
        "persian": "حساب، لطفاً",
        "english": "The bill, please",
        "transliteration": "hesāb, lotfan",
        "words": [
            {"persian": "حساب", "transliteration": "hesāb", "english": "bill / check"},
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
        ],
    },
    {
        "id": "kheyli-khoshmaze-ast",
        "category": "food",
        "formality": None,
        "persian": "خیلی خوشمزه است",
        "english": "It's very delicious",
        "transliteration": "kheyli khoshmaze ast",
        "words": [
            {"persian": "خیلی", "transliteration": "kheyli", "english": "very"},
            {"persian": "خوشمزه", "transliteration": "khoshmaze", "english": "delicious"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "nush-jan",
        "category": "food",
        "formality": None,
        "persian": "نوش جان",
        "english": "Enjoy / bon appétit (said when someone eats or drinks)",
        "transliteration": "nush jān",
        "words": [
            {"persian": "نوش", "transliteration": "nush", "english": "drink / may it be wholesome"},
            {"persian": "جان", "transliteration": "jān", "english": "life / soul"},
        ],
    },
    {
        "id": "nan-mikhaham",
        "category": "food",
        "formality": None,
        "persian": "نان می‌خواهم",
        "english": "I would like bread",
        "transliteration": "nān mikhāham",
        "words": [
            {"persian": "نان", "transliteration": "nān", "english": "bread"},
            {"persian": "می‌خواهم", "transliteration": "mikhāham", "english": "I want"},
        ],
    },
    {
        "id": "in-tond-ast",
        "category": "food",
        "formality": None,
        "persian": "این تند است؟",
        "english": "Is this spicy?",
        "transliteration": "in tond ast?",
        "words": [
            {"persian": "این", "transliteration": "in", "english": "this"},
            {"persian": "تند", "transliteration": "tond", "english": "spicy / hot"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "giyakhvar-hastam",
        "category": "food",
        "formality": None,
        "persian": "گیاه‌خوار هستم",
        "english": "I'm vegetarian",
        "transliteration": "giyākhār hastam",
        "words": [
            {"persian": "گیاه‌خوار", "transliteration": "giyākhār", "english": "vegetarian"},
            {"persian": "هستم", "transliteration": "hastam", "english": "I am"},
        ],
    },
    {
        "id": "bedune-gusht-lotfan",
        "category": "food",
        "formality": None,
        "persian": "بدون گوشت، لطفاً",
        "english": "Without meat, please",
        "transliteration": "bedun-e gusht, lotfan",
        "words": [
            {"persian": "بدون", "transliteration": "bedun", "english": "without"},
            {"persian": "گوشت", "transliteration": "gusht", "english": "meat"},
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
        ],
    },
    {
        "id": "qahve-darid",
        "category": "food",
        "formality": "formal",
        "persian": "قهوه دارید؟",
        "english": "Do you have coffee? (formal/plural)",
        "transliteration": "qahve dārid?",
        "words": [
            {"persian": "قهوه", "transliteration": "qahve", "english": "coffee"},
            {"persian": "دارید", "transliteration": "dārid", "english": "you have (formal)"},
        ],
    },
    {
        "id": "yek-ab-mive-lotfan",
        "category": "food",
        "formality": None,
        "persian": "یک آب‌میوه لطفاً",
        "english": "One juice, please",
        "transliteration": "yek āb-mive lotfan",
        "words": [
            {"persian": "یک", "transliteration": "yek", "english": "one / a"},
            {"persian": "آب‌میوه", "transliteration": "āb-mive", "english": "juice"},
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
        ],
    },
    # --- Travel ---
    {
        "id": "forudgah-kojast",
        "category": "travel",
        "formality": None,
        "persian": "فرودگاه کجاست؟",
        "english": "Where is the airport?",
        "transliteration": "forudgāh kojāst?",
        "words": [
            {"persian": "فرودگاه", "transliteration": "forudgāh", "english": "airport"},
            {"persian": "کجاست", "transliteration": "kojāst", "english": "where is"},
        ],
    },
    {
        "id": "yek-belit-lotfan",
        "category": "travel",
        "formality": None,
        "persian": "یک بلیط لطفاً",
        "english": "One ticket, please",
        "transliteration": "yek belit lotfan",
        "words": [
            {"persian": "یک", "transliteration": "yek", "english": "one / a"},
            {"persian": "بلیط", "transliteration": "belit", "english": "ticket"},
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
        ],
    },
    {
        "id": "taksi-mikhaham",
        "category": "travel",
        "formality": None,
        "persian": "تاکسی می‌خواهم",
        "english": "I would like a taxi",
        "transliteration": "tāksi mikhāham",
        "words": [
            {"persian": "تاکسی", "transliteration": "tāksi", "english": "taxi"},
            {"persian": "می‌خواهم", "transliteration": "mikhāham", "english": "I want"},
        ],
    },
    {
        "id": "gom-shode-am",
        "category": "travel",
        "formality": None,
        "persian": "گم شده‌ام",
        "english": "I'm lost",
        "transliteration": "gom shode-am",
        "words": [
            {"persian": "گم", "transliteration": "gom", "english": "lost"},
            {"persian": "شده‌ام", "transliteration": "shode-am", "english": "I have become"},
        ],
    },
    {
        "id": "dastshuyi-kojast",
        "category": "travel",
        "formality": None,
        "persian": "دستشویی کجاست؟",
        "english": "Where is the restroom?",
        "transliteration": "dastshuyi kojāst?",
        "words": [
            {"persian": "دستشویی", "transliteration": "dastshuyi", "english": "restroom"},
            {"persian": "کجاست", "transliteration": "kojāst", "english": "where is"},
        ],
    },
    {
        "id": "cheghadr-ast",
        "category": "travel",
        "formality": None,
        "persian": "چقدر است؟",
        "english": "How much is it?",
        "transliteration": "cheghadr ast?",
        "words": [
            {"persian": "چقدر", "transliteration": "cheghadr", "english": "how much"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "kheyli-geran-ast",
        "category": "travel",
        "formality": None,
        "persian": "خیلی گران است",
        "english": "It's very expensive",
        "transliteration": "kheyli gerān ast",
        "words": [
            {"persian": "خیلی", "transliteration": "kheyli", "english": "very"},
            {"persian": "گران", "transliteration": "gerān", "english": "expensive"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "chap-bepichid",
        "category": "travel",
        "formality": "formal",
        "persian": "به چپ بپیچید",
        "english": "Turn left",
        "transliteration": "be chap bepichid",
        "words": [
            {"persian": "به", "transliteration": "be", "english": "to"},
            {"persian": "چپ", "transliteration": "chap", "english": "left"},
            {"persian": "بپیچید", "transliteration": "bepichid", "english": "turn (formal/plural)"},
        ],
    },
    {
        "id": "rast-bepichid",
        "category": "travel",
        "formality": "formal",
        "persian": "به راست بپیچید",
        "english": "Turn right",
        "transliteration": "be rāst bepichid",
        "words": [
            {"persian": "به", "transliteration": "be", "english": "to"},
            {"persian": "راست", "transliteration": "rāst", "english": "right"},
            {"persian": "بپیچید", "transliteration": "bepichid", "english": "turn (formal/plural)"},
        ],
    },
    {
        "id": "istgah-metro-kojast",
        "category": "travel",
        "formality": None,
        "persian": "ایستگاه مترو کجاست؟",
        "english": "Where is the metro station?",
        "transliteration": "istgāh-e metro kojāst?",
        "words": [
            {"persian": "ایستگاه", "transliteration": "istgāh", "english": "station"},
            {"persian": "مترو", "transliteration": "metro", "english": "metro / subway"},
            {"persian": "کجاست", "transliteration": "kojāst", "english": "where is"},
        ],
    },
    {
        "id": "otagh-mikhaham",
        "category": "travel",
        "formality": None,
        "persian": "اتاق می‌خواهم",
        "english": "I would like a room",
        "transliteration": "otāgh mikhāham",
        "words": [
            {"persian": "اتاق", "transliteration": "otāgh", "english": "room"},
            {"persian": "می‌خواهم", "transliteration": "mikhāham", "english": "I want"},
        ],
    },
    {
        "id": "rezerv-daram",
        "category": "travel",
        "formality": None,
        "persian": "رزرو دارم",
        "english": "I have a reservation",
        "transliteration": "rezerv dāram",
        "words": [
            {"persian": "رزرو", "transliteration": "rezerv", "english": "reservation"},
            {"persian": "دارم", "transliteration": "dāram", "english": "I have"},
        ],
    },
    {
        "id": "komak",
        "category": "travel",
        "formality": None,
        "persian": "کمک!",
        "english": "Help!",
        "transliteration": "komak!",
        "words": [
            {"persian": "کمک", "transliteration": "komak", "english": "help"},
        ],
    },
    # --- Daily ---
    {
        "id": "bale",
        "category": "daily",
        "formality": None,
        "persian": "بله",
        "english": "Yes",
        "transliteration": "bale",
        "words": [
            {"persian": "بله", "transliteration": "bale", "english": "yes"},
        ],
    },
    {
        "id": "na",
        "category": "daily",
        "formality": None,
        "persian": "نه",
        "english": "No",
        "transliteration": "na",
        "words": [
            {"persian": "نه", "transliteration": "na", "english": "no"},
        ],
    },
    {
        "id": "bashe",
        "category": "daily",
        "formality": "informal",
        "persian": "باشه",
        "english": "Okay (informal)",
        "transliteration": "bāshe",
        "words": [
            {"persian": "باشه", "transliteration": "bāshe", "english": "okay / all right"},
        ],
    },
    {
        "id": "nemifahmam",
        "category": "daily",
        "formality": None,
        "persian": "نمی‌فهمم",
        "english": "I don't understand",
        "transliteration": "nemifahmam",
        "words": [
            {"persian": "نمی‌فهمم", "transliteration": "nemifahmam", "english": "I do not understand"},
        ],
    },
    {
        "id": "aheste-tar-sohbat-konid",
        "category": "daily",
        "formality": "formal",
        "persian": "لطفاً آهسته‌تر صحبت کنید",
        "english": "Please speak more slowly",
        "transliteration": "lotfan āheste-tar sohbat konid",
        "words": [
            {"persian": "لطفاً", "transliteration": "lotfan", "english": "please"},
            {"persian": "آهسته‌تر", "transliteration": "āheste-tar", "english": "more slowly"},
            {"persian": "صحبت", "transliteration": "sohbat", "english": "speech / talk"},
            {"persian": "کنید", "transliteration": "konid", "english": "do (formal/plural)"},
        ],
    },
    {
        "id": "englisi-beladid",
        "category": "daily",
        "formality": "formal",
        "persian": "انگلیسی بلدید؟",
        "english": "Do you speak English? (formal)",
        "transliteration": "englisi beladid?",
        "words": [
            {"persian": "انگلیسی", "transliteration": "englisi", "english": "English"},
            {"persian": "بلدید", "transliteration": "beladid", "english": "do you know how (formal)"},
        ],
    },
    {
        "id": "kami-farsi-beladam",
        "category": "daily",
        "formality": None,
        "persian": "کمی فارسی بلدم",
        "english": "I speak a little Persian",
        "transliteration": "kami fārsi beladam",
        "words": [
            {"persian": "کمی", "transliteration": "kami", "english": "a little"},
            {"persian": "فارسی", "transliteration": "fārsi", "english": "Persian"},
            {"persian": "بلدم", "transliteration": "beladam", "english": "I know how"},
        ],
    },
    {
        "id": "saat-chande",
        "category": "daily",
        "formality": "informal",
        "persian": "ساعت چنده؟",
        "english": "What time is it? (informal)",
        "transliteration": "sā'at chande?",
        "words": [
            {"persian": "ساعت", "transliteration": "sā'at", "english": "hour / clock / time"},
            {"persian": "چنده", "transliteration": "chande", "english": "how much is it?"},
        ],
    },
    {
        "id": "hava-kheyli-garm-ast",
        "category": "daily",
        "formality": None,
        "persian": "هوا خیلی گرم است",
        "english": "The weather is very hot",
        "transliteration": "havā kheyli garm ast",
        "words": [
            {"persian": "هوا", "transliteration": "havā", "english": "weather / air"},
            {"persian": "خیلی", "transliteration": "kheyli", "english": "very"},
            {"persian": "گرم", "transliteration": "garm", "english": "hot / warm"},
            {"persian": "است", "transliteration": "ast", "english": "is"},
        ],
    },
    {
        "id": "baran-mibarad",
        "category": "daily",
        "formality": None,
        "persian": "باران می‌بارد",
        "english": "It's raining",
        "transliteration": "bārān mibārad",
        "words": [
            {"persian": "باران", "transliteration": "bārān", "english": "rain"},
            {"persian": "می‌بارد", "transliteration": "mibārad", "english": "it falls / is raining"},
        ],
    },
    {
        "id": "farda-mibinamet",
        "category": "daily",
        "formality": "informal",
        "persian": "فردا می‌بینمت",
        "english": "See you tomorrow (informal)",
        "transliteration": "fardā mibinamet",
        "words": [
            {"persian": "فردا", "transliteration": "fardā", "english": "tomorrow"},
            {"persian": "می‌بینمت", "transliteration": "mibinamet", "english": "I will see you"},
        ],
    },
    {
        "id": "dustet-daram",
        "category": "daily",
        "formality": "informal",
        "persian": "دوستت دارم",
        "english": "I love you (informal)",
        "transliteration": "dustet dāram",
        "words": [
            {"persian": "دوستت", "transliteration": "dustet", "english": "your friend / you (object)"},
            {"persian": "دارم", "transliteration": "dāram", "english": "I have / I hold"},
        ],
    },
    {
        "id": "tavallodet-mobarak",
        "category": "daily",
        "formality": "informal",
        "persian": "تولدت مبارک",
        "english": "Happy birthday (informal)",
        "transliteration": "tavallodet mobārak",
        "words": [
            {"persian": "تولدت", "transliteration": "tavallodet", "english": "your birthday"},
            {"persian": "مبارک", "transliteration": "mobārak", "english": "blessed / congratulations"},
        ],
    },
    {
        "id": "mitavanam-komak-konam",
        "category": "daily",
        "formality": "formal",
        "persian": "می‌توانم کمک کنم؟",
        "english": "Can I help?",
        "transliteration": "mitavānam komak konam?",
        "words": [
            {"persian": "می‌توانم", "transliteration": "mitavānam", "english": "I can"},
            {"persian": "کمک", "transliteration": "komak", "english": "help"},
            {"persian": "کنم", "transliteration": "konam", "english": "I do"},
        ],
    },
    {
        "id": "internet-darid",
        "category": "daily",
        "formality": "formal",
        "persian": "اینترنت دارید؟",
        "english": "Do you have internet? (formal)",
        "transliteration": "internet dārid?",
        "words": [
            {"persian": "اینترنت", "transliteration": "internet", "english": "internet"},
            {"persian": "دارید", "transliteration": "dārid", "english": "you have (formal)"},
        ],
    },
    {
        "id": "kojā-zendegi-mikoni",
        "category": "daily",
        "formality": "informal",
        "persian": "کجا زندگی می‌کنی؟",
        "english": "Where do you live? (informal)",
        "transliteration": "kojā zendegi mikoni?",
        "words": [
            {"persian": "کجا", "transliteration": "kojā", "english": "where"},
            {"persian": "زندگی", "transliteration": "zendegi", "english": "life"},
            {"persian": "می‌کنی", "transliteration": "mikoni", "english": "you do (informal)"},
        ],
    },
    {
        "id": "man-az-amrika-hastam",
        "category": "daily",
        "formality": None,
        "persian": "من از آمریکا هستم",
        "english": "I'm from the United States",
        "transliteration": "man az āmrikā hastam",
        "words": [
            {"persian": "من", "transliteration": "man", "english": "I"},
            {"persian": "از", "transliteration": "az", "english": "from"},
            {"persian": "آمریکا", "transliteration": "āmrikā", "english": "America / USA"},
            {"persian": "هستم", "transliteration": "hastam", "english": "I am"},
        ],
    },
]


def _norm_fa(text: str) -> str:
    return " ".join(text.replace("ي", "ی").replace("ك", "ک").split())


def main() -> None:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from phrase_expansion import expand_catalog

    catalog = list(PHRASES) + expand_catalog()

    by_id: dict[str, dict] = {}
    seen_fa: set[str] = set()
    unique: list[dict] = []
    for phrase in catalog:
        fa = _norm_fa(phrase["persian"])
        if fa in seen_fa:
            continue
        pid = phrase["id"]
        if pid in by_id:
            n = 2
            while f"{pid}-{n}" in by_id:
                n += 1
            pid = f"{pid}-{n}"
            phrase = {**phrase, "id": pid}
        by_id[pid] = phrase
        seen_fa.add(fa)
        unique.append(phrase)

    assert len(unique) >= 1000, f"need at least 1000 phrases, got {len(unique)}"
    for phrase in unique:
        assert phrase["persian"] and phrase["english"] and phrase["transliteration"], phrase["id"]
        assert phrase["words"], phrase["id"]
        assert phrase["category"], phrase["id"]
        for word in phrase["words"]:
            assert word["persian"] and word["transliteration"] and word["english"], phrase["id"]

    out = Path(__file__).resolve().parents[1] / "PersianPhrasesKit" / "Sources" / "PersianPhrasesKit" / "Resources" / "phrases.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(unique, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cats: dict[str, int] = {}
    for p in unique:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    print(f"Wrote {len(unique)} phrases to {out}")
    print("by category:", dict(sorted(cats.items())))


if __name__ == "__main__":
    main()
