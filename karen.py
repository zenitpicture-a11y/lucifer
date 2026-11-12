import requests
import random
from mnemonic import Mnemonic

# لیست کلمات استاندارد BIP39
WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse",
    # ... (بقیه کلمات را برای خلاصه اینجا نگذارم، اما در کد کامل هست)
]

def get_random_mnemonic():
    mnemo = Mnemonic("english")
    return mnemo.generate(128)

def get_tron_address(mnemonic):
    # استفاده از کتابخانه سبک‌تر یا مستقیم API
    # برای سادگی، فرض می‌کنیم کاربر کتابخانه tronpy را دارد
    # اگر ندارد، این بخش را با API مستقیم جایگزین می‌کنیم
    try:
        from tronapi import Tron
        tron_instance = Tron()
        account = tron_instance.to_tron_account(mnemonic)
        return account.address
    except ImportError:
        # اگر tronpy نصب نیست، آدرس را محاسبه می‌کنیم
        # (این بخش پیچیده است، پس بهتر است پکیج را نصب کنیم)
        return "TRON_PY_MISSING"

def check_balance(address):
    url = f"https://api.trongrid.io/v1/accounts/{address}/tokens"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            total_usd = 0
            for token in data.get('data', []):
                balance = float(token.get('balance', 0)) / (10 ** int(token.get('token_id', 0))) # Simplified logic
                # قیمت واقعی نیاز به API جداگانه دارد
                total_usd += balance * float(token.get('price_usd', 0))
            return total_usd
    except Exception as e:
        print(f"Error checking {address}: {e}")
    return 0

if __name__ == "__main__":
    print("Starting Karen Crawler...")
    for i in range(5):
        mnem = get_random_mnemonic()
        addr = get_tron_address(mnem)
        bal = check_balance(addr)
        if bal > 0:
            print(f"[!] FOUND BALANCE: {addr} - ${bal}")
        else:
            print(f"Checked {addr[:10]}...${bal}")
