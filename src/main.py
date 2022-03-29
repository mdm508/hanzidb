from not_main import *

def main():
    Glossary.init()
    with TinyDB('hanzi.json') as db:
        all_of_it = db.all()
        make_json_glossary(all_of_it)
        make_stardict_glossary(all_of_it)


if __name__ == '__main__':
    main()

