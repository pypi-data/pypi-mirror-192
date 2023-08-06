#!python

import argparse
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import re


def clean_text(text):
    fixed = []
    for line in text.split('\n'):
        line = re.sub('\s+', ' ', line)
        if len(line) < 10:
            continue
        if '©' in line:
            continue
        line = line.encode('ascii',errors='ignore').decode()
        fixed.append(line)
    return "\n".join(fixed)

def convert_pdf_to_txt(in_file, separate_pages = True):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    pages = []
    with open(in_file, 'rb') as file:
        for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
            interpreter.process_page(page)
            if separate_pages:
                text = retstr.getvalue()
                text = clean_text(text)
                pages.append(text)  

    device.close()
    retstr.close()
    return pages

def paper2txt_main():
    parser = argparse.ArgumentParser(description="Converts scientific papers to txt")
    parser.add_argument('infile',  nargs=1, help="Input file")
    parser.add_argument('outfile', nargs=1, help="Output file")
    parser.add_argument('-p', '--pages', action="store_true", help="Make one file per pdf page")
    args = parser.parse_args()

    pages = convert_pdf_to_txt(args.infile[0])

    if args.pages:
        pgn = 1
        for page in pages:
            with open("{}_{}.txt".format(args.outfile[0], pgn), 'w') as out:
                out.write(page)
            pgn +=1
    else:
        with open(args.outfile[0], 'w') as out:
            out.write("\n".join(pages))

