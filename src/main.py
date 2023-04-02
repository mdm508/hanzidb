from not_main import *
import argparse
import shutil






def make_parser():
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
    return parser


def command_line_main():
    parser = make_parser()
    args = parser.parse_args()
    args.func(args)


# print(e)
#
# if __name__ == '__main__':
#     #command_line_main()
#     #update_decompstrV2(10)
#     db = TinyDB('hanzi.json')
#     # with open("../dataSources/hanzi.csv", 'r', encoding='utf-8') as f:
#     #     reader = csv.reader(f)
#     #     for row in reader:
#     #         hanzi = row[0]
#     #         q = Query()
#     #         keyword = row[1]
#     #         db.update({'primitive': None}, q.hanzi == hanzi)
#     for e in db:
#         e.update({'primitive': None})
