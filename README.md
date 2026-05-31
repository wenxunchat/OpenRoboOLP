# OpenRoboOLP

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![C++](https://img.shields.io/badge/C++-17-blue.svg)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)

**Open-source Offline Programming Software for Industrial Robots**

A free, extensible, and community-driven alternative to commercial OLP tools like RoboDK, Robotmaster, and Delmia.

> **Vision**: Democratize industrial robot programming through open standards (URDF), transparent algorithms, and a community-curated post-processor ecosystem.

---

## Key Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Multi-brand robots** | ✅ MVP | URDF-based unified modeling; supports UR, KUKA, ABB, FANUC, HuiChuan |
| **Offline Programming** | ✅ MVP | Python API + chainable motion commands (MoveJ / MoveL) |
| **Post-processors** | ✅ MVP | Template-based code generation (Jinja2); community extensible |
| **Kinematics** | ✅ MVP | FK/IK via Pinocchio; analytic + numerical solvers |
| **Collision Detection** | 🔄 Scaffold | FCL integration planned for v0.2 |
| **3D GUI** | 📋 Planned | Qt6 + OpenGL viewport (v0.3) |
| **ROS2 Digital Twin** | 📋 Planned | Native rclpy bridge for real-time sync |
| **Trajectory Optimization** | 📋 Planned | TOPP-RA time-optimal parameterization |

---

## Quick Start

### Prerequisites

- **C++**: GCC 9+ / Clang 12+ / MSVC 2019+
- **CMake**: 3.16+
- **Python**: 3.9, 3.10, 3.11, or 3.12
- **System deps**: `eigen3`, `pinocchio`, `fcl`, `pybind11`

**Ubuntu 22.04/24.04:**
```bash
sudo apt update
sudo apt install -y build-essential cmake libeigen3-dev     libpinocchio-dev libfcl-dev pybind11-dev python3-dev     python3-pip qt6-base-dev  # optional for GUI
```

**macOS:**
```bash
brew install cmake eigen pinocchio fcl pybind11 qt@6
```

### Build & Install

```bash
git clone https://github.com/your-org/openrobolp.git
cd openrobolp

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install Python deps
pip install -e ".[dev]"

# Build C++ core + Python bindings
mkdir build && cd build
cmake .. -DBUILD_PYTHON_BINDINGS=ON -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cd ..

# The C++ module is now importable as `orolp.orolp_core`
python -c "import orolp; print(orolp.__version__)"
```

### Your First Program

```python
import orolp as orp

# Load robot model
robot = orp.Robot("models/ur/ur5e.urdf", name="UR5")
robot.tool = orp.Pose.from_xyz_rpy(0, 0, 150, 0, 0, 0)

# Define pick-and-place
pick = orp.Pose.from_xyz_rpy(500, 200, 100, 0, 0, 0)
place = orp.Pose.from_xyz_rpy(600, 300, 100, 0, 0, 0)

program = (
    robot.moveJ([0, -90, 90, -90, 90, 0], speed=80)
    .then(robot.moveL(pick, speed=50, blend=5))
    .then(robot.moveL(place, speed=80, blend=5))
)

# Simulate & generate native code
traj = program.simulate()
print(f"Cycle time: {traj.duration():.2f}s")

ur_code = program.to_post("ur_polyscope")
print(ur_code)
```

See `examples/` for more: pick-and-place, welding paths, multi-robot sync.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Python API Layer (User Scripts, Node-based Editor)          │
│  ─────────────────────────────────────────────────────────  │
│  Robot · Pose · Motion · Program · SimulationWorld           │
├─────────────────────────────────────────────────────────────┤
│  C++ Core Engine (Performance-critical)                      │
│  ─────────────────────────────────────────────────────────  │
│  RobotModel (Pinocchio) · MotionPlanner · CollisionWorld    │
├─────────────────────────────────────────────────────────────┤
│  Post-Processor Ecosystem (Jinja2 Templates)                 │
│  ─────────────────────────────────────────────────────────  │
│  KUKA KRL · ABB RAPID · FANUC TP · URScript · HuiChuan     │
└─────────────────────────────────────────────────────────────┘
```

---

## Supported Robots & Controllers

| Brand | Controller | Post-Processor | Tested |
|-------|-----------|----------------|--------|
| Universal Robots | PolyScope | `ur_polyscope` | ✅ |
| KUKA | KRC4 | `kuka_krc4` | 🔄 |
| ABB | IRC5 | `abb_irc5` | 🔄 |
| FANUC | R-30iB | `fanuc_r30ib` | 🔄 |
| HuiChuan (汇川) | InoTeach | `huichuan_inoteach` | 🔄 |

> 🔄 = Template implemented, pending real hardware validation

**Adding a new brand takes < 30 minutes.** See [docs/post_dev_guide.md](docs/post_dev_guide.md).

---

## Roadmap

### v0.1.0 (Current — Alpha)
- [x] C++ core with Pinocchio FK/IK
- [x] Python bindings (pybind11)
- [x] Chainable motion API
- [x] 5 reference post-processors
- [x] Trajectory interpolation (trapezoidal)

### v0.2.0 (Beta)
- [ ] FCL collision detection
- [ ] Cartesian linear path with IK seeding
- [ ] Work object / tool frame calibration
- [ ] CI/CD with real URDF regression tests

### v0.3.0 (Production Candidate)
- [ ] Qt6 3D viewport
- [ ] Node-based visual programming
- [ ] ROS2 digital twin bridge
- [ ] Plugin marketplace

### v1.0.0 (Stable)
- [ ] TOPP-RA trajectory optimization
- [ ] Multi-robot coordination
- [ ] Force-controlled process simulation
- [ ] IEC 61131-3 PLC code generation

---

## Contributing

We welcome contributions from robotics engineers, researchers, and manufacturers.

- **Post-processors**: Add your robot brand — easiest entry point
- **Core algorithms**: IK solvers, planners, calibration
- **Documentation**: Tutorials, API docs, translations
- **Testing**: Hardware validation reports

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [docs/post_dev_guide.md](docs/post_dev_guide.md) for post-processor development.

---

## License

OpenRoboOLP is licensed under the **Apache License 2.0**.

Robot CAD models (URDFs, meshes) in `models/` may carry separate licenses from their original authors. See individual `README.md` files for details.

---

## Acknowledgements

- [Pinocchio](https://github.com/stack-of-tasks/pinocchio) — INRIA / LAAS-CNRS
- [FCL](https://github.com/flexible-collision-library/fcl) — Flexible Collision Library
- [OMPL](https://ompl.kavrakilab.org/) — Open Motion Planning Library
- [RoboDK](https://robodk.com/) — Inspiration and industry benchmark

---

**Made with ❤️ by the open robotics community.**
