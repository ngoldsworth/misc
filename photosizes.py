import pathlib as pl
import numpy as np
import matplotlib.pyplot as plt

root = pl.Path(r"Q:\PHOTOGRAPHY_RAW")

total_size = 0
ct = 0
biggest_file_sz = 0
smallest_file_sz = 10**100
biggest_name = ""
smallest_name = ""
sizes = []
for nef in root.glob('**/*.nef'):
    sz = nef.stat().st_size
    total_size += sz
    ct+=1

    sizes.append(sz)

    # if sz < smallest_file_sz:
    #     smallest_file_sz = sz
    #     smallest_name = nef
    # elif sz > biggest_file_sz:
    #     biggest_file_sz = sz
    #     biggest_name = nef


print(total_size, ct)
sizes = np.asarray(sizes)

mem_card_size = 256 * 1000 * 1000 * 1000
average_size = total_size / ct
pictures_to_fill_card = mem_card_size / average_size
print(pictures_to_fill_card)

# print("Smallest file is {}, {} Mbytes".format(smallest_name, smallest_file_sz/1024**2))
# print("Biggest file is {}, {} Mbytes".format(biggest_name, biggest_file_sz/1024**2))

plt.hist(sizes/(1024**2), 200)
plt.show()