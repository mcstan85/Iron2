import os
import re
import random
import aiohttp
import asyncio
import aiofiles

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL
from MarkMusic import app

from youtubesearchpython.__future__ import VideosSearch
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)


def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 30:        
            text1 += " " + i
        elif len(text2) + len(i) < 30:       
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]


async def gen_thumb(videoid, user_id):
    if os.path.isfile(f"cache/{videoid}_{user_id}.jpg"):
        return f"cache/{videoid}_{user_id}.jpg"
    try:
        url = f"https://www.youtube.com/watch?v={videoid}"
        if 1==1:
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
                async with session.get(f"http://img.youtube.com/vi/{videoid}/maxresdefault.jpg") as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(
                            f"cache/thumb{videoid}.jpg", mode="wb"
                        )
                        await f.write(await resp.read())
                        await f.close()
            wxyz = await app.get_profile_photos(user_id)
            try:
                wxy = await app.download_media(wxyz[0]['file_id'], file_name=f'{user_id}.jpg')
            except:
                hehe = await app.get_profile_photos(app.id)
                wxy = await app.download_media(hehe[0]['file_id'], file_name=f'{app.id}.jpg')
            xy = Image.open(wxy)

            a = Image.new('L', [640, 640], 0)
            b = ImageDraw.Draw(a)
            b.pieslice([(0, 0), (640, 640)], 0, 360, fill = 255, outline = "white")
            c = np.array(xy)
            d = np.array(a)
            e = np.dstack((c, d))
            f = Image.fromarray(e)
            x = f.resize((170, 170))

            youtube = Image.open(f"cache/thumb{videoid}.jpg")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(30))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)
            image2 = background
                                                                                            
            circle = Image.open("assets/circle.png")

            im = circle
            im = im.convert('RGBA')
            color = make_col()

            data = np.array(im)
            white, white, white, alpha = data.T

            white_areas = (white == 255) & (white == 255) & (white == 255)
            data[..., :-1]

            im2 = Image.fromarray(data)
            circle = im2

            image3 = image1.crop((280,0,1000,720))
            lum_img = Image.new('L', [720,720] , 0)
            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
            img_arr = np.array(image3)
            lum_img_arr = np.array(lum_img)
            final_img_arr = np.dstack((img_arr,lum_img_arr))
            image3 = Image.fromarray(final_img_arr)
            image3 = image3.resize((600,600))

            image2.paste(image3, (50,70), mask=image3)
            image2.paste(x, (470, 490), mask=x)
            image2.paste(circle, (0,0), mask=circle)

            # fonts
            font1 = ImageFont.truetype('assets/font.ttf', 30)
            font2 = ImageFont.truetype('assets/font2.ttf', 70)
            font3 = ImageFont.truetype('assets/font2.ttf', 40)
            font4 = ImageFont.truetype('assets/font2.ttf', 35)

            image4 = ImageDraw.Draw(image2)
            image4.text((10, 10), "MARK MUSIC", fill="white", font = font1, align ="left")
            image4.text((670, 150), "MARRK PLAYER", fill="white", font = font2, stroke_width=2, stroke_fill="white", align ="left") 

            # title
            title1 = truncate(title)
            image4.text((670, 300), text=title1[0], fill="white", stroke_width=1, stroke_fill="white",font = font3, align ="left") 
            image4.text((670, 350), text=title1[1], fill="white", stroke_width=1, stroke_fill="white", font = font3, align ="left") 

            # description
            views = f"Views : {views}"
            duration = f"Duration : {duration} Mins"
            channel = f"Channel : {channel}"

            image4.text((670, 450), text=views, fill="white", font = font4, align ="left") 
            image4.text((670, 500), text=duration, fill="white", font = font4, align ="left") 
            image4.text((670, 550), text=channel, fill="white", font = font4, align ="left")
            
            image2 = ImageOps.expand(image2,border=20,fill="white",)
            image2 = image2.convert('RGB')
            try:
                os.remove(f"cache/thumb{videoid}.png")
            except:
                pass
            image2.save(f"cache/{videoid}_{user_id}.jpg")
            file = f"cache/{videoid}_{user_id}.jpg"
            return file
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
