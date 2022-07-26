from pathlib import Path
import platform

class GeneratorFormats:
    json = "Json"
    stardict = "Stardict"

class Config:
    # optional
    #stardict_path = "/Users/f/Documents/StarDicts/stardict/hanzi_key.ifo"

    base_path = Path("/Volumes/GoogleDrive-100763791435668895390/My Drive/Dicts")
    stardict_path = base_path.joinpath("/hanzi_star_dict/hanzi_key.ifo")
    csv_path = base_path.joinpath("/ordinary_csv.txt")
    # Put your anki path to collection.media folder
    if platform.system() == "Windows":
        json_path = Path("C:/Users/metta/AppData/Roaming/Anki2/Ye qiu/collection.media/_hzdb.json")
    else:
        json_path = Path("/Users/f/Library/Application Support/Anki2/yeqiu90210/collection.media/_hzdb.json")
    title = "Hanzi To Keyword"
    author = "Ant King"

    format_to_path = {GeneratorFormats.json: json_path, GeneratorFormats.stardict: stardict_path}
    # testing related
    stardict_path_test_path = Path("../out/stardict/hanzi_key.ifo")
    json_path_test_path = Path("../out/json/hanzi.json")