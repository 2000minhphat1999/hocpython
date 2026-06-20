"""
hr_logic.py - Tầng nghiệp vụ (Business logic) cho hệ thống nhân sự.

Chứa các quy tắc "thông minh":
  - Tính lương gross/net (bảo hiểm, thuế thu nhập cá nhân).
  - Xếp loại hiệu suất (KPI) - tương tự bài "xếp loại học sinh".
  - Các hàm thống kê cho dashboard.

Mọi con số dựa trên quy định phổ biến tại Việt Nam để mang tính minh họa.
"""

# Số ngày công chuẩn trong tháng (dùng để tính lương theo ngày công thực tế).
NGAY_CONG_CHUAN = 26

# --- Tỷ lệ bảo hiểm bắt buộc phần người lao động đóng ---
#   BHXH 8% + BHYT 1.5% + BHTN 1% = 10.5% (tính trên lương đóng BH).
TY_LE_BHXH = 0.08
TY_LE_BHYT = 0.015
TY_LE_BHTN = 0.01

# --- Trần (mức tối đa) tiền lương đóng bảo hiểm, áp dụng từ 01/01/2026 ---
# BHXH & BHYT: tối đa 20 lần lương cơ sở (mức tham chiếu) = 20 x 2.340.000.
LUONG_CO_SO = 2_340_000
TRAN_BHXH_BHYT = 20 * LUONG_CO_SO        # = 46.800.000đ

# BHTN: tối đa 20 lần lương tối thiểu vùng (Nghị định 293/2025/NĐ-CP).
LUONG_TOI_THIEU_VUNG = {
    1: 5_310_000,
    2: 4_730_000,
    3: 4_140_000,
    4: 3_700_000,
}
# Vùng của doanh nghiệp (đổi theo địa bàn đặt trụ sở). Mặc định Vùng I.
VUNG_DOANH_NGHIEP = 1

# --- Giảm trừ gia cảnh (Nghị quyết 110/2025/UBTVQH15, từ kỳ thuế 2026) ---
GIAM_TRU_BAN_THAN = 15_500_000          # cho bản thân người nộp thuế
GIAM_TRU_NGUOI_PHU_THUOC = 6_200_000    # cho mỗi người phụ thuộc

# Biểu thuế thu nhập cá nhân lũy tiến từng phần (theo tháng).
# Mỗi phần tử: (giới hạn trên của bậc, thuế suất). None = không giới hạn.
BAC_THUE = [
    (5_000_000, 0.05),
    (10_000_000, 0.10),
    (18_000_000, 0.15),
    (32_000_000, 0.20),
    (52_000_000, 0.25),
    (80_000_000, 0.30),
    (None, 0.35),
]


def tinh_bao_hiem(luong_dong_bh: float, vung: int = VUNG_DOANH_NGHIEP) -> dict:
    """Tính bảo hiểm bắt buộc phần người lao động đóng (có áp trần).

    - BHXH (8%) và BHYT (1.5%) tính trên min(lương, trần 20 x lương cơ sở).
    - BHTN (1%) tính trên min(lương, trần 20 x lương tối thiểu vùng).

    Trả về dict gồm: bhxh, bhyt, bhtn, tong.
    """
    can_cu_xh_yt = min(luong_dong_bh, TRAN_BHXH_BHYT)
    tran_bhtn = 20 * LUONG_TOI_THIEU_VUNG.get(vung, LUONG_TOI_THIEU_VUNG[1])
    can_cu_tn = min(luong_dong_bh, tran_bhtn)

    bhxh = can_cu_xh_yt * TY_LE_BHXH
    bhyt = can_cu_xh_yt * TY_LE_BHYT
    bhtn = can_cu_tn * TY_LE_BHTN

    return {
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "tong": bhxh + bhyt + bhtn,
    }


def tinh_thue_tncn(thu_nhap_tinh_thue: float) -> float:
    """Tính thuế TNCN theo biểu lũy tiến từng phần.

    thu_nhap_tinh_thue = thu nhập chịu thuế - các khoản giảm trừ.
    Nếu <= 0 thì không phải nộp thuế.
    """
    if thu_nhap_tinh_thue <= 0:
        return 0.0

    thue = 0.0
    gioi_han_duoi = 0
    for gioi_han_tren, thue_suat in BAC_THUE:
        if gioi_han_tren is None:
            # Bậc cuối cùng: tính trên toàn bộ phần còn lại.
            phan_thu_nhap = thu_nhap_tinh_thue - gioi_han_duoi
        else:
            phan_thu_nhap = min(thu_nhap_tinh_thue, gioi_han_tren) - gioi_han_duoi

        if phan_thu_nhap > 0:
            thue += phan_thu_nhap * thue_suat

        if gioi_han_tren is not None and thu_nhap_tinh_thue <= gioi_han_tren:
            break
        gioi_han_duoi = gioi_han_tren if gioi_han_tren else gioi_han_duoi

    return thue


def tinh_luong(nv) -> dict:
    """Tính bảng lương chi tiết cho một nhân viên.

    Tham số nv: một sqlite3.Row hoặc dict có các khoá:
        luong_co_ban, phu_cap, ngay_cong, so_nguoi_phu_thuoc.

    Trả về dict gồm: luong_thuc_te, phu_cap, thu_nhap_gross,
    bao_hiem, giam_tru, thu_nhap_tinh_thue, thue, luong_net.
    """
    luong_co_ban = float(nv["luong_co_ban"])
    phu_cap = float(nv["phu_cap"])
    ngay_cong = int(nv["ngay_cong"])
    so_phu_thuoc = int(nv["so_nguoi_phu_thuoc"])

    # Lương theo ngày công thực tế so với ngày công chuẩn.
    luong_thuc_te = luong_co_ban * ngay_cong / NGAY_CONG_CHUAN

    # Tổng thu nhập trước thuế (gross).
    thu_nhap_gross = luong_thuc_te + phu_cap

    # Bảo hiểm tính trên lương cơ bản (đã áp trần theo quy định).
    bh = tinh_bao_hiem(luong_co_ban)
    bao_hiem = bh["tong"]

    # Giảm trừ gia cảnh.
    giam_tru = GIAM_TRU_BAN_THAN + so_phu_thuoc * GIAM_TRU_NGUOI_PHU_THUOC

    # Thu nhập tính thuế = gross - bảo hiểm - giảm trừ.
    thu_nhap_tinh_thue = thu_nhap_gross - bao_hiem - giam_tru
    thue = tinh_thue_tncn(thu_nhap_tinh_thue)

    # Lương thực nhận (net).
    luong_net = thu_nhap_gross - bao_hiem - thue

    return {
        "luong_thuc_te": luong_thuc_te,
        "phu_cap": phu_cap,
        "thu_nhap_gross": thu_nhap_gross,
        "bhxh": bh["bhxh"],
        "bhyt": bh["bhyt"],
        "bhtn": bh["bhtn"],
        "bao_hiem": bao_hiem,
        "giam_tru": giam_tru,
        "thu_nhap_tinh_thue": max(thu_nhap_tinh_thue, 0),
        "thue": thue,
        "luong_net": luong_net,
    }


def xep_loai_kpi(diem: float) -> str:
    """Xếp loại hiệu suất theo điểm KPI (thang 10).

    Tương tự bài tập "xếp loại học sinh" đã làm:
        >= 8.5 : Xuất sắc
        7 - 8.5: Tốt
        5 - 7  : Đạt
        < 5    : Cần cải thiện
    """
    if diem >= 8.5:
        return "Xuất sắc"
    elif diem >= 7:
        return "Tốt"
    elif diem >= 5:
        return "Đạt"
    else:
        return "Cần cải thiện"


def mau_kpi(xep_loai: str) -> str:
    """Trả về tên lớp CSS theo xếp loại (để tô màu badge trên web)."""
    return {
        "Xuất sắc": "kpi-xuatsac",
        "Tốt": "kpi-tot",
        "Đạt": "kpi-dat",
        "Cần cải thiện": "kpi-canclt",
    }.get(xep_loai, "")


# ---------------------------------------------------------------------------
# Thống kê thông minh cho dashboard
# ---------------------------------------------------------------------------

def thong_ke(danh_sach) -> dict:
    """Tính các chỉ số thống kê từ danh sách nhân viên.

    danh_sach: list các sqlite3.Row (hoặc dict).
    Trả về dict gồm tổng quan, theo phòng ban, phân bố KPI, top nhân viên.
    """
    tong_so = len(danh_sach)

    # Tổng quỹ lương net và lương net trung bình.
    tong_luong_net = 0.0
    for nv in danh_sach:
        tong_luong_net += tinh_luong(nv)["luong_net"]
    luong_tb = tong_luong_net / tong_so if tong_so else 0

    # Thống kê theo phòng ban: số người + tổng lương net.
    theo_phong_ban = {}
    for nv in danh_sach:
        pb = nv["phong_ban"]
        if pb not in theo_phong_ban:
            theo_phong_ban[pb] = {"so_nguoi": 0, "tong_luong": 0.0}
        theo_phong_ban[pb]["so_nguoi"] += 1
        theo_phong_ban[pb]["tong_luong"] += tinh_luong(nv)["luong_net"]

    # Phân bố xếp loại KPI.
    phan_bo_kpi = {"Xuất sắc": 0, "Tốt": 0, "Đạt": 0, "Cần cải thiện": 0}
    for nv in danh_sach:
        phan_bo_kpi[xep_loai_kpi(nv["diem_kpi"])] += 1

    # Top 5 nhân viên theo điểm KPI.
    top_nhan_vien = sorted(
        danh_sach, key=lambda nv: nv["diem_kpi"], reverse=True
    )[:5]

    return {
        "tong_so": tong_so,
        "tong_luong_net": tong_luong_net,
        "luong_tb": luong_tb,
        "so_phong_ban": len(theo_phong_ban),
        "theo_phong_ban": theo_phong_ban,
        "phan_bo_kpi": phan_bo_kpi,
        "top_nhan_vien": top_nhan_vien,
    }


def dinh_dang_tien(so: float) -> str:
    """Định dạng số tiền kiểu Việt Nam: 12,500,000đ."""
    return f"{so:,.0f}đ"
