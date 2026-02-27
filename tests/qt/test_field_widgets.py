# Copyright (C) 2025
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.qt.controllers.preview_panel_controller import PreviewPanel
from tagstudio.qt.mixed.text_field import TextWidget
from tagstudio.qt.ts_qt import QtDriver


def render_last_widget(panel, qt_driver, entry_id):
    qt_driver.toggle_item_selection(entry_id, append=False, bridge=False)
    panel.set_selection(qt_driver.selected)


def test_text_line_renders_text_widget(qt_driver: QtDriver, library: Library, entry_full: Entry):
    panel = PreviewPanel(library, qt_driver)

    render_last_widget(
        panel,
        qt_driver,
        entry_full.id,
    )
    title_container = next(
        c for c in panel.field_containers_widget.containers if "Title" in c.title
    )
    assert isinstance(title_container.get_inner_widget(), TextWidget)


def test_text_box_renders_text_widget(qt_driver: QtDriver, library: Library, entry_full: Entry):
    panel = PreviewPanel(library, qt_driver)

    library.add_field_to_entry(entry_full.id, field_id="DESCRIPTION")

    render_last_widget(
        panel,
        qt_driver,
        entry_full.id,
    )
    description_container = next(
        c for c in panel.field_containers_widget.containers if "Description" in c.title
    )
    assert isinstance(description_container.get_inner_widget(), TextWidget)


def test_date_time_renders_text_widget(qt_driver: QtDriver, library: Library, entry_full: Entry):
    panel = PreviewPanel(library, qt_driver)

    library.add_field_to_entry(entry_full.id, field_id="DATE")

    render_last_widget(
        panel,
        qt_driver,
        entry_full.id,
    )
    date_container = next(c for c in panel.field_containers_widget.containers if "Date" in c.title)
    assert isinstance(date_container.get_inner_widget(), TextWidget)
