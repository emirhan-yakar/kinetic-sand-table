#!/usr/bin/env python3
# Her uretim MD dokumanini modern, standalone HTML sayfasina cevirir (icerik sayfada).
# Calistir: python3 build_site.py
import os, re, markdown
ROOT=os.path.dirname(os.path.abspath(__file__))
GH="https://github.com/emirhan-yakar/kinetic-sand-table"

# (md yolu, cikti html, baslik, indirilebilir PDF/dosya veya None)
PAGES=[
 ("docs/uretim/URETIM_DOSYASI.md","uretim-dosyasi.html","Üretim Gerçekleme Dosyası",None),
 ("docs/uretim/PCB_inceleme.md","pcb-inceleme.html","PCB Elektriksel İnceleme",None),
 ("docs/uretim/mekanizma_tasarim.md","mekanizma.html","Mekanizma Tasarımı",None),
 ("docs/uretim/elektrik_montaj.md","elektrik.html","Elektrik Montaj",[("Elektrik talimatı (PDF)","docs/uretim/ELEKTRIK_TALIMATI.pdf")]),
 ("docs/uretim/QA_kontrol_listesi.md","qa.html","QA / FCT Test Fişi",[("Elektrik+QA (PDF)","docs/uretim/ELEKTRIK_TALIMATI.pdf")]),
 ("docs/uretim/montaj.md","montaj.html","Materyal / Mekanik Montaj",[("Montaj kılavuzu (PDF)","docs/uretim/MONTAJ_KILAVUZU.pdf")]),
 ("docs/uretim/BOM_uretim.md","bom.html","BOM & Maliyet",None),
 ("docs/realizm_yol_haritasi.md","realizm.html","Gerçeklik Yol Haritası",None),
 ("docs/uretim/dxf/README.md","dxf.html","CNC / Lazer DXF + STEP",None),
 ("firmware/README.md","firmware.html","Firmware & Yazılım",[("FluidNC config","firmware/fluidnc_config.yaml")]),
]
MD2HTML={os.path.basename(m):h for m,h,_,_ in PAGES}  # *.md -> *.html eslemesi

def nav(active=""):
    L=[("index.html","Genel Bakış","ov"),("gorseller.html","Görseller","gor"),
       ("simulasyon.html","Simülasyon","sim"),("muhendislik.html","Mühendislik","muh")]
    items="".join(f'<a class="link{" active" if k==active else ""}" href="{u}">{t}</a>' for u,t,k in L)
    return (f'<nav class="nav"><div class="wrap">'
            f'<a class="brand" href="index.html">Kinetik Kum Masası <small>· üretim paketi</small></a>'
            f'{items}<a class="link" href="{GH}" target="_blank">GitHub ↗</a></div></nav>')
FOOT=(f'<footer><div class="wrap"><span>Kinetik Kum Sanatı Masası · üretim paketi</span>'
      f'<a href="{GH}">github.com/emirhan-yakar/kinetic-sand-table ↗</a></div></footer>')

def rewrite(html, md_dir):
    # rel src/href'leri koke gore duzelt; .md -> .html
    def fix(m):
        attr,val=m.group(1),m.group(2)
        if re.match(r'^(https?:|/|#|mailto:)',val): return m.group(0)
        base=val.split('#')[0]; frag=val[len(base):]
        if base in MD2HTML: return f'{attr}="{MD2HTML[base]}{frag}"'
        # rel yol -> kok gore
        p=os.path.normpath(os.path.join(md_dir,base)).replace("\\","/")
        return f'{attr}="{p}{frag}"'
    return re.sub(r'(src|href)="([^"]+)"', fix, html)

md=markdown.Markdown(extensions=['tables','fenced_code','sane_lists','attr_list','md_in_html'])
for mdpath,out,title,dls in PAGES:
    md_dir=os.path.dirname(mdpath)
    txt=open(os.path.join(ROOT,mdpath),encoding="utf-8").read()
    md.reset(); body=md.convert(txt)
    body=rewrite(body, md_dir)
    dlrow=""
    if dls:
        btns="".join(f'<a class="btn" href="{u}">⬇ {t}</a>' for t,u in dls)
        dlrow=f'<div class="dlrow">{btns}</div>'
    page=f'''<!DOCTYPE html><html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Kinetik Kum Masası</title>
<link rel="stylesheet" href="style.css"></head><body>
{nav("muh")}
<div class="wrap">
  <div class="dochead"><a class="back" href="muhendislik.html">← Mühendislik &amp; Üretim</a>{dlrow}</div>
  <article class="prose">{body}</article>
</div>
{FOOT}
</body></html>'''
    open(os.path.join(ROOT,out),"w",encoding="utf-8").write(page)
    print("yazildi:",out)
print("Bitti:",len(PAGES),"sayfa")
