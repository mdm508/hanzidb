from not_main import *
import argparse
import shutil






def main():
    #toplevel parser
    parser = argparse.ArgumentParser(prog='Hanzi DB')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_a = subparsers.add_parser('show', help='look at data for character')
    parser_a.add_argument('hanzi')
    parser_a.set_defaults(func=show_hanzi)
    parser_b = subparsers.add_parser('update', help='update keyword for hanzi')
    parser_b.add_argument('hanzi')
    parser_b.add_argument('keyword')
    parser_b.set_defaults(func=update_hanzi)

    upp = subparsers.add_parser("rebuild")
    upp.set_defaults(func=update_glossary)

    args = parser.parse_args()
    args.func(args)




if __name__ == '__main__':
    # update_glossary()
    main()
    # def decomp_many():
    #     from hanzipy.decomposer import HanziDecomposer
    #     decomposer = HanziDecomposer()
    #     with TinyDB('hanzi.json') as db:
    #         q = Query()
    #         for h in db.all():
    #             dstr = decomposer.decompose(h['hanzi'])
    #             #dstr = decomposer.once_decomposition(h['hanzi'])
    #             #dstr = ','.join(filter(lambda s : s != 'No glyph available', dstr))
    #             #print(dstr)
    #             db.update({Hanzi.Field.decomposition: dstr}, q['hanzi'] == h['hanzi'])
    # update_db(decomp_many)
    # main()
    #with TinyDB('hanzi.json') as db:

        #make_csv_from_db(db)
    # hlist = csv_to_hanzi_list()
    #
    # with open('../dataSources/ChineseCharacterMap.csv', 'r') as f:
    #     r = csv.DictReader(f)
    #     with TinyDB('hanzi.json') as db:
    #         q = Query()
    #         count = 0
    #         for row in r:
    #             order = row['loa']
    #             hz = row['hanzi']
    #             x = db.update({'learn_order': order}, q.hanzi == hz)
    #             count += 1
    #             if count % 500 == 0:
    #                 print(count)