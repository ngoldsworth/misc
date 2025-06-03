import pathlib as pl

json_dictionary = pl.Path(r'C:\Users\nelson.goldsworth\Downloads\raw-wiktextract-data.jsonl')

with open(json_dictionary, 'r',encoding='cp850') as f:
    for line in f.readlines():
        