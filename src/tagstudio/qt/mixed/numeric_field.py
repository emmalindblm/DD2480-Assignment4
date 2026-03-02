# Copyright (C) 2025
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

from PySide6.QtWidgets import QDoubleSpinBox, QHBoxLayout

# Ändra importen här:
from tagstudio.qt.mixed.field_widget import FieldWidget


class NumericWidget(FieldWidget):
    def __init__(self, title, value: float | int = 0, parent=None):
        super().__init__(title)  # FieldWidget vill ha title som första argument
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.spinbox = QDoubleSpinBox(self)
        self.spinbox.setRange(-999999999, 999999999)
        self.spinbox.setValue(float(value))

        self._layout.addWidget(self.spinbox)

    def get_value(self) -> float | int:
        val = self.spinbox.value()
        return int(val) if val.is_integer() else val

    def set_value(self, value: float | int):
        self.spinbox.setValue(float(value))
