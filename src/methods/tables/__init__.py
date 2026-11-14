"""
Таблицы поиска и предварительно рассчитанные матричные коэффициенты.
"""

from methods.tables.mc_tables import (
    CORRECTION_M0,
    CORRECTION_M1,
    CORRECTION_M2,
    BASE_TABLE_S,
    BASE_TABLE_V,
    get_lookup_table_raw,
    build_table_arrays,
)

__all__ = [
    "CORRECTION_M0",
    "CORRECTION_M1",
    "CORRECTION_M2",
    "BASE_TABLE_S",
    "BASE_TABLE_V",
    "get_lookup_table_raw",
    "build_table_arrays",
]
