#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from termcolor import colored

from os import listdir, mkdir, rename, rmdir
from os.path import basename, dirname, isfile, isdir, join
from shutil import move as mvfiles

parse = argparse.ArgumentParser(description='Create folder from selected files:')
parse.add_argument('-f', '--filelist', nargs='+', metavar='filelist', help='CMD create folder')
parse.add_argument('-d', '--dir', metavar='newdir', help='Name of new dir to create')
parse.add_argument('-m', '--move', metavar='pathtomove', help='Name of new path to move')
args = parse.parse_args()


def pprint(size, *args): # print the 3 message with colors, just informing pprint(4, message, color)

    if type(size) is not int:
        print('first argument is not a int nunber')
        pass

    if len(args) == 1:
        print('Enter at least one message and one color.')
    elif len(args) in [3, 5, 7]:
        print('Please, give a color for last message')
    else:
        if len(args) == 2:
            print(size * ' ', colored(args[0], args[1], attrs=['bold']))
        elif len(args) == 4:
            print(size * ' ', colored(args[0], args[1], attrs=['bold']), colored(args[2], args[3], attrs=['bold']))
        elif len(args) == 6:
            print(size * ' ', colored(args[0], args[1], attrs=['bold']), colored(args[2], args[3], attrs=['bold']), colored(args[4], args[5], attrs=['bold']))


class FilesManager():
    def __init__(self):
        pprint(2, 'CMD folderfromselected', 'yellow')

    def createNewDir(self, newdir, filelist):
        self.current_dir_of_files = dirname(filelist[0])
        self.pathtomovefiles = join(self.current_dir_of_files, newdir)
        self.tmp_dir = None

        truelist = []
        for __file in filelist:
            if isfile(__file) is True or isdir(__file) is True:
                truelist.append(True)
            else:
                truelist.append(False)

        if not True in truelist:
            pprint(4, 'no existent files informed', 'red')
        else:
            if isdir(self.pathtomovefiles) is False and isfile(self.pathtomovefiles) is False: # create new dir if not exist like a dir, or file
                try:
                    mkdir(self.pathtomovefiles)
                    pprint(4, 'The directory was created:', 'white', newdir, 'green')
                except Exception as e:
                    pprint(4, 'Error creating new directory:', 'white', newdir, 'red')
                    raise e
            elif isdir(self.pathtomovefiles) is True: # check if new dir exist
                pprint(4, 'The directory', 'white', newdir, 'green', 'already exists.', 'white')
            elif isfile(self.pathtomovefiles) is True: # check if newdir is a file
                pprint(4, 'The directory', 'white', newdir, 'blue', 'and its a', 'white', 'file.', 'blue')
                tmp_dir = join(self.current_dir_of_files, 'tmp_dir') 

                # create a tmp dir
                if not isdir(tmp_dir):
                    pprint('tmp_dir', 'green' 'not exist')
                    try:
                        mkdir(tmp_dir)
                    except Exception as e:
                        raise e
                else:
                    pprint('tmp_dir', 'green' 'created')
                    pass

                # check content of var tmp_dir
                if len(tmp_dir) > 0: # check if tmp_dir is a valid dir
                    if isdir(tmp_dir) is True: # store tmp_dir in a new var to grand acess to other funcs
                        self.tmp_dir = tmp_dir
                    else:
                        self.tmp_dir = None

    def movefiles(self, _filelist):
        def doMove(__filelist, _dir): # func to move files based in a filelist and dir
            for file in __filelist:
                try:
                    if isfile(file) or isdir(file): # check if file (in filelist) is a valid file or a dir
                        if isdir(_dir): # check if _dir is a valid dir
                            mvfiles(file, _dir) # move files to this informed dir
                            #
                            # checks if the file has been successfully moved
                            if isfile(join(_dir, basename(file))) is True or isdir(join(_dir, basename(file))) is True:
                                pprint(4, basename(file), 'blue', 'successfully moved to', 'white', _dir, 'green')
                            else:
                                pprint(4, basename(file), 'red', 'error when moving', 'white', file, 'red')
                except Exception as e:
                    raise e
        if self.tmp_dir is not None and isdir(self.tmp_dir) is True: # if tmp_dir is a valid directory, move files to it
            pprint(4, 'Creating the temporary directory', 'white', self.tmp_dir, 'red')
            doMove(_filelist, self.tmp_dir)
            try:
                rename(self.tmp_dir, self.pathtomovefiles) # rename tmp_dir to delected dir 
            except Exception as e:
                raise e
        else:
            doMove(_filelist, self.pathtomovefiles) # moves files directly to the informed directory

    def moveToNewPath(self, newpath):
        if isdir(newpath) is True and newpath != self.current_dir_of_files: # check if newpath is a valid path
            if isdir(join(newpath, basename(self.pathtomovefiles))) is False: # check if dir exist in new path 
                for file in listdir(self.pathtomovefiles):
                    if isdir(join(self.pathtomovefiles, file)) is True or isfile(join(self.pathtomovefiles, file)) is True:
                        try:
                            mvfiles(join(self.pathtomovefiles, file), join(newpath, basename(self.pathtomovefiles))) # moves all files to newpath
                        except Exception as e:
                            pprint(4, file, 'red', 'already exists in', 'white', join(newpath, basename(self.pathtomovefiles)), 'blue')

                            # in case of error during the copy the files are returned to the original directory
                            try:
                                mvfiles(join(self.pathtomovefiles, file), self.current_dir_of_files) # move files back to original dir
                            except Exception as e:
                                raise e

                            pprint(4, file, 'red', 'moved back to', 'white', self.current_dir_of_files, 'green')
                            
                        # after copying the files to newdir, delete the source directory
                        if len(listdir(self.pathtomovefiles)) == 0:
                            rmdir(self.pathtomovefiles)
                            if not isdir(self.pathtomovefiles):
                                pprint(4, self.pathtomovefiles, 'blue', 'deleted', 'white')
                            else:
                                pprint(4, self.pathtomovefiles, 'red', 'error', 'yellow', 'when deleting', 'white')
            elif newpath == self.current_dir_of_files:
                pprint(4, 'New path is equal current path', 'red')


if __name__ == '__main__':
    mf = FilesManager()

    if args.dir is not None:
        if len(args.dir) > 0 and len(args.filelist) >= 1:
            mf.createNewDir(args.dir, args.filelist)

    else:
        pprint(4, '-d, --dir', 'red', 'is a required argument', 'white')
        pass

    if args.filelist is not None:
        if len(args.filelist) >= 1:
            mf.movefiles(args.filelist)
    else:
        pprint(4, '-f, --filelist', 'red', 'is a required argument', 'white')
        pass
    
    if args.move is not None and len(args.dir) > 0 and len(args.filelist) >= 1:
        if len(args.move) > 0:
            mf.moveToNewPath(args.move)
            
        

