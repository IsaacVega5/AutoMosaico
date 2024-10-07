IMG_TYPES = ["RGB", "Termal", "OCN", "RGN"]

IMG_TYPES_FILES = (("All Image Files", "*.jpg;*.png;*.tif"), ("JPG files", "*.jpg"),("PNG files", "*.png"), ("TIFF files", "*.tif"))  # Crea un tuple con las extensiones permitidas

ROI_SET_PATH = "json/roiSets.json"

INV_255 = 1 / 255.0
MIN_H_GA = 60
MAX_H  = 180
MIN_SAT = 1
MIN_H_GGA = 80

ORDER_BY = ["Búsqueda", "ABC asc", "ABC desc", "Creación asc", "Creación desc", "Edición asc", "Edición desc"]

EXPORT_TYPES = ["Individual", "Conjunto"]

RGB_VALUES = ['Intensity', 'Hue', 'Saturation', 'Lightness', '*a', '*b', '*u', '*v', 'GA%', 'GGA%', 'CSI']
ONE_CHANNEL_VALUES = ['Area', 'Mean', 'Min', 'Max']

HUE_MASK_TYPE =  ["Hue del suelo", "Mascara externa"]