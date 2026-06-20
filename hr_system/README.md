# Hệ thống quản lý nhân sự thông minh (HR System)

Ứng dụng web quản lý nhân sự xây dựng bằng **Flask + SQLite**, là dự án tổng
hợp các kiến thức Python đã học (hàm, list, dict, vòng lặp, điều kiện) và mở
rộng sang web, cơ sở dữ liệu.

## Tính năng

- **Quản lý hồ sơ nhân viên** (CRUD): thêm, xem, sửa, xóa.
- **Tìm kiếm & lọc** theo mã, tên, email và phòng ban.
- **Tự động tính lương** (lương theo ngày công, phụ cấp, bảo hiểm 10.5%,
  thuế thu nhập cá nhân lũy tiến, lương net).
- **Xếp loại hiệu suất (KPI)**: Xuất sắc / Tốt / Đạt / Cần cải thiện
  (tương tự bài tập "xếp loại học sinh").
- **Bảng điều khiển thông minh**: tổng nhân viên, quỹ lương, lương trung
  bình, thống kê theo phòng ban, phân bố KPI, top nhân viên.

## Cấu trúc dự án

```
hr_system/
├── app.py            # Ứng dụng Flask, định nghĩa các route
├── database.py       # Tầng dữ liệu: kết nối & truy vấn SQLite (CRUD)
├── hr_logic.py       # Tầng nghiệp vụ: lương, thuế, KPI, thống kê
├── seed_data.py      # Nạp dữ liệu mẫu để chạy thử
├── requirements.txt  # Thư viện cần cài
├── templates/        # Giao diện HTML (Jinja2)
│   ├── base.html
│   ├── dashboard.html
│   ├── danh_sach.html
│   ├── chi_tiet.html
│   └── form.html
└── static/
    └── style.css     # Giao diện CSS
```

## Cách chạy

```bash
# 1. Cài thư viện
pip install -r requirements.txt

# 2. (Tùy chọn) Nạp dữ liệu mẫu
python seed_data.py

# 3. Chạy ứng dụng
python app.py
```

Mở trình duyệt tại **http://127.0.0.1:5000**

## Quy tắc tính lương (minh họa theo quy định Việt Nam)

| Khoản | Công thức |
|-------|-----------|
| Lương theo ngày công | `lương cơ bản × ngày công / 26` |
| Thu nhập gross | `lương theo ngày công + phụ cấp` |
| Bảo hiểm | `lương cơ bản × 10.5%` (BHXH 8% + BHYT 1.5% + BHTN 1%) |
| Giảm trừ gia cảnh | `11.000.000 + 4.400.000 × số người phụ thuộc` |
| Thuế TNCN | Lũy tiến từng phần (5% → 35%) |
| Lương net | `gross − bảo hiểm − thuế` |

> Các con số mang tính minh họa cho mục đích học tập.
