class GeneratorFormats:
    json = "Json"
    stardict = "Stardict"

class Config:
    # optional
    #stardict_path = "/Users/f/Documents/StarDicts/stardict/hanzi_key.ifo"

    base_path = "/Volumes/GoogleDrive-100763791435668895390/My Drive/Dicts"
    stardict_path = base_path + "/hanzi_star_dict/hanzi_key.ifo"
    csv_path = base_path + "/ordinary_csv.txt"
    # Put your anki path to collection.media folder
    json_path = "/Users/f/Library/Application Support/Anki2/yeqiu90210/collection.media/_hzdb.json"
    title = "Hanzi To Keyword"
    author = "Ant King"
    #
    format_to_path = {GeneratorFormats.json: json_path, GeneratorFormats.stardict: stardict_path}
    # testing related
    stardict_path_test_path = "../out/stardict/hanzi_key.ifo"
    json_path_test_path = "../out/json/hanzi.json"