# Sơ đồ mô hình hệ thống quản lý nhân sự

Tài liệu mô tả kiến trúc và mô hình dữ liệu của ứng dụng. Các sơ đồ viết bằng
[Mermaid](https://mermaid.js.org/) nên GitHub tự render trực tiếp dưới đây.
Bản ảnh vector kèm theo: [`kien-truc.svg`](kien-truc.svg) và
[`mo-hinh-du-lieu.svg`](mo-hinh-du-lieu.svg).

## 1. Kiến trúc hệ thống (kiến trúc phân tầng)

Ứng dụng tách thành 4 tầng rõ ràng, mỗi tầng một file/thư mục:

```mermaid
flowchart TB
    User([Người dùng / Trình duyệt])

    subgraph App["Tầng điều hướng - app.py (Flask)"]
        Routes["Routes<br/>/ dashboard · /nhan-vien · /nhan-vien/them<br/>/nhan-vien/sua · /nhan-vien/xoa · /giu-chan"]
    end

    subgraph View["Tầng giao diện - templates + static (Jinja2/CSS)"]
        T["base · dashboard · danh_sach<br/>chi_tiet · form · giu_chan"]
    end

    subgraph Logic["Tầng nghiệp vụ - hr_logic.py"]
        L1["Tính lương<br/>(bảo hiểm + thuế TNCN 2026)"]
        L2["Xếp loại KPI"]
        L3["Thống kê dashboard"]
        L4["Giữ chân nhân tài<br/>(điểm rủi ro nghỉ việc)"]
    end

    subgraph Dataf["Tầng dữ liệu - database.py"]
        D["CRUD: thêm/sửa/xóa/tìm kiếm"]
    end

    DB[("hr.db<br/>SQLite")]

    User -->|HTTP request| Routes
    Routes -->|render| T
    T -->|HTML response| User
    Routes --> Logic
    Routes --> D
    Logic --> D
    D --> DB
```

**Nguyên tắc:** tầng trên gọi tầng dưới, không ngược lại. Giao diện không truy
cập trực tiếp database; mọi nghiệp vụ (lương, thuế, KPI, rủi ro) nằm gọn trong
`hr_logic.py` để dễ kiểm thử và thay đổi.

## 2. Mô hình dữ liệu

Toàn bộ dữ liệu nằm trong một bảng `nhan_vien` (SQLite):

```mermaid
erDiagram
    NHAN_VIEN {
        int id PK "Khóa chính, tự tăng"
        text ma_nv UK "Mã NV, duy nhất"
        text ho_ten "Họ tên"
        text gioi_tinh "Giới tính"
        text email "Email"
        text phong_ban "Phòng ban"
        text chuc_vu "Chức vụ"
        text ngay_vao_lam "Ngày vào làm"
        real luong_co_ban "Lương cơ bản"
        real phu_cap "Phụ cấp"
        int ngay_cong "Ngày công"
        int so_nguoi_phu_thuoc "Số người phụ thuộc"
        real diem_kpi "Điểm KPI (0-10)"
        text trang_thai "Đang làm / Nghỉ việc"
    }
```

## 3. Luồng xử lý một yêu cầu (ví dụ: xem chi tiết nhân viên)

```mermaid
sequenceDiagram
    participant U as Người dùng
    participant A as app.py (route chi_tiet)
    participant DB as database.py
    participant L as hr_logic.py
    U->>A: GET /nhan-vien/5
    A->>DB: lay_nhan_vien(5)
    DB-->>A: dữ liệu nhân viên
    A->>L: tinh_luong(nv) + xep_loai_kpi(diem)
    L-->>A: bảng lương + xếp loại
    A-->>U: trang chi_tiet.html (đã render)
```
