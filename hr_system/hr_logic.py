"""
hr_logic.py - Tầng nghiệp vụ (Business logic) cho hệ thống nhân sự.

Chứa các quy tắc "thông minh":
  - Tính lương gross/net (bảo hiểm, thuế thu nhập cá nhân).
  - Xếp loại hiệu suất (KPI) - tương tự bài "xếp loại học sinh".
  - Các hàm thống kê cho dashboard.

Mọi con số dựa trên quy định phổ biến tại Việt Nam để mang tính minh họa.
"""

from datetime import date

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


# ---------------------------------------------------------------------------
# Giữ chân nhân tài (Talent retention) - phát hiện nhân sự giỏi có nguy cơ
# nghỉ việc và gợi ý hành động. Logic theo quy tắc, dễ giải thích.
# ---------------------------------------------------------------------------

# Ngưỡng điểm KPI để coi là "nhân sự giỏi" (Tốt trở lên).
NGUONG_NHAN_TAI = 7.0


def so_nam_lam_viec(ngay_vao_lam: str) -> float:
    """Tính số năm làm việc tính đến hôm nay từ ngày vào làm (YYYY-MM-DD)."""
    if not ngay_vao_lam:
        return 0.0
    try:
        nam, thang, ngay = map(int, str(ngay_vao_lam)[:10].split("-"))
        bat_dau = date(nam, thang, ngay)
        return max((date.today() - bat_dau).days / 365.25, 0.0)
    except (ValueError, TypeError):
        return 0.0


def _luong_net_tb_phong_ban(danh_sach) -> dict:
    """Tính lương net trung bình từng phòng ban (chỉ nhân viên đang làm)."""
    tong, dem = {}, {}
    for nv in danh_sach:
        if nv["trang_thai"] != "Đang làm":
            continue
        pb = nv["phong_ban"]
        net = tinh_luong(nv)["luong_net"]
        tong[pb] = tong.get(pb, 0.0) + net
        dem[pb] = dem.get(pb, 0) + 1
    return {pb: tong[pb] / dem[pb] for pb in tong}


def muc_rui_ro(diem: float) -> str:
    """Phân mức rủi ro nghỉ việc theo điểm (0-100)."""
    if diem >= 60:
        return "Cao"
    elif diem >= 30:
        return "Trung bình"
    else:
        return "Thấp"


def mau_rui_ro(muc: str) -> str:
    """Lớp CSS tô màu badge mức rủi ro (tái dùng màu của KPI)."""
    return {
        "Cao": "kpi-canclt",
        "Trung bình": "kpi-dat",
        "Thấp": "kpi-tot",
    }.get(muc, "")


def danh_gia_rui_ro_nghi_viec(nv, mat_bang_pb: float) -> dict:
    """Đánh giá rủi ro nghỉ việc của một nhân viên (điểm 0-100) + gợi ý.

    Công thức:
        kpi_factor   = (KPI - 5) / 5                 -> càng giỏi, càng đáng giữ
        pay_signal   = chênh lệch lương / (25% mặt bằng)  -> thấp hơn 25% là báo động
        tham_nien    = số năm / 4 (tối đa 1)          -> gắn bó lâu, cần ghi nhận
        rủi ro = 100 × kpi_factor × (0.7 × pay_signal + 0.3 × thâm niên)

    Nghĩa là: chỉ nhân viên GIỎI mà bị trả thấp / gắn bó lâu mới rủi ro cao.
    """
    net = tinh_luong(nv)["luong_net"]
    benchmark = mat_bang_pb if mat_bang_pb > 0 else net
    kpi = nv["diem_kpi"]
    so_nam = so_nam_lam_viec(nv["ngay_vao_lam"])

    kpi_factor = max(0.0, min((kpi - 5) / 5, 1.0))
    chenh_lech = benchmark - net
    # Trả thấp hơn 25% mặt bằng phòng ban được coi là tín hiệu rủi ro tối đa.
    nguong = 0.25 * benchmark
    pay_signal = min(max(chenh_lech, 0.0) / nguong, 1.0) if nguong > 0 else 0.0
    tham_nien_factor = min(so_nam / 4, 1.0)

    diem = round(100 * kpi_factor * (0.7 * pay_signal + 0.3 * tham_nien_factor))

    # Gợi ý hành động cụ thể.
    goi_y = []
    if chenh_lech > 0:
        goi_y.append(
            f"Xem xét tăng ~{dinh_dang_tien(chenh_lech)} để đạt mặt bằng phòng ban"
        )
    if so_nam >= 3:
        goi_y.append("Đánh giá lộ trình thăng tiến / ghi nhận thâm niên")
    if kpi >= 8.5:
        goi_y.append("Khen thưởng, giữ chân nhân tài xuất sắc")
    if not goi_y:
        goi_y.append("Duy trì chính sách hiện tại")

    return {
        "diem_rui_ro": diem,
        "muc_rui_ro": muc_rui_ro(diem),
        "luong_net": net,
        "mat_bang_pb": benchmark,
        "chenh_lech": chenh_lech,
        "so_nam": so_nam,
        "goi_y": goi_y,
    }


def phan_tich_giu_chan(danh_sach) -> list:
    """Phân tích giữ chân nhân tài: nhân viên đang làm có KPI >= 7.

    Trả về danh sách dict (gồm thông tin nhân viên + đánh giá rủi ro),
    sắp xếp theo điểm rủi ro giảm dần (nguy cơ cao lên đầu).
    """
    mat_bang = _luong_net_tb_phong_ban(danh_sach)
    ket_qua = []
    for nv in danh_sach:
        if nv["trang_thai"] != "Đang làm" or nv["diem_kpi"] < NGUONG_NHAN_TAI:
            continue
        danh_gia = danh_gia_rui_ro_nghi_viec(nv, mat_bang.get(nv["phong_ban"], 0))
        danh_gia["nv"] = nv
        ket_qua.append(danh_gia)

    ket_qua.sort(key=lambda x: x["diem_rui_ro"], reverse=True)
    return ket_qua
