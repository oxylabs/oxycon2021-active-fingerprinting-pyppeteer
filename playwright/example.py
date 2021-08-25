import asyncio
from playwright.async_api import async_playwright

from proxy_auth import PROXY_URL, PROXY_USERNAME, PROXY_PASSWORD
from urls import (
    WEBRTC,
    IP_CHECK,
    FINGERPRINT_STUNDZIALT,
    TIMEZONE_INFO,
)

# Run `python -m playwright install` before running script.

webRTCargs = [
    "-use-fake-device-for-media-stream",  # add fake speakers, mic
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
}
wait_until = [
        "load",
        "domcontentloaded",
        "networkidle2",
    ]


async def plugins(page, count: int = 3):
    plugins_array = ','.join(str(i) for i in range(count))
    await page.add_init_script(
        'Object.defineProperty('
        'Object.getPrototypeOf(navigator),'
        '"plugins",'
        '{get() {return [' + plugins_array + ']}})'
    )


async def mocks(
        browser,
        timezone_id: str = None,
        locale: str = None,
):
    if not timezone_id:
        page = await browser.new_page()
        await page.goto(TIMEZONE_INFO)
        content = await page.content()
        timezone_id = content.replace("<html><head></head><body>", "").replace(
            "\n</body></html>",
            "",
        )
    if not locale:
        locale = 'lt-LT'
    context = await browser.new_context(
        locale=locale,
        timezone_id=timezone_id,
        user_agent=USER_AGENT,
    )
    return context


async def get_chromium_browser_and_page(
        playwright,
        use_proxy: bool = True,
):
    args = [
        "--start-maximized",
        "--no-sandbox",
        "--disable-setuid-sandbox",  # TODO: Chrome reports unknown flag.
        "--disable-web-security",  # CORS checks are now disabled.
        "--disable-gpu",  # Reduces CPU usage when running headful.
    ]
    args += webRTCargs
    if use_proxy:
        browser = await playwright.chromium.launch(
            headless=True,
            args=args,
            devtools=False,
            proxy={
                'server': PROXY_URL,
                'username': PROXY_USERNAME,
                'password': PROXY_PASSWORD,
            },
        )
    else:
        browser = await playwright.chromium.launch(
            headless=True,
            args=args,
            devtools=False,
        )

    context = await mocks(browser)
    page = await context.new_page()

    # Mocking:
    await plugins(page, 5)

    await page.set_extra_http_headers(headers=HEADERS)

    return browser, page


async def main():
    async with async_playwright() as p:
        browser, page = await get_chromium_browser_and_page(p, use_proxy=False)
        await asyncio.sleep(1)
        response = await page.goto(
            url=FINGERPRINT_STUNDZIALT,
            wait_until='networkidle',
        )
        await asyncio.sleep(2)
        await page.screenshot(path="test_playwright.png")
        print("Response status: ", response.status)

if __name__ == '__main__':
    asyncio.run(main())
