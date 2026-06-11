#!/usr/bin/env python3
# ============================================================================
#  Kinetik Kum Masasi - montaj geometrisi hesabi + olculu cizim (SVG)
#  Tum kotalar/aci/PCD/delik koordinatlari hesaplanir; montaj_sheet.svg uretir.
#  Calistir: python3 montaj_hesap.py
# ============================================================================
import math, os
HERE=os.path.dirname(os.path.abspath(__file__))

# ---------- ANA PARAMETRELER (mm) ----------
D_OUT   = 600          # drum dis cap
WALL    = 18           # govde et (ceviz kaplama MDF)
H_DRUM  = 150          # drum yuksekligi
WELL_D  = 50           # kum havuzu derinligi
GLASS_T = 6            # temperli cam
LEG_LEN = 320          # ayak boyu (eksen)
LEG_SPLAY = 8          # ayak disa acilma acisi (derece)
LEG_PCD = 420          # ayak baglanti dairesi (cap)
N_LEG   = 4

# ---------- TUREV HESAPLAR ----------
R_OUT = D_OUT/2
D_WELL = D_OUT - 2*WALL - 24      # kum havuzu cap (cidardan icerde)
D_SAND = D_WELL - 24
D_GLASS = D_WELL + 12             # cam, havuz uzerine biner (rabbet)
spl = math.radians(LEG_SPLAY)
leg_vert = LEG_LEN*math.cos(spl)            # ayak dikey izdusumu
leg_out  = LEG_LEN*math.sin(spl)            # ayak ucu disa kacis
H_TABLE = leg_vert + H_DRUM                 # toplam masa yuksekligi
FOOT_PCD = LEG_PCD + 2*leg_out              # ayak ucu temas dairesi

# ust modul mıknatis tutucu
N_MAG_TOP = 8
MAG_TOP_PCD = D_OUT - 28        # rim icinde mıknatis dairesi
MAG = dict(D=20,H=3,grade="N52",pull_kgf=2.7)   # ust modul mıknatisi
MAG_BALL = dict(D=20,H=10,grade="N52",pull_kgf=9.0)  # bilye surucu

# ust modul agirligi (cam + cerceve) -> mıknatis SF
glass_kg = math.pi*(D_GLASS/2/1000)**2*(GLASS_T/1000)*2500
frame_kg = 0.6
top_kg = glass_kg+frame_kg
mag_hold = N_MAG_TOP*MAG["pull_kgf"]
SF = mag_hold/top_kg

# ---------- KISIM KOORDINATLARI ----------
def polar(pcd,deg): r=pcd/2; a=math.radians(deg); return (r*math.cos(a), r*math.sin(a))
leg_angles=[45+90*i for i in range(N_LEG)]
leg_pos=[polar(LEG_PCD,a) for a in leg_angles]
mag_pos=[polar(MAG_TOP_PCD,45*i) for i in range(N_MAG_TOP)]
# NEMA17 delik deseni (31mm kare, M3) - merkez motor
NEMA=31.0
nema_holes=[(NEMA/2*sx,NEMA/2*sy) for sx in(-1,1) for sy in(-1,1)]

def report():
    print("="*56)
    print("MONTAJ GEOMETRISI")
    print("="*56)
    print(f"Drum dis cap        : Ø{D_OUT} mm  (et {WALL} mm)")
    print(f"Kum havuzu          : Ø{D_WELL} mm, derinlik {WELL_D} mm")
    print(f"Kum yatagi          : Ø{D_SAND} mm")
    print(f"Temperli cam        : Ø{D_GLASS} mm x {GLASS_T} mm")
    print(f"Ayak                : {N_LEG} adet, boy {LEG_LEN} mm, splay {LEG_SPLAY}°")
    print(f"  ayak baglanti PCD : Ø{LEG_PCD} mm  (acilar {leg_angles})")
    print(f"  ayak ucu PCD      : Ø{FOOT_PCD:.0f} mm  (disa kacis {leg_out:.1f} mm)")
    print(f"  dikey izdusum     : {leg_vert:.1f} mm")
    print(f"TOPLAM MASA YUKSEK. : {H_TABLE:.0f} mm")
    print(f"Ust modul mıknatis  : {N_MAG_TOP}x {MAG['grade']} Ø{MAG['D']}x{MAG['H']} @ Ø{MAG_TOP_PCD} PCD")
    print(f"  ust modul agirlik : {top_kg:.2f} kg (cam {glass_kg:.2f})")
    print(f"  tutma kuvveti     : {mag_hold:.1f} kgf  -> guvenlik kat {SF:.1f}x")
    print(f"Bilye surucu mıknatis: {MAG_BALL['grade']} Ø{MAG_BALL['D']}x{MAG_BALL['H']} (~{MAG_BALL['pull_kgf']}kgf)")
    print(f"NEMA17 delik         : {NEMA}x{NEMA} kare, M3 (merkez Ø22 boşluk)")
    print("="*56)

# ---------- SVG OLCULU CIZIM ----------
def svg():
    W,Hh=1760,980; cx=W/2
    def L(x1,y1,x2,y2,c="#333",w=1,d=""): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" {d}/>'
    def T(x,y,s,sz=15,c="#111",anc="middle"): return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" fill="{c}" text-anchor="{anc}" font-family="Arial">{str(s).replace("&","ve")}</text>'
    def dim(x1,y,x2,txt):  # yatay olcu cizgisi
        return (L(x1,y,x2,y,"#0a6",1)+L(x1,y-4,x1,y+4,"#0a6",1)+L(x2,y-4,x2,y+4,"#0a6",1)+T((x1+x2)/2,y-6,txt,13,"#0a6"))
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" style="background:#fff">']
    s.append(T(cx,34,"KİNETİK KUM MASASI — MONTAJ SHEET (ölçüler mm)",20,"#111"))
    # ---- ON GORUNUS (sol) ----
    ox,oy=360,160; sc=0.62
    def fx(x): return ox+x*sc
    def fy(y): return oy+y*sc
    s.append(T(fx(-R_OUT),oy-40,"ÖN GÖRÜNÜŞ",15,"#06c","start"))
    # drum
    s.append(f'<rect x="{fx(-R_OUT):.1f}" y="{fy(0):.1f}" width="{D_OUT*sc:.1f}" height="{H_DRUM*sc:.1f}" fill="#e8d4b0" stroke="#5a3" stroke-width="0"/>'.replace("#5a3","#7a5a2a"))
    s.append(f'<rect x="{fx(-R_OUT):.1f}" y="{fy(0):.1f}" width="{D_OUT*sc:.1f}" height="{H_DRUM*sc:.1f}" fill="none" stroke="#7a5a2a" stroke-width="2"/>')
    # well + cam
    s.append(f'<rect x="{fx(-D_WELL/2):.1f}" y="{fy(0):.1f}" width="{D_WELL*sc:.1f}" height="{WELL_D*sc:.1f}" fill="#efe2c4" stroke="#9a7" stroke-width="1"/>')
    s.append(L(fx(-D_GLASS/2),fy(2),fx(D_GLASS/2),fy(2),"#39f",3))
    s.append(T(fx(0),fy(-6),"temperli cam Ø%d"%D_GLASS,12,"#39f"))
    # ayaklar
    for sgn in (-1,1):
        x0=sgn*LEG_PCD/2; x1=sgn*(LEG_PCD/2+leg_out)
        s.append(L(fx(x0),fy(H_DRUM),fx(x1),fy(H_DRUM+leg_vert),"#4a2",6).replace("#4a2","#6b4423"))
    # olcu: toplam yukseklik
    s.append(L(fx(R_OUT)+40,fy(0),fx(R_OUT)+40,fy(H_TABLE),"#0a6",1))
    s.append(T(fx(R_OUT)+54,fy(H_TABLE/2),"H=%d"%H_TABLE,13,"#0a6"))
    s.append(dim(fx(-R_OUT),fy(0)-14,fx(R_OUT),"Ø%d"%D_OUT))
    s.append(dim(fx(-LEG_PCD/2),fy(H_TABLE)+30,fx(LEG_PCD/2),"ayak PCD Ø%d"%LEG_PCD))
    s.append(dim(fx(-FOOT_PCD/2),fy(H_TABLE)+60,fx(FOOT_PCD/2),"ayak ucu Ø%d"%FOOT_PCD))
    # ayak aci
    s.append(T(fx(LEG_PCD/2+leg_out)+8,fy(H_DRUM+leg_vert/2),"%d° splay"%LEG_SPLAY,12,"#c30","start"))
    # ---- UST GORUNUS (sag) ----
    tx,ty=1300,470; ts=0.46
    def gx(x): return tx+x*ts
    def gy(y): return ty+y*ts
    s.append(T(tx,ty-R_OUT*ts-16,"ÜST GÖRÜNÜŞ (delik ve PCD)",15,"#06c"))
    s.append(f'<circle cx="{gx(0)}" cy="{gy(0)}" r="{R_OUT*ts:.1f}" fill="#f3e9d4" stroke="#7a5a2a" stroke-width="2"/>')
    s.append(f'<circle cx="{gx(0)}" cy="{gy(0)}" r="{D_WELL/2*ts:.1f}" fill="#efe2c4" stroke="#9a7" stroke-width="1"/>')
    s.append(f'<circle cx="{gx(0)}" cy="{gy(0)}" r="{D_SAND/2*ts:.1f}" fill="none" stroke="#cbb" stroke-width="1" stroke-dasharray="4 3"/>')
    # ayak baglanti delikleri (PCD)
    s.append(f'<circle cx="{gx(0)}" cy="{gy(0)}" r="{LEG_PCD/2*ts:.1f}" fill="none" stroke="#c30" stroke-width="1" stroke-dasharray="6 4"/>')
    for (x,y),a in zip(leg_pos,leg_angles):
        s.append(f'<rect x="{gx(x)-9}" y="{gy(y)-9}" width="18" height="18" fill="#fff" stroke="#c30" stroke-width="1.5"/>')
        s.append(T(gx(x),gy(y)+3,"A",10,"#c30"))
    s.append(T(gx(0),gy(LEG_PCD/2*ts)+16,"ayak PCD Ø%d (4× @45°,135°,225°,315°)"%LEG_PCD,11,"#c30"))
    # mıknatis daireleri
    s.append(f'<circle cx="{gx(0)}" cy="{gy(0)}" r="{MAG_TOP_PCD/2*ts:.1f}" fill="none" stroke="#06c" stroke-width="1" stroke-dasharray="3 3"/>')
    for (x,y) in mag_pos:
        s.append(f'<circle cx="{gx(x)}" cy="{gy(y)}" r="5" fill="#06c"/>')
    s.append(T(gx(0),gy(0)-MAG_TOP_PCD/2*ts-6,"8× N52 Ø20×3 mıknatıs @ Ø%d"%MAG_TOP_PCD,11,"#06c"))
    # merkez motor NEMA17 deseni
    for (x,y) in nema_holes:
        s.append(f'<circle cx="{gx(x)}" cy="{gy(y)}" r="3" fill="#111"/>')
    s.append(f'<circle cx="{gx(0)}" cy="{gy(0)}" r="{11*ts:.1f}" fill="none" stroke="#111" stroke-width="1"/>')
    s.append(T(gx(0),gy(0)+2,"NEMA17 31×31 M3",10,"#111"))
    s.append('</svg>')
    open(os.path.join(HERE,"montaj_sheet.svg"),"w").write("\n".join(s))
    print("montaj_sheet.svg yazildi")

report(); svg()
