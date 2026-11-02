import sys, re, zlib
data = open(sys.argv[1], 'rb').read()
out = []
for m in re.finditer(rb'stream\r?\n', data):
    s = m.end()
    e = data.find(b'endstream', s)
    if e < 0: continue
    try:
        d = zlib.decompress(data[s:e])
    except Exception:
        try: d = zlib.decompressobj().decompress(data[s:e])
        except Exception: continue
    if b'BT' not in d: continue
    parts = []
    for t in re.finditer(rb'\((.*?)(?<!\\)\)\s*Tj|\[(.*?)\]\s*TJ', d, re.S):
        if t.group(1) is not None:
            parts.append(t.group(1))
        else:
            parts.append(b''.join(re.findall(rb'\((.*?)(?<!\\)\)', t.group(2), re.S)))
    txt = b' '.join(parts).decode('latin-1')
    if txt.strip(): out.append(txt)
print('\n----\n'.join(out))
