import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG WEB & THEME
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Quản Lý Điểm Sinh Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. CUSTOM CSS (TÙY CHỈNH GIAO DIỆN XỊN SÒ)
# ==========================================
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Header */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-weight: 700;
        margin: 0;
        font-size: 2.2rem;
    }
    .main-header p {
        color: #e0e6ed;
        margin-top: 8px;
        font-size: 1rem;
    }

    /* Metric Cards Custom Styling */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.88rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 8px 0 4px 0;
    }
    .metric-subtext {
        font-size: 0.82rem;
        color: #28a745;
        font-weight: 500;
    }

    /* Colors for Metrics */
    .val-blue { color: #2a5298; }
    .val-green { color: #2e7d32; }
    .val-red { color: #c62828; }
    .val-purple { color: #6a1b9a; }

    /* Profile Card for Tab 3 */
    .profile-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    .profile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    .profile-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e293b;
    }
    .badge {
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-gioi { background-color: #d1e7dd; color: #0f5132; }
    .badge-kha { background-color: #cff4fc; color: #055160; }
    .badge-tb { background-color: #fff3cd; color: #664d03; }
    .badge-yeu { background-color: #f8d7da; color: #842029; }

    /* Sidebar Developer Card */
    .dev-card {
        background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .dev-card h4 {
        margin: 0 0 10px 0;
        font-size: 1.05rem;
        color: #ffdd59;
    }
    .dev-card p {
        margin: 4px 0;
        font-size: 0.88rem;
        color: #f1f2f6;
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

  # Tính điểm tổng kết: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
  df["Tong_ket"] = (
      0.2 * df["Điểm chuyên cần"]
      + 0.3 * df["Điểm giữa kỳ"]
      + 0.5 * df["Điểm cuối kỳ"]
  ).round(2)

  # Xếp loại sinh viên
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
# 4. THANH BÊN (SIDEBAR) & BỘ LỌC TƯƠNG TÁC
# ==========================================
with st.sidebar:
  st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=80)
  st.title("⚙️ BẢNG ĐIỀU KHIỂN")

  st.subheader("🔍 Lọc dữ liệu")

  # Ô tìm kiếm tên
  search_name = st.text_input("Tìm kiếm theo tên:", placeholder="Nhập tên SV...")

  # Lọc theo Xếp loại
  categories = ["Tất cả"] + list(df_students["Xep_loai"].unique())
  selected_category = st.selectbox("Lọc theo xếp loại:", categories)

  # Áp dụng bộ lọc
  df_filtered = df_students.copy()
  if search_name:
    df_filtered = df_filtered[
        df_filtered["Họ và tên"]
        .str.lower()
        .str.contains(search_name.lower().strip())
    ]
  if selected_category != "Tất cả":
    df_filtered = df_filtered[df_filtered["Xep_loai"] == selected_category]

  st.markdown("---")

  # Thẻ thông tin người thực hiện
  st.markdown(
      """
    <div class="dev-card">
        <h4>👨‍💻 THÔNG TIN SINH VIÊN</h4>
        <p><b>Họ và tên:</b> Nguyễn Văn A</p>
        <p><b>MSSV:</b> 22110000</p>
        <p><b>Lớp:</b> Lập trình Python K63</p>
        <p><b>Trường:</b> ĐH Giao Thông Vận Tải</p>
    </div>
    """,
      unsafe_allow_html=True,
  )


# ==========================================
# 5. TIÊU ĐỀ CHÍNH CỦA ỨNG DỤNG
# ==========================================
st.markdown(
    """
    <div class="main-header">
        <h1>📊 QUẢN LÝ ĐIỂM SINH VIÊN</h1>
        <p>Hệ thống thống kê, phân tích và tra cứu kết quả học tập tự động</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. GIAO DIỆN TABS (BO CỤC 3 TAB CHUYÊN NGHIỆP)
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
  st.subheader("📌 Chỉ số thống kê toàn lớp")

  # Tính toán các chỉ số thống kê
  avg_score = df_students["Tong_ket"].mean()
  max_student = df_students.loc[df_students["Tong_ket"].idxmax()]
  min_student = df_students.loc[df_students["Tong_ket"].idxmin()]
  passed_count = (df_students["Tong_ket"] >= 5.0).sum()
  pass_rate = (passed_count / len(df_students)) * 100

  # Hiển thị 4 thẻ Metric nâng cao
  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.markdown(
        f"""
        <div class="metric-card">
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
        <div class="metric-card">
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
        <div class="metric-card">
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
        <div class="metric-card">
            <div class="metric-label">Tỷ lệ đạt</div>
            <div class="metric-value val-purple">{pass_rate:.0f}%</div>
            <div class="metric-subtext">✅ {passed_count}/{len(df_students)} Sinh viên</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.subheader("📋 Bảng điểm sinh viên đầy đủ")

  # Định dạng tô màu cho cột Xếp loại trong Pandas Styler
  def highlight_xep_loai(val):
    if val == "Giỏi":
      return "background-color: #d1e7dd; color: #0f5132; font-weight: bold;"
    elif val == "Khá":
      return "background-color: #cff4fc; color: #055160; font-weight: bold;"
    elif val == "Trung bình":
      return "background-color: #fff3cd; color: #664d03; font-weight: bold;"
    else:
      return "background-color: #f8d7da; color: #842029; font-weight: bold;"

  styled_df = df_filtered.style.applymap(
      highlight_xep_loai, subset=["Xep_loai"]
  ).format({"Tong_ket": "{:.2f}"})

  st.dataframe(styled_df, use_container_width=True, height=380)


# ------------------------------------------
# TAB 2: BIỂU ĐỒ & PHÂN TÍCH (PLOTLY INTERACTIVE)
# ------------------------------------------
with tab2:
  st.subheader("📈 Phân tích trực quan dữ liệu điểm")

  col_chart1, col_chart2 = st.columns([6, 4])

  with col_chart1:
    st.markdown("##### **Biểu đồ cột điểm tổng kết từng sinh viên**")

    # Map màu sắc riêng theo từng xếp loại
    color_map = {
        "Giỏi": "#198754",
        "Khá": "#0dcaf0",
        "Trung bình": "#ffc107",
        "Yếu": "#dc3545",
    }

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
        textposition="outside", hovertemplate="<b>%{x}</b><br>Điểm: %{y}"
    )
    fig_bar.update_layout(
        yaxis=dict(range=[0, 10.5]),
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

  with col_chart2:
    st.markdown("##### **Tỷ lệ xếp loại của lớp**")

    # Biểu đồ tròn Donut chart
    rank_counts = df_students["Xep_loai"].value_counts().reset_index()
    rank_counts.columns = ["Xếp loại", "Số lượng"]

    fig_pie = px.pie(
        rank_counts,
        names="Xếp loại",
        values="Số lượng",
        color="Xếp loại",
        color_discrete_map=color_map,
        hole=0.45,
        height=420,
    )
    fig_pie.update_traces(
        textinfo="percent+label", hovertemplate="%{label}: %{value} SV (%{percent})"
    )
    fig_pie.update_layout(
        showlegend=False, margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)


# ------------------------------------------
# TAB 3: TRA CỨU CÁ NHÂN (STUDENT PROFILE CARD)
# ------------------------------------------
with tab3:
  st.subheader("🔍 Tra cứu chi tiết học tập cá nhân")

  selected_student_name = st.selectbox(
      "Chọn sinh viên cần tra cứu:",
      options=df_students["Họ và tên"].tolist(),
      index=0,
  )

  # Lấy dữ liệu sinh viên được chọn
  student_info = df_students[
      df_students["Họ và tên"] == selected_student_name
  ].iloc[0]

  # Xác định Badge Class tương ứng
  rank_class = "badge-yeu"
  if student_info["Xep_loai"] == "Giỏi":
    rank_class = "badge-gioi"
  elif student_info["Xep_loai"] == "Khá":
    rank_class = "badge-kha"
  elif student_info["Xep_loai"] == "Trung bình":
    rank_class = "badge-tb"

  # Hiển thị Thẻ hồ sơ cá nhân
  st.markdown(
      f"""
    <div class="profile-card">
        <div class="profile-header">
            <div>
                <span style="font-size: 0.9rem; color: #6c757d;">HỒ SƠ SINH VIÊN</span>
                <div class="profile-name">👤 {student_info['Họ và tên']}</div>
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

  # Hiển thị điểm thành phần dạng Metric cột
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

  # Thanh tiến trình thể hiện điểm tổng kết
  progress_val = float(student_info["Tong_ket"]) / 10.0
  st.write("")
  st.write(f"**Tiến độ đạt thang điểm tối đa (10.0):**")
  st.progress(progress_val)
