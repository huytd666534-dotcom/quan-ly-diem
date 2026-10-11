import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên", layout="wide"
)

# 1. Hiển thị tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Chuẩn bị dữ liệu[cite: 1]
data = {
    'Họ và tên': [
        'An',
        'Bình',
        'Chi',
        'Dũng',
        'Hà',
        'Lan',
        'Minh',
        'Nam',
        'Phúc',
        'Trang',
    ],
    'Điểm chuyên cần': [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.5],
    'Điểm giữa kỳ': [8.0, 8.0, 6.0, 9.0, 7.0, 5.5, 8.0, 6.5, 7.0, 9.0],
    'Điểm cuối kỳ': [8.0, 8.5, 6.5, 9.0, 7.5, 5.5, 8.5, 7.0, 7.5, 9.0],
}
df = pd.DataFrame(data)

# Tính điểm tổng kết và xếp loại[cite: 1]
df['Tong_ket'] = (
    0.2 * df['Điểm chuyên cần']
    + 0.3 * df['Điểm giữa kỳ']
    + 0.5 * df['Điểm cuối kỳ']
).round(2)


def phan_loai(diem):
  if diem >= 8.5:
    return 'Giỏi'
  elif diem >= 7.0:
    return 'Khá'
  elif diem >= 5.0:
    return 'Trung bình'
  else:
    return 'Yếu'


df['Xep_loai'] = df['Tong_ket'].apply(phan_loai)

# 3. Hiển thị bảng điểm[cite: 2]
st.subheader('📋 Bảng điểm sinh viên')
st.dataframe(df, use_container_width=True)

# 4. Hiển thị thông tin thống kê[cite: 2]
st.subheader('📊 Thống kê chung')
diem_tb = df['Tong_ket'].mean()
sv_max = df.loc[df['Tong_ket'].idxmax()]
sv_min = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Điểm TB cả lớp", f"{diem_tb:.2f}")
c2.metric("Cao nhất", f"{sv_max['Tong_ket']} ({sv_max['Họ và tên']})")
c3.metric("Thấp nhất", f"{sv_min['Tong_ket']} ({sv_min['Họ và tên']})")
c4.metric("Số sinh viên đạt", f"{so_sv_dat}/{len(df)}")

# 5. Danh sách chọn sinh viên (Selectbox) tra cứu[cite: 2]
st.subheader('🔍 Tra cứu thông tin từng sinh viên')
selected_student = st.selectbox(
    'Chọn sinh viên để xem chi tiết:', options=df['Họ và tên'].tolist()
)

sv_info = df[df['Họ và tên'] == selected_student].iloc[0]

col_a, col_b, col_c, col_d, col_e = st.columns(5)
col_a.metric("Chuyên cần", sv_info['Điểm chuyên cần'])
col_b.metric("Giữa kỳ", sv_info['Điểm giữa kỳ'])
col_c.metric("Cuối kỳ", sv_info['Điểm cuối kỳ'])
col_d.metric("Tổng kết", sv_info['Tong_ket'])
col_e.metric("Xếp loại", sv_info['Xep_loai'])

# 6. Biểu đồ cột điểm tổng kết[cite: 2]
st.subheader('📈 Biểu đồ điểm tổng kết')
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df['Họ và tên'], df['Tong_ket'], color='#3182bd')
ax.set_ylabel('Điểm tổng kết')
ax.set_ylim(0, 10)
for i, val in enumerate(df['Tong_ket']):
  ax.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=8)
st.pyplot(fig)

# 7. Thông tin người thực hiện ở chân trang[cite: 2]
st.markdown('---')
st.caption('Người thực hiện: Nguyễn Văn A | MSSV: 12345678')