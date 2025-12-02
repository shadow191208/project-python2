# Run: streamlit run math_beauty_app.py

import streamlit as st
import numpy as np
import subprocess
import glob
import re
import os

st.set_page_config(page_title="VẺ ĐẸP TOÁN HỌC", layout="wide")
st.title("✨ VẺ ĐẸP TOÁN HỌC – Math Beauty (Streamlit → Manim)")

if "vars" not in st.session_state:
    st.session_state.vars = {}

st.subheader("🔢 Biến số phụ (R, r, a, b, h...)")

cols = st.columns([3,1])
with cols[0]:
    to_delete = []
    for k, val in st.session_state.vars.items():
        newval = st.number_input(k, value=val)
        st.session_state.vars[k] = newval
        if st.button(f"Xóa {k}", key=f"del_{k}"):
            to_delete.append(k)
    for k in to_delete:
        del st.session_state.vars[k]

with cols[1]:
    var_new = st.text_input("Tên biến mới")
    var_val = st.number_input("Giá trị:", value=1.0)
    if st.button("+ Thêm biến"):
        if var_new.strip():
            # kiểm tra tên biến chỉ gồm chữ cái, số và dấu _
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var_new):
                st.session_state.vars[var_new] = var_val
            else:
                st.error("Tên biến không hợp lệ!")

st.markdown("---")

st.subheader("🧮 Nhập phương trình tham số (Manim)")

# Nhập các phương trình tham số
fx = st.text_input("X(u,v) =", "np.sin(u) * (1 + np.cos(v))")
fy = st.text_input("Y(u,v) =", "np.sin(v)")
fz = st.text_input("Z(u,v) =", "np.cos(u) * (1 + np.cos(v))")

# Thay thế an toàn biến u, v thành uu, vv
def safe_replace(expr):
    expr = re.sub(r'\bu\b', 'uu', expr)
    expr = re.sub(r'\bv\b', 'vv', expr)
    return expr

fx2 = safe_replace(fx)
fy2 = safe_replace(fy)
fz2 = safe_replace(fz)

res = st.slider("Độ mịn (số hạt theo mỗi chiều)", 40, 250, 120)
dot_size = st.slider("Kích thước hạt", 0.01, 0.15, 0.04)

st.markdown("---")

def generate_manim_code():
    var_init = "\n".join([f"        {k} = {v}" for k,v in st.session_state.vars.items()])

    code = f"""
from manim import *
import numpy as np

class MathBeautyScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=45*DEGREES)

{var_init if st.session_state.vars else "        pass"}

        res = {res}
        u = np.linspace(0, 2*np.pi, res)
        v = np.linspace(0, 2*np.pi, res)

        points = []
        for uu in u:
            for vv in v:
                x = float({fx2})
                y = float({fy2})
                z = float({fz2})
                points.append([x, y, z])

        points = np.array(points)

        # Tạo đám mây điểm bằng Dot3D + VGroup (an toàn tuyệt đối)
        cloud = VGroup()
        for p in points:
            dot = Dot3D(point=p, radius={dot_size}, color=YELLOW)
            cloud.add(dot)

        self.add(cloud)

        # Animation quay camera
        self.play(Rotate(self.camera.theta_tracker, angle=2*PI, run_time=8, rate_func=linear))
        self.wait()
"""
    return code


if st.button("🎥 TẠO VIDEO BẰNG MANIM"):
    # 🧹 Xóa video cũ nếu có
    old_files = glob.glob("media/videos/**/MathBeautyScene.mp4", recursive=True)
    for f in old_files:
        try:
            os.remove(f)
        except:
            pass

    # 📝 Ghi file manim code
    with open("math_beauty_manim.py", "w", encoding="utf-8") as f:
        f.write(generate_manim_code())

    st.success("📄 Đã tạo file math_beauty_manim.py")

    # 🚀 Chạy Manim render video
    cmd = [
        "manim",
        "-pqh",
        "math_beauty_manim.py",
        "MathBeautyScene"
    ]

    st.info("🎬 Đang render video bằng Manim… vui lòng chờ…")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        st.error(f"❌ Lỗi khi render Manim:\n{result.stderr}")

    else:
        # 🔎 Tìm đúng file video vừa được xuất
        generated = glob.glob("media/videos/**/MathBeautyScene.mp4", recursive=True)

        if len(generated) == 0:
            st.error("❌ Render xong nhưng không tìm thấy video!")
        else:
            video_path = generated[-1]

            st.success("🎉 VIDEO ĐÃ SẴN SÀNG!")
            st.video(video_path)

            st.info(f"📁 File video nằm tại: {video_path}")