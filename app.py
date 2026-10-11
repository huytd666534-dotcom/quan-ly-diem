import inspect
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Quản Lý Điểm Sinh Viên VIP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. BẢNG MÀU PASTEL (dùng chung cho CSS, biểu đồ, bảng điểm)
#    Muốn đổi màu chủ đạo: sửa các biến ở :root trong CSS và dict bên dưới.
# ==========================================
INK = "#2f4a60"  # Màu chữ chính
INK_SOFT = "#6d8aa0"  # Màu chữ phụ
LINE = "#d4e6f3"  # Màu viền nhạt
BLUE, BLUE_D = "#8cc4ee", "#4a8fc4"
MINT, MINT_D = "#a8e0cb", "#2f7a5d"
PEACH, PEACH_D = "#f6c7b6", "#9a5640"
ROSE, ROSE_D = "#f4b6c0", "#9b4a5a"

# Màu cột / biểu đồ theo xếp loại
GRADE_FILL = {"Giỏi": BLUE, "Khá": MINT, "Trung bình": PEACH, "Yếu": ROSE}
# Màu nền + màu chữ của badge / ô xếp loại
GRADE_BADGE = {
    "Giỏi": ("#d7eefc", "#2f6a95"),
    "Khá": ("#daf3e9", MINT_D),
    "Trung bình": ("#fde6dc", PEACH_D),
    "Yếu": ("#fbe1e5", ROSE_D),
}
GRADE_CLASS = {
    "Giỏi": "badge-gioi",
    "Khá": "badge-kha",
    "Trung bình": "badge-tb",
    "Yếu": "badge-yeu",
}

# ==========================================
# 3. CSS: GIAO DIỆN PASTEL, KÍNH MỜ, CHUYỂN ĐỘNG MƯỢT
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

    /* Đăng ký biến số để tạo hiệu ứng đếm số tăng dần bằng CSS */
    @property --ci { syntax: '<integer>'; inherits: false; initial-value: 0; }
    @property --cd { syntax: '<integer>'; inherits: false; initial-value: 0; }

    :root {
        --bg: #eef6fc;
        --card: rgba(255, 255, 255, 0.82);
        --ink: #2f4a60;
        --ink-soft: #6d8aa0;
        --line: #d4e6f3;
        --blue: #8cc4ee;
        --blue-d: #4a8fc4;
        --mint: #a8e0cb;
        --mint-d: #2f7a5d;
        --peach: #f6c7b6;
        --peach-d: #9a5640;
        --rose: #f4b6c0;
        --rose-d: #9b4a5a;
        --shadow: 0 10px 30px rgba(74, 143, 196, 0.14);
        --shadow-hover: 0 18px 38px rgba(74, 143, 196, 0.22);
        --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* ---------- Nền và font chung ---------- */
    html, body, [class*="css"], .stApp {
        font-family: 'Be Vietnam Pro', 'Segoe UI', sans-serif;
        color: var(--ink);
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 12% 8%, #dcecfa 0, transparent 42%),
            radial-gradient(circle at 88% 18%, #e3f5ee 0, transparent 38%),
            radial-gradient(circle at 60% 95%, #f3ecfa 0, transparent 40%),
            var(--bg);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2rem; max-width: 1200px; }
    h1, h2, h3, h4, h5, h6, label, [data-testid="stWidgetLabel"] p {
        color: var(--ink) !important;
        font-weight: 600;
    }

    /* ---------- Keyframes ---------- */
    @keyframes rise {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes heroShift {
        from { background-position: 0% 50%; }
        to { background-position: 100% 50%; }
    }
    @keyframes sheen {
        0% { transform: translateX(-120%); }
        35%, 100% { transform: translateX(120%); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.45; transform: scale(0.7); }
    }
    @keyframes grow { from { width: 0; } }
    @keyframes flow {
        from { background-position: 0% 0; }
        to { background-position: 200% 0; }
    }
    @keyframes countI { from { --ci: 0; } }
    @keyframes countD { from { --cd: 0; } }

    /* ---------- Banner đầu trang ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 30px 34px;
        margin-bottom: 22px;
        background: linear-gradient(120deg, #cfe6f7, #dff3ea 55%, #e8e1f7);
        background-size: 200% 200%;
        border: 1px solid rgba(255, 255, 255, 0.85);
        box-shadow: var(--shadow);
        animation: heroShift 14s ease-in-out infinite alternate, rise 0.8s var(--ease) both;
    }
    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(105deg, transparent 35%, rgba(255, 255, 255, 0.55) 50%, transparent 65%);
        transform: translateX(-120%);
        animation: sheen 8s ease-in-out 1.2s infinite;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.25;
        background: linear-gradient(90deg, #24445e, #4a8fc4);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
    }
    .hero-sub { margin-top: 6px; color: #56768e; font-size: 1.02rem; }

    /* ---------- Thẻ số liệu ---------- */
    .m-card {
        position: relative;
        overflow: hidden;
        background: var(--card);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 22px;
        padding: 18px 20px 16px 24px;
        box-shadow: var(--shadow);
        transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease);
        animation: rise 0.7s var(--ease) both;
        animation-delay: var(--d, 0s);
    }
    .m-card::before {
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 6px;
        background: var(--accent);
    }
    .m-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-hover); }
    .m-top { display: flex; align-items: center; gap: 10px; }
    .m-icon {
        width: 36px; height: 36px;
        border-radius: 12px;
        display: grid; place-items: center;
        background: var(--tint);
        font-size: 1.1rem;
    }
    .m-label { font-size: 0.88rem; color: var(--ink-soft); font-weight: 500; }
    .m-value { font-size: 2.1rem; font-weight: 700; margin: 10px 0 2px; line-height: 1.1; color: var(--ink); }
    .m-sub { font-size: 0.88rem; color: var(--ink-soft); }

    /* Số đếm tăng dần: giá trị cuối đặt qua --ci (phần nguyên) và --cd (phần thập phân) */
    .count {
        counter-reset: ci var(--ci) cd var(--cd);
        animation: countI 1.5s var(--ease) both, countD 1.5s var(--ease) both;
    }
    .count::before { content: counter(ci) "." counter(cd, decimal-leading-zero); }
    .count-pct::before { content: counter(ci) "%"; }

    /* ---------- Badge xếp loại ---------- */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 600;
        transition: transform 0.25s var(--ease);
    }
    .badge:hover { transform: scale(1.05); }
    .badge::before {
        content: "";
        width: 8px; height: 8px;
        border-radius: 50%;
        background: currentColor;
        animation: pulse 2.4s ease-in-out infinite;
    }
    .badge-gioi { background: #d7eefc; color: #2f6a95; }
    .badge-kha { background: #daf3e9; color: #2f7a5d; }
    .badge-tb { background: #fde6dc; color: #9a5640; }
    .badge-yeu { background: #fbe1e5; color: #9b4a5a; }

    /* ---------- Banner chào ở tab Tổng quan ---------- */
    .welcome {
        background: var(--card);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 18px;
        padding: 14px 20px;
        margin-bottom: 18px;
        color: var(--ink);
        box-shadow: var(--shadow);
        animation: rise 0.6s var(--ease) both;
    }

    /* ---------- Hồ sơ cá nhân ---------- */
    .profile {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        background: var(--card);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 28px;
        padding: 22px 26px;
        box-shadow: var(--shadow);
        animation: rise 0.6s var(--ease) both;
    }
    .avatar {
        width: 72px; height: 72px;
        padding: 3px;
        border-radius: 50%;
        background: conic-gradient(#8cc4ee, #a8e0cb, #f6c7b6, #cfc6ef, #8cc4ee);
    }
    .avatar span {
        display: grid; place-items: center;
        width: 100%; height: 100%;
        border-radius: 50%;
        background: #fff;
        color: var(--blue-d);
        font-size: 1.5rem;
        font-weight: 700;
    }
    .p-name { font-size: 1.6rem; font-weight: 700; line-height: 1.2; }
    .p-meta { color: var(--ink-soft); font-size: 0.92rem; margin-top: 2px; }
    .p-right { margin-left: auto; display: flex; align-items: center; flex-wrap: wrap; gap: 10px; }
    .pill {
        padding: 6px 14px;
        border-radius: 999px;
        background: #fff;
        border: 1px solid var(--line);
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* ---------- Ô điểm thành phần ---------- */
    .s-tile {
        background: var(--card);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 16px 18px;
        box-shadow: var(--shadow);
        height: 100%;
        transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease);
        animation: rise 0.6s var(--ease) both;
        animation-delay: var(--d, 0s);
    }
    .s-tile:hover { transform: translateY(-4px); box-shadow: var(--shadow-hover); }
    .s-label { font-size: 0.86rem; color: var(--ink-soft); font-weight: 500; }
    .s-value { font-size: 1.9rem; font-weight: 700; margin: 6px 0 8px; line-height: 1.1; }
    .delta { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; }
    .delta-up { background: #daf3e9; color: #2f7a5d; }
    .delta-down { background: #fde6dc; color: #9a5640; }
    .delta-eq { background: #e8eef4; color: #5b7589; }

    /* ---------- Thanh tiến độ ---------- */
    .pbar { height: 16px; border-radius: 999px; background: #e0edf7; overflow: hidden; }
    .pfill {
        height: 100%;
        width: var(--w);
        border-radius: 999px;
        background: linear-gradient(90deg, #8cc4ee, #a8e0cb, #8cc4ee);
        background-size: 200% 100%;
        animation: grow 1.3s var(--ease) both, flow 5s linear infinite;
    }
    .pscale { display: flex; justify-content: space-between; margin-top: 6px; font-size: 0.8rem; color: var(--ink-soft); }
    .note {
        background: var(--card);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 22px;
        padding: 18px 20px;
        margin-top: 16px;
        box-shadow: var(--shadow);
        line-height: 1.6;
    }

    /* ---------- Thẻ tác giả ở sidebar ---------- */
    .dev-card {
        display: flex;
        gap: 14px;
        align-items: center;
        margin-top: 18px;
        padding: 16px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.95);
        box-shadow: var(--shadow);
    }
    .dev-avatar {
        flex: none;
        width: 48px; height: 48px;
        padding: 3px;
        border-radius: 50%;
        background: conic-gradient(#8cc4ee, #a8e0cb, #f6c7b6, #cfc6ef, #8cc4ee);
    }
    .dev-avatar span {
        display: grid; place-items: center;
        width: 100%; height: 100%;
        border-radius: 50%;
        background: #fff;
        color: var(--blue-d);
        font-weight: 700;
        font-size: 0.95rem;
    }
    .dev-card h4 { margin: 0 0 6px 0; font-size: 1rem; }
    .dev-card p { margin: 2px 0; font-size: 0.84rem; color: var(--ink-soft); }

    /* ---------- Tùy biến thành phần Streamlit ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d9eaf7, #e9f3fa 60%, #eef6fc);
        border-right: 1px solid var(--line);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        width: fit-content;
        max-width: 100%;
        overflow-x: auto;
        padding: 6px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid var(--line);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        padding: 0 20px;
        border-radius: 999px;
        background: transparent;
        color: var(--ink-soft);
        font-weight: 600;
        transition: background 0.3s var(--ease), color 0.3s var(--ease), box-shadow 0.3s var(--ease);
    }
    .stTabs [data-baseweb="tab"]:hover { background: rgba(140, 196, 238, 0.22); color: var(--ink); }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #8cc4ee, #a8e0cb) !important;
        color: #1f3f58 !important;
        box-shadow: 0 6px 16px rgba(74, 143, 196, 0.25);
    }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

    [data-baseweb="select"] > div {
        border-radius: 14px !important;
        background: #fff !important;
        border: 1px solid var(--line) !important;
        transition: box-shadow 0.25s ease, border-color 0.25s ease;
    }
    [data-baseweb="select"] > div:hover, [data-baseweb="select"] > div:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 4px rgba(140, 196, 238, 0.3);
    }

    [data-testid="stPlotlyChart"] {
        background: var(--card);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        padding: 14px;
        box-shadow: var(--shadow);
    }
    [data-testid="stDataFrame"] {
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
    }
    .stDownloadButton button {
        border-radius: 999px;
        border: 1px solid var(--blue);
        background: #fff;
        color: var(--blue-d);
        font-weight: 600;
        padding: 0.45rem 1.4rem;
        transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease), background 0.3s ease;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        background: linear-gradient(120deg, #e3f1fc, #e1f5ee);
        border-color: var(--blue-d);
        box-shadow: 0 8px 18px rgba(74, 143, 196, 0.2);
    }

    .footer { text-align: center; color: var(--ink-soft); font-size: 0.86rem; margin-top: 2.5rem; padding: 1rem; }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-thumb { background: #bcdaf0; border-radius: 10px; border: 2px solid var(--bg); }
    ::-webkit-scrollbar-track { background: transparent; }

    /* ---------- Responsive ---------- */
    @media (max-width: 640px) {
        .hero { padding: 22px; }
        .hero-title { font-size: 1.5rem; }
        .m-value { font-size: 1.7rem; }
        .profile { padding: 18px; }
        .p-right { margin-left: 0; }
    }

    /* Tôn trọng người dùng muốn giảm chuyển động */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 4. HÀM TIỆN ÍCH
# ==========================================
def html(markup):
    """Hiển thị HTML: gộp xuống dòng để Markdown không hiểu nhầm thành code."""
    st.markdown(re.sub(r"\s*\n\s*", " ", markup.strip()), unsafe_allow_html=True)


def _width_kwargs(func):
    """Dùng width='stretch' nếu phiên bản Streamlit hỗ trợ, ngược lại dùng use_container_width."""
    try:
        if "width" in inspect.signature(func).parameters:
            return {"width": "stretch"}
    except (TypeError, ValueError):
        pass
    return {"use_container_width": True}


PLOTLY_KW = _width_kwargs(st.plotly_chart)
DATAFRAME_KW = _width_kwargs(st.dataframe)


def count_up(value, kind="dec"):
    """Số đếm tăng dần bằng CSS. kind='dec' -> 7.63, kind='pct' -> 100%."""
    if kind == "pct":
        return (
            f'<span class="count count-pct" style="--ci:{int(round(value))}"'
            f' aria-label="{value:.0f}%"></span>'
        )
    value = round(float(value), 2)
    whole = int(value)
    frac = int(round((value - whole) * 100))
    return (
        f'<span class="count" style="--ci:{whole};--cd:{frac}"'
        f' aria-label="{value:.2f}"></span>'
    )


def initials(name):
    parts = name.split()
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


def style_fig(fig, height):
    """Áp dụng phong cách pastel chung cho mọi biểu đồ Plotly."""
    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=16, r=16, t=24, b=16),
        font=dict(family="Be Vietnam Pro, sans-serif", color=INK),
        hoverlabel=dict(
            bgcolor="white", font=dict(family="Be Vietnam Pro, sans-serif", color=INK)
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor=LINE)
    fig.update_yaxes(gridcolor="#e3eef7", zeroline=False)
    return fig


# ==========================================
# 5. CHUẨN BỊ & XỬ LÝ DỮ LIỆU (GIỮ NGUYÊN LOGIC)
# ==========================================
@st.cache_data
def get_student_data():
    data = {
        "Họ và tên": [
            "An", "Bình", "Chi", "Dũng", "Hà",
            "Lan", "Minh", "Nam", "Phúc", "Trang",
        ],
        "Điểm chuyên cần": [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.5],
        "Điểm giữa kỳ": [8.0, 8.0, 6.0, 9.0, 7.0, 5.5, 8.0, 6.5, 7.0, 9.0],
        "Điểm cuối kỳ": [8.0, 8.5, 6.5, 9.0, 7.5, 5.5, 8.5, 7.0, 7.5, 9.0],
    }
    df = pd.DataFrame(data)

    # Công thức: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
    df["Tong_ket"] = (
        0.2 * df["Điểm chuyên cần"]
        + 0.3 * df["Điểm giữa kỳ"]
        + 0.5 * df["Điểm cuối kỳ"]
    ).round(2)

    # Xếp loại
    def phan_loai(score):
        if score >= 8.5:
            return "Giỏi"
        elif score >= 7.0:
            return "Khá"
        elif score >= 5.0:
            return "Trung bình"
        else:
            return "Yếu"

    df["Xep_loai"] = df["Tong_ket"].apply(phan_loai)
    # Thứ hạng trong lớp (điểm cao nhất = hạng 1)
    df["Hang"] = df["Tong_ket"].rank(ascending=False, method="min").astype(int)
    return df


df_students = get_student_data()
TOTAL = len(df_students)
COMPONENTS = ["Điểm chuyên cần", "Điểm giữa kỳ", "Điểm cuối kỳ"]
class_avg = df_students[COMPONENTS + ["Tong_ket"]].mean()


# ==========================================
# 6. THANH BÊN (SIDEBAR) & BỘ LỌC
# ==========================================
with st.sidebar:
    st.title("🎓 Bảng điều khiển")
    st.subheader("Lọc và tìm kiếm")

    search_options = ["Tất cả sinh viên"] + df_students["Họ và tên"].tolist()
    selected_student_search = st.selectbox(
        "Tìm kiếm hoặc chọn sinh viên",
        options=search_options,
        index=0,
        help="Bấm vào ô hoặc gõ chữ cái đầu của tên để chọn nhanh sinh viên.",
    )

    categories = ["Tất cả xếp loại"] + list(df_students["Xep_loai"].unique())
    selected_category = st.selectbox("Lọc theo xếp loại", categories)

    # Xử lý dữ liệu sau lọc
    df_filtered = df_students.copy()
    if selected_student_search != "Tất cả sinh viên":
        df_filtered = df_filtered[df_filtered["Họ và tên"] == selected_student_search]
    if selected_category != "Tất cả xếp loại":
        df_filtered = df_filtered[df_filtered["Xep_loai"] == selected_category]

    html(
        f"""
        <div class="dev-card">
            <div class="dev-avatar"><span>{initials("Nguyễn Văn A")}</span></div>
            <div>
                <h4>Thông tin tác giả</h4>
                <p><b>Họ và tên:</b> Nguyễn Văn A</p>
                <p><b>MSSV:</b> 22110000</p>
                <p><b>Lớp:</b> Lập trình Python K63</p>
                <p><b>Trường:</b> ĐH Giao Thông Vận Tải</p>
            </div>
        </div>
        """
    )


# ==========================================
# 7. TIÊU ĐỀ TRANG WEB
# ==========================================
html(
    """
    <div class="hero">
        <div class="hero-title">Quản lý điểm sinh viên</div>
        <div class="hero-sub">Thống kê tự động, biểu đồ tương tác và tra cứu hồ sơ học tập của cả lớp.</div>
    </div>
    """
)


# ==========================================
# 8. BỐ CỤC TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(
    ["📊 Tổng quan & Bảng điểm", "📈 Biểu đồ & Phân tích", "🔍 Tra cứu cá nhân"]
)


# ------------------------------------------
# TAB 1: TỔNG QUAN & BẢNG ĐIỂM
# ------------------------------------------
with tab1:
    avg_score = df_students["Tong_ket"].mean()
    max_student = df_students.loc[df_students["Tong_ket"].idxmax()]
    min_student = df_students.loc[df_students["Tong_ket"].idxmin()]
    passed_count = int((df_students["Tong_ket"] >= 5.0).sum())
    pass_rate = passed_count / TOTAL * 100

    html(
        f"""
        <div class="welcome">
            Xin chào! Lớp hiện có <b>{TOTAL}</b> sinh viên với điểm trung bình
            <b>{avg_score:.2f}</b>. Đang hiển thị <b>{len(df_filtered)}/{TOTAL}</b>
            sinh viên theo bộ lọc ở thanh bên.
        </div>
        """
    )

    cards = [
        ("🎯", "Điểm TB lớp", count_up(avg_score), "Thang điểm 10", BLUE, "#e3f1fc"),
        ("🏆", "Điểm cao nhất", count_up(max_student["Tong_ket"]), max_student["Họ và tên"], MINT, "#e1f5ee"),
        ("📉", "Điểm thấp nhất", count_up(min_student["Tong_ket"]), min_student["Họ và tên"], PEACH, "#fdeee7"),
        ("✅", "Tỷ lệ đạt", count_up(pass_rate, "pct"), f"{passed_count}/{TOTAL} sinh viên", "#cfc6ef", "#ece7f8"),
    ]
    for col, (icon, label, value, sub, accent, tint), i in zip(
        st.columns(4), cards, range(4)
    ):
        with col:
            html(
                f"""
                <div class="m-card" style="--accent:{accent};--tint:{tint};--d:{i * 0.09}s">
                    <div class="m-top">
                        <div class="m-icon">{icon}</div>
                        <div class="m-label">{label}</div>
                    </div>
                    <div class="m-value">{value}</div>
                    <div class="m-sub">{sub}</div>
                </div>
                """
            )

    st.write("")
    head_col, btn_col = st.columns([4, 1])
    with head_col:
        st.subheader("📋 Bảng điểm sinh viên")
    with btn_col:
        csv_bytes = df_students.drop(columns=["Hang"]).to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇ Tải bảng điểm (CSV)",
            data=csv_bytes,
            file_name="bang_diem_sinh_vien.csv",
            mime="text/csv",
        )

    if df_filtered.empty:
        st.info("Không có sinh viên nào khớp bộ lọc. Hãy đổi điều kiện ở thanh bên.")
    else:
        df_show = df_filtered[
            ["Hang", "Họ và tên"] + COMPONENTS + ["Tong_ket", "Xep_loai"]
        ].rename(columns={"Hang": "Hạng", "Tong_ket": "Tổng kết", "Xep_loai": "Xếp loại"})

        def highlight_xep_loai(val):
            bg, fg = GRADE_BADGE.get(val, GRADE_BADGE["Yếu"])
            return f"background-color: {bg}; color: {fg}; font-weight: 600;"

        styler = df_show.style
        apply_cell = styler.map if hasattr(styler, "map") else styler.applymap
        styled_df = apply_cell(highlight_xep_loai, subset=["Xếp loại"]).format(
            {
                "Điểm chuyên cần": "{:.1f}",
                "Điểm giữa kỳ": "{:.1f}",
                "Điểm cuối kỳ": "{:.1f}",
                "Tổng kết": "{:.2f}",
            }
        )
        st.dataframe(styled_df, hide_index=True, height=390, **DATAFRAME_KW)


# ------------------------------------------
# TAB 2: BIỂU ĐỒ & PHÂN TÍCH
# ------------------------------------------
with tab2:
    st.subheader("📈 Phân tích trực quan kết quả học tập")
    col_chart1, col_chart2 = st.columns([6, 4])

    with col_chart1:
        st.markdown("##### Điểm tổng kết từng sinh viên")
        fig_bar = px.bar(
            df_students,
            x="Họ và tên",
            y="Tong_ket",
            color="Xep_loai",
            color_discrete_map=GRADE_FILL,
            text="Tong_ket",
            labels={"Tong_ket": "Điểm tổng kết", "Họ và tên": "Sinh viên", "Xep_loai": "Xếp loại"},
        )
        fig_bar.update_traces(
            textposition="outside",
            texttemplate="%{text:.2f}",
            hovertemplate="<b>%{x}</b><br>Điểm tổng kết: %{y:.2f}<extra></extra>",
            marker_line_width=0,
        )
        try:  # Bo góc cột (chỉ có ở Plotly bản mới)
            fig_bar.update_traces(marker_cornerradius=10)
        except Exception:
            pass
        fig_bar.add_hline(
            y=df_students["Tong_ket"].mean(),
            line_dash="dot",
            line_color=BLUE_D,
            annotation_text=f"TB lớp {df_students['Tong_ket'].mean():.2f}",
            annotation_position="top left",
            annotation_font_color=BLUE_D,
        )
        style_fig(fig_bar, 420)
        fig_bar.update_layout(
            yaxis=dict(range=[0, 10.8], title="Điểm số"),
            xaxis=dict(title=""),
            legend=dict(orientation="h", y=-0.15, title_text=""),
            bargap=0.28,
        )
        st.plotly_chart(fig_bar, **PLOTLY_KW)

    with col_chart2:
        st.markdown("##### Tỷ lệ phân bổ xếp loại của lớp")
        rank_counts = df_students["Xep_loai"].value_counts().reset_index()
        rank_counts.columns = ["Xếp loại", "Số lượng"]
        fig_pie = px.pie(
            rank_counts,
            names="Xếp loại",
            values="Số lượng",
            color="Xếp loại",
            color_discrete_map=GRADE_FILL,
            hole=0.62,
        )
        fig_pie.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=3)),
            hovertemplate="<b>%{label}</b>: %{value} SV (%{percent})<extra></extra>",
        )
        style_fig(fig_pie, 420)
        fig_pie.update_layout(
            showlegend=False,
            annotations=[
                dict(
                    text=f"<b>{TOTAL}</b><br>sinh viên",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=18, color=INK),
                )
            ],
        )
        st.plotly_chart(fig_pie, **PLOTLY_KW)

    st.write("")
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.markdown("##### Điểm trung bình theo từng thành phần")
        comp_avg = pd.DataFrame(
            {
                "Thành phần": ["Chuyên cần (20%)", "Giữa kỳ (30%)", "Cuối kỳ (50%)"],
                "Điểm TB": [class_avg[c] for c in COMPONENTS],
            }
        )
        fig_comp = px.bar(
            comp_avg,
            x="Điểm TB",
            y="Thành phần",
            orientation="h",
            color="Thành phần",
            color_discrete_sequence=[BLUE, MINT, PEACH],
            text="Điểm TB",
        )
        fig_comp.update_traces(texttemplate="%{text:.2f}", textposition="outside", marker_line_width=0)
        try:
            fig_comp.update_traces(marker_cornerradius=10)
        except Exception:
            pass
        style_fig(fig_comp, 340)
        fig_comp.update_layout(
            showlegend=False,
            xaxis=dict(range=[0, 10.5], title="Điểm số"),
            yaxis=dict(title="", autorange="reversed"),
            bargap=0.35,
        )
        st.plotly_chart(fig_comp, **PLOTLY_KW)

    with col_chart4:
        st.markdown("##### So sánh ba loại điểm của từng sinh viên")
        fig_line = go.Figure()
        for comp, color in zip(COMPONENTS, [BLUE_D, "#5fbf9a", "#e8927c"]):
            fig_line.add_trace(
                go.Scatter(
                    x=df_students["Họ và tên"],
                    y=df_students[comp],
                    mode="lines+markers",
                    name=comp.replace("Điểm ", "").capitalize(),
                    line=dict(color=color, width=3, shape="spline"),
                    marker=dict(size=9, color="white", line=dict(color=color, width=2.5)),
                    hovertemplate="<b>%{x}</b><br>%{y}<extra>" + comp + "</extra>",
                )
            )
        style_fig(fig_line, 340)
        fig_line.update_layout(
            yaxis=dict(range=[4, 10.5], title="Điểm số"),
            legend=dict(orientation="h", y=-0.2, title_text=""),
        )
        st.plotly_chart(fig_line, **PLOTLY_KW)


# ------------------------------------------
# TAB 3: TRA CỨU CÁ NHÂN
# ------------------------------------------
with tab3:
    st.subheader("🔍 Tra cứu chi tiết hồ sơ thành tích cá nhân")

    selected_student_name = st.selectbox(
        "Chọn sinh viên cần tra cứu hồ sơ",
        options=df_students["Họ và tên"].tolist(),
        index=0,
    )
    student_info = df_students[df_students["Họ và tên"] == selected_student_name].iloc[0]

    rank_class = GRADE_CLASS.get(student_info["Xep_loai"], "badge-yeu")
    rank_pos = int(student_info["Hang"])

    html(
        f"""
        <div class="profile">
            <div class="avatar"><span>{initials(student_info['Họ và tên'])}</span></div>
            <div>
                <div class="p-meta">Hồ sơ học tập cá nhân</div>
                <div class="p-name">{student_info['Họ và tên']}</div>
            </div>
            <div class="p-right">
                <span class="pill">🏅 Hạng {rank_pos}/{TOTAL}</span>
                <span class="badge {rank_class}">Xếp loại: {student_info['Xep_loai']}</span>
            </div>
        </div>
        """
    )
    st.write("")

    def delta_chip(diff):
        if abs(diff) < 0.005:
            return '<span class="delta delta-eq">Bằng TB lớp</span>'
        cls, arrow = ("delta-up", "▲") if diff > 0 else ("delta-down", "▼")
        return f'<span class="delta {cls}">{arrow} {abs(diff):.2f} so với TB lớp</span>'

    tiles = [
        ("🎯 Chuyên cần (20%)", f"{student_info['Điểm chuyên cần']:.1f}", student_info["Điểm chuyên cần"] - class_avg["Điểm chuyên cần"], BLUE_D),
        ("📝 Giữa kỳ (30%)", f"{student_info['Điểm giữa kỳ']:.1f}", student_info["Điểm giữa kỳ"] - class_avg["Điểm giữa kỳ"], BLUE_D),
        ("✍️ Cuối kỳ (50%)", f"{student_info['Điểm cuối kỳ']:.1f}", student_info["Điểm cuối kỳ"] - class_avg["Điểm cuối kỳ"], BLUE_D),
        ("🌟 Điểm tổng kết", count_up(student_info["Tong_ket"]), student_info["Tong_ket"] - class_avg["Tong_ket"], MINT_D),
    ]
    for col, (label, value, diff, color), i in zip(st.columns(4), tiles, range(4)):
        with col:
            html(
                f"""
                <div class="s-tile" style="--d:{i * 0.08}s">
                    <div class="s-label">{label}</div>
                    <div class="s-value" style="color:{color}">{value}</div>
                    {delta_chip(diff)}
                </div>
                """
            )

    st.write("")
    col_radar, col_info = st.columns([5, 4])

    with col_radar:
        st.markdown("##### So sánh với điểm trung bình lớp")
        cats = ["Chuyên cần", "Giữa kỳ", "Cuối kỳ"]
        mine = [student_info[c] for c in COMPONENTS]
        avg = [class_avg[c] for c in COMPONENTS]
        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=avg + [avg[0]], theta=cats + [cats[0]], name="Trung bình lớp",
                line=dict(color="#e8927c", dash="dash", width=2),
                fill="toself", fillcolor="rgba(246,199,182,0.25)",
            )
        )
        fig_radar.add_trace(
            go.Scatterpolar(
                r=mine + [mine[0]], theta=cats + [cats[0]], name=selected_student_name,
                line=dict(color=BLUE_D, width=3),
                fill="toself", fillcolor="rgba(140,196,238,0.4)",
            )
        )
        style_fig(fig_radar, 380)
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[0, 10], gridcolor="#dbe9f4", tickfont=dict(size=11)),
                angularaxis=dict(gridcolor="#dbe9f4"),
            ),
            legend=dict(orientation="h", y=-0.1, title_text=""),
        )
        st.plotly_chart(fig_radar, **PLOTLY_KW)

    with col_info:
        st.markdown("##### Tiến độ điểm số (thang 10)")
        progress_pct = float(student_info["Tong_ket"]) / 10.0 * 100
        html(
            f"""
            <div class="pbar"><div class="pfill" style="--w:{progress_pct:.0f}%"></div></div>
            <div class="pscale"><span>0</span><span>5</span><span>10</span></div>
            """
        )

        weakest = min(COMPONENTS, key=lambda c: student_info[c])
        comments = {
            "Giỏi": "Kết quả rất tốt, các thành phần điểm đều ở mức cao. Hãy duy trì phong độ này.",
            "Khá": "Kết quả khá tốt. Cải thiện thêm thành phần điểm thấp nhất sẽ giúp tiến gần mức Giỏi.",
            "Trung bình": "Đã đạt yêu cầu. Nên ôn tập thêm để nâng điểm ở các bài kiểm tra tới.",
            "Yếu": "Cần cố gắng nhiều hơn. Hãy trao đổi với giảng viên để có kế hoạch ôn tập phù hợp.",
        }
        html(
            f"""
            <div class="note">
                <b>Nhận xét tự động</b><br>
                {comments.get(student_info['Xep_loai'], '')}<br>
                Thành phần cần chú ý nhất: <b>{weakest.replace('Điểm ', '')}</b>
                ({student_info[weakest]:.1f} điểm).
            </div>
            """
        )


# ==========================================
# 9. FOOTER
# ==========================================
html(
    """
    <div class="footer">
        Hệ thống quản lý điểm sinh viên · Xây dựng với Streamlit, Pandas và Plotly
    </div>
    """
)
