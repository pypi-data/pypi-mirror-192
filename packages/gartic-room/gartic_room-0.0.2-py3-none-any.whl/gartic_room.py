import asyncio
from ayaka import AyakaCat
try:
    from nonebot_plugin_htmlrender import get_browser
except:
    from ayaka.playwright import get_browser

cat = AyakaCat("你画我猜")
cat.help = "https://gartic.io/create"


@cat.on_cmd(cmds="你画我猜")
async def _():
    browser = await get_browser()
    page = await browser.new_page()

    url = "https://gartic.io/create"

    # 打开页面
    await cat.send(f"正在访问官网 {url}")
    await page.goto(url)
    await page.wait_for_selector("#screens > div > div.actions.mobileActCreate > button")

    # 设置为中文
    await cat.send("设置房间语言为 中文 (简化字)")
    language = page.locator(
        "#screens > div > div.content.bg.createRoom > div.globalSettings > div.alignLang > div:nth-child(1) > label > select")
    await language.select_option("中文 (简化字)")
    await asyncio.sleep(1)

    # 选择类别
    await cat.send("设置房间主题为 综合")
    room_type = page.locator("li.official", has_text="综合")
    await room_type.click()

    # 新建房间
    await cat.send("正在创建房间")
    create = page.get_by_text("创建新房间")
    await create.click()
    await asyncio.sleep(1)

    # 点击skip ad
    ad = page.locator("#aipVideoAdUiSkipButton")
    if await ad.is_visible():
        print("skip ad")
        await ad.click()
        await asyncio.sleep(1)

    await page.click("#popUp > div.content > button")

    # 地址
    await cat.send(page.url)
    await cat.send(f"房间持续60s\n当有其他人加入房间后，我将启动游戏并退出房间，该房间将不再有房主但仍可允许其他人加入并游玩")

    for i in range(60):
        second = page.locator(
            "#users > div > div.scrollElements > div:nth-child(3)", has_text="空位")
        cnt = await second.count()
        if not cnt:
            start = page.locator(
                "#notification > div.buttons > button", has_text="开始")
            await start.click()
            await asyncio.sleep(5)
            await cat.send(f"已移交房间 {page.url}")
            break

        await asyncio.sleep(1)
    else:
        await cat.send("无人加入，已解散房间")

    await page.close()

if __name__ == "__main__":
    from ayaka.adapters.console import run
    run(reload=False)
