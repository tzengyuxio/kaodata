#!/usr/bin/env python3

import csv
import os
from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style
from utils import to_unicode_name


def lempe_combine_persons():
    CSV_TW = 'lempe-persons-tw.csv'
    CSV_EN = 'lempe-persons-en.csv'
    with open(CSV_TW, 'r', encoding='utf-8') as ftw, open(CSV_EN, 'r', encoding='utf-8') as fen:
        csv_tw = csv.reader(ftw)
        csv_en = csv.reader(fen)

        header = next(csv_tw)
        header = header[0:2] + ['Name', '國家'] + header[2:-2]
        next(csv_en)

        persons = []
        for row_tw, row_en in zip(csv_tw, csv_en):
            person = row_tw[0:2] + [row_en[1], row_tw[-1]] + row_tw[2:-2]
            persons.append(person)
        for person in persons:
            person[1] = '[{}](/人物/拿破崙時代/{})'.format(person[1], person[1])

    writer = MarkdownTableWriter(
        table_name='拿破崙 人物資料',
        headers=header,
        value_matrix=persons,
        column_styles=[
            Style(),
            Style(),
            Style(),
            Style(),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
            Style(align='center'),
        ]
    )
    writer.write_table()


def lempe_list_cities_and_nations():
    HOME_DIR = os.path.expanduser('~')
    NPDATA_EN = HOME_DIR + '/DOSBox/empereur/NPDATA.CIM'
    NPDATA_TW = HOME_DIR + '/DOSBox/lempereur/NPDATA.CIM'
    with open(NPDATA_EN, 'rb') as fen, open(NPDATA_TW, 'rb') as ftw:
        cities = []
        nations = []

        # extract nations
        fen.seek(7220)
        ftw.seek(7220)
        for _ in range(15):
            nation_en = to_unicode_name(fen.read(10)[:9])
            nation_tw = to_unicode_name(ftw.read(10)[:8])
            nations.append((nation_en, nation_tw))

        # extract cities
        for _ in range(46):
            city_en = to_unicode_name(fen.read(34)[:15])
            city_tw = to_unicode_name(ftw.read(34)[:14])
            cities.append((city_en, city_tw))

    # print(nations)
    # print(cities)
    # print('nations:', len(nations))
    # print('cities:', len(cities))

    writer = MarkdownTableWriter(
        table_name='拿破崙 國家',
        headers=['ID', '中文', '英文'],
        value_matrix=[(i, nation[1], nation[0]) for i, nation in enumerate(nations)],
    )
    writer.write_table()

    writer = MarkdownTableWriter(
        table_name='拿破崙 城市',
        headers=['ID', '中文', '英文'],
        value_matrix=[(i, city[1], city[0]) for i, city in enumerate(cities)],
    )
    writer.write_table()


if __name__ == '__main__':
    lempe_combine_persons()  # 拿破崙 合併中英文人名
    # lempe_list_cities_and_nations()  # 拿破崙 列出所有城市與國家
