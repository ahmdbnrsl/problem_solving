import math as m 

def calculate(tinggi_atap, sudut_antara):
    tinggi_atap /= 1000
    jarak_matahari = 149_600_000
    radius_bumi = 6_371
    waktu_rotasi = 23 * 60 * 60 + 56 * 60 + 4
    keliling_jarak_matahari = (jarak_matahari + radius_bumi) * 2 * m.pi
    
    theta = lambda t, d, r: 2 * (t/2 - m.asin(d/r * m.sin(t/2)))
    
    return  (theta(sudut_antara, radius_bumi + tinggi_atap, keliling_jarak_matahari)/360) / (1 / waktu_rotasi * 3600)

result = calculate(5, 45)
print(result)