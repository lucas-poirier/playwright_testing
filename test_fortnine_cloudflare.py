from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import pytest
import random, time

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

def random_sleep():
    time.sleep(random.uniform(1, 3))


@pytest.fixture()
def browser():
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Set headless=False to see the browser

        yield browser

        browser.close()
        

@pytest.fixture()
def page(browser):
    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1280, "height": 800},
        locale="en_US",
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        },
    )

    # Avoiding cloudflare detection
    context.add_init_script(
        """
    // Mask navigator.webdriver to avoid detection
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false
    });

    // Add realistic plugins and language properties
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });

    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
    });

    // Pass the chrome test
    window.navigator.chrome = {
        runtime: {},
    };

    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
    Promise.resolve({ state: Notification.permission }) :
    originalQuery(parameters)
        );
    """
    )
    page = context.new_page()
    stealth_sync(page)

    yield page
    context.close()


def test_homepage(page):
    # Navigate to the FortNine website
    page.goto("https://fortnine.ca/en")

    # Wait for the page to load
    page.wait_for_selector("body")
    link = page.query_selector('a[data-content-piece="Motorcycle Helmets"][class="symmetry-sides-subdued symmetry-sides-icon-big-right symmetry-sides"]')
    assert link is not None, "Link to Motorcycle Helmets not found"
    assert link.get_attribute("href") == "https://fortnine.ca/en/motorcycle-helmets", "Link to Motorcycle Helmets is incorrect"

def test_motorcycle_helmets(page):
    #Navigate to the motorcycle helmets page
    page.goto("https://fortnine.ca/en/motorcycle-helmets")
    page.wait_for_selector("body")
    link = page.query_selector('a[data-content-piece="[951054] AGV K1 S Solid Helmet"]')
    assert link is not None, "Link to AGV K1 S Solid Helmet not found"
    assert link.get_attribute("href") == "https://fortnine.ca/en/agv-k1-s-solid-helmet", "Link to AGV K1 S Solid Helmet is incorrect"

def test_AGV_K1_S_Solid_Helmet(page):
    # Navigate to the AGV K1 S Solid Helmet page
    page.goto("https://fortnine.ca/en/agv-k1-s-solid-helmet")
    # page.wait_for_load_state("networkidle")
    # page.wait_for_selector("body")
    time.sleep(10)

    # Select the white color
    page.wait_for_selector('select#attribute76')
    page.select_option("select#attribute76", value="14")
    time.sleep(5)


    # Select the M size
    page.wait_for_selector('select#attribute493')
    page.select_option("select#attribute493", value="10")


    # Input the quantity
    page.fill('input#qty', '2')


    # Test Selected values
    selected_color = page.query_selector('select#attribute76').input_value()
    assert selected_color == "14", "Incorrect color selected"
    selected_size = page.query_selector('select#attribute493').input_value()
    assert selected_size == "10", "Incorrect size selected"
    quantity = page.query_selector('input#qty').input_value()
    assert quantity == "2", "Quantity not set correctly"



