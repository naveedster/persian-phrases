"""Generate concepts.json + per-language translation files for Daily Phrases."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from languages import LANG_CODES, NON_LATIN, language_payload
from lexicon import (
    BODY,
    COUNTRIES,
    DAYS,
    DRINKS,
    E,
    FEELINGS,
    FOOD,
    FOOD_DRINK,
    HOURS,
    MONTHS,
    PEOPLE,
    PLACES,
    SHOP,
    TRANSPORT,
    WEATHER,
    WORK,
    english_key,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "PersianPhrasesKit" / "Sources" / "PersianPhrasesKit" / "Resources"
NO_SPACE = {"zh-Hans", "ja", "th"}

# Question punctuation
Q_PREFIX = {"es": "¿"}
Q_SUFFIX = {code: "؟" for code in ("fa", "ar", "ur")} | {"el": ";", "es": "?"}


def slug(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
    return s[:72] or "phrase"


def form(entry: dict, lang: str) -> tuple[str, str | None]:
    return entry[lang]


def word_obj(text: str, tr: str | None, english: str, lang: str) -> dict:
    obj: dict = {"text": text, "english": english}
    if lang in NON_LATIN and tr:
        obj["transliteration"] = tr
    return obj


def join_text(lang: str, pieces: list[str]) -> str:
    sep = "" if lang in NO_SPACE else " "
    return sep.join(p for p in pieces if p)


def join_tr(lang: str, pieces: list[str | None]) -> str | None:
    if lang not in NON_LATIN:
        return None
    parts = [p for p in pieces if p]
    return " ".join(parts) if parts else None


def apply_question(lang: str, text: str) -> str:
    prefix = Q_PREFIX.get(lang, "")
    suffix = Q_SUFFIX.get(lang, "?")
    if text.endswith(("?", "؟", ";", "？")):
        return prefix + text if prefix and not text.startswith("¿") else text
    return f"{prefix}{text}{suffix}"


# --- Function / frame parts (gloss is English) ---
P = {
    "want": E("I want", fa="می‌خواهم|mikhāham", ar="أريد|urīd", zh="我想要|wǒ xiǎng yào", ja="が欲しいです|ga hoshii desu", ko="주세요|juseyo", hi="चाहिए|chāhiye", ru="Я хочу|ya khochu", th="อยากได้|yàak dâi", el="Θέλω|Thélo", he="אני רוצה|ani rotzé", uk="Я хочу|ya khochu", ur="چاہیے|chāhiye", bn="চাই|chai", es="Quiero", fr="Je voudrais", de="Ich möchte", pt="Eu quero", it="Vorrei", tr="istiyorum", vi="Tôi muốn", idn="Saya ingin", pl="Chcę", nl="Ik wil", sv="Jag vill ha", ro="Aș vrea", cs="Chtěl bych", hu="Kérek", ms="Saya mahu", fil="Gusto ko ng", sw="Nataka"),
    "want_inf": E("I want (informal)", fa="می‌خوام|mikhām", ar="بدي|biddī", zh="我要|wǒ yào", ja="が欲しい|ga hoshii", ko="줘|jwo", hi="चाहिए|chāhiye", ru="Хочу|khochu", th="เอา|ao", el="Θέλω|Thélo", he="אני רוצה|ani rotzé", uk="Хочу|khochu", ur="چاہیے|chāhiye", bn="চাই|chai", es="Quiero", fr="Je veux", de="Ich will", pt="Quero", it="Voglio", tr="istiyorum", vi="Tôi muốn", idn="Saya mau", pl="Chcę", nl="Ik wil", sv="Jag vill ha", ro="Vreau", cs="Chci", hu="Kérek", ms="Saya nak", fil="Gusto ko", sw="Nataka"),
    "please": E("please", fa="لطفاً|lotfan", ar="من فضلك|min faḍlik", zh="请|qǐng", ja="お願いします|onegaishimasu", ko="주세요|juseyo", hi="कृपया|kṛpayā", ru="пожалуйста|pozhaluysta", th="กรุณา|karúnaa", el="παρακαλώ|parakaló", he="בבקשה|bevakahá", uk="будь ласка|bud' laska", ur="براہ کرم|barāh-e karam", bn="দয়া করে|doya kore", es="por favor", fr="s'il vous plaît", de="bitte", pt="por favor", it="per favore", tr="lütfen", vi="làm ơn", idn="tolong", pl="proszę", nl="alsjeblieft", sv="tack", ro="te rog", cs="prosím", hu="kérem", ms="tolong", fil="please", sw="tafadhali"),
    "one": E("one / a", fa="یک|yek", ar="واحد|wāḥid", zh="一个|yí ge", ja="一つ|hitotsu", ko="하나|hana", hi="एक|ek", ru="один|odin", th="หนึ่ง|nʉ̀ng", el="ένα|éna", he="אחד|ekhád", uk="один|odyn", ur="ایک|ek", bn="এক|ek", es="un", fr="un", de="ein", pt="um", it="un", tr="bir", vi="một", idn="satu", pl="jeden", nl="een", sv="en", ro="un", cs="jeden", hu="egy", ms="satu", fil="isang", sw="moja"),
    "have_you": E("do you have", fa="دارید|dārid", ar="هل لديك|hal ladayk", zh="你有|nǐ yǒu", ja="はありますか|wa arimasu ka", ko="있어요?|isseoyo", hi="क्या आपके पास है|kyā āpke pās hai", ru="У вас есть|u vas yest'", th="มีไหม|mii mǎi", el="Έχετε|Échete", he="יש לך|yesh lekhá", uk="У вас є|u vas ye", ur="کیا آپ کے پاس ہے|kyā āp ke pās hai", bn="আপনার কি আছে|apnar ki ache", es="¿Tiene", fr="Avez-vous", de="Haben Sie", pt="Você tem", it="Ha", tr="var mı", vi="Bạn có", idn="Apakah Anda punya", pl="Czy ma pan", nl="Heeft u", sv="Har du", ro="Aveți", cs="Máte", hu="Van", ms="Ada ke", fil="Mayroon ka bang", sw="Una"),
    "this_is": E("this is", fa="این … است|in … ast", ar="هذا|hādhā", zh="这是|zhè shì", ja="これは|kore wa", ko="이것은|igeoseun", hi="यह है|yah hai", ru="Это|eto", th="นี่คือ|nîi khʉʉ", el="Αυτό είναι|Aftó eínai", he="זה|ze", uk="Це|tse", ur="یہ ہے|yeh hai", bn="এটা|eta", es="Esto es", fr="C'est", de="Das ist", pt="Isto é", it="Questo è", tr="Bu", vi="Đây là", idn="Ini", pl="To jest", nl="Dit is", sv="Det här är", ro="Acesta este", cs="Tohle je", hu="Ez", ms="Ini ialah", fil="Ito ay", sw="Hiki ni"),
    "is": E("is", fa="است|ast", ar="هو|huwa", zh="是|shì", ja="です|desu", ko="입니다|imnida", hi="है|hai", ru="это|eto", th="คือ|khʉʉ", el="είναι|eínai", he="זה|ze", uk="є|ye", ur="ہے|hai", bn="হয়|hoy", es="es", fr="est", de="ist", pt="é", it="è", tr="dır", vi="là", idn="adalah", pl="jest", nl="is", sv="är", ro="este", cs="je", hu="ez", ms="ialah", fil="ay", sw="ni"),
    "delicious": E("is delicious", fa="خیلی خوشمزه است|kheyli khoshmaze ast", ar="لذيذ جدا|ladhīdh jiddan", zh="很好吃|hěn hǎochī", ja="とても美味しいです|totemo oishii desu", ko="정말 맛있어요|jeongmal masisseoyo", hi="बहुत स्वादिष्ट है|bahut svādiṣṭ hai", ru="очень вкусный|ochen' vkusnyy", th="อร่อยมาก|aròi mâak", el="είναι πολύ νόστιμο|eínai polý nóstimo", he="טעים מאוד|ta'ím me'ód", uk="дуже смачний|duzhe smachnyy", ur="بہت مزیدار ہے|bohat mazīdār hai", bn="খুব সুস্বাদু|khub suswadu", es="está delicioso", fr="est délicieux", de="ist sehr lecker", pt="está delicioso", it="è delizioso", tr="çok lezzetli", vi="rất ngon", idn="sangat enak", pl="jest pyszny", nl="is heerlijk", sv="är jättegott", ro="este delicios", cs="je výborný", hu="nagyon finom", ms="sangat sedap", fil="masarap", sw="ni kitamu sana"),
    "without": E("without", fa="بدون|bedun", ar="بدون|bidūn", zh="不要|bú yào", ja="抜きで|nuki de", ko="빼 주세요|ppae juseyo", hi="बिना|binā", ru="без|bez", th="ไม่ใส่|mâi sài", el="χωρίς|chorís", he="בלי|bli", uk="без|bez", ur="کے بغیر|ke baghair", bn="ছাড়া|chhara", es="sin", fr="sans", de="ohne", pt="sem", it="senza", tr="olmadan", vi="không", idn="tanpa", pl="bez", nl="zonder", sv="utan", ro="fără", cs="bez", hu="nélkül", ms="tanpa", fil="walang", sw="bila"),
    "like": E("I like", fa="دوست دارم|dust dāram", ar="أحب|uḥibb", zh="我喜欢|wǒ xǐhuan", ja="が好きです|ga suki desu", ko="좋아해요|joahaeyo", hi="मुझे पसंद है|mujhe pasand hai", ru="Мне нравится|mne nravitsya", th="ฉันชอบ|chăn chɔ̂ɔp", el="Μου αρέσει|Mou arései", he="אני אוהב|ani ohév", uk="Мені подобається|meni podobayet'sya", ur="مجھے پسند ہے|mujhe pasand hai", bn="আমি পছন্দ করি|ami pochhondo kori", es="Me gusta", fr="J'aime", de="Ich mag", pt="Eu gosto de", it="Mi piace", tr="seviyorum", vi="Tôi thích", idn="Saya suka", pl="Lubię", nl="Ik hou van", sv="Jag gillar", ro="Îmi place", cs="Mám rád", hu="Szeretem", ms="Saya suka", fil="Gusto ko ang", sw="Napenda"),
    "dont_eat": E("I don't eat", fa="نمی‌خورم|nemikhoram", ar="لا آكل|lā ākul", zh="我不吃|wǒ bù chī", ja="は食べません|wa tabemasen", ko="안 먹어요|an meogeoyo", hi="मैं नहीं खाता|main nahī̃ khātā", ru="Я не ем|ya ne yem", th="ฉันไม่กิน|chăn mâi kin", el="Δεν τρώω|Den tróo", he="אני לא אוכל|ani lo okhél", uk="Я не їм|ya ne yim", ur="میں نہیں کھاتا|main nahī̃ khātā", bn="আমি খাই না|ami khai na", es="No como", fr="Je ne mange pas", de="Ich esse kein", pt="Eu não como", it="Non mangio", tr="yemem", vi="Tôi không ăn", idn="Saya tidak makan", pl="Nie jem", nl="Ik eet geen", sv="Jag äter inte", ro="Nu mănânc", cs="Nejím", hu="Nem eszem", ms="Saya tidak makan", fil="Hindi ako kumakain ng", sw="Sili"),
    "more": E("more, please", fa="بیشتر لطفاً|bishtar lotfan", ar="المزيد من فضلك|al-mazīd min faḍlik", zh="再来一点|zài lái yìdiǎn", ja="もっとください|motto kudasai", ko="더 주세요|deo juseyo", hi="और दीजिए|aur dījiye", ru="ещё, пожалуйста|yeshchyo pozhaluysta", th="ขออีก|khɔ̌ɔ ìik", el="ακόμα παρακαλώ|akóma parakaló", he="עוד בבקשה|od bevakahá", uk="ще, будь ласка|shche bud' laska", ur="اور دیں|aur deñ", bn="আর দিন|ar din", es="más, por favor", fr="encore, s'il vous plaît", de="noch mehr, bitte", pt="mais, por favor", it="ancora, per favore", tr="biraz daha lütfen", vi="thêm nữa", idn="tambah, tolong", pl="jeszcze, proszę", nl="meer, alsjeblieft", sv="mer, tack", ro="încă, te rog", cs="ještě, prosím", hu="még, kérem", ms="lagi, tolong", fil="dagdag pa", sw="zaidi, tafadhali"),
    "where_is": E("where is", fa="کجاست|kojāst", ar="أين|ayna", zh="在哪里|zài nǎlǐ", ja="はどこですか|wa doko desu ka", ko="어디예요|eodiyeyo", hi="कहाँ है|kahā̃ hai", ru="Где|gde", th="อยู่ที่ไหน|yùu thîi nǎi", el="Πού είναι|Poú eínai", he="איפה|éifo", uk="Де|de", ur="کہاں ہے|kahā̃ hai", bn="কোথায়|kothay", es="Dónde está", fr="Où est", de="Wo ist", pt="Onde fica", it="Dov'è", tr="nerede", vi="Ở đâu", idn="Di mana", pl="Gdzie jest", nl="Waar is", sv="Var är", ro="Unde este", cs="Kde je", hu="Hol van", ms="Di manakah", fil="Nasaan ang", sw="Iko wapi"),
    "going": E("I'm going to", fa="می‌روم به|miravam be", ar="أنا ذاهب إلى|anā dhāhib ilā", zh="我去|wǒ qù", ja="に行きます|ni ikimasu", ko="에 가요|e gayo", hi="मैं जा रहा हूँ|main jā rahā hū̃", ru="Я иду в|ya idu v", th="ฉันไป|chăn pai", el="Πάω στο|Páo sto", he="אני הולך ל|ani holékh le", uk="Я йду до|ya ydu do", ur="میں جا رہا ہوں|main jā rahā hū̃", bn="আমি যাচ্ছি|ami jacchi", es="Voy a", fr="Je vais à", de="Ich gehe zu", pt="Vou para", it="Vado a", tr="gidiyorum", vi="Tôi đi đến", idn="Saya pergi ke", pl="Idę do", nl="Ik ga naar", sv="Jag går till", ro="Merg la", cs="Jdu do", hu="Megyek a", ms="Saya pergi ke", fil="Pupunta ako sa", sw="Naenda"),
    "nearby": E("is nearby", fa="نزدیک است|nazdik ast", ar="قريب|qarīb", zh="很近|hěn jìn", ja="は近いです|wa chikai desu", ko="가까워요|gakkawoyo", hi="पास है|pās hai", ru="рядом|ryadom", th="อยู่ใกล้|yùu glâi", el="είναι κοντά|eínai kontá", he="קרוב|karóv", uk="поруч|poruch", ur="قریب ہے|qarīb hai", bn="কাছে|kache", es="está cerca", fr="est tout près", de="ist in der Nähe", pt="fica perto", it="è vicino", tr="yakın", vi="ở gần", idn="dekat", pl="jest blisko", nl="is dichtbij", sv="är nära", ro="este aproape", cs="je blízko", hu="közel van", ms="dekat", fil="malapit", sw="ni karibu"),
    "came_from": E("I came from", fa="آمدم از|āmadam az", ar="أتيت من|ataytu min", zh="我从…来|wǒ cóng … lái", ja="から来ました|kara kimashita", ko="에서 왔어요|eseo wasseoyo", hi="मैं … से आया हूँ|main … se āyā hū̃", ru="Я пришёл из|ya prishël iz", th="ฉันมาจาก|chăn maa jàak", el="Ήρθα από|Írtha apó", he="באתי מ|bati mi", uk="Я прийшов з|ya pryyshov z", ur="میں … سے آیا ہوں|main … se āyā hū̃", bn="আমি … থেকে এসেছি|ami theke esechi", es="Vengo de", fr="Je viens de", de="Ich komme von", pt="Eu vim de", it="Vengo da", tr="geldim", vi="Tôi đến từ", idn="Saya datang dari", pl="Przyjechałem z", nl="Ik kom van", sv="Jag kommer från", ro="Vin de la", cs="Přijel jsem z", hu="Érkeztem", ms="Saya datang dari", fil="Galing ako sa", sw="Nimetoka"),
    "how_get": E("how do I get to", fa="چطور بروم به|chetor beravam be", ar="كيف أصل إلى|kayfa aṣilu ilā", zh="怎么去|zěnme qù", ja="にはどう行きますか|ni wa dō ikimasu ka", ko="어떻게 가요|eotteoke gayo", hi="कैसे जाऊँ|kaise jāū̃", ru="Как пройти к|kak proyti k", th="ไปยังไง|pai yang ngai", el="Πώς πάω στο|Pós páo sto", he="איך מגיעים ל|ekh magi'ím le", uk="Як дістатися до|yak distatysya do", ur="کیسے جاؤں|kaise jāū̃", bn="কীভাবে যাব|kibhabe jabo", es="Cómo llego a", fr="Comment aller à", de="Wie komme ich zu", pt="Como chego a", it="Come arrivo a", tr="nasıl giderim", vi="Làm sao đến", idn="Bagaimana ke", pl="Jak dotrzeć do", nl="Hoe kom ik bij", sv="Hur kommer jag till", ro="Cum ajung la", cs="Jak se dostanu do", hu="Hogyan jutok a", ms="Macam mana ke", fil="Paano pumunta sa", sw="Nifikaje"),
    "is_open": E("is it open", fa="باز است|bāz ast", ar="هل هو مفتوح|hal huwa maftūḥ", zh="开门吗|kāi mén ma", ja="は開いていますか|wa aite imasu ka", ko="열렸어요|yeollyeosseoyo", hi="खुला है|khulā hai", ru="открыто|otkryto", th="เปิดไหม|pə̀ət mǎi", el="Είναι ανοιχτό|Eínai anoichtó", he="פתוח|patúakh", uk="відчинено|vidchyneno", ur="کھلا ہے|khulā hai", bn="খোলা কি|khola ki", es="está abierto", fr="est ouvert", de="hat geöffnet", pt="está aberto", it="è aperto", tr="açık mı", vi="có mở không", idn="buka", pl="jest otwarte", nl="is open", sv="har öppet", ro="este deschis", cs="je otevřeno", hu="nyitva van", ms="buka ke", fil="bukas ba", sw="imefunguliwa"),
    "is_far": E("is far", fa="دور است|dur ast", ar="بعيد|baʿīd", zh="很远|hěn yuǎn", ja="は遠いです|wa tōi desu", ko="멀어요|meoreoyo", hi="दूर है|dūr hai", ru="далеко|daleko", th="ไกล|glai", el="είναι μακριά|eínai makriá", he="רחוק|rakhók", uk="далеко|daleko", ur="دور ہے|dūr hai", bn="দূরে|dure", es="está lejos", fr="est loin", de="ist weit", pt="fica longe", it="è lontano", tr="uzak", vi="ở xa", idn="jauh", pl="jest daleko", nl="is ver", sv="är långt borta", ro="este departe", cs="je daleko", hu="messze van", ms="jauh", fil="malayo", sw="ni mbali"),
    "is_closed": E("is closed", fa="بسته است|baste ast", ar="مغلق|mughlaq", zh="关门了|guān mén le", ja="は閉まっています|wa shimatte imasu", ko="닫았어요|dadasseoyo", hi="बंद है|band hai", ru="закрыто|zakryto", th="ปิด|pìt", el="είναι κλειστό|eínai kleistó", he="סגור|sagúr", uk="зачинено|zachyneno", ur="بند ہے|band hai", bn="বন্ধ|bondho", es="está cerrado", fr="est fermé", de="ist geschlossen", pt="está fechado", it="è chiuso", tr="kapalı", vi="đã đóng", idn="tutup", pl="jest zamknięte", nl="is dicht", sv="har stängt", ro="este închis", cs="je zavřeno", hu="zárva van", ms="tutup", fil="sarado", sw="imefungwa"),
    "meet_me": E("meet me at", fa="ملاقات کنیم در|molāghāt konim dar", ar="قابلني في|qābilnī fī", zh="在…见|zài … jiàn", ja="で会いましょう|de aimashō", ko="에서 만나요|eseo mannayo", hi="मुझसे मिलो|mujhse milo", ru="Встретимся у|vstretimsya u", th="เจอกันที่|jəə gan thîi", el="Βρεθείτε μου στο|Vretheíte mou sto", he="תיפגש איתי ב|tipagesh ití be", uk="Зустрінемось біля|zustrinemos' bilya", ur="ملو مجھ سے|milo mujh se", bn="আমার সাথে দেখা|amar sathe dekha", es="Encuéntrame en", fr="Retrouve-moi à", de="Treffen Sie mich bei", pt="Encontre-me no", it="Incontrami a", tr="buluşalım", vi="Gặp tôi ở", idn="Temui saya di", pl="Spotkajmy się przy", nl="Ontmoet me bij", sv="Träffa mig vid", ro="Ne întâlnim la", cs="Sejdeme se u", hu="Találkozzunk a", ms="Jumpa saya di", fil="Hanapin mo ako sa", sw="Nikutane"),
    "how_much": E("how much is this", fa="این … چند است|in … chand ast", ar="بكم هذا|bikam hādhā", zh="这个多少钱|zhège duōshǎo qián", ja="これはいくらですか|kore wa ikura desu ka", ko="이거 얼마예요|igeo eolmayeyo", hi="यह कितने का है|yah kitne kā hai", ru="Сколько стоит этот|skol'ko stoit etot", th="อันนี้เท่าไหร่|an níi thâo rài", el="Πόσο κάνει αυτό|Póso kánει aftó", he="כמה זה|káma ze", uk="Скільки коштує цей|skil'ky koshtuye tsey", ur="یہ کتنے کا ہے|yeh kitne kā hai", bn="এটার দাম কত|etar dam koto", es="Cuánto cuesta este", fr="Combien coûte ce", de="Was kostet dieses", pt="Quanto custa este", it="Quanto costa questo", tr="bu kaç para", vi="Cái này bao nhiêu", idn="Berapa harga", pl="Ile kosztuje ten", nl="Hoeveel kost deze", sv="Vad kostar den här", ro="Cât costă acest", cs="Kolik stojí tenhle", hu="Mennyibe kerül ez a", ms="Berapa harga", fil="Magkano ang", sw="Bei gani hii"),
    "expensive": E("is expensive", fa="گران است|gerān ast", ar="غالٍ|ghālin", zh="很贵|hěn guì", ja="は高いです|wa takai desu", ko="비싸요|bissayo", hi="महंगा है|mahaṅgā hai", ru="дорогой|dorogoy", th="แพง|phɛɛng", el="είναι ακριβό|eínai akrivó", he="יקר|yakár", uk="дорогий|dorohyy", ur="مہنگا ہے|mahangā hai", bn="দামি|dami", es="es caro", fr="est cher", de="ist teuer", pt="é caro", it="è caro", tr="pahalı", vi="đắt", idn="mahal", pl="jest drogi", nl="is duur", sv="är dyr", ro="este scump", cs="je drahý", hu="drága", ms="mahal", fil="mahal", sw="ni ghali"),
    "smaller": E("a smaller one", fa="کوچک‌تر دارید|kuchek-tar dārid", ar="أصغر|aṣghar", zh="有小一点的吗|yǒu xiǎo yìdiǎn de ma", ja="の小さいのはありますか|no chiisai no wa arimasu ka", ko="더 작은 거 있어요|deo jageun geo isseoyo", hi="छोटा है क्या|choṭā hai kyā", ru="есть меньше|yest' men'she", th="มีไซส์เล็กกว่าไหม|mii sái lék gwàa mǎi", el="μικρότερο|mikrótero", he="יש יותר קטן|yesh yoter katán", uk="є менший|ye menshyy", ur="چھوٹا ہے|choṭā hai", bn="ছোট আছে|chhoto ache", es="más pequeño", fr="plus petit", de="eine kleinere", pt="menor", it="più piccolo", tr="daha küçük", vi="nhỏ hơn", idn="yang lebih kecil", pl="mniejszy", nl="een kleinere", sv="en mindre", ro="mai mic", cs="menší", hu="kisebb", ms="yang lebih kecil", fil="mas maliit", sw="ndogo zaidi"),
    "i_take": E("I'll take", fa="برمی‌دارم|barmidāram", ar="سآخذ|sa'ākhudh", zh="我要这个|wǒ yào zhège", ja="にします|ni shimasu", ko="이걸로 할게요|igeollo halgeyo", hi="मैं यह लूँगा|main yah lū̃gā", ru="Я возьму|ya voz'mu", th="เอาอันนี้|ao an níi", el="Θα πάρω|Tha páro", he="אני אקח|ani ekákh", uk="Я візьму|ya viz'mu", ur="میں یہ لوں گا|main yeh lū̃gā", bn="আমি নেব|ami nebo", es="Me llevo", fr="Je prends", de="Ich nehme", pt="Eu levo", it="Prendo", tr="alacağım", vi="Tôi lấy", idn="Saya ambil", pl="Wezmę", nl="Ik neem", sv="Jag tar", ro="Iau", cs="Vezmu si", hu="Elvisszem", ms="Saya ambil", fil="Kukunin ko", sw="Nitachukua"),
    "cheap": E("is cheap", fa="ارزان است|arzān ast", ar="رخيص|rakhīṣ", zh="很便宜|hěn piányi", ja="は安いです|wa yasui desu", ko="싸요|ssayo", hi="सस्ता है|sastā hai", ru="дешёвый|deshovyy", th="ถูก|thùuk", el="είναι φθηνό|eínai fthinó", he="זול|zol", uk="дешевий|deshevyy", ur="سستا ہے|sastā hai", bn="সস্তা|sosta", es="es barato", fr="est bon marché", de="ist günstig", pt="é barato", it="è economico", tr="ucuz", vi="rẻ", idn="murah", pl="jest tani", nl="is goedkoop", sv="är billig", ro="este ieftin", cs="je levný", hu="olcsó", ms="murah", fil="mura", sw="ni nafuu"),
    "i_bought": E("I bought", fa="خریدم|kharidam", ar="اشتريت|ishtaraytu", zh="我买了|wǒ mǎi le", ja="を買いました|o kaimashita", ko="샀어요|sasseoyo", hi="मैंने खरीदा|maine kharīdā", ru="Я купил|ya kupil", th="ฉันซื้อ|chăn súue", el="Αγόρασα|Agórasa", he="קניתי|kaníti", uk="Я купив|ya kupyv", ur="میں نے خریدا|maine kharīdā", bn="আমি কিনেছি|ami kinechi", es="Compré", fr="J'ai acheté", de="Ich habe gekauft", pt="Eu comprei", it="Ho comprato", tr="aldım", vi="Tôi đã mua", idn="Saya membeli", pl="Kupiłem", nl="Ik heb gekocht", sv="Jag köpte", ro="Am cumpărat", cs="Koupil jsem", hu="Vettem", ms="Saya beli", fil="Bumili ako ng", sw="Nilinunua"),
    "dont_need": E("I don't need", fa="لازم ندارم|lāzem nadāram", ar="لا أحتاج|lā aḥtāj", zh="我不需要|wǒ bù xūyào", ja="は要りません|wa irimasen", ko="필요 없어요|piryo eopseoyo", hi="मुझे ज़रूरत नहीं|mujhe zarūrat nahī̃", ru="Мне не нужно|mne ne nuzhno", th="ฉันไม่ต้องการ|chăn mâi tông gaan", el="Δεν χρειάζομαι|Den chreiázomai", he="אני לא צריך|ani lo tsaríkh", uk="Мені не потрібно|meni ne potribno", ur="مجھے ضرورت نہیں|mujhe zarūrat nahī̃", bn="আমার দরকার নেই|amar darkar nei", es="No necesito", fr="Je n'ai pas besoin de", de="Ich brauche kein", pt="Eu não preciso de", it="Non ho bisogno di", tr="gerek yok", vi="Tôi không cần", idn="Saya tidak perlu", pl="Nie potrzebuję", nl="Ik heb geen … nodig", sv="Jag behöver inte", ro="Nu am nevoie de", cs="Nepotřebuji", hu="Nincs szükségem", ms="Saya tidak perlukan", fil="Hindi ko kailangan ang", sw="Sitaki"),
    "i_love": E("I love", fa="را دوست دارم|rā dust dāram", ar="أحب|uḥibb", zh="我爱|wǒ ài", ja="を愛しています|o aishite imasu", ko="사랑해요|saranghaeyo", hi="मुझे प्यार है|mujhe pyār hai", ru="Я люблю|ya lyublyu", th="ฉันรัก|chăn rák", el="Αγαπώ|Agapó", he="אני אוהב|ani ohév", uk="Я люблю|ya lyublyu", ur="میں محبت کرتا ہوں|main muhabbat kartā hū̃", bn="আমি ভালোবাসি|ami bhalobashi", es="Quiero a", fr="J'aime", de="Ich liebe", pt="Eu amo", it="Amo", tr="seviyorum", vi="Tôi yêu", idn="Saya mencintai", pl="Kocham", nl="Ik hou van", sv="Jag älskar", ro="Iubesc", cs="Miluji", hu="Szeretem", ms="Saya sayang", fil="Mahal ko", sw="Nampenda"),
    "waiting": E("I'm waiting for", fa="منتظرم|montazeram", ar="أنتظر|antaẓiru", zh="我在等|wǒ zài děng", ja="を待っています|o matte imasu", ko="기다리고 있어요|gidarigo isseoyo", hi="मैं इंतज़ार कर रहा हूँ|main intazār kar rahā hū̃", ru="Я жду|ya zhdu", th="ฉันรอ|chăn rɔɔ", el="Περιμένω|Periméno", he="אני מחכה ל|ani mekhaké le", uk="Я чекаю|ya chekayu", ur="میں انتظار کر رہا ہوں|main intizār kar rahā hū̃", bn="আমি অপেক্ষা করছি|ami opekkha korchi", es="Estoy esperando a", fr="J'attends", de="Ich warte auf", pt="Estou esperando", it="Aspetto", tr="bekliyorum", vi="Tôi đang chờ", idn="Saya menunggu", pl="Czekam na", nl="Ik wacht op", sv="Jag väntar på", ro="Aștept", cs="Čekám na", hu="Várok a", ms="Saya tunggu", fil="Hinihintay ko", sw="Ninasubiri"),
    "i_am": E("I am", fa="هستم|hastam", ar="أنا|anā", zh="我很|wǒ hěn", ja="です|desu", ko="이에요|ieyo", hi="मैं हूँ|main hū̃", ru="Я|ya", th="ฉัน|chăn", el="Είμαι|Eímai", he="אני|ani", uk="Я|ya", ur="میں ہوں|main hū̃", bn="আমি|ami", es="Estoy", fr="Je suis", de="Ich bin", pt="Estou", it="Sono", tr="im", vi="Tôi", idn="Saya", pl="Jestem", nl="Ik ben", sv="Jag är", ro="Sunt", cs="Jsem", hu="vagyok", ms="Saya", fil="Ako ay", sw="Mimi ni"),
    "i_am_very": E("I am very", fa="خیلی …‌ام|kheyli …-am", ar="أنا جدا|anā jiddan", zh="我非常|wǒ fēicháng", ja="とても…です|totemo … desu", ko="정말 …해요|jeongmal …haeyo", hi="मैं बहुत|main bahut", ru="Я очень|ya ochen'", th="ฉัน…มาก|chăn … mâak", el="Είμαι πολύ|Eímai polý", he="אני מאוד|ani me'ód", uk="Я дуже|ya duzhe", ur="میں بہت|main bohat", bn="আমি খুব|ami khub", es="Estoy muy", fr="Je suis très", de="Ich bin sehr", pt="Estou muito", it="Sono molto", tr="çok …im", vi="Tôi rất", idn="Saya sangat", pl="Jestem bardzo", nl="Ik ben heel", sv="Jag är väldigt", ro="Sunt foarte", cs="Jsem velmi", hu="Nagyon … vagyok", ms="Saya sangat", fil="Napakaka", sw="Mimi ni sana"),
    "why_are": E("why are you", fa="چرا هستید|cherā hastid", ar="لماذا أنت|limādhā anta", zh="你为什么|nǐ wèishéme", ja="なぜ…ですか|naze … desu ka", ko="왜 …예요|wae …yeyo", hi="आप क्यों हैं|āp kyõ haĩ", ru="Почему вы|pochemu vy", th="ทำไมคุณ|thammai khun", el="Γιατί είσαι|Giatí eísai", he="למה אתה|láma atá", uk="Чому ви|chomu vy", ur="آپ کیوں ہیں|āp kyõ haĩ", bn="আপনি কেন|apni keno", es="Por qué está", fr="Pourquoi êtes-vous", de="Warum sind Sie", pt="Por que você está", it="Perché sei", tr="neden siniz", vi="Tại sao bạn", idn="Mengapa Anda", pl="Dlaczego jesteś", nl="Waarom bent u", sv="Varför är du", ro="De ce ești", cs="Proč jste", hu="Miért vagy", ms="Mengapa anda", fil="Bakit ka", sw="Kwa nini wewe ni"),
    "dont_be": E("don't be", fa="نباش|nabāsh", ar="لا تكن|lā takun", zh="别|bié", ja="しないで|shinaide", ko="하지 마세요|haji maseyo", hi="मत होइए|mat hoiye", ru="Не будь|ne bud'", th="อย่า|yàa", el="Μην είσαι|Min eísai", he="אל תהיה|al tihyé", uk="Не будь|ne bud'", ur="مت بنو|mat bano", bn="হয়ো না|hoyona", es="No estés", fr="Ne sois pas", de="Sei nicht", pt="Não fique", it="Non essere", tr="olma", vi="Đừng", idn="Jangan", pl="Nie bądź", nl="Wees niet", sv="Var inte", ro="Nu fi", cs="Nebuď", hu="Ne légy", ms="Jangan", fil="Huwag kang", sw="Usiwe"),
    "weather_is": E("the weather is", fa="هوا … است|havā … ast", ar="الطقس|al-ṭaqs", zh="天气|tiānqì", ja="天気は|tenki wa", ko="날씨가|nalssiga", hi="मौसम|mausam", ru="Погода|pogoda", th="อากาศ|ʔaakàat", el="Ο καιρός είναι|O kairós eínai", he="מזג האוויר|mezeg ha'avír", uk="Погода|pohoda", ur="موسم|mausam", bn="আবহাওয়া|abohawa", es="El tiempo está", fr="Il fait", de="Das Wetter ist", pt="O tempo está", it="Il tempo è", tr="hava", vi="Thời tiết", idn="Cuacanya", pl="Pogoda jest", nl="Het weer is", sv="Vädret är", ro="Vremea este", cs="Počasí je", hu="Az idő", ms="Cuaca", fil="Ang panahon ay", sw="Hali ya hewa ni"),
    "today": E("today", fa="امروز|emruz", ar="اليوم|al-yawm", zh="今天|jīntiān", ja="今日|kyō", ko="오늘|oneul", hi="आज|āj", ru="сегодня|segodnya", th="วันนี้|wan níi", el="σήμερα|símera", he="היום|hayóm", uk="сьогодні|s'ohodni", ur="آج|āj", bn="আজ|aj", es="hoy", fr="aujourd'hui", de="heute", pt="hoje", it="oggi", tr="bugün", vi="hôm nay", idn="hari ini", pl="dzisiaj", nl="vandaag", sv="idag", ro="astăzi", cs="dnes", hu="ma", ms="hari ini", fil="ngayon", sw="leo"),
    "tomorrow": E("tomorrow", fa="فردا|fardā", ar="غدا|ghadan", zh="明天|míngtiān", ja="明日|ashita", ko="내일|naeil", hi="कल|kal", ru="завтра|zavtra", th="พรุ่งนี้|phrûng níi", el="αύριο|ávrio", he="מחר|makhár", uk="завтра|zavtra", ur="کل|kal", bn="কাল|kal", es="mañana", fr="demain", de="morgen", pt="amanhã", it="domani", tr="yarın", vi="ngày mai", idn="besok", pl="jutro", nl="morgen", sv="imorgon", ro="mâine", cs="zítra", hu="holnap", ms="esok", fil="bukas", sw="kesho"),
    "hurts": E("hurts", fa="درد می‌کند|dard mikonad", ar="يؤلمني|yu'limunī", zh="疼|téng", ja="が痛いです|ga itai desu", ko="아파요|apayo", hi="दर्द करता है|dard kartā hai", ru="болит|bolit", th="เจ็บ|jèp", el="πονάει|ponáei", he="כואב|ko'év", uk="болить|bolyt'", ur="درد کرتا ہے|dard kartā hai", bn="ব্যথা করে|byatha kore", es="me duele", fr="me fait mal", de="tut weh", pt="dói", it="fa male", tr="ağrıyor", vi="bị đau", idn="sakit", pl="boli", nl="doet pijn", sv="gör ont", ro="mă doare", cs="bolí", hu="fáj", ms="sakit", fil="masakit", sw="inauma"),
    "not_well": E("is not well", fa="خوب نیست|khub nist", ar="ليس بخير|laysa bikhayr", zh="不舒服|bù shūfu", ja="の調子が悪いです|no chōshi ga warui desu", ko="안 좋아요|an joayo", hi="ठीक नहीं है|ṭhīk nahī̃ hai", ru="не в порядке|ne v poryadke", th="ไม่ค่อยดี|mâi khôi dii", el="δεν είναι καλά|den eínai kalá", he="לא בסדר|lo beséder", uk="недобре|nedobre", ur="ٹھیک نہیں|ṭhīk nahī̃", bn="ভালো নয়|bhalo noy", es="no está bien", fr="ne va pas bien", de="ist nicht gut", pt="não está bem", it="non sta bene", tr="iyi değil", vi="không khỏe", idn="tidak baik", pl="nie jest w porządku", nl="is niet goed", sv="mår inte bra", ro="nu e bine", cs="není v pořádku", hu="nincs jól", ms="tidak sihat", fil="hindi maayos", sw="si vizuri"),
    "i_have": E("I have a", fa="دارم|dāram", ar="لدي|ladayya", zh="我有|wǒ yǒu", ja="があります|ga arimasu", ko="있어요|isseoyo", hi="मेरे पास है|mere pās hai", ru="У меня есть|u menya yest'", th="ฉันมี|chăn mii", el="Έχω|Écho", he="יש לי|yesh li", uk="У мене є|u mene ye", ur="میرے پاس ہے|mere pās hai", bn="আমার আছে|amar ache", es="Tengo", fr="J'ai", de="Ich habe", pt="Eu tenho", it="Ho", tr="var", vi="Tôi có", idn="Saya punya", pl="Mam", nl="Ik heb", sv="Jag har", ro="Am", cs="Mám", hu="Van", ms="Saya ada", fil="Mayroon akong", sw="Nina"),
    "when_is": E("when is", fa="کی است|key ast", ar="متى|matā", zh="什么时候|shénme shíhou", ja="はいつですか|wa itsu desu ka", ko="언제예요|eonjeyeyo", hi="कब है|kab hai", ru="Когда|kogda", th="เมื่อไหร่|mûea rài", el="Πότε είναι|Póte eínai", he="מתי|matái", uk="Коли|koly", ur="کب ہے|kab hai", bn="কখন|kokhon", es="Cuándo es", fr="Quand est", de="Wann ist", pt="Quando é", it="Quando è", tr="ne zaman", vi="Khi nào", idn="Kapan", pl="Kiedy jest", nl="Wanneer is", sv="När är", ro="Când este", cs="Kdy je", hu="Mikor van", ms="Bila", fil="Kailan ang", sw="Ni lini"),
    "i_finished": E("I finished", fa="را تمام کردم|rā tamām kardam", ar="أنهيت|anhaytu", zh="我做完了|wǒ zuò wán le", ja="を終えました|o oemashita", ko="끝냈어요|kkeunnaesseoyo", hi="मैंने पूरा किया|maine pūrā kiyā", ru="Я закончил|ya zakonchil", th="ฉันทำเสร็จ|chăn tham sèt", el="Τελείωσα|Teleíosa", he="סיימתי|siyámti", uk="Я закінчив|ya zakinchyv", ur="میں نے مکمل کیا|maine mukammal kiyā", bn="আমি শেষ করেছি|ami shesh korechi", es="Terminé", fr="J'ai fini", de="Ich habe fertig", pt="Eu terminei", it="Ho finito", tr="bitirdim", vi="Tôi đã xong", idn="Saya selesai", pl="Skończyłem", nl="Ik ben klaar met", sv="Jag är klar med", ro="Am terminat", cs="Dokončil jsem", hu="Befejeztem", ms="Saya siap", fil="Tapos ko na ang", sw="Nimemaliza"),
    "im_from": E("I'm from", fa="هستم از|hastam az", ar="أنا من|anā min", zh="我来自|wǒ láizì", ja="出身です|shusshin desu", ko="에서 왔어요|eseo wasseoyo", hi="मैं … से हूँ|main … se hū̃", ru="Я из|ya iz", th="ฉันมาจาก|chăn maa jàak", el="Είμαι από|Eímai apó", he="אני מ|ani mi", uk="Я з|ya z", ur="میں … سے ہوں|main … se hū̃", bn="আমি … থেকে|ami theke", es="Soy de", fr="Je viens de", de="Ich komme aus", pt="Eu sou de", it="Sono di", tr="liyim", vi="Tôi đến từ", idn="Saya dari", pl="Jestem z", nl="Ik kom uit", sv="Jag kommer från", ro="Sunt din", cs="Jsem z", hu="…-ból jövök", ms="Saya dari", fil="Taga", sw="Nimetoka"),
    "want_go": E("I want to go to", fa="می‌خواهم بروم به|mikhāham beravam be", ar="أريد أن أذهب إلى|urīd an adhhab ilā", zh="我想去|wǒ xiǎng qù", ja="に行きたいです|ni ikitai desu", ko="에 가고 싶어요|e gago sipeoyo", hi="मैं जाना चाहता हूँ|main jānā chāhtā hū̃", ru="Я хочу поехать в|ya khochu poyekhat' v", th="ฉันอยากไป|chăn yàak pai", el="Θέλω να πάω στην|Thélo na páo stin", he="אני רוצה לנסוע ל|ani rotzé linsoa le", uk="Я хочу поїхати до|ya khochu poyikhaty do", ur="میں جانا چاہتا ہوں|main jānā chāhtā hū̃", bn="আমি যেতে চাই|ami jete chai", es="Quiero ir a", fr="Je veux aller en", de="Ich möchte nach … fahren", pt="Eu quero ir para", it="Voglio andare in", tr="gitmek istiyorum", vi="Tôi muốn đi đến", idn="Saya ingin pergi ke", pl="Chcę pojechać do", nl="Ik wil naar … gaan", sv="Jag vill åka till", ro="Vreau să merg în", cs="Chci jet do", hu="Szeretnék menni", ms="Saya mahu pergi ke", fil="Gusto kong pumunta sa", sw="Ninataka kwenda"),
    "i_live": E("I live in", fa="زندگی می‌کنم در|zendegi mikonam dar", ar="أسكن في|askunu fī", zh="我住在|wǒ zhù zài", ja="に住んでいます|ni sunde imasu", ko="에 살아요|e sarayo", hi="मैं रहता हूँ|main rahtā hū̃", ru="Я живу в|ya zhivu v", th="ฉันอยู่ที่|chăn yùu thîi", el="Μένω στην|Méno stin", he="אני גר ב|ani gar be", uk="Я живу в|ya zhyvu v", ur="میں رہتا ہوں|main rahtā hū̃", bn="আমি থাকি|ami thaki", es="Vivo en", fr="J'habite en", de="Ich wohne in", pt="Eu moro em", it="Vivo in", tr="yaşıyorum", vi="Tôi sống ở", idn="Saya tinggal di", pl="Mieszkam w", nl="Ik woon in", sv="Jag bor i", ro="Locuiesc în", cs="Bydlím v", hu="Lakom", ms="Saya tinggal di", fil="Nakatira ako sa", sw="Ninaishi"),
    "i_drink": E("I drink", fa="می‌نوشم|minusham", ar="أشرب|ashrab", zh="我喝|wǒ hē", ja="を飲みます|o nomimasu", ko="마셔요|masyeoyo", hi="मैं पीता हूँ|main pītā hū̃", ru="Я пью|ya p'yu", th="ฉันดื่ม|chăn dùuem", el="Πίνω|Píno", he="אני שותה|ani shoté", uk="Я п'ю|ya p'yu", ur="میں پیتا ہوں|main pītā hū̃", bn="আমি খাই|ami khai", es="Bebo", fr="Je bois", de="Ich trinke", pt="Eu bebo", it="Bevo", tr="içerim", vi="Tôi uống", idn="Saya minum", pl="Piję", nl="Ik drink", sv="Jag dricker", ro="Beau", cs="Piju", hu="Iszom", ms="Saya minum", fil="Umiinom ako ng", sw="Nanywa"),
    "i_ate": E("I ate", fa="خوردم|khordam", ar="أكلت|akaltu", zh="我吃了|wǒ chī le", ja="を食べました|o tabemashita", ko="먹었어요|meogeosseoyo", hi="मैंने खाया|maine khāyā", ru="Я ел|ya yel", th="ฉันกิน|chăn kin", el="Έφαγα|Éfaga", he="אכלתי|akhálti", uk="Я їв|ya yiv", ur="میں نے کھایا|maine khāyā", bn="আমি খেয়েছি|ami kheyechi", es="Comí", fr="J'ai mangé", de="Ich habe gegessen", pt="Eu comi", it="Ho mangiato", tr="yedim", vi="Tôi đã ăn", idn="Saya makan", pl="Zjadłem", nl="Ik heb gegeten", sv="Jag åt", ro="Am mâncat", cs="Snědl jsem", hu="Ettem", ms="Saya makan", fil="Kumain ako ng", sw="Nilikula"),
    "please_bring": E("please bring", fa="بیاورید لطفاً|biyāvarid lotfan", ar="أحضر من فضلك|aḥḍir min faḍlik", zh="请拿来|qǐng ná lái", ja="を持ってきてください|o motte kite kudasai", ko="가져다 주세요|gajyeoda juseyo", hi="लाइए|lāie", ru="принесите, пожалуйста|prinesite pozhaluysta", th="เอามาให้หน่อย|ao maa hâi nòi", el="Φέρτε παρακαλώ|Férte parakaló", he="תביא בבקשה|taví bevakahá", uk="принесіть, будь ласка|prynesit' bud' laska", ur="لائیے|lāiye", bn="আনুন|anun", es="Traiga", fr="Apportez", de="Bitte bringen Sie", pt="Traga", it="Porti", tr="getirin lütfen", vi="Làm ơn mang", idn="Tolong bawa", pl="Proszę przynieść", nl="Breng alstublieft", sv="Ta med", ro="Aduceți", cs="Přineste prosím", hu="Hozza el", ms="Tolong bawa", fil="Pakikuha ang", sw="Tafadhali leta"),
    "can_i_have": E("can I have", fa="می‌توانم … داشته باشم|mitavānam … dāshte bāsham", ar="هل يمكنني الحصول على|hal yumkinunī al-ḥuṣūl ʿalā", zh="我可以要|wǒ kěyǐ yào", ja="をいただけますか|o itadakemasu ka", ko="주실래요|jushillaeyo", hi="क्या मुझे मिल सकता है|kyā mujhe mil saktā hai", ru="Можно мне|mozhno mne", th="ขอได้ไหม|khɔ̌ɔ dâi mǎi", el="Μπορώ να έχω|Boró na écho", he="אפשר לקבל|efshár lekabél", uk="Можна мені|mozhna meni", ur="کیا مجھے مل سکتا ہے|kyā mujhe mil saktā hai", bn="আমি কি পেতে পারি|ami ki pete pari", es="Puedo tomar", fr="Puis-je avoir", de="Kann ich … haben", pt="Posso ter", it="Posso avere", tr="alabilir miyim", vi="Cho tôi xin", idn="Boleh saya minta", pl="Czy mogę dostać", nl="Mag ik", sv="Kan jag få", ro="Pot să am", cs="Mohu dostat", hu="Kaphatok", ms="Boleh saya dapat", fil="Pwede ba akong kumuha ng", sw="Naweza pata"),
    "is_spicy": E("is spicy", fa="تند است|tond ast", ar="حار|ḥārr", zh="很辣|hěn là", ja="は辛いです|wa karai desu", ko="매워요|maewoyo", hi="तीखा है|tīkhā hai", ru="острый|ostryy", th="เผ็ด|phèt", el="είναι καυτερό|eínai kafteó", he="חריף|kharíf", uk="гострий|hostryy", ur="مرچ دار ہے|mirch dār hai", bn="ঝাল|jhal", es="está picante", fr="est épicé", de="ist scharf", pt="está apimentado", it="è piccante", tr="acı", vi="cay", idn="pedas", pl="jest ostry", nl="is pittig", sv="är stark", ro="este iute", cs="je pálivý", hu="csípős", ms="pedas", fil="maanghang", sw="ni kali"),
    "is_cold_food": E("is cold", fa="سرد است|sard ast", ar="بارد|bārid", zh="是凉的|shì liáng de", ja="は冷たいです|wa tsumetai desu", ko="차가워요|chagawoyo", hi="ठंडा है|ṭhaṇḍā hai", ru="холодный|kholodnyy", th="เย็น|yen", el="είναι κρύο|eínai krýo", he="קר|kar", uk="холодний|kholodnyy", ur="ٹھنڈا ہے|ṭhaṇḍā hai", bn="ঠান্ডা|thanda", es="está frío", fr="est froid", de="ist kalt", pt="está frio", it="è freddo", tr="soğuk", vi="lạnh", idn="dingin", pl="jest zimny", nl="is koud", sv="är kall", ro="este rece", cs="je studený", hu="hideg", ms="sejuk", fil="malamig", sw="ni baridi"),
    "is_hot_food": E("is hot", fa="داغ است|dāgh ast", ar="ساخن|sākhin", zh="是热的|shì rè de", ja="は熱いです|wa atsui desu", ko="뜨거워요|tteugeowoyo", hi="गरम है|garam hai", ru="горячий|goryachiy", th="ร้อน|rɔ́ɔn", el="είναι ζεστό|eínai zestó", he="חם|kham", uk="гарячий|haryachyy", ur="گرم ہے|garm hai", bn="গরম|gorom", es="está caliente", fr="est chaud", de="ist heiß", pt="está quente", it="è caldo", tr="sıcak", vi="nóng", idn="panas", pl="jest gorący", nl="is heet", sv="är varm", ro="este cald", cs="je horký", hu="forró", ms="panas", fil="mainit", sw="ni moto"),
    "ticket_for": E("a ticket for", fa="بلیط … می‌خواهم|belit … mikhāham", ar="تذكرة إلى|tadhkira ilā", zh="一张去…的票|yì zhāng qù … de piào", ja="の切符をください|no kippu o kudasai", ko="표 주세요|pyo juseyo", hi="का टिकट|kā ṭikaṭ", ru="билет на|bilet na", th="ตั๋วไป|tǔa pai", el="ένα εισιτήριο για|éna eisitírio gia", he="כרטיס ל|kartís le", uk="квиток на|kvytok na", ur="کا ٹکٹ|kā ṭikaṭ", bn="টিকিট|ticket", es="un billete para", fr="un billet pour", de="eine Fahrkarte nach", pt="uma passagem para", it="un biglietto per", tr="bileti lütfen", vi="một vé", idn="tiket ke", pl="bilet na", nl="een kaartje voor", sv="en biljett till", ro="un bilet pentru", cs="jízdenku na", hu="jegyet", ms="tiket ke", fil="isang tiket para sa", sw="tiketi ya"),
    "oclock": E("o'clock", fa="ساعت … است|sā'at … ast", ar="الساعة|al-sāʿa", zh="点|diǎn", ja="時です|ji desu", ko="시예요|siyeyo", hi="बजे हैं|baje haĩ", ru="час|chas", th="นาฬิกา|naalíkaa", el="η ώρα είναι|i óra eínai", he="השעה|hasha'á", uk="година|hodyna", ur="بجے ہیں|baje haĩ", bn="টা বাজে|ta baje", es="son las", fr="il est", de="es ist … Uhr", pt="são", it="sono le", tr="saat", vi="giờ", idn="pukul", pl="jest godzina", nl="het is … uur", sv="klockan är", ro="este ora", cs="je … hodin", hu="óra van", ms="pukul", fil="alas", sw="saa"),
    "wait_min": E("please wait … minutes", fa="دقیقه صبر کنید|daqiqe sabr konid", ar="دقائق من فضلك|daqāʾiq min faḍlik", zh="请等…分钟|qǐng děng … fēnzhōng", ja="分待ってください|fun matte kudasai", ko="분만 기다려 주세요|bunman gidaryeo juseyo", hi="मिनट रुकिए|minaṭ rukiye", ru="минут подождите|minut podozhdite", th="นาที กรุณารอ|naathii karúnaa rɔɔ", el="λεπτά παρακαλώ|leptá parakaló", he="דקות בבקשה|dakót bevakahá", uk="хвилин зачекайте|khvylyn zachekaite", ur="منٹ انتظار کیجئے|minaṭ intizār kījiye", bn="মিনিট অপেক্ষা করুন|minute", es="minutos, por favor", fr="minutes, s'il vous plaît", de="Minuten, bitte", pt="minutos, por favor", it="minuti, per favore", tr="dakika bekleyin", vi="phút, làm ơn", idn="menit, tolong", pl="minut, proszę", nl="minuten, alstublieft", sv="minuter, tack", ro="minute, te rog", cs="minut, prosím", hu="percet várjon", ms="minit, tolong", fil="minuto, please", sw="dakika, tafadhali"),
    "i_need": E("I need", fa="لازم دارم|lāzem dāram", ar="أحتاج|aḥtāj", zh="我需要|wǒ xūyào", ja="が必要です|ga hitsuyō desu", ko="필요해요|piryohaeyo", hi="मुझे ज़रूरत है|mujhe zarūrat hai", ru="Мне нужно|mne nuzhno", th="ฉันต้องการ|chăn tông gaan", el="Χρειάζομαι|Chreiázomai", he="אני צריך|ani tsaríkh", uk="Мені потрібно|meni potribno", ur="مجھے ضرورت ہے|mujhe zarūrat hai", bn="আমার দরকার|amar darkar", es="Necesito", fr="J'ai besoin de", de="Ich brauche", pt="Eu preciso de", it="Ho bisogno di", tr="lazım", vi="Tôi cần", idn="Saya perlu", pl="Potrzebuję", nl="Ik heb … nodig", sv="Jag behöver", ro="Am nevoie de", cs="Potřebuji", hu="Szükségem van", ms="Saya perlukan", fil="Kailangan ko ng", sw="Nahitaji"),
}

# Languages that put the noun before the verb-like predicate
ITEM_FIRST = {
    "fa", "ja", "ko", "hi", "tr", "ur", "bn",
}
# Exceptions per frame id
ITEM_FIRST_EXCEPT = {
    "im_from": set(),  # many are preposition-first
    "want_go": {"fa", "ja", "ko", "hi", "tr", "ur", "bn"},
}


def part_first(frame_id: str, lang: str) -> bool:
    if frame_id in ITEM_FIRST_EXCEPT:
        return lang in ITEM_FIRST_EXCEPT[frame_id]
    return lang in ITEM_FIRST


def build_phrase(frame_id: str, part_key: str, item: dict, lang: str, question: bool = False) -> tuple[str, str | None, list[dict]]:
    item_text, item_tr = form(item, lang)
    item_en = english_key(item)
    pred_text, pred_tr = form(P[part_key], lang)
    pred_en = english_key(P[part_key])
    item_word = word_obj(item_text, item_tr, item_en, lang)
    pred_word = word_obj(pred_text, pred_tr, pred_en, lang)
    if part_first(frame_id, lang):
        words = [item_word, pred_word]
        text = join_text(lang, [item_text, pred_text])
        tr = join_tr(lang, [item_tr, pred_tr])
    else:
        words = [pred_word, item_word]
        text = join_text(lang, [pred_text, item_text])
        tr = join_tr(lang, [pred_tr, item_tr])
    if question:
        text = apply_question(lang, text)
        if tr and lang in NON_LATIN:
            tr = tr.rstrip("?؟;") + ("?" if lang not in ("fa", "ar", "ur") else "")
    return text, tr, words


def add_please(lang: str, text: str, tr: str | None, words: list[dict]) -> tuple[str, str | None, list[dict]]:
    p_text, p_tr = form(P["please"], lang)
    p_word = word_obj(p_text, p_tr, "please", lang)
    if lang in NO_SPACE:
        text = text + p_text
    else:
        text = f"{text} {p_text}"
    if tr and p_tr:
        tr = f"{tr} {p_tr}"
    words = words + [p_word]
    return text, tr, words


FRAMES = [
    # food / drink
    ("want", "food", "formal", "I would like {item}", "want", FOOD_DRINK, False, False),
    ("want-inf", "food", "informal", "I want {item} (informal)", "want_inf", FOOD_DRINK, False, False),
    ("one", "food", None, "One {item}, please", "one", FOOD_DRINK, False, True),
    ("have", "food", "formal", "Do you have {item}?", "have_you", FOOD_DRINK, True, False),
    ("this-is", "food", None, "This is {item}", "this_is", FOOD_DRINK, False, False),
    ("more", "food", None, "More {item}, please", "more", FOOD_DRINK, False, False),
    ("can-have", "food", "formal", "Can I have {item}?", "can_i_have", FOOD_DRINK, True, False),
    ("need-food", "food", None, "I need {item}", "i_need", FOOD_DRINK, False, False),
    ("tasty", "food", None, "The {item} is delicious", "delicious", FOOD, False, False),
    ("without", "food", None, "Without {item}, please", "without", FOOD, False, True),
    ("like", "food", None, "I like {item}", "like", FOOD, False, False),
    ("dont-eat", "food", None, "I don't eat {item}", "dont_eat", FOOD, False, False),
    ("ate", "food", None, "I ate {item}", "i_ate", FOOD, False, False),
    ("bring", "food", "formal", "Please bring {item}", "please_bring", FOOD, False, False),
    ("spicy", "food", None, "The {item} is spicy", "is_spicy", FOOD, False, False),
    ("cold-food", "food", None, "The {item} is cold", "is_cold_food", FOOD, False, False),
    ("hot-food", "food", None, "The {item} is hot", "is_hot_food", FOOD, False, False),
    ("drink", "food", None, "I drink {item}", "i_drink", DRINKS, False, False),
    # travel / places
    ("where", "travel", None, "Where is {item}?", "where_is", PLACES, True, False),
    ("going", "travel", None, "I'm going to {item}", "going", PLACES, False, False),
    ("near", "travel", None, "{item} is nearby", "nearby", PLACES, False, False),
    ("from", "travel", None, "I came from {item}", "came_from", PLACES, False, False),
    ("how", "travel", None, "How do I get to {item}?", "how_get", PLACES, True, False),
    ("open", "travel", None, "Is {item} open?", "is_open", PLACES, True, False),
    ("far", "travel", None, "{item} is far", "is_far", PLACES, False, False),
    ("closed", "travel", None, "{item} is closed", "is_closed", PLACES, False, False),
    ("meet", "travel", None, "Meet me at {item}", "meet_me", PLACES, False, False),
    # shopping
    ("price", "shopping", None, "How much is this {item}?", "how_much", SHOP, True, False),
    ("buy", "shopping", "formal", "I would like the {item}", "want", SHOP, False, False),
    ("exp", "shopping", None, "This {item} is expensive", "expensive", SHOP, False, False),
    ("smaller", "shopping", "formal", "Do you have a smaller {item}?", "smaller", SHOP, True, False),
    ("take", "shopping", None, "I'll take the {item}", "i_take", SHOP, False, False),
    ("cheap", "shopping", None, "This {item} is cheap", "cheap", SHOP, False, False),
    ("bought", "shopping", None, "I bought a {item}", "i_bought", SHOP, False, False),
    ("need-not", "shopping", None, "I don't need {item}", "dont_need", SHOP, False, False),
    # family
    ("fam-where", "family", None, "Where is {item}?", "where_is", PEOPLE, True, False),
    ("fam-love", "family", None, "I love {item}", "i_love", PEOPLE, False, False),
    ("fam-this", "family", None, "This is {item}", "this_is", PEOPLE, False, False),
    ("fam-wait", "family", None, "I'm waiting for {item}", "waiting", PEOPLE, False, False),
    ("fam-need", "family", None, "I need {item}", "i_need", PEOPLE, False, False),
    # feelings
    ("feel", "feelings", None, "I am {item}", "i_am", FEELINGS, False, False),
    ("feel-very", "feelings", "informal", "I am very {item}", "i_am_very", FEELINGS, False, False),
    ("feel-why", "feelings", "formal", "Why are you {item}?", "why_are", FEELINGS, True, False),
    ("feel-dont", "feelings", None, "Don't be {item}", "dont_be", FEELINGS, False, False),
    # weather
    ("wx", "weather", None, "The weather is {item}", "weather_is", WEATHER, False, False),
    ("wx-today", "weather", None, "Today is {item}", "today", WEATHER, False, False),
    ("wx-tmr", "weather", None, "Tomorrow will be {item}", "tomorrow", WEATHER, False, False),
    # health
    ("hurt", "health", None, "My {item} hurts", "hurts", BODY, False, False),
    ("unwell", "health", None, "My {item} is not well", "not_well", BODY, False, False),
    # work
    ("work-have", "work", None, "I have a {item}", "i_have", WORK, False, False),
    ("work-when", "work", None, "When is the {item}?", "when_is", WORK, True, False),
    ("work-done", "work", None, "I finished the {item}", "i_finished", WORK, False, False),
    # transport
    ("tr-where", "travel", None, "Where is the {item}?", "where_is", TRANSPORT, True, False),
    ("tr-going", "travel", None, "I'm going by {item}", "going", TRANSPORT, False, False),
    ("tr-ticket", "travel", None, "A ticket for the {item}", "ticket_for", TRANSPORT, False, False),
    # countries
    ("from-c", "travel", None, "I'm from {item}", "im_from", COUNTRIES, False, False),
    ("go-c", "travel", None, "I want to go to {item}", "want_go", COUNTRIES, False, False),
    ("live-c", "daily", None, "I live in {item}", "i_live", COUNTRIES, False, False),
    # time
    ("today-d", "time", None, "Today is {item}", "today", DAYS, False, False),
    ("tmr-d", "time", None, "Tomorrow is {item}", "tomorrow", DAYS, False, False),
    ("month", "time", None, "It is {item}", "today", MONTHS, False, False),
    ("hour", "time", None, "It is {item} o'clock", "oclock", HOURS, False, False),
    ("wait", "time", "formal", "Please wait {item} minutes", "wait_min", HOURS, False, False),
    ("like-drink", "food", None, "I like {item}", "like", DRINKS, False, False),
    ("need-place", "travel", None, "I need {item}", "i_need", PLACES, False, False),
    ("need-shop", "shopping", None, "I need {item}", "i_need", SHOP, False, False),
    ("need-work", "work", None, "I need the {item}", "i_need", WORK, False, False),
    ("need-body", "health", None, "I need my {item}", "i_need", BODY, False, False),
    ("take-food", "food", None, "I'll take the {item}", "i_take", FOOD_DRINK, False, False),
    ("bought-food", "food", None, "I bought {item}", "i_bought", FOOD_DRINK, False, False),
    ("no-need-food", "food", None, "I don't need {item}", "dont_need", FOOD_DRINK, False, False),
    ("have-place", "travel", "formal", "Do you have {item}?", "have_you", PLACES, True, False),
    ("have-shop", "shopping", "formal", "Do you have {item}?", "have_you", SHOP, True, False),
    ("like-shop", "shopping", None, "I like this {item}", "like", SHOP, False, False),
    ("like-place", "travel", None, "I like {item}", "like", PLACES, False, False),
    ("this-shop", "shopping", None, "This is {item}", "this_is", SHOP, False, False),
    ("bring-shop", "shopping", "formal", "Please bring the {item}", "please_bring", SHOP, False, False),
    ("this-place", "travel", None, "This is {item}", "this_is", PLACES, False, False),
    ("fam-have", "family", None, "I have {item}", "i_have", PEOPLE, False, False),
    ("need-tr", "travel", None, "I need a {item}", "i_need", TRANSPORT, False, False),
    ("take-tr", "travel", None, "I'll take the {item}", "i_take", TRANSPORT, False, False),
    ("have-tr", "travel", "formal", "Do you have a {item}?", "have_you", TRANSPORT, True, False),
    ("this-tr", "travel", None, "This is a {item}", "this_is", TRANSPORT, False, False),
    ("near-tr", "travel", None, "The {item} is nearby", "nearby", TRANSPORT, False, False),
    ("far-tr", "travel", None, "The {item} is far", "is_far", TRANSPORT, False, False),
    ("this-work", "work", None, "This is the {item}", "this_is", WORK, False, False),
    ("going-work", "work", None, "I'm going to the {item}", "going", WORK, False, False),
    ("this-body", "health", None, "This is my {item}", "this_is", BODY, False, False),
]


def generate_framed() -> tuple[list[dict], dict[str, dict[str, dict]], set[str]]:
    concepts: list[dict] = []
    translations: dict[str, dict[str, dict]] = {code: {} for code in LANG_CODES}
    seen_ids: set[str] = set()

    for prefix, category, formality, en_tmpl, part_key, vocab, question, with_please in FRAMES:
        for item in vocab:
            en_item = english_key(item)
            cid = f"{prefix}-{slug(en_item)}"
            if cid in seen_ids:
                continue
            seen_ids.add(cid)
            concepts.append(
                {
                    "id": cid,
                    "category": category,
                    "formality": formality,
                    "english": en_tmpl.format(item=en_item),
                    "source": "generated",
                }
            )
            for lang in LANG_CODES:
                text, tr, words = build_phrase(prefix, part_key, item, lang, question=question)
                if with_please:
                    text, tr, words = add_please(lang, text, tr, words)
                payload: dict = {"text": text, "words": words}
                if tr:
                    payload["transliteration"] = tr
                translations[lang][cid] = payload
    return concepts, translations, seen_ids


def core_phrases() -> list[dict]:
    from lexicon import LANG_FROM_ARG, parse_form

    def c(id, category, formality, en, **forms):
        missing_args = set(LANG_FROM_ARG) - set(forms)
        extra = set(forms) - set(LANG_FROM_ARG)
        if missing_args or extra:
            raise ValueError(f"core {id}: missing={sorted(missing_args)} extra={sorted(extra)}")
        packed = {code: parse_form(forms[arg]) for arg, code in LANG_FROM_ARG.items()}
        return {
            "id": id,
            "category": category,
            "formality": formality,
            "english": en,
            "source": "curated",
            "forms": packed,
        }

    return [
        c("hello", "greetings", "informal", "Hello (informal / everyday)",
          fa="سلام|salām", ar="مرحبا|marḥaban", zh="你好|nǐ hǎo", ja="こんにちは|konnichiwa", ko="안녕하세요|annyeonghaseyo",
          hi="नमस्ते|namaste", ru="Привет|Privet", th="สวัสดี|sàwàtdii", el="Γεια σου|Yá sou", he="שלום|shalóm",
          uk="Привіт|Pryvit", ur="سلام|salām", bn="হ্যালো|hyalo",
          es="Hola", fr="Salut", de="Hallo", pt="Oi", it="Ciao", tr="Merhaba", vi="Xin chào", idn="Halo",
          pl="Cześć", nl="Hoi", sv="Hej", ro="Salut", cs="Ahoj", hu="Szia", ms="Hai", fil="Kumusta", sw="Habari"),
        c("hello-formal", "greetings", "formal", "Hello (formal)",
          fa="سلام علیکم|salām aleikom", ar="السلام عليكم|as-salāmu ʿalaykum", zh="您好|nín hǎo", ja="はじめまして|hajimemashite", ko="안녕하십니까|annyeonghashimnikka",
          hi="नमस्कार|namaskār", ru="Здравствуйте|Zdravstvuyte", th="สวัสดีครับ|sàwàtdii khráp", el="Γεια σας|Yá sas", he="שלום רב|shalóm rav",
          uk="Доброго дня|Dobroho dnya", ur="السلام علیکم|assalāmu ʿalaykum", bn="নমস্কার|nomoshkar",
          es="Buenos días", fr="Bonjour", de="Guten Tag", pt="Bom dia", it="Buongiorno", tr="İyi günler", vi="Kính chào", idn="Selamat pagi",
          pl="Dzień dobry", nl="Goedendag", sv="God dag", ro="Bună ziua", cs="Dobrý den", hu="Jó napot", ms="Selamat sejahtera", fil="Magandang araw", sw="Shikamoo"),
        c("good-morning", "greetings", None, "Good morning",
          fa="صبح بخیر|sobh bekheyr", ar="صباح الخير|ṣabāḥ al-khayr", zh="早上好|zǎoshang hǎo", ja="おはようございます|ohayō gozaimasu", ko="좋은 아침이에요|joeun achimieyo",
          hi="सुप्रभात|suprabhāt", ru="Доброе утро|Dobroye utro", th="อรุณสวัสดิ์|àrun sàwàt", el="Καλημέρα|Kaliméra", he="בוקר טוב|bóker tov",
          uk="Доброго ранку|Dobroho ranku", ur="صبح بخیر|subḥ bakhair", bn="শুভ সকাল|shubho sokal",
          es="Buenos días", fr="Bonjour", de="Guten Morgen", pt="Bom dia", it="Buongiorno", tr="Günaydın", vi="Chào buổi sáng", idn="Selamat pagi",
          pl="Dzień dobry", nl="Goedemorgen", sv="God morgon", ro="Bună dimineața", cs="Dobré ráno", hu="Jó reggelt", ms="Selamat pagi", fil="Magandang umaga", sw="Habari za asubuhi"),
        c("good-afternoon", "greetings", None, "Good afternoon",
          fa="عصر بخیر|asr bekheyr", ar="مساء الخير|masāʾ al-khayr", zh="下午好|xiàwǔ hǎo", ja="こんにちは|konnichiwa", ko="좋은 오후예요|joeun ohuyeoyo",
          hi="नमस्कार|namaskār", ru="Добрый день|Dobryy den'", th="สวัสดีตอนบ่าย|sàwàtdii tɔɔn bàai", el="Καλό απόγευμα|Kaló apógevma", he="אחר צהריים טובים|achar tsohoráyim tovím",
          uk="Добрий день|Dobryy den'", ur="دوپہر بخیر|dopahar bakhair", bn="শুভ অপরাহ্ন|shubho oporahnho",
          es="Buenas tardes", fr="Bon après-midi", de="Guten Tag", pt="Boa tarde", it="Buon pomeriggio", tr="Tünaydın", vi="Chào buổi chiều", idn="Selamat siang",
          pl="Dzień dobry", nl="Goedemiddag", sv="God eftermiddag", ro="Bună ziua", cs="Dobré odpoledne", hu="Jó napot", ms="Selamat petang", fil="Magandang hapon", sw="Habari za mchana"),
        c("good-night", "greetings", None, "Good night",
          fa="شب بخیر|shab bekheyr", ar="تصبح على خير|tuṣbiḥ ʿalā khayr", zh="晚安|wǎn'ān", ja="おやすみなさい|oyasuminasai", ko="안녕히 주무세요|annyeonghi jumuseyo",
          hi="शुभ रात्रि|śubh rātri", ru="Спокойной ночи|Spokoynoy nochi", th="ราตรีสวัสดิ์|raatrii sàwàt", el="Καληνύχτα|Kalinýchta", he="לילה טוב|láila tov",
          uk="На добраніч|Na dobranich", ur="شب بخیر|shab bakhair", bn="শুভ রাত্রি|shubho ratri",
          es="Buenas noches", fr="Bonne nuit", de="Gute Nacht", pt="Boa noite", it="Buonanotte", tr="İyi geceler", vi="Chúc ngủ ngon", idn="Selamat malam",
          pl="Dobranoc", nl="Welterusten", sv="God natt", ro="Noapte bună", cs="Dobrou noc", hu="Jó éjszakát", ms="Selamat malam", fil="Magandang gabi", sw="Usiku mwema"),
        c("goodbye", "greetings", None, "Goodbye",
          fa="خداحافظ|khodāhāfez", ar="مع السلامة|maʿa as-salāma", zh="再见|zàijiàn", ja="さようなら|sayōnara", ko="안녕히 가세요|annyeonghi gaseyo",
          hi="अलविदा|alvidā", ru="До свидания|Do svidaniya", th="ลาก่อน|laa kɔ̀ɔn", el="Αντίο|Adío", he="להתראות|lehitra'ót",
          uk="До побачення|Do pobachennya", ur="خدا حافظ|khudā ḥāfiz", bn="বিদায়|biday",
          es="Adiós", fr="Au revoir", de="Auf Wiedersehen", pt="Tchau", it="Arrivederci", tr="Hoşça kal", vi="Tạm biệt", idn="Selamat tinggal",
          pl="Do widzenia", nl="Tot ziens", sv="Hej då", ro="La revedere", cs="Na shledanou", hu="Viszontlátásra", ms="Selamat tinggal", fil="Paalam", sw="Kwaheri"),
        c("how-are-you", "greetings", "informal", "How are you? (informal)",
          fa="حالت چطوره؟|hālet chetore?", ar="كيفك؟|kīfak?", zh="你好吗？|nǐ hǎo ma?", ja="元気？|genki?", ko="잘 지내?|jal jinae?",
          hi="कैसे हो?|kaise ho?", ru="Как дела?|Kak dela?", th="สบายดีไหม?|sàbaai dii mǎi?", el="Τι κάνεις;|Ti kánis?", he="מה שלומך?|ma shlomkhá?",
          uk="Як справи?|Yak spravy?", ur="کیسے ہو؟|kaise ho?", bn="কেমন আছো?|kemon acho?",
          es="¿Qué tal?", fr="Ça va ?", de="Wie geht's?", pt="Tudo bem?", it="Come stai?", tr="Nasılsın?", vi="Bạn khỏe không?", idn="Apa kabar?",
          pl="Jak leci?", nl="Hoe gaat het?", sv="Hur mår du?", ro="Ce mai faci?", cs="Jak se máš?", hu="Hogy vagy?", ms="Apa khabar?", fil="Kamusta ka?", sw="Habari yako?"),
        c("how-are-you-formal", "greetings", "formal", "How are you? (formal)",
          fa="حال شما چطور است؟|hāl-e shomā chetor ast?", ar="كيف حالكم؟|kayfa ḥālukum?", zh="您好吗？|nín hǎo ma?", ja="お元気ですか？|o-genki desu ka?", ko="잘 지내세요?|jal jinaeseyo?",
          hi="आप कैसे हैं?|āp kaise haĩ?", ru="Как вы поживаете?|Kak vy pozhivayete?", th="สบายดีไหมครับ?|sàbaai dii mǎi khráp?", el="Τι κάνετε;|Ti kánete?", he="מה שלומכם?|ma shlomkhém?",
          uk="Як ви себе почуваєте?|Yak vy sebe pochuvayete?", ur="آپ کیسے ہیں؟|āp kaise haĩ?", bn="আপনি কেমন আছেন?|apni kemon achen?",
          es="¿Cómo está usted?", fr="Comment allez-vous ?", de="Wie geht es Ihnen?", pt="Como vai?", it="Come sta?", tr="Nasılsınız?", vi="Quý vị có khỏe không?", idn="Apa kabar Anda?",
          pl="Jak się Pan ma?", nl="Hoe maakt u het?", sv="Hur mår ni?", ro="Ce mai faceți?", cs="Jak se máte?", hu="Hogy van?", ms="Apa khabar anda?", fil="Kamusta po kayo?", sw="Habari yenu?"),
        c("im-fine", "greetings", None, "I'm fine, thanks",
          fa="خوبم، ممنون|khubam, mamnun", ar="بخير، شكرا|bikhayr, shukran", zh="我很好，谢谢|wǒ hěn hǎo, xièxie", ja="元気です、ありがとう|genki desu, arigatō", ko="잘 지내요, 감사합니다|jal jinaeyo, gamsahamnida",
          hi="मैं ठीक हूँ, धन्यवाद|main ṭhīk hū̃, dhanyavād", ru="Хорошо, спасибо|Khorosho, spasibo", th="สบายดี ขอบคุณ|sàbaai dii khɔ̀ɔp khun", el="Καλά, ευχαριστώ|Kalá, efcharistó", he="בסדר, תודה|beséder, todá",
          uk="Добре, дякую|Dobre, dyakuyu", ur="میں ٹھیک ہوں، شکریہ|main ṭhīk hū̃, shukriya", bn="আমি ভালো আছি, ধন্যবাদ|ami bhalo achi",
          es="Bien, gracias", fr="Ça va, merci", de="Gut, danke", pt="Estou bem, obrigado", it="Sto bene, grazie", tr="İyiyim, teşekkürler", vi="Tôi khỏe, cảm ơn", idn="Baik, terima kasih",
          pl="Dobrze, dziękuję", nl="Goed, dank je", sv="Bra, tack", ro="Bine, mulțumesc", cs="Dobře, díky", hu="Jól, köszönöm", ms="Baik, terima kasih", fil="Mabuti, salamat", sw="Nzuri, asante"),
        c("welcome", "greetings", "formal", "Welcome",
          fa="خوش آمدید|khosh āmadid", ar="أهلا وسهلا|ahlan wa sahlan", zh="欢迎|huānyíng", ja="いらっしゃいませ|irasshaimase", ko="환영합니다|hwan-yeonghamnida",
          hi="स्वागत है|svāgat hai", ru="Добро пожаловать|Dobro pozhalovat'", th="ยินดีต้อนรับ|yindi tɔ̂ɔn ráp", el="Καλώς ήρθατε|Kalós írthate", he="ברוכים הבאים|brukhím haba'ím",
          uk="Ласкаво просимо|Laskavo prosymo", ur="خوش آمدید|khush āmdīd", bn="স্বাগতম|swagotom",
          es="Bienvenido", fr="Bienvenue", de="Willkommen", pt="Bem-vindo", it="Benvenuto", tr="Hoş geldiniz", vi="Chào mừng", idn="Selamat datang",
          pl="Witamy", nl="Welkom", sv="Välkommen", ro="Bine ați venit", cs="Vítejte", hu="Isten hozott", ms="Selamat datang", fil="Maligayang pagdating", sw="Karibu"),
        c("nice-to-meet-you", "greetings", None, "Nice to meet you",
          fa="خوشبختم|khoshbakhtam", ar="تشرفنا|tasharrafnā", zh="很高兴认识你|hěn gāoxìng rènshi nǐ", ja="はじめまして、どうぞよろしく|hajimemashite, dōzo yoroshiku", ko="만나서 반가워요|mannaseo bangawoyo",
          hi="आपसे मिलकर खुशी हुई|āpse milkar khushī huī", ru="Приятно познакомиться|Priyatno poznakomit'sya", th="ยินดีที่ได้รู้จัก|yindi thîi dâi rúu jàk", el="Χάρηκα για τη γνωριμία|Chárika gia ti gnorimía", he="נעים להכיר|na'ím lehakír",
          uk="Приємно познайомитися|Pryyemno poznayomytysya", ur="مل کر خوشی ہوئی|mil kar khushī huī", bn="আপনার সাথে দেখা হয়ে ভালো লাগল|apnar sathe",
          es="Encantado", fr="Enchanté", de="Freut mich", pt="Prazer em conhecê-lo", it="Piacere di conoscerti", tr="Memnun oldum", vi="Rất vui được gặp bạn", idn="Senang bertemu Anda",
          pl="Miło mi", nl="Aangenaam", sv="Trevligt att träffas", ro="Încântat de cunoștință", cs="Těší mě", hu="Örülök a találkozásnak", ms="Gembira berkenalan", fil="Ikinagagalak kitang makilala", sw="Nimefurahi kukutana nawe"),
        c("what-is-your-name", "greetings", "formal", "What is your name? (formal)",
          fa="اسم شما چیست؟|esm-e shomā chist?", ar="ما اسمك؟|mā ismuka?", zh="您叫什么名字？|nín jiào shénme míngzi?", ja="お名前は？|o-namae wa?", ko="성함이 어떻게 되세요?|seonghami eotteoke doeseyo?",
          hi="आपका नाम क्या है?|āpkā nām kyā hai?", ru="Как вас зовут?|Kak vas zovut?", th="คุณชื่ออะไรครับ?|khun chûue àrai khráp?", el="Πώς σας λένε;|Pós sas léne?", he="איך קוראים לך?|ekh kor'ím lekhá?",
          uk="Як вас звати?|Yak vas zvaty?", ur="آپ کا نام کیا ہے؟|āp kā nām kyā hai?", bn="আপনার নাম কি?|apnar nam ki?",
          es="¿Cómo se llama?", fr="Comment vous appelez-vous ?", de="Wie heißen Sie?", pt="Qual é o seu nome?", it="Come si chiama?", tr="Adınız nedir?", vi="Tên bạn là gì?", idn="Siapa nama Anda?",
          pl="Jak się Pan nazywa?", nl="Hoe heet u?", sv="Vad heter ni?", ro="Cum vă numiți?", cs="Jak se jmenujete?", hu="Mi a neve?", ms="Siapa nama anda?", fil="Ano po ang pangalan ninyo?", sw="Jina lako nani?"),
        c("my-name-is", "greetings", None, "My name is…",
          fa="اسم من … است|esm-e man … ast", ar="اسمي …|ismī …", zh="我叫…|wǒ jiào …", ja="私の名前は…です|watashi no namae wa … desu", ko="제 이름은 …입니다|je ireumeun …imnida",
          hi="मेरा नाम … है|merā nām … hai", ru="Меня зовут …|Menya zovut …", th="ฉันชื่อ…|chăn chûue …", el="Με λένε …|Me léne …", he="קוראים לי …|kor'ím li …",
          uk="Мене звати …|Mene zvaty …", ur="میرا نام … ہے|merā nām … hai", bn="আমার নাম …|amar nam",
          es="Me llamo…", fr="Je m'appelle…", de="Ich heiße…", pt="Meu nome é…", it="Mi chiamo…", tr="Adım…", vi="Tên tôi là…", idn="Nama saya…",
          pl="Nazywam się…", nl="Ik heet…", sv="Jag heter…", ro="Mă numesc…", cs="Jmenuji se…", hu="A nevem…", ms="Nama saya…", fil="Ang pangalan ko ay…", sw="Jina langu ni…"),
        c("please", "polite", "formal", "Please",
          fa="لطفاً|lotfan", ar="من فضلك|min faḍlik", zh="请|qǐng", ja="お願いします|onegaishimasu", ko="부탁합니다|butakhamnida",
          hi="कृपया|kṛpayā", ru="Пожалуйста|Pozhaluysta", th="กรุณา|karúnaa", el="Παρακαλώ|Parakaló", he="בבקשה|bevakahá",
          uk="Будь ласка|Bud' laska", ur="براہ کرم|barāh-e karam", bn="দয়া করে|doya kore",
          es="Por favor", fr="S'il vous plaît", de="Bitte", pt="Por favor", it="Per favore", tr="Lütfen", vi="Làm ơn", idn="Tolong",
          pl="Proszę", nl="Alsjeblieft", sv="Snälla", ro="Te rog", cs="Prosím", hu="Kérem", ms="Tolong", fil="Paki", sw="Tafadhali"),
        c("thank-you", "polite", None, "Thank you",
          fa="متشکرم|moteshakkeram", ar="شكرا|shukran", zh="谢谢|xièxie", ja="ありがとう|arigatō", ko="감사합니다|gamsahamnida",
          hi="धन्यवाद|dhanyavād", ru="Спасибо|Spasibo", th="ขอบคุณ|khɔ̀ɔp khun", el="Ευχαριστώ|Efcharistó", he="תודה|todá",
          uk="Дякую|Dyakuyu", ur="شکریہ|shukriya", bn="ধন্যবাদ|dhonnobad",
          es="Gracias", fr="Merci", de="Danke", pt="Obrigado", it="Grazie", tr="Teşekkürler", vi="Cảm ơn", idn="Terima kasih",
          pl="Dziękuję", nl="Dank je", sv="Tack", ro="Mulțumesc", cs="Děkuji", hu="Köszönöm", ms="Terima kasih", fil="Salamat", sw="Asante"),
        c("thank-you-very-much", "polite", "formal", "Thank you very much",
          fa="خیلی ممنون|kheyli mamnun", ar="شكرا جزيلا|shukran jazīlan", zh="非常感谢|fēicháng gǎnxiè", ja="どうもありがとうございます|dōmo arigatō gozaimasu", ko="대단히 감사합니다|daedanhi gamsahamnida",
          hi="बहुत धन्यवाद|bahut dhanyavād", ru="Большое спасибо|Bol'shoye spasibo", th="ขอบคุณมาก|khɔ̀ɔp khun mâak", el="Ευχαριστώ πολύ|Efcharistó polý", he="תודה רבה|todá rabá",
          uk="Дуже дякую|Duzhe dyakuyu", ur="بہت شکریہ|bohat shukriya", bn="অনেক ধন্যবাদ|onek dhonnobad",
          es="Muchas gracias", fr="Merci beaucoup", de="Vielen Dank", pt="Muito obrigado", it="Grazie mille", tr="Çok teşekkür ederim", vi="Cảm ơn rất nhiều", idn="Terima kasih banyak",
          pl="Bardzo dziękuję", nl="Hartelijk dank", sv="Tack så mycket", ro="Mulțumesc foarte mult", cs="Mockrát děkuji", hu="Nagyon köszönöm", ms="Terima kasih banyak", fil="Maraming salamat", sw="Asante sana"),
        c("youre-welcome", "polite", None, "You're welcome",
          fa="خواهش می‌کنم|khāhesh mikonam", ar="عفوا|ʿafwan", zh="不客气|bú kèqi", ja="どういたしまして|dō itashimashite", ko="천만에요|cheonmaneyo",
          hi="आपका स्वागत है|āpkā svāgat hai", ru="Пожалуйста|Pozhaluysta", th="ไม่เป็นไร|mâi bpen rai", el="Παρακαλώ|Parakaló", he="על לא דבר|al lo davár",
          uk="Будь ласка|Bud' laska", ur="خوش آمدید|khush āmdīd", bn="স্বাগতম|swagotom",
          es="De nada", fr="De rien", de="Gern geschehen", pt="De nada", it="Prego", tr="Rica ederim", vi="Không có chi", idn="Sama-sama",
          pl="Nie ma za co", nl="Graag gedaan", sv="Varsågod", ro="Cu plăcere", cs="Není zač", hu="Szívesen", ms="Sama-sama", fil="Walang anuman", sw="Karibu"),
        c("excuse-me", "polite", "formal", "Excuse me",
          fa="ببخشید|bebakhshid", ar="عفوا|ʿafwan", zh="对不起|duìbuqǐ", ja="すみません|sumimasen", ko="실례합니다|sillyehamnida",
          hi="क्षमा कीजिए|kṣamā kījiye", ru="Извините|Izvinite", th="ขอโทษ|khɔ̌ɔ thôot", el="Συγγνώμη|Sygnómi", he="סליחה|slikhá",
          uk="Вибачте|Vybachte", ur="معاف کیجئے|maʿāf kījiye", bn="মাফ করবেন|maf korben",
          es="Perdón", fr="Excusez-moi", de="Entschuldigung", pt="Com licença", it="Mi scusi", tr="Affedersiniz", vi="Xin lỗi", idn="Permisi",
          pl="Przepraszam", nl="Pardon", sv="Ursäkta", ro="Scuzați-mă", cs="Promiňte", hu="Elnézést", ms="Maaf", fil="Paumanhin", sw="Samahani"),
        c("im-sorry", "polite", None, "I'm sorry",
          fa="متأسفم|mote'assefam", ar="أنا آسف|anā āsif", zh="抱歉|bàoqiàn", ja="ごめんなさい|gomen nasai", ko="미안합니다|mianhamnida",
          hi="मुझे माफ़ कीजिए|mujhe māf kījiye", ru="Простите|Prostite", th="ขอโทษนะ|khɔ̌ɔ thôot ná", el="Λυπάμαι|Lypámai", he="אני מצטער|ani mitzta'ér",
          uk="Вибачте|Vybachte", ur="مجھے افسوس ہے|mujhe afsos hai", bn="দুঃখিত|dukkhito",
          es="Lo siento", fr="Je suis désolé", de="Es tut mir leid", pt="Desculpe", it="Mi dispiace", tr="Özür dilerim", vi="Tôi xin lỗi", idn="Saya minta maaf",
          pl="Przepraszam", nl="Het spijt me", sv="Förlåt", ro="Îmi pare rău", cs="Je mi líto", hu="Sajnálom", ms="Saya minta maaf", fil="Pasensya na", sw="Pole"),
        c("yes", "polite", None, "Yes",
          fa="بله|bale", ar="نعم|naʿam", zh="是|shì", ja="はい|hai", ko="네|ne",
          hi="हाँ|hā̃", ru="Да|Da", th="ใช่|châi", el="Ναι|Nai", he="כן|ken",
          uk="Так|Tak", ur="ہاں|hā̃", bn="হ্যাঁ|hyan",
          es="Sí", fr="Oui", de="Ja", pt="Sim", it="Sì", tr="Evet", vi="Vâng", idn="Ya",
          pl="Tak", nl="Ja", sv="Ja", ro="Da", cs="Ano", hu="Igen", ms="Ya", fil="Oo", sw="Ndiyo"),
        c("no", "polite", None, "No",
          fa="نه|na", ar="لا|lā", zh="不|bù", ja="いいえ|iie", ko="아니요|aniyo",
          hi="नहीं|nahī̃", ru="Нет|Nyet", th="ไม่|mâi", el="Όχι|Óchi", he="לא|lo",
          uk="Ні|Ni", ur="نہیں|nahī̃", bn="না|na",
          es="No", fr="Non", de="Nein", pt="Não", it="No", tr="Hayır", vi="Không", idn="Tidak",
          pl="Nie", nl="Nee", sv="Nej", ro="Nu", cs="Ne", hu="Nem", ms="Tidak", fil="Hindi", sw="Hapana"),
        c("i-dont-understand", "polite", None, "I don't understand",
          fa="نمی‌فهمم|nemifahmam", ar="لا أفهم|lā afham", zh="我听不懂|wǒ tīng bù dǒng", ja="わかりません|wakarimasen", ko="이해가 안 돼요|ihaega an dwaeyo",
          hi="मुझे समझ नहीं आया|mujhe samajh nahī̃ āyā", ru="Я не понимаю|Ya ne ponimayu", th="ฉันไม่เข้าใจ|chăn mâi khâo jai", el="Δεν καταλαβαίνω|Den katalavaíno", he="אני לא מבין|ani lo mevín",
          uk="Я не розумію|Ya ne rozumiyu", ur="مجھے سمجھ نہیں آیا|mujhe samajh nahī̃ āyā", bn="আমি বুঝতে পারছি না|ami bujhte parchhi na",
          es="No entiendo", fr="Je ne comprends pas", de="Ich verstehe nicht", pt="Eu não entendo", it="Non capisco", tr="Anlamıyorum", vi="Tôi không hiểu", idn="Saya tidak mengerti",
          pl="Nie rozumiem", nl="Ik begrijp het niet", sv="Jag förstår inte", ro="Nu înțeleg", cs="Nerozumím", hu="Nem értem", ms="Saya tidak faham", fil="Hindi ko naiintindihan", sw="Sielewi"),
        c("please-speak-slowly", "polite", "formal", "Please speak slowly",
          fa="لطفاً آهسته صحبت کنید|lotfan āheste sohbat konid", ar="تحدث ببطء من فضلك|taḥaddath bibuṭʾ min faḍlik", zh="请说慢一点|qǐng shuō màn yìdiǎn", ja="ゆっくり話してください|yukkuri hanashite kudasai", ko="천천히 말해 주세요|cheoncheonhi malhae juseyo",
          hi="कृपया धीरे बोलिए|kṛpayā dhīre boliye", ru="Говорите медленнее, пожалуйста|Govorite medlenneye, pozhaluysta", th="พูดช้าๆ ได้ไหม|phûut cháa cháa dâi mǎi", el="Μιλήστε αργά παρακαλώ|Milíste argá parakaló", he="דבר לאט בבקשה|dabér le'át bevakahá",
          uk="Говоріть повільніше, будь ласка|Hovorít' povil'nishe, bud' laska", ur="براہ کرم آہستہ بولیں|barāh-e karam āhista bolẽ", bn="দয়া করে আস্তে বলুন|doya kore aste bolun",
          es="Hable más despacio, por favor", fr="Parlez plus lentement, s'il vous plaît", de="Bitte sprechen Sie langsam", pt="Fale mais devagar, por favor", it="Parli più lentamente, per favore", tr="Lütfen yavaş konuşun", vi="Làm ơn nói chậm", idn="Tolong bicara pelan-pelan",
          pl="Proszę mówić wolniej", nl="Spreek alstublieft langzaam", sv="Prata långsamt, tack", ro="Vorbiți mai încet, vă rog", cs="Mluvte pomalu, prosím", hu="Kérem, beszéljen lassan", ms="Tolong cakap perlahan", fil="Paki-usap po nang dahan-dahan", sw="Tafadhali sema polepole"),
        c("do-you-speak-english", "polite", "formal", "Do you speak English?",
          fa="انگلیسی صحبت می‌کنید؟|engelisi sohbat mikonid?", ar="هل تتحدث الإنجليزية؟|hal tataḥaddath al-injlīziyya?", zh="你会说英语吗？|nǐ huì shuō yīngyǔ ma?", ja="英語を話せますか？|eigo o hanasemasu ka?", ko="영어 하세요?|yeongeo haseyo?",
          hi="क्या आप अंग्रेज़ी बोलते हैं?|kyā āp aṅgrezī bolte haĩ?", ru="Вы говорите по-английски?|Vy govorite po-angliyski?", th="พูดภาษาอังกฤษได้ไหม?|phûut phaa-sǎa angkrìt dâi mǎi?", el="Μιλάτε αγγλικά;|Miláte angliká?", he="אתה מדבר אנגלית?|atá medabér anglít?",
          uk="Ви розмовляєте англійською?|Vy rozmovlyayete anhliys'koyu?", ur="کیا آپ انگریزی بولتے ہیں؟|kyā āp angrezī bolte haĩ?", bn="আপনি কি ইংরেজি বলেন?|apni ki ingreji bolen?",
          es="¿Habla inglés?", fr="Parlez-vous anglais ?", de="Sprechen Sie Englisch?", pt="Você fala inglês?", it="Parla inglese?", tr="İngilizce biliyor musunuz?", vi="Bạn nói tiếng Anh không?", idn="Apa Anda bisa bahasa Inggris?",
          pl="Czy mówi Pan po angielsku?", nl="Spreekt u Engels?", sv="Talar ni engelska?", ro="Vorbiți engleză?", cs="Mluvíte anglicky?", hu="Beszél angolul?", ms="Adakah anda cakap bahasa Inggeris?", fil="Nagsasalita po ba kayo ng Ingles?", sw="Unazungumza Kiingereza?"),
        c("help", "emergency", "formal", "Help!",
          fa="کمک کنید!|komak konid!", ar="النجدة!|an-najda!", zh="救命！|jiùmìng!", ja="助けて！|tasukete!", ko="도와주세요!|dowajuseyo!",
          hi="मदद कीजिए!|madad kījiye!", ru="Помогите!|Pomogite!", th="ช่วยด้วย!|chûai dûai!", el="Βοήθεια!|Voítheia!", he="הצילו!|hatzílu!",
          uk="Допоможіть!|Dopomozhit'!", ur="مدد!|madad!", bn="সাহায্য!|shahajjo!",
          es="¡Ayuda!", fr="Au secours !", de="Hilfe!", pt="Socorro!", it="Aiuto!", tr="İmdat!", vi="Cứu!", idn="Tolong!",
          pl="Pomocy!", nl="Help!", sv="Hjälp!", ro="Ajutor!", cs="Pomoc!", hu="Segítség!", ms="Tolong!", fil="Tulong!", sw="Nisaidie!"),
        c("call-the-police", "emergency", "formal", "Call the police",
          fa="با پلیس تماس بگیرید|bā polis tamās begirid", ar="اتصل بالشرطة|ittaṣil bi-sh-shurṭa", zh="报警|bàojǐng", ja="警察を呼んでください|keisatsu o yonde kudasai", ko="경찰을 불러 주세요|gyeongchareul bulleo juseyo",
          hi="पुलिस को बुलाओ|pulis ko bulāo", ru="Вызовите полицию|Vyzovite politsiyu", th="เรียกตำรวจ|rîak tamrùat", el="Καλέστε την αστυνομία|Kaléste tin astynomía", he="תתקשר למשטרה|titkashér lamishtará",
          uk="Викличте поліцію|Vyklychte politsiyu", ur="پولیس کو بلاؤ|pulis ko bulāo", bn="পুলিশকে ডাকুন|pulishke dakun",
          es="Llame a la policía", fr="Appelez la police", de="Rufen Sie die Polizei", pt="Chame a polícia", it="Chiami la polizia", tr="Polisi arayın", vi="Gọi cảnh sát", idn="Panggil polisi",
          pl="Zadzwoń na policję", nl="Bel de politie", sv="Ring polisen", ro="Sunați la poliție", cs="Zavolejte policii", hu="Hívja a rendőrséget", ms="Panggil polis", fil="Tawagan ang pulis", sw="Piga simu polisi"),
        c("call-an-ambulance", "emergency", "formal", "Call an ambulance",
          fa="با اورژانس تماس بگیرید|bā orzhāns tamās begirid", ar="اتصل بالإسعاف|ittaṣil bi-l-isʿāf", zh="叫救护车|jiào jiùhùchē", ja="救急車を呼んでください|kyūkyūsha o yonde kudasai", ko="구급차를 불러 주세요|gugeupchareul bulleo juseyo",
          hi="एम्बुलेंस बुलाओ|embulens bulāo", ru="Вызовите скорую|Vyzovite skoruyu", th="เรียกรถพยาบาล|rîak rót pháyaabaan", el="Καλέστε ασθενοφόρο|Kaléste asthenofóro", he="תזמין אמבולנס|tazmín ambulans",
          uk="Викличте швидку|Vyklychte shvydku", ur="ایمبولینس بلاؤ|ambulance bulāo", bn="অ্যাম্বুলেন্স ডাকুন|ambulance dakun",
          es="Llame a una ambulancia", fr="Appelez une ambulance", de="Rufen Sie einen Krankenwagen", pt="Chame uma ambulância", it="Chiami un'ambulanza", tr="Ambulans çağırın", vi="Gọi xe cấp cứu", idn="Panggil ambulans",
          pl="Zadzwoń po karetkę", nl="Bel een ambulance", sv="Ring en ambulans", ro="Sunați la ambulanță", cs="Zavolejte sanitku", hu="Hívjon mentőt", ms="Panggil ambulans", fil="Tawagan ang ambulansya", sw="Piga simu ambulansi"),
        c("im-lost", "emergency", None, "I'm lost",
          fa="گم شده‌ام|gom shode-am", ar="أنا تائه|anā tāʾih", zh="我迷路了|wǒ mílù le", ja="道に迷いました|michi ni mayoimashita", ko="길을 잃었어요|gireul ireosseoyo",
          hi="मैं रास्ता भटक गया हूँ|main rāstā bhaṭak gayā hū̃", ru="Я заблудился|Ya zabludilsya", th="ฉันหลงทาง|chăn lǒng thaang", el="Έχω χαθεί|Écho chatheí", he="אני אבוד|ani avúd",
          uk="Я заблукав|Ya zablukav", ur="میں راہ بھول گیا ہوں|main rāh bhūl gayā hū̃", bn="আমি পথ হারিয়েছি|ami poth hariyechi",
          es="Estoy perdido", fr="Je suis perdu", de="Ich habe mich verlaufen", pt="Estou perdido", it="Mi sono perso", tr="Kayboldum", vi="Tôi bị lạc", idn="Saya tersesat",
          pl="Zgubiłem się", nl="Ik ben verdwaald", sv="Jag har gått vilse", ro="M-am rătăcit", cs="Zabloudil jsem", hu="Eltévedtem", ms="Saya sesat", fil="Naligaw ako", sw="Nimepotea"),
        c("i-need-a-doctor", "emergency", None, "I need a doctor",
          fa="دکتر لازم دارم|doktor lāzem dāram", ar="أحتاج طبيبا|aḥtāj ṭabīban", zh="我需要医生|wǒ xūyào yīshēng", ja="医者が必要です|isha ga hitsuyō desu", ko="의사가 필요해요|uisaga piryohaeyo",
          hi="मुझे डॉक्टर चाहिए|mujhe ḍŏkṭar chāhiye", ru="Мне нужен врач|Mne nuzhen vrach", th="ฉันต้องการหมอ|chăn tông gaan mɔ̌ɔ", el="Χρειάζομαι γιατρό|Chreiázomai giatró", he="אני צריך רופא|ani tsaríkh rofé",
          uk="Мені потрібен лікар|Meni potriben likar", ur="مجھے ڈاکٹر چاہیے|mujhe ḍākṭar chāhiye", bn="আমার ডাক্তার দরকার|amar daktar darkar",
          es="Necesito un médico", fr="J'ai besoin d'un médecin", de="Ich brauche einen Arzt", pt="Preciso de um médico", it="Ho bisogno di un medico", tr="Doktora ihtiyacım var", vi="Tôi cần bác sĩ", idn="Saya butuh dokter",
          pl="Potrzebuję lekarza", nl="Ik heb een dokter nodig", sv="Jag behöver en läkare", ro="Am nevoie de un doctor", cs="Potřebuji lékaře", hu="Orvosra van szükségem", ms="Saya perlukan doktor", fil="Kailangan ko ng doktor", sw="Nahitaji daktari"),
        c("fire", "emergency", None, "There's a fire",
          fa="آتش‌سوزی است|ātash-suzi ast", ar="هناك حريق|hunāka ḥarīq", zh="着火了|zháohuǒ le", ja="火事です|kaji desu", ko="불이에요|burieyo",
          hi="आग लगी है|āg lagī hai", ru="Пожар|Pozhar", th="ไฟไหม้|fai mâi", el="Υπάρχει φωτιά|Ypárchei fotiá", he="יש שריפה|yesh srefá",
          uk="Пожежа|Pozhezha", ur="آگ لگی ہے|āg lagī hai", bn="আগুন লেগেছে|agun legeche",
          es="Hay un incendio", fr="Il y a un incendie", de="Es brennt", pt="Há um incêndio", it="C'è un incendio", tr="Yangın var", vi="Có cháy", idn="Ada kebakaran",
          pl="Pożar", nl="Er is brand", sv="Det brinner", ro="Este un incendiu", cs="Hoří", hu="Tűz van", ms="Ada kebakaran", fil="May sunog", sw="Kuna moto"),
        c("i-love-you", "feelings", "informal", "I love you",
          fa="دوستت دارم|dustet dāram", ar="أحبك|uḥibbuk", zh="我爱你|wǒ ài nǐ", ja="愛してる|aishiteru", ko="사랑해|saranghae",
          hi="मैं तुमसे प्यार करता हूँ|main tumse pyār kartā hū̃", ru="Я тебя люблю|Ya tebya lyublyu", th="ฉันรักเธอ|chăn rák thəə", el="Σ' αγαπώ|S' agapó", he="אני אוהב אותך|ani ohév otákh",
          uk="Я тебе кохаю|Ya tebe kokhayu", ur="میں تم سے پیار کرتا ہوں|main tum se pyār kartā hū̃", bn="আমি তোমাকে ভালোবাসি|ami tomake bhalobashi",
          es="Te quiero", fr="Je t'aime", de="Ich liebe dich", pt="Eu te amo", it="Ti amo", tr="Seni seviyorum", vi="Anh yêu em", idn="Aku cinta kamu",
          pl="Kocham cię", nl="Ik hou van je", sv="Jag älskar dig", ro="Te iubesc", cs="Miluji tě", hu="Szeretlek", ms="Saya sayang kamu", fil="Mahal kita", sw="Nakupenda"),
        c("happy-birthday", "daily", "informal", "Happy birthday",
          fa="تولدت مبارک|tavallodet mobārak", ar="عيد ميلاد سعيد|ʿīd mīlād saʿīd", zh="生日快乐|shēngrì kuàilè", ja="お誕生日おめでとう|otanjōbi omedetō", ko="생일 축하해요|saengil chukahaeyo",
          hi="जन्मदिन मुबारक|janmadin mubārak", ru="С днём рождения|S dnyom rozhdeniya", th="สุขสันต์วันเกิด|sùk sǎn wan kèət", el="Χρόνια πολλά|Chrónia pollá", he="יום הולדת שמח|yom hulédet saméakh",
          uk="З днем народження|Z dnem narodzhennya", ur="سالگرہ مبارک|sālgirah mubārak", bn="শুভ জন্মদিন|shubho jonmodin",
          es="Feliz cumpleaños", fr="Joyeux anniversaire", de="Alles Gute zum Geburtstag", pt="Feliz aniversário", it="Buon compleanno", tr="Doğum günün kutlu olsun", vi="Chúc mừng sinh nhật", idn="Selamat ulang tahun",
          pl="Wszystkiego najlepszego", nl="Gefeliciteerd met je verjaardag", sv="Grattis på födelsedagen", ro="La mulți ani", cs="Všechno nejlepší k narozeninám", hu="Boldog születésnapot", ms="Selamat hari jadi", fil="Maligayang kaarawan", sw="Heri ya kuzaliwa"),
        c("cheers", "food", "informal", "Cheers!",
          fa="به سلامتی|be salāmati", ar="في صحتك|fī ṣiḥḥatik", zh="干杯|gānbēi", ja="乾杯|kanpai", ko="건배|geonbae",
          hi="चियर्स|chears", ru="Будем здоровы|Budem zdorovy", th="ชนแก้ว|chon kâeo", el="Γεια μας|Yiá mas", he="לחיים|lekhayím",
          uk="Будьмо|Bud'mo", ur="چیرز|cheers", bn="চিয়ার্স|cheers",
          es="¡Salud!", fr="Santé !", de="Prost!", pt="Saúde!", it="Cin cin!", tr="Şerefe!", vi="Cạn ly!", idn="Bersulang!",
          pl="Na zdrowie!", nl="Proost!", sv="Skål!", ro="Noroc!", cs="Na zdraví!", hu="Egészségedre!", ms="Yam seng!", fil="Tagay!", sw="Afya!"),
        c("how-much-is-this", "shopping", None, "How much is this?",
          fa="این چند است؟|in chand ast?", ar="بكم هذا؟|bikam hādhā?", zh="这个多少钱？|zhège duōshǎo qián?", ja="これはいくらですか？|kore wa ikura desu ka?", ko="이거 얼마예요?|igeo eolmayeyo?",
          hi="यह कितने का है?|yah kitne kā hai?", ru="Сколько это стоит?|Skol'ko eto stoit?", th="อันนี้เท่าไหร่?|an níi thâo rài?", el="Πόσο κάνει αυτό;|Póso kánει aftó?", he="כמה זה עולה?|káma ze olé?",
          uk="Скільки це коштує?|Skil'ky tse koshtuye?", ur="یہ کتنے کا ہے؟|yeh kitne kā hai?", bn="এটার দাম কত?|etar dam koto?",
          es="¿Cuánto cuesta esto?", fr="Combien ça coûte ?", de="Was kostet das?", pt="Quanto custa isso?", it="Quanto costa questo?", tr="Bu ne kadar?", vi="Cái này bao nhiêu?", idn="Berapa harganya?",
          pl="Ile to kosztuje?", nl="Hoeveel kost dit?", sv="Vad kostar det här?", ro="Cât costă asta?", cs="Kolik to stojí?", hu="Mennyibe kerül ez?", ms="Berapa harganya?", fil="Magkano ito?", sw="Bei gani hii?"),
        c("where-is-the-bathroom", "travel", None, "Where is the bathroom?",
          fa="دستشویی کجاست؟|dastshuyi kojāst?", ar="أين الحمام؟|ayna al-ḥammām?", zh="洗手间在哪里？|xǐshǒujiān zài nǎlǐ?", ja="トイレはどこですか？|toire wa doko desu ka?", ko="화장실이 어디예요?|hwajangsiri eodiyeyo?",
          hi="बाथरूम कहाँ है?|bāthrūm kahā̃ hai?", ru="Где туалет?|Gde tualet?", th="ห้องน้ำอยู่ที่ไหน?|hông náam yùu thîi nǎi?", el="Πού είναι η τουαλέτα;|Poú eínai i toualéta?", he="איפה השירותים?|éifo hasherutím?",
          uk="Де туалет?|De tualet?", ur="غسل خانہ کہاں ہے؟|ghusl khāna kahā̃ hai?", bn="বাথরুম কোথায়?|bathroom kothay?",
          es="¿Dónde está el baño?", fr="Où sont les toilettes ?", de="Wo ist die Toilette?", pt="Onde fica o banheiro?", it="Dov'è il bagno?", tr="Tuvalet nerede?", vi="Nhà vệ sinh ở đâu?", idn="Di mana toilet?",
          pl="Gdzie jest toaleta?", nl="Waar is het toilet?", sv="Var är toaletten?", ro="Unde este toaleta?", cs="Kde je toaleta?", hu="Hol van a mosdó?", ms="Di manakah tandas?", fil="Nasaan ang CR?", sw="Choo kiko wapi?"),
        c("i-dont-know", "daily", None, "I don't know",
          fa="نمی‌دانم|nemidānam", ar="لا أعرف|lā aʿrif", zh="我不知道|wǒ bù zhīdào", ja="わかりません|wakarimasen", ko="모르겠어요|moreugesseoyo",
          hi="मुझे नहीं पता|mujhe nahī̃ patā", ru="Я не знаю|Ya ne znayu", th="ฉันไม่รู้|chăn mâi rúu", el="Δεν ξέρω|Den kséro", he="אני לא יודע|ani lo yodéa",
          uk="Я не знаю|Ya ne znayu", ur="مجھے نہیں معلوم|mujhe nahī̃ maʿlūm", bn="আমি জানি না|ami jani na",
          es="No sé", fr="Je ne sais pas", de="Ich weiß nicht", pt="Eu não sei", it="Non lo so", tr="Bilmiyorum", vi="Tôi không biết", idn="Saya tidak tahu",
          pl="Nie wiem", nl="Ik weet het niet", sv="Jag vet inte", ro="Nu știu", cs="Nevím", hu="Nem tudom", ms="Saya tidak tahu", fil="Hindi ko alam", sw="Sijui"),
        c("see-you-later", "greetings", "informal", "See you later",
          fa="بعداً می‌بینمت|ba'dan mibinamet", ar="أراك لاحقا|arāka lāḥiqan", zh="回头见|huítóu jiàn", ja="またね|matane", ko="나중에 봐|najunge bwa",
          hi="बाद में मिलते हैं|bād mẽ milte haĩ", ru="Увидимся|Uvidimsya", th="แล้วเจอกัน|láew jəə gan", el="Τα λέμε|Ta léme", he="נתראה אחר כך|nitra'é akhar kakh",
          uk="Побачимось|Pobachymos'", ur="بعد میں ملتے ہیں|baʿd mẽ milte haĩ", bn="পরে দেখা হবে|pore dekha hobe",
          es="Hasta luego", fr="À plus tard", de="Bis später", pt="Até mais", it="A dopo", tr="Sonra görüşürüz", vi="Hẹn gặp lại", idn="Sampai jumpa",
          pl="Do zobaczenia", nl="Tot later", sv="Vi ses", ro="Pe curând", cs="Naviděnou", hu="Később találkozunk", ms="Jumpa lagi", fil="Kita tayo later", sw="Tutaonana baadaye"),
        c("can-you-help-me", "daily", "formal", "Can you help me?",
          fa="می‌توانید کمک کنید؟|mitavānid komak konid?", ar="هل يمكنك مساعدتي؟|hal yumkinuka musāʿadatī?", zh="你能帮我吗？|nǐ néng bāng wǒ ma?", ja="手伝っていただけますか？|tetsudatte itadakemasu ka?", ko="도와주시겠어요?|dowajusigesseoyo?",
          hi="क्या आप मेरी मदद कर सकते हैं?|kyā āp merī madad kar sakte haĩ?", ru="Вы можете мне помочь?|Vy mozhete mne pomoch'?", th="ช่วยหน่อยได้ไหม?|chûai nòi dâi mǎi?", el="Μπορείτε να με βοηθήσετε;|Boreíte na me voithísete?", he="אתה יכול לעזור לי?|atá yakhol la'azór li?",
          uk="Ви можете мені допомогти?|Vy mozhete meni dopomohty?", ur="کیا آپ میری مدد کر سکتے ہیں؟|kyā āp merī madad kar sakte haĩ?", bn="আপনি কি আমাকে সাহায্য করতে পারেন?|apni ki amake shahajjo korte paren?",
          es="¿Puede ayudarme?", fr="Pouvez-vous m'aider ?", de="Können Sie mir helfen?", pt="Você pode me ajudar?", it="Può aiutarmi?", tr="Bana yardım eder misiniz?", vi="Bạn có thể giúp tôi không?", idn="Bisakah Anda membantu saya?",
          pl="Czy może mi Pan pomóc?", nl="Kunt u me helpen?", sv="Kan ni hjälpa mig?", ro="Mă puteți ajuta?", cs="Můžete mi pomoci?", hu="Tudna segíteni?", ms="Bolehkah anda bantu saya?", fil="Pwede niyo po ba akong tulungan?", sw="Unaweza kunisaidia?"),
        c("i-am-allergic", "health", None, "I have an allergy",
          fa="آلرژی دارم|ālerzhi dāram", ar="لدي حساسية|ladayya ḥasāsiyya", zh="我有过敏|wǒ yǒu guòmǐn", ja="アレルギーがあります|arerugī ga arimasu", ko="알레르기가 있어요|allereugiga isseoyo",
          hi="मुझे एलर्जी है|mujhe elarjī hai", ru="У меня аллергия|U menya allergiya", th="ฉันแพ้|chăn phɛ́ɛ", el="Έχω αλλεργία|Écho allergía", he="יש לי אלרגיה|yesh li alergya",
          uk="У мене алергія|U mene alerhiya", ur="مجھے الرجی ہے|mujhe allergy hai", bn="আমার অ্যালার্জি আছে|amar allergy ache",
          es="Tengo alergia", fr="J'ai une allergie", de="Ich habe eine Allergie", pt="Eu tenho alergia", it="Ho un'allergia", tr="Alerjim var", vi="Tôi bị dị ứng", idn="Saya punya alergi",
          pl="Mam alergię", nl="Ik heb een allergie", sv="Jag har allergi", ro="Am o alergie", cs="Mám alergii", hu="Allergiám van", ms="Saya ada alahan", fil="May allergy ako", sw="Nina mzio"),
        c("it-hurts-here", "health", None, "It hurts here",
          fa="اینجا درد می‌کند|injā dard mikonad", ar="يؤلمني هنا|yu'limunī hunā", zh="这里疼|zhèlǐ téng", ja="ここが痛いです|koko ga itai desu", ko="여기가 아파요|yeogiga apayo",
          hi="यहाँ दर्द हो रहा है|yahā̃ dard ho rahā hai", ru="Здесь болит|Zdes' bolit", th="เจ็บตรงนี้|jèp trong níi", el="Πονάει εδώ|Ponáei edó", he="כואב לי כאן|ko'év li kan",
          uk="Тут болить|Tut bolyt'", ur="یہاں درد ہو رہا ہے|yahā̃ dard ho rahā hai", bn="এখানে ব্যথা|ekhane byatha",
          es="Me duele aquí", fr="Ça fait mal ici", de="Es tut hier weh", pt="Dói aqui", it="Fa male qui", tr="Burası ağrıyor", vi="Đau ở đây", idn="Sakit di sini",
          pl="Boli tutaj", nl="Het doet hier pijn", sv="Det gör ont här", ro="Mă doare aici", cs="Bolí to tady", hu="Itt fáj", ms="Sakit di sini", fil="Masakit dito", sw="Inauma hapa"),
        c("what-time-is-it", "time", None, "What time is it?",
          fa="ساعت چند است؟|sā'at chand ast?", ar="كم الساعة؟|kam as-sāʿa?", zh="现在几点？|xiànzài jǐ diǎn?", ja="今何時ですか？|ima nanji desu ka?", ko="지금 몇 시예요?|jigeum myeot siyeyo?",
          hi="कितने बजे हैं?|kitne baje haĩ?", ru="Который час?|Kotoryy chas?", th="กี่โมงแล้ว?|kìi moong láew?", el="Τι ώρα είναι;|Ti óra eínai?", he="מה השעה?|ma hasha'á?",
          uk="Котра година?|Kotra hodyna?", ur="کتنے بجے ہیں؟|kitne baje haĩ?", bn="কয়টা বাজে?|koyta baje?",
          es="¿Qué hora es?", fr="Quelle heure est-il ?", de="Wie spät ist es?", pt="Que horas são?", it="Che ora è?", tr="Saat kaç?", vi="Bây giờ là mấy giờ?", idn="Jam berapa sekarang?",
          pl="Która godzina?", nl="Hoe laat is het?", sv="Vad är klockan?", ro="Cât e ceasul?", cs="Kolik je hodin?", hu="Hány óra van?", ms="Pukul berapa sekarang?", fil="Anong oras na?", sw="Ni saa ngapi?"),
        c("i-am-vegetarian", "food", None, "I'm vegetarian",
          fa="گیاه‌خوار هستم|giyāh-khār hastam", ar="أنا نباتي|anā nabātī", zh="我吃素|wǒ chī sù", ja="ベジタリアンです|bejitarian desu", ko="채식주의자예요|chaesikjuuijayeyo",
          hi="मैं शाकाहारी हूँ|main shākāhārī hū̃", ru="Я вегетарианец|Ya vegetarianets", th="ฉันกินเจ|chăn kin jee", el="Είμαι χορτοφάγος|Eímai chortofágos", he="אני צמחוני|ani tsimkhoní",
          uk="Я вегетаріанець|Ya vehetarianets'", ur="میں سبزی خور ہوں|main sabzī khor hū̃", bn="আমি নিরামিষাশী|ami niramishashi",
          es="Soy vegetariano", fr="Je suis végétarien", de="Ich bin Vegetarier", pt="Eu sou vegetariano", it="Sono vegetariano", tr="Vejetaryenim", vi="Tôi ăn chay", idn="Saya vegetarian",
          pl="Jestem wegetarianinem", nl="Ik ben vegetariër", sv="Jag är vegetarian", ro="Sunt vegetarian", cs="Jsem vegetarián", hu="Vegetáriánus vagyok", ms="Saya vegetarian", fil="Vegetarian ako", sw="Mimi ni mboga"),
        c("the-bill-please", "food", "formal", "The bill, please",
          fa="صورتحساب لطفاً|surat-hesāb lotfan", ar="الحساب من فضلك|al-ḥisāb min faḍlik", zh="买单|mǎidān", ja="お会計お願いします|o-kaikei onegaishimasu", ko="계산해 주세요|gyesanhae juseyo",
          hi="बिल दीजिए|bil dījiye", ru="Счёт, пожалуйста|Schyot, pozhaluysta", th="เช็คบิลด้วย|chék bin dûai", el="Τον λογαριασμό παρακαλώ|Ton logariasmó parakaló", he="את החשבון בבקשה|et hakheshbón bevakahá",
          uk="Рахунок, будь ласка|Rakhunok, bud' laska", ur="بل دیجئے|bill dījiye", bn="বিল দিন|bill din",
          es="La cuenta, por favor", fr="L'addition, s'il vous plaît", de="Die Rechnung, bitte", pt="A conta, por favor", it="Il conto, per favore", tr="Hesap lütfen", vi="Tính tiền, làm ơn", idn="Minta bon, tolong",
          pl="Poproszę rachunek", nl="De rekening, alstublieft", sv="Notan, tack", ro="Nota de plată, vă rog", cs="Účet, prosím", hu="A számlát kérem", ms="Bil, tolong", fil="Ang bill po", sw="Bili, tafadhali"),
        c("i-agree", "work", None, "I agree",
          fa="موافقم|movāfeqam", ar="أوافق|uwāfiq", zh="我同意|wǒ tóngyì", ja="賛成です|sansei desu", ko="동의해요|donguihaeyo",
          hi="मैं सहमत हूँ|main sahmat hū̃", ru="Я согласен|Ya soglasen", th="ฉันเห็นด้วย|chăn hěn dûai", el="Συμφωνώ|Symfonó", he="אני מסכים|ani maskím",
          uk="Я згоден|Ya zhoden", ur="میں متفق ہوں|main muttafiq hū̃", bn="আমি একমত|ami ekmot",
          es="Estoy de acuerdo", fr="Je suis d'accord", de="Ich stimme zu", pt="Eu concordo", it="Sono d'accordo", tr="Katılıyorum", vi="Tôi đồng ý", idn="Saya setuju",
          pl="Zgadzam się", nl="Ik ben het eens", sv="Jag håller med", ro="Sunt de acord", cs="Souhlasím", hu="Egyetértek", ms="Saya setuju", fil="Sang-ayon ako", sw="Nakubali"),
        c("happy-new-year", "time", None, "Happy New Year",
          fa="سال نو مبارک|sāl-e now mobārak", ar="سنة جديدة سعيدة|sana jadīda saʿīda", zh="新年快乐|xīnnián kuàilè", ja="明けましておめでとう|akemashite omedetō", ko="새해 복 많이 받으세요|saehae bok mani badeuseyo",
          hi="नया साल मुबारक|nayā sāl mubārak", ru="С Новым годом|S Novym godom", th="สวัสดีปีใหม่|sàwàtdii pii mài", el="Καλή χρονιά|Kalí chroniá", he="שנה טובה|shaná tová",
          uk="З Новим роком|Z Novym rokom", ur="نیا سال مبارک|nayā sāl mubārak", bn="শুভ নববর্ষ|shubho nabobarsho",
          es="Feliz Año Nuevo", fr="Bonne année", de="Frohes neues Jahr", pt="Feliz Ano Novo", it="Buon anno", tr="Mutlu yıllar", vi="Chúc mừng năm mới", idn="Selamat tahun baru",
          pl="Szczęśliwego Nowego Roku", nl="Gelukkig nieuwjaar", sv="Gott nytt år", ro="An Nou fericit", cs="Šťastný nový rok", hu="Boldog új évet", ms="Selamat tahun baru", fil="Manigong Bagong Taon", sw="Heri ya Mwaka Mpya"),
    ]


def split_words(text: str, tr: str | None, english: str, lang: str) -> list[dict]:
    tokens = text.replace("؟", "").replace("?", "").replace("!", "").split()
    tr_tokens = (tr or "").split() if tr else []
    if len(tokens) <= 1:
        return [word_obj(text, tr, english, lang)]
    words = []
    for i, tok in enumerate(tokens):
        ttr = tr_tokens[i] if i < len(tr_tokens) else None
        words.append(word_obj(tok, ttr, tok if lang not in NON_LATIN else (ttr or tok), lang))
    return words


def merge_core(concepts, translations, seen_ids):
    for row in core_phrases():
        cid = row["id"]
        if cid in seen_ids:
            continue
        seen_ids.add(cid)
        concepts.append(
            {
                "id": cid,
                "category": row["category"],
                "formality": row["formality"],
                "english": row["english"],
                "source": "curated",
            }
        )
        for lang in LANG_CODES:
            text, tr = row["forms"][lang]
            payload = {
                "text": text,
                "words": split_words(text, tr, row["english"], lang),
            }
            if tr:
                payload["transliteration"] = tr
            translations[lang][cid] = payload


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> None:
    concepts, translations, seen_ids = generate_framed()
    merge_core(concepts, translations, seen_ids)

    # Drop unused import leftovers
    cats: dict[str, int] = {}
    for c in concepts:
        cats[c["category"]] = cats.get(c["category"], 0) + 1

    assert len(concepts) >= 3000, f"need >= 3000 concepts, got {len(concepts)}"
    ids = [c["id"] for c in concepts]
    assert len(ids) == len(set(ids))

    for lang in LANG_CODES:
        missing = [c["id"] for c in concepts if c["id"] not in translations[lang]]
        assert not missing, f"{lang} missing {missing[:5]}"
        empty = [cid for cid, row in translations[lang].items() if not row["text"].strip()]
        assert not empty, f"{lang} empty {empty[:5]}"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    trans_dir = OUT_DIR / "translations"
    trans_dir.mkdir(parents=True, exist_ok=True)

    write_json(OUT_DIR / "languages.json", language_payload())
    write_json(OUT_DIR / "concepts.json", concepts)
    for lang in LANG_CODES:
        fname = lang.replace("-", "_") + ".json"
        write_json(trans_dir / fname, translations[lang])

    # Remove legacy Persian-only catalog if present
    legacy = OUT_DIR / "phrases.json"
    if legacy.exists():
        legacy.unlink()

    print(f"Wrote {len(concepts)} concepts × {len(LANG_CODES)} languages")
    print("by category:", dict(sorted(cats.items())))
    curated = sum(1 for c in concepts if c["source"] == "curated")
    print(f"curated core: {curated}; generated: {len(concepts) - curated}")
    print(f"output: {OUT_DIR}")


if __name__ == "__main__":
    main()

