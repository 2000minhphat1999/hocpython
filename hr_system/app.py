"""
app.py - Ứng dụng web Flask cho hệ thống quản lý nhân sự thông minh.

Cách chạy:
    cd hr_system
    python app.py
Sau đó mở trình duyệt tại http://127.0.0.1:5000

Cấu trúc theo mô hình tách lớp:
    database.py  -> thao tác cơ sở dữ liệu (SQLite)
    hr_logic.py  -> nghiệp vụ (lương, thuế, KPI, thống kê)
    app.py       -> điều hướng (routes) và kết nối với giao diện (templates)
"""

from flask import Flask, render_template, request, redirect, url_for, flash

import database
import hr_logic

app = Flask(__name__)
# secret_key cần thiết để dùng flash message (thông báo sau khi thêm/sửa/xóa).
app.secret_key = "he-thong-nhan-su-thong-minh"

# Đăng ký các hàm tiện ích để gọi trực tiếp trong template (Jinja2).
app.jinja_env.globals.update(
    tinh_luong=hr_logic.tinh_luong,
    xep_loai_kpi=hr_logic.xep_loai_kpi,
    mau_kpi=hr_logic.mau_kpi,
    dinh_dang_tien=hr_logic.dinh_dang_tien,
)

# Các lựa chọn cố định dùng trong form.
DANH_SACH_TRANG_THAI = ["Đang làm", "Nghỉ việc"]


def doc_form() -> dict:
    """Đọc dữ liệu nhân viên từ form gửi lên, chuẩn hóa kiểu dữ liệu."""

    def so(ten, mac_dinh=0):
        """Đọc một số từ form, nếu rỗng/sai thì trả về mặc định."""
        try:
            return float(request.form.get(ten, mac_dinh) or mac_dinh)
        except ValueError:
            return mac_dinh

    return {
        "ma_nv": request.form.get("ma_nv", "").strip(),
        "ho_ten": request.form.get("ho_ten", "").strip(),
        "gioi_tinh": request.form.get("gioi_tinh", ""),
        "email": request.form.get("email", "").strip(),
        "phong_ban": request.form.get("phong_ban", "").strip(),
        "chuc_vu": request.form.get("chuc_vu", "").strip(),
        "ngay_vao_lam": request.form.get("ngay_vao_lam", ""),
        "luong_co_ban": so("luong_co_ban"),
        "phu_cap": so("phu_cap"),
        "ngay_cong": int(so("ngay_cong", 26)),
        "so_nguoi_phu_thuoc": int(so("so_nguoi_phu_thuoc", 0)),
        "diem_kpi": so("diem_kpi"),
        "trang_thai": request.form.get("trang_thai", "Đang làm"),
    }


def kiem_tra_hop_le(data: dict, bo_qua_id: int = None) -> list:
    """Kiểm tra dữ liệu form. Trả về danh sách lỗi (rỗng nếu hợp lệ)."""
    loi = []
    if not data["ma_nv"]:
        loi.append("Mã nhân viên không được để trống.")
    elif database.dem_theo_ma(data["ma_nv"], bo_qua_id) > 0:
        loi.append(f"Mã nhân viên '{data['ma_nv']}' đã tồn tại.")

    if not data["ho_ten"]:
        loi.append("Họ tên không được để trống.")
    if not data["phong_ban"]:
        loi.append("Phòng ban không được để trống.")
    if data["luong_co_ban"] < 0:
        loi.append("Lương cơ bản không hợp lệ.")
    if not (0 <= data["diem_kpi"] <= 10):
        loi.append("Điểm KPI phải trong khoảng 0 - 10.")
    return loi


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def dashboard():
    """Trang chủ - bảng điều khiển thống kê."""
    danh_sach = database.danh_sach_nhan_vien()
    tk = hr_logic.thong_ke(danh_sach)
    return render_template("dashboard.html", tk=tk)


@app.route("/nhan-vien")
def danh_sach():
    """Danh sách nhân viên, có tìm kiếm và lọc theo phòng ban."""
    tu_khoa = request.args.get("tu_khoa", "").strip()
    phong_ban = request.args.get("phong_ban", "").strip()
    ds = database.danh_sach_nhan_vien(tu_khoa, phong_ban)
    return render_template(
        "danh_sach.html",
        danh_sach=ds,
        tu_khoa=tu_khoa,
        phong_ban=phong_ban,
        cac_phong_ban=database.lay_danh_sach_phong_ban(),
    )


@app.route("/nhan-vien/<int:nv_id>")
def chi_tiet(nv_id):
    """Chi tiết một nhân viên kèm bảng lương."""
    nv = database.lay_nhan_vien(nv_id)
    if nv is None:
        flash("Không tìm thấy nhân viên.", "error")
        return redirect(url_for("danh_sach"))
    luong = hr_logic.tinh_luong(nv)
    return render_template("chi_tiet.html", nv=nv, luong=luong)


@app.route("/nhan-vien/them", methods=["GET", "POST"])
def them():
    """Thêm nhân viên mới."""
    if request.method == "POST":
        data = doc_form()
        loi = kiem_tra_hop_le(data)
        if loi:
            for l in loi:
                flash(l, "error")
            return render_template(
                "form.html", nv=data, tieu_de="Thêm nhân viên",
                trang_thais=DANH_SACH_TRANG_THAI,
            )
        nv_id = database.them_nhan_vien(data)
        flash(f"Đã thêm nhân viên {data['ho_ten']}.", "success")
        return redirect(url_for("chi_tiet", nv_id=nv_id))

    # GET: form trống với vài giá trị mặc định.
    nv_mac_dinh = {
        "ma_nv": "", "ho_ten": "", "gioi_tinh": "Nam", "email": "",
        "phong_ban": "", "chuc_vu": "", "ngay_vao_lam": "",
        "luong_co_ban": 0, "phu_cap": 0, "ngay_cong": 26,
        "so_nguoi_phu_thuoc": 0, "diem_kpi": 0, "trang_thai": "Đang làm",
    }
    return render_template(
        "form.html", nv=nv_mac_dinh, tieu_de="Thêm nhân viên",
        trang_thais=DANH_SACH_TRANG_THAI,
    )


@app.route("/nhan-vien/<int:nv_id>/sua", methods=["GET", "POST"])
def sua(nv_id):
    """Sửa thông tin nhân viên."""
    nv = database.lay_nhan_vien(nv_id)
    if nv is None:
        flash("Không tìm thấy nhân viên.", "error")
        return redirect(url_for("danh_sach"))

    if request.method == "POST":
        data = doc_form()
        loi = kiem_tra_hop_le(data, bo_qua_id=nv_id)
        if loi:
            for l in loi:
                flash(l, "error")
            data["id"] = nv_id
            return render_template(
                "form.html", nv=data, tieu_de="Sửa nhân viên",
                trang_thais=DANH_SACH_TRANG_THAI,
            )
        database.cap_nhat_nhan_vien(nv_id, data)
        flash("Đã cập nhật thông tin.", "success")
        return redirect(url_for("chi_tiet", nv_id=nv_id))

    return render_template(
        "form.html", nv=nv, tieu_de="Sửa nhân viên",
        trang_thais=DANH_SACH_TRANG_THAI,
    )


@app.route("/nhan-vien/<int:nv_id>/xoa", methods=["POST"])
def xoa(nv_id):
    """Xóa nhân viên."""
    nv = database.lay_nhan_vien(nv_id)
    if nv is None:
        flash("Không tìm thấy nhân viên.", "error")
    else:
        database.xoa_nhan_vien(nv_id)
        flash(f"Đã xóa nhân viên {nv['ho_ten']}.", "success")
    return redirect(url_for("danh_sach"))


if __name__ == "__main__":
    # Khởi tạo bảng dữ liệu khi chạy lần đầu.
    database.init_db()
    app.run(debug=True)
