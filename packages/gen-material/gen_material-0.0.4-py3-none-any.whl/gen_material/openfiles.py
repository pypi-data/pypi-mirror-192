from PIL import Image
import threading
from weakref import WeakValueDictionary
from pathlib import Path

lock = threading.Lock()
cache = WeakValueDictionary()
assets = Path(__file__).parent / 'assets'


font = str(assets / 'font' / 'Genshin_Impact.ttf')



mapping = {
    'logo': assets/'bg'/'LK_LOGO_X.png',
    'AnemoBg': assets/'bg'/'ANEMO.png',
    'Cryo': assets/'bg'/'CRYO.png',
    'DendroBg': assets/'bg'/'DENDRO.png',
    'ElectroBg': assets/'bg'/'ELECTRO.png',
    'GeoBg': assets/'bg'/'GEO.png',
    'GydroBg': assets/'bg'/'GYDRO.png',
    'PyroBg': assets/'bg'/'PYRO.png',

    
    'BG_MOB': assets/'bg'/'BG_MOB.png',
    'MASKA_FARM_BOSS': assets/'bg'/'MASKA_FARM_BOSS.png',


    'PYRO_FRAME': assets/'frame'/'PYRO.png',
    'ANEMO_FRAME': assets/'frame'/'ANEMO.png',
    'CRYO_FRAME': assets/'frame'/'CRYO.png',
    'DENDRO_FRAME': assets/'frame'/'DENDRO.png',
    'ELECTRO_FRAME': assets/'frame'/'ELECTRO.png',
    'GEO_FRAME': assets/'frame'/'GEO.png',
    'GYDRO_FRAME': assets/'frame'/'GYDRO.png',

    'FRAME_DAY_BOSS': assets/'frame'/'FRAME_DAY_BOSS.png',
}





def __dir__():
    return sorted(set([*globals(), *mapping]))

def __getattr__(name):
    try:
        path = mapping[name]
    except KeyError:
        raise AttributeError(name) from None
    
    with lock:
        try:
            image = cache[name]
        except KeyError:
            cache[name] = image = Image.open(path)
        
        return image