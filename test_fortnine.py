from playwright.sync_api import sync_playwright
import pytest


@pytest.fixture(scope="module")
def context():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )  # Set headless=True to run in the background
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="module")
def page(context):
    page = context.new_page()
    yield page
    page.close()


def test_homepage(page):
    # Navigate to the FortNine website
    page.goto("https://fortnine.ca/en")
    page.wait_for_selector("body")

    # Go to motorcycle helmets page
    motorcycle_helmets_link = page.locator("#maincontent").get_by_role("link", name="Motorcycle Helmets")

    assert motorcycle_helmets_link is not None, "Link to Motorcycle Helmets not found"
    assert (
        motorcycle_helmets_link.get_attribute("href") == "https://fortnine.ca/en/motorcycle-helmets"
    ), "Link to Motorcycle Helmets is incorrect"
    motorcycle_helmets_link.click()


def test_motorcycle_helmets(page):
    assert "motorcycle-helmets" in page.url, "Not on motorcycle helmets page"
    page.wait_for_selector("body")

    helmet_link = page.get_by_role("link", name="AGV K1 S Solid Helmet $309.99")
    assert helmet_link is not None, "Link to AGV K1 S Solid Helmet not found"
    assert (
        helmet_link.get_attribute("href") == "https://fortnine.ca/en/agv-k1-s-solid-helmet"
    ), "Link to AGV K1 S Solid Helmet is incorrect"
    helmet_link.click()


def test_AGV_K1_S_Solid_Helmet(page):
    # Navigate to the AGV K1 S Solid Helmet page
    assert "agv-k1-s-solid-helmet" in page.url, "Not on AGV K1 S Solid Helmet page"

    # Get 2 white, medium helmets
    page.get_by_label("Color").select_option("14")
    page.get_by_label("Size").select_option("10")
    page.get_by_placeholder("Qty").fill("2")

    assert page.get_by_label("Color").input_value() == "14", "Incorrect color selected"
    assert page.get_by_label("Size").input_value() == "10", "Incorrect size selected"
    assert page.get_by_placeholder("Qty").input_value() == "2", "Quantity not set correctly"
    
    # Add to cart
    cart_link = page.get_by_role("button", name="Add to Cart")
    assert cart_link is not None, "Add to Cart button not found"
    cart_link.click()

def test_cart(page):

    helmet = page.get_by_role("link", name="AGV K1 S Solid Helmet Options")
    assert helmet is not None, "AGV K1 S Solid Helmet not found in cart"
    assert (
        helmet.get_attribute("href") == "https://fortnine.ca/en/agv-k1-s-solid-helmet"
    ), "AGV K1 S Solid Helmet link is incorrect"
    assert helmet.get_by_text("Qty: 2").is_visible(), "Incorrect quantity in cart"
    assert helmet.get_by_text("White M").is_visible(), "Incorrect color or size in cart"
