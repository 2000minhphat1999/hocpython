""" 6. Tìm số lớn nhất  

   Nhập 3 số nguyên, tìm và in ra số lớn nhất. """

a = int(input("Nhập số a: "))
b = int(input("Nhập số b: "))
c = int(input("Nhập số c: "))

if a%1 == 0 and b%1 == 0 and c%1 == 0: 
    if a>b:
        if a>c: 
            print(f"số lớn nhất là {a}")
        else: 
            print(f"số lớn nhất là {c}")
    else:
        if b>c:
            print(f"số lớn nhất là {b}")
        else: 
            print(f"số lớn nhất là {c}")




""" 7. Giải phương trình bậc 1  

   Giải phương trình ax + b = 0 với a và b nhập từ bàn phím. """

a = float(input("nhap so a: "))
b = float(input("nhap so b: "))

match (a,b):
    case(0, 0): 
        print("phương trình có vô số nghiệm")
    case(0, _): 
        print("phương trình có vô số nghiệm")
    case(_, _):
        print(f"phương trình có nghiệm là x = {-b/a}")


""" 8. Xếp loại học sinh  

   Nhập điểm trung bình, xếp loại:  

    Giỏi nếu điểm ≥ 8  

    Khá nếu 6.5 ≤ điểm < 8  

    Trung bình nếu 5 ≤ điểm < 6.5  

    Yếu nếu điểm < 5. """

p = float(input("nhap so điểm: "))

match (p):
    case p if p>=8: 
        print("Xếp loại: Giỏi ")
    case p if 6.5 <= p <8: 
        print("Xếp loại: Khá ")
    case p if 5 <= p < 6.5:
        print(f"Xếp loại: Trung bình")
    case _: 
        print(f"Xếp loại: Yếu")



""" 9. Kiểm tra năm nhuận  

   Nhập một năm, kiểm tra xem đó có phải năm nhuận không (năm nhuận chia hết cho 4 nhưng không chia hết cho 100, hoặc chia hết cho 400). """
year = int(input("Nhập năm: "))

match year:
    case y if y % 400 == 0:
        print(f"{y} là năm nhuận.")
    case y if y % 100 == 0:
        print(f"{y} không phải là năm nhuận.")
    case y if y % 4 == 0:
        print(f"{y} là năm nhuận.")
    case _:
        print(f"{year} không phải là năm nhuận.")






""" 10. Tính tiền taxi  

    Biết giá mở cửa là 15,000đ cho 1km đầu. Từ km thứ 2 đến km thứ 5: 13,500đ/km. Từ km thứ 6 trở đi: 11,000đ/km. Tính tiền taxi dựa trên số km nhập vào. """
# Nhập số km đã đi
km = float(input("Nhập số km đã đi: "))

# Tính tiền taxi
match km:
    case km if km <= 0:
        print("Số km không hợp lệ.")
    case km if km <= 1:
        fare = 15000
        print(f"Tiền taxi: {fare:,.0f}đ")
    case km if km <= 5:
        fare = 15000 + (km - 1) * 13500
        print(f"Tiền taxi: {fare:,.0f}đ")
    case _:
        fare = 15000 + 4 * 13500 + (km - 5) * 11000
        print(f"Tiền taxi: {fare:,.0f}đ")
