#!/usr/bin/env bash
# التشغيل من أي مكان. بدون خيارات: يبني index.html و drive.html من الموجود.
# --art يعيد توليد source/a من art_raw   --snd يعيد توليد snd/ من snd_raw
set -e; cd "$(dirname "$0")"
for x in "$@"; do case $x in --art) python3 assets.py;; --snd) python3 snd.py;; esac; done
python3 build.py; python3 dbuild.py
V=$(grep -oE "awwal-v[0-9]+" ../sw.js); echo "built. sw cache = $V (زوده قبل النشر)"
