# Copyright (C) 2025
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

from pathlib import Path

from tagstudio.core.library.alchemy.fields import SliderField
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.core.utils.types import unwrap


def create_slider_entry(
    library: Library,
    path: str,
    value: int | float,
    min: int | float,
    max: int | float,
    step: int | float,
) -> int:
    entry = Entry(
        path=Path(path),
        folder=unwrap(library.folder),
        fields=[SliderField(type_key="SLIDER", value=value, min=min, max=max, step=step)],
    )
    return library.add_entries([entry])[0]


def test_slider_has_configurable_minimum(library: Library):
    entry_id = create_slider_entry(library, "test_min.txt", value=50, min=10, max=100.2, step=1)
    retrieved_entry = unwrap(library.get_entry_full(entry_id))
    assert retrieved_entry.slider_fields[0].min == 10


def test_slider_has_configurable_maximum(library: Library):
    entry_id = create_slider_entry(library, "test_max.txt", value=50, min=10, max=100.2, step=1)
    retrieved_entry = unwrap(library.get_entry_full(entry_id))
    assert retrieved_entry.slider_fields[0].max == 100.2


def test_slider_has_configurable_step(library: Library):
    entry_id = create_slider_entry(library, "test_step.txt", value=50, min=10, max=100.2, step=1)
    retrieved_entry = unwrap(library.get_entry_full(entry_id))
    assert retrieved_entry.slider_fields[0].step == 1


def test_slider_handles_value_below_minimum(library: Library):
    entry_id = create_slider_entry(
        library, "test_min_handle.txt", value=3, min=10, max=100.2, step=1
    )
    retrieved_entry = unwrap(library.get_entry_full(entry_id))
    assert retrieved_entry.slider_fields[0].value == 10


def test_slider_handles_value_above_maximum(library: Library):
    entry_id = create_slider_entry(
        library, "test_max_handle.txt", value=105.3, min=10, max=100.2, step=1
    )
    retrieved_entry = unwrap(library.get_entry_full(entry_id))
    assert retrieved_entry.slider_fields[0].value == 100.2
