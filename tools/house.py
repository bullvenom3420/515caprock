"""515 Cap Rock Drive - conceptual 3D model, built from the June 3, 2026 plan set.

All units are FEET.  Coordinate system:
  x : left -> right as seen from the street (0 = outer face of the left wall)
  y : front -> rear  (0 = front wall of the dining room / study)
  z : up (0 = first finished floor)

Sources (all measured from the vector PDF at its true 1/4" = 1'-0" scale):
  sheet 3  first floor plan      -> first-floor walls, openings
  sheet 4  second floor plan     -> second-floor walls, Bed #5 over the porch
  sheet 5  roof plan             -> every eave, rake, ridge, hip and valley line
  sheet 1  front / rear elev.    -> plate heights, window and door heights
  sheet 2  left / right elev.    -> side windows, gable stacking
Plate heights from the drawings: 10'-1" (garage, primary suite), 20'-7" (two-story
walls), 21'-7" (front block and Bed #5).  Pitches 8:12 with 4:12 kicks where noted.
The roof surface sits 0.56 ft above plate at each eave edge, which puts the main
ridge at the drawings' 34'-10 1/2" overall height.

Only what the drawings show is modelled.  Items marked optional on the drawings
(dashed "OPT. 3050" windows) and light fixtures are left out.

geometry() returns a list of faces: (points[[x,y,z],...], material)
TAGS maps a face index to a name for faces other tools need (window glass).
"""
import math

T = 0.5                 # roof slab thickness (ft)
C = 0.56                # roof top surface above plate at the eave edge
P1, P2, P2F = 10 + 1 / 12, 20 + 7 / 12, 21 + 7 / 12
E1, E2, EF = P1 + C, P2 + C, P2F + C
S8, S4 = 8 / 12, 4 / 12

faces = []
TAGS = {}
FACE_GROUP = []          # build-animation piece of each face (parallel to faces)
GROUP = ['ff']
PET_QUADS = {}
INTERIOR = [False]       # True: floors are hollow shells with rooms and doorways (build animation, viewer floors)
FF = 0.0                 # first finished floor
F2 = P1 + 1.0            # second finished floor
WALL_T, PART_T = 0.8, 0.42


def setgroup(g):
    GROUP[0] = g


def face(pts, mat, tag=None):
    if tag:
        TAGS[tag] = len(faces)
    faces.append(([list(map(float, p)) for p in pts], mat))
    FACE_GROUP.append(GROUP[0])


# ---------------------------------------------------------------- primitives
def prism_z(z0, z1, poly_xy, mat='wall'):
    n = len(poly_xy)
    face([(x, y, z0) for x, y in poly_xy], mat)
    face([(x, y, z1) for x, y in poly_xy], mat)
    for i in range(n):
        (xa, ya), (xb, yb) = poly_xy[i], poly_xy[(i + 1) % n]
        face([(xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1)], mat)


def prism_x(x0, x1, poly_yz, mat='wall'):
    n = len(poly_yz)
    face([(x0, y, z) for y, z in poly_yz], mat)
    face([(x1, y, z) for y, z in poly_yz], mat)
    for i in range(n):
        (ya, za), (yb, zb) = poly_yz[i], poly_yz[(i + 1) % n]
        face([(x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb)], mat)


def prism_y(y0, y1, poly_xz, mat='wall'):
    n = len(poly_xz)
    face([(x, y0, z) for x, z in poly_xz], mat)
    face([(x, y1, z) for x, z in poly_xz], mat)
    for i in range(n):
        (xa, za), (xb, zb) = poly_xz[i], poly_xz[(i + 1) % n]
        face([(xa, y0, za), (xa, y1, za), (xb, y1, zb), (xb, y0, zb)], mat)


def slab(poly_xy, zfun, t=T, mat='roof'):
    """Roof plane: top surface on zfun(x,y), thickness t below it."""
    n = len(poly_xy)
    top = [(x, y, zfun(x, y)) for x, y in poly_xy]
    bot = [(x, y, zfun(x, y) - t) for x, y in poly_xy]
    face(top, mat)
    face(bot[::-1], mat)
    for i in range(n):
        j = (i + 1) % n
        face([bot[i], bot[j], top[j], top[i]], mat)


def arch_pts(x0, x1, zs, n=12):
    """Semicircle from (x1, zs) over the top to (x0, zs)."""
    c, r = (x0 + x1) / 2, (x1 - x0) / 2
    return [(c + r * math.cos(math.pi * i / n), zs + r * math.sin(math.pi * i / n)) for i in range(n + 1)]


def seg_pts(x0, x1, zs, rise, n=12):
    """Segmental arch from (x1, zs) over to (x0, zs) with the given rise."""
    hw = (x1 - x0) / 2
    if rise >= hw - 1e-6:
        return arch_pts(x0, x1, zs, n)
    r = (hw * hw + rise * rise) / (2 * rise)
    c, cz = (x0 + x1) / 2, zs + rise - r
    a0 = math.asin((zs - cz) / r)
    return [(c + r * math.cos(a0 + (math.pi - 2 * a0) * i / n), cz + r * math.sin(a0 + (math.pi - 2 * a0) * i / n))
            for i in range(n + 1)]


def opening(axis, at, u0, u1, z0, z1, out, arch=False, mat='glass', d=0.06, tag=None, rise=None):
    """Glass/door panel on a wall plane.  axis 'y': plane y=at spanning x u0..u1;
    axis 'x': plane x=at spanning y u0..u1.  out = direction the wall faces (+1/-1).
    arch=True: z1 is the springline and a semicircle (or a segment of the given
    rise) sits on top."""
    if arch:
        prof = [(u0, z0), (u1, z0)] + (seg_pts(u0, u1, z1, rise) if rise else arch_pts(u0, u1, z1))
    else:
        prof = [(u0, z0), (u1, z0), (u1, z1), (u0, z1)]
    c = at + out * d
    if axis == 'y':
        face([(u, c, z) for u, z in prof], mat, tag)
    else:
        face([(c, u, z) for u, z in prof], mat, tag)


def shutter(axis, at, u0, u1, z0, z1, out, t=0.14):
    """Shutter panel standing proud of the wall (both drawn on the elevations)."""
    if axis == 'y':
        a, b = sorted((at, at + out * t))
        prism_y(a, b, [(u0, z0), (u1, z0), (u1, z1), (u0, z1)])
    else:
        a, b = sorted((at, at + out * t))
        prism_x(a, b, [(u0, z0), (u1, z0), (u1, z1), (u0, z1)])


# ---------------------------------------------------------------- hollow shells (build animation / viewer floors)
def box(x0, x1, y0, y1, z0, z1, mat='wall'):
    prism_z(z0, z1, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], mat)


def _area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def inset(poly, d):
    ccw = _area(poly) > 0
    n = len(poly); lines = []
    for i in range(n):
        (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
        dx, dy = xb - xa, yb - ya; L = (dx * dx + dy * dy) ** 0.5
        nx, ny = (-dy / L, dx / L) if ccw else (dy / L, -dx / L)
        lines.append(((xa + nx * d, ya + ny * d), (dx / L, dy / L)))
    out = []
    for i in range(n):
        (p1, d1), (p2, d2) = lines[i - 1], lines[i]
        den = d1[0] * d2[1] - d1[1] * d2[0]
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
        out.append((p1[0] + d1[0] * t, p1[1] + d1[1] * t))
    return out


def shell(z0, z1, poly, floor_z, bottom=False, t=None, floor=True):
    """Exterior walls of thickness t around poly, open on top, with a floor."""
    t = WALL_T if t is None else t
    inner = inset(poly, t); n = len(poly)
    for i in range(n):
        (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
        face([(xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1)], 'wall')
        (ia, ja), (ib, jb) = inner[i], inner[(i + 1) % n]
        face([(ia, ja, floor_z), (ib, jb, floor_z), (ib, jb, z1), (ia, ja, z1)], 'wall')
        face([(xa, ya, z1), (xb, yb, z1), (ib, jb, z1), (ia, ja, z1)], 'wall')
        if bottom:
            face([(xa, ya, z0), (xb, yb, z0), (ib, jb, z0), (ia, ja, z0)], 'wall')
    if floor:
        face([(x, y, floor_z) for x, y in inner], 'floor')
    return inner


def partitions(walls, inner, z0, z1, door_top, t=None):
    """Interior walls ('h', y, x0, x1[, doors]) / ('v', x, y0, y1[, doors]); doors are (center, width).
    Ends near an exterior wall or another partition snap to its face exactly, so nothing overlaps."""
    t = PART_T if t is None else t
    n = len(inner)
    def stops(kind, at):
        c = []
        for i in range(n):
            (xa, ya), (xb, yb) = inner[i], inner[(i + 1) % n]
            if kind == 'h' and abs(xa - xb) < 1e-6 and min(ya, yb) <= at <= max(ya, yb):
                c.append((xa, 0.0))
            if kind == 'v' and abs(ya - yb) < 1e-6 and min(xa, xb) <= at <= max(xa, xb):
                c.append((ya, 0.0))
        for w2 in walls:
            k2, at2, a2, b2 = w2[:4]
            if k2 != kind and min(a2, b2) - 0.5 <= at <= max(a2, b2) + 0.5:
                c.append((at2, t / 2))
        return c
    def snap(v, cands, lo_end):
        best = None
        for c, half in cands:
            target = c + half if lo_end else c - half
            if abs(target - v) < 1.6 + half and (best is None or abs(target - v) < abs(best - v)):
                best = target
        return v if best is None else best
    def piece(kind, at, u0, u1, za, zb):
        if u1 - u0 < 1e-3:
            return
        if kind == 'h':
            box(u0, u1, at - t / 2, at + t / 2, za, zb)
        else:
            box(at - t / 2, at + t / 2, u0, u1, za, zb)
    for w in walls:
        kind, at, a, b = w[:4]
        doors = sorted(w[4]) if len(w) > 4 else []
        a, b = min(a, b), max(a, b)
        cands = stops(kind, at)
        a2, b2 = snap(a, cands, True), snap(b, cands, False)
        u = a2
        for c, wd in doors:
            d0, d1 = max(c - wd / 2, a2), min(c + wd / 2, b2)
            piece(kind, at, u, d0, z0, z1); piece(kind, at, d0, d1, door_top, z1); u = d1
        piece(kind, at, u, b2, z0, z1)


# ---------------------------------------------------------------- roof planes
def f_front(x, y):                        # front block: 4:12 kick to y=6, then 8:12
    return EF + (y + 3) * S4 if y <= 6 else EF + 3 + (y - 6) * S8


def wing_front(x, y):                     # side wings: 4:12 kick to y=15, then 8:12
    return E2 + (y - 6) * S4 if y <= 15 else E2 + 3 + (y - 15) * S8


def rear(x, y):                           # one rear plane runs the full width
    return E2 + (41.17 - y) * S8


RIDGE = f_front(0, 20.59)                 # 34.87 ft = 34'-10 1/2" overall
WING_RIDGE = rear(0, 25.83)
SMALL_RIDGE = rear(0, 29.59)


def build():
    faces.clear()
    TAGS.clear()
    FACE_GROUP.clear()
    PET_QUADS.clear()
    setgroup('ff')

    # ============ WALLS ============
    if INTERIOR[0]:
        # first floor: one shell around the two-story house, garage wing and primary suite
        ff = [(0, 9), (8.33, 9), (8.33, 0), (49.33, 0), (49.33, 9), (56.67, 9), (56.67, 19.5), (59, 19.5),
              (59, 33.83), (61.5, 33.83), (61.5, 56.17), (45.5, 56.17), (45.5, 49.17), (39.5, 49.17),
              (39.5, 36.67), (22, 36.67), (22, 67.33), (0, 67.33)]
        inner = shell(0, P1, ff, FF)
        partitions([                                       # traced from the first floor plan; (center, width) doors
            ('h', 40.9, 0, 22, [(12.5, 2.8)]),              # mud, laundry | garage
            ('v', 8.75, 10.4, 36.9, [(17.9, 4.0)]),         # laundry, scullery | kitchen (cased opening)
            ('h', 25.0, 0, 8.75),                           # laundry | scullery
            ('h', 36.6, 8.75, 22, [(10.6, 2.6)]),           # kitchen | mud hall
            ('h', 37.9, 0, 8.75, [(6.8, 2.6)]),             # laundry | mud hall
            ('v', 24.25, 0, 15.9, [(8.4, 8.0)]),            # dining | foyer (8090 arched opening)
            ('h', 15.9, 8.75, 24.25, [(16.5, 11.0)]),       # dining | kitchen (11490 arched opening)
            ('v', 34.25, 0, 11.4, [(8.0, 4.6)]),            # foyer | study (French doors)
            ('h', 11.4, 34.25, 49.33, [(36.0, 2.6)]),       # study | storage, closet
            ('v', 47.25, 11.4, 36.15),                      # family, stair | primary bath and closet
            ('h', 19.6, 47.25, 59, [(51.5, 2.8)]),          # primary bath | closet
            ('h', 33.4, 47.25, 59, [(50.0, 2.8)]),          # primary bath | hall
            ('v', 45.5, 39.83, 49.17),                      # primary bedroom | powder
            ('h', 44.0, 39.5, 45.5, [(42.5, 2.5)]),         # powder | hall
            ('h', 39.4, 45.5, 61.5, [(49.5, 2.8)]),         # primary bedroom | hall
        ], inner, FF, P1, FF + 8.0)
        setgroup('gceil')
        box(0 + WALL_T, 22 - WALL_T, 40.9 + PART_T / 2, 67.33 - WALL_T, P1 - 0.25, P1)    # garage ceiling
        setgroup('sf')
        sf = [(0, 9), (8.33, 9), (8.33, 0), (49.33, 0), (49.33, 9), (56.67, 9), (56.67, 19.5), (59, 19.5),
              (59, 39.83), (39.67, 39.83), (39.67, 50.67), (23.83, 50.67), (23.83, 39.83), (0, 39.83)]
        inner = shell(P1, P2, sf, F2, bottom=True)
        face([(x, y, P1) for x, y in inner], 'wall')       # underside of the second floor deck (porch ceiling)
        partitions([                                       # traced from the second floor plan
            ('v', 15.0, 25.75, 39.83, [(28.0, 2.6)]),       # Bed 2 | hall
            ('h', 25.75, 0, 15.0, [(4.0, 2.5)]),            # Bed 2 | Bath 2
            ('h', 30.0, 15.0, 24.5, [(17.5, 2.6)]),         # attic storage | hall
            ('v', 24.5, 16.25, 39.83, [(27.5, 3.0)]),       # attic, hall | game room
            ('h', 19.0, 0, 15.0, [(5.0, 2.5)]),             # Bath 2 | closet
            ('v', 9.25, 13.75, 25.75, [(16.5, 2.5)]),       # closets | baths
            ('h', 13.75, 9.25, 23.75, [(13.5, 2.6)]),       # baths | Bed 3
            ('v', 23.75, 0, 13.75, [(3.0, 2.6)]),           # Bed 3 | stair landing
            ('h', 16.25, 24.5, 45.0, [(29.5, 7.0), (39.0, 7.0)]),   # game room | stair (open, railed)
            ('v', 45.0, 27.0, 39.83, [(33.0, 2.6)]),        # game room | Bed 4
            ('h', 27.0, 45.0, 59, [(47.8, 2.8)]),           # Bed 4 | closet, bath
            ('h', 32.65, 24.5, 45.0, [(27.5, 2.8)]),        # game room | Bath 5, closet
            ('v', 30.0, 32.65, 38.75, [(35.7, 2.4)]),       # hall | Bath 5
            ('h', 38.75, 30.0, 39.75, [(34.5, 2.4)]),       # Bath 5 | Bed 5
            ('v', 39.75, 32.65, 39.83, [(36.0, 2.4)]),      # Bath 5 | closet
        ], inner, F2, P2, F2 + 7.0)
        # the front block and Bed #5 rise to the 21'-7" plate: wall rings, open over the rooms
        for poly in ([(8.33, 0), (49.33, 0), (49.33, 9), (8.33, 9)],
                     [(23.83, 39.83), (39.67, 39.83), (39.67, 50.67), (23.83, 50.67)]):
            shell(P2, P2F, poly, P2, floor=False)
        setgroup('ff')
    else:
        # two-story mass, first floor to the 20'-7" plate (porch recess cut out)
        two_story = [(0, 9), (8.33, 9), (8.33, 0), (49.33, 0), (49.33, 9), (56.67, 9),
                     (56.67, 19.5), (59, 19.5), (59, 39.83), (39.5, 39.83), (39.5, 36.67),
                     (22, 36.67), (22, 39.83), (0, 39.83)]
        prism_z(0, P2, two_story)
        # front block rises to the 21'-7" plate
        prism_z(P2, P2F, [(8.33, 0), (49.33, 0), (49.33, 9), (8.33, 9)])
        # second floor over the outdoor living porch, Bed #5 projecting to the rear
        prism_z(P1, P2, [(22, 36.67), (39.5, 36.67), (39.5, 39.83), (39.67, 39.83),
                         (39.67, 50.67), (23.83, 50.67), (23.83, 39.83), (22, 39.83)])
        prism_z(P2, P2F, [(23.83, 39.83), (39.67, 39.83), (39.67, 50.67), (23.83, 50.67)])
        # one-story garage / mud wing
        prism_z(0, P1, [(0, 39.83), (22, 39.83), (22, 67.33), (0, 67.33)])
        # one-story primary suite and hall
        prism_z(0, P1, [(39.5, 39.83), (59, 39.83), (59, 33.83), (61.5, 33.83), (61.5, 56.17),
                        (45.5, 56.17), (45.5, 49.17), (39.5, 49.17)])

    # ============ ROOF (roof plan, sheet 5) ============
    setgroup('froof')
    # front block
    slab([(5.33, -3), (52.33, -3), (50.33, -1), (50.33, 6), (7.33, 6), (7.33, -1)], f_front)
    slab([(7.33, 6), (50.33, 6), (50.33, 20.59), (7.33, 20.59)], f_front)
    slab([(5.33, -3), (7.33, -1), (7.33, 11), (5.33, 9)], lambda x, y: EF + (x - 5.33) * S4)
    slab([(52.33, -3), (52.33, 9), (50.33, 11), (50.33, -1)], lambda x, y: EF + (52.33 - x) * S4)
    setgroup('wroof')
    # left wing + left side skirt
    slab([(-3, 6), (5.33, 6), (5.33, 9), (7.33, 11), (7.33, 15), (-1, 15), (-1, 8)], wing_front)
    slab([(-1, 15), (7.33, 15), (7.33, 25.83), (-1, 25.83)], wing_front)
    slab([(-3, 6), (-1, 8), (-1, 40.17), (-3, 41.17)], lambda x, y: E2 + (x + 3) * S4)
    # right wing + right skirt + the small gable over the primary bath
    slab([(52.33, 6), (59.67, 6), (57.67, 8), (57.67, 15), (50.33, 15), (50.33, 11), (52.33, 9)],
         wing_front)
    slab([(50.33, 15), (57.67, 15), (57.67, 25.83), (50.33, 25.83)], wing_front)
    slab([(59.67, 6), (59.67, 18), (57.67, 19), (57.67, 8)], lambda x, y: E2 + (59.67 - x) * S4)
    slab([(57.67, 19), (59.67, 18), (60.5, 18), (60.5, 29.59), (57.67, 29.59)],
         lambda x, y: E2 + (y - 18) * S8)
    setgroup('rroof')
    # the full-width rear plane
    slab([(-1, 25.83), (7.33, 25.83), (7.33, 20.59), (50.33, 20.59), (50.33, 25.83),
          (57.67, 25.83), (57.67, 29.59), (60.5, 29.59), (60.5, 41.17), (40.5, 41.17),
          (40.5, 39.67), (31.67, 30.83), (22.83, 39.67), (22.83, 41.17), (-3, 41.17),
          (-1, 40.17)], rear)
    # Bed #5 hip (21'-7" plate)
    slab([(22.83, 39.67), (31.67, 30.83), (31.67, 42.83), (22.83, 51.67)],
         lambda x, y: EF + (x - 22.83) * S8)
    slab([(40.5, 39.67), (40.5, 51.67), (31.67, 42.83), (31.67, 30.83)],
         lambda x, y: EF + (40.5 - x) * S8)
    slab([(22.83, 51.67), (31.67, 42.83), (40.5, 51.67)], lambda x, y: EF + (51.67 - y) * S8)
    setgroup('low')
    # garage hip (10'-1" plate), ridge dies into the main house
    slab([(-1.5, 39.83), (11, 39.83), (11, 56.33), (-1.5, 68.83)], lambda x, y: E1 + (x + 1.5) * S8)
    slab([(-1.5, 68.83), (11, 56.33), (23.5, 68.83)], lambda x, y: E1 + (68.83 - y) * S8)
    slab([(11, 56.33), (11, 39.83), (11.14, 39.83), (22, 51.67), (23.5, 51.67), (23.5, 68.83)],
         lambda x, y: E1 + (23.5 - x) * S8)
    # "slope as req'd" between the garage and Bed #5
    zg = E1 + (23.5 - 12.37) * S8
    k = (zg - (E1 + 1.5 * S8)) / 10.5
    slab([(11.14, 39.83), (23.83, 39.83), (23.83, 51.67), (22, 51.67)],
         lambda x, y: zg - (y - 41.17) * k)
    # primary suite hip (10'-1" plate) and the 4:12 roof beside Bed #5
    slab([(59, 32.33), (63, 32.33), (63, 57.67), (53.5, 48.17), (53.5, 39.83), (59, 39.83)],
         lambda x, y: E1 + (63 - x) * S8)
    slab([(44, 57.67), (63, 57.67), (53.5, 48.17)], lambda x, y: E1 + (57.67 - y) * S8)
    slab([(44, 51.67), (44, 57.67), (53.5, 48.17), (53.5, 39.83), (51.42, 39.83), (45.5, 51.67)],
         lambda x, y: E1 + (x - 44) * S8)
    slab([(39.67, 39.83), (51.42, 39.83), (45.5, 51.67), (39.67, 51.67)],
         lambda x, y: E1 + 1.5 * S8 + (51.67 - y) * S4)

    setgroup('gable')
    # ============ GABLE WALLS (side elevations: three stepped gables each side) ============
    # Gable walls stop just under the roof surface and sit a hair inside the rake,
    # so the roof's own edge reads as the rake trim.
    g, dz = 0.3, 0.45
    lo = lambda pts: [(y, z - dz) for y, z in pts]
    # left wing gable, sitting on the side skirt
    prism_x(-0.9, -0.9 + g, lo([(8, E2 + 2 * S4), (15, E2 + 3), (25.83, WING_RIDGE), (40.17, E2 + 2 * S4)]))
    # main gables at the ends of the 34'-10 1/2" ridge
    main = lo([(-1, EF + 2 * S4), (6, EF + 3), (20.59, RIDGE), (25.83, WING_RIDGE),
               (15, E2 + 3), (11, E2 + 5 * S4)])
    prism_x(7.43, 7.43 + g, main)
    prism_x(50.23 - g, 50.23, main)
    # right wing gable, sitting on the right skirt and the small gable roof
    prism_x(57.57 - g, 57.57, lo([(8, E2 + 2 * S4), (15, E2 + 3), (25.83, WING_RIDGE),
                                  (29.59, SMALL_RIDGE), (19, E2 + 2 * S4)]))
    # small gable over the primary bath (wall line x=59, rake at 60.5)
    prism_x(59 - g, 59, [(19.5, P2), (19.5, E2 + 1.5 * S8 - dz), (29.59, SMALL_RIDGE - dz),
                         (39.83, rear(0, 39.83) - dz), (39.83, P2)])

    setgroup('rroof')
    # ============ CHIMNEY (brick chimney w/ metal cap) ============
    prism_z(rear(0, 26.4) - 1.0, 37.2, [(44.2, 23.2), (47.0, 23.2), (47.0, 26.4), (44.2, 26.4)])
    prism_z(37.2, 37.6, [(43.95, 22.95), (47.25, 22.95), (47.25, 26.65), (43.95, 26.65)])

    setgroup('froof')
    # ============ ROLL-TOP DORMERS (three, 2040 fixed arch windows) ============
    yf = -0.12
    for xc in (16.33, 28.83, 41.33):
        x0, x1 = xc - 2.455, xc + 2.455
        spring = 28.33 - 2.455             # crown 6'-2" above the 22'-2" base (dormer detail)
        zb = f_front(0, yf) - 0.3
        prism_y(yf - 0.01, yf, [(x0, zb), (x1, zb)] + arch_pts(x0, x1, spring))
        yb = 6 + (spring - (EF + 3)) / S8  # where the side walls die into the roof
        side = [(yf, zb), (6, f_front(0, 6) - 0.3), (yb, spring - 0.3), (yb, spring), (yf, spring)]
        prism_x(x0, x0 + 0.01, side)
        prism_x(x1 - 0.01, x1, side)
        ye = 6 + (spring + 2.455 + 0.1 - (EF + 3)) / S8
        arc = arch_pts(x0 - 0.15, x1 + 0.15, spring, 14)
        for i in range(len(arc) - 1):
            (ua, za), (ub, zb2) = arc[i], arc[i + 1]
            face([(ua, yf - 0.35, za), (ub, yf - 0.35, zb2), (ub, ye, zb2), (ua, ye, za)], 'roof')
        opening('y', yf, xc - 1.0, xc + 1.0, 23 + 1 / 12, 26 + 1 / 12, -1, arch=True)   # sill @ 23'-1"

    setgroup('open')
    # ============ FRONT (sheet 1) ============
    F = -1
    for i, xc in enumerate((16.33, 28.83, 41.33)):
        opening('y', 0, xc - 1.5, xc + 1.5, 14.7, 19.7, F, tag=('win2f_%d' % i))
        shutter('y', 0, xc - 3.0, xc - 1.6, 14.5, 20.0, F)
        shutter('y', 0, xc + 1.6, xc + 3.0, 14.5, 20.0, F)
    # dining room and study: 5086 segmental-arch openings (R3'-6", springpoint 7'-2")
    # with arched French doors, tall shutters either side
    for xc, tg in ((16.33, 'door_dining'), (41.33, 'door_study')):
        opening('y', 0, xc - 2.5, xc + 2.5, 0.1, 7 + 2 / 12, F, arch=True, rise=8.5 - (7 + 2 / 12), tag=tg)
        shutter('y', 0, xc - 4.15, xc - 2.65, 0.3, 8.9, F)
        shutter('y', 0, xc + 2.65, xc + 4.15, 0.3, 8.9, F)
    # entry: 7'-0" x 9'-0" full-arch opening (springpoint 5'-6")
    opening('y', 0, 25.33, 32.33, 0.1, 5.5, F, arch=True)
    # recessed wing faces (y = 9)
    for x0 in (2.67, 52.5):
        opening('y', 9, x0, x0 + 2.0, 3.0, 8.0, F, mat='darkglass' if x0 < 10 else 'glass', tag='wing_l' if x0 < 10 else None)
        opening('y', 9, x0, x0 + 2.0, 16.0, 20.0, F)

    # ============ LEFT SIDE (x = 0) ============
    L = -1
    opening('x', 0, 16.17, 20.17, 3.6, 8.4, L)
    opening('x', 0, 27.83, 29.83, 4.0, 8.0, L)
    opening('x', 0, 37.83, 39.83, 4.0, 8.0, L)
    opening('x', 0, 18.5, 20.5, 14.6, 19.0, L)
    opening('x', 0, 30.75, 34.75, 14.6, 19.0, L)

    # ============ RIGHT SIDE (x = 59) ============
    R = 1
    opening('x', 59, 23.75, 25.75, 4.0, 8.6, R)
    opening('x', 59, 28.4, 33.0, 4.0, 8.6, R)
    opening('x', 59, 28.8, 32.6, 14.4, 19.6, R)

    # ============ REAR ============
    for x0 in (48.9, 52.55, 56.2):                       # three 3060 SH, primary bedroom
        opening('y', 56.17, x0, x0 + 3.0, 3.0, 9.2, R)
    opening('y', 49.17, 40.8, 43.8, 0.1, 8.0, R)        # door to the porch
    opening('y', 36.67, 23.0, 39.0, 0.1, 8.0, R)        # 16080 sliding door unit
    opening('y', 50.67, 29.8, 34.8, 15.4, 19.6, R, tag='win_bed5')   # Bed #5
    opening('y', 67.33, 2.8, 20.6, 0.1, 8.0, R, mat='void')   # 18080 overhead garage door
    opening('x', 22, 54.5, 57.2, 0.1, 8.0, R)           # garage service door

    # ============ PETS (true to life; seen in the last, street-facing view of the intro) ============
    # Huckleberry (70 lb sheepadoodle) stands side-on just inside the study's arched French door;
    # the cat (12 lb Russian Blue) sits tall on the sill of the left wing window, darker glass behind her.
    PET_QUADS['dog'] = dict(o=(41.33 - 1.95, -0.075, FF), U=(3.9, 0, 0), V=(0, 0, 3.9 * 48 / 64), n=(0, -1, 0),
                            fid=TAGS['door_study'] + 1, sprite='dog')
    PET_QUADS['cat'] = dict(o=(3.67 - 0.44, 9 - 0.075, 3.0), U=(0.88, 0, 0), V=(0, 0, 1.1), n=(0, -1, 0),
                            fid=TAGS['wing_l'] + 1, sprite='cat')
    return list(faces)


def geometry():
    return build()


# render / glb tooling
CENTER = (30.0, 33.0, 12.0)

# Pets change spot and pose on every site.  Here Huckleberry sits just inside the
# dining room's arched French door, and the cat sits on the sill of the Bed #5
# window at the back, so she only appears once the house has turned around.
# (tag, anchor = bottom-centre of the sprite's full viewBox in world ft, viewBox height ft, sprite)
PETS = [('door_dining', (16.33, 1.4, -0.05), 5.4, 'dog.png'),
        ('win_bed5', (32.3, 50.0, 15.3), 3.2, 'cat.png')]

if __name__ == '__main__':
    g = geometry()
    print(len(g), 'faces', 'ridge', round(RIDGE, 3), 'wing', round(WING_RIDGE, 2), 'small', round(SMALL_RIDGE, 2))
