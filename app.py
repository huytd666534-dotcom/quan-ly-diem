import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG WEB EXECUTIVE VIP
# ==========================================
st.set_page_config(
    page_title="Executive Grade Management Dashboard VIP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. CUSTOM CSS GLASSMORPHISM & SLATE NAVY THEME
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0284c7 100%);
        padding: 32px;
        border-radius: 20px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeIn 0.8s ease-out;
    }
    .main-header h1 {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 2.4rem;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 8px;
        font-weight: 400;
    }

    .metric-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        text-align: center;
        animation: slideUp 0.6s ease-out forwards;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.12);
    }
    .card-accent-blue { border-left: 5px solid #0284c7; }
    .card-accent-green { border-left: 5px solid #10b981; }
    .card-accent-red { border-left: 5px solid #f43f5e; }
    .card-accent-purple { border-left: 5px solid #8b5cf6; }

    .metric-label {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 8px 0 4px 0;
    }
    .metric-subtext {
        font-size: 0.85rem;
        font-weight: 600;
    }

    .txt-blue { color: #0284c7; }
    .txt-green { color: #10b981; }
    .txt-red { color: #f43f5e; }
    .txt-purple { color: #8b5cf6; }

    .executive-profile {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 20px;
        padding: 28px;
        color: white;
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
        animation: fadeIn 0.6s ease-out;
    }
    .profile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 16px;
        margin-bottom: 20px;
    }
    .profile-name {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f8fafc;
    }

    .badge-pill {
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 700;
        display: inline-block;
    }
    .pill-gioi { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .pill-kha { background-color: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
    .pill-tb { background-color: #fef3c7; color: #b45309; border: 1px solid #fde047; }
    .pill-yeu { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

    .dev-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px;
        border-radius: 14px;
        margin-top: 20px;
        color: #cbd5e1;
    }
    .dev-card h4 {
        margin: 0 0 8px 0;
        font-size: 0.95rem;
        color: #38bdf8;
    }
    .dev-card p {
        margin: 4px 0;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 3. CHUẨN BỊ DỮ LIỆU
# ==========================================
@st.cache_data
def get_student_data():
    data = {
        "Họ và tên": [
            "An", "Bình", "Chi", "Dũng", "Hà",
            "Lan", "Minh", "Nam", "Phúc", "Trang"
        ],
        "Điểm chuyên cần": [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.5],
        "Điểm giữa kỳ": [8.0, 8.0, 6.0, 9.0, 7.0, 5.5, 8.0, 6.5, 7.0, 9.0],
        "Điểm cuối kỳ": [8.0, 8.5, 6.5, 9.0, 7.5, 5.5, 8.5, 7.0, 7.5, 9.0],
    }
    df = pd.DataFrame(data)

    df["Tong_ket"] = (
        0.2 * df["Điểm chuyên cần"]
        + 0.3 * df["Điểm giữa kỳ"]
        + 0.5 * df["Điểm cuối kỳ"]
    ).round(2)

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
    return df

df_students = get_student_data()


# ==========================================
# 4. THANH BÊN (SIDEBAR) - Ô TÌM KIẾM ĐỂ TRỐNG MẶC ĐỊNH
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=70)
    st.title("⚙️ EXECUTIVE CONTROL")
    st.markdown("---")

    st.subheader("🔍 Lọc & Tìm kiếm")

    student_names = df_students["Họ and tên"].tolist() if "Họ and tên" in df_students else df_students["Họ và tên"].tolist()

    # Bọc Try/Except giúp tương thích hoàn toàn với tham số index=None trên Streamlit
    try:
        selected_student_search = st.selectbox(
            "Tìm kiếm tên sinh viên:",
            options=student_names,
            index=None,
            placeholder="🔍 Nhập hoặc chọn tên sinh viên...",
            help="Click vào ô và gõ chữ cái để hiển thị danh sách gợi ý. Bỏ trống để chọn toàn bộ."
        )
    except Exception:
        fallback_options = ["-- Tất cả sinh viên --"] + student_names
        sel = st.selectbox("Tìm kiếm tên sinh viên:", options=fallback_options)
        selected_student_search = None if sel == "-- Tất cả sinh viên --" else sel

    selected_category = st.selectbox(
        "🏷️ Lọc theo xếp loại:",
        options=["Tất cả xếp loại", "Giỏi", "Khá", "Trung bình", "Yếu"],
        index=0,
    )

    # Logic lọc dữ liệu
    df_filtered = df_students.copy()

    if selected_student_search is not None:
        df_filtered = df_filtered[df_filtered["Họ và tên"] == selected_student_search]

    if selected_category != "Tất cả xếp loại":
        df_filtered = df_filtered[df_filtered["Xep_loai"] == selected_category]

    st.markdown("---")
    st.markdown(
        """
        <div class="dev-card">
            <h4>👨‍💻 THÔNG TIN QUẢN TRỊ</h4>
            <p><b>Hệ thống:</b> Executive Dashboard VIP</p>
            <p><b>Phiên bản:</b> 3.0 Enterprise</p>
            <p><b>Trạng thái:</b> Hoạt động ổn định</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 5. TIÊU ĐỀ HỆ THỐNG
# ==========================================
st.markdown(
    """
    <div class="main-header">
        <h1>📊 HỆ THỐNG QUẢN LÝ ĐIỂM EXECUTIVE VIP</h1>
        <p>Trung tâm phân tích học tập, báo cáo hiệu suất và tra cứu điểm thông minh</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. BỐ CỤC 3 TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊 Tổng Quan & Bảng Điểm",
    "📈 Biểu Đồ & Phân Tích",
    "🔍 Tra Cứu Hồ Sơ Học Tập VIP",
])


# ------------------------------------------
# TAB 1: TỔNG QUAN & BẢNG ĐIỂM
# ------------------------------------------
with tab1:
    st.subheader("📌 Chỉ số hiệu suất lớp học")

    avg_score = df_students["Tong_ket"].mean()
    max_student = df_students.loc[df_students["Tong_ket"].idxmax()]
    min_student = df_students.loc[df_students["Tong_ket"].idxmin()]
    passed_count = (df_students["Tong_ket"] >= 5.0).sum()
    pass_
