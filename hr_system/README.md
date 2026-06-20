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

## Quy tắc tính lương (theo quy định Việt Nam, hiệu lực 2026)

| Khoản | Công thức |
|-------|-----------|
| Lương theo ngày công | `lương cơ bản × ngày công / 26` |
| Thu nhập gross | `lương theo ngày công + phụ cấp` |
| BHXH | `8% × min(lương, 46.800.000)` |
| BHYT | `1.5% × min(lương, 46.800.000)` |
| BHTN | `1% × min(lương, 20 × lương tối thiểu vùng)` |
| Giảm trừ gia cảnh | `15.500.000 + 6.200.000 × số người phụ thuộc` |
| Thuế TNCN | Lũy tiến từng phần (5% → 35%) |
| Lương net | `gross − bảo hiểm − thuế` |

### Căn cứ pháp lý áp dụng

- **Giảm trừ gia cảnh** 15,5tr (bản thân) / 6,2tr (mỗi người phụ thuộc):
  Nghị quyết 110/2025/UBTVQH15, hiệu lực từ kỳ tính thuế 2026.
- **Trần đóng BHXH/BHYT** = 20 × lương cơ sở (2.340.000đ) = 46.800.000đ.
- **Trần đóng BHTN** = 20 × lương tối thiểu vùng (Nghị định 293/2025/NĐ-CP):
  Vùng I 5.310.000đ · II 4.730.000đ · III 4.140.000đ · IV 3.700.000đ.
  Vùng doanh nghiệp đặt trong `hr_logic.VUNG_DOANH_NGHIEP` (mặc định Vùng I).

> Lưu ý: lấy lương cơ bản làm lương đóng bảo hiểm (giả định đơn giản hóa);
> phụ cấp được coi là thu nhập chịu thuế.
