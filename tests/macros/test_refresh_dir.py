# Copyright (C) 2025
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tagstudio.core.enums import LibraryPrefs
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.refresh import RefreshTracker
from tagstudio.core.utils.types import unwrap
from tagstudio.core.library.alchemy.registries.ignored_registry import IgnoredRegistry
from tagstudio.core.library.ignore import Ignore

from tagstudio.core.library.refresh import RefreshTracker
from tagstudio.core.library.alchemy.registries.ignored_registry import IgnoredRegistry
from tagstudio.core.library.ignore import Ignore
from tagstudio.core.utils.types import unwrap
from tagstudio.core.library.alchemy.library import Library
    

CWD = Path(__file__).parent


@pytest.mark.parametrize("exclude_mode", [True, False])
@pytest.mark.parametrize("library", [TemporaryDirectory()], indirect=True)
def test_refresh_new_files(library: Library, exclude_mode: bool):
    library_dir = unwrap(library.library_dir)
    # Given
    library.set_prefs(LibraryPrefs.IS_EXCLUDE_LIST, exclude_mode)
    library.set_prefs(LibraryPrefs.EXTENSION_LIST, [".md"])
    registry = RefreshTracker(library=library)
    library.included_files.clear()
    (library_dir / "FOO.MD").touch()

    # Test if the single file was added
    list(registry.refresh_dir(library_dir, force_internal_tools=True))
    assert registry.files_not_in_library == [Path("FOO.MD")]


@pytest.mark.parametrize("library", [TemporaryDirectory()], indirect=True)
def test_refresh_multi_byte_filenames(library: Library):
    library_dir = unwrap(library.library_dir)
    # Given
    registry = RefreshTracker(library=library)
    library.included_files.clear()
    (library_dir / ".TagStudio").mkdir()
    (library_dir / "こんにちは.txt").touch()
    (library_dir / "em–dash.txt").touch()
    (library_dir / "apostrophe’.txt").touch()
    (library_dir / "umlaute äöü.txt").touch()

    # Test if all files were added with their correct names and without exceptions
    list(registry.refresh_dir(library_dir))
    assert Path("こんにちは.txt") in registry.files_not_in_library
    assert Path("em–dash.txt") in registry.files_not_in_library
    assert Path("apostrophe’.txt") in registry.files_not_in_library
    assert Path("umlaute äöü.txt") in registry.files_not_in_library


@pytest.mark.parametrize("library", [TemporaryDirectory()], indirect=True)
def test_refresh_tracker_adds_new_file(library: Library):
    library_dir = unwrap(library.library_dir)

    # Create a file
    file_path = library_dir / "example.txt"
    file_path.touch()

    tracker = RefreshTracker(library=library)
    library.included_files.clear()

    # Run refresh
    list(tracker.refresh_dir(library_dir, force_internal_tools=True))

    # The file should be detected as new
    assert Path("example.txt") in tracker.files_not_in_library


@pytest.mark.parametrize("library", [TemporaryDirectory()], indirect=True)
def test_removing_entry_does_not_delete_file(library: Library):
    library_dir = unwrap(library.library_dir)

    file_path = library_dir / "file.txt"
    file_path.touch()

    tracker = RefreshTracker(library)
    library.included_files.clear()
    list(tracker.refresh_dir(library_dir, force_internal_tools=True))
    list(tracker.save_new_files())

    assert file_path.exists()
