import sys
from urllib.parse import parse_qsl
import xbmcgui
import xbmcplugin
###import sys
import requests
###import xbmcgui
###import xbmcplugin

###import xbmc
import xbmcaddon
import xbmcvfs
#import resources.lib.common as common


### addon_handle = int(sys.argv[1])


### xbmcplugin.setContent(addon_handle, 'videos')
#xbmcplugin.setContent(int(sys.argv[1]), 'videos')

#url = 'http://localhost/some_video.mkv'
#li = xbmcgui.ListItem('My First Video!')
#xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])


ADDON_ID = 'plugin.video.lrt.lt'
addon = xbmcaddon.Addon(id=ADDON_ID)

addon_dir = xbmcvfs.translatePath( addon.getAddonInfo('path') )
asset_dir = addon_dir+'/resources/assets/'

xbmcplugin.setContent(__handle__, 'videos')

channels = [{'name': 'LRT TV', 'video_id':'LTV1', 'img_id':'lrt_tv'},
            {'name': 'LRT Plius', 'video_id':'LTV2', 'img_id':'lrt_plius'},
            {'name': 'LRT Lituanica', 'video_id':'WORLD', 'img_id':'lrt_lituanica'},
            {'name': 'LRT Radijas', 'video_id':'LR', 'img_id':'lrt_radijas'},
            {'name': 'LRT Klasika', 'video_id':'Klasika', 'img_id':'lrt_klasika'},
            {'name': 'LRT Opus', 'video_id':'Opus', 'img_id':'lrt_opus'}]

def list_channels():
    for c in channels:
        url = '{0}?action=play&channel={1}'.format(__url__, c['video_id'])
        listitem = xbmcgui.ListItem(label=c['name'])
        listitem.setArt({'icon': asset_dir+'poster-'+c['img_id']+'.png', 'poster': asset_dir+'poster-'+c['img_id']+'.png', 'fanart': asset_dir+'poster-'+c['img_id']+'.png'})
        listitem.setProperty('IsPlayable','true')
        listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": c['name'] })
        xbmcplugin.addDirectoryItem(__handle__, url=url, listitem=listitem)
    xbmcplugin.endOfDirectory(__handle__)

def play_channel(path):
    """
    Play a video by the provided path.
    :param path: str
    :return: None
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)

def router(paramstring):
    # Check the parameters passed to the plugin
    params = dict(parse_qsl(paramstring[1:]))
    if params:
        if params['action'] == 'play':
            # Play a video from a provided URL.
            resp = requests.get("https://www.lrt.lt/servisai/stream_url/live/get_live_url.php?channel="+params['channel'])
            data = resp.json()
            stream_url = data['response']['data']['content']
            play_channel(stream_url)
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_channels()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    router(sys.argv[2])
