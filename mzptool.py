# -*- coding:utf8 -*-
__author__ = 'CGACE'
__qq__ = 394452216

import zipfile
import os

from argparse import ArgumentParser

p = ArgumentParser(usage='Compressed file to mzp', description='This Script for Quick Build 3dsmax Script Zip File.')
p.add_argument('-outpath', help='mzp output filename')
p.add_argument('-filepath', help='source files filename')


class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def add_path(self, path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                self.zfile.write(os.path.join(dirpath, filename), os.path.join(dirpath.split(path)[-1], filename))

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f, 'wb').write(self.zfile.read(filename))


def create_mzp(zfile, path):

    z = ZFile(zfile, 'w')
    z.add_path(path)
    z.close()

if __name__ == "__main__":
    args = p.parse_args()

    print p.format_help()
    if args.outpath and args.filepath:
        create_mzp(args.outpath, args.filepath)