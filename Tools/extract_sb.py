#!/usr/bin/env python
#
# Python program to extract superbank-related info from a yaYUL listing..
# 
# Jim Lawton 2012-10-05
# 
# This little utility is part of an attempt to try and systematically 
# figure out the algorithm for generating Superbank corrections, without 
# resorting to adding extra SBANK= directives.
#
# The input file is the listing generated by yaYUL. The script searches 
# for all instructions relating to superbank processing, i.e.  
# BANK, SETLOC, 2CADR, BBCON, BBCON*, SBANK=, EBANK=, and prints out the 
# matching lines, ignoring comments.

import sys
from optparse import OptionParser

def main():
    parser = OptionParser("usage: %prog listing_file")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("Listing file must be supplied!")
        sys.exit(1)

    lstfile = open(args[0], 'r')
    lines = lstfile.readlines()
   
    outlines = []

    gotStart = False
    
    for line in lines:
        line.strip()
        if '#' in line:
            line = line[:line.index('#')].strip()
        if gotStart and line.startswith("---"):
            print line,
            continue
        if gotStart and line.startswith(">>>"):
            print line,
            continue
        elems = line.split()
        if len(elems) > 0:
            if not line.startswith(' '):
                if elems[0][0].isdigit():
                    gotStart = True
                    if len(elems) > 1:
                        if elems[1].startswith('$'):
                            module = elems[1][1:].split('.')[0]
                        if "# Page" in line and "scans" not in line and "Pages" not in line and "Page:" not in line:
                            pagestr = line[line.index("# Page")+6:][:-1].split()[0]
                            if pagestr[0] == ' ':
                                pagenum = pagestr.strip()
                            else:
                                pagenum = pagestr
                            if pagenum.endswith(','):
                                pagenum = pagenum[:-1]
                            if pagenum.isdigit():
                                pagenum = int(pagenum)
                            else:
                                print >>sys.stderr,"%s: line %d, invalid page number \"%s\"" % (listing, linenum, pagenum)
                    if len(elems) >= 3:
                        if elems[2] == "BANK":
                            print line
                        elif elems[2] == "SETLOC":
                            print line
                    if len(elems) >= 4:
                        if elems[3] == "BBCON" or elems[3] == "BBCON*":
                            print line
                        elif elems[3] == "EBANK=":
                            print line
                        elif elems[3] == "SBANK=":
                            print line
                        elif elems[3] == "2CADR":
                            print line
                    if len(elems) >= 5:
                        if elems[4] == "BBCON" or elems[4] == "BBCON*":
                            print line
                        elif elems[4] == "2CADR":
                            print line

    lstfile.close()

    for line in outlines:
        print line

if __name__ == "__main__":
    main()