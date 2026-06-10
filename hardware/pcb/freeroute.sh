#!/usr/bin/env bash
# ============================================================================
#  Tam Freerouting akisi: yerlesim -> DSN -> Freerouting -> SES -> final board
#  Gereksinim: KiCad 9 (~/Applications), Java 25 (JAVA env), Freerouting jar.
#    JAVA            : java 25 ikili yolu (vars: ~/jdk25/Contents/Home/bin/java)
#    FREEROUTING_JAR : freerouting jar (vars: /tmp/freerouting.jar)
# ============================================================================
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
KPY=~/Applications/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
KPP=~/Applications/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages
JAVA="${JAVA:-$HOME/jdk25/Contents/Home/bin/java}"
JAR="${FREEROUTING_JAR:-/tmp/freerouting.jar}"
export PYTHONPATH="$KPP"

echo "== 1) yerlesim board (controller.kicad_pcb) =="
"$KPY" -u "$HERE/build_kicad.py" 2>/dev/null | grep -E "net=|OK" || true

echo "== 2) DSN uret =="
"$KPY" -u "$HERE/make_dsn.py" 2>/dev/null | grep -E "DSN|sinyal"

echo "== 3) Freerouting (headless, Java 25) =="
"$JAVA" -jar "$JAR" -de "$HERE/controller.dsn" -do "$HERE/controller.ses" -mp 30 2>&1 \
  | grep -iE "unrouted|completed|session" | tail -4

echo "== 4) SES'i board'a uygula (fresh build + GND refill) =="
SES_FILE="$HERE/controller.ses" "$KPY" -u "$HERE/build_kicad.py" 2>/dev/null | grep -E "\[4\]|net=|OK"

echo "== 5) final Gerber + STEP + DRC =="
bash "$HERE/kicad_export.sh" >/tmp/fr_export.log 2>&1
"$KPY" - <<'PY'
import json,collections
d=json.load(open("hardware/pcb/final/drc.json")) if __import__('os').path.exists("hardware/pcb/final/drc.json") else json.load(open("final/drc.json"))
v=d.get("violations",[]); c=collections.Counter(x["type"] for x in v)
print("DRC: ihlal",len(v),"| ratsnest",len(d.get("unconnected_items",[])),"| short",c.get("shorting_items",0))
PY
echo "BITTI"
