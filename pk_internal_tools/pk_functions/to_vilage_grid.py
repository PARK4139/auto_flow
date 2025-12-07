import math

def to_vilage_grid(lat, lon):
    """
    Convert WGS84(lat, lon) -> KMA DFS grid (x,y).
    """
    # Lambert Conformal Conic (KMA DFS) simplified impl.
    RE, GRID, SLAT1, SLAT2, OLON, OLAT = 6371.00877, 5.0, 30.0, 60.0, 126.0, 38.0
    XO, YO = 43, 136
    DEGRAD = math.pi / 180.0
    re = RE / GRID
    slat1 = SLAT1 * DEGRAD; slat2 = SLAT2 * DEGRAD
    olon  = OLON  * DEGRAD; olat  = OLAT  * DEGRAD
    sn = math.tan(math.pi*0.25 + slat2*0.5) / math.tan(math.pi*0.25 + slat1*0.5)
    sn = math.log(math.cos(slat1)/math.cos(slat2)) / math.log(sn)
    sf = (math.tan(math.pi*0.25 + slat1*0.5) ** sn) * math.cos(slat1) / sn
    ro = re * sf / (math.tan(math.pi*0.25 + olat*0.5) ** sn)
    ra = re * sf / (math.tan(math.pi*0.25 + lat*DEGRAD*0.5) ** sn)
    theta = (lon*DEGRAD) - olon
    if theta > math.pi: theta -= 2.0 * math.pi
    if theta < -math.pi: theta += 2.0 * math.pi
    theta *= sn
    x = int(ra*math.sin(theta) + XO + 0.5)
    y = int(ro - ra*math.cos(theta) + YO + 0.5)
    return x, y