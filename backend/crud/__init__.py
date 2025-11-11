"""
CRUD package.
"""

from crud.fabric import (
    get_fabric,
    get_fabric_by_name,
    get_fabrics,
    create_fabric,
    update_fabric,
    delete_fabric,
)
from crud.color import (
    get_color,
    get_color_by_name,
    get_colors,
    create_color,
    update_color,
    delete_color,
)
from crud.design import (
    get_design,
    get_designs,
    create_design,
    update_design,
    delete_design,
)

__all__ = [
    "get_fabric",
    "get_fabric_by_name",
    "get_fabrics",
    "create_fabric",
    "update_fabric",
    "delete_fabric",
    "get_color",
    "get_color_by_name",
    "get_colors",
    "create_color",
    "update_color",
    "delete_color",
    "get_design",
    "get_designs",
    "create_design",
    "update_design",
    "delete_design",
]
