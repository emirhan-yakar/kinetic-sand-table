#!/usr/bin/env python3
# Mekanizma KESITI - profesyonel teknik kesit (matplotlib, taramali). -> mekanizma_kesit.png
import os, math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch
HERE=os.path.dirname(os.path.abspath(__file__))
INK="#1a1a20"; BLUE="#1769c8"; GRN="#1f8a4c"; GR="#9a9a9a"
W_WOOD="#7a5230"; W_AL="#c9cdd2"; W_SAND="#cdb277"; W_GLASS="#bcd6e6"; W_MOT="#5b6068"; W_MAG="#cf5247"

fig=plt.figure(figsize=(11.5,8.2)); ax=fig.add_axes([0.02,0.04,0.70,0.9]); ax.set_aspect("equal"); ax.axis("off")
fig.text(0.03,0.95,"MEKANİZMA KESİTİ — yan kesit (şematik, ölçüsüz)",fontsize=15,fontweight="bold",color=INK)
fig.text(0.03,0.915,"θ = dönen kol · ρ = taşıyıcı · bilye kumun altından mıknatısla sürüklenir",fontsize=10,color="#555")

def R(x0,y0,x1,y1,fc,hatch=None,ec=INK,lw=1.2,a=1):
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor=fc,edgecolor=ec,lw=lw,hatch=hatch,alpha=a))

# --- olculer (mm, kesit) ---
H=467; BODY=320; WO=300; WI=270; SAND_T=410; SAND_TOP=460; GLASS=461
# ayaklar (kesitte iki, egik)
for s in(-1,1):
    ax.add_patch(Polygon([(s*210,BODY),(s*224,BODY),(s*262,8),(s*248,8)],closed=True,facecolor=W_WOOD,edgecolor=INK,lw=1,hatch="////"))
# govde duvarlari (ahsap, tarali)
R(-WO,BODY,-WI,H,W_WOOD,"////"); R(WI,BODY,WO,H,W_WOOD,"////"); R(-WO,BODY,WO,BODY+14,W_WOOD,"////")
# cam
R(-276,GLASS,276,H,W_GLASS,None,ec=INK,lw=1)
# kum + tepsi
R(-WI,SAND_T,WI,SAND_TOP,W_SAND,"....",ec=INK,lw=.8)
R(-WI,406,WI,SAND_T,W_AL,None,ec=INK,lw=.8)   # tepsi tabani (Al)
# bilye
ax.add_patch(Circle((150,468),7,facecolor="#b9bcc2",edgecolor=INK,lw=1,zorder=6))

# ===== MEKANIZMA =====
mz=332
R(-258,340,258,346,W_AL,"\\\\\\\\")            # sasi plakasi (Al)
R(-72,346,72,356,W_AL,None,ec=INK,lw=1)         # lazy-susan / turntable
R(-14,346,14,392,W_AL,None,ec=INK,lw=1)         # slip ring (merkez)
R(-30,356,30,372,W_MOT,None,ec=INK,lw=1)        # buyuk theta kasnak
# theta motoru (offset, govde + boss + saft)
R(64,332,106,366,W_MOT,None,ec=INK,lw=1); R(74,366,96,372,W_MOT); R(82,372,88,386,W_MOT)
ax.text(85,328,"θ motor",fontsize=8,ha="center",va="top",color=INK)
# kol + MGN12 ray
R(-30,384,250,392,W_AL,None,ec=INK,lw=1)        # kol
R(0,392,250,398,W_MOT,None,ec=INK,lw=.8)        # MGN12 ray
# tasiyici + miknatis (rho=140)
R(140-26,398,140+26,412,W_AL,None,ec=INK,lw=1)  # MGN12H araba
R(140-12,412,140+12,420,W_MAG,None,ec=INK,lw=1) # miknatis
# rho motoru (kol ucu)
R(228,384,250,418,W_MOT,None,ec=INK,lw=1); R(234,418,244,424,W_MOT)
ax.text(239,380,"ρ motor",fontsize=8,ha="center",va="top",color=INK)

# --- aralik (gap) ---
ax.annotate("",(166,420),(166,406),arrowprops=dict(arrowstyle="<->",color=BLUE,lw=1))
ax.text(172,413,"aralık ~4–6 mm",fontsize=8,color=BLUE,va="center")
# --- theta donme oku ---
ax.add_patch(FancyArrowPatch((-34,378),(34,378),connectionstyle="arc3,rad=-0.55",arrowstyle="-|>",mutation_scale=14,color=BLUE,lw=1.6))
ax.text(0,366,"θ",fontsize=15,color=BLUE,ha="center",fontweight="bold")
# --- rho ok ---
ax.annotate("",(244,406),(20,406),arrowprops=dict(arrowstyle="-|>",color=GRN,lw=1.6))
ax.text(130,400,"ρ",fontsize=15,color=GRN,ha="center",fontweight="bold")

ax.set_xlim(-340,300); ax.set_ylim(-10,500)

# ===== sag etiket sutunu (leader) =====
labels=[(276,464,"Temperli cam üst modül (mıknatıslı)"),(150,460,"Kum + çelik bilye Ø12"),
 (200,408,"Kum tepsisi (Al/akrilik ≤4mm — ferromanyetik DEĞİL)"),(152,418,"N52 mıknatıs"),
 (166,405,"Taşıyıcı (MGN12H araba)"),(250,395,"MGN12 ray (ρ ekseni)"),(250,388,"Dönen kol (Al)"),
 (239,400,"ρ motoru (NEMA17, kolda)"),(72,351,"Lazy-susan / turntable yatağı (θ)"),
 (14,360,"Slip ring (ρ motor+endstop kablosu)"),(30,364,"θ büyük kasnak (3:1)"),
 (258,343,"Şasi plakası (Al 4mm)"),(300,400,"Ahşap gövde (drum)"),(262,40,"Ayaklar (4×, 8°)")]
import numpy as np
lx=0.74; ax2=fig.add_axes([0,0,1,1]); ax2.axis("off")
# eksen->figure donusumu icin display->axes2 transform
fig.canvas.draw()
ly=0.90
for (hx,hy,t) in labels:
    px,py=ax.transData.transform((hx,hy)); fx,fy=fig.transFigure.inverted().transform((px,py))
    ax2.plot([fx,lx-0.008],[fy,ly+0.006],color="#cfcfd6",lw=.7,transform=fig.transFigure)
    ax2.add_patch(Circle((fx,fy),0.004,color=BLUE,transform=fig.transFigure))
    fig.text(lx,ly,t,fontsize=8.6,color=INK,va="center")
    ly-=0.045
# cozunurluk kutusu
fig.text(lx,0.20,"ÇÖZÜNÜRLÜK",fontsize=10,color=BLUE,fontweight="bold")
for i,t in enumerate(["θ: 3:1 redüksiyon → 26.667 step/derece (~0.16mm @R250)",
                      "ρ: GT2 20T → 80 step/mm (0.0125mm)","Tahrik: 2× NEMA17 + TMC2209"]):
    fig.text(lx,0.165-i*0.028,t,fontsize=8,color="#444")

fig.savefig(os.path.join(HERE,"mekanizma_kesit.png"),dpi=140,facecolor="white")
print("mekanizma_kesit.png yazildi")
