#!/usr/bin/env python3
# ============================================================================
#  Kinetik Kum Masasi - Kontrol Karti uretici (gerbonara, saf Python)
#  Cikti: tam Gerber seti + Excellon drill + katman SVG render'lari + netlist
#  Calistir:  python3 pcb_gen.py
#  KiCad GEREKTIRMEZ. Uretilen Gerber'lar JLCPCB/PCBWay'e dogrudan yuklenebilir.
# ============================================================================
import os, math
from gerbonara.rs274x import GerberFile
from gerbonara.excellon import ExcellonFile, ExcellonTool
from gerbonara import graphic_objects as go, apertures as ap
from gerbonara.utils import MM
from gerbonara import LayerStack

OUT = os.path.dirname(os.path.abspath(__file__))
GERB = os.path.join(OUT, "gerbers"); os.makedirs(GERB, exist_ok=True)
PLOT = os.path.join(OUT, "plots");   os.makedirs(PLOT, exist_ok=True)

# ---- kart parametreleri (mm) ----
BW, BH = 100.0, 75.0          # kart olculeri
TRACE_SIG, TRACE_PWR = 0.3, 0.6
VIA_CU, VIA_DR = 0.8, 0.4
PAD_CU, PAD_DR = 1.7, 1.0     # standart THT pin
TERM_CU, TERM_DR = 2.4, 1.3   # vidali klemens (5.08 pitch)
MASK_SWELL = 0.1

# ---- katman nesne listeleri ----
L = {k: [] for k in ("top_cu","bot_cu","top_mask","bot_mask","top_silk","bot_silk","edge")}
drills_pth, drills_npth = [], []          # (x,y,dia)
NETS = {}                                  # net -> list[(x,y)]
PADLABELS = []                             # (x,y,text) assembly drawing icin
OUTLINES = []                              # (x,y,w,h,label) silk + assembly
ALLPADS = []                               # (x,y,net,cu) tum THT padler (pour clearance icin)
SMDPADS = []                               # (x,y,net)
VIAS = []                                  # (x,y,net)

def net(name, x, y):
    NETS.setdefault(name, []).append((x, y))

# ---- pad / via primitifleri ----
def tht_pad(x, y, net_name=None, cu=PAD_CU, dr=PAD_DR, square=False):
    if square:
        L["top_cu"].append(go.Flash(x, y, ap.RectangleAperture(cu, cu, unit=MM), unit=MM))
        L["bot_cu"].append(go.Flash(x, y, ap.RectangleAperture(cu, cu, unit=MM), unit=MM))
        L["top_mask"].append(go.Flash(x, y, ap.RectangleAperture(cu+MASK_SWELL, cu+MASK_SWELL, unit=MM), unit=MM))
        L["bot_mask"].append(go.Flash(x, y, ap.RectangleAperture(cu+MASK_SWELL, cu+MASK_SWELL, unit=MM), unit=MM))
    else:
        for lay in ("top_cu","bot_cu"):
            L[lay].append(go.Flash(x, y, ap.CircleAperture(cu, unit=MM), unit=MM))
        for lay in ("top_mask","bot_mask"):
            L[lay].append(go.Flash(x, y, ap.CircleAperture(cu+MASK_SWELL, unit=MM), unit=MM))
    drills_pth.append((x, y, dr))
    ALLPADS.append((x, y, net_name, cu))
    if net_name: net(net_name, x, y)

def smd_pad(x, y, w, h, net_name=None):
    L["top_cu"].append(go.Flash(x, y, ap.RectangleAperture(w, h, unit=MM), unit=MM))
    L["top_mask"].append(go.Flash(x, y, ap.RectangleAperture(w+MASK_SWELL, h+MASK_SWELL, unit=MM), unit=MM))
    SMDPADS.append((x, y, net_name))
    if net_name: net(net_name, x, y)

def via(x, y, net_name=None):
    for lay in ("top_cu","bot_cu"):
        L[lay].append(go.Flash(x, y, ap.CircleAperture(VIA_CU, unit=MM), unit=MM))
    drills_pth.append((x, y, VIA_DR))
    VIAS.append((x, y, net_name))
    if net_name: net(net_name, x, y)

# ---- silk yardimcilari ----
def silk_rect(x, y, w, h, side="top"):
    lay = "top_silk" if side=="top" else "bot_silk"
    a = ap.CircleAperture(0.15, unit=MM)
    pts = [(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2),(x-w/2,y-h/2)]
    for (x1,y1),(x2,y2) in zip(pts, pts[1:]):
        L[lay].append(go.Line(x1,y1,x2,y2,a,unit=MM))

def silk_dot(x, y):
    L["top_silk"].append(go.Flash(x, y, ap.CircleAperture(0.5, unit=MM), unit=MM))

# ---- footprint: pin header / modul ----
def header(refx, refy, ncols, nrows, pitch, rowsp, nets_map, label,
           pin1=(0,0), term=False, body=None):
    """nets_map: {(col,row): netname}. Pad indeksleri sol-alttan."""
    cu, dr = (TERM_CU, TERM_DR) if term else (PAD_CU, PAD_DR)
    for c in range(ncols):
        for r in range(nrows):
            x = refx + c*(rowsp if ncols>1 else 0) if False else refx + c*pitch_or_row(c, ncols, pitch, rowsp)
    # basit: iki boyutlu izgara, x = col ekseni, y = row ekseni
    pads=[]
    for r in range(nrows):
        for c in range(ncols):
            x = refx + c*(rowsp if rowsp and ncols>1 else pitch)
            y = refy + r*pitch
            nm = nets_map.get((c,r))
            tht_pad(x, y, nm, cu=cu, dr=dr, square=(c==0 and r==0))
            pads.append((c,r,x,y,nm))
    # govde + pin1
    if body:
        bw,bh = body
        cx = refx + (rowsp if (rowsp and ncols>1) else pitch*(ncols-1))/2
        cy = refy + pitch*(nrows-1)/2
        silk_rect(cx, cy, bw, bh)
        OUTLINES.append((cx, cy, bw, bh, label))
        PADLABELS.append((cx, cy, label))
    silk_dot(refx-1.4, refy-1.4)
    return pads

def pitch_or_row(c, ncols, pitch, rowsp):
    return (rowsp if (rowsp and ncols>1) else pitch)

# ============================================================================
#  YERLESIM  (mm) -- bilesenler cevreye, ESP32 ortada
# ============================================================================
# --- U1: ESP32-DevKitC 30 pin (2x15), satir araligi 25.4mm ---
ESP_X, ESP_Y, P = 36.0, 16.0, 2.54
esp_nets = {
    # sol kolon (c=0)            sag kolon (c=1)
    (0,0):"N_3V3",  (1,0):"N_GND",
    (0,1):"N_EN_BTN",(1,1):"GPIO23",
    (0,5):"N_THDIR",(1,5):"N_THSTEP",   # gpio18 / gpio19
    (0,6):"N_RHDIR",(1,6):"N_RHSTEP",   # gpio5  / gpio21
    (0,7):"N_UART", (1,7):"N_UART_RX",  # gpio17 / gpio16
    (0,8):"N_EN",   (1,8):"N_ENDSTOP",  # gpio25 / gpio22
    (0,9):"N_LEDG", (1,4):"N_5V",       # gpio4  ; 5V pin
    (1,14):"N_GND",
}
header(ESP_X, ESP_Y, 2, 15, P, 25.4, esp_nets, "U1 ESP32",
       body=(28.0, 15*P+2))

# --- A1 (theta) ve A2 (rho) TMC2209 StepStick: 2x8, satir araligi 12.7mm ---
def stepstick(refx, refy, label, prefix, motor_conn):
    # sol kolon: EN,MS1,MS2,UART,STEP,DIR,VIO,GND ; sag: VM,GND,coilB-,coilB+,coilA-,coilA+,(2)
    nm = {
        (0,7):"N_EN", (0,6):"N_MS1", (0,5):"N_MS2", (0,4):"N_UART",
        (0,3):prefix+"STEP", (0,2):prefix+"DIR", (0,1):"N_5V", (0,0):"N_GND",
        (1,7):"N_12V",(1,6):"N_GND",
        (1,5):motor_conn+"_B2",(1,4):motor_conn+"_B1",
        (1,3):motor_conn+"_A2",(1,2):motor_conn+"_A1",
        (1,1):"N_GND",(1,0):"N_GND",
    }
    return header(refx, refy, 2, 8, P, 12.7, nm, label, body=(12.7+4, 8*P+1))

stepstick(8.0,  26.0, "A1 TMC(th)", "N_TH", "THM")
stepstick(78.0, 26.0, "A2 TMC(rh)", "N_RH", "RHM")

# --- BK1 buck 12V->5V : 1x4 (IN+ IN- OUT+ OUT-) ---
header(40.0, 64.0, 4, 1, P, P, {(0,0):"N_12V",(1,0):"N_GND",(2,0):"N_5V",(3,0):"N_GND"},
       "BK1 5V", body=(4*P+1, 5))

# --- J_PWR 12V girisi (2p klemens 5.08) ---
header(6.0, 64.0, 2, 1, 5.08, 5.08, {(0,0):"N_12V",(1,0):"N_GND"}, "J1 12V", term=True,
       body=(2*5.08+2, 7))

# --- J_THETA / J_RHO motor klemensleri (4p) ---
header(6.0, 8.0, 4, 1, 5.08, 5.08,
       {(0,0):"THM_A1",(1,0):"THM_A2",(2,0):"THM_B1",(3,0):"THM_B2"}, "J2 TH-MOT", term=True,
       body=(4*5.08+2,7))
header(74.0, 8.0, 4, 1, 5.08, 5.08,
       {(0,0):"RHM_A1",(1,0):"RHM_A2",(2,0):"RHM_B1",(3,0):"RHM_B2"}, "J3 RH-MOT (slipring)", term=True,
       body=(4*5.08+2,7))

# --- J_LED (3p: 5V DIN GND) + R1 330R(0805) + C1 1000uF ---
header(70.0, 64.0, 3, 1, 5.08, 5.08, {(0,0):"N_5V",(1,0):"N_LEDDIN",(2,0):"N_GND"},
       "J4 LED", term=True, body=(3*5.08+2,7))
smd_pad(60.0, 60.0, 1.3, 1.0, "N_LEDG"); smd_pad(62.0, 60.0, 1.3, 1.0, "N_LEDDIN")
silk_rect(61.0, 60.0, 4.0, 2.0); OUTLINES.append((61,60,4,2,"R1 330")); PADLABELS.append((61,62,"R1"))
tht_pad(52.0, 64.0, "N_5V"); tht_pad(52.0, 59.0, "N_GND")
silk_rect(52.0,61.5,11,11); OUTLINES.append((52,61.5,11,11,"C1 1000uF")); PADLABELS.append((52,68,"C1"))

# --- J_ENDSTOP (3p: 3V3 SIG GND) ---
header(40.0, 8.0, 3, 1, 5.08, 5.08, {(0,0):"N_3V3",(1,0):"N_ENDSTOP",(2,0):"N_GND"},
       "J5 ENDSTOP", term=True, body=(3*5.08+2,7))

# --- decoupling C2,C3 (0805) driver VIO/GND ---
for (cx, nm) in [(20.0,"A1d"),(90.0,"A2d")]:
    smd_pad(cx-1.0, 50.0, 1.3,1.0, "N_5V"); smd_pad(cx+1.0,50.0,1.3,1.0,"N_GND")
    silk_rect(cx,50.0,4,2)

# ============================================================================
#  KENAR + MONTAJ DELIKLERI
# ============================================================================
ea = ap.CircleAperture(0.15, unit=MM)
corners = [(0,0),(BW,0),(BW,BH),(0,BH),(0,0)]
for (x1,y1),(x2,y2) in zip(corners, corners[1:]):
    L["edge"].append(go.Line(x1,y1,x2,y2,ea,unit=MM))
for mx,my in [(4,4),(BW-4,4),(BW-4,BH-4),(4,BH-4)]:
    L["top_silk"].append(go.Flash(mx,my, ap.CircleAperture(6.5,unit=MM), unit=MM, polarity_dark=True))
    drills_npth.append((mx,my,3.2))

# ============================================================================
#  YONLENDIRME  (cakisma kontrollu greedy 2-katman)
# ============================================================================
def seg_cross(a, b):
    (x1,y1,x2,y2)=a; (x3,y3,x4,y4)=b
    def o(ax,ay,bx,by,cx,cy): return (by-ay)*(cx-bx)-(bx-ax)*(cy-by)
    d1=o(x3,y3,x4,y4,x1,y1); d2=o(x3,y3,x4,y4,x2,y2)
    d3=o(x1,y1,x2,y2,x3,y3); d4=o(x1,y1,x2,y2,x4,y4)
    if ((d1>0)!=(d2>0)) and ((d3>0)!=(d4>0)): return True
    return False

placed = {"top":[], "bot":[]}   # (net, x1,y1,x2,y2)
def try_seg(net_name, x1,y1,x2,y2, layer):
    for (n,a,b,c,d) in placed[layer]:
        if n==net_name: continue
        if seg_cross((x1,y1,x2,y2),(a,b,c,d)): return False
        # ayni nokta paylasimi (farkli net) = kisa devre
        for px,py in ((x1,y1),(x2,y2)):
            if abs(px-a)<0.2 and abs(py-b)<0.2: return False
            if abs(px-c)<0.2 and abs(py-d)<0.2: return False
    placed[layer].append((net_name,x1,y1,x2,y2))
    return True

def order_nn(pts):
    pts=list(pts); out=[pts.pop(0)]
    while pts:
        last=out[-1]
        j=min(range(len(pts)), key=lambda i:(pts[i][0]-last[0])**2+(pts[i][1]-last[1])**2)
        out.append(pts.pop(j))
    return out

routed, ratsnest = 0, []
power = {"N_5V","N_12V","N_3V3"}            # GND -> alt katman dolgu (router'a girmez)
BOT_TRACES = []                             # (x1,y1,x2,y2,w) pour clearance icin
order = sorted(NETS.items(), key=lambda kv: (kv[0] not in power, len(kv[1])))
for name, pts in order:
    if name == "N_GND" or len(pts)<2: continue
    pref = ["bot","top"] if name in power else ["top","bot"]
    w = TRACE_PWR if name in power else TRACE_SIG
    def lay_seg(layer,a,b,c,d):
        if layer=="top":
            L["top_cu"].append(go.Line(a,b,c,d, ap.CircleAperture(w,unit=MM), unit=MM))
        else:
            L["bot_cu"].append(go.Line(a,b,c,d, ap.CircleAperture(w,unit=MM), unit=MM))
            BOT_TRACES.append((a,b,c,d,w))
    chain = order_nn(pts)
    for (x1,y1),(x2,y2) in zip(chain, chain[1:]):
        done=False
        # 1) dogrudan iz
        for layer in pref:
            if try_seg(name,x1,y1,x2,y2,layer):
                lay_seg(layer,x1,y1,x2,y2); routed+=1; done=True; break
        # 2) L-seklinde (Manhattan) iki kose adayi
        if not done:
            for cx,cy in ((x2,y1),(x1,y2)):
                for layer in pref:
                    if try_seg(name,x1,y1,cx,cy,layer) and try_seg(name,cx,cy,x2,y2,layer):
                        lay_seg(layer,x1,y1,cx,cy); lay_seg(layer,cx,cy,x2,y2)
                        routed+=1; done=True; break
                if done: break
        if not done:
            ratsnest.append((name,x1,y1,x2,y2))   # KiCad'de tamamlanacak

# --- SMD GND padlerini alt GND dolgusuna baglamak icin via ekle ---
for (x,y,nm) in list(SMDPADS):
    if nm=="N_GND":
        via(x, y-0.0, "N_GND")  # ped uzerine via -> through-hole ile alt pour

# ============================================================================
#  ALT KATMAN GND DOLGUSU (ground plane, clearance'li)
#  Sira: dolgu(dark) -> clearance(clear) -> mevcut bot_cu pad/trace (dark)
# ============================================================================
GAP = 0.45
existing_bot = L["bot_cu"]; L["bot_cu"] = []
# 1) buyuk dolgu dikdortgeni (kenardan 0.6 icerde)
L["bot_cu"].append(go.Flash(BW/2, BH/2,
    ap.RectangleAperture(BW-1.2, BH-1.2, unit=MM), unit=MM, polarity_dark=True))
# 2) GND OLMAYAN padlerin etrafini ac (clear)
for (x,y,nm,cu) in ALLPADS:
    if nm!="N_GND":
        L["bot_cu"].append(go.Flash(x,y, ap.CircleAperture(cu+2*GAP, unit=MM), unit=MM, polarity_dark=False))
for (x,y,nm) in VIAS:
    if nm!="N_GND":
        L["bot_cu"].append(go.Flash(x,y, ap.CircleAperture(VIA_CU+2*GAP, unit=MM), unit=MM, polarity_dark=False))
# 3) GND olmayan alt traceler icin clearance kanali
for (x1,y1,x2,y2,w) in BOT_TRACES:
    L["bot_cu"].append(go.Line(x1,y1,x2,y2, ap.CircleAperture(w+2*GAP, unit=MM), unit=MM, polarity_dark=False))
# 4) montaj delikleri etrafi ac
for mx,my in [(4,4),(BW-4,4),(BW-4,BH-4),(4,BH-4)]:
    L["bot_cu"].append(go.Flash(mx,my, ap.CircleAperture(7.0, unit=MM), unit=MM, polarity_dark=False))
# 5) mevcut pad ve traceleri tekrar ciz (dark) -> GND padler dolguya kaynar
L["bot_cu"].extend(existing_bot)

# ratsnest'i ust silk'e ince kesik cizgi olarak isaretle (bakir DEGIL)
rn_ap = ap.CircleAperture(0.1, unit=MM)
for (n,x1,y1,x2,y2) in ratsnest:
    L["top_silk"].append(go.Line(x1,y1,x2,y2, rn_ap, unit=MM))

# ============================================================================
#  KAYDET: Gerber + Excellon
# ============================================================================
def write_gerber(objs, fname):
    gf = GerberFile(); gf.objects.extend(objs); gf.save(os.path.join(GERB, fname))

write_gerber(L["top_cu"],   "controller-F_Cu.gtl")
write_gerber(L["bot_cu"],   "controller-B_Cu.gbl")
write_gerber(L["top_mask"], "controller-F_Mask.gts")
write_gerber(L["bot_mask"], "controller-B_Mask.gbs")
write_gerber(L["top_silk"], "controller-F_Silkscreen.gto")
write_gerber(L["bot_silk"], "controller-B_Silkscreen.gbo")
write_gerber(L["edge"],     "controller-Edge_Cuts.gko")

ex = ExcellonFile()
for (x,y,d) in drills_pth:
    ex.objects.append(go.Flash(x,y, ExcellonTool(d, plated=True, unit=MM), unit=MM))
ex.save(os.path.join(GERB, "controller-PTH.drl"))
exn = ExcellonFile()
for (x,y,d) in drills_npth:
    exn.objects.append(go.Flash(x,y, ExcellonTool(d, plated=False, unit=MM), unit=MM))
exn.save(os.path.join(GERB, "controller-NPTH.drl"))

# ============================================================================
#  RENDER: her katman ayri SVG + kompozit ust/alt
# ============================================================================
def gf_of(objs):
    gf=GerberFile(); gf.objects.extend(objs); return gf

colors = {"top_cu":"#1f7a1f","bot_cu":"#b34700","top_mask":"#0b5", "bot_mask":"#0b5",
          "top_silk":"#ffffff","bot_silk":"#dddddd","edge":"#ffd000"}
for key, objs in L.items():
    if not objs: continue
    svg = gf_of(objs).to_svg(margin=3, fg=colors[key], bg="#101015")
    open(os.path.join(PLOT, f"{key}.svg"),"w").write(str(svg))

# --- montaj cizimi (assembly drawing): govde + refdes metinleri + pin1 ---
def assembly_svg(path):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{BW*4}" height="{BH*4}" '
         f'viewBox="-3 -3 {BW+6} {BH+6}" style="background:#0d1117">']
    s.append(f'<rect x="0" y="0" width="{BW}" height="{BH}" fill="none" stroke="#ffd000" stroke-width="0.3"/>')
    def Y(y): return BH-y
    for mx,my in [(4,4),(BW-4,4),(BW-4,BH-4),(4,BH-4)]:
        s.append(f'<circle cx="{mx}" cy="{Y(my)}" r="1.6" fill="#222" stroke="#888" stroke-width="0.2"/>')
    for (cx,cy,bw,bh,label) in OUTLINES:
        s.append(f'<rect x="{cx-bw/2}" y="{Y(cy)-bh/2}" width="{bw}" height="{bh}" '
                 f'fill="#16304a" stroke="#7fd4ff" stroke-width="0.2"/>')
    for (x,y,nm,cu) in ALLPADS:
        s.append(f'<circle cx="{x}" cy="{Y(y)}" r="{cu/2}" fill="#c8a23a"/>')
    for (x,y,nm) in SMDPADS:
        s.append(f'<rect x="{x-0.65}" y="{Y(y)-0.5}" width="1.3" height="1.0" fill="#c8a23a"/>')
    for (cx,cy,label) in PADLABELS:
        s.append(f'<text x="{cx}" y="{Y(cy)}" font-size="2.2" fill="#fff" '
                 f'text-anchor="middle" font-family="monospace">{label}</text>')
    s.append('</svg>')
    open(path,"w").write("\n".join(s))
assembly_svg(os.path.join(PLOT,"assembly.svg"))

# kompozit (LayerStack)
try:
    pth = ex; npth = exn
    stack = LayerStack(graphic_layers={
        ('top','copper'):gf_of(L["top_cu"]), ('bottom','copper'):gf_of(L["bot_cu"]),
        ('top','mask'):gf_of(L["top_mask"]), ('bottom','mask'):gf_of(L["bot_mask"]),
        ('top','silk'):gf_of(L["top_silk"]), ('bottom','silk'):gf_of(L["bot_silk"]),
        ('mechanical','outline'):gf_of(L["edge"]),
    }, drill_pth=pth, drill_npth=npth, board_name="controller")
    open(os.path.join(PLOT,"composite-top.svg"),"w").write(str(stack.to_svg(side_re='top', margin=3)))
    open(os.path.join(PLOT,"composite-bottom.svg"),"w").write(str(stack.to_svg(side_re='bottom', margin=3)))
    comp_ok=True
except Exception as e:
    comp_ok=False; comp_err=str(e)[:120]

# ============================================================================
#  NETLIST (KiCad pcbnew "Update from netlist" ile import edilebilir)
# ============================================================================
refs = {}
for (cx,cy,t) in PADLABELS:
    refs[t.split()[0]] = t
with open(os.path.join(OUT,"controller.net"),"w") as f:
    f.write("(export (version D)\n  (components\n")
    seen=set()
    for (cx,cy,t) in PADLABELS:
        r=t.split()[0]
        if r in seen: continue
        seen.add(r)
        f.write(f'    (comp (ref "{r}") (value "{t}"))\n')
    f.write("  )\n  (nets\n")
    for i,(name,pts) in enumerate(sorted(NETS.items()),1):
        f.write(f'    (net (code "{i}") (name "{name}")) ;; {len(pts)} pad\n')
    f.write("  )\n)\n")

# ============================================================================
#  RAPOR
# ============================================================================
total = routed + len(ratsnest)
print("="*60)
print(f"Kart: {BW:.0f}x{BH:.0f} mm, 2 katman")
print(f"Net sayisi      : {len(NETS)}")
print(f"PTH delik       : {len(drills_pth)}   NPTH: {len(drills_npth)}")
print(f"Yonlendirilen   : {routed}/{total} segment")
print(f"Ratsnest (KiCad): {len(ratsnest)} segment (ust silk'te kesik cizgi)")
print(f"Kompozit render : {'OK' if comp_ok else 'FALLBACK ('+comp_err+')'}")
print(f"Gerber  -> {GERB}")
print(f"Renders -> {PLOT}")
print(f"Netlist -> {os.path.join(OUT,'controller.net')}")
print("="*60)
