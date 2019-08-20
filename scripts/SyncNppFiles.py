import urllib3
import shutil

URL_ROOT = 'https://raw.githubusercontent.com/notepad-plus-plus/notepad-plus-plus/master/'
PATH_ROOT = '../{{cookiecutter.plugin_slug}}/src/Npp/'

def download(url, path):
    http = urllib3.PoolManager()
    with http.request('GET', URL_ROOT + url, preload_content=False) as r, open(PATH_ROOT + path, 'wb') as out_file:
        shutil.copyfileobj(r, out_file)

download('PowerEditor/src/menuCmdID.h', 'menuCmdID.h')
download('PowerEditor/src/MISC/PluginsManager/Notepad_plus_msgs.h', 'Notepad_plus_msgs.h')
download('PowerEditor/src/MISC/PluginsManager/PluginInterface.h', 'PluginInterface.h')
download('scintilla/include/Sci_Position.h', 'Sci_Position.h')
download('scintilla/include/SciLexer.h', 'SciLexer.h')
download('scintilla/include/Scintilla.h', 'Scintilla.h')
