#!/usr/bin/env python3
# JLCPCB uretim paketi: Gerber zip + BOM.csv + CPL.csv (pick&place).
# Onkosul: jlcpcb/pos_raw.csv (kicad-cli pcb export pos) + final/gerbers/.
# Calistir: python3 make_jlcpcb.py
import csv, os, zipfile, glob
HERE=os.path.dirname(os.path.abspath(__file__))
JL=os.path.join(HERE,"jlcpcb")

# SMD parcalar (JLCPCB SMT diziyor). ref: (value, footprint, LCSC, not)
# Not: LCSC kodlari/stoklari degisir -> JLCPCB yuklemede DOGRULA.
SMD={
 "R1":("330",  "0805","C17630",""),
 "R2":("100k", "0805","C17407",""),
 "R3":("10k",  "0805","C17414",""),
 "R4":("1k",   "0805","C17513",""),
 "C2":("100nF","0805","C49678",""),
 "C3":("100nF","0805","C49678",""),
 "C5":("100nF","0805","C49678",""),
 "C7":("100nF","0805","C49678",""),
 "C8":("100nF","0805","C49678",""),
 "U2":("74AHCT1G125","SOT-23-5","DOGRULA","3.3->5V level shifter; JLCPCB kutuphanesinden sec"),
 "Q1":("AO3401A","SOT-23","C15127","P-FET ters polarite (Vgs +-12V, 12V'de zener clamp sart)"),
 "D1":("BZT52C10 10V","SOD-323","DOGRULA","Vgs zener clamp; MMSZ5240/BZT52C10 sec"),
 "F1":("PTC 3A","1206","DOGRULA","resettable fuse; akima gore sec"),
}
# Elle lehimlenecek (THT/modul; JLCPCB SMT'ye girmez) -> README'de
HAND={
 "U1L":"ESP32-DevKitC soketi (1x15)","U1R":"ESP32-DevKitC soketi (1x15)",
 "A1":"TMC2209 modul soketi (2x08)","A2":"TMC2209 modul soketi (2x08)",
 "BK1":"buck modul soketi (1x04)",
 "J1":"klemens 2p (12V)","J2":"klemens 4p (theta motor)","J3":"klemens 4p (rho motor)",
 "J4":"klemens 3p (LED)","J5":"klemens 3p (endstop)",
 "C1":"1000uF/16V elektrolitik (THT)","C6":"100uF/25V elektrolitik (THT)",
}

# pos oku
pos={}
with open(os.path.join(JL,"pos_raw.csv")) as f:
    for r in csv.DictReader(f):
        pos[r["Ref"]]=r

# CPL (JLCPCB: Designator, Mid X, Mid Y, Layer, Rotation)
with open(os.path.join(JL,"CPL_jlcpcb.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["Designator","Mid X","Mid Y","Layer","Rotation"])
    n=0
    for ref in SMD:
        if ref in pos:
            p=pos[ref]; w.writerow([ref,f'{float(p["PosX"]):.3f}',f'{float(p["PosY"]):.3f}',
                                    p["Side"].capitalize(),f'{float(p["Rot"]):.0f}']); n+=1
print("CPL_jlcpcb.csv ->",n,"SMD parca")

# BOM (JLCPCB: Comment, Designator, Footprint, LCSC Part #)  -> ayni LCSC'leri grupla
groups={}
for ref,(val,fp,lcsc,note) in SMD.items():
    groups.setdefault((val,fp,lcsc),[]).append(ref)
with open(os.path.join(JL,"BOM_jlcpcb.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["Comment","Designator","Footprint","LCSC Part #"])
    for (val,fp,lcsc),refs in groups.items():
        w.writerow([val,",".join(sorted(refs)),fp,lcsc])
print("BOM_jlcpcb.csv ->",len(groups),"satir")

# Gerber zip
zp=os.path.join(JL,"gerbers_revB.zip")
with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
    for g in glob.glob(os.path.join(HERE,"final","gerbers","*")):
        z.write(g,os.path.basename(g))
print("gerbers_revB.zip ->",os.path.getsize(zp),"byte")
print("DOGRULA gereken LCSC:", [r for r,(v,fp,l,nt) in SMD.items() if l=="DOGRULA"])
