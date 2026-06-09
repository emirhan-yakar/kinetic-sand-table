// ============================================================================
//  Kinetik Kum Sanatı Masası — Parametrik Model (Polar / Theta-Rho)
//  Hedef: Yuvarlak Ø60 cm sehpa. OpenSCAD'de aç, parametreleri değiştir,
//  Render (F6) -> Export STL. Her ana parça ayrı modül; STL için altta seç.
//  Birim: mm
// ============================================================================

/* [Ana ölçüler] */
TABLE_DIAMETER   = 600;   // cam yüzey çapı
TABLE_HEIGHT     = 380;   // toplam masa yüksekliği (sehpa)
WALL             = 18;    // gövde et kalınlığı (MDF)
GLASS_THICK      = 6;     // temperli cam
SAND_DEPTH       = 8;     // kum tabakası (görsel)
LED_RING_H       = 14;    // LED halka yüksekliği

/* [Mekanizma] */
ARM_LENGTH       = (TABLE_DIAMETER/2) - 30;  // dönen kol uzunluğu (ρ menzili)
ARM_WIDTH        = 40;
ARM_THICK        = 12;
CARRIAGE         = 35;     // mıknatıs taşıyıcı
MAGNET_D         = 18;     // neodyum mıknatıs çapı
TURNTABLE_D      = 130;    // lazy-susan tabla çapı
NEMA             = 42.3;   // NEMA17 gövde

/* [Görünüm] */
SHOW_GLASS       = true;
SHOW_SAND        = true;
EXPLODE          = 0;      // 0 = montajlı, >0 patlatılmış görünüm (mm)
$fn              = 120;

// ----------------------------------------------------------------------------
//  RENK/MALZEME yardımcıları (sadece önizleme için)
// ----------------------------------------------------------------------------
module body_color()  color([0.18,0.13,0.10]) children();   // koyu ceviz ahşap
module metal()       color([0.75,0.75,0.78]) children();
module glassc()      color([0.7,0.85,0.9,0.18]) children();
module sandc()       color([0.86,0.78,0.62]) children();
module ledc()        color([0.2,0.6,1.0,0.9]) children();

// ----------------------------------------------------------------------------
//  1) GÖVDE (silindirik kabin + alt taban)
// ----------------------------------------------------------------------------
module enclosure() {
    body_color() difference() {
        cylinder(d=TABLE_DIAMETER, h=TABLE_HEIGHT);
        // iç boşluk
        translate([0,0,WALL])
            cylinder(d=TABLE_DIAMETER-2*WALL, h=TABLE_HEIGHT);
        // üst açıklık (cam oturma kademesi)
        translate([0,0,TABLE_HEIGHT-GLASS_THICK-2])
            cylinder(d=TABLE_DIAMETER-2*8, h=GLASS_THICK+4);
    }
}

// ----------------------------------------------------------------------------
//  2) NEMA17 step motor (basit gövde)
// ----------------------------------------------------------------------------
module nema17(shaft=24) {
    metal() {
        cube([NEMA,NEMA,40], center=true);
        translate([0,0,20]) cylinder(d=22, h=2);
        translate([0,0,20]) cylinder(d=5, h=shaft);
    }
}

// ----------------------------------------------------------------------------
//  3) DÖNEN TABLA + KOL + TAŞIYICI (polar mekanizma)
// ----------------------------------------------------------------------------
module turntable() {
    metal() cylinder(d=TURNTABLE_D, h=8);
}

module arm() {
    // ρ ekseni: kol + üstünde lineer ray + taşıyıcı
    color([0.3,0.3,0.32]) difference() {
        hull() {
            cylinder(d=ARM_WIDTH, h=ARM_THICK);
            translate([ARM_LENGTH,0,0]) cylinder(d=ARM_WIDTH*0.6, h=ARM_THICK);
        }
        // hafifletme kanalı
        translate([ARM_WIDTH/2,0,ARM_THICK-3])
            cube([ARM_LENGTH, 8, 6], center=false);
    }
}

module carriage(rho=0.6) {
    // rho: 0..1 kol üzerindeki konum
    x = ARM_LENGTH * rho;
    translate([x,0,ARM_THICK]) {
        color([0.1,0.1,0.1]) cube([CARRIAGE,CARRIAGE,10], center=true);
        // neodyum mıknatıs
        color([0.6,0.6,0.65])
            translate([0,0,8]) cylinder(d=MAGNET_D, h=6);
    }
}

module mechanism(theta=25, rho=0.65) {
    translate([0,0,WALL+10]) {
        // θ tahrik motoru (sabit, tabanda)
        translate([TABLE_DIAMETER/2-50,0,-5]) nema17();
        // dönen tabla + kol
        rotate([0,0,theta]) {
            turntable();
            translate([0,0,8]) arm();
            // ρ motoru kol ucunda (kabloları slip ring'den)
            translate([0,0,8]) rotate([0,0,0])
                translate([-ARM_WIDTH/2,0,0]) scale(0.7) nema17(12);
            translate([0,0,8]) carriage(rho);
        }
    }
}

// ----------------------------------------------------------------------------
//  4) LED HALKA (kenar aydınlatma)
// ----------------------------------------------------------------------------
module led_ring() {
    ledc() translate([0,0,TABLE_HEIGHT-GLASS_THICK-LED_RING_H])
        difference() {
            cylinder(d=TABLE_DIAMETER-2*10, h=LED_RING_H);
            translate([0,0,-1]) cylinder(d=TABLE_DIAMETER-2*16, h=LED_RING_H+2);
        }
}

// ----------------------------------------------------------------------------
//  5) KUM + CAM (görsel katmanlar)
// ----------------------------------------------------------------------------
module sand() if (SHOW_SAND)
    sandc() translate([0,0,TABLE_HEIGHT-GLASS_THICK-SAND_DEPTH])
        cylinder(d=TABLE_DIAMETER-2*14, h=SAND_DEPTH);

module glass() if (SHOW_GLASS)
    glassc() translate([0,0,TABLE_HEIGHT-GLASS_THICK])
        cylinder(d=TABLE_DIAMETER-2*6, h=GLASS_THICK);

// ----------------------------------------------------------------------------
//  MONTAJ
// ----------------------------------------------------------------------------
module assembly() {
    enclosure();
    mechanism(theta=25, rho=0.65);
    translate([0,0,EXPLODE*1]) led_ring();
    translate([0,0,EXPLODE*2]) sand();
    translate([0,0,EXPLODE*3]) glass();
}

// ====== ÇIKTI SEÇİMİ ======
// Tüm montaj önizleme:
assembly();

// STL için tek parça istersen üsttekini yorum satırı yap ve birini aç:
// enclosure();
// arm();
// carriage();
// led_ring();
