#!/usr/bin/env python3
"""
X account reorganization script.
Deletes 5 old lists, unfollows 332, follows 46 new, creates 10 lists, adds 246 members.
Estimated cost: ~$6.80

DO NOT RUN without reviewing the plan first.
Run with: python3 reorganize.py
"""

import json
import subprocess
import sys
import time

MY_USER_ID = "18781061"
APP = "langkilde"

OLD_LIST_IDS = [
    "954334888995557377",  # annotell
    "941408557379080193",  # venturecap
    "941407284890136576",  # technews
    "941399499230121984",  # machinelearning
    "941398090803830785",  # datacuration
]

FINAL_LISTS = {
    "ai-builders": ["karpathy","tri_dao","natolambert","cwolferesearch","rasbt","hardmaru","swyx","hendrycks","_jasonwei","NoamShazeer","fchollet","ilyasut","ylecun","geoffreyhinton","demishassabis","ShaneLegg","goodfellow_ian","quocleix","drfeifei","lilianweng","polynoamial","denny_zhou","OriolVinyalsML","sedielem","DaniloJRezende","poolio","janexwang","jalayrac","bousmalis","tejasdkulkarni","_rockt","soumithchintala","fhuszar","hugo_larochelle","ryan_p_adams","rsalakhu","nalkalc","johnplattml","tdietterich","SebastienBubeck","yoavgo","arankomatsuzaki","_akhaliq","syhw","MirowskiPiotr","NandoDF","lawrennd","chrmanning","jurafsky","haldaume3","gneubig","guestrin","FrankRHutter","JoakimNivre","pmddomingos","mmitchell_ai","ch402","earnmyturns","matei_zaharia","ctnzr","SchmidhuberAI","RichardSocher","JeffDean","erichorvitz","erikbryn","iamtrask","bernhardsson","eyvindn","dgillblad","FakePsyho","clattner_llvm","janleike","emollick","goodside","davidchalmers42","FredrikHeintz","antonosika","yoheinakajima","Yulun_Du","_LuoFuli","lossfunk","jarredsumner","maxkirkby"],
    "ai-orgs": ["OpenAI","AnthropicAI","GoogleDeepMind","GoogleAI","MetaAI","GenReasoning","MSFTResearch","MIT_CSAIL","stanfordnlp","icmlconf","kognic_","PyTorch","jiqizhixin","EpochAIResearch","MistralAI","nvidia","xAI","deepseek_ai","Alibaba_Qwen","DARPA"],
    "physical-ai-builders": ["qasar","TechTekedra","aelluswamy","olivercameron","chris_urmson","pabbeel","chelseabfinn","DrJimFan","svlevine","BradPorter_","ericjang11"],
    "physical-ai-orgs": ["robotaxi","Tesla_AI","Waymo","aurora_inno","AppliedInt","physical_int","Figure_robot","1x_tech"],
    "operators": ["sama","gdb","mustafasuleyman","woj_zaremba","npew","alexandr_wang","Thom_Wolf","soundboy","AndrewYNg","l2k","jackclarkSF","patrickc","natfriedman","JeffBezos","finkd","tim_cook","satyanadella","eldsjal","klarnaseb","MartinLorentzon","ericschmidt","sundarpichai","BillGates","GustavS","ChrisJBakke","bentossell","karimatiyeh","cahlberg","ankush_gola11","DarioAmodei","DanielaAmodei","arthurmensch","jimkxa","AravSrinivas","aidangomez","elonmusk"],
    "vc-people": ["johanbrenner","Ljungman","simonschmincke","fritjofsson","Jameswise","Maren_Bannon","louicop","maxniederhofer","sophiabendz","bjarkestaun","vkhosla","pmarca","fredwilson","cdixon","reidhoffman","bhorowitz","hdubugras","saranormous","paulg","WarrenBuffett","gustaf","wolfejosh","eladgil","bznotes"],
    "vc-funds": ["creandum","northzoneVC","a16z","sequoia","_fredrik","LuxCapital","EclipseVenture","redglassvc"],
    "personal": ["jkronand","drnovac","JohanHarvard","shelgesson","kallus","oscarlsson","torbjornlundh","johanpaccamonti","flangkilde","liuhuanjim013","rikardsteiber","forskarskolan","emileifrem","jesolem","truve","ZachFlom","joe_hellerstein","evanrsparks","pbailis","JoelEnquist","chalmersuniv","IVA1919"],
    "media-outlets": ["TechCrunch","WIRED","techreview","breakit_se","TheEconomist","TechEmails","stratechery","fermatslibrary"],
    "media-writers": ["KelseyTuoc","_KarenHao","willknight","MMinevich","MimiBilling","karaswisher","ingridlunden","packyM","lillianmli","benedictevans","a_m_mastroianni","rmilneNordic","adwooldridge","LiYuan6","johanknorberg","scaling01","dylan522p","lexfridman","ESYudkowsky","GaryMarcus","slatestarcodex","benthompson","gwern","leopoldasch","SemiAnalysis_","IanCutress","asianometry","chipstrat","crmiller1","dwarkesh_sp"],
}

TO_UNFOLLOW_IDS = {
    "500GlobalVC": "168857946", "Aitellu": "82131783", "AndrzejB52": "316908260",
    "AnnaPJansson": "2182854368", "Anna_Ystroem": "256054354", "ApacheSpark": "1551361069",
    "AstraZeneca": "62465691", "BigDATAwireNews": "317632729", "BigData_": "60959947",
    "ByJohnnyLee": "1504845539468263451", "ChalmersStudent": "434014979", "CircleCI": "381223731",
    "Claudia_Olsson": "2835003459", "CodeWisdom": "396238794", "CompSciFact": "220145170",
    "Dagk": "18130874", "DataJunkie": "11595422", "DataconomyMedia": "2318606822",
    "DeepLearningHub": "2895770934", "Docker": "1138959692", "EMostaque": "407800233",
    "EmilStenstrom": "16038461", "GVteam": "27814665", "Gartner_inc": "15231287",
    "GjoaCLB": "55953023", "GoogleStartups": "2281044080", "GoogleWorkspace": "17003765",
    "Google_Sverige": "149134959", "Haoyuan": "19157755", "HoverStatus": "84093311",
    "IBMwatsonx": "29735775", "Joi": "691353", "K_D_Simmons": "1230382532",
    "KodSnack": "725900462", "LangChain": "1589007443853340672", "LindauLindau": "1452276234",
    "LinkedInEng": "316869223", "MalinEstelli": "606184530", "McKAnalytics": "770385734461190144",
    "MikaelHolmstr": "1341554347", "MikeCafarella": "57556736", "MrChrisJohnson": "29661283",
    "NLTK_org": "2183287052", "OReillyMedia": "11069462", "Porserud": "42634479",
    "ProductHunt": "2208027565", "PrometheusIO": "3173809816", "ProtonPrivacy": "1927923236",
    "Raspberry_Pi": "302666251", "ReactJSNews": "2426422297", "Recode": "2244340904",
    "RecordedFuture": "95292874", "SCB_nyheter": "22117644", "SUP_46": "1582511168",
    "SamaAI": "31685247", "ScalaFriends": "2340978469", "ScalaNLP": "473099533",
    "SebastianBlanco": "29147759", "SiaSearch": "1204059460060303361", "SirPatStew": "602317143",
    "SlackHQ": "1305940272", "StartupGrindSTO": "1149548186", "StartupManage": "1276563415",
    "StephenAtHome": "16303106", "TELUSIntAI_DS": "3294675582", "Tamr_Inc": "2445447283",
    "TeamPraescient": "367580356", "TensorFlow": "254107028", "TheAIConf": "878679838243999749",
    "TinyToCS": "495663839", "TobiasBostrom": "42293", "Valleywag": "9085532",
    "VentureBeat": "60642052", "WWRob": "116897811", "Wallstiftelsen": "517791371",
    "XEng": "6844292", "YacineGhalim": "350026492", "_inesmontani": "14622002",
    "abt_programming": "1606588254", "acmurthy": "39383125", "alansaid": "22994885",
    "allthingsd": "5746402", "amcafee": "15008449", "amplab": "224379103",
    "andrew_n_carr": "3378986176", "andyhpalmer": "21392407", "basistechnology": "104599119",
    "bcherny": "159337660", "bigmlcom": "235821180", "bkrunner": "250722893",
    "brianacton": "21038221", "ceciliauddenm": "29242390", "chalmersTME": "2328762121",
    "chris_biow": "24463816", "crowdgenbyappen": "28165790", "cutting": "7542902",
    "davemcclure": "1081", "davidwkenny": "32868144", "deanwampler": "15232432",
    "deep_thesis": "951136234038026241", "deepenai": "821471635995639808", "dlwh": "8630302",
    "einrideofficial": "834754970834583552", "eli_schiff": "29162709",
    "explosion_ai": "744095828013424640", "exponentfm": "1923374760", "fastml": "798227418",
    "fisherwebdev": "68720435", "garyvee": "5768872", "gavagai_corp": "44869788",
    "genekogan": "51757957", "getfoxtype": "3852400152", "golovashkin": "263859089",
    "heartaerospace": "1146392728886026240", "heyBarsee": "1552871185431527424",
    "holdenkarau": "15594928", "iamdevloper": "564919357", "ilparone": "18134210",
    "jarredsumner": "2489440172", "jaykreps": "126226388", "jaynitx": "1871582672121954304",
    "jlprendki": "3026913266", "johncutlefish": "533409964", "jsrailton": "243032876",
    "kaggle": "80422885", "karenxcheng": "21829724", "kdnuggets": "20167623",
    "kryptera": "144474629", "kubernetesio": "2813398537", "lintool": "114485232",
    "lousylinguist": "48459936", "lufritjofsson": "100546284", "macgirlsweden": "5728752",
    "mailihammargren": "3025514190", "meownessxx": "976673256", "mhausenblas": "817540",
    "michaelarmbrust": "459949985", "miha_jlo": "630671901", "mitchellh": "12819682",
    "mitultiwari": "14704253", "mitvcconference": "27663215", "mljockers": "113764386",
    "mmartynas": "96224514", "molly_g": "15449897", "moxie": "76980293",
    "mreflow": "1544387652811493377", "netnod": "192873466", "ngaleforce": "161155176",
    "nickfloats": "146358342", "nin_artificial": "1494431362568364037", "notch": "63485337",
    "omead": "44481652", "pacoid": "14066472", "patrikhson": "21293468",
    "paulin_dan": "2817005690", "pebourne": "239255514", "petergudmundson": "2308006554",
    "peterneubauer": "14721805", "precisely": "2389949911", "pwendell": "48159875",
    "radar": "14984090", "randhindi": "50722668", "rbordoli": "5921452",
    "reactjs": "1566463268", "reactnative": "3003743254", "richminer": "16407251",
    "rmetzger_": "1970848320", "russelljkaplan": "1075605139", "rxin": "17712257",
    "sagasustainable": "787082013597728768", "sebmarkbage": "18022416", "sfwriter": "12337072",
    "sheeraf": "20052487", "siliconvikings": "300109488", "singularityhub": "15249166",
    "singularityu": "16870421", "sirbonar": "52387673", "sohear": "3799821",
    "spacy_io": "3422200198", "spolsky": "15948437", "squarecog": "46440718",
    "ste_grider": "1018946341", "stefan_vhk": "298021599", "stevesi": "13418072",
    "stingsthlm": "214403744", "strataconf": "167169119", "systematicls": "1779775861589504000",
    "taehoonai": "235786679", "tathadas": "479920148", "thisisdhaas": "417878976",
    "tryolabs": "77909615", "tswaterman": "13408762", "ungaforskare": "51834545",
    "venturehacks": "11620792", "xprize": "15919988", "zen_habits": "15859268",
    # batch 2
    "MahshidHelali": "...", "oerich": "...", "emiliojorge_": "...", "ecarlsn": "...",
    "kyeandersson": "...", "fBeiron": "...", "horken7": "...", "DennisNobelius": "...",
    "johnwetzel": "...", "JohanJaveus": "...", "morrisseyjoe": "...", "NathanThinks": "...",
    "HaddadNavid": "...", "ValdemarL": "...", "gustavmaskowitz": "...", "MichelWesther": "...",
    "rebeckaangstrom": "...", "couch_patrick": "...", "WestmanSanna": "...", "specht_p": "...",
    "d_blomquist": "...", "hillbergs": "...", "TheresiaSH": "...", "MagnusBergman": "...",
    "FredrikHrstedt": "...", "lenamaartensson": "...", "DEbbevi": "...", "GustafTadaa": "...",
    "DElebring": "...", "philipfrick_": "...", "mattias_br": "...", "Klintcho": "...",
    "niklaswicen": "...", "andreasrolen": "...", "kashew": "...", "PeterSMagnusson": "...",
    "JonasLeijon": "...", "stefanlundell": "...", "miriamolsson": "...", "j_jakobsson": "...",
    "viktorstrom": "...", "danielg0ldberg": "...", "puffran": "...", "AmnaPir": "...",
    "sven43": "...", "gunthermarder": "...", "jgreyfriend": "...",
    # batch 3
    "MarieWall1": "...", "agnesorstadius": "...", "pweiderholm": "...", "andersbresell": "...",
    "torbjornhagglof": "...", "lenap61": "...", "kohlschuetter": "...", "RobertGullander": "...",
    "carlrivera": "...", "svejoha": "...", "JohWendt": "...", "IsolaMonte": "...",
    "LinnEfsing": "...", "mo_oscar": "...", "jacob_lundberg": "...", "Mitelman": "...",
    "gustavborgefalk": "...", "TorbjornNilsso": "...", "tdstyret": "...",
    "magnussonhampus": "...", "frick": "...", "SaraJMagnusson": "...", "MariaKWedel": "...",
    "PetterEverydh": "...", "Clobbe": "...", "carincarlsson": "...", "ohlsont": "...",
    "CEE1983": "...", "csvennberg": "...", "Ingemyr": "...", "csholmq": "...",
    "MarcusGidekull": "...", "amanda_s_tevell": "...", "RedNilsson": "...", "BjrnJnssn": "...",
    "liljeste": "...", "mattefnattek": "...", "erikhedlund": "...", "dgottlander": "...",
    "louisewallin": "...", "gustavjoh": "...", "gywillia": "...", "gywilliams": "...",
    "jasonsamuelsson": "...", "deeeepka": "...", "clemensley": "...", "p1dgeon": "...",
    "ArfurRock": "...", "latentjasper": "...", "serkancabi": "...", "jasonjmu": "...",
    "fionaosaurusrex": "...", "Rodelius": "...", "mynameisper": "...", "lotrproject": "...",
    "vetenskapoallm": "...", "EjohPhotography": "...",
    # batch 4
    "emilymbender": "...", "psresnik": "...", "Allen_Schmaltz": "...", "petewarden": "...",
    "ogrisel": "...", "amuellerml": "...", "dpatil": "...", "pierrelux": "...",
    "j_gauthier": "...", "tim_kraska": "...", "jakeporway": "...", "randal_olson": "...",
    "neiltyson": "...", "timberners_lee": "...", "TSchnoebelen": "...",
    "johnmyleswhite": "...", "mdreid": "...",
    # batch 5
    "chalmersnyheter": "...", "ChalmersICT": "...", "KTHuniversity": "...",
    "RISEsweden": "...", "RISE_SICS": "...", "vinnovase": "...",
    "Intize_Gbg": "...", "Mattecentrum": "...", "FHIOxford": "...",
    "EricssonLabs": "...", "combitech": "...", "Spotify": "...",
    "Google": "...", "hackernews__": "...", "ycombinator": "...",
}

NEW_FOLLOWS = [
    "1x_tech","_fabknowledge_","_jasonwei","aidangomez","Alibaba_Qwen",
    "applied_int","AravSrinivas","arthurmensch","asianometry","aurora_inno",
    "BradPorter_","chipstrat","chris_urmson","cikimill","cwolferesearch",
    "DanHendrycks","DanielaAmodei","DarioAmodei","deepseek_ai","elonmusk",
    "EpochAIResearch","ericjang11","Figure_robot","hardmaru","IanCutress",
    "jimkxa","leopold_asch","MistralAI","natolambert","NoamShazeer",
    "nvidia","PaulGChristiano","physical_int","rasbt","svlevine",
    "swyx","tri_dao","Waymo","xAI",
    "wolfejosh","eladgil","bznotes","LuxCapital","EclipseVenture","redglassvc","dwarkesh_sp",
    "SemiAnalysis_","AppliedInt","crmiller1","hendrycks","leopoldasch",
    "MetaAI","GenReasoning","Yulun_Du","_LuoFuli","lossfunk","jarredsumner","maxkirkby",
]


LOG_FILE = "reorganize.log"


def load_log():
    """Returns set of completed operation keys for resume support."""
    done = set()
    list_ids = {}
    if not __import__("os").path.exists(LOG_FILE):
        return done, list_ids
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            op = parts[0]
            done.add(line)
            if op == "created_list" and len(parts) == 3:
                list_ids[parts[1]] = parts[2]
    return done, list_ids


def log(done, key):
    with open(LOG_FILE, "a") as f:
        f.write(key + "\n")
    done.add(key)
    ts = time.strftime("%H:%M:%S")
    print(f"  [{ts}] ✓ {key}", flush=True)


def parse_json(text):
    """Extract first JSON object from text that may have trailing content."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i+1])
                except Exception:
                    return None
    return None


def run(args):
    cmd = ["xurl", "--app", APP] + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        err = parse_json(r.stdout)
        status = err.get("status", 0) if err else 0
        if status == 429:
            now = time.time()
            window = 15 * 60
            next_boundary = (int(now / window) + 1) * window + 30
            wait = next_boundary - now
            ts = time.strftime("%H:%M:%S")
            resume = time.strftime("%H:%M:%S", time.localtime(next_boundary))
            print(f"  [{ts}] Rate limited — sleeping {int(wait)}s until {resume}...", flush=True)
            time.sleep(wait)
            return run(args)
        detail = err.get("detail", r.stdout.strip()) if err else r.stdout.strip()
        print(f"  ERROR {status}: {detail}", flush=True)
        return None
    return parse_json(r.stdout) or r.stdout


def get_user_id(username):
    data = run([f"/2/users/by/username/{username}"])
    if data and "data" in data:
        return data["data"]["id"]
    return None


def follow(user_id):
    return run(["-X", "POST", f"/2/users/{MY_USER_ID}/following",
                "-d", json.dumps({"target_user_id": user_id})])


def unfollow(user_id):
    return run(["-X", "DELETE", f"/2/users/{MY_USER_ID}/following/{user_id}"])


def create_list(name):
    data = run(["-X", "POST", "/2/lists", "-d", json.dumps({"name": name})])
    if data and "data" in data:
        return data["data"]["id"]
    return None


def delete_list(list_id):
    return run(["-X", "DELETE", f"/2/lists/{list_id}"])


def add_to_list(list_id, user_id):
    return run(["-X", "POST", f"/2/lists/{list_id}/members",
                "-d", json.dumps({"user_id": user_id})])


def main():
    done, list_ids = load_log()
    if done:
        print(f"Resuming — {len(done)} operations already completed.")

    # --- STEP 1: Delete old lists ---
    print("\n=== STEP 1: Delete old lists ===")
    for lid in OLD_LIST_IDS:
        key = f"deleted_list:{lid}"
        if key in done:
            print(f"  skip (done): {lid}")
            continue
        result = delete_list(lid)
        if result is not None:
            log(done, key)
        else:
            print(f"  FAILED: delete list {lid}")
        time.sleep(0.3)

    # --- STEP 2: Load cached IDs ---
    print("\n=== STEP 2: Load cached following IDs ===")
    with open("/Users/langkilde/.claude/projects/-Users-langkilde-dev-personal-tools-x-admin/3c0105ad-ab0d-40c7-9c7a-d7365d4bcdb7/tool-results/b783tmwcm.txt") as f:
        cached = json.load(f)
    id_map = {u["username"].lower(): u["id"] for u in cached["data"]}
    # Recover new follow IDs from log
    for entry in done:
        if entry.startswith("followed:"):
            _, uname, uid = entry.split(":")
            id_map[uname.lower()] = uid
    print(f"Loaded {len(id_map)} IDs")

    # --- STEP 3: Follow new accounts ---
    print("\n=== STEP 3: Follow new accounts (46) ===")
    all_final_lower = {h.lower() for handles in FINAL_LISTS.values() for h in handles}
    for username in NEW_FOLLOWS:
        key = f"followed:{username}:{id_map.get(username.lower(), '?')}"
        # Check if already logged (username match is enough)
        if any(e.startswith(f"followed:{username}:") for e in done):
            print(f"  skip (done): @{username}")
            continue
        uid = id_map.get(username.lower())
        if not uid:
            print(f"  Looking up @{username}...")
            uid = get_user_id(username)
            if not uid:
                print(f"  SKIP: could not find @{username}")
                continue
            id_map[username.lower()] = uid
        result = follow(uid)
        if result is not None:
            log(done, f"followed:{username}:{uid}")
        else:
            print(f"  FAILED: follow @{username}")
        time.sleep(0.5)

    # --- STEP 4: Unfollow accounts ---
    print("\n=== STEP 4: Unfollow 332 accounts ===")
    unfollowed = skipped = 0
    for username, uid in TO_UNFOLLOW_IDS.items():
        if username.lower() in all_final_lower:
            skipped += 1
            continue
        if any(e.startswith(f"unfollowed:{username}:") for e in done):
            print(f"  skip (done): @{username}")
            continue
        if uid == "...":
            uid = id_map.get(username.lower())
            if not uid:
                print(f"  SKIP (no ID): @{username}")
                continue
        result = unfollow(uid)
        if result is not None:
            log(done, f"unfollowed:{username}:{uid}")
            unfollowed += 1
        else:
            print(f"  FAILED: unfollow @{username}")
        time.sleep(0.3)
    print(f"Unfollowed: {unfollowed}, skipped (in final list): {skipped}")

    # --- STEP 5: Create new lists ---
    print("\n=== STEP 5: Create 10 new lists ===")
    for list_name in FINAL_LISTS:
        if list_name in list_ids:
            print(f"  skip (done): {list_name} → {list_ids[list_name]}")
            continue
        lid = create_list(list_name)
        if lid:
            list_ids[list_name] = lid
            log(done, f"created_list:{list_name}:{lid}")
        else:
            print(f"  FAILED: create list '{list_name}'")
        time.sleep(0.5)

    # --- STEP 6: Add members to lists ---
    print("\n=== STEP 6: Add 246 members to lists ===")
    for list_name, handles in FINAL_LISTS.items():
        lid = list_ids.get(list_name)
        if not lid:
            print(f"  SKIP list '{list_name}': no ID (creation may have failed)")
            continue
        print(f"  Populating '{list_name}' ({len(handles)} members)...")
        for username in handles:
            if any(e.startswith(f"added:{list_name}:{username}:") for e in done):
                continue
            uid = id_map.get(username.lower())
            if not uid:
                print(f"    SKIP @{username}: no ID")
                continue
            result = add_to_list(lid, uid)
            if result is not None:
                log(done, f"added:{list_name}:{username}:{uid}")
            else:
                print(f"    FAILED: add @{username} to {list_name}")
            time.sleep(0.3)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
