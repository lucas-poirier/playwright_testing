from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import random, time

def random_sleep():
    time.sleep(random.uniform(1, 3))

def test_fortnine():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Set headless=True to run in the background
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en_US")
        page = context.new_page()
        # stealth_sync(page)

        # Navigate to the FortNine website
        page.goto("https://fortnine.ca/en/agv-k1-s-solid-helmet")


        # Wait for the page to load
        # page.wait_for_load_state("networkidle")
        page.wait_for_selector("body")



        # #Go to motorcycle helmets
        # page.locator('a[data-content-piece="Motorcycle Helmets"][class="symmetry-sides-subdued symmetry-sides-icon-big-right symmetry-sides"]').click()
        # page.wait_for_selector("body")


        # # Select AGV K1 S Solid Helmet
        # page.locator('a[data-content-piece="[951054] AGV K1 S Solid Helmet"]').click()
        # # Wait for the page to load
        

        # Select the white color
        page.select_option('select#attribute76', value='14')
        #Select the XS size
        page.select_option('select#attribute493', value='11')
        # Input the quantity
        page.fill('input#qty', '2')
        # Add to cart
        page.click('button#product-addtocart-button')
        # page.wait_for_selector("body")
        # page.pause()
        browser.close()

