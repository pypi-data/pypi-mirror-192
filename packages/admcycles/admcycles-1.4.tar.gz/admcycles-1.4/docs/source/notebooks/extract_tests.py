#!/usr/bin/env python
# This script extract the doctests from the tex source main.tex and writes
# them in doctest.rst so that they can be parsed by the sage doctester.

import sys
infilename = sys.argv[1]
outfilename = infilename[:-8]+"rst"  # remove "asciidoc" from filename

infile = open(infilename)
outfile = open(outfilename, "w")


outfile.write("admcycles Notebook doctest\n")
outfile.write("=========================\n\n")
outfile.write(".. linkall\n\n")
outfile.write("This file was automatically generated, do not edit.\n\n")
outfile.write("TESTS::\n")

l = infile.readline()

in_lstlistings = False
bad_doctest = False

while l:
    if "[source, ipython3]" in l:
        outfile.write("\n")
        l = infile.readline() # read ----
        l = ''
        while True:
            l = infile.readline() # read next line
            l = l.rstrip()
            if not l:
                continue
            if "----" in l:
                break
            if l[0]==" ":
                outfile.write("    ....: "+l+"\n")
            else:
                outfile.write("    sage: "+l+"\n")            
    if "+*Out" in l:
        l = infile.readline()
        l = l[4:] # strip "----" from left
        if l == "\n":
            l = ""  # avoid weird error with function that returns None but executes print-functions
        while "----" not in l:
            nextline = infile.readline()
            if nextline == "\n":
                nextline = "<BLANKLINE>" + nextline
            l+= "    "+ nextline
        l = "    "+l.rstrip("-\n")
        outfile.write(l)

    l = infile.readline()

outfile.close()
infile.close()