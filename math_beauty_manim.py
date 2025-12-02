
from manim import *
import numpy as np

class MathBeautyScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=45*DEGREES)

        pass

        res = 161
        u = np.linspace(0, 2*np.pi, res)
        v = np.linspace(0, 2*np.pi, res)

        points = []
        for uu in u:
            for vv in v:
                x = float(np.sin(uu) * (1 + np.cos(vv)))
                y = float(np.sin(vv))
                z = float(np.cos(uu) * (1 + np.cos(vv)))
                points.append([x, y, z])

        points = np.array(points)

        # Tạo đám mây điểm bằng Dot3D + VGroup (an toàn tuyệt đối)
        cloud = VGroup()
        for p in points:
            dot = Dot3D(point=p, radius=0.04, color=YELLOW)
            cloud.add(dot)

        self.add(cloud)

        # Animation quay camera
        self.play(Rotate(self.camera.theta_tracker, angle=2*PI, run_time=8, rate_func=linear))
        self.wait()
