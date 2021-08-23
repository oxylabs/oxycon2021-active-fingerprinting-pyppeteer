import asyncio

import pyppeteer
from pyppeteer.page import Page, Request
from pyppeteer.browser import Browser

from proxy_auth import PROXY_URL, PROXY_USERNAME, PROXY_PASSWORD


async def request_intercept(req: Request):
    req.__setattr__('_allowInterception', True)
    if req.url.startswith('http'):
        print(f"\nreq.url: {req.url}")
        print(f"  req.resourceType: {req.resourceType}")
        print(f"  req.method: {req.method}")
        print(f"  req.postData: {req.postData}")
        print(f"  req.headers: {req.headers}")
        print(f"  req.response: {req.response}")
    return await req.continue_()


async def get_browser_and_page(
        headless: bool = True,
        use_proxy: bool = True,
        fake_audio: bool = True,
        headers: dict = None,
        request_interception: bool = False,
) -> (Browser, Page):
    args = [
        "--start-maximized",
        "--no-sandbox",
        "--disable-web-security",  # CORS checks are now disabled.
        "--disable-gpu",  # Reduces CPU usage when running headful.
    ]
    if fake_audio:
        # Add fake audio input/output devices.
        args.append("-use-fake-device-for-media-stream")
    if use_proxy:
        args.append(f"--proxy-server={PROXY_URL}")
    browser = await pyppeteer.launch(
        args=args,
        options={
            "headless": headless,
            "autoClose": False,
            "waitUntil": [
                "load",
                "domcontentloaded",
                "networkidle2",
            ],
        }
    )

    pages = await browser.pages()
    print("Browser version: ", await browser._getVersion())
    page = pages[0]

    if headers:
        await page.setExtraHTTPHeaders(headers=headers)
    if use_proxy:
        await page.authenticate(
            credentials={
                "username": PROXY_USERNAME,
                "password": PROXY_PASSWORD,
            },
        )
    if request_interception:
        page.on(
            'request',
            lambda req: asyncio.ensure_future(request_intercept(req)),
        )
    return browser, page
