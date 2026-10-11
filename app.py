import pandas as pd
import plotly.express as px
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
# 2. CUSTOM CSS NÂNG CAO (KEYFRAME ANIMATIONS & GLASSMORPHISM)
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Animation Classes */
    .animate-fade {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .animate-slide {
        animation: slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Header Thiết Kế Mới */
    .main-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeIn 0.8s ease-out;
    }
    .main-header h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.3rem;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #b0bec5;
        margin-top: 8px;
        font-size: 1.05rem;
        font-weight: 400;
    }

    /* Metric Cards Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: slideUp 0.6s ease-out forwards;
    }
    .metric-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
        border-color: #cbd5e1;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 10px 0 6px 0;
    }
    .metric-subtext {
        font-size: 0.85rem;
        font-weight: 600;
    }

    .val-blue { color: #1e40af; }
    .val-green { color: #15803d; }
    .val-red { color: #b91c1c; }
    .val-purple { color: #6b21a8; }

    /* VIP Student Profile Card */
    .vip-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        animation: fadeIn 0.5s ease-in-out;
    }
    .vip-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 18px;
        margin-bottom: 22px;
    }
    .vip-title {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0f172a;
    }

    /* Badges Xếp loại */
    .badge {
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 0.3px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .badge-gioi { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .badge-kha { background-color: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
    .badge-tb { background-color: #fef3c7; color: #b45309; border: 1px solid #fde047; }
    .badge-yeu { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

    /* Developer Card Sidebar */
    .dev-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 18px;
        border-radius: 16px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .dev-card h4 {
        margin: 0 0 10px 0;
        font-size: 1.05rem;
        color: #38bdf8;
    }
    .dev-card p {
        margin: 5px 0;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 3. CHUẨN BỊ & XỬ LÝ DỮ LIỆU
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
# 4. THANH BÊN (SIDEBAR) & TÌM KIẾM AUTOCOMPLETE
# ==========================================
with st.sidebar:
  st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=75)
  st.title("⚙️ BẢNG ĐIỀU KHIỂN")
  st.markdown("---")

  st.subheader("🔍 Lọc & Tìm kiếm Autocomplete")

  # Ô tìm kiếm gợi ý danh sách tự động (Autocomplete Selectbox)
  search_options = df_students["Họ và tên"].tolist()
  selected_student_search = st.selectbox(
      "🔎 Tìm kiếm/Chọn sinh viên (Gõ chữ để gợi ý):",
      options=search_options,
      index=0,
      help=(
          "Click vào ô hoặc gõ trực tiếp chữ cái (vd: A, B, T...) để chọn"
          " nhanh sinh viên."
      ),
  )

  # Lọc theo Xếp loại
  categories = ["Tất cả xếp loại"] + list(df_students["Xep_loai"].unique())
  selected_category = st.selectbox("🏷️ Lọc theo xếp loại:", categories)

  # Xử lý dữ liệu sau lọc
  df_filtered = df_students.copy()

  if selected_student_search != "Tất cả sinh viên":
    df_filtered = df_filtered[
        df_filtered["Họ và tên"] == selected_student_search
    ]

  if selected_category != "Tất cả xếp loại":
    df_filtered = df_filtered[df_filtered["Xep_loai"] == selected_category]

  st.markdown("---")

  # Thẻ thông tin tác giả
  st.markdown(
      """
    <div class="dev-card">
        <h4>👨‍💻 THÔNG TIN TÁC GIẢ</h4>
        <p><b>Họ và tên:</b> Nguyễn Văn A</p>
        <p><b>MSSV:</b> 22110000</p>
        <p><b>Lớp:</b> Lập trình Python K63</p>
        <p><b>Trường:</b> ĐH Giao Thông Vận Tải</p>
    </div>
    """,
      unsafe_allow_html=True,
  )


# ==========================================
# 5. TIÊU ĐỀ TRANG WEB
# ==========================================
st.markdown(
    """
    <div class="main-header">
        <h1>📊 QUẢN LÝ ĐIỂM SINH VIÊN VIP</h1>
        <p>Hệ thống tự động thống kê, phân tích biểu đồ tương tác & tra cứu hồ sơ học tập</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. BO CỤC TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊 Tổng quan & Bảng điểm",
    "📈 Biểu đồ & Phân tích",
    "🔍 Tra cứu cá nhân",
])


# ------------------------------------------
# TAB 1: TỔNG QUAN & BẢNG ĐIỂM
# ------------------------------------------
with tab1:
  st.subheader("📌 Chỉ số thống kê tổng quan toàn lớp")

  avg_score = df_students["Tong_ket"].mean()
  max_student = df_students.loc[df_students["Tong_ket"].idxmax()]
  min_student = df_students.loc[df_students["Tong_ket"].idxmin()]
  passed_count = (df_students["Tong_ket"] >= 5.0).sum()
  pass_rate = (passed_count / len(df_students)) * 100

  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.markdown(
        f"""
            <div class="metric-card animate-slide">
                <div class="metric-label">Điểm TB Lớp</div>
                <div class="metric-value val-blue">{avg_score:.2f}</div>
                <div class="metric-subtext">Thang điểm 10</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with m2:
    st.markdown(
        f"""
            <div class="metric-card animate-slide">
                <div class="metric-label">Điểm Cao Nhất</div>
                <div class="metric-value val-green">{max_student['Tong_ket']}</div>
                <div class="metric-subtext">🏆 {max_student['Họ và tên']}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with m3:
    st.markdown(
        f"""
            <div class="metric-card animate-slide">
                <div class="metric-label">Điểm Thấp Nhất</div>
                <div class="metric-value val-red">{min_student['Tong_ket']}</div>
                <div class="metric-subtext">📉 {min_student['Họ và tên']}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with m4:
    st.markdown(
        f"""
            <div class="metric-card animate-slide">
                <div class="metric-label">Tỷ Lệ Đạt</div>
                <div class="metric-value val-purple">{pass_rate:.0f}%</div>
                <div class="metric-subtext">✅ {passed_count}/{len(df_students)} Sinh viên</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.write("")
  st.subheader("📋 Bảng điểm sinh viên đầy đủ")

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
# TAB 2: BIỂU ĐỒ & PHÂN TÍCH
# ------------------------------------------
with tab2:
  st.subheader("📈 Phân tích trực quan kết quả học tập")

  col_chart1, col_chart2 = st.columns([6, 4])

  color_map = {
      "Giỏi": "#15803d",
      "Khá": "#0284c7",
      "Trung bình": "#d97706",
      "Yếu": "#dc2626",
  }

  with col_chart1:
    st.markdown("##### **Biểu đồ cột điểm tổng kết từng sinh viên**")
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
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

  with col_chart2:
    st.markdown("##### **Tỷ lệ phân bổ xếp loại của lớp**")
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
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)


# ------------------------------------------
# TAB 3: TRA CỨU CÁ NHÂN
# ------------------------------------------
with tab3:
  st.subheader("🔍 Tra cứu chi tiết hồ sơ thành tích cá nhân")

  selected_student_name = st.selectbox(
      "🎯 Chọn sinh viên cần tra cứu hồ sơ:",
      options=df_students["Họ và tên"].tolist(),
      index=0,
  )

  student_info = df_students[
      df_students["Họ và tên"] == selected_student_name
  ].iloc[0]

  rank_class = "badge-yeu"
  if student_info["Xep_loai"] == "Giỏi":
    rank_class = "badge-gioi"
  elif student_info["Xep_loai"] == "Khá":
    rank_class = "badge-kha"
  elif student_info["Xep_loai"] == "Trung bình":
    rank_class = "badge-tb"

  st.markdown(
      f"""
        <div class="vip-card animate-fade">
            <div class="vip-header">
                <div>
                    <span style="font-size: 0.88rem; color: #64748b; font-weight: 600; text-transform: uppercase;">HỒ SƠ HỌC TẬP CÁ NHÂN</span>
                    <div class="vip-title">👤 {student_info['Họ và tên']}</div>
                </div>
                <div>
                    <span class="badge {rank_class}">Xếp loại: {student_info['Xep_loai']}</span>
                </div>
            </div>
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
    st.metric(
        label="🌟 ĐIỂM TỔNG KẾT",
        value=f"{student_info['Tong_ket']}",
        delta=f"{student_info['Xep_loai']}",
    )

  progress_val = float(student_info["Tong_ket"]) / 10.0
  st.write("")
  st.write("**Tiến độ hoàn thành điểm số (thang điểm 10.0):**")
  st.progress(progress_val)
