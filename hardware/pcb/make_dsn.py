#!/usr/bin/env python3
# ============================================================================
#  controller.kicad_pcb -> Specctra DSN  (Freerouting girdisi)
#  pcbnew DSN export headless'ta False donduğu icin DSN'i geometriden uretiyoruz.
#  GND = B.Cu plane (router GND'yi atlar), sinyaller F/B.Cu'da via ile routlanir.
#  KiCad python ile calistir (bkz. freeroute.sh).
# ============================================================================
import os, sys
import pcbnew
from pcbnew import ToMM

HERE = os.path.dirname(os.path.abspath(__file__))
PCB  = os.path.join(HERE, "controller.kicad_pcb")
DSN  = os.path.join(HERE, "controller.dsn")
BW_um, BH_um = 100000, 75000          # 100x75 mm -> um
TRACK_um, CLR_um = 250, 220           # iz / clearance (DRC 0.2 uzerine pay)

def um(nm_val_mm):  # mm -> um (int)
    return int(round(nm_val_mm*1000))

def main():
    b = pcbnew.LoadBoard(PCB)
    b.BuildConnectivity()

    pads=[]   # (comp, pin, netname, x_mm, y_mm, lx_mm, ly_mm, kind, sx, sy)
    for fp in b.GetFootprints():
        ref=fp.GetReference()
        ox,oy = ToMM(fp.GetPosition().x), ToMM(fp.GetPosition().y)
        for p in fp.Pads():
            num=p.GetNumber()
            if not num: continue
            x,y = ToMM(p.GetPosition().x), ToMM(p.GetPosition().y)
            net=p.GetNetname()
            smd = (p.GetAttribute()==pcbnew.PAD_ATTRIB_SMD)
            sx,sy = ToMM(p.GetSizeX()), ToMM(p.GetSizeY())
            dia = 2*ToMM(p.GetBoundingRadius())
            kind = ("smd",sx,sy) if smd else ("rnd",dia,dia)
            pads.append((ref,num,net,x,y,x-ox,y-oy,kind))

    # padstack havuzu
    pstacks={}   # name -> dsn shape lines
    def pstack_for(kind):
        k,a,bsz=kind
        if k=="rnd":
            nm=f"PS_RND_{um(a)}"
            pstacks[nm]=[f'(shape (circle F.Cu {um(a)}))', f'(shape (circle B.Cu {um(a)}))']
        else:
            nm=f"PS_SMD_{um(a)}x{um(bsz)}"
            hx,hy=um(a)//2,um(bsz)//2
            pstacks[nm]=[f'(shape (rect F.Cu {-hx} {-hy} {hx} {hy}))']
        return nm

    # komponent -> image (pinler local koord)
    comps={}  # ref -> list[(pin, pstack, lx_um, ly_um)]
    for (ref,num,net,x,y,lx,ly,kind) in pads:
        ps=pstack_for(kind)
        comps.setdefault(ref,[]).append((num,ps,um(lx),um(ly)))
    comp_origin={}
    for fp in b.GetFootprints():
        comp_origin[fp.GetReference()]=(um(ToMM(fp.GetPosition().x)), um(ToMM(fp.GetPosition().y)))

    # network: net -> [(ref,pin)]
    nets={}
    for (ref,num,net,*_ ) in pads:
        if net: nets.setdefault(net,[]).append(f"{ref}-{num}")
    sig_nets={n:p for n,p in nets.items() if len(p)>=2}

    L=[]
    L.append('(pcb controller.dsn')
    L.append('  (parser (string_quote ") (space_in_quoted_tokens on) (host_cad "KiCad") (host_version "9.0.9"))')
    L.append('  (resolution um 1)')
    L.append('  (unit um)')
    # structure
    L.append('  (structure')
    L.append('    (layer F.Cu (type signal) (property (index 0)))')
    L.append('    (layer B.Cu (type signal) (property (index 1)))')
    L.append(f'    (boundary (rect pcb 0 0 {BW_um} {BH_um}))')
    # GND plane B.Cu (router GND'yi atlar)
    L.append(f'    (plane "N_GND" (polygon B.Cu 0 500 500 {BW_um-500} 500 {BW_um-500} {BH_um-500} 500 {BH_um-500}))')
    L.append('    (via "PS_VIA")')
    L.append(f'    (rule (width {TRACK_um}) (clearance {CLR_um}))')
    L.append('  )')
    # placement
    L.append('  (placement')
    for ref,(ox,oy) in comp_origin.items():
        L.append(f'    (component IMG_{ref} (place {ref} {ox} {oy} front 0))')
    L.append('  )')
    # library
    L.append('  (library')
    for ref,pins in comps.items():
        L.append(f'    (image IMG_{ref}')
        for (num,ps,lx,ly) in pins:
            L.append(f'      (pin {ps} {num} {lx} {ly})')
        L.append('    )')
    pstacks['PS_VIA']=['(shape (circle F.Cu 800))','(shape (circle B.Cu 800))']
    for nm,shapes in pstacks.items():
        L.append(f'    (padstack {nm}')
        for s in shapes: L.append(f'      {s}')
        L.append('      (attach off)')
        L.append('    )')
    L.append('  )')
    # network
    L.append('  (network')
    for net,pins in sig_nets.items():
        L.append(f'    (net "{net}"')
        L.append('      (pins '+' '.join(pins)+')')
        L.append('    )')
    L.append('    (class default (rule (width %d) (clearance %d))'%(TRACK_um,CLR_um))
    L.append('      '+' '.join('"%s"'%n for n in sig_nets))
    L.append('    )')
    L.append('  )')
    L.append('  (wiring')
    L.append('  )')
    L.append(')')
    open(DSN,"w").write("\n".join(L)+"\n")
    print(f"DSN yazildi: {DSN}  ({os.path.getsize(DSN)} byte)")
    print(f"sinyal net={len(sig_nets)} komponent={len(comps)} pad={len(pads)} (GND plane disinda)")

main()
