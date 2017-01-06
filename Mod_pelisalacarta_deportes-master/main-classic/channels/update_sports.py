# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal actualizador para canales deportivos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os, time, urllib2

from core import config
from core import jsontools
from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "update_sports"
REMOTE_VERSION_FILE = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/actualizador/update_sports.xml"
LOCAL_XML_FILE = os.path.join(config.get_runtime_path() , 'channels', "update_sports.xml" )


def mainlist(item):
    logger.info("pelisalacarta.channels.update_sports mainlist")

    itemlist = []
    if config.get_setting("primeruso", "update_sports"):
        configuracion(item)
        config.set_setting("primeruso", False, "update_sports")

    actualizar, version1, version2, fecha, message = check()

    folder_update = config.get_setting("folder_update", "update_sports")
    if not folder_update:
        actualiza(item)
        config.set_setting("folder_update", True, "update_sports")

    if actualizar:
        title = "[COLOR darkorange]Nueva actualización: v"+version2+" a v"+version1+"  ("+fecha+")[/COLOR]"
        itemlist.append(Item(channel=CHANNELNAME, title=title, action="", thumbnail="http://i.imgur.com/pl3ENtX.png", fanart="http://i.imgur.com/RHRbg7M.jpg?1"))
        title = "[COLOR green]Cambios: "+message+"[/COLOR]"
        itemlist.append(Item(channel=CHANNELNAME, title=title, action="", thumbnail="http://i.imgur.com/pl3ENtX.png", fanart="http://i.imgur.com/RHRbg7M.jpg?1"))
    else:
        itemlist.append(Item(channel=CHANNELNAME, title="[COLOR darkorange]Ninguna actualización disponible. Versión actual: v%s[/COLOR]" % version2, action="do_nothing", thumbnail=item.thumbnail, fanart="http://i.imgur.com/RHRbg7M.jpg?1", folder=False))

    itemlist.append( Item(channel=CHANNELNAME, title="Actualizar todo", action="actualiza", thumbnail="http://i.imgur.com/04c7GtV.png", fanart="http://i.imgur.com/RHRbg7M.jpg?1", folder=False) )
    itemlist.append( Item(channel=CHANNELNAME, title="Configurar Actualizador", action="configuracion", thumbnail="http://i.imgur.com/04c7GtV.png", fanart="http://i.imgur.com/RHRbg7M.jpg?1", folder=False) )

    return itemlist


def configuracion(item):
    from platformcode import platformtools
    platformtools.show_channel_settings()


def actualiza(item):
    logger.info("pelisalacarta.channels.update_sports actualiza")

    error = False
    url = "https://api.github.com/repos/CmosGit/Mod_pelisalacarta_deportes/git/trees/master?recursive=1"
    data = scrapertools.cachePage(url)
    data = jsontools.load_json(data)
    count = 0
    progreso = dialog_progress("Progreso de la actualización", "Descargando...")
    for child in data["tree"]:
        if not child["path"].startswith("main-classic"): continue
        if child["type"] == "blob":
            url = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/" + child["path"]
            # Progreso
            count += 1
            percent = (count * 100) / len(data["tree"]) 
            progreso.update(percent, "[B][COLOR red]Actualizado al %d%%[/COLOR][/B]" % int(percent), "Descargando archivo %s" % url.rsplit("/",1)[1])

            git_file = child["path"].replace("main-classic/","")
            filename = os.path.join(config.get_runtime_path(), git_file)
            error_download = do_download(url, filename)
            if error_download: error = True

    url = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/actualizador/update_sports.xml"
    error = do_download(url, LOCAL_XML_FILE)
    count += 1
    progreso.close()

    from platformcode import platformtools
    if error:
        platformtools.dialog_ok("Error", "Se ha producido un error en la actualización de los archivos")
    else:
        platformtools.dialog_ok("Actualizado correctamente", str(count)+" archivos actualizados", item.extra)
    
    import xbmc
    xbmc.executebuiltin("Container.Refresh")
        

def do_download(url, localfilename):
    # Corregimos el filename para que se adapte al sistema en el que se ejecuta
    localfilename = os.path.normpath(localfilename)
    logger.info("pelisalacarta.channels.update_sports localfilename=%s" % localfilename)
    logger.info("pelisalacarta.channels.update_sports url=%s" % url)
    logger.info("pelisalacarta.channels.update_sports descarga fichero...")
    inicio = time.clock()
    
    error = False
    try:
        folder = os.path.dirname(localfilename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if os.path.exists(localfilename.rsplit(".",1)[0] + ".pyo"):
            os.remove(localfilename.rsplit(".",1)[0] + ".pyo")
        data = urllib2.urlopen(url).read()
        outfile = open(localfilename ,"wb")
        outfile.write(data)
        outfile.close()
        logger.info("pelisalacarta.channels.update_sports Grabado a " + localfilename)
         
    except:
        logger.info("pelisalacarta.channels.update_sports Error al grabar " + localfilename)
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        error = True
    
    fin = time.clock()
    logger.info("pelisalacarta.channels.update_sports Descargado en %d segundos " % (fin-inicio+1))
    return error


def check():
    logger.info("pelisalacarta.channels.update_sports Comprobando versión de update_sports.xml")
    try:
        data = scrapertools.downloadpage(REMOTE_VERSION_FILE)
        version_publicada = scrapertools.find_single_match(data,"<version>([^<]+)</version>").strip()
        message = scrapertools.find_single_match(data,"<changes>([^<]+)</changes>").strip()
        fecha = scrapertools.find_single_match(data,"<date>([^<]+)</date>").strip()
        logger.info("pelisalacarta.channels.update_sports Versión en el repositorio: %s" % version_publicada)

        # Lee el fichero con la versión instalada
        fichero = open(LOCAL_XML_FILE, "r")
        data = fichero.read()
        fichero.close()
        version_local = scrapertools.find_single_match(data,"<version>([^<]+)</version>").strip()

        logger.info("pelisalacarta.channels.update_sports Versión local: %s" % version_local)
        if float(version_publicada) > float(version_local):
            logger.info("pelisalacarta.channels.update_sports Nueva versión encontrada")
            return True, version_publicada, version_local, fecha, message
        else:
            logger.info("pelisalacarta.channels.update_sports No existe versión actualizada")
            return False, "", version_local, "", ""
    except:
        import traceback
        logger.error("pelisalacarta.platformcode.launcher "+traceback.format_exc())


def dialog_progress(heading, line1, line2="", line3=""):
    import xbmcgui
    dialog = xbmcgui.DialogProgress()
    dialog.create(heading, line1, line2, line3)
    return dialog
