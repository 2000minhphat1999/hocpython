""" 26. Viết hàm tính tổng  

    Viết hàm nhận vào hai số và trả về tổng của chúng. """

def add(a, b):
    """Trả về tổng của a và b."""
    return a + b

# Ví dụ sử dụng
x = float(input("Nhập số thứ nhất: "))
y = float(input("Nhập số thứ hai: "))
print("Tổng là:", add(x, y))


""" 27. Hàm kiểm tra số hoàn hảo  

    Số hoàn hảo là số bằng tổng các ước nhỏ hơn nó (ví dụ: 6 = 1 + 2 + 3). Viết hàm kiểm tra. """

def is_perfect(n):
    """Trả về True nếu n là số hoàn hảo."""
    total = 0
    for i in range(1, n):
        if n % i == 0:
            total += i
    return total == n

# Ví dụ sử dụng
num = int(input("Nhập số cần kiểm tra: "))
print(f"{num} là số hoàn hảo:", is_perfect(num))


""" 28. Hàm tính Fibonacci  

    Viết hàm trả về số Fibonacci thứ n (dùng đệ quy hoặc vòng lặp). """

def fib(n):
    """Trả về số Fibonacci thứ n (F0 = 0, F1 = 1)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Ví dụ sử dụng
n = int(input("Nhập n (chỉ số Fibonacci): "))
print(f"Số Fibonacci thứ {n} là {fib(n)}")


""" 29. Hàm tính lũy thừa  

    Viết hàm tính a^b (không dùng toán tử  hoặc hàm có sẵn). """

def power(a, b):
    """Tính a mũ b với b ≥ 0 (integer) bằng lặp nhân."""
    result = 1
    for _ in range(b):
        result *= a
    return result

# Ví dụ sử dụng
base = float(input("Nhập cơ số a: "))
exp  = int(input("Nhập số mũ b (nguyên ≥ 0): "))
print(f"{base}^{exp} =", power(base, exp))


""" 30. Hàm sắp xếp list  

    Viết hàm sắp xếp một list số nguyên theo thứ tự tăng dần (không dùng hàm có sẵn). """

def bubble_sort(lst):
    """Sắp xếp list tăng dần bằng thuật toán Bubble Sort."""
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

# Ví dụ sử dụng
data = [5, 2, 9, 1, 5, 6]
print("Trước:", data)
print("Sau sắp xếp:", bubble_sort(data.copy()))
