import pathlib as pl
import zipfile
import os
import datetime
import shutil

# file_list = [d for d in pl.Path(r'W:\NELSON\Downloads\winter_trip_pcis').glob('*.zip')]
# dst = pl.Path(r'D:\PHOTOGRAPHY_RAW\2024_01')

# for j, zipped_file in enumerate(file_list):
#     directory_to_extract_to = dst / f'batch{j:>02}'
#     print(directory_to_extract_to)
#     with zipfile.ZipFile(zipped_file, 'r') as zip_ref:
#         zip_ref.extractall(directory_to_extract_to)

# # do the renaming
# folder_map = {}
# for j, raw_img_file in enumerate(dst.glob('**/*.NEF')):

dst  = pl.Path(r'D:\PHOTOGRAPHY_RAW\2024_01\cali_trip')
for raw_img_file in pl.Path(r'G:\My Drive\pictures_winter_24').glob('**/*.NEF'):
    t = datetime.datetime.fromtimestamp(os.path.getctime(raw_img_file))
    st = t.strftime('%Y_%m_%d_%H%M%S')

    folder = dst / f'{t.strftime('%d')}_cali_visit'
    if not folder.exists():
        folder.mkdir(parents=True)

    new_name = f'cali_visit{st}_{raw_img_file.stem}.NEF'
    new_locn = folder / new_name

    shutil.copy2(raw_img_file, new_locn)
    print(f'copied {raw_img_file} to {new_locn}')


