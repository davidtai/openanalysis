# Print filled rectangles (x, y, w, h, fill rgb) from one PDF page's content stream, including form XObjects.
import sys, re
from pypdf import PdfReader
r = PdfReader(sys.argv[1]); page = r.pages[int(sys.argv[2]) - 1]
def streams(obj):
    c = obj.get_contents()
    yield c.get_data() if c is not None else b''
    res = obj.get('/Resources') or {}
    xo = res.get('/XObject') or {}
    for k in xo:
        x = xo[k].get_object()
        if x.get('/Subtype') == '/Form':
            yield x.get_data()
data = b'\n'.join(streams(page)).decode('latin-1')
tok = re.findall(r'[-+]?\d*\.?\d+|[A-Za-z*\'"]+', data)
stack = []; fill = None; cm = None
for t in tok:
    if re.match(r'^[-+]?\d*\.?\d+$', t): stack.append(float(t)); continue
    if t in ('rg', 'sc', 'scn') and len(stack) >= 3: fill = tuple(round(v, 3) for v in stack[-3:])
    elif t == 'g' and len(stack) >= 1: fill = (stack[-1],)*3
    elif t == 're' and len(stack) >= 4:
        x, y, w, h = stack[-4:]
        print(f"re x={x:.1f} y={y:.1f} w={w:.1f} h={h:.1f} fill={fill}")
    elif t == 'cm' and len(stack) >= 6: print('cm', stack[-6:])
    stack = []
