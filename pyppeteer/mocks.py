import random

from pyppeteer.page import Page


TIMEZONE_INFO = "https://ipinfo.io/timezone"


async def platform(page: Page, platform: str = ""):
    if platform != "":
        ev = (
            "navigator.__defineGetter__('platform', function(){return 'foo'})"
            .replace("foo", platform)
        )
        await page.evaluateOnNewDocument(ev)


async def navigator_ua(page: Page, ua: str, platform: str):
    override = {
      'userAgent': ua,
      'platform': platform,
      'userAgentMetadata': {
        # 'brands': '',
        # 'fullVersion': '',
        'platform': platform,
        # 'platformVersion': '',
        # 'architecture': '',
        # 'model': '',
        # 'mobile': False,
      }
    }

    await page._client.send('Network.setUserAgentOverride', override)


async def timezone(page: Page, timezone_id: str = ""):
    if not timezone_id:
        await page.goto(TIMEZONE_INFO)
        content = await page.content()
        timezone_id = content.replace("<html><head></head><body>", "").replace("\n</body></html>", "")
    await page._networkManager._client.send(
        "Emulation.setTimezoneOverride", {"timezoneId": timezone_id},
    )


async def history(page: Page, length: int = -1):
    if length == -1:
        length = random.randint(5, 25)
    await page.evaluateOnNewDocument(
        """
        () => {
            if (history.length <= 2) {
        """
        +
        f"for (i = 0; i < {length}; i++)" +
        """{
                    history.pushState({page: i}, "")
                }
            }
        }
        """
    )


async def plugins(page: Page, count: int = 3):
    plugins_array = ','.join(str(i) for i in range(count))
    await page.evaluateOnNewDocument(
        'Object.defineProperty('
        'Object.getPrototypeOf(navigator),'
        '"plugins",'
        '{get() {return [' + plugins_array + ']}})'
    )
