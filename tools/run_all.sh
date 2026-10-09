python3 parse3.py q1 q2 q3 h1 h2 p1 p2 p3 l2 g1 g2 g2b g3 s1 m1 m2 m2b m3 >/dev/null 2>&1
python3 lit_add.py && python3 geo_add.py
for p in m1 m2 m2b m3; do python3 qcrop.py $p $p; done
python3 math_add.py
