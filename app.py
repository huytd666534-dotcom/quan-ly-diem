import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG WEB EXECUTIVE
# ==========================================
st.set_page_config(
    page_title="Executive Grade Management Dashboard",
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

    /* Keyframe Animations */
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    /* Main Container & Header */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0284c7 100%);
        padding: 32px;
        border-radius: 20px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
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

    /* Executive Metric Cards */
    .metric-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.05), 0 4px 6px -4px rgba(15, 23, 42, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: slideUp 0.6s ease-out forwards;
    }
    .metric-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.12);
        border-color: #cbd5e1;
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
        color: #0f172a;
    }
    .metric-subtext {
        font-size: 0.85rem;
        font-weight: 600;
    }

    .txt-blue { color: #0284c7; }
    .txt-green { color: #10b981; }
    .txt-red { color: #f43f5e; }
    .txt-purple { color: #8b5cf6; }

    /* Executive Student Profile Card */
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

    /* Badges Xếp loại Pill-tag */
    .badge-pill {
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 0.3px;
    }
    .pill-gioi { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .pill-kha { background-color: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
    .pill-tb { background-color: #fef3c7; color: #b45309; border: 1px solid #fde047; }
    .pill-yeu { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

    /* Sidebar Styling */
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
          "An",
          "Bình",
          "Chi",
          "Dũng",
          "Hà",
          "Lan",
          "Minh",
          "Nam",
          "Phúc",
          "Trang",
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
  return df


df_students = get_student_data()


# ==========================================
# 4. THANH BÊN (SIDEBAR) - TÌM KIẾM ĐỂ TRỐNG MẶC ĐỊNH
# ==========================================
with st.sidebar:
  st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=70)
  st.title("⚙️ EXECUTIVE CONTROL")
  st.markdown("---")

  st.subheader("🔍 Lọc & Tìm kiếm")

  # Ô tìm kiếm ĐỂ TRỐNG MẶC ĐỊNH (index=None, placeholder chuẩn)
  selected_student_search = st.selectbox(
      "Tìm kiếm tên sinh viên:",
      options=df_students["Họ và tên"].tolist(),
      index=None,
      placeholder="🔍 Nhập hoặc chọn tên sinh viên...",
      help="Gõ chữ cái để lọc danh sách gợi ý. Bỏ trống để xem toàn bộ danh sách.",
  )

  # Bộ lọc xếp loại
  selected_category = st.selectbox(
      "🏷️ Lọc theo xếp loại:",
      options=["Tất cả xếp loại", "Giỏi", "Khá", "Trung bình", "Yếu"],
      index=0,
  )

  # Xử lý logic lọc
  df_filtered = df_students.copy()

  # Khi ô tìm kiếm KHÔNG trống -> lọc theo tên sinh viên được chọn
  if selected_student_search is not None:
    df_filtered = df_filtered[
        df_filtered["Họ và tên"] == selected_student_search
    ]

  # Lọc theo nhóm xếp loại
  if selected_category != "Tất cả xếp loại":
    df_filtered = df_filtered[df_filtered["Xep_loai"] == selected_category]

  st.markdown("---")
  st.markdown(
      """
    <div class="dev-card">
        <h4>👨‍💻 THÔNG TIN QUẢN TRỊ</h4>
        <p><b>Hệ thống:</b> Executive Dashboard</p>
        <p><b>Phiên bản:</b> 3.0 Enterprise</p>
        <p><b>Trạng thái:</b> Tự động cập nhật</p>
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
        <h1>📊 HỆ THỐNG QUẢN LÝ ĐIỂM EXECUTIVE</h1>
        <p>Trung tâm phân tích học tập, báo cáo hiệu suất và tra cứu điểm thông minh</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. BỐ CỤC 3 TABS EXECUTIVE
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
  pass_rate = (passed_count / len(df_students)) * 100

  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.markdown(
        f"""
        <div class="metric-card card-accent-blue">
            <div class="metric-label">Điểm TB Lớp</div>
            <div class="metric-value txt-blue">{avg_score:.2f}</div>
            <div class="metric-subtext">Thang điểm 10.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with m2:
    st.markdown(
        f"""
        <div class="metric-card card-accent-green">
            <div class="metric-label">Điểm Cao Nhất</div>
            <div class="metric-value txt-green">{max_student['Tong_ket']}</div>
            <div class="metric-subtext">🏆 {max_student['Họ và tên']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with m3:
    st.markdown(
        f"""
        <div class="metric-card card-accent-red">
            <div class="metric-label">Điểm Thấp Nhất</div>
            <div class="metric-value txt-red">{min_student['Tong_ket']}</div>
            <div class="metric-subtext">📉 {min_student['Họ và tên']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with m4:
    st.markdown(
        f"""
        <div class="metric-card card-accent-purple">
            <div class="metric-label">Tỷ Lệ Đạt</div>
            <div class="metric-value txt-purple">{pass_rate:.0f}%</div>
            <div class="metric-subtext">✅ {passed_count}/{len(df_students)} Sinh viên</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.write("")
  st.subheader("📋 Bảng điểm chi tiết sinh viên")

  # Style ô xếp loại với hàm map tương thích Pandas mới nhất
  def highlight_xep_loai(val):
    if val == "Giỏi":
      return "background-color: #dcfce7; color: #15803d; font-weight: bold;"
    elif val == "Khá":
      return "background-color: #e0f2fe; color: #0369a1; font-weight: bold;"
    elif val == "Trung bình":
      return "background-color: #fef3c7; color: #b45309; font-weight: bold;"
    else:
      return "background-color: #fee2e2; color: #b91c1c; font-weight: bold;"

  styled_df = df_filtered.style.map(
      highlight_xep_loai, subset=["Xep_loai"]
  ).format({"Tong_ket": "{:.2f}"})

  st.dataframe(styled_df, use_container_width=True, height=380)


# ------------------------------------------
# TAB 2: BIỂU ĐỒ & PHÂN TÍCH PLOTLY
# ------------------------------------------
with tab2:
  st.subheader("📈 Phân tích trực quan dữ liệu")

  col_chart1, col_chart2 = st.columns([6, 4])

  color_map = {
      "Giỏi": "#10b981",
      "Khá": "#0284c7",
      "Trung bình": "#f59e0b",
      "Yếu": "#f43f5e",
  }

  with col_chart1:
    st.markdown("##### **Phân bố điểm tổng kết từng sinh viên**")
    fig_bar = px.bar(
        df_students,
        x="Họ và tên",
        y="Tong_ket",
        color="Xep_loai",
        color_discrete_map=color_map,
        text="Tong_ket",
        labels={
            "Tong_ket": "Điểm tổng kết",
            "Họ và tên": "Sinh viên",
            "Xep_loai": "Xếp loại",
        },
        height=420,
    )
    fig_bar.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Điểm tổng kết: %{y}<extra></extra>",
    )
    fig_bar.update_layout(
        yaxis=dict(range=[0, 10.5], title="Điểm số"),
        xaxis=dict(title="Sinh viên"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(family="Plus Jakarta Sans, sans-serif"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

  with col_chart2:
    st.markdown("##### **Tỷ lệ phần trăm xếp loại**")
    rank_counts = df_students["Xep_loai"].value_counts().reset_index()
    rank_counts.columns = ["Xếp loại", "Số lượng"]

    fig_pie = px.pie(
        rank_counts,
        names="Xếp loại",
        values="Số lượng",
        color="Xếp loại",
        color_discrete_map=color_map,
        hole=0.5,
        height=420,
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b>: %{value} SV (%{percent})<extra></extra>",
    )
    fig_pie.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(family="Plus Jakarta Sans, sans-serif"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)


# ------------------------------------------
# TAB 3: TRA CỨU HỒ SƠ HỌC TẬP VIP
# ------------------------------------------
with tab3:
  st.subheader("🔍 Tra cứu thẻ hồ sơ thành tích cá nhân")

  # Tra cứu cá nhân ở Tab 3 cũng có placeholder trống mặc định
  selected_student_vip = st.selectbox(
      "🎯 Chọn tên sinh viên để xem hồ sơ chi tiết:",
      options=df_students["Họ và tên"].tolist(),
      index=0,
  )

  student_info = df_students[
      df_students["Họ và tên"] == selected_student_vip
  ].iloc[0]

  pill_class = "pill-yeu"
  if student_info["Xep_loai"] == "Giỏi":
    pill_class = "pill-gioi"
  elif student_info["Xep_loai"] == "Khá":
    pill_class = "pill-kha"
  elif student_info["Xep_loai"] == "Trung bình":
    pill_class = "pill-tb"

  # Thẻ hồ sơ cá nhân sang trọng phong cách Executive
  st.markdown(
      f"""
        <div class="executive-profile">
            <div class="profile-header">
                <div>
                    <span style="font-size: 0.82rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">EXECUTIVE STUDENT PROFILE</span>
                    <div class="profile-name">👤 {student_info['Họ và tên']}</div>
                </div>
                <div>
                    <span class="badge-pill {pill_class}">Xếp loại: {student_info['Xep_loai']}</span>
                </div>
            </div>
            <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Mã hồ sơ: <b>SV-{student_info['Họ và tên'].upper()}-2026</b> | Hệ đào tạo: Chính quy</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")

  c_cc, c_gk, c_ck, c_tk = st.columns(4)
  with c_cc:
    st.metric(
        label="🎯 Điểm Chuyên Cần (20%)", value=f"{student_info['Điểm chuyên cần']}"
    )
  with c_gk:
    st.metric(
        label="📝 Điểm Giữa Kỳ (30%)", value=f"{student_info['Điểm giữa kỳ']}"
    )
  with c_ck:
    st.metric(
        label="✍️ Điểm Cuối Kỳ (50%)", value=f"{student_info['Điểm cuối kỳ']}"
    )
  with c_tk:
    st
