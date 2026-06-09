// ============================================================================
//  Kontrol Karti - 3D dizgi modeli (populated PCB)
//  pcb_gen.py ile ayni yerlesim. OpenSCAD'de Render (F6) -> Export STL.
//  Birim: mm
// ============================================================================
BW = 100; BH = 75; TH = 1.6;        // kart olculeri (pcb_gen.py ile ayni)
$fn = 48;

module pcb() {
    color([0.05,0.35,0.12]) difference() {              // FR4 yesil
        linear_extrude(TH) offset(r=2) offset(r=-2)
            square([BW,BH]);
        for (p=[[4,4],[BW-4,4],[BW-4,BH-4],[4,BH-4]])
            translate([p[0],p[1],-1]) cylinder(d=3.2,h=TH+2);
    }
    // bakir alt GND plane ipucu (ince katman)
    color([0.72,0.45,0.2]) translate([2,2,-0.05]) cube([BW-4,BH-4,0.05]);
}

// --- jenerik dik pin header / modul govdesi ---
module block(x,y,w,d,h,col) translate([x-w/2,y-d/2,TH]) color(col) cube([w,d,h]);
module pinrow(x,y,n,pitch=2.54,horiz=true)
    for(i=[0:n-1]) translate(horiz?[x+i*pitch,y,TH]:[x,y+i*pitch,TH])
        color([0.85,0.75,0.2]) cylinder(d=0.6,h=4);

module esp32()    { block(36+12.7,16+15*2.54/2-1.27, 28,40, 13,[0.1,0.1,0.12]);
                    color([0.8,0.8,0.85]) block(36+12.7,16+38, 16,18,2,[0.8,0.8,0.85]); } // anten
module stepstick(x,y,c){ block(x+6.35,y+8.9, 16,21, 3,[0.15,0.15,0.15]);
                    color([0.6,0.6,0.65]) translate([x+6.35-3,y+8.9,TH+3]) cube([6,6,5],center=true); } // surucu IC + heatsink
module buck(x,y)  block(x+3.8,y, 11,17,4,[0.05,0.05,0.4]);
module term(x,y,n){ block(x+(n-1)*5.08/2,y, n*5.08+2,8,9,[0.1,0.25,0.6]); }  // mavi vidali klemens
module ecap(x,y)  translate([x,y,TH]) color([0.1,0.1,0.12]) cylinder(d=10,h=12);
module smd(x,y)   block(x,y,3,1.6,0.6,[0.1,0.1,0.1]);

module assembly() {
    pcb();
    esp32();
    stepstick(8,26,"th"); stepstick(78,26,"rh");
    buck(40,64);
    term(6,64,2);                 // J1 12V
    term(6,8,4); term(74,8,4);    // J2/J3 motor
    term(70,64,3);                // J4 LED
    term(40,8,3);                 // J5 endstop
    ecap(52,61.5);                // C1
    smd(61,60);                   // R1
    smd(20,50); smd(90,50);       // C2,C3
}
assembly();
