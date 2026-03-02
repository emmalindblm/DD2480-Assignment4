# Copyright (C) 2025
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

from PySide6.QtWidgets import QHBoxLayout, QSlider

from tagstudio.qt.mixed.field_widget import FieldWidget


class SliderWidget(FieldWidget):
    def __init__(
        self,
        title: str,
        value: int | float,
        min: int | float,
        max: int | float,
        step: int | float,
    ) -> None:
        super().__init__(title)
        self.setObjectName("sliderBox")
        self.base_layout = QHBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.base_layout)
        self.slider = QSlider()
        self.slider.setMinimum(int(min))
        self.slider.setMaximum(int(max))
        self.slider.setSingleStep(int(step))
        self.slider.setValue(int(value))
        self.base_layout.addWidget(self.slider)
        self.set_value(value)

    def set_value(self, value: int | float) -> None:
        self.slider.setValue(int(value))
