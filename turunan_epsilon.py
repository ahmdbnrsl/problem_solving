import math

class DualNumber:
    def __init__(self, real, dual=0.0):
        self.real = real
        self.dual = dual

    def __repr__(self):
        return f"Dual(val={self.real:.4f}, der={self.dual:.4f})"

    # --- Operasi Dasar ---
    def __add__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(self.real + other.real, self.dual + other.dual)

    def __sub__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(self.real - other.real, self.dual - other.dual)

    def __mul__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        # Product Rule: (uv)' = u'v + uv'
        return DualNumber(self.real * other.real, 
                          self.dual * other.real + self.real * other.dual)

    def __truediv__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        # Quotient Rule: (u/v)' = (u'v - uv') / v^2
        return DualNumber(self.real / other.real,
                          (self.dual * other.real - self.real * other.dual) / (other.real**2))

    def __pow__(self, n):
        # Power Rule: (u^n)' = n * u^(n-1) * u'
        # n di sini dianggap konstanta (angka biasa)
        return DualNumber(self.real**n, n * (self.real**(n-1)) * self.dual)

    # --- Fungsi-Fungsi Transendental (Static Methods) ---
    @staticmethod
    def sin(d):
        return DualNumber(math.sin(d.real), math.cos(d.real) * d.dual)

    @staticmethod
    def cos(d):
        return DualNumber(math.cos(d.real), -math.sin(d.real) * d.dual)

    @staticmethod
    def tan(d):
        return DualNumber(math.tan(d.real), (1 / math.cos(d.real)**2) * d.dual)

    @staticmethod
    def exp(d):
        return DualNumber(math.exp(d.real), math.exp(d.real) * d.dual)

    @staticmethod
    def log(d):
        return DualNumber(math.log(d.real), (1 / d.real) * d.dual)

    @staticmethod
    def sqrt(d):
        return d**0.5

    # --- Invers Trigonometri ---
    @staticmethod
    def asin(d):
        return DualNumber(math.asin(d.real), (1 / math.sqrt(1 - d.real**2)) * d.dual)

    @staticmethod
    def acos(d):
        return DualNumber(math.acos(d.real), (-1 / math.sqrt(1 - d.real**2)) * d.dual)

    @staticmethod
    def atan(d):
        return DualNumber(math.atan(d.real), (1 / (1 + d.real**2)) * d.dual)

# Memungkinkan operasi reflektif (misal: 5 + Dual)
DualNumber.__radd__ = DualNumber.__add__
DualNumber.__rmul__ = DualNumber.__mul__


# Definisi fungsi
def my_complex_func(x):
    return DualNumber.sin(x**2) + DualNumber.log(x) * DualNumber.sqrt(x)

# Hitung di x = 2
x_val = DualNumber(2, 1) # Turunan dx/dx = 1
result = my_complex_func(x_val)

print(f"Fungsi: sin(x^2) + ln(x) * sqrt(x)")
print(f"Hasil f(2)  : {result.real}")
print(f"Hasil f'(2) : {result.dual}")

# Masukkan class DualNumber yang sudah kita buat tadi di sini...

def gradient_descent(func, start_x, learning_rate=0.1, iterations=150):
    x = start_x
    
    print(f"Memulai pencarian dari x = {x}")
    print("-" * 30)
    
    for i in range(iterations):
        # 1. Bungkus x ke dalam DualNumber(x, 1) 
        # Ingat: angka 1 di bagian dual berfungsi sebagai 'dx/dx'
        x_dual = DualNumber(x, 1.0)
        
        # 2. Hitung nilai fungsi dan turunannya sekaligus
        result = func(x_dual)
        
        gradien = result.dual  # Ini adalah f'(x)
        nilai_f = result.real  # Ini adalah f(x)
        
        # 3. Update x: geser x ke arah yang berlawanan dengan gradien
        x = x - learning_rate * gradien
        
        if i % 5 == 0:
            print(f"Iterasi {i:2d}: x = {x:.4f}, f(x) = {nilai_f:.4f}, f'(x) = {gradien:.4f}")

    return x

# --- Uji Coba ---

# Fungsi yang ingin kita optimasi
def my_function(x):
    return x**2 - 10*x + 25

# Jalankan! Mulai dari x = 0
titik_minimum = gradient_descent(my_function, start_x=0.0)

print("-" * 30)
print(f"Hasil Akhir: Titik minimum ditemukan di x ≈ {titik_minimum:.8f}")
