#!/usr/bin/env python3
# ============================================================================
#  TEKNIK CIZIM montaj kilavuzu (2D, olculu) -- 3D render DEGIL.
#  matplotlib PdfPages. -> MONTAJ_CIZIM.pdf
#  Olculer montaj_hesap.py / montaj.md ile tutarli (mm).
# ============================================================================
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,"MONTAJ_CIZIM.pdf")

# --- olculer (mm) ---
DRUM_D=600; CAM_D=552; WELL_D=540; SASI_D=520; H=467; BODY_H=147; LEG_H=320
LEG_PCD=420; FOOT=509
BLUE="#1769c8"; INK="#1a1a20"; GR="#888"

def titleblock(fig, title, page, total=4):
    ax=fig.add_axes([0.06,0.03,0.88,0.055]); ax.axis("off")
    ax.add_patch(Rectangle((0,0),1,1,fill=False,ec=INK,lw=1.2,transform=ax.transAxes))
    ax.plot([0.62,0.62],[0,1],color=INK,lw=1,transform=ax.transAxes)
    ax.plot([0.84,0.84],[0,1],color=INK,lw=1,transform=ax.transAxes)
    ax.text(0.02,0.62,"DEVRAN — Kinetik Kum Masası",fontsize=10,fontweight="bold",transform=ax.transAxes)
    ax.text(0.02,0.22,title,fontsize=8,color="#444",transform=ax.transAxes)
    ax.text(0.50,0.62,"Ölçüler: mm",fontsize=8,transform=ax.transAxes)
    ax.text(0.50,0.22,"Tolerans ±0.5 (aksi belirtilmedikçe)",fontsize=7,color="#444",transform=ax.transAxes)
    ax.text(0.64,0.62,f"DWG-{page:03d}",fontsize=8,fontweight="bold",color=BLUE,transform=ax.transAxes)
    ax.text(0.64,0.22,"3. açı izdüşüm",fontsize=7,color="#444",transform=ax.transAxes)
    ax.text(0.86,0.62,f"Sayfa {page}/{total}",fontsize=8,transform=ax.transAxes)
    ax.text(0.86,0.22,"Rev B · 2026",fontsize=8,color="#444",transform=ax.transAxes)
    ax.plot([0.48,0.48],[0,1],color=INK,lw=1,transform=ax.transAxes)

def dimh(ax,x0,x1,y,txt,off=0,tcol=INK):
    ax.annotate("",(x1,y),(x0,y),arrowprops=dict(arrowstyle="<->",color=BLUE,lw=.9))
    ax.text((x0+x1)/2,y+off+4,txt,ha="center",va="bottom",fontsize=7.5,color=tcol)
def dimv(ax,y0,y1,x,txt):
    ax.annotate("",(x,y1),(x,y0),arrowprops=dict(arrowstyle="<->",color=BLUE,lw=.9))
    ax.text(x+5,(y0+y1)/2,txt,ha="left",va="center",fontsize=7.5,color=INK,rotation=90)
def balloon(ax,x,y,n):
    ax.add_patch(Circle((x,y),11,fc=BLUE,ec="white",lw=1.2,zorder=5))
    ax.text(x,y,str(n),ha="center",va="center",color="white",fontsize=8,fontweight="bold",zorder=6)

pp=PdfPages(OUT)

# ====== SAYFA 1: PARCA LISTESI (BOM) ======
fig=plt.figure(figsize=(8.27,11.69))
fig.text(0.07,0.93,"MONTAJ — PARÇA LİSTESİ",fontsize=18,fontweight="bold")
fig.text(0.07,0.905,"Teknik çizim montaj kılavuzu · ölçüler dahil",fontsize=10,color="#555")
rows=[["No","Parça","Malzeme","Ölçü (mm)","Adet"],
 ["1","Temperli cam","low-iron temperli","Ø552 × 6","1"],
 ["2","Üst çerçeve (rim)","ceviz kaplama","Ø600 / Ø560 × 18","1"],
 ["3","Kum tepsisi + kum","Al/akrilik + kuvars","Ø540 × 50","1"],
 ["4","LED halka","WS2812B","Ø535 (60 LED)","1"],
 ["5","Gövde (drum)","ceviz kaplama kontrplak","Ø600 × 147","1"],
 ["6","Şasi plakası","Al 6082, 4mm","Ø520","1"],
 ["7","Dönen kol","Al, 5mm","320 × 40","1"],
 ["8","θ / ρ motor","NEMA17","42 × 42 × 34","2"],
 ["9","Ayak","masif ceviz","8° splay, L320","4"],
]
ax=fig.add_axes([0.07,0.12,0.86,0.74]); ax.axis("off")
t=ax.table(cellText=rows[1:],colLabels=rows[0],loc="upper center",cellLoc="left",
           colWidths=[0.07,0.30,0.27,0.24,0.08])
t.auto_set_font_size(False); t.set_fontsize(10); t.scale(1,1.9)
for (r,c),cell in t.get_celld().items():
    cell.set_edgecolor("#ccc")
    if r==0: cell.set_facecolor("#eaf1fb"); cell.set_text_props(fontweight="bold")
fig.text(0.07,0.085,"Genel ölçü: Ø600 × H467 mm · ayak PCD Ø420 · ayak ucu Ø509 (stabilite).",fontsize=9,color="#555")
titleblock(fig,"Parça listesi",1); pp.savefig(fig); plt.close(fig)

# ====== SAYFA 2: PATLATILMIS ELEVASYON (olculu) ======
fig=plt.figure(figsize=(8.27,11.69)); ax=fig.add_axes([0.05,0.12,0.9,0.8]); ax.set_aspect("equal"); ax.axis("off")
fig.text(0.07,0.94,"PATLATILMIŞ ELEVASYON (ön görünüş)",fontsize=15,fontweight="bold")
# parca: (no, etiket, cap, kalinlik)
parts=[(1,"Cam",CAM_D,6),(2,"Üst çerçeve",DRUM_D,18),(3,"Kum tepsisi + kum",WELL_D,50),
       (4,"LED halka",535,8),(5,"Gövde (drum)",DRUM_D,90),(6,"Şasi + mekanizma",SASI_D,55)]
y=0; GAP=46; ys=[]
for no,lbl,dia,t in parts:
    y-=t
    ax.add_patch(Rectangle((-dia/2,y),dia,t,fill=False,ec=INK,lw=1.4))
    balloon(ax,-dia/2-28,y+t/2,no)
    ax.text(dia/2+18,y+t/2,f"{lbl}  Ø{dia}×{t}",va="center",fontsize=8,color=INK)
    ys.append(y); y-=GAP
# ayaklar
yl=y-6
for sx in(-1,1):
    ax.plot([sx*LEG_PCD/2*0.5, sx*FOOT/2*0.5],[yl,yl-LEG_H*0.5],color=INK,lw=3)
balloon(ax,-FOOT/2*0.5-28,yl-LEG_H*0.25,9); ax.text(FOOT/2*0.5+14,yl-LEG_H*0.25,"Ayak ×4 · 8° · L320",va="center",fontsize=8)
# olculer
dimh(ax,-DRUM_D/2,DRUM_D/2,52,"Ø600"); dimh(ax,-CAM_D/2,CAM_D/2,ys[0]+30,"Ø552")
dimh(ax,-WELL_D/2,WELL_D/2,ys[2]-20,"Ø540 (kum havuzu)")
ax.text(0,82,"Montaj sırası: 6→3→4→2→1 (üst modül 8× N52 mıknatısla oturur) · ayaklar gövdeye 8° plaka",
        ha="center",fontsize=8,color="#555")
ax.set_xlim(-360,690); ax.set_ylim(yl-LEG_H*0.5-20,100)
titleblock(fig,"Patlatılmış elevasyon",2); pp.savefig(fig); plt.close(fig)

# ====== SAYFA 3: GENEL MONTAJ (on + ust, olculu) ======
fig=plt.figure(figsize=(8.27,11.69)); fig.text(0.07,0.94,"GENEL MONTAJ — ön + üst görünüş",fontsize=15,fontweight="bold")
# on gorunus
ax=fig.add_axes([0.07,0.55,0.86,0.34]); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((-DRUM_D/2,0),DRUM_D,BODY_H,fill=False,ec=INK,lw=1.5))   # govde
ax.add_patch(Rectangle((-CAM_D/2,BODY_H-6),CAM_D,6,fill=False,ec=GR,lw=1))       # cam
for sx in(-1,1):
    ax.plot([sx*LEG_PCD/2, sx*FOOT/2],[0,-LEG_H],color=INK,lw=4)
dimh(ax,-DRUM_D/2,DRUM_D/2,BODY_H+22,"Ø600")
dimv(ax,-LEG_H,BODY_H,DRUM_D/2+40,"H 467")
dimv(ax,0,BODY_H,-DRUM_D/2-40,"gövde 147")
ax.text(0,-LEG_H-25,"ayak 8° splay · PCD Ø420 · ucu Ø509",ha="center",fontsize=8,color="#555")
ax.autoscale_view()
# ust gorunus
ax2=fig.add_axes([0.07,0.13,0.86,0.36]); ax2.set_aspect("equal"); ax2.axis("off")
ax2.add_patch(Circle((0,0),DRUM_D/2,fill=False,ec=INK,lw=1.5))
ax2.add_patch(Circle((0,0),WELL_D/2,fill=False,ec=GR,lw=1))
ax2.add_patch(Circle((0,0),CAM_D/2,fill=False,ec=GR,lw=.8,ls=(0,(4,3))))
import math
for a in (45,135,225,315):
    x=LEG_PCD/2*math.cos(math.radians(a)); yv=LEG_PCD/2*math.sin(math.radians(a))
    ax2.add_patch(Circle((x,yv),9,fill=False,ec=BLUE,lw=1.2))
dimh(ax2,-DRUM_D/2,DRUM_D/2,DRUM_D/2+22,"Ø600")
dimh(ax2,-WELL_D/2,WELL_D/2,-DRUM_D/2-30,"Ø540 havuz")
ax2.annotate("Ø420 ayak PCD",(LEG_PCD/2*0.707,LEG_PCD/2*0.707),(120,180),
             fontsize=8,color=BLUE,arrowprops=dict(arrowstyle="->",color=BLUE))
ax2.autoscale_view(); titleblock(fig,"Genel montaj",3); pp.savefig(fig); plt.close(fig)

# ====== SAYFA 4: PARCA DETAY (sasi/kol/ayak, olculu) ======
fig=plt.figure(figsize=(8.27,11.69)); fig.text(0.07,0.94,"PARÇA DETAYLARI (ölçülü)",fontsize=15,fontweight="bold")
# sasi
ax=fig.add_axes([0.07,0.55,0.5,0.36]); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Şasi plakası (Al 4mm)",fontsize=9)
ax.add_patch(Circle((0,0),SASI_D/2,fill=False,ec=INK,lw=1.4))
ax.add_patch(Circle((0,0),45,fill=False,ec=GR,lw=1))
for a in (45,135,225,315):
    ax.add_patch(Circle((250*math.cos(math.radians(a)),250*math.sin(math.radians(a))),4,fill=False,ec=BLUE))
for sx in(-1,1):
    for sy in(-1,1): ax.add_patch(Circle((95+sx*15.5,sy*15.5),3,fill=False,ec=BLUE))
dimh(ax,-SASI_D/2,SASI_D/2,SASI_D/2+18,"Ø520")
ax.text(0,-SASI_D/2-30,"drum 4×M4@Ø500 · merkez Ø90 · NEMA17 31×31",ha="center",fontsize=7,color="#555")
ax.autoscale_view()
# kol
ax=fig.add_axes([0.6,0.6,0.36,0.28]); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Dönen kol (Al 5mm)",fontsize=9)
ax.add_patch(Rectangle((-30,-20),320,40,fill=False,ec=INK,lw=1.3))
for i in range(11): ax.add_patch(Circle((40+i*20,0),1.6,fill=False,ec=BLUE))
dimh(ax,-30,290,28,"320"); dimv(ax,-20,20,300,"40")
ax.autoscale_view()
# ayak plakasi
ax=fig.add_axes([0.07,0.16,0.32,0.3]); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Ayak plakası (4×)",fontsize=9)
ax.add_patch(Rectangle((-30,-30),60,60,fill=False,ec=INK,lw=1.3))
for sx in(-1,1):
    for sy in(-1,1): ax.add_patch(Circle((sx*18,sy*18),2.75,fill=False,ec=BLUE))
ax.add_patch(Circle((0,0),10,fill=False,ec=GR))
dimh(ax,-30,30,36,"60"); dimh(ax,-18,18,-40,"36 (M5)")
ax.autoscale_view()
fig.text(0.6,0.22,"Tam kesim dosyaları:\n docs/uretim/dxf/ (DXF + STEP)\n\nDelik konumları gerçek COTS\n parçalarla doğrulanmalı\n (MGN12, lazy-susan, slip ring).",fontsize=8.5,color="#444")
titleblock(fig,"Parça detayları",4); pp.savefig(fig); plt.close(fig)

pp.close()
print("MONTAJ_CIZIM.pdf yazildi:",os.path.getsize(OUT),"byte")
