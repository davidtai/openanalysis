import sys
from pypdf import PdfReader, PdfWriter
r = PdfReader(sys.argv[1]); w = PdfWriter()
w.add_page(r.pages[int(sys.argv[2]) - 1]); w.write(sys.argv[3])
