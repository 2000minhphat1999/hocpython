""" 11. In số từ 1 đến N  
    Nhập số nguyên dương N, in các số từ 1 đến N. """
N = int(input("nhap số n: "))
if N%1 == 0: 
    for i in range(N): 
        print(i)


""" 12. Tính giai thừa  
Nhập số nguyên n, tính n! (ví dụ: 5! = 120). """
N = int(input("nhap số n: "))
if N%1 == 0: 
    for i in range(1, 11): 
        i = i * (i + 1)
print(i)

"""13 . In bảng cửu chương  
    In bảng cửu chương của một số được nhập từ bàn phím. """
N = int(input("nhap số n: "))
if N%1 == 0: 
    for i in range(1, 11): 
        print(f"{N} x {N} = {n * i}")

""" 14. Tính tổng các số chẵn  
    Tính tổng các số chẵn từ 1 đến N (N nhập từ bàn phím). """

N = int(input("nhập số N"))

first_even = 2 
last_even = 2 * (N//2)

count = N//2

total = count * (first_even + last_even)//2 

print(f"Tổng các số chẵn từ {first_even} đến {last_even} là {total}")

""" 15. Kiểm tra số nguyên tố  

    Nhập một số nguyên, kiểm tra xem nó có phải số nguyên tố không. """

def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
