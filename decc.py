#!/usr/bin/env python3
# import the modules
import os
import sys
import argparse
import script.parser
import script.exec
from sys import exit

# program config
version = 1.1

# make argparser
argv = argparse.ArgumentParser(description="\ndecimal script " + str(version))

# add argument
argv.add_argument("-v", "--version", action="store_true", help="print version and exit")
argv.add_argument("-c", help="program execute by argv string")
argv.add_argument("-e", nargs='*', help="compile it into decimal script binary file")
argv.add_argument("-i", help="load from decimal script binary file")
argv.add_argument("-o", help="set the name of the output file", default="a.dsc")
argv.add_argument("arg", nargs='*', help="file | argv")

# build args
args = argv.parse_args()

# define run
if args.version:
    print("decimal script", version)
    exit(0)
elif args.c:
    try:
        compiled = script.parser.compile(args.c)
        if compiled: script.exec.execd(compiled)
    except:
        print("Segmentation ERROR")
        exit(-1)
elif args.e:
    src = ""
    for i in args.e:
        try:
            fp = open(i, 'r')
            src += fp.read()
            fp.close()
        except:
            print("file", i, "not found")
            exit(-1)
    compiled = script.parser.compile(src)
    if compiled:
        fp = open(args.o, 'w')
        fp.write(compiled)
        fp.close()
elif args.i:
    try:
        fp = open(args.i, 'r')
    except:
        print("file", i, "not found")
        exit(-1)
    try:
        script.exec.execd(fp.read(), args.arg)
    except:
        print("Segmentation ERROR")
        fp.close()
        exit(-1)
    fp.close()
else:
    if not args.arg:
        print("decimal script", version)
        print()
        s = ""
        while True:
            try:
                t = input('')
            except:
                exit(0)
            if t == "quit" or t == 'q': break
            if t.split() == []: continue
            if t[-1] == ';': t = t[:-1]
            compiled = script.parser.compile(t + "; write();")
            try:
                if compiled: script.exec.execd(compiled)
                else: os._exit(-1)
            except:
                print("Segmentation ERROR")
                exit(-1)
            print()
        exit(0)
    src = ""
    for i in args.arg:
        try:
            fp = open(i, 'r')
            src += fp.read()
            fp.close()
        except:
            print("file", i, "not found")
            exit(-1)
    compiled = script.parser.compile(src)
    try:
        if compiled: script.exec.execd(compiled, sys.argv)
    except:
        print("Segmentation ERROR")
        exit(-1)
exit(0)