import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
for i, p in enumerate(r.pages):
    try:
        t = p.extract_text() or ""
    except Exception as e:
        t = f"<err {e}>"
    print(f"=== page {i+1} ===")
    print(t)
