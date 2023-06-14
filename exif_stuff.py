import pathlib as pl

import PIL.ExifTags
import PIL.Image

img_fn = pl.Path(r'D:\NELSON\Desktop\untitled20230319_0129.dng')
desktop = pl.Path(r'D:\NELSON\Desktop')
folder = pl.Path(r'Q:\PHOTOGRAPHY_RAW\2023_03\25')
folder = pl.Path(r'D:\NELSON\Desktop\test_print')

# nefs = list(folder.glob('*.dng'))
nefs = list(folder.glob('*.tif'))

img = PIL.Image.open(desktop / '3colts.jpg')
exif_data = img.getexif()
print(exif_data)

exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img.getexif().items()
    if k in PIL.ExifTags.TAGS
}
print(exif)