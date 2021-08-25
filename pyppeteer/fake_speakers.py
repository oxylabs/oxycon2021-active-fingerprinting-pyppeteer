import asyncio

from browser import get_browser_and_page
from urls import WEBRTC


options = {
    "waitUntil": [
        "load",
        "domcontentloaded",
        "networkidle2",
    ],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36",
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
        fake_audio=False,
    )
    await asyncio.sleep(1)
    await page.goto(
        url=url,
        options=options,
    )
    await asyncio.sleep(wait_after)

    await page.screenshot(
        options={
            "path": "no-fake-devices.png",
            "fullPage": True,
        }
    )
    await browser.close()

    browser, page = await get_browser_and_page(
        use_proxy=use_proxy,
        headless=headless,
        headers=HEADERS,
        fake_audio=True,
    )
    await asyncio.sleep(1)
    await page.goto(
        url=url,
        options=options,
    )
    await asyncio.sleep(wait_after)
    await page.screenshot(
        options={
            "path": "with-fake-devices.png",
            "fullPage": True,
        }
    )
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main(url=WEBRTC, headless=True, wait_after=2, use_proxy=True))
