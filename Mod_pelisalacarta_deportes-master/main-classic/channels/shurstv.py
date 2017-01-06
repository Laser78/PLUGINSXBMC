# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Shurs.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "shurstv"

DEBUG = config.get_setting("debug")


def login():
    logger.info("pelisalacarta.channels.shurstv login")

    try:
        user = config.get_setting("shurstvuser", __channel__)
        password = config.get_setting("shurstvpassword", __channel__)
        if user == "" or password == "":
            return False, "Regístrate en http://shurs.xyz e introduce tus credenciales", ""
        data = scrapertools.downloadpage("http://shurs.xyz/login")
        if "Mi Perfil" in data: return True, "", data

        token = scrapertools.find_single_match(data, 'value="([^"]+)" name="_token"')
        post = "_token=%s&username=%s&password=%s&remember=1" % (token, user, password)
        data = scrapertools.downloadpage("http://shurs.xyz/login", post=post)
        if '<div class="alert alert-danger alert-notification">' in data:
            logger.info("pelisalacarta.channels.shurstv Error en el login")
            return False, "Error en el usuario y/o contraseña. Comprueba tus credenciales", data
        else:
            logger.info("pelisalacarta.channels.shurstv Login correcto")
            return True, "", data
    except:
        return False, "Error durante el login. Comprueba tus credenciales", data


def mainlist(item):
    logger.info("pelisalacarta.channels.shurstv mainlist")
    itemlist = []
    item.fanart = "http://i.imgur.com/Bt9PHVR.jpg?1"
    
    logueado, message, data = login()
    if not logueado:
        itemlist.append(item.clone(title="[COLOR darkorange]"+message+"[/COLOR]", action="configuracion", folder=False))
        return itemlist

    bloques = scrapertools.find_multiple_matches(data, '<i class="fa\s*fa-bars"></i>\s*([^<]+)<span.*?<ul class="nav nav-second-level collapse">(.*?)</ul>')
    for titulo, bloque in bloques:
        itemlist.append(item.clone(title=titulo.strip(), action="", text_color="blue"))
        matches = scrapertools.find_multiple_matches(bloque, '<a href="([^"]+)".*?>\s*(.*?)<img.*?Boton_([^\.]+).')
        for scrapedurl, scrapedtitle, estado in matches:
            scrapedtitle = "     [COLOR skyblue]"+scrapedtitle.strip()+"[/COLOR]"
            if estado == "Verde":
                scrapedtitle += "  [COLOR green][ON][/COLOR]"
            else:
                scrapedtitle += "  [COLOR red][OFF][/COLOR]"
            itemlist.append(item.clone(title=scrapedtitle, url=scrapedurl, action="play"))

    itemlist.append(item.clone(title="[COLOR darkorange]Canal y web en pruebas. Es normal que fallen varios streamings[/COLOR]"))
    return itemlist


def configuracion(item):
    from platformcode import platformtools
    platformtools.show_channel_settings()
    if config.is_xbmc():
        import xbmc
        xbmc.executebuiltin("Container.Refresh")


def play(item):
    logger.info("pelisalacarta.channels.shurstv play")
    itemlist = []
    data = scrapertools.downloadpage(item.url)

    videourl = scrapertools.find_single_match(data, "(?:source|file)\s*:\s*['\"]([^'\"]+)['\"]")
    itemlist.append(item.clone(url=videourl, server="directo"))

    return itemlist
