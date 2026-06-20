"""
seed_data.py - Tạo dữ liệu mẫu để chạy thử hệ thống.

Cách dùng:
    cd hr_system
    python seed_data.py

Lưu ý: file này sẽ XÓA toàn bộ dữ liệu cũ rồi nạp lại dữ liệu mẫu.
"""

import database

MAU = [
    # ma_nv, ho_ten, gioi_tinh, email, phong_ban, chuc_vu, ngay_vao_lam,
    # luong_co_ban, phu_cap, ngay_cong, so_phu_thuoc, diem_kpi, trang_thai
    ("NV001", "Nguyễn Văn An", "Nam", "an.nv@congty.vn", "Kỹ thuật", "Trưởng phòng",
     "2019-03-01", 35_000_000, 5_000_000, 26, 2, 9.2, "Đang làm"),
    ("NV002", "Trần Thị Bình", "Nữ", "binh.tt@congty.vn", "Kỹ thuật", "Lập trình viên",
     "2021-06-15", 22_000_000, 2_000_000, 26, 1, 8.0, "Đang làm"),
    ("NV003", "Lê Hoàng Cường", "Nam", "cuong.lh@congty.vn", "Kỹ thuật", "Lập trình viên",
     "2022-01-10", 18_000_000, 1_500_000, 24, 0, 6.5, "Đang làm"),
    ("NV004", "Phạm Thị Dung", "Nữ", "dung.pt@congty.vn", "Nhân sự", "Trưởng phòng",
     "2018-09-01", 30_000_000, 4_000_000, 26, 2, 8.8, "Đang làm"),
    ("NV005", "Vũ Minh Đức", "Nam", "duc.vm@congty.vn", "Nhân sự", "Chuyên viên",
     "2023-02-20", 15_000_000, 1_000_000, 26, 0, 7.2, "Đang làm"),
    ("NV006", "Hoàng Thị Em", "Nữ", "em.ht@congty.vn", "Kinh doanh", "Trưởng phòng",
     "2017-05-12", 32_000_000, 8_000_000, 26, 3, 9.5, "Đang làm"),
    ("NV007", "Đặng Văn Phú", "Nam", "phu.dv@congty.vn", "Kinh doanh", "Nhân viên sale",
     "2022-11-01", 12_000_000, 6_000_000, 26, 1, 5.5, "Đang làm"),
    ("NV008", "Bùi Thị Giang", "Nữ", "giang.bt@congty.vn", "Kinh doanh", "Nhân viên sale",
     "2023-07-03", 12_000_000, 4_000_000, 25, 0, 4.2, "Đang làm"),
    ("NV009", "Ngô Văn Hải", "Nam", "hai.nv@congty.vn", "Kế toán", "Kế toán trưởng",
     "2016-08-15", 28_000_000, 3_000_000, 26, 2, 8.5, "Đang làm"),
    ("NV010", "Đỗ Thị Lan", "Nữ", "lan.dt@congty.vn", "Kế toán", "Kế toán viên",
     "2024-03-01", 14_000_000, 1_000_000, 26, 0, 6.8, "Đang làm"),
]

KHOA = [
    "ma_nv", "ho_ten", "gioi_tinh", "email", "phong_ban", "chuc_vu",
    "ngay_vao_lam", "luong_co_ban", "phu_cap", "ngay_cong",
    "so_nguoi_phu_thuoc", "diem_kpi", "trang_thai",
]


def nap_du_lieu():
    database.init_db()

    # Xóa dữ liệu cũ.
    conn = database.get_connection()
    conn.execute("DELETE FROM nhan_vien")
    conn.commit()
    conn.close()

    # Nạp dữ liệu mẫu.
    for hang in MAU:
        data = dict(zip(KHOA, hang))
        database.them_nhan_vien(data)

    print(f"Đã nạp {len(MAU)} nhân viên mẫu vào database.")


if __name__ == "__main__":
    nap_du_lieu()
