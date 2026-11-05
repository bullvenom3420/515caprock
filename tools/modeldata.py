"""Write assets/mobile/model-data.js for the touch-rotatable phone viewer.
Same white-clay colours and outline edges as the rendered frames.
python3 modeldata.py OUT.js"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import house, render

FT = 0.3048
CX, CY = house.CENTER[0], house.CENTER[1]


def tf(p):                       # viewer space: metres, Y up, front of house faces +Z
    return [(p[0] - CX) * FT, p[2] * FT, -(p[1] - CY) * FT]


COL = {'wall': [0.93, 0.92, 0.89], 'roof': [0.87, 0.86, 0.84],
       'glass': [0.62, 0.62, 0.65], 'void': [0.30, 0.29, 0.31]}
pos, nrm, col, lines, seen = [], [], [], [], set()
for pts, mat in house.geometry():
    tris, n = render.triangulate(pts)
    N = np.array([n[0], n[2], -n[1]])
    N /= np.linalg.norm(N) + 1e-12
    for t in tris:
        for i in t:
            pos.append(tf(pts[i])); nrm.append(list(N)); col.append(COL[mat])
    k = len(pts)
    for i in range(k):
        a = tuple(round(v, 3) for v in tf(pts[i])); b = tuple(round(v, 3) for v in tf(pts[(i + 1) % k]))
        key = tuple(sorted([a, b]))
        if a == b or key in seen:
            continue
        seen.add(key); lines += [list(a), list(b)]

enc = lambda a: base64.b64encode(np.asarray(a, np.float32).tobytes()).decode()
js = 'window.CAPROCK_MODEL={pos:"%s",nrm:"%s",col:"%s",lines:"%s"};' % (enc(pos), enc(nrm), enc(col), enc(lines))
open(sys.argv[1], 'w').write(js)
print(sys.argv[1], len(js), 'bytes', len(pos) // 3, 'triangles', len(lines) // 2, 'edges')
