import random
import time
from playwright.sync_api import sync_playwright, Error
import json

class MacbookBot:
    def __init__(self):
        self.request_count = 0
       
    def delaydelay(self):
        self.request_count += 1
        if self.request_count > 100:
            base_delay = 15
        elif self.request_count > 50:
            base_delay = 7
        else:
            base_delay = 3
        delay = random.uniform(base_delay, base_delay * 3)
        time.sleep(delay)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.popmart.com/us/brand-ip/21/LABUBU')
    page.wait_for_timeout(5000)

    bot = MacbookBot()

    while True:
        try:
            result = page.evaluate(
                """
                async () => {
                    const res = await fetch("https://prod-na-api.popmart.com/shop/v3/shop/productOnCollection", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/json, text/plain, */*"
                        },
                        body: JSON.stringify({
                            "pageSize": 20,
                            "page": 1,
                            "sortWay": 1,
                            "brandIDs": [21],
                            "categoryIDs": [],
                            "s": "0f039f11769fde84755449dfeccffc8b",
                            "t": 1753366884
                        })
                    });
                    return await res.json();
                }
                """
            )

            print("✅ Page retrieved successfully")
            print(json.dumps(result, indent=2))

            if 'captcha' in json.dumps(result).lower():
                print("🚨 CAPTCHA detected")

            bot.delaydelay()

        except Error as e:
            print(f"❌ Error occurred: {e}")
            break






