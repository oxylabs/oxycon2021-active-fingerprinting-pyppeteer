import asyncio

from pyppeteer_stealth import stealth

from browser import get_browser_and_page
from mocks import platform, navigator_ua, timezone, history, plugins
from oxycon2021.constants.urls import (
    HEADLESS_TEST1,
    HEADLESS_TEST2,
    HEADLESS_TEST3,
    FINGERPRINT_STUNDZIALT,
)


options = {
    "waitUntil": [
        "load",
        "domcontentloaded",
        "networkidle2",
    ],
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT
}


async def main(
        url: str,
        headless: bool = True,
        wait_after: int = 5,
        use_proxy: bool = True,
):
    browser, page = await get_browser_and_page(
        use_proxy=use_proxy,
        headless=headless,
        headers=HEADERS,
        fake_audio=True,
    )
    await stealth(page)  # Should beat most tests.
    # await asyncio.sleep(1)
    # await timezone(page)
    # await history(page, 5)
    # await plugins(page, 3)
    # await platform(page, "Win64")
    # await navigator_ua(page, USER_AGENT, platform="Win64")
    response = await page.goto(
        url=url,
        options=options,
    )
    print("Response status: ", response.headers)
    print("Response headers: ", response.headers)

    await asyncio.sleep(wait_after)

    await page.screenshot(
        options={
            "path": "beating_headless_test.png",
            "fullPage": False,
        }
    )
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main(
        url=HEADLESS_TEST3,
        headless=True,
        wait_after=2,
        use_proxy=False,
    ))
