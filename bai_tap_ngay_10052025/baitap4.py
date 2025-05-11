""" 16. Tìm max/min trong list  

    Tạo một list số nguyên, tìm giá trị lớn nhất và nhỏ nhất. """

numbers = [5, 3, 9, 1, 7, 9, 2]

# Khởi tạo giả sử phần tử đầu là min và max
current_min = numbers[0]
current_max = numbers[0]

for x in numbers:
    if x < current_min:
        current_min = x
    if x > current_max:
        current_max = x

print(f"Giá trị nhỏ nhất: {current_min}")
print(f"Giá trị lớn nhất: {current_max}")


""" 17. Đảo ngược list  

    Đảo ngược các phần tử trong list (không dùng hàm có sẵn). """


orig = [1, 2, 3, 4, 5]
rev = []

# Lấy từ cuối về đầu
for i in range(len(orig) - 1, -1, -1):
    rev.append(orig[i])

print("Original:", orig)
print("Reversed:", rev)
##################################
lst = [1, 2, 3, 4, 5]
i, j = 0, len(lst) - 1
while i < j:
    lst[i], lst[j] = lst[j], lst[i]
    i += 1
    j -= 1

print("Reversed in-place:", lst)



""" 18. Tính tổng các phần tử chẵn  

    Tính tổng các phần tử chẵn trong list. """

nums = [4, 7, 2, 9, 10, 3]
total_even = 0

for x in nums:
    if x % 2 == 0:
        total_even += x

print(f"Tổng các phần tử chẵn: {total_even}")



""" 19. Xóa phần tử trùng lặp  

    Tạo một list mới từ list đã cho bằng cách xóa các phần tử trùng lặp. """

data = [3, 5, 3, 2, 5, 1, 2]
unique = []

for x in data:
    if x not in unique:
        unique.append(x)

print("Original:", data)
print("After removing duplicates:", unique)



""" 20. Tìm phần tử xuất hiện nhiều nhất  

    Tìm phần tử xuất hiện nhiều lần nhất trong list. """

items = [2, 3, 5, 3, 2, 3, 5, 2, 2]

# Đếm số lần xuất hiện bằng dict
counts = {}
for x in items:
    if x in counts:
        counts[x] += 1
    else:
        counts[x] = 1

# Tìm key có giá trị lớn nhất
most_item = None
most_count = 0
for x, cnt in counts.items():
    if cnt > most_count:
        most_count = cnt
        most_item  = x

print(f"Phần tử xuất hiện nhiều nhất: {most_item} (xuất hiện {most_count} lần)")
