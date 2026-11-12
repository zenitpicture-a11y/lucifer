import random
import time
import logging
import requests
from datetime import datetime
from eth_account import Account
from tronapy import Tron
from tronapi.contract import TronContract
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
import os

# تنظیمات لاگینگ برای گیت‌هاب اکتیونز
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LuciferScanner:
    def __init__(self):
        # آدرس‌های RPC عمومی برای سرعت بهتر
        self.eth_rpc = "https://eth.llamarpc.com"
        self.bsc_rpc = "https://bsc-dataseed1.defibit.io"
        self.tron_rpc = "http://api.trongrid.io"
        
        # توکن‌های معروف برای اسکن (آدرس قرارداد)
        self.tokens = {
            "USDT": {"address": "0xdac17f958d2ee523a2206206994597c13d831ec7", "decimals": 6},
            "SHIB": {"address": "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4c4", "decimals": 8},
            "PEPE": {"address": "0x6982508075e77022a00848bbE195F4e104AC31C2", "decimals": 18}
        }

    def get_random_mnemonic(self):
        """تولید یک عبارت Mnemonic معتبر"""
        wordlist = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse",
            "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
            "action", "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit",
            "adult", "age", "agent", "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
            "alert", "alibi", "align", "alive", "all", "alley", "almost", "alone", "alpha", "already",
            "alter", "always", "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient",
            "anger", "angle", "angry", "animal", "ankle", "announce", "annual", "another", "answer", "antenna",
            "anticipate", "anxious", "any", "apart", "apology", "appear", "apple", "approve", "april", "arch",
            "arctic", "area", "arena", "argue", "arm", "armed", "armor", "army", "around", "arrange", "arrest",
            "arrive", "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset",
            "assist", "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
            "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid", "awake",
            "aware", "awesome", "awful", "awkward", "axis", "baby", "bachelor", "bacon", "badge", "bag",
            "balance", "balcony", "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel",
            "base", "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become", "beef",
            "before", "begin", "behave", "behind", "believe", "bell", "benefit", "best", "betray", "better",
            "between", "beyond", "bicycle", "bid", "bike", "bin", "binary", "bird", "birth", "bitter",
            "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood", "blossom",
            "blush", "board", "boat", "body", "boil", "bomb", "bone", "bonus", "book", "boost", "border",
            "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass",
            "brave", "bread", "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk", "broccoli",
            "broken", "bronze", "broom", "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo",
            "build", "bulb", "bulk", "bullet", "bundle", "bunny", "burden", "burger", "burst", "bus",
            "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable", "cactus", "cage",
            "cake", "call", "calm", "camera", "camp", "can", "canal", "cancel", "candy", "cannon", "canoe",
            "canvas", "canyon", "capable", "capital", "captain", "car", "carbon", "card", "cargo", "carpet",
            "carry", "cart", "case", "cash", "casino", "castle", "casual", "cat", "catalog", "catch", "category",
            "cattle", "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census", "century",
            "cereal", "certain", "chair", "chalk", "chase", "cheap", "check", "cheese", "chef", "cherry",
            "chest", "chicken", "chief", "child", "chimney", "choice", "choose", "chronic", "cinnamon", "chunk",
            "cigar", "citizen", "city", "civil", "claim", "clap", "clarify", "claw", "clay", "clean", "clerk",
            "clever", "click", "client", "cliff", "climb", "clinic", "clip", "clock", "close", "cloth",
            "cloud", "club", "clown", "cluster", "coach", "coast", "coconut", "code", "coffee", "coil",
            "coin", "collect", "color", "column", "combine", "come", "comfort", "comic", "common", "company",
            "concert", "conduct", "confirm", "congress", "connect", "consider", "control", "convince", "cook",
            "cool", "copper", "copy", "coral", "core", "corn", "correct", "cost", "cotton", "couch", "country",
            "couple", "course", "cousin", "cover", "coyote", "crack", "cradle", "craft", "cram", "crane",
            "crash", "crater", "crawl", "crazy", "cream", "credit", "creek", "crew", "cricket", "crime",
            "crisp", "critic", "crop", "cross", "cruise", "crumble", "cry", "crystal", "cube", "culture",
            "cup", "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom", "cycle", "dad",
            "damage", "damp", "dance", "danger", "daring", "dash", "daughter", "dawn", "day", "deal",
            "debate", "debris", "decade", "december", "decide", "decline", "decorate", "decrease", "deer",
            "defense", "define", "defy", "degree", "delay", "deliver", "demand", "deny", "depart", "depend",
            "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk", "despair", "destroy",
            "detail", "detect", "develop", "device", "devote", "diagram", "dial", "diamond", "diary", "dice",
            "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur", "direct", "dirt",
            "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display", "distance", "divert",
            "divide", "divorced", "do", "dodge", "dog", "donor", "door", "dose", "double", "dove", "draft",
            "dragon", "drama", "draw", "dream", "dress", "drift", "drill", "drink", "drip", "drive", "drop",
            "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf", "dynamic",
            "eager", "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo", "ecology", "economy",
            "edge", "edit", "educate", "effort", "eight", "either", "elbow", "elder", "electric", "elegant",
            "element", "elephant", "elevator", "elite", "else", "embark", "embody", "embrace", "emerge",
            "emotion", "employ", "empower", "empty", "enable", "encourage", "end", "endless", "endorse",
            "enemy", "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlist", "enough",
            "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope", "episode", "equal", "equip",
            "era", "erase", "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate",
            "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example", "excess",
            "exchange", "excite", "exclude", "excuse", "execute", "exercise", "exhaust", "exhibit", "exit",
            "exotic", "expand", "expect", "expire", "explain", "expose", "express", "extend", "extra",
            "eye", "eyebrow", "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false",
            "fame", "family", "famous", "fan", "fantasy", "farm", "fashion", "fat", "fatal", "father",
            "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed", "feel",
            "female", "fence", "festival", "fetch", "fever", "few", "fiber", "fiction", "field", "figure",
            "file", "film", "filter", "final", "find", "fine", "finger", "finish", "fire", "firm",
            "first", "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat",
            "flavor", "flee", "flight", "flip", "float", "flock", "floor", "flower", "fluid", "flush",
            "fly", "foam", "focus", "fog", "foil", "fold", "follow", "food", "foot", "force", "forest",
            "forget", "fork", "fortune", "forum", "forward", "fossil", "foster", "found", "fox",
            "fragile", "frame", "frequent", "fresh", "friend", "frog", "front", "frost", "frown", "fruit",
            "fuel", "fun", "funny", "furnace", "fury", "future", "gadget", "gain", "galaxy", "gallery",
            "game", "gap", "garage", "garbage", "garden", "garlic", "gas", "gasp", "gate", "gather",
            "gauge", "gaze", "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost",
            "giant", "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance", "glass",
            "glide", "glimpse", "globe", "gloom", "glory", "glove", "glow", "glue", "goat", "goddess",
            "gold", "good", "goose", "gorilla", "gospel", "gossip", "govern", "grab", "grace", "grain",
            "grant", "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit", "grocery",
            "group", "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar", "gun", "gym",
            "habit", "hair", "half", "hammer", "hamster", "hand", "happy", "harbor", "hard", "harsh",
            "harvest", "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy", "hedgehog",
            "height", "hello", "helmet", "help", "her", "hide", "high", "hill", "hint", "hip", "hire",
            "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow", "home", "honey", "hood",
            "hope", "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover", "hub",
            "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "husband",
            "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill", "illegal", "illness",
            "image", "imitate", "immense", "immune", "impact", "impose", "improve", "impulse", "inch",
            "include", "income", "increase", "index", "indicate", "indoor", "industry", "infant",
            "inflict", "inform", "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner",
            "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire", "install", "intact",
            "interest", "into", "invest", "invite", "involve", "iron", "island", "isolate", "issue",
            "item", "ivory", "jacket", "jaguar", "january", "japan", "jelly", "jewel", "job", "join",
            "joke", "journey", "judge", "juice", "jump", "jungle", "july", "junior", "jupiter", "justice",
            "keen", "keep", "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit",
            "kitchen", "kite", "kitten", "knife", "knob", "knock", "know", "label", "labor", "ladder",
            "lady", "lake", "lamp", "language", "laptop", "large", "later", "latin", "last", "late",
            "laugh", "launch", "lawsuit", "lawyer", "lay", "layer", "lazy", "leader", "leaf", "learn",
            "leave", "lecture", "left", "leg", "legend", "length", "lens", "leopard", "lesson", "letter",
            "level", "liberty", "library", "license", "life", "lift", "light", "like", "limb", "limit",
            "link", "lion", "liquid", "list", "little", "live", "lizard", "load", "loan", "lobster",
            "local", "logic", "log", "lonely", "long", "loop", "lottery", "loud", "lounge", "love",
            "loyal", "lucky", "luggage", "lumber", "lunar", "lung", "luxury", "machine", "magazine",
            "magnet", "maid", "mail", "main", "major", "make", "mammal", "man", "manage", "mandate",
            "mango", "mansion", "manual", "maple", "marble", "march", "margin", "marine", "market",
            "marriage", "mask", "mass", "master", "match", "material", "math", "matrix", "matter",
            "maximum", "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal", "media",
            "melody", "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry",
            "mesh", "message", "metal", "method", "middle", "midnight", "milk", "million", "mind",
            "minute", "mini", "minister", "mint", "mirror", "miss", "mistake", "mix", "mixed",
            "mixture", "mobile", "model", "modify", "mom", "moment", "monitor", "monkey", "month",
            "moon", "moral", "more", "morning", "mosquito", "mother", "motion", "motor", "mountain",
            "mouse", "move", "movie", "much", "multiplier", "muscle", "museum", "mushroom", "music",
            "must", "mutual", "myself", "mystery", "myth", "naive", "name", "napkin", "narrow",
            "nasty", "nation", "nature", "near", "neck", "need", "negative", "neglect", "neither",
            "nephew", "nerve", "nest", "net", "network", "neutral", "never", "news", "next",
            "nice", "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose",
            "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number", "nurse",
            "nut", "ocean", "offer", "often", "oil", "okay", "old", "olive", "olympic", "omit",
            "once", "one", "onion", "online", "only", "open", "opera", "opinion", "opponent",
            "opportunity", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ",
            "orient", "origin", "other", "ounce", "out", "outcome", "outside", "oven", "over",
            "owner", "oxygen", "oyster", "ozone", "pace", "pack", "package", "page", "pain",
            "paint", "pair", "palace", "palm", "panda", "panel", "panic", "panther", "paper",
            "parade", "parent", "park", "part", "party", "pass", "past", "patch", "path",
            "patient", "patrol", "pattern", "pause", "paw", "peak", "peanut", "pear", "peasant",
            "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person",
            "pet", "phone", "photo", "phrase", "physical", "piano", "picnic", "picture", "piece",
            "pig", "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch",
            "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge", "pluck",
            "plug", "plunge", "poem", "point", "polar", "pole", "police", "pond", "pony",
            "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery",
            "poverty", "powder", "power", "practice", "praise", "predict", "prefer", "prepare",
            "present", "pretty", "prevent", "price", "pride", "primary", "print", "priority",
            "prison", "private", "prize", "problem", "process", "produce", "product", "profit",
            "program", "project", "proof", "prop", "proper", "protect", "proud", "provide",
            "public", "pudding", "pull", "pulp", "pump", "punch", "punishment", "purpose",
            "pure", "push", "put", "quality", "quantum", "quarter", "question", "quick",
            "quiet", "quit", "quote", "rabbit", "raccoon", "race", "rack", "radar", "radio",
            "rain", "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare",
            "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason", "rebel",
            "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect",
            "reform", "refuse", "region", "regret", "regular", "reject", "relax", "release",
            "relief", "rely", "remain", "remember", "remind", "remove", "render", "renew",
            "rent", "reopen", "repair", "repeat", "replace", "report", "require", "rescue",
            "resent", "resist", "resource", "response", "result", "retire", "retreat", "return",
            "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice", "rich",
            "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "ripple", "rise",
            "risk", "ritual", "rival", "river", "road", "roast", "robot", "robust", "rocket",
            "romance", "roof", "rookie", "room", "rose", "rotate", "rough", "round", "route",
            "royal", "rubber", "rude", "rug", "rule", "run", "runner", "rush", "rust",
            "rural", "sad", "saddle", "sadness", "safe", "sail", "salad", "salmon", "salon",
            "salt", "salute", "same", "sample", "sand", "satisfaction", "save", "say", "scale",
            "scan", "scare", "scatter", "scene", "scheme", "school", "science", "scissors",
            "scorpion", "score", "scout", "scrap", "screen", "script", "sea", "search",
            "season", "seat", "second", "secret", "section", "security", "seed", "seek",
            "segment", "select", "sell", "senior", "sense", "sentence", "series", "service",
            "session", "settle", "setup", "seven", "shadow", "shaft", "shake", "shall",
            "shame", "shape", "share", "sharp", "she", "shed", "shield", "shift", "shine",
            "ship", "shiver", "shock", "shoe", "shoot", "shop", "short", "shoulder", "shovel",
            "show", "shrimp", "scholarship", "shut", "sign", "silence", "silk", "silly",
            "silver", "similar", "simple", "sin", "sing", "singer", "single", "sink",
            "sister", "sit", "site", "situation", "six", "size", "skate", "skill", "skin",
            "skirt", "sky", "slab", "slave", "sleep", "slice", "slide", "slight", "slim",
            "slope", "slow", "small", "smart", "smell", "smile", "smoke", "smooth", "snack",
            "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soft",
            "soil", "solar", "soldier", "solid", "solution", "solve", "some", "son",
            "song", "soon", "sort", "soul", "sound", "soup", "source", "south", "space",
            "spare", "spark", "speak", "special", "species", "specific", "speech", "speed",
            "spend", "spider", "spin", "spirit", "split", "sponsor", "sport", "spot",
            "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable",
            "stadium", "staff", "stage", "stairs", "stamp", "stand", "start", "state",
            "stay", "steak", "steel", "stem", "step", "stereo", "stick", "still", "stock",
            "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike",
            "strong", "struggle", "student", "stuff", "stumble", "style", "subject",
            "submit", "subway", "success", "such", "sudden", "suffer", "sugar", "suggest",
            "suit", "summer", "sun", "sunny", "sunset", "super", "supply", "supreme",
            "sure", "surface", "surge", "surprise", "surround", "survey", "suspect",
            "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swim",
            "swing", "switch", "sword", "symbol", "symptom", "system", "table", "tackle",
            "tag", "tail", "talent", "talk", "tank", "tape", "target", "task", "taste",
            "tax", "tea", "teach", "team", "tell", "ten", "tenant", "tennis", "tent",
            "term", "test", "text", "thank", "that", "theme", "then", "theory", "there",
            "they", "thing", "this", "thought", "three", "thrive", "throw", "thumb",
            "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time", "tiny",
            "tip", "tired", "tissue", "title", "toast", "today", "toilet", "token",
            "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total",
            "tourist", "toward", "tower", "town", "toy", "track", "trade", "traffic",
            "tragic", "train", "transfer", "trap", "trash", "travel", "tray", "treat",
            "tree", "trend", "trial", "tribe", "trick", "trigger", "trim", "trip",
            "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust", "truth",
            "try", "tube", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve",
            "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly",
            "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo",
            "unfair", "unfold", "unhappy", "uniform", "unique", "unit", "universe",
            "unknown", "unlock", "until", "unusual", "up", "upon", "upper", "upset",
            "urban", "urge", "usage", "use", "used", "useful", "useless", "user",
            "usher", "usual", "utility", "vacant", "vague", "valid", "valley",
            "valve", "van", "vanish", "vapor", "various", "vast", "vault", "vehicle",
            "velvet", "vendor", "venture", "venue", "verb", "verify", "version",
            "very", "vessel", "veteran", "viable", "vibrant", "vicious", "victory",
            "video", "view", "village", "violate", "violence", "virtual", "virus",
            "visa", "visit", "visual", "vital", "vivid", "vocal", "voice", "void",
            "volcano", "volume", "vote", "voyage", "wage", "wait", "walk", "wall",
            "walnut", "want", "warfare", "warm", "warrior", "wash", "was", "wasp",
            "waste", "water", "wave", "way", "wealth", "weapon", "wear", "weasel",
            "weather", "web", "wedding", "weekend", "weird", "weight", "well",
            "west", "wet", "whale", "what", "wheat", "wheel", "when", "where",
            "whip", "whisper", "wide", "width", "wife", "wild", "will", "win",
            "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom",
            "wise", "wish", "withdraw", "within", "without", "witness", "wolf",
            "woman", "wonder", "wood", "wool", "word", "work", "world", "worry",
            "worth", "wrap", "wreck", "wrestle", "wrist", "write", "wrong",
            "yard", "year", "yellow", "you", "young", "youth", "zebra", "zero",
            "zone", "zoo"
        ]
        try:
            return ' '.join(random.sample(wordlist, 12))
        except Exception as e:
            logger.error(f"Mnemonic generation error: {e}")
            return None

    def derive_addresses(self, mnemonic):
        addresses = {}
        try:
            # ETH & BSC
            acc = Account.from_mnemonic(mnemonic)
            addresses['ETH'] = acc.address
            addresses['BSC'] = acc.address
            
            # TRON
            seed = Bip39SeedGenerator(mnemonic).Generate()
            bip44 = Bip44.FromSeed(seed, Bip44Coins.TRON)
            priv_key_bytes = bip44.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PrivateKey().Raw().ToBytes()
            addresses['TRX'] = TronPrivateKey(priv_key_bytes).public_key.to_base58check_address()
            
            return addresses
        except Exception as e:
            logger.error(f"Derivation error: {e}")
            return {}

    def check_evm_balance(self, rpc_url, address):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": 1
        }
        try:
            res = requests.post(rpc_url, json=payload, timeout=5)
            bal_wei = int(res.json().get('result', '0x0'), 16)
            return bal_wei / 1e18
        except:
            return 0

    def check_tron_balance(self, address):
        try:
            tron = Tron(full_node=self.tron_rpc, grid_node=self.tron_rpc)
            addr_obj = tron.get_account(address)
            return addr_obj.get('balance', 0) / 1e6
        except:
            return 0

    def check_tokens(self, rpc_url, address):
        found_tokens = []
        for token_name, token_info in self.tokens.items():
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_call",
                "params": [{
                    "to": token_info["address"],
                    "data": f"0x70a08231{address[2:].zfill(64)}"
                }, "latest"],
                "id": 1
            }
            try:
                res = requests.post(rpc_url, json=payload, timeout=5)
                result = res.json().get('result', '0x0')
                if result != '0x0':
                    balance = int(result, 16) / (10 ** token_info['decimals'])
                    if balance > 0:
                        found_tokens.append(f"{token_name}: {balance:.4f}")
            except:
                continue
        return found_tokens

    def run(self):
        logger.info("Lucifer Scanner started...")
        count = 0
        while True:
            try:
                mnem = self.get_random_mnemonic()
                if not mnem:
                    continue
                
                addrs = self.derive_addresses(mnem)
                if not addrs:
                    continue
                
                results = []
                
                # Check EVM
                eth_bal = self.check_evm_balance(self.eth_rpc, addrs['ETH'])
                bsc_bal = self.check_evm_balance(self.bsc_rpc, addrs['BSC'])
                
                if eth_bal > 0:
                    results.append(f"ETH: {eth_bal:.6f}")
                if bsc_bal > 0:
                    results.append(f"BSC: {bsc_bal:.6f}")
                    
                # Check Tokens on ETH
                if eth_bal > 0 or len(results) == 0: # Only check tokens if ETH has some activity or we want to be thorough
                     tokens = self.check_tokens(self.eth_rpc, addrs['ETH'])
                     results.extend(tokens)

                # Check TRON
                trx_bal = self.check_tron_balance(addrs['TRX'])
                if trx_bal > 0:
                    results.append(f"TRX: {trx_bal:.4f}")

                if results:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    msg = f"🔥 Found Wallet!\n\n📅 Time: {timestamp}\n🗝️ MN: `{mnem}`\n💰 Balances:\n" + "\n".join(results)
                    
                    # Send to Telegram
                    send_telegram(msg)
                    logger.info(f"Found! {msg}")
                
                count += 1
                if count % 100 == 0:
                    logger.info(f"Scanned: {count} wallets")
                
                time.sleep(0.5)

            except KeyboardInterrupt:
                logger.info("Stopping scanner...")
                break
            except Exception as e:
                logger.error(f"Error in loop: {e}")
                time.sleep(1)

def send_telegram(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logger.warning("Telegram secrets not set.")
        print(f"[LOCAL] {message}")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        logger.error(f"Telegram error: {e}")

if __name__ == "__main__":
    scanner = LuciferScanner()
    scanner.run()
