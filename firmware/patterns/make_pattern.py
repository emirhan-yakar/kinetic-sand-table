#!/usr/bin/env python3
# Sandify uyumlu theta-rho (.thr) desen ureteci.
# Cikti satirlari: "<theta_radyan> <rho 0..1>".  Top bu yolu izleyerek kumu cizer.
import math, os
HERE=os.path.dirname(os.path.abspath(__file__))

def write_thr(name, pts):
    with open(os.path.join(HERE,name),"w") as f:
        for th,rh in pts:
            f.write(f"{th:.5f} {max(0.0,min(1.0,rh)):.5f}\n")
    print(name, len(pts), "nokta")

# --- 1) spiral + gul (rose) bilesimi: ice spiral, salinimli yariçap ---
def spiral_rose(turns=26, petals=5, steps=4200):
    pts=[]
    for i in range(steps+1):
        t=i/steps
        theta=t*turns*2*math.pi
        base=1.0-t                      # disardan ice spiral
        rho=base*(0.55+0.45*abs(math.sin(petals*theta/turns)))
        pts.append((theta,rho))
    # geri disari, faz kaymali (desen zenginlesir)
    for i in range(steps+1):
        t=i/steps
        theta=turns*2*math.pi + t*turns*2*math.pi
        base=t
        rho=base*(0.55+0.45*abs(math.sin((petals+2)*theta/turns + 0.6)))
        pts.append((theta,rho))
    return pts

# --- 2) sade konsantrik+spiral (klasik Sisyphus) ---
def classic(loops=40, steps=6000):
    pts=[]
    for i in range(steps+1):
        t=i/steps
        theta=t*loops*2*math.pi
        rho=0.5+0.5*math.sin(t*math.pi)         # ice-disa-ice tek gecis spirali
        pts.append((theta,rho))
    return pts

write_thr("spiral_rose.thr", spiral_rose())
write_thr("classic.thr", classic())
