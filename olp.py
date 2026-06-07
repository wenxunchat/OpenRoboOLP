#!/usr/bin/env python3
"""
OpenRoboOLP - OLP Terminal
"""

import sys
import math
import struct
import numpy as np
from pathlib import Path

try:
    from PySide6 import QtWidgets, QtCore, QtOpenGLWidgets, QtGui
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QFont, QAction, QKeySequence
except ImportError:
    print("PySide6 not installed. Install with: pip install PySide6")
    sys.exit(1)

try:
    import OpenGL.GL as gl
except ImportError:
    print("PyOpenGL not installed. Install with: pip install PyOpenGL")
    sys.exit(1)


GL_COLOR_BUFFER_BIT = 0x00004000
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_TRIANGLES = 0x00000004
GL_QUADS = 0x00000007
GL_QUAD_STRIP = 0x00000008
GL_TRIANGLE_FAN = 0x00000006
GL_LINES = 0x00000001
GL_DEPTH_TEST = 0x00000B71
GL_MODELVIEW = 0x00001700
GL_PROJECTION = 0x00001701


class RobotRenderer:
    def __init__(self):
        self.links = {}
        self.joints = {}
        self.root_link = None
        self.joint_values = {}
        self.urdf_dir = None
        self.robot_name = "Unknown"

    def load_urdf(self, path):
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        self.links.clear()
        self.joints.clear()
        self.joint_values.clear()
        self.urdf_dir = Path(path).parent
        self.robot_name = root.get("name", "Unknown")

        for link in root.findall("link"):
            name = link.get("name")
            visual = link.find("visual")
            if visual is None:
                continue

            geom = visual.find("geometry")
            material = visual.find("material")
            mat = material.find("color") if material is not None else None
            rgba = [0.7, 0.7, 0.75, 1.0]
            if mat is not None:
                rgba = [float(x) for x in mat.get("rgba", "0.7 0.7 0.75 1").split()]

            origin = visual.find("origin")
            xyz = [0.0, 0.0, 0.0]
            rpy = [0.0, 0.0, 0.0]
            if origin is not None:
                xyz = [float(x) for x in origin.get("xyz", "0 0 0").split()]
                rpy = [float(x) for x in origin.get("rpy", "0 0 0").split()]

            geo_type = None
            params = ()
            
            if geom.find("cylinder") is not None:
                cyl = geom.find("cylinder")
                geo_type = "cylinder"
                params = (float(cyl.get("radius", "0.03")), float(cyl.get("length", "0.15")))
            elif geom.find("box") is not None:
                box = geom.find("box")
                geo_type = "box"
                params = tuple(float(x) for x in box.get("size", "0.1 0.1 0.1").split())
            elif geom.find("sphere") is not None:
                sph = geom.find("sphere")
                geo_type = "sphere"
                params = (float(sph.get("radius", "0.02")),)

            self.links[name] = {
                "name": name,
                "type": geo_type,
                "params": params,
                "origin_xyz": xyz,
                "origin_rpy": rpy,
                "color": rgba[:3],
            }

        print(f"Loaded {len(self.links)} links from URDF")

        for joint in root.findall("joint"):
            jname = joint.get("name")
            jtype = joint.get("type", "fixed")
            parent = joint.find("parent").get("link")
            child = joint.find("child").get("link")
            origin = joint.find("origin")
            jxyz = [0.0, 0.0, 0.0]
            jrpy = [0.0, 0.0, 0.0]
            if origin is not None:
                jxyz = [float(x) for x in origin.get("xyz", "0 0 0").split()]
                jrpy = [float(x) for x in origin.get("rpy", "0 0 0").split()]
            axis = [0.0, 0.0, 1.0]
            axis_el = joint.find("axis")
            if axis_el is not None:
                axis = [float(x) for x in axis_el.get("xyz", "0 0 1").split()]

            limit_lower = -math.pi
            limit_upper = math.pi
            limit = joint.find("limit")
            if limit is not None:
                limit_lower = float(limit.get("lower", "-3.14159"))
                limit_upper = float(limit.get("upper", "3.14159"))

            self.joints[jname] = {
                "name": jname,
                "type": jtype,
                "parent": parent,
                "child": child,
                "origin_xyz": jxyz,
                "origin_rpy": jrpy,
                "axis": axis,
                "limit": {"lower": limit_lower, "upper": limit_upper}
            }
            self.joint_values[jname] = 0.0

        child_links = set(j["child"] for j in self.joints.values())
        for name in self.links:
            if name not in child_links:
                self.root_link = name
                break

        print(f"Loaded {len(self.joints)} joints, root={self.root_link}")
        return len(self.links) > 0


class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = RobotRenderer()
        self.camera_dist = 1.2
        self.camera_az = 45.0
        self.camera_el = 30.0
        self.dragging = False
        self.last_pos = None

    def load_robot(self, path):
        success = self.renderer.load_urdf(path)
        self.update()
        return success

    def set_joints(self, q):
        self.renderer.set_joints(q)
        self.update()

    def initializeGL(self):
        gl.glClearColor(0.15, 0.15, 0.18, 1.0)
        gl.glEnable(GL_DEPTH_TEST)

    def paintGL(self):
        gl.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        w, h = self.width(), self.height()

        gl.glMatrixMode(GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = w / max(1, h)
        fov = 45.0
        near, far = 0.01, 100.0
        top = near * math.tan(math.radians(fov / 2))
        right = top * aspect
        gl.glFrustum(-right, right, -top, top, near, far)

        gl.glMatrixMode(GL_MODELVIEW)
        gl.glLoadIdentity()

        az = math.radians(self.camera_az)
        el = math.radians(self.camera_el)
        cx = self.camera_dist * math.cos(el) * math.cos(az)
        cy = self.camera_dist * math.cos(el) * math.sin(az)
        cz = self.camera_dist * math.sin(el)

        eye = np.array([cx, cy, cz], dtype=np.float64)
        center = np.array([0.0, 0.0, 0.4], dtype=np.float64)
        up_vec = np.array([0.0, 0.0, 1.0], dtype=np.float64)

        f = center - eye
        norm = np.linalg.norm(f)
        if norm > 0:
            f = f / norm
        s = np.cross(f, up_vec)
        norm = np.linalg.norm(s)
        if norm > 0:
            s = s / norm
        u = np.cross(s, f)

        rot = [
            float(s[0]), float(s[1]), float(s[2]), 0.0,
            float(u[0]), float(u[1]), float(u[2]), 0.0,
            float(-f[0]), float(-f[1]), float(-f[2]), 0.0,
            0.0, 0.0, 0.0, 1.0
        ]
        gl.glLoadMatrixf(rot)
        gl.glTranslated(float(-eye[0]), float(-eye[1]), float(-eye[2]))

        self._draw_grid()
        self._draw_robot()

    def _draw_grid(self):
        gl.glBegin(GL_LINES)
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

    def _draw_robot(self):
        if self.renderer.root_link is None:
            return
        self._draw_link_recursive(self.renderer.root_link)

    def _draw_link_recursive(self, link_name, parent_joint=None):
        link = self.renderer.links.get(link_name)
        if link is None:
            return

        gl.glPushMatrix()

        if parent_joint is not None:
            jx, jy, jz = parent_joint["origin_xyz"]
            gl.glTranslatef(jx, jy, jz)
            
            jrx, jry, jrz = parent_joint["origin_rpy"]
            if any(v != 0 for v in [jrx, jry, jrz]):
                gl.glRotatef(math.degrees(jrz), 0, 0, 1)
                gl.glRotatef(math.degrees(jry), 0, 1, 0)
                gl.glRotatef(math.degrees(jrx), 1, 0, 0)

            q = self.renderer.joint_values.get(parent_joint["name"], 0.0)
            if parent_joint["type"] == "revolute" and q != 0:
                ax, ay, az = parent_joint["axis"]
                gl.glRotatef(math.degrees(q), ax, ay, az)

        ox, oy, oz = link["origin_xyz"]
        orx, ory, orz = link["origin_rpy"]
        if any(v != 0 for v in [orx, ory, orz]):
            gl.glRotatef(math.degrees(orz), 0, 0, 1)
            gl.glRotatef(math.degrees(ory), 0, 1, 0)
            gl.glRotatef(math.degrees(orx), 1, 0, 0)
        gl.glTranslatef(ox, oy, oz)

        gl.glColor3f(*link["color"])
        geo = link["type"]
        if geo == "cylinder":
            radius, length = link["params"]
            self._draw_cylinder(radius, length)
        elif geo == "box":
            w, h, d = link["params"]
            self._draw_box(w, h, d)
        elif geo == "sphere":
            radius = link["params"][0]
            self._draw_sphere(radius)

        for jname, joint in self.renderer.joints.items():
            if joint["parent"] == link_name:
                self._draw_link_recursive(joint["child"], joint)

        gl.glPopMatrix()

    def _draw_cylinder(self, radius, length):
        segments = 24
        half_len = length / 2.0
        gl.glBegin(GL_QUADS)
        for i in range(segments):
            a1 = 2 * math.pi * i / segments
            a2 = 2 * math.pi * (i + 1) / segments
            x1 = radius * math.cos(a1)
            y1 = radius * math.sin(a1)
            x2 = radius * math.cos(a2)
            y2 = radius * math.sin(a2)
            gl.glNormal3f(x1, y1, 0)
            gl.glVertex3f(x1, y1, -half_len)
            gl.glVertex3f(x1, y1, half_len)
            gl.glNormal3f(x2, y2, 0)
            gl.glVertex3f(x2, y2, half_len)
            gl.glVertex3f(x2, y2, -half_len)
        gl.glEnd()
        gl.glBegin(GL_TRIANGLE_FAN)
        gl.glNormal3f(0, 0, 1)
        gl.glVertex3f(0, 0, half_len)
        for i in range(segments + 1):
            a = 2 * math.pi * i / segments
            gl.glVertex3f(radius * math.cos(a), radius * math.sin(a), half_len)
        gl.glEnd()
        gl.glBegin(GL_TRIANGLE_FAN)
        gl.glNormal3f(0, 0, -1)
        gl.glVertex3f(0, 0, -half_len)
        for i in range(segments + 1):
            a = 2 * math.pi * i / segments
            gl.glVertex3f(radius * math.cos(a), radius * math.sin(a), -half_len)
        gl.glEnd()

    def _draw_box(self, w, h, d):
        x, y, z = w/2, h/2, d/2
        gl.glBegin(GL_QUADS)
        gl.glNormal3f(0, 0, 1)
        gl.glVertex3f(-x, -y, z); gl.glVertex3f(x, -y, z)
        gl.glVertex3f(x, y, z); gl.glVertex3f(-x, y, z)
        gl.glNormal3f(0, 0, -1)
        gl.glVertex3f(-x, -y, -z); gl.glVertex3f(-x, y, -z)
        gl.glVertex3f(x, y, -z); gl.glVertex3f(x, -y, -z)
        gl.glNormal3f(1, 0, 0)
        gl.glVertex3f(x, -y, -z); gl.glVertex3f(x, y, -z)
        gl.glVertex3f(x, y, z); gl.glVertex3f(x, -y, z)
        gl.glNormal3f(-1, 0, 0)
        gl.glVertex3f(-x, -y, -z); gl.glVertex3f(-x, -y, z)
        gl.glVertex3f(-x, y, z); gl.glVertex3f(-x, y, -z)
        gl.glNormal3f(0, 1, 0)
        gl.glVertex3f(-x, y, -z); gl.glVertex3f(-x, y, z)
        gl.glVertex3f(x, y, z); gl.glVertex3f(x, y, -z)
        gl.glNormal3f(0, -1, 0)
        gl.glVertex3f(-x, -y, -z); gl.glVertex3f(x, -y, -z)
        gl.glVertex3f(x, -y, z); gl.glVertex3f(-x, -y, z)
        gl.glEnd()

    def _draw_sphere(self, radius):
        stacks = 12
        slices = 16
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + i / stacks)
            lat1 = math.pi * (-0.5 + (i + 1) / stacks)
            z0 = radius * math.sin(lat0)
            zr0 = radius * math.cos(lat0)
            z1 = radius * math.sin(lat1)
            zr1 = radius * math.cos(lat1)
            gl.glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * j / slices
                x = math.cos(lng)
                y = math.sin(lng)
                gl.glNormal3f(x * math.cos(lat0), y * math.cos(lat0), math.sin(lat0))
                gl.glVertex3f(x * zr0, y * zr0, z0)
                gl.glNormal3f(x * math.cos(lat1), y * math.cos(lat1), math.sin(lat1))
                gl.glVertex3f(x * zr1, y * zr1, z1)
            gl.glEnd()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragging and self.last_pos:
            current_pos = event.position().toPoint()
            dx = current_pos.x() - self.last_pos.x()
            dy = current_pos.y() - self.last_pos.y()
            self.camera_az -= dx * 0.5
            self.camera_el += dy * 0.5
            self.camera_el = max(-89, min(89, self.camera_el))
            self.last_pos = current_pos
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.camera_dist *= 0.9 ** delta
        self.camera_dist = max(0.3, min(10.0, self.camera_dist))
        self.update()


class PathCodeEditor(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 10))
        self.setStyleSheet("background-color: #1a1a1a; color: #e0e0e0;")
        self.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.setTabStopDistance(20)
        self.setPlainText("# OLP Path Code\nmovej([0, -90, 90, -90, 90, 0], vel=0.5)\n")


class DevicePropertyPanel(QtWidgets.QWidget):
    jointChanged = Signal(str, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sliders = {}
        self.value_labels = {}
        self.joint_layout = None
        self.log_text = None
        self.name_label = None
        self.type_label = None
        self.manufacturer_label = None
        self.dof_label = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        info_group = QtWidgets.QGroupBox("Robot Info")
        info_layout = QtWidgets.QFormLayout(info_group)
        self.name_label = QtWidgets.QLabel("N/A")
        self.type_label = QtWidgets.QLabel("Industrial Robot")
        self.manufacturer_label = QtWidgets.QLabel("Unknown")
        self.dof_label = QtWidgets.QLabel("0")
        info_layout.addRow("Name:", self.name_label)
        info_layout.addRow("Type:", self.type_label)
        info_layout.addRow("Manufacturer:", self.manufacturer_label)
        info_layout.addRow("DOF:", self.dof_label)
        layout.addWidget(info_group)
        
        joint_group = QtWidgets.QGroupBox("Joint Controls")
        self.joint_layout = QtWidgets.QVBoxLayout(joint_group)
        layout.addWidget(joint_group)
        
        log_group = QtWidgets.QGroupBox("Log")
        log_layout = QtWidgets.QVBoxLayout(log_group)
        self.log_text = QtWidgets.QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("background-color: #1a1a1a; color: #ffffff;")
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)
        
        layout.addStretch()
    
    def setup_joints(self, renderer):
        while self.joint_layout.count() > 0:
            item = self.joint_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.sliders.clear()
        self.value_labels.clear()
        
        joint_items = []
        for name, joint in renderer.joints.items():
            if joint["type"] == "revolute":
                child = joint["child"]
                if child in renderer.links:
                    try:
                        idx = list(renderer.links.keys()).index(child)
                        joint_items.append((idx, name, joint))
                    except ValueError:
                        pass
        
        joint_items.sort(key=lambda x: x[0])
        
        for _, name, joint in joint_items:
            frame = QtWidgets.QFrame()
            frame.setFrameStyle(QtWidgets.QFrame.StyledPanel)
            flayout = QtWidgets.QVBoxLayout(frame)
            flayout.setContentsMargins(5, 5, 5, 5)
            
            header = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(f"<b>{name}</b>")
            self.value_labels[name] = QtWidgets.QLabel("0.0°")
            header.addWidget(label)
            header.addStretch()
            header.addWidget(self.value_labels[name])
            flayout.addLayout(header)
            
            slider = QtWidgets.QSlider(Qt.Horizontal)
            slider.setMinimum(int(math.degrees(joint["limit"]["lower"]) * 100))
            slider.setMaximum(int(math.degrees(joint["limit"]["upper"]) * 100))
            slider.setValue(0)
            slider.valueChanged.connect(lambda v, n=name: self._on_joint_changed(n, v))
            flayout.addWidget(slider)
            self.sliders[name] = slider
            
            limit_layout = QtWidgets.QHBoxLayout()
            limit_layout.addWidget(QtWidgets.QLabel(f"{math.degrees(joint['limit']['lower']):.1f}°"))
            limit_layout.addStretch()
            limit_layout.addWidget(QtWidgets.QLabel(f"{math.degrees(joint['limit']['upper']):.1f}°"))
            flayout.addLayout(limit_layout)
            
            self.joint_layout.addWidget(frame)
    
    def _on_joint_changed(self, name, value):
        angle = value / 100.0
        if name in self.value_labels:
            self.value_labels[name].setText(f"{angle:.2f}°")
        self.jointChanged.emit(name, math.radians(angle))
    
    def update_robot_info(self, renderer):
        self.name_label.setText(renderer.robot_name)
        self.dof_label.setText(str(len(renderer.joints)))
        self.log_text.append(f"Loaded: {renderer.robot_name}")
        self.log_text.append(f"Joints: {len(renderer.joints)}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, urdf_path=None):
        super().__init__()
        self.setWindowTitle("OpenRoboOLP Terminal v0.1.0")
        self.resize(1400, 900)
        self.setup_menu()
        self.setup_ui()
        self.urdf_path = urdf_path
    
    def showEvent(self, event):
        super().showEvent(event)
        if self.urdf_path and Path(self.urdf_path).exists():
            self.load_robot(self.urdf_path)
        self.gl_widget.update()
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&File")
        open_action = QAction("&Open Model...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_model)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save Path Code...", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_path_code)
        file_menu.addAction(save_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        view_menu = menubar.addMenu("&View")
        reset_view = QAction("&Reset View", self)
        reset_view.setShortcut("R")
        reset_view.triggered.connect(self.reset_view)
        view_menu.addAction(reset_view)
    
    def setup_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        
        main_layout = QtWidgets.QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)
        
        left_panel = QtWidgets.QWidget()
        left_panel.setMaximumWidth(350)
        left_panel.setMinimumWidth(250)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        left_header = QtWidgets.QLabel("<h3>Path Code Editor</h3>")
        left_layout.addWidget(left_header)
        
        self.code_editor = PathCodeEditor()
        left_layout.addWidget(self.code_editor)
        
        code_btn_layout = QtWidgets.QHBoxLayout()
        self.run_btn = QtWidgets.QPushButton("▶ Run")
        self.run_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.stop_btn = QtWidgets.QPushButton("■ Stop")
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white;")
        code_btn_layout.addWidget(self.run_btn)
        code_btn_layout.addWidget(self.stop_btn)
        left_layout.addLayout(code_btn_layout)
        
        main_layout.addWidget(left_panel)
        
        self.gl_widget = GLWidget(self)
        self.gl_widget.setMinimumSize(400, 300)
        main_layout.addWidget(self.gl_widget, 1)
        
        self.property_panel = DevicePropertyPanel()
        self.property_panel.setMaximumWidth(300)
        self.property_panel.setMinimumWidth(250)
        self.property_panel.jointChanged.connect(self.on_joint_changed)
        main_layout.addWidget(self.property_panel)
        
        self.statusBar().showMessage("Ready")
    
    def open_model(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Robot Model", "models", "URDF Files (*.urdf);;All Files (*)"
        )
        if file_path:
            self.load_robot(file_path)
    
    def load_robot(self, path):
        if not self.gl_widget.load_robot(path):
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load URDF: {path}")
            return
        self.property_panel.setup_joints(self.gl_widget.renderer)
        self.property_panel.update_robot_info(self.gl_widget.renderer)
        self.statusBar().showMessage(f"Loaded: {Path(path).name}")
        self.gl_widget.update()
    
    def on_joint_changed(self, name, value):
        self.gl_widget.renderer.joint_values[name] = value
        self.gl_widget.update()
    
    def save_path_code(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Path Code", "", "Python Files (*.py);;All Files (*)"
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.code_editor.toPlainText())
            self.statusBar().showMessage(f"Saved: {Path(file_path).name}")
    
    def reset_view(self):
        self.gl_widget.camera_dist = 1.2
        self.gl_widget.camera_az = 45.0
        self.gl_widget.camera_el = 30.0
        self.gl_widget.update()


def main():
    fmt = QtGui.QSurfaceFormat()
    fmt.setVersion(2, 1)
    fmt.setProfile(QtGui.QSurfaceFormat.NoProfile)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)
    
    app = QtWidgets.QApplication(sys.argv)
    
    urdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(urdf_path)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
