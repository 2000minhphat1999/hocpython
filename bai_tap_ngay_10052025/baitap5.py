""" 21. Đảo ngược chuỗi  
    Nhập một chuỗi, in ra chuỗi đảo ngược (ví dụ: "hello" → "olleh"). """

s = input("Nhập chuỗi: ")
reversed_s = ""
for ch in s:
    reversed_s = ch + reversed_s
print("Chuỗi đảo ngược:", reversed_s)



""" 22. Đếm nguyên âm/phụ âm  
    Đếm số nguyên âm (a, e, i, o, u) và phụ âm trong một chuỗi. """
 
s = input("Nhập chuỗi: ").lower()
vowels = set("aeiou")
count_vowel = 0
count_consonant = 0

for ch in s:
    if ch.isalpha():             # chỉ xét chữ cái
        if ch in vowels:
            count_vowel += 1
        else:
            count_consonant += 1

print(f"Số nguyên âm: {count_vowel}")
print(f"Số phụ âm: {count_consonant}")



"""23. Kiểm tra chuỗi palindrome  
    Kiểm tra xem một chuỗi có phải là palindrome không (ví dụ: "madam"). """

s = input("Nhập chuỗi: ").lower()
vowels = set("aeiou")
count_vowel = 0
count_consonant = 0

for ch in s:
    if ch.isalpha():             # chỉ xét chữ cái
        if ch in vowels:
            count_vowel += 1
        else:
            count_consonant += 1

print(f"Số nguyên âm: {count_vowel}")
print(f"Số phụ âm: {count_consonant}")


""" 24. Viết hoa chữ cái đầu  
    Viết hoa chữ cái đầu tiên của mỗi từ trong chuỗi (ví dụ: "hello world" → "Hello World")."""

s = input("Nhập chuỗi: ")
normalized = "".join(ch.lower() for ch in s if ch.isalnum())  # loại bỏ ký tự không phải chữ/số
if normalized == normalized[::-1]:
    print("Đây là chuỗi palindrome.")
else:
    print("Đây không phải chuỗi palindrome.")


""" 25. Tìm từ dài nhất  

    Tìm từ dài nhất trong một chuỗi. """
s = input("Nhập chuỗi: ")
words = s.split()                # tách theo khoảng trắng
capitalized = []
for w in words:
    if w:
        capitalized.append(w[0].upper() + w[1:].lower())
    else:
        capitalized.append(w)
result = " ".join(capitalized)
print("Kết quả:", result)
