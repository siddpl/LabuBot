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
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]

    context.storage_state(path="state.json")
    print("Session saved to state.json")

    intercepted = {}

    def handle_request(request):
        if "productOnCollection" in request.url and request.method == "POST":
            print("Captured request to:", request.url)
            intercepted["url"] = request.url
            intercepted["headers"] = request.headers
            intercepted["body"] = request.post_data

            # Save to file for later use
            with open("intercepted_request.json", "w") as f:
                json.dump(intercepted, f, indent=2)
            print("Saved to intercepted_request.json")

    page.on("request", handle_request)

    print(" Waiting for request to be triggered manually in tab...")
    page.wait_for_timeout(30000)  # 30 seconds to let the page load & trigger request

    if not intercepted:
        print(" No request was intercepted. Try scrolling or reloading the page.")
    else:
        print(" Request captured! Ready to replay.")

        try:
            result = page.evaluate(
                f"""
                async () => {{
                    const res = await fetch("{intercepted['url']}", {{
                        method: "POST",
                        headers: {json.dumps(intercepted['headers'])},
                        body: `{intercepted['body']}`
                    }});
                    return await res.json();
                }}
                """
            )

            print(" Page retrieved successfully")
            print(json.dumps(result, indent=2))

            if result.get("data", {}).get("productData") is None:
                print(" Still nothing — possibly blocked again.")
            else:
                print(" Got product data!")

            if 'captcha' in json.dumps(result).lower():
                print(" CAPTCHA detected again!")

            bot = MacbookBot()
            bot.delaydelay()

        except Error as e:
            print(f" Error occurred: {e}")






    

        