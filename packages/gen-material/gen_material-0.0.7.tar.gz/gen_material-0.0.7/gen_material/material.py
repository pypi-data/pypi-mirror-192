from PIL import Image, ImageFont, ImageDraw
import aiohttp, asyncio, requests
from . import openfiles
from .data import charterDB as CDB
from .data import monsterDB as MDB
from .data import bossDB as BDB
from io import BytesIO

async def dowloadImg(link = ""):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                return await response.read()
    except:
        raise

async def info(idC,mobs = False):
    if not mobs:
        r = requests.get(f"https://api.ambr.top/v2/en/avatar/{idC}?vh=35F5")
    else:
        r = requests.get(f"https://api.ambr.top/v2/EN/material/{idC}?vh=35F5")

    return r.json()

async def imgD(link = ""):
    imgs = await dowloadImg(link = link)
    imgs = Image.open(BytesIO(imgs))
    return imgs.convert("RGBA")


def openBg(element):
    if element == "Ice":
        return openfiles.Cryo.copy(), openfiles.CRYO_FRAME, (0,211,212,255)#
    
    elif element == "Grass":
        return openfiles.DendroBg.copy(), openfiles.DENDRO_FRAME, (0,212,0,255)#
    
    elif element == "Wind":
        return openfiles.AnemoBg.copy(), openfiles.ANEMO_FRAME, (0,212,124,255)#
    
    elif element == "Electric":
        return openfiles.ElectroBg.copy(), openfiles.ELECTRO_FRAME, (176,49,220,255)#
    
    elif element == "Water":
        return openfiles.GydroBg.copy(), openfiles.GYDRO_FRAME, (0,99,218,255)#
    
    elif element == "Fire":
        return openfiles.PyroBg.copy(), openfiles.PYRO_FRAME, (243,52,54,255)#
    
    else:
        return openfiles.GeoBg.copy(), openfiles.GEO_FRAME, (245,170,0,255)#



async def icon_mobs(idM, indx = 0):
    infM = await info(idM,mobs = True)
    nameMobs = ""
    ni = 0
    bgs = openfiles.BG_MOB.copy()
    for key in infM["data"]["source"]:
        if indx == 0:
            if "Dropped" in key["name"].split():
                if ni == 2:
                    break
                nameMob = key["name"].split("+ ")[1]
                if nameMob in MDB.itemsName:
                    nameMob = nameMob
                else:
                    if nameMob[:-1] in MDB.itemsName:
                        nameMob = nameMob[:-1]
                    else:
                        nameMob = nameMob[:-2]
                if nameMob in MDB.itemsName:
                    icons = await imgD(MDB.itemsName[nameMob]["icon"])
                    if nameMobs == "":
                        bgs.alpha_composite(icons.convert("RGBA").resize((127,130)),(-58,0))#openfiles.MASKA_FARM_BOSS
                        nameMobs += nameMob
                        ni+= 1
                    else:
                        bgs.alpha_composite(icons.convert("RGBA").resize((127,130)),(57,0))#,openfiles.MASKA_FARM_BOSS
                        nameMobs += f"\n+\n {nameMob}"
                        ni+= 1
                elif nameMob[:-1] in MDB.itemsName:
                    icons = await imgD(MDB.itemsName[nameMob[:-1]]["icon"])
                    if nameMobs == "":
                        bgs.alpha_composite(icons.convert("RGBA").resize((127,130)),(-58,0))#openfiles.MASKA_FARM_BOSS
                        nameMobs += nameMob
                        ni+= 1
                    else:
                        bgs.alpha_composite(icons.convert("RGBA").resize((127,130)),(57,0))#,openfiles.MASKA_FARM_BOSS
                        nameMobs += f"\n+\n {nameMob}"
                        ni+= 1

        elif indx == 12:
            for key in BDB.items:
                if int(idM) in BDB.items[key]["meterial"]:
                    icons = await imgD(BDB.items[key]["url"])
                    icons = icons.resize((93,92))
                    return icons.convert("RGBA")
                
            if nameMob[len(nameMob)-2:] == "es" or nameMob[len(nameMob)-1:] == "s":
                nameMob = nameMob[:-1]
            if nameMob in MDB.itemsName:
                icons = await imgD(MDB.itemsName[nameMob]["icon"])
                icons = icons.resize((93,92))

                return icons.convert("RGBA")

        else:
            nameMob = infM["data"]["source"][0]["name"].split("+ ")[1].split(" Challenge ")[0]
            if nameMob in MDB.itemsName:
                nameMob = nameMob
            else:
                if nameMob[:-1] in MDB.itemsName:
                    nameMob = nameMob[:-1]
                else:
                    nameMob = nameMob[:-2]
            if nameMob in MDB.itemsName:
                icons = await imgD(MDB.itemsName[nameMob]["icon"])
                bgs.alpha_composite(icons.convert("RGBA").resize((127,130)),(0,0))#openfiles.MASKA_FARM_BOSS
                nameMobs += " ".join(nameMob.split(" ")[:2])
            else:
                for key in MDB.itemsName.keys():
                    if nameMob in key:
                        icons = await imgD(MDB.itemsName[key]["icon"])
                        bgs.alpha_composite(icons.convert("RGBA").resize((127,130)),(0,0))#openfiles.MASKA_FARM_BOSS
                        print(nameMob.split(" ")[:2])
                        nameMobs += " ".join(nameMob.split(" ")[:2])

    return {"img": bgs, "name": nameMobs}

async def creat(idC, element = None):
    t21 = ImageFont.truetype(openfiles.font, 19)
    t134 = ImageFont.truetype(openfiles.font, 134)
    t90 = ImageFont.truetype(openfiles.font, 90)
    banner = ""
    if element != None:
        banner = await imgD(CDB.dataItems[element][idC]["splash"]).resize((1692,838))
        banner = banner.resize((1692,838))
    else:
        for key in CDB.dataItems:
            if idC in CDB.dataItems[key]:
                element = key
                banner = await imgD(CDB.dataItems[key][idC]["splash"])
                banner = banner.resize((1692,838))
                break
    inf = await info(idC)
    cname = inf["data"]["name"]

    bg,frames, colords = openBg(element)
    bg = bg.convert("RGBA")
    if banner == "":
        cname = cname.replace(" ", "_")
        if cname == "Alhaitham":
            cname = "Alhatham"
        banner = await imgD(f'https://enka.network/ui/UI_Gacha_AvatarImg_{cname}.png')
        banner = banner.resize((1692,838))

    d = ImageDraw.Draw(bg)
    d.text((0,171),cname,font= t134, fill=colords)
    d.text((59,362),cname,font= t90, fill=(255,255,255,255))
    d.text((-215,515),cname,font= t134, fill=colords)

    bg.alpha_composite(banner,(-27,0))
    i = 0
    inx = 0
    for key in inf["data"]["ascension"]:
        if inx in [0,5,6,7,8,9,10,11,12,13]:
            if int(key) in [202,104319]:
                continue
            icons = await imgD(f'https://api.ambr.top/assets/UI/UI_ItemIcon_{key}.png')
            icons.thumbnail((73,74))
            if i < 4:
                if inf["data"]["ascension"][key] == 1:
                    bg.alpha_composite(icons,(1629,113))
                elif inf["data"]["ascension"][key] == 2:
                    bg.alpha_composite(icons,(1568,552))
                elif inf["data"]["ascension"][key] == 3:
                    bg.alpha_composite(icons,(1676,552))
                elif inf["data"]["ascension"][key] == 4:
                    bg.alpha_composite(icons,(1777,552))
                i += 1
            else:
                if inf["data"]["ascension"][key] == 1:
                    bg.alpha_composite(icons,(1583,247))
                    bg.alpha_composite(icons,(1557,667))
                elif inf["data"]["ascension"][key] == 2:
                    bg.alpha_composite(icons,(1700,247))
                    bg.alpha_composite(icons,(1674,667))
                elif inf["data"]["ascension"][key] == 3:
                    bg.alpha_composite(icons,(1806,247))
                    bg.alpha_composite(icons,(1780,667))
                elif inf["data"]["ascension"][key] == 4:
                    bg.alpha_composite(icons,(1435,424))
                    iconM = await icon_mobs(key,13)
                    bg.alpha_composite(iconM["img"],(1423,252))
                    bg.alpha_composite(frames,(1423,252))
                    d.multiline_text((1390,390), iconM["name"], align ="center", font= t21, fill=(255,255,255,255))
                elif inf["data"]["ascension"][key] == 5:
                    bg.alpha_composite(icons,(1418,666))
                    iconM = await icon_mobs(key,12)
                    bg.paste(iconM,(1406,581),openfiles.FRAME_DAY_BOSS.convert("L"))
        else:
            if inx == 2:
                if inf["data"]["ascension"][key] == 3:
                    iconM = await icon_mobs(key)
                    bg.alpha_composite(iconM["img"],(1910,252))
                    bg.alpha_composite(frames,(1910,252))
                    d.multiline_text((1882,390), iconM["name"],align ="center", font= t21, fill=(255,255,255,255))
        inx += 1
        bg.alpha_composite(openfiles.logo,(68,664))
    return bg

