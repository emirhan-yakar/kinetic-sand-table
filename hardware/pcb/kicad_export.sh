#!/usr/bin/env bash
# KiCad ile FINAL cikti: Gerber + Excellon drill + STEP 3D + PDF + DRC
# Onkosul: controller.kicad_pcb (build_kicad.py ile uretilir)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
PCB="$HERE/controller.kicad_pcb"

# kicad-cli'yi bul
CLI="$(command -v kicad-cli || true)"
for c in \
  "$HOME/Applications/KiCad.app/Contents/MacOS/kicad-cli" \
  /Applications/KiCad.app/Contents/MacOS/kicad-cli \
  /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli \
  "$HOME/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"; do
  [ -z "$CLI" ] && [ -x "$c" ] && CLI="$c"
done
[ -z "$CLI" ] && { echo "kicad-cli bulunamadi"; exit 1; }
echo "kicad-cli: $CLI"; "$CLI" version

OUT="$HERE/final"; mkdir -p "$OUT/gerbers"
echo "== Gerber =="
"$CLI" pcb export gerbers --no-protel-ext -o "$OUT/gerbers/" "$PCB"
echo "== Drill (Excellon) =="
"$CLI" pcb export drill --format excellon -o "$OUT/gerbers/" "$PCB"
echo "== STEP 3D =="
"$CLI" pcb export step --subst-models --no-dnp -o "$OUT/controller.step" "$PCB"
echo "== PDF (katmanlar) =="
"$CLI" pcb export pdf --layers F.Cu,F.Silkscreen,Edge_Cuts -o "$OUT/top.pdf" "$PCB"
"$CLI" pcb export pdf --layers B.Cu,Edge_Cuts -o "$OUT/bottom.pdf" "$PCB"
echo "== DRC =="
"$CLI" pcb drc --format json -o "$OUT/drc.json" "$PCB" || true
echo "BITTI -> $OUT"
ls -la "$OUT" "$OUT/gerbers"
