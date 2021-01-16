#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import core_app
import db_app
import argparse


def create_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--filePath', nargs='?')
    arg_parser.add_argument('-p', '--playlistPath', nargs='?', default='example.xspf')
    arg_parser.add_argument('-cmd', '--command', nargs='?', default='addTag')
    arg_parser.add_argument('-n', '--name', nargs='?')
    arg_parser.add_argument('-c', '--category', nargs='?')

    return arg_parser


if __name__ == "__main__":
    dir_path = os.path.dirname(sys.argv[0])
    dbApp = db_app.DBApp(dir_path + "/db")
    coreApp = core_app.App(dbApp)

    arg_parser = create_parser()
    args = arg_parser.parse_args()

    if args.command == 'addTag' and args.filePath and args.category:
        coreApp.add_tag_to_file(args.filePath, args.category)
    elif args.command == 'deleteTag':
        coreApp.delete_tag(args.filePath, args.category)
    elif args.command == 'addCategory':
        coreApp.add_category(args.name)
    elif args.command == 'listCategories':
        categories = coreApp.get_categories()
        if categories:
            print(categories)
    elif args.command == 'exportInVlc':
        coreApp.export_to_playlist(args.category, args.playlistPath)
    else:
        print("Command don't found. Read documentation first")

    '''
    print('add category with name BEST')
    dbApp.addCategory("BEST")

    print('add category with name BEST')
    dbApp.disableCategory(1)

    print('add file with /1 size=32000, hash=123123234345dfsadf')
    dbApp.addFile("1", "/1", 32000, "123123234345dfsadf")

    print('must find file')
    dbApp.findSameFile(32000, "123123234345dfsadf")

    print('mustnt find file')
    dbApp.findSameFile(33000, "123123234345dfsadf")

    print('mustnt find file')
    dbApp.findSameFile(32000, "123123234345dfsada")

    print('add tag for file(1) and category(1)')
    dbApp.addTag(1, 2)

    coreApp.add_tag_to_file('/home/diogenoz/PycharmProjects/catalogizator2020/[[DAP][Legal][Germany]]1.mp4', 1)
    coreApp.delete_tag('/home/diogenoz/PycharmProjects/catalogizator2020/[[Best][DAP][Legal][Germany]]1.mp4', 1)
    

    #coreApp.createPlaylist("1.xspf", ["1.avi", "1.avi", "1.avi"])
    coreApp.addTagToFile("1.avi", 2)
    coreApp.exportToPlaylist(2, "1.xspf")
    print(coreApp.getCategories())
    '''
