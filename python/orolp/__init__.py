"""OpenRoboOLP - Open-source Offline Programming Software for Industrial Robots

A free, extensible alternative to commercial OLP tools like RoboDK.
Supports multi-brand robots via open URDF standards and community-driven
post-processors.
"""

__version__ = "0.1.0"

# Core C++ bindings
try:
    from . import orolp_core as _core
except ImportError as e:
    raise ImportError(
        "C++ core module not found. Please build the project first:
"
        "  mkdir build && cd build && cmake .. -DBUILD_PYTHON_BINDINGS=ON && make"
    ) from e

# Python user-layer API
from .robot import Robot, Pose
from .program import Program, Motion
from .simulation import SimulationWorld

__all__ = [
    "Robot",
    "Pose",
    "Program",
    "Motion",
    "SimulationWorld",
]
