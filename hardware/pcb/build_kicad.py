#!/usr/bin/env python3
# ============================================================================
#  controller.kicad_pcb uretici  (KiCad 9 pcbnew API ile)
#  KiCad'in kendi python'u ile calistirilir (bkz. build_kicad.sh).
#  Standart kutuphane footprintleri + net atamasi + iz yonlendirme + GND zone.
# ============================================================================
import os, sys, math, re
import pcbnew   # not: CreateEmptyBoard 'create wxApp' assert'i basar; zararsiz, devam eder
from pcbnew import VECTOR2I, FromMM, ToMM

SES_FILE = os.environ.get("SES_FILE")   # ayarliysa greedy yerine Freerouting SES uygulanir

def parse_ses(txt):
    out=[]   # ("wire",net,layer,width_um,[(x,y)..]) / ("via",net,x,y)
    m=re.search(r'\(network_out\b', txt)
    body=txt[m.start():] if m else txt
    for nm in re.finditer(r'\(net\s+"([^"]+)"', body):
        name=nm.group(1); depth=0; p=nm.start()
        while p<len(body):
            if body[p]=='(':depth+=1
            elif body[p]==')':
                depth-=1
                if depth==0:break
            p+=1
        block=body[nm.start():p+1]
        for w in re.finditer(r'\(path\s+(\S+)\s+([0-9.]+)\s+([-0-9.\s]+?)\)', block):
            nums=[float(x) for x in w.group(3).split()]
            out.append(("wire",name,w.group(1).strip('"'),float(w.group(2)),
                        list(zip(nums[0::2],nums[1::2]))))
        for v in re.finditer(r'\(via\s+\S+\s+([-0-9.]+)\s+([-0-9.]+)', block):
            out.append(("via",name,float(v.group(1)),float(v.group(2))))
    return out

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPCB = os.path.join(HERE, "controller.kicad_pcb")
FPROOT = os.path.expanduser("~/Applications/KiCad.app/Contents/SharedSupport/footprints")
PS  = FPROOT+"/Connector_PinSocket_2.54mm.pretty"
TB  = FPROOT+"/TerminalBlock.pretty"
RES = FPROOT+"/Resistor_SMD.pretty"
CTH = FPROOT+"/Capacitor_THT.pretty"
CSM = FPROOT+"/Capacitor_SMD.pretty"
MH  = FPROOT+"/MountingHole.pretty"

BW, BH = 100.0, 75.0
WSIG, WPWR = 0.25, 0.5

# ---- bilesenler: (ref, lib, fpname, x, y, rot, {padnum: net}) ----
COMPONENTS = [
  # ESP32 -> iki 1x15 soket strip (25.4mm arali)
  ("U1L", PS, "PinSocket_1x15_P2.54mm_Vertical", 30.0, 12.0, 0, {
      "1":"N_3V3","2":"N_EN_BTN","6":"N_THDIR","7":"N_RHDIR","8":"N_UART","9":"N_EN","10":"N_LEDG"}),
  ("U1R", PS, "PinSocket_1x15_P2.54mm_Vertical", 55.4, 12.0, 0, {
      "1":"N_GND","5":"N_5V","6":"N_THSTEP","7":"N_RHSTEP","8":"N_UART_RX","9":"N_ENDSTOP","15":"N_GND"}),
  # TMC2209 theta -> 2x08 soket
  ("A1", PS, "PinSocket_2x08_P2.54mm_Vertical", 10.0, 20.0, 0, {
      "1":"N_GND","3":"N_5V","5":"N_THDIR","7":"N_THSTEP","9":"N_UART","11":"N_MS2","13":"N_MS1","15":"N_EN",
      "2":"N_GND","4":"N_GND","6":"THM_A1","8":"THM_A2","10":"THM_B1","12":"THM_B2","14":"N_GND","16":"N_12V"}),
  ("A2", PS, "PinSocket_2x08_P2.54mm_Vertical", 80.0, 20.0, 0, {
      "1":"N_GND","3":"N_5V","5":"N_RHDIR","7":"N_RHSTEP","9":"N_UART","11":"N_MS2","13":"N_MS1","15":"N_EN",
      "2":"N_GND","4":"N_GND","6":"RHM_A1","8":"RHM_A2","10":"RHM_B1","12":"RHM_B2","14":"N_GND","16":"N_12V"}),
  # buck 12->5
  ("BK1", PS, "PinSocket_1x04_P2.54mm_Vertical", 36.0, 56.0, 0, {
      "1":"N_12V","2":"N_GND","3":"N_5V","4":"N_GND"}),
  # klemensler (MaiXu 5.0mm generic)
  ("J1", TB, "TerminalBlock_MaiXu_MX126-5.0-02P_1x02_P5.00mm", 6.0, 60.0, 0, {"1":"N_12V","2":"N_GND"}),
  ("J2", TB, "TerminalBlock_MaiXu_MX126-5.0-04P_1x04_P5.00mm", 6.0, 6.0, 0, {
      "1":"THM_A1","2":"THM_A2","3":"THM_B1","4":"THM_B2"}),
  ("J3", TB, "TerminalBlock_MaiXu_MX126-5.0-04P_1x04_P5.00mm", 72.0, 6.0, 0, {
      "1":"RHM_A1","2":"RHM_A2","3":"RHM_B1","4":"RHM_B2"}),
  ("J4", TB, "TerminalBlock_MaiXu_MX126-5.0-03P_1x03_P5.00mm", 66.0, 60.0, 0, {
      "1":"N_5V","2":"N_LEDDIN","3":"N_GND"}),
  ("J5", TB, "TerminalBlock_MaiXu_MX126-5.0-03P_1x03_P5.00mm", 40.0, 6.0, 0, {
      "1":"N_3V3","2":"N_ENDSTOP","3":"N_GND"}),
  # pasifler
  ("R1", RES, "R_0805_2012Metric", 64.0, 47.0, 0, {"1":"N_LEDG","2":"N_LEDDIN"}),
  ("C1", CTH, "CP_Radial_D10.0mm_P5.00mm", 52.0, 47.0, 0, {"1":"N_5V","2":"N_GND"}),
  ("C2", CSM, "C_0805_2012Metric", 24.0, 42.0, 0, {"1":"N_5V","2":"N_GND"}),
  ("C3", CSM, "C_0805_2012Metric", 88.0, 42.0, 0, {"1":"N_5V","2":"N_GND"}),
]
MOUNT = [(4,4),(BW-4,4),(BW-4,BH-4),(4,BH-4)]

def main():
    P=lambda *a: (print(*a), sys.stdout.flush())
    P("[1] board")
    board = pcbnew.CreateEmptyBoard()

    # --- net'leri olustur ---
    netnames = set()
    for *_, nets in COMPONENTS:
        netnames.update(nets.values())
    netmap = {}
    for n in sorted(netnames):
        ni = pcbnew.NETINFO_ITEM(board, n)
        board.Add(ni); netmap[n] = ni
    P("[2] nets", len(netmap))

    # --- footprintleri yerlestir + net ata ---
    netpts = {}   # net -> [(x_mm,y_mm)]
    ALLPADS = []  # (x_mm, y_mm, netname|None, radius_mm) -> pour clearance + pad-aware routing
    for ref, lib, fpname, x, y, rot, nets in COMPONENTS:
        fp = pcbnew.FootprintLoad(lib, fpname)
        if fp is None:
            print("FOOTPRINT YOK:", lib, fpname); sys.exit(2)
        fp.SetReference(ref)
        fp.SetPosition(VECTOR2I(FromMM(x), FromMM(y)))
        if rot: fp.SetOrientationDegrees(rot)
        board.Add(fp)
        fp.Reference().SetVisible(False)   # silk gurultusunu azalt (etiketler assembly.svg'de)
        fp.Value().SetVisible(False)
        for pad in fp.Pads():
            num = pad.GetNumber()
            nm = nets.get(num)
            p = pad.GetPosition()
            r = ToMM(pad.GetBoundingRadius())
            ALLPADS.append((ToMM(p.x), ToMM(p.y), nm, r))
            if nm:
                pad.SetNet(netmap[nm])
                netpts.setdefault(nm, []).append((ToMM(p.x), ToMM(p.y)))
        P("   fp", ref, "ok")
    P("[3] footprints yerlesti, padler:", len(ALLPADS))

    # --- kenar (Edge.Cuts) dikdortgen ---
    rect = pcbnew.PCB_SHAPE(board)
    rect.SetShape(pcbnew.SHAPE_T_RECT)
    rect.SetStart(VECTOR2I(FromMM(0), FromMM(0)))
    rect.SetEnd(VECTOR2I(FromMM(BW), FromMM(BH)))
    rect.SetLayer(pcbnew.Edge_Cuts); rect.SetWidth(FromMM(0.15))
    board.Add(rect)

    # --- montaj delikleri ---
    for (mx,my) in MOUNT:
        h = pcbnew.FootprintLoad(MH, "MountingHole_3.2mm_M3")
        if h: h.SetPosition(VECTOR2I(FromMM(mx),FromMM(my))); board.Add(h)

    # --- yonlendirme (cakisma kontrollu, GND haric) ---
    def cross(a,b):
        (x1,y1,x2,y2)=a;(x3,y3,x4,y4)=b
        def o(ax,ay,bx,by,cx,cy):return (by-ay)*(cx-bx)-(bx-ax)*(cy-by)
        return ((o(x3,y3,x4,y4,x1,y1)>0)!=(o(x3,y3,x4,y4,x2,y2)>0)) and \
               ((o(x1,y1,x2,y2,x3,y3)>0)!=(o(x1,y1,x2,y2,x4,y4)>0))
    def pt_seg(px,py,a,b,c,d):
        dx,dy=c-a,d-b; L2=dx*dx+dy*dy
        t=0 if L2==0 else max(0,min(1,((px-a)*dx+(py-b)*dy)/L2))
        return math.hypot(px-(a+t*dx), py-(b+t*dy))
    placed={"F":[],"B":[]}
    OBST=list(ALLPADS)   # pad + via engelleri (x,y,net,r)
    def free(net,a,b,c,d,lay):
        # bu segment lay katmaninda baska netlerle cakisiyor mu?
        for (n,x1,y1,x2,y2) in placed[lay]:
            if n==net: continue
            if cross((a,b,c,d),(x1,y1,x2,y2)): return False
            for px,py in ((a,b),(c,d)):
                if (abs(px-x1)<0.2 and abs(py-y1)<0.2) or (abs(px-x2)<0.2 and abs(py-y2)<0.2): return False
        for (px,py,pn,pr) in OBST:
            if pn==net: continue
            if pt_seg(px,py,a,b,c,d) < pr + w/2 + 0.22: return False   # DRC clearance payi
        return True
    def free_pt(net,x,y):     # via/kose noktasi yabanci pad ustunde mi?
        for (px,py,pn,pr) in OBST:
            if pn==net: continue
            if math.hypot(px-x,py-y) < pr+0.3: return False
        return True
    def commit(net,a,b,c,d,lay): placed[lay].append((net,a,b,c,d))
    def nn(pts):
        pts=list(pts);out=[pts.pop(0)]
        while pts:
            l=out[-1];j=min(range(len(pts)),key=lambda i:(pts[i][0]-l[0])**2+(pts[i][1]-l[1])**2)
            out.append(pts.pop(j))
        return out
    LAYER={"F":pcbnew.F_Cu,"B":pcbnew.B_Cu}
    routed=rats=nvia=0
    power={"N_5V","N_12V","N_3V3"}
    BOT_TRACKS=[]; ROUTE_VIAS=[]
    def addtrack(net,a,b,c,d,lay,w):
        t=pcbnew.PCB_TRACK(board)
        t.SetStart(VECTOR2I(FromMM(a),FromMM(b))); t.SetEnd(VECTOR2I(FromMM(c),FromMM(d)))
        t.SetWidth(FromMM(w)); t.SetLayer(LAYER[lay]); t.SetNet(netmap[net]); board.Add(t)
        commit(net,a,b,c,d,lay)
        if lay=="B": BOT_TRACKS.append((a,b,c,d,w))
    def addvia(net,x,y):
        v=pcbnew.PCB_VIA(board); v.SetPosition(VECTOR2I(FromMM(x),FromMM(y)))
        v.SetDrill(FromMM(0.4)); v.SetWidth(FromMM(0.8)); v.SetNet(netmap[net]); board.Add(v)
        OBST.append((x,y,net,0.4)); ROUTE_VIAS.append((x,y,net))
    SES_APPLIED=False
    if SES_FILE and os.path.exists(SES_FILE):
        for it in parse_ses(open(SES_FILE).read()):
            if it[0]=="wire":
                _,name,layer,width,coords=it
                if name not in netmap: continue
                lay="F" if layer=="F.Cu" else "B"; w=max(0.2,width/1000.0)
                for (x1,y1),(x2,y2) in zip(coords,coords[1:]):
                    addtrack(name,x1/1000,y1/1000,x2/1000,y2/1000,lay,w); routed+=1
            else:
                _,name,x,y=it
                if name in netmap: addvia(name,x/1000,y/1000); nvia+=1
        SES_APPLIED=True
        P("[4] Freerouting SES uygulandi: iz_segment=",routed,"via=",nvia)
    for net in ([] if SES_APPLIED else sorted(netpts, key=lambda k:(k not in power, len(netpts[k])))):
        pts=netpts[net]
        if net=="N_GND" or len(pts)<2: continue
        pref=["B","F"] if net in power else ["F","B"]
        w=WPWR if net in power else WSIG
        chain=nn(pts)
        for (a,b),(c,d) in zip(chain,chain[1:]):
            done=False
            # 1) dogrudan (tek katman)
            for lay in pref:
                if free(net,a,b,c,d,lay): addtrack(net,a,b,c,d,lay,w);routed+=1;done=True;break
            # 2) L-route (tek katman)
            if not done:
                for cx,cy in ((c,b),(a,d)):
                    if not free_pt(net,cx,cy): continue
                    for lay in pref:
                        if free(net,a,b,cx,cy,lay) and free(net,cx,cy,c,d,lay):
                            addtrack(net,a,b,cx,cy,lay,w);addtrack(net,cx,cy,c,d,lay,w);routed+=1;done=True;break
                    if done:break
            # 3) L-route + via (bacaklar farkli katmanda)
            if not done:
                for cx,cy in ((c,b),(a,d)):
                    if not free_pt(net,cx,cy): continue
                    for l1,l2 in (("F","B"),("B","F")):
                        if free(net,a,b,cx,cy,l1) and free(net,cx,cy,c,d,l2):
                            addtrack(net,a,b,cx,cy,l1,w); addtrack(net,cx,cy,c,d,l2,w)
                            addvia(net,cx,cy); nvia+=1; routed+=1; done=True; break
                    if done:break
            if not done: rats+=1
    P("[4] yonlendirme: iz=",routed,"via=",nvia,"rats=",rats)

    # --- SMD GND pedleri icin via (alt GND plane'e baglanti) ---
    gnd = netmap["N_GND"]
    for (px,py,pn,pr) in ALLPADS:
        if pn=="N_GND" and pr<0.8:   # kucuk = SMD ped
            v=pcbnew.PCB_VIA(board); v.SetPosition(VECTOR2I(FromMM(px),FromMM(py)))
            v.SetDrill(FromMM(0.4)); v.SetWidth(FromMM(0.8)); v.SetNet(gnd); board.Add(v)

    # --- alt katman GND zone (ground plane), self-fill (ZONE_FILLER segfault workaround) ---
    GAP=0.6
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.B_Cu)
    zone.SetNetCode(gnd.GetNetCode())
    zone.SetIsRuleArea(False)
    poly = zone.Outline(); poly.NewOutline()
    for (px,py) in [(0.5,0.5),(BW-0.5,0.5),(BW-0.5,BH-0.5),(0.5,BH-0.5)]:
        poly.Append(VECTOR2I(FromMM(px),FromMM(py)))
    # clearance kurali fiziksel boslukdan (GAP, ~poligon yaklasimi) KUCUK olmali,
    # yoksa DRC "zone clearance" ihlali verir. Fiziksel boslugu GAP korur.
    zone.SetLocalClearance(FromMM(0.3)); zone.SetMinThickness(FromMM(0.25))

    def circle_sps(cx,cy,r,n=24):
        s=pcbnew.SHAPE_POLY_SET(); s.NewOutline()
        for k in range(n):
            a=2*math.pi*k/n
            s.Append(int(FromMM(cx+r*math.cos(a))), int(FromMM(cy+r*math.sin(a))))
        return s
    def seg_sps(a,b,c,d,half):
        dx,dy=c-a,d-b; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L*half,dx/L*half
        s=pcbnew.SHAPE_POLY_SET(); s.NewOutline()
        for (px,py) in [(a+nx,b+ny),(c+nx,d+ny),(c-nx,d-ny),(a-nx,b-ny)]:
            s.Append(int(FromMM(px)),int(FromMM(py)))
        return s
    # dolgu poligonu = dikdortgen - (yabanci pad/iz/montaj clearance'lari)
    fill=pcbnew.SHAPE_POLY_SET(); fill.NewOutline()
    for (px,py) in [(0.6,0.6),(BW-0.6,0.6),(BW-0.6,BH-0.6),(0.6,BH-0.6)]:
        fill.Append(int(FromMM(px)),int(FromMM(py)))
    for (px,py,pn,pr) in ALLPADS:
        if pn!="N_GND":
            fill.BooleanSubtract(circle_sps(px,py,pr+GAP))
    for (a,b,c,d,w) in BOT_TRACKS:
        fill.BooleanSubtract(seg_sps(a,b,c,d,w/2+GAP))
        fill.BooleanSubtract(circle_sps(a,b,w/2+GAP,12)); fill.BooleanSubtract(circle_sps(c,d,w/2+GAP,12))
    for (vx,vy,vn) in ROUTE_VIAS:
        if vn!="N_GND": fill.BooleanSubtract(circle_sps(vx,vy,0.4+GAP,12))
    for (mx,my) in MOUNT:
        fill.BooleanSubtract(circle_sps(mx,my,3.6))
    try: fill.Fracture(pcbnew.SHAPE_POLY_SET.PM_FAST)
    except Exception:
        try: fill.Fracture()
        except Exception: pass
    zone.SetFilledPolysList(pcbnew.B_Cu, fill); zone.SetIsFilled(True)
    board.Add(zone)
    board.BuildConnectivity()
    P("[5] GND plane self-fill tamam (clearance'li)")

    pcbnew.SaveBoard(OUTPCB, board)
    print(f"OK kaydedildi: {OUTPCB}")
    print(f"net={len(netnames)} footprint={len(COMPONENTS)} iz={routed} ratsnest={rats} zone=1(GND/B.Cu)")

main()
