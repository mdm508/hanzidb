from tinydb import TinyDB, Query
from collections.abc import Mapping
import argparse
import csv
from pyglossary.glossary import Glossary
from dominate.tags import *

model = {'hanzi': None, 'keyword': None,
         'zhuyin': None, 'pinyin': 'rén',
         'decomposition': '人',
         'definition': None,
         'example': None, 'example_zhuyin': None,
         'example_pinyin': None,
         'simplified': '人',
         'rth_index': None,
         'frequency_index': None, 'learn_order': None, 'network_level': None
         }


def reset_db():
    new_hanzi = csv_with_header_to_hanzi_list('../dataSources/ChineseCharacterMap.csv')
    old_hanzi = csv_to_hanzi_list()
    for newh in new_hanzi:
        if newh in old_hanzi:
            merged = newh.__dict__ | old_hanzi[newh].__dict__
            old_hanzi[newh].__dict__ = merged
        else:
            old_hanzi.__setitem__(newh, newh.hanzi)

    for h in old_hanzi.values():
        h.__dict__ = model | h.__dict__
    # with open('../out/hanzidb.csv', 'w') as f:
    #     writer = csv.DictWriter(f, fieldnames=Hanzi.Field.all)
    #     writer.writeheader()
    #     for h in old_hanzi.values():
    #         writer.writerow(h.__dict__)

    assert all([model.keys() == h.__dict__.keys() for h in old_hanzi])
    with TinyDB('hanzi.json') as db:
        db.truncate()
        for k, v in old_hanzi.items():
            db.insert(v.__dict__)


# SECTION: GENERATOR RELATED
class GeneratorFormats:
    json = "Json"
    stardict = "Stardict"


class Config:
    stardict_path_test_path = "../out/stardict/hanzi_key.ifo"
    json_path_test_path = "../out/json/hanzi.json"
    stardict_path = "/Users/f/Documents/StarDicts/stardict/hanzi_key.ifo"
    json_path = "/Users/f/Library/Application Support/Anki2/yeqiu90210/collection.media/hanzi.json"
    title = "Hanzi To Keyword"
    author = "Ant King"
    format_to_path = {GeneratorFormats.json: json_path, GeneratorFormats.stardict: stardict_path}
    pickle_path = "../pickledData/data.pickle"


def make_glossary_obj():
    glos = Glossary()
    glos.setInfo("title", Config.title)
    glos.setInfo("author", Config.author)
    return glos


def make_glossary(db, head_words, write_format, text_format, def_str_maker):
    """
    note that text_format is m for text and h for html
    def_str_maker is funct that can produce definition strings from db enteries
    head_words: A list of attributes in the Hanzi object. These define what you will be able to search for
    write_format: What format to write to
    """
    glos = make_glossary_obj()
    for entry in db:
        #print([entry[hw] for hw in head_words if entry[hw]])
        glos.addEntryObj(glos.newEntry(word=[entry[hw] for hw in head_words if entry[hw]],
                                       defi=def_str_maker(entry),
                                       defiFormat=text_format))
    glos.write(Config.format_to_path[write_format], write_format)

def json_def_str(e):
    d = div(id='hzinfo')
    with d:
        for k,v in e.items():
            if v:
                entry = div(id=k)
                with entry:
                    entry += v
    return d.render()

def make_json_glossary(db):
    make_glossary(db, ['hanzi'], GeneratorFormats.json, 'h', json_def_str)

def star_def_str(e):
    me = e.copy()
    for k,v in me.items():
        me[k] = v or ""
    return '\n'.join( [me['keyword'],
                      "{} {}".format(me['zhuyin'], me['pinyin']),
                      me['definition'],
                      me['decomposition'],
                      "RTH {} , FREQ {}, NL {}".format(me['rth_index'],
                                                       me['frequency_index'],
                                                       me['network_level']),
                      me['example'],
                      me['example_zhuyin'],
                      me['example_pinyin']])

def make_stardict_glossary(db):
    make_glossary(db, ['hanzi', 'keyword', 'zhuyin', 'pinyin', 'rth_index'], GeneratorFormats.stardict, 'm', star_def_str)
    #make_glossary(db, ['hanzi', 'keyword', 'zhuyin', 'pinyin', 'rth_index'], GeneratorFormats.stardict, 'h', json_def_str)

# SECTION: Command interface

def make_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hanzi', help="the character", required=True)
    parser.add_argument('--keyword', help="the keyword to associate with the argument", required=True)
    parser.add_argument('--zhuyin', required=False)
    parser.add_argument('--pinyin', required=False)
    parser.add_argument('--decomp', required=False)
    parser.add_argument('--def', help="the definition", required=False)
    parser.add_argument('--ex', help="example in chinese", required=False)
    parser.add_argument('--ez', help="bopomofo for example", required=False)
    parser.add_argument('--ep', help="pinyin for example", required=False)
    parser.add_argument('--simp', help="simplified of hanzi", required=False)
    parser.add_argument('--rth', help="Heisig index", required=False)
    parser.add_argument('--freq', help="frequency number", required=False)
    return parser


# SECTION: LEGACY
def csv_to_hanzi_list():
    """
    Builds initial dataSources set.
    :return: list of Hanzi Objects
    """
    hl = []
    with open('../dataSources/hanzi.csv', "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            hl.append(Hanzi(row))
        return HanziList(hl)


def csv_with_header_to_hanzi_list(filename):
    """
    """
    hl = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hl.append(Hanzi(row))
    return hl


class Hanzi:
    class Field():
        hanzi = "hanzi"
        keyword = "keyword"
        zhuyin = "zhuyin"
        pinyin = "pinyin"
        decomposition = "decomposition"
        definition = "definition"
        example = "example"
        example_zhuyin = "example_zhuyin"
        example_pinyin = "example_pinyin"
        simplified = "simplified"
        rth_index = "rth_index"
        frequency_index = "frequency_index"
        learn_order = "learn_order"
        network_level = "network_level"
        all = [hanzi, keyword, zhuyin, pinyin, decomposition, definition, example, example_zhuyin, example_pinyin,
               simplified, rth_index, frequency_index, learn_order, network_level]

    def __init__(self, data):
        if type(data) == list:
            self.hanzi = data[0]
            self.keyword = data[1]
            self.zhuyin = data[2]
            self.pinyin = data[3]
            self.decomposition = data[4]
            self.definition = data[5]
            self.example = data[6]
            self.example_zhuyin = data[7]
            self.example_pinyin = data[8]
            self.simplified = data[9]
            self.rth_index = data[10]
            self.frequency_index = data[11]
        else:
            keep_field = set(Hanzi.Field.all)
            my_keys = set(data.keys())
            # init Hanzi for all keys that data has in common with the Hanzi Object.
            # ignores keys in data but not in Hanzi.Field.all
            for k in Hanzi.Field.all:
                if k in my_keys:
                    self.__setattr__(k, data[k])
                else:
                    self.__setattr__(k, None)

    def __str__(self):
        return self.hanzi + '\n' + self.definition_str()

    def definition_str(self):
        net = ""
        return '\n'.join([self.keyword or "",
                          "{} {}".format(self.zhuyin or "", self.pinyin or ""),
                          self.definition or "",
                          self.decomposition or "",
                          "RTH {} , FREQ {}, NL {}".format(self.rth_index or "",
                                                           self.frequency_index or "",
                                                           net),
                          self.example or "",
                          self.example_zhuyin or "",
                          self.example_pinyin or ""
                          ])


class HanziList(Mapping):
    # Inherited Mapping methods and pop, popitem, clear, update, and setdefault
    def __init__(self, list_of_hanzi: [Hanzi] = []):
        self.map = dict()
        for h in list_of_hanzi:
            self.map[h.hanzi] = h

    def __contains__(self, hanzi: Hanzi):
        return hanzi.hanzi in self.map

    def __getitem__(self, item):
        if type(item) == Hanzi:
            return self.map[item.hanzi]
        if type(item) == 'str':
            return self.map[item]

    def __setitem__(self, h: Hanzi, value: str):
        self.map[value] = h

    def __delitem__(self, key):
        self.map.pop(key, None)

    def __iter__(self):
        return iter(self.map.values())

    def __len__(self):
        return len(self.map)
