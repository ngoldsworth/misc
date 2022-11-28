## 2022-10-18: Dad called me and asked how to split a PDF file into seperate pages.
# This is a script to do that.

import pathlib as pl
from PyPDF2 import PdfFileWriter, PdfFileReader

## VARIABLES TO CHANGE
# the path to the file you want to split. the letter "r" before the
# single-quotes mark is necessary
input_dir = r'C:\Users\Nelson.Goldsworth\Documents\repos\misc\pdfs' # the folder your PDF lives in
input_file_name = r'latino-production-1018-1666078927880-CLEANED.pdf' # the name of your PDF

# what prefix do you want the individual files to have before the numbers in the filename?
usr_prefix = '12121_Page'


## MAIN PROGRAM
if __name__ == '__main__':
    # get information about location on disk that things will be saved to
    p_input_dir = pl.Path(input_dir)
    p_input_file_name = pl.Path(input_file_name)
    input_file_path = pl.Path(input_dir) / pl.Path(input_file_name)

    # place the individual pages into a folder called "split" that lives right next to the original document
    output_dir  = p_input_dir / 'split'
    if not output_dir.exists():
        output_dir.mkdir()

    input_pdf = PdfFileReader(input_file_path)

    # determine zero-padding needs
    page_count = input_pdf.numPages
    z_width = len(str(page_count))

    # iterate over PDF pages, saving each to new file
    for p in range(input_pdf.numPages):
        # convert the page number to a character, and zero pad to desired width
        page_number_as_string = str(p+1).zfill(z_width)
        out = PdfFileWriter()
        out.addPage(input_pdf.getPage(p))

        # TODO: name format
        name = f'{usr_prefix}_{page_number_as_string}.pdf'
        with open(output_dir / name, 'wb') as out_stream:
            out.write(out_stream)