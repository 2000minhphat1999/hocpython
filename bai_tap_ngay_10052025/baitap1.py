""" 1. In "Hello, World!" ra màn hình

   Viết chương trình in ra dòng chữ "Hello, World!". """


print("Hello, World!")


""" 2. Tính tổng hai số

   Nhập hai số từ bàn phím, tính tổng và in kết quả. """
SoThuNhat = int(input("nhap so thu Nhat:"))
SoThuHai = int(input("nhap so thu Hai:"))
print(f"Tổng của {SoThuNhat} và {SoThuHai} lầ { SoThuHai + SoThuNhat}")


""" 3. Chuyển đổi nhiệt độ  

   Viết chương trình chuyển đổi nhiệt độ từ độ Celsius sang độ Fahrenheit (công thức: F = C * 9/5 + 32). """



C = int(input("nhap so :"))
print( C * 9/5 + 32)

""" 4. Tính diện tích hình tròn  

   Nhập bán kính, tính diện tích hình tròn (công thức: S = π * r², sử dụng π = 3.14). """

PI = 3.14
r = int(input("nhap so :"))
print( PI * r  * r)


""" 5. Kiểm tra số chẵn/lẻ  

   Nhập một số nguyên, kiểm tra xem nó là chẵn hay lẻ. """  


n = int(input("nhap so :"))
if n % 2 == 0: 
    print(f"{n} là số chẵn")
else:
    print(f"{n} là số lẻ")