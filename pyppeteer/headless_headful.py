import asyncio

from browser import get_browser_and_page
from urls import (
    HEADLESS_TEST1,
    HEADLESS_TEST2,
    HEADLESS_TEST3,
)

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/70.0.3542.0 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
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
    )
    await asyncio.sleep(1)
    response = await page.goto(
        url=url,
    )
    print("Response status: ", response.status)

    await asyncio.sleep(wait_after)

    scrn_fname = "headless.png" if headless else "headful.png"
    await page.screenshot(
        options={
            "path": scrn_fname,
            "fullPage": False,
        }
    )
    with open("test.html", "w") as f:
        f.write(await page.content())
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main(
        url=HEADLESS_TEST2,
        headless=True,
        wait_after=2,
        use_proxy=False,
    ))
    asyncio.run(main(
        url=HEADLESS_TEST2,
        headless=False,
        wait_after=2,
        use_proxy=False,
    ))
