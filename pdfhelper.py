import os
import argparse
from random import randint
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject
from PyPDF2.generic import NameObject
from datetime import date
import replacements

def replace_text(content, replacements = dict()):
    lines = content.splitlines()

    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"

    return result


def process_data(object, replacements):
    data = object.getData()
    decoded_data = data.decode('ascii', 'ignore')

    replaced_data = replace_text(decoded_data, replacements)

    encoded_data = replaced_data.encode('ascii', 'ignore')
    if object.decodedSelf is not None:
        object.decodedSelf.setData(encoded_data)
    else:
        object.setData(encoded_data)


def go(in_file: str):
    print('GONE')
    filename_base = in_file.replace(os.path.splitext(in_file)[1], "")

    # Provide replacements list that you need here
    replacements = replacements.getReplacementsV()

    pdf = PdfFileReader(in_file)
    writer = PdfFileWriter()

    for page_number in range(0, pdf.getNumPages()):

        page = pdf.getPage(page_number)
        contents = page.getContents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, replacements)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.getObject()
                    process_data(streamObj, replacements)

        # Force content replacement
        page[NameObject("/Contents")] = contents.decodedSelf
        writer.addPage(page)

    with open(filename_base + ".result.pdf", 'wb') as out_file:
        writer.write(out_file)
        
if __name__ == '__main__':
    go('v.pdf')