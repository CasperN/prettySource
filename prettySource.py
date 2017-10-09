"""
Author: Casper Neo
Updated: 2017 October 9

This program uses pandoc to turn a list of source code files to a syntax
highlighted pdf document.

Usage:
  python prettySouce.py [inputFiles] [outputFile.pdf]
"""
import sys
import os

LANGUAGES = {"c": "c", "py": "python", "h": "haskell", "R": "R"}
TMPFILE = "pandocTMP"
PANDOC_HEADER = """---
geometry: margin=1.5cm
output: pdf_document
linestretch: 0.95
---
"""

def readAndFormat(inputFiles):
  """Reads source code and puts in pandoc code env for processing."""
  pandocInput = PANDOC_HEADER
  for fname in inputFiles:
    # Pandoc code environment
    extension = fname.split(".")[1]
    begin = "~" * 10 + "{.%s .numberLines}\n" % LANGUAGES[extension]
    end = "~" * 10 + "\n\n"
    # Put file in said environment
    with open(fname,'r') as f:
      pandocInput += begin + f.read() + end
  return pandocInput


def writeAndOpen(pandocInput, outputFile):
  """Writes `pandocInput` to a tmp file and renders to outputFile."""
  # Write to tmp
  with open(TMPFILE,'w') as f:
    f.write(pandocInput)
  # render tmp file
  os.system(
    "pandoc %s -s --highlight-style pygments -o %s" % (TMPFILE, outputFile))
  os.system("rm pandocTMP")
  os.system("open %s" % outputFile)


if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("Renders a list of source code files to PDF.")
    print("args: [source code files] [outputFile]")
    sys.exit()
  inputFiles = sys.argv[1:-1]
  outputFile = sys.argv[-1]

  pandocInput = readAndFormat(inputFiles)
  writeAndOpen(pandocInput, outputFile)
