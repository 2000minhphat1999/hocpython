"""
database.py - Tầng dữ liệu (Data layer) cho hệ thống quản lý nhân sự.

Sử dụng SQLite - một cơ sở dữ liệu nhẹ, lưu trong một file duy nhất (hr.db),
rất phù hợp để học vì không cần cài đặt server.
"""

import sqlite3
import os

# Đường dẫn tới file database, đặt cùng thư mục với file này.
THU_MUC = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(THU_MUC, "hr.db")


def get_connection():
    """Tạo kết nối tới database.

    row_factory = sqlite3.Row giúp truy cập cột theo tên (row["ho_ten"])
    thay vì theo chỉ số (row[1]), code dễ đọc hơn.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Bật ràng buộc khoá ngoại (foreign key) cho SQLite.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Khởi tạo các bảng nếu chưa tồn tại."""
    conn = get_connection()
    cur = conn.cursor()

    # Bảng nhân viên: lưu hồ sơ và các thông tin tính lương.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS nhan_vien (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_nv           TEXT    NOT NULL UNIQUE,
            ho_ten          TEXT    NOT NULL,
            gioi_tinh       TEXT,
            email           TEXT,
            phong_ban       TEXT    NOT NULL,
            chuc_vu         TEXT,
            ngay_vao_lam    TEXT,
            luong_co_ban    REAL    NOT NULL DEFAULT 0,
            phu_cap         REAL    NOT NULL DEFAULT 0,
            ngay_cong       INTEGER NOT NULL DEFAULT 26,
            so_nguoi_phu_thuoc INTEGER NOT NULL DEFAULT 0,
            diem_kpi        REAL    NOT NULL DEFAULT 0,
            trang_thai      TEXT    NOT NULL DEFAULT 'Đang làm'
        )
        """
    )

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Các hàm thao tác với nhân viên (CRUD: Create - Read - Update - Delete)
# ---------------------------------------------------------------------------

def them_nhan_vien(data: dict) -> int:
    """Thêm một nhân viên mới. Trả về id vừa tạo."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO nhan_vien
            (ma_nv, ho_ten, gioi_tinh, email, phong_ban, chuc_vu,
             ngay_vao_lam, luong_co_ban, phu_cap, ngay_cong,
             so_nguoi_phu_thuoc, diem_kpi, trang_thai)
        VALUES
            (:ma_nv, :ho_ten, :gioi_tinh, :email, :phong_ban, :chuc_vu,
             :ngay_vao_lam, :luong_co_ban, :phu_cap, :ngay_cong,
             :so_nguoi_phu_thuoc, :diem_kpi, :trang_thai)
        """,
        data,
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def cap_nhat_nhan_vien(nv_id: int, data: dict) -> None:
    """Cập nhật thông tin một nhân viên theo id."""
    conn = get_connection()
    cur = conn.cursor()
    data = dict(data)
    data["id"] = nv_id
    cur.execute(
        """
        UPDATE nhan_vien SET
            ma_nv = :ma_nv,
            ho_ten = :ho_ten,
            gioi_tinh = :gioi_tinh,
            email = :email,
            phong_ban = :phong_ban,
            chuc_vu = :chuc_vu,
            ngay_vao_lam = :ngay_vao_lam,
            luong_co_ban = :luong_co_ban,
            phu_cap = :phu_cap,
            ngay_cong = :ngay_cong,
            so_nguoi_phu_thuoc = :so_nguoi_phu_thuoc,
            diem_kpi = :diem_kpi,
            trang_thai = :trang_thai
        WHERE id = :id
        """,
        data,
    )
    conn.commit()
    conn.close()


def xoa_nhan_vien(nv_id: int) -> None:
    """Xóa một nhân viên theo id."""
    conn = get_connection()
    conn.execute("DELETE FROM nhan_vien WHERE id = ?", (nv_id,))
    conn.commit()
    conn.close()


def lay_nhan_vien(nv_id: int):
    """Lấy một nhân viên theo id. Trả về sqlite3.Row hoặc None."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM nhan_vien WHERE id = ?", (nv_id,)).fetchone()
    conn.close()
    return row


def danh_sach_nhan_vien(tu_khoa: str = "", phong_ban: str = ""):
    """Lấy danh sách nhân viên, có thể lọc theo từ khóa và phòng ban.

    - tu_khoa: tìm trong mã NV, họ tên, email (không phân biệt hoa thường).
    - phong_ban: lọc đúng phòng ban (để trống = tất cả).
    """
    conn = get_connection()
    sql = "SELECT * FROM nhan_vien WHERE 1 = 1"
    params = []

    if tu_khoa:
        sql += " AND (ma_nv LIKE ? OR ho_ten LIKE ? OR email LIKE ?)"
        like = f"%{tu_khoa}%"
        params += [like, like, like]

    if phong_ban:
        sql += " AND phong_ban = ?"
        params.append(phong_ban)

    sql += " ORDER BY ho_ten"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def lay_danh_sach_phong_ban():
    """Lấy danh sách các phòng ban hiện có (để đổ vào ô lọc)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT phong_ban FROM nhan_vien ORDER BY phong_ban"
    ).fetchall()
    conn.close()
    return [r["phong_ban"] for r in rows]


def dem_theo_ma(ma_nv: str, bo_qua_id: int = None) -> int:
    """Đếm số nhân viên có cùng mã NV (để kiểm tra trùng mã).

    bo_qua_id: khi sửa, bỏ qua chính nhân viên đang sửa.
    """
    conn = get_connection()
    if bo_qua_id is None:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM nhan_vien WHERE ma_nv = ?", (ma_nv,)
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM nhan_vien WHERE ma_nv = ? AND id <> ?",
            (ma_nv, bo_qua_id),
        ).fetchone()
    conn.close()
    return row["c"]
