#!/usr/bin/env python
# -*- coding: utf-8 -*-
import core_app
import db_app
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filePath', nargs='?')
    parser.add_argument('-p', '--playlistPath', nargs='?', default='example.xspf')
    parser.add_argument('-cmd', '--command', nargs='?', default='addTag')
    parser.add_argument('-n', '--name', nargs='?')
    parser.add_argument('-c', '--category', nargs='?')

    return parser


if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()

    dbApp = db_app.DBApp("/home/diogenoz/PycharmProjects/catalogizator2020/db")
    coreApp = core_app.App(dbApp)

    if args.command == 'addTag' and args.filePath and args.category:
        coreApp.addTagToFile(args.filePath, args.category)
    elif args.command == 'deleteTag':
        coreApp.deleteTag(args.filePath, args.category)
    elif args.command == 'addCategory':
        coreApp.addCategory(args.name)
    elif args.command == 'listCategories':
        categories = coreApp.getCategories()
        if categories:
            print(categories)
    elif args.command == 'exportInVlc':
        coreApp.exportToPlaylist(args.category, args.playlistPath)
    else:
        print("Command don't fund. Read documentation first")

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



    #coreApp.createPlaylist("1.xspf", ["1.avi", "1.avi", "1.avi"])
    coreApp.addTagToFile("1.avi", 2)
    coreApp.exportToPlaylist(2, "1.xspf")
    print(coreApp.getCategories())
    '''
