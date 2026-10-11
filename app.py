from pathlib import Path

code = r'''import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# 1. CẤU HÌNH ỨNG DỤNG
# =========================================================
st.set_page_config(
    page_title="AURORA | Student Performance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. DESIGN SYSTEM — AURORA VIP
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #eaf1ff;
        --muted: #9aa9c6;
        --panel: rgba(17, 27, 49, .78);
        --line: rgba(148, 163, 184, .16);
        --cyan: #6ee7f9;
        --violet: #a78bfa;
        --mint: #6ee7b7;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(70, 95, 180, .22), transparent 34%),
            radial-gradient(ellipse at 88% 12%, rgba(14, 165, 233, .12), transparent 30%),
            linear-gradient(145deg, #080e1b 0%, #0b1222 48%, #10152a 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(8, 14, 27, .72); }
    [data-testid="stToolbar"] { right: 1rem; }
    .block-container { padding: 2rem 2.5rem 3rem; max-width: 1600px; }

    @keyframes silkIn {
        from { opacity: 0; transform: translate3d(0, 18px, 0) scale(.99); filter: blur(3px); }
        to { opacity: 1; transform: translate3d(0, 0, 0) scale(1); filter: blur(0); }
    }
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 rgba(110, 231, 249, 0); }
        50% { box-shadow: 0 0 24px rgba(110, 231, 249, .12); }
    }
    .main-header {
        position: relative; overflow: hidden;
        padding: 2rem 2.2rem; margin: .25rem 0 1.7rem;
        border-radius: 26px; border: 1px solid rgba(148, 163, 184, .22);
        background: linear-gradient(115deg, rgba(22, 36, 67, .96), rgba(21, 29, 55, .88) 55%, rgba(34, 30, 75, .86));
        box-shadow: 0 24px 70px rgba(0,0,0,.28), inset 0 1px rgba(255,255,255,.06);
        animation: silkIn .75s cubic-bezier(.16, 1, .3, 1) both;
    }
    .main-header:before {
        content: ""; position: absolute; width: 330px; height: 330px; right: -90px; top: -190px;
        border-radius: 50%; background: rgba(110,231,249,.13); filter: blur(5px);
    }
    .eyebrow {
        color: var(--cyan); text-transform: uppercase; letter-spacing: .2em;
        font-size: .72rem; font-weight: 800; margin-bottom: .65rem;
    }
    .main-header h1 {
        color: #f7f9ff !important; font-size: clamp(1.8rem, 3vw, 2.65rem);
        font-weight: 800; letter-spacing: -.055em; line-height: 1.15; margin: 0;
    }
    .main-header p { color: #aab8d2; margin: .75rem 0 0; font-size: .98rem; }
    .status-pill {
        display: inline-flex; align-items: center; gap: .5rem; margin-top: 1.2rem;
        padding: .45rem .8rem; border-radius: 99px; color: #baf7e2;
        background: rgba(16,185,129,.1); border: 1px solid rgba(110,231,183,.25);
        font-size: .76rem; font-weight: 700;
    }
    .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #6ee7b7; box-shadow: 0 0 12px #6ee7b7; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1426 0%, #101a30 58%, #11162a 100%);
        border-right: 1px solid rgba(148,163,184,.14);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #aab8d2; }
    .sidebar-brand {
        padding: 1rem .9rem 1.2rem; border-radius: 20px; margin-bottom: 1.3rem;
        background: linear-gradient(135deg, rgba(110,231,249,.09), rgba(167,139,250,.09));
        border: 1px solid rgba(148,163,184,.18); text-align: center;
    }
    .sidebar-brand .symbol { font-size: 2.1rem; margin-bottom: .35rem; }
    .sidebar-brand h2 {
        color: #f1f5ff; font-size: 1.03rem; line-height: 1.5; letter-spacing: .12em;
        font-weight: 800; margin: 0;
    }
    .sidebar-brand span { display:block; color: #8294b7; font-size: .68rem; letter-spacing: .16em; margin-top: .35rem; }
    [data-testid="stSidebar"] label { color: #d7e1f4 !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(7, 14, 28, .8); border: 1px solid rgba(148,163,184,.22);
        border-radius: 12px;
    }
    .dev-card {
        margin-top: 1.25rem; padding: 1.1rem; border-radius: 17px;
        background: linear-gradient(145deg, rgba(26,40,70,.95), rgba(13,21,39,.95));
        border: 1px solid rgba(148,163,184,.17); box-shadow: 0 12px 30px rgba(0,0,0,.18);
    }
    .dev-card h4 { color: var(--cyan); font-size: .82rem; letter-spacing: .08em; margin: 0 0 .8rem; }
    .dev-card p { color: #b8c5dd; font-size: .78rem; margin: .42rem 0; }

    /* Section headings and tabs */
    h2, h3, h4 { color: #edf3ff !important; letter-spacing: -.025em; }
    [data-testid="stTabs"] [role="tablist"] {
        gap: .55rem; border-bottom: 1px solid rgba(148,163,184,.16);
        padding-bottom: .45rem;
    }
    [data-testid="stTabs"] button[role="tab"] {
        color: #9eacc7; border: 1px solid transparent; border-radius: 12px;
        padding: .72rem 1rem; font-weight: 700; transition: all .28s cubic-bezier(.16,1,.3,1);
    }
    [data-testid="stTabs"] button[role="tab"]:hover {
        color: #eafaff; background: rgba(110,231,249,.07); transform: translateY(-2px);
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #d8fbff; background: linear-gradient(135deg, rgba(34,211,238,.13), rgba(139,92,246,.13));
        border-color: rgba(110,231,249,.26); box-shadow: inset 0 0 0 1px rgba(255,255,255,.02);
    }
    [data-testid="stTabs"] [role="tabpanel"] { animation: silkIn .55s cubic-bezier(.16,1,.3,1) both; padding-top: 1.2rem; }

    /* Metric cards */
    .metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 1rem; margin: .9rem 0 1.7rem; }
    .metric-card {
        position: relative; overflow: hidden; min-height: 158px; padding: 1.25rem 1.3rem;
        border-radius: 21px; border: 1px solid rgba(255,255,255,.12);
        background: linear-gradient(140deg, rgba(30,48,81,.92), rgba(17,27,49,.96));
        box-shadow: 0 12px 30px rgba(0,0,0,.17), inset 0 1px rgba(255,255,255,.04);
        transition: transform .35s cubic-bezier(.16,1,.3,1), box-shadow .35s ease, border-color .35s ease;
        animation: silkIn .65s cubic-bezier(.16,1,.3,1) both;
    }
    .metric-card:nth-child(2) { animation-delay: .08s; }
    .metric-card:nth-child(3) { animation-delay: .16s; }
    .metric-card:nth-child(4) { animation-delay: .24s; }
    .metric-card:after {
        content: attr(data-icon); position: absolute; right: 12px; bottom: -23px;
        font-size: 6.8rem; opacity: .075; line-height: 1; filter: grayscale(1);
        transform: rotate(-10deg); pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-7px) scale(1.012); border-color: rgba(110,231,249,.42);
        box-shadow: 0 22px 45px rgba(0,0,0,.28), 0 0 25px rgba(110,231,249,.09);
    }
    .metric-label { color: #aab8d2; text-transform: uppercase; letter-spacing: .11em; font-size: .72rem; font-weight: 800; }
    .metric-value { margin: .7rem 0 .35rem; font-size: 2.2rem; font-weight: 800; letter-spacing: -.06em; line-height: 1; }
    .metric-subtext { color: #9eacc7; font-size: .78rem; font-weight: 600; }
    .val-blue { color: #7dd3fc; } .val-green { color: #86efac; }
    .val-red { color: #fda4af; } .val-purple { color: #c4b5fd; }

    /* Panel and profile */
    .section-kicker { color: #8ea2c6; font-size: .72rem; letter-spacing: .16em; font-weight: 800; text-transform: uppercase; margin-bottom: .35rem; }
    .panel {
        border: 1px solid rgba(148,163,184,.16); border-radius: 20px;
        background: linear-gradient(145deg, rgba(20,32,57,.82), rgba(13,21,39,.8));
        padding: 1.15rem 1.2rem; box-shadow: 0 12px 30px rgba(0,0,0,.12);
        animation: silkIn .65s cubic-bezier(.16,1,.3,1) both;
    }
    .vip-card {
        padding: 1.5rem 1.6rem; border-radius: 23px; margin: .8rem 0 1.2rem;
        border: 1px solid rgba(110,231,249,.2);
        background: radial-gradient(circle at 90% 0%, rgba(167,139,250,.13), transparent 33%),
                    linear-gradient(135deg, rgba(24,42,73,.98), rgba(15,24,44,.98));
        box-shadow: 0 20px 48px rgba(0,0,0,.22); transition: transform .3s ease, box-shadow .3s ease;
        animation: silkIn .6s cubic-bezier(.16,1,.3,1) both;
    }
    .vip-card:hover { transform: translateY(-4px); box-shadow: 0 25px 55px rgba(0,0,0,.3), 0 0 28px rgba(110,231,249,.07); }
    .vip-header { display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap; border-bottom:1px solid rgba(148,163,184,.17); padding-bottom:1.15rem; margin-bottom:1rem; }
    .vip-title { font-size: 1.85rem; font-weight: 800; color:#f3f7ff; letter-spacing:-.045em; }
    .badge { display:inline-block; padding:.48rem .9rem; border-radius:999px; font-size:.78rem; font-weight:800; border:1px solid; }
    .badge-gioi { background:rgba(34,197,94,.13); color:#86efac; border-color:rgba(134,239,172,.35); }
    .badge-kha { background:rgba(56,189,248,.13); color:#7dd3fc; border-color:rgba(125,211,252,.35); }
    .badge-tb { background:rgba(251,191,36,.12); color:#fcd34d; border-color:rgba(252,211,77,.35); }
    .badge-yeu { background:rgba(251,113,133,.12); color:#fda4af; border-color:rgba(253,164,175,.35); }

    /* Native Streamlit widgets */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(28,43,72,.85), rgba(15,24,43,.9));
        padding: 1rem 1.1rem; border: 1px solid rgba(148,163,184,.16);
        border-radius: 17px; transition: transform .28s ease, box-shadow .28s ease;
    }
    [data-testid="stMetric"]:hover { transform: translateY(-4px); box-shadow: 0 16px 32px rgba(0,0,0,.22); }
    [data-testid="stMetricLabel"] { color: #aab8d2 !important; }
    [data-testid="stMetricValue"] { color: #eff6ff !important; }
    [data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #22d3ee, #a78bfa); }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid rgba(148,163,184,.16); border-radius: 14px; overflow: hidden; }
    .stButton button, [data-testid="baseButton-secondary"] {
        border-radius: 12px; border: 1px solid rgba(110,231,249,.3);
        background: linear-gradient(135deg, rgba(34,211,238,.12), rgba(139,92,246,.12));
        color: #eafaff; font-weight: 700; transition: all .25s cubic-bezier(.16,1,.3,1);
    }
    .stButton button:hover { transform: translateY(-2px); border-color: rgba(110,231,249,.65); box-shadow: 0 10px 25px rgba(34,211,238,.1); }
    hr { border-color: rgba(148,163,184,.14); }
    @media (max-width: 900px) {
        .block-container { padding: 1.2rem 1rem 2rem; }
        .metric-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
        .main-header { padding: 1.5rem; }
    }
    @media (max-width: 520px) { .metric-grid { grid-template-columns: 1fr; } }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 3. DỮ LIỆU & LOGIC — GIỮ NGUYÊN
# =========================================================
@st.cache_data
def get_student_data():
    data = {
        "Họ và tên": ["An", "Bình", "Chi", "Dũng", "Hà", "Lan", "Minh", "Nam", "Phúc", "Trang"],
        "Điểm chuyên cần": [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.5],
        "Điểm giữa kỳ": [8.0, 8.0, 6.0, 9.0, 7.0, 5.5, 8.0, 6.5, 7.0, 9.0],
        "Điểm cuối kỳ": [8.0, 8.5, 6.5, 9.0, 7.5, 5.5, 8.5, 7.0, 7.5, 9.0],
    }
    df = pd.DataFrame(data)

    # Công thức gốc: 20% chuyên cần + 30% giữa kỳ + 50% cuối kỳ
    df["Tong_ket"] = (
        0.2 * df["Điểm chuyên cần"]
        + 0.3 * df["Điểm giữa kỳ"]
        + 0.5 * df["Điểm cuối kỳ"]
    ).round(2)

    # Các mốc xếp loại gốc
    def phan_loai(score):
        if score >= 8.5:
            return "Giỏi"
        elif score >= 7.0:
            return "Khá"
        elif score >= 5.0:
            return "Trung bình"
        return "Yếu"

    df["Xep_loai"] = df["Tong_ket"].map(phan_loai)
    return df


df_students = get_student_data()

# =========================================================
# 4. SIDEBAR — BẢNG ĐIỀU KHIỂN
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="symbol">◈</div>
            <h2>BẢNG ĐIỀU KHIỂN</h2>
            <span>AURORA • ACADEMIC INTELLIGENCE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### 🔎 Bộ lọc thông minh")

    search_options = ["Tất cả sinh viên"] + df_students["Họ và tên"].tolist()
    selected_student_search = st.selectbox(
        "Tìm kiếm / chọn sinh viên",
        options=search_options,
        index=0,
        help="Gõ tên hoặc chữ cái để tìm nhanh sinh viên.",
    )

    categories = ["Tất cả xếp loại"] + [
        category for category in ["Giỏi", "Khá", "Trung bình", "Yếu"]
        if category in df_students["Xep_loai"].values
    ]
    selected_category = st.selectbox("Lọc theo xếp loại", categories)

    df_filtered = df_students.copy()
    if selected_student_search != "Tất cả sinh viên":
        df_filtered = df_filtered[df_filtered["Họ và tên"] == selected_student_search]
    if selected_category != "Tất cả xếp loại":
        df_filtered = df_filtered[df_filtered["Xep_loai"] == selected_category]

    st.markdown("---")
    st.markdown(
        """
        <div class="dev-card">
            <h4>✦ THÔNG TIN TÁC GIẢ</h4>
            <p><b>Họ và tên:</b> Nguyễn Văn A</p>
            <p><b>MSSV:</b> 22110000</p>
            <p><b>Lớp:</b> Lập trình Python K63</p>
            <p><b>Trường:</b> ĐH Giao Thông Vận Tải</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("AURORA UI • Student Analytics")

# =========================================================
# 5. HERO HEADER
# =========================================================
st.markdown(
    """
    <div class="main-header">
        <div class="eyebrow">Academic Intelligence Platform</div>
        <h1>QUẢN LÝ ĐIỂM SINH VIÊN <span style="color:#6ee7f9">VIP</span></h1>
        <p>Phân tích thành tích học tập, trực quan hóa dữ liệu và tra cứu hồ sơ trong một không gian cao cấp.</p>
        <div class="status-pill"><span class="status-dot"></span> HỆ THỐNG SẴN SÀNG &nbsp;·&nbsp; DỮ LIỆU 10 SINH VIÊN</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    ["◈  Tổng quan & Bảng điểm", "⌁  Biểu đồ & Phân tích", "◎  Tra cứu cá nhân"]
)

# =========================================================
# 6. TAB 1 — OVERVIEW & SCORE TABLE
# =========================================================
with tab1:
    st.markdown('<div class="section-kicker">Class overview</div>', unsafe_allow_html=True)
    st.subheader("Chỉ số thống kê tổng quan toàn lớp")

    avg_score = df_students["Tong_ket"].mean()
    max_student = df_students.loc[df_students["Tong_ket"].idxmax()]
    min_student = df_students.loc[df_students["Tong_ket"].idxmin()]
    passed_count = int((df_students["Tong_ket"] >= 5.0).sum())
    pass_rate = (passed_count / len(df_students)) * 100

    metric_items = [
        ("Điểm TB lớp", f"{avg_score:.2f}", "Thang điểm 10", "val-blue", "◉"),
        ("Điểm cao nhất", f"{max_student['Tong_ket']:.2f}", f"🏆 {max_student['Họ và tên']}", "val-green", "✦"),
        ("Điểm thấp nhất", f"{min_student['Tong_ket']:.2f}", f"↘ {min_student['Họ và tên']}", "val-red", "⌁"),
        ("Tỷ lệ đạt", f"{pass_rate:.0f}%", f"{passed_count}/{len(df_students)} sinh viên", "val-purple", "✓"),
    ]
    cards_html = '<div class="metric-grid">'
    for label, value, subtext, color_class, icon in metric_items:
        cards_html += (
            f'<div class="metric-card" data-icon="{icon}">'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value {color_class}">{value}</div>'
            f'<div class="metric-subtext">{subtext}</div></div>'
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Student records</div>', unsafe_allow_html=True)
    st.subheader("Bảng điểm sinh viên")
    st.caption(f"Đang hiển thị {len(df_filtered)} / {len(df_students)} sinh viên theo bộ lọc ở thanh điều khiển.")

    def highlight_xep_loai(val):
        styles = {
            "Giỏi": "background-color: #dcfce7; color: #166534; font-weight: 700;",
            "Khá": "background-color: #dbeafe; color: #1d4ed8; font-weight: 700;",
            "Trung bình": "background-color: #fef3c7; color: #92400e; font-weight: 700;",
            "Yếu": "background-color: #fee2e2; color: #991b1b; font-weight: 700;",
        }
        return styles.get(val, "")

    styled_df = (
        df_filtered.style
        .map(highlight_xep_loai, subset=["Xep_loai"])
        .format({"Tong_ket": "{:.2f}"})
    )
    st.dataframe(styled_df, use_container_width=True, height=390, hide_index=True)

# =========================================================
# 7. TAB 2 — CHARTS & ANALYTICS
# =========================================================
with tab2:
    st.markdown('<div class="section-kicker">Visual analytics</div>', unsafe_allow_html=True)
    st.subheader("Phân tích trực quan kết quả học tập")

    col_chart1, col_chart2 = st.columns([1.35, 1], gap="large")
    color_map = {
        "Giỏi": "#6ee7b7",
        "Khá": "#7dd3fc",
        "Trung bình": "#fcd34d",
        "Yếu": "#fda4af",
    }
    chart_font = "Plus Jakarta Sans, sans-serif"
    common_layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=chart_font, color="#dbe7ff"),
        margin=dict(l=12, r=12, t=35, b=12),
        hoverlabel=dict(
            bgcolor="#111c32", bordercolor="rgba(110,231,249,.35)",
            font=dict(family=chart_font, color="#f1f5ff", size=13),
        ),
        transition=dict(duration=450, easing="cubic-in-out"),
    )

    with col_chart1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Điểm tổng kết từng sinh viên**")
        fig_bar = px.bar(
            df_students,
            x="Họ và tên",
            y="Tong_ket",
            color="Xep_loai",
            color_discrete_map=color_map,
            text="Tong_ket",
            labels={"Tong_ket": "Điểm tổng kết", "Họ và tên": "Sinh viên", "Xep_loai": "Xếp loại"},
            height=420,
            category_orders={"Họ và tên": df_students["Họ và tên"].tolist()},
        )
        fig_bar.update_traces(
            textposition="outside",
            texttemplate="%{y:.2f}",
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Điểm tổng kết: %{y:.2f}<br>Xếp loại: %{fullData.name}<extra></extra>",
        )
        fig_bar.update_layout(**common_layout, bargap=.34, showlegend=True, legend_title_text="")
        fig_bar.update_xaxes(showgrid=False, zeroline=False, title=None, tickfont=dict(size=11))
        fig_bar.update_yaxes(
            range=[0, 10.6], title="Điểm số", showgrid=False,
            zeroline=False, ticksuffix="  ",
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Cơ cấu xếp loại của lớp**")
        rank_order = ["Giỏi", "Khá", "Trung bình", "Yếu"]
        rank_counts = (
            df_students["Xep_loai"].value_counts()
            .reindex(rank_order, fill_value=0)
            .rename_axis("Xếp loại")
            .reset_index(name="Số lượng")
        )
        rank_counts = rank_counts[rank_counts["Số lượng"] > 0]
        fig_pie = px.pie(
            rank_counts,
            names="Xếp loại",
            values="Số lượng",
            color="Xếp loại",
            color_discrete_map=color_map,
            hole=.68,
            height=420,
        )
        fig_pie.update_traces(
            textinfo="percent",
            textfont=dict(size=13, color="#f1f5ff"),
            marker=dict(line=dict(color="#10182b", width=3)),
            hovertemplate="<b>%{label}</b><br>%{value} sinh viên · %{percent}<extra></extra>",
            sort=False,
        )
        fig_pie.update_layout(**common_layout, showlegend=True, legend_title_text="")
        fig_pie.update_layout(legend=dict(orientation="h", y=-.05, x=.5, xanchor="center"))
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Gợi ý: rê chuột lên từng cột hoặc lát biểu đồ để xem chi tiết.")

# =========================================================
# 8. TAB 3 — STUDENT PROFILE
# =========================================================
with tab3:
    st.markdown('<div class="section-kicker">Individual student profile</div>', unsafe_allow_html=True)
    st.subheader("Tra cứu chi tiết hồ sơ thành tích cá nhân")

    selected_student_name = st.selectbox(
        "Chọn sinh viên cần tra cứu hồ sơ:",
        options=df_students["Họ và tên"].tolist(),
        index=0,
        key="profile_student",
    )
    student_info = df_students[df_students["Họ và tên"] == selected_student_name].iloc[0]

    rank_class = {
        "Giỏi": "badge-gioi",
        "Khá": "badge-kha",
        "Trung bình": "badge-tb",
        "Yếu": "badge-yeu",
    }.get(student_info["Xep_loai"], "badge-yeu")

    st.markdown(
        f"""
        <div class="vip-card">
            <div class="vip-header">
                <div>
                    <div class="section-kicker">Personal academic record</div>
                    <div class="vip-title">◉ &nbsp;{student_info['Họ và tên']}</div>
                    <div style="color:#9eacc7;font-size:.86rem;margin-top:.35rem;">Hồ sơ thành tích học tập · Thang điểm 10</div>
                </div>
                <span class="badge {rank_class}">Xếp loại: {student_info['Xep_loai']}</span>
            </div>
            <div style="color:#aab8d2;font-size:.84rem;">ĐIỂM TỔNG KẾT</div>
            <div style="font-size:3.1rem;font-weight:800;letter-spacing:-.06em;color:#8be9f8;line-height:1.2;">
                {student_info['Tong_ket']:.2f}<span style="font-size:1rem;color:#7f91b3;font-weight:600;"> / 10.00</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_cc, c_gk, c_ck, c_tk = st.columns(4, gap="medium")
    with c_cc:
        st.metric("🎯 Điểm chuyên cần", f"{student_info['Điểm chuyên cần']:.1f}", "Trọng số 20%")
    with c_gk:
        st.metric("📝 Điểm giữa kỳ", f"{student_info['Điểm giữa kỳ']:.1f}", "Trọng số 30%")
    with c_ck:
        st.metric("✍️ Điểm cuối kỳ", f"{student_info['Điểm cuối kỳ']:.1f}", "Trọng số 50%")
    with c_tk:
        st.metric("🌟 Điểm tổng kết", f"{student_info['Tong_ket']:.2f}", student_info["Xep_loai"])

    st.markdown("**Tiến độ điểm tổng kết trên thang điểm 10**")
    st.progress(float(student_info["Tong_ket"]) / 10.0)

    with st.expander("Xem cách tính điểm của sinh viên"):
        st.latex(
            r"\text{Tổng kết} = 0.2 \times \text{Chuyên cần}"
            r" + 0.3 \times \text{Giữa kỳ} + 0.5 \times \text{Cuối kỳ}"
        )
        st.write(
            f"= 0.2 × {student_info['Điểm chuyên cần']:.1f}"
            f" + 0.3 × {student_info['Điểm giữa kỳ']:.1f}"
            f" + 0.5 × {student_info['Điểm cuối kỳ']:.1f}"
            f" = **{student_info['Tong_ket']:.2f}**"
        )

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#7183a5;font-size:.75rem;padding:.25rem 0 1rem;">'
    'AURORA STUDENT ANALYTICS · Designed for clarity, built for insight</div>',
    unsafe_allow_html=True,
)
'''
out = Path("/mnt/data/app.py")
out.write_text(code, encoding="utf-8")
print(f"Đã tạo {out} ({out.stat().st_size:,} bytes)")
