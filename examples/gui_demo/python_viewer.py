#!/usr/bin/env python3
"""
OpenRoboOLP Python 3D Viewer (Minimal Demo)
A lightweight alternative using PySide6 + OpenGL, no C++ compilation needed.

Usage:
    python examples/gui_demo/python_viewer.py models/ur/test_6dof.urdf
"""

import sys
import numpy as np
from pathlib import Path

try:
    from PySide6 import QtWidgets, QtCore, QtOpenGLWidgets, QtOpenGL
    from PySide6.QtCore import Qt
except ImportError:
    print("PySide6 not installed. Install with: pip install PySide6")
    sys.exit(1)

# Simple OpenGL robot renderer
class RobotRenderer:
    def __init__(self):
        self.links = []
        self.joint_values = [0.0] * 6

    def load_urdf(self, path):
        """Parse URDF and create primitive geometries."""
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        self.links = []
        for link in root.findall("link"):
            name = link.get("name")
            visual = link.find("visual")
            if visual is None:
                continue

            geom = visual.find("geometry")
            mat = visual.find("material/color") if visual.find("material") else None
            rgba = [0.7, 0.7, 0.75, 1.0]
            if mat is not None:
                rgba_str = mat.get("rgba", "0.7 0.7 0.75 1")
                rgba = [float(x) for x in rgba_str.split()]

            origin = visual.find("origin")
            xyz = [0, 0, 0]
            if origin is not None:
                xyz_str = origin.get("xyz", "0 0 0")
                xyz = [float(x) for x in xyz_str.split()]

            # Create primitive based on geometry type
            if geom.find("cylinder") is not None:
                cyl = geom.find("cylinder")
                r = float(cyl.get("radius", "0.03"))
                l = float(cyl.get("length", "0.15"))
                self.links.append({
                    "name": name,
                    "type": "cylinder",
                    "params": (r, l),
                    "origin": xyz,
                    "color": rgba[:3],
                })
            elif geom.find("box") is not None:
                box = geom.find("box")
                size = [float(x) for x in box.get("size", "0.1 0.1 0.1").split()]
                self.links.append({
                    "name": name,
                    "type": "box",
                    "params": tuple(size),
                    "origin": xyz,
                    "color": rgba[:3],
                })
            elif geom.find("sphere") is not None:
                sph = geom.find("sphere")
                r = float(sph.get("radius", "0.02"))
                self.links.append({
                    "name": name,
                    "type": "sphere",
                    "params": (r,),
                    "origin": xyz,
                    "color": rgba[:3],
                })

        print(f"Loaded {len(self.links)} links from URDF")
        return len(self.links) > 0

    def set_joints(self, q):
        self.joint_values = list(q)

class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = RobotRenderer()
        self.camera_dist = 1.5
        self.camera_az = 45.0
        self.camera_el = 30.0
        self.dragging = False
        self.last_pos = None

    def load_robot(self, path):
        return self.renderer.load_urdf(path)

    def set_joints(self, q):
        self.renderer.set_joints(q)
        self.update()

    def initializeGL(self):
        gl = self.context().functions()
        gl.glClearColor(0.15, 0.15, 0.18, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def paintGL(self):
        gl = self.context().functions()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Setup projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = self.width() / max(1, self.height())
        from PySide6.QtOpenGL import QGLWidget
        # Use fixed-function pipeline for simplicity
        import math

        # Simple perspective
        fov = 45.0
        near = 0.01
        far = 100.0
        top = near * math.tan(math.radians(fov / 2))
        right = top * aspect
        gl.glFrustum(-right, right, -top, top, near, far)

        # View matrix
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        az = math.radians(self.camera_az)
        el = math.radians(self.camera_el)
        cx = self.camera_dist * math.cos(el) * math.cos(az)
        cy = self.camera_dist * math.cos(el) * math.sin(az)
        cz = self.camera_dist * math.sin(el)
        gl.gluLookAt(cx, cy, cz, 0, 0, 0.5, 0, 0, 1)

        # Draw grid
        self._draw_grid(gl)

        # Draw robot
        self._draw_robot(gl)

    def _draw_grid(self, gl):
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(0.3, 0.3, 0.35)
        size = 1.0
        steps = 20
        for i in range(steps + 1):
            x = -size + 2 * size * i / steps
            gl.glVertex3f(x, -size, 0)
            gl.glVertex3f(x, size, 0)
            gl.glVertex3f(-size, x, 0)
            gl.glVertex3f(size, x, 0)
        gl.glEnd()

    def _draw_robot(self, gl):
        import math
        q = self.renderer.joint_values

        # Simple serial chain visualization
        gl.glPushMatrix()
        gl.glTranslatef(0, 0, 0)

        for i, link in enumerate(self.renderer.links):
            gl.glColor3f(*link["color"])

            if link["type"] == "cylinder":
                r, l = link["params"]
                self._draw_cylinder(gl, r, l)
                gl.glTranslatef(0, 0, l)
            elif link["type"] == "box":
                w, h, d = link["params"]
                self._draw_box(gl, w, h, d)
                gl.glTranslatef(0, 0, d)
            elif link["type"] == "sphere":
                r = link["params"][0]
                self._draw_sphere(gl, r)
                gl.glTranslatef(0, 0, r * 2)

            # Apply joint rotation (simplified: all rotate around Z)
            if i < len(q):
                gl.glRotatef(math.degrees(q[i]), 0, 0, 1)

        gl.glPopMatrix()

    def _draw_cylinder(self, gl, radius, length):
        import math
        segments = 16
        gl.glBegin(gl.GL_QUADS)
        for i in range(segments):
            a1 = 2 * math.pi * i / segments
            a2 = 2 * math.pi * (i + 1) / segments
            x1 = radius * math.cos(a1)
            y1 = radius * math.sin(a1)
            x2 = radius * math.cos(a2)
            y2 = radius * math.sin(a2)
            gl.glNormal3f(x1, y1, 0)
            gl.glVertex3f(x1, y1, 0)
            gl.glVertex3f(x1, y1, length)
            gl.glNormal3f(x2, y2, 0)
            gl.glVertex3f(x2, y2, length)
            gl.glVertex3f(x2, y2, 0)
        gl.glEnd()

    def _draw_box(self, gl, w, h, d):
        x, y, z = w/2, h/2, d/2
        gl.glBegin(gl.GL_QUADS)
        # Front
        gl.glNormal3f(0, 0, 1)
        gl.glVertex3f(-x, -y, z); gl.glVertex3f(x, -y, z)
        gl.glVertex3f(x, y, z); gl.glVertex3f(-x, y, z)
        # Back
        gl.glNormal3f(0, 0, -1)
        gl.glVertex3f(-x, -y, -z); gl.glVertex3f(-x, y, -z)
        gl.glVertex3f(x, y, -z); gl.glVertex3f(x, -y, -z)
        gl.glEnd()

    def _draw_sphere(self, gl, radius):
        import math
        # Approximate with small box for simplicity
        self._draw_box(gl, radius*2, radius*2, radius*2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging and self.last_pos:
            dx = event.pos().x() - self.last_pos.x()
            dy = event.pos().y() - self.last_pos.y()
            self.camera_az -= dx * 0.5
            self.camera_el += dy * 0.5
            self.camera_el = max(-89, min(89, self.camera_el))
            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.camera_dist *= 0.9 ** delta
        self.camera_dist = max(0.3, min(10.0, self.camera_dist))
        self.update()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, urdf_path=None):
        super().__init__()
        self.setWindowTitle("OpenRoboOLP Python Viewer v0.1.0")
        self.resize(1200, 800)

        # Central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # GL Widget
        self.gl_widget = GLWidget(self)
        layout.addWidget(self.gl_widget, 1)

        # Control panel
        panel = QtWidgets.QWidget(self)
        panel.setMaximumWidth(350)
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.addWidget(QtWidgets.QLabel("<h2>Joint Control</h2>"))

        self.sliders = []
        self.value_labels = []

        # Load robot
        if urdf_path and Path(urdf_path).exists():
            self.load_robot(urdf_path)

        layout.addWidget(panel)
        self.panel = panel

    def load_robot(self, path):
        if not self.gl_widget.load_robot(path):
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load URDF: {path}")
            return

        # Create sliders
        # Clear old
        while self.panel.layout().count() > 1:
            item = self.panel.layout().takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        self.sliders.clear()
        self.value_labels.clear()

        for i in range(len(self.gl_widget.renderer.links)):
            row = QtWidgets.QWidget(self.panel)
            row_layout = QtWidgets.QHBoxLayout(row)

            label = QtWidgets.QLabel(f"J{i+1}:", row)
            row_layout.addWidget(label)

            slider = QtWidgets.QSlider(Qt.Horizontal, row)
            slider.setRange(-1800, 1800)  # -180 to 180 degrees, *10 for precision
            slider.setValue(0)
            row_layout.addWidget(slider, 1)

            val_label = QtWidgets.QLabel("0.0°", row)
            val_label.setMinimumWidth(50)
            row_layout.addWidget(val_label)

            self.panel.layout().addWidget(row)
            self.sliders.append(slider)
            self.value_labels.append(val_label)

            slider.valueChanged.connect(lambda v, lbl=val_label, idx=i: self.on_joint_changed(v, lbl, idx))

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        zero_btn = QtWidgets.QPushButton("Zero All")
        home_btn = QtWidgets.QPushButton("Home Pose")
        btn_layout.addWidget(zero_btn)
        btn_layout.addWidget(home_btn)
        self.panel.layout().addLayout(btn_layout)

        zero_btn.clicked.connect(self.zero_all)
        home_btn.clicked.connect(self.home_pose)
        self.panel.layout().addStretch()

    def on_joint_changed(self, value, label, idx):
        deg = value / 10.0
        label.setText(f"{deg:.1f}°")
        q = [s.value() / 10.0 * math.pi / 180.0 for s in self.sliders]
        self.gl_widget.set_joints(q)

    def zero_all(self):
        for s in self.sliders:
            s.setValue(0)

    def home_pose(self):
        if len(self.sliders) >= 6:
            self.sliders[0].setValue(0)
            self.sliders[1].setValue(-900)
            self.sliders[2].setValue(900)
            self.sliders[3].setValue(-900)
            self.sliders[4].setValue(900)
            self.sliders[5].setValue(0)

if __name__ == "__main__":
    import math
    app = QtWidgets.QApplication(sys.argv)

    urdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(urdf_path)
    window.show()

    sys.exit(app.exec())
