#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import os
import re
import textwrap

import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newHeight, newWidth))
    newImg = ImageOps.expand(newImage, border=10, fill="yellow")
    return newImg


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(720, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(35))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.8)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 400
        y1 = Ycenter - 400
        x2 = Xcenter + 400
        y2 = Ycenter + 400
        logo = youtube.crop((250, 10 ,1150, 700))
        logo.thumbnail((400, 400), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=10, fill="orange")
        background.paste(logo, (170, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("assets/font2.ttf", 40)
        font2 = ImageFont.truetype("assets/font2.ttf", 70)
        font3 = ImageFont.truetype("assets/font.ttf", 40)
        jokerman = ImageFont.truetype("assets/font2.ttf", 35)
        name_font = ImageFont.truetype("assets/font.ttf", 35)
        para = textwrap.wrap(title, width=25)
        j = 0
        draw.text(
            (10, 10), f"{MUSIC_BOT_NAME}", fill="white", font=font
        )
        draw.text(
            (110, 460),
            "Enjoy the song!",
            fill="black",
            stroke_width=2,
            stroke_fill="white",
            font=font2,
        )        
        for line in para:
            if j == 1:
                j += 1
                draw.text(
                    (50, 650),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font3,
                )
            if j == 0:
                j += 1
                draw.text(
                    (50, 610),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font3,
                )

        draw.text(
            (100, 790),
            f"Views : {views[:23]}",
            (255, 255, 255),
            font=jokerman,
            stroke_width=1,
            stroke_fill="black",
        )
        draw.text(
            (100, 840),
            f"Duration : {duration[:23]} Mins",
            (255, 255, 255),
            font=jokerman,
            stroke_width=1,
            stroke_fill="black",
        )
        draw.text(
            (100, 890),
            f"Channel : {channel}",
            (255, 255, 255),
            font=jokerman,
            stroke_width=1,
            stroke_fill="black",
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception:
        return YOUTUBE_IMG_URL
