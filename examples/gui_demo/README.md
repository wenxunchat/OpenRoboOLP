# Qt6 3D Viewer Demo

This is a minimal runnable 3D visualization demo for OpenRoboOLP.

## Build Instructions

### Prerequisites
- Qt6 (Core, Widgets, OpenGLWidgets, OpenGL)
- CMake 3.16+
- C++17 compiler

### Ubuntu 22.04/24.04
```bash
sudo apt install qt6-base-dev libqt6opengl6-dev libqt6openglwidgets6
```

### macOS
```bash
brew install qt@6
```

### Build
```bash
cd openrobolp
mkdir build && cd build
cmake .. -DBUILD_GUI=ON -DBUILD_PYTHON_BINDINGS=ON
make -j$(nproc)
```

### Run
```bash
./bin/orolp_viewer ../models/ur/test_6dof.urdf
```

## Features
- **Orbit camera**: Left-click drag to rotate around robot
- **Zoom**: Mouse wheel
- **Joint sliders**: Right panel with real-time joint control
- **Home pose**: One-click return to standard home position
- **Auto-load**: Pass URDF path as command-line argument

## Screenshot
```
┌─────────────────────────────────────────┬──────────────┐
│                                         │  Joint Control│
│    [3D Robot View]                      │  ────────────│
│                                         │  J1: 0.0°    │
│    Orbit: Left-drag                     │  [━━━━━━━]   │
│    Zoom: Wheel                          │  J2: -90.0°  │
│                                         │  [━━━━━━━]   │
│                                         │  ...         │
│                                         │              │
│                                         │ [Zero All]   │
│                                         │ [Home Pose]  │
└─────────────────────────────────────────┴──────────────┘
```
