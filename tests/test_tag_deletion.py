# Copyright (C) 2025
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio

from collections.abc import Callable
from pathlib import Path

import pytest

from tagstudio.core.library.alchemy.enums import BrowsingState
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry, Tag
from tagstudio.core.utils.types import unwrap


def test_delete_child_tag_preserves_parent_search(library: Library, generate_tag: Callable[..., Tag]):
    """When a child tag is deleted, entries tagged only with the child
    should still appear in searches for the parent tag."""
    # create parent tag A and child tag B
    parent = unwrap(library.add_tag(generate_tag("genre", id=3000)))
    child = unwrap(library.add_tag(generate_tag("rock", id=3001)))
    library.add_parent_tag(child.id, parent.id)

    # create an entry tagged with only the child tag
    entry = Entry(
        path=Path("song.mp3"),
        folder=unwrap(library.folder),
        fields=library.default_fields,
    )
    entry_id = library.add_entries([entry])[0]
    library.add_tags_to_entries(entry_id, child.id)

    # searching for the parent should find the entry (via child hierarchy)
    results = library.search_library(
        BrowsingState.from_tag_name("genre"),
        page_size=500,
    )
    assert results.total_count >= 1

    # delete the child tag
    library.remove_tag(child.id)

    # searching for the parent should still find the entry
    results = library.search_library(
        BrowsingState.from_tag_name("genre"),
        page_size=500,
    )
    assert results.total_count >= 1


def test_delete_child_tag_entry_becomes_untagged(library: Library, generate_tag: Callable[..., Tag]):
    """When a child tag is deleted and the entry has no other tags,
    it should appear in special:untagged searches."""
    parent = unwrap(library.add_tag(generate_tag("category", id=3100)))
    child = unwrap(library.add_tag(generate_tag("subcategory", id=3101)))
    library.add_parent_tag(child.id, parent.id)

    entry = Entry(
        path=Path("lonely_file.txt"),
        folder=unwrap(library.folder),
        fields=library.default_fields,
    )
    entry_id = library.add_entries([entry])[0]
    library.add_tags_to_entries(entry_id, child.id)

    # entry should not be untagged right now
    results = library.search_library(
        BrowsingState.from_search_query("special:untagged"),
        page_size=500,
    )
    untagged_before = results.total_count

    # delete both child and parent tags
    library.remove_tag(child.id)
    library.remove_tag(parent.id)

    # entry should now appear as untagged
    results = library.search_library(
        BrowsingState.from_search_query("special:untagged"),
        page_size=500,
    )
    assert results.total_count > untagged_before


def test_delete_child_tag_keeps_direct_parent_tag(library: Library, generate_tag: Callable[..., Tag]):
    """When an entry has both parent and child tags directly applied,
    deleting the child should leave the parent tag intact."""
    parent = unwrap(library.add_tag(generate_tag("animal", id=3200)))
    child = unwrap(library.add_tag(generate_tag("dog", id=3201)))
    library.add_parent_tag(child.id, parent.id)

    entry = Entry(
        path=Path("pet_photo.jpg"),
        folder=unwrap(library.folder),
        fields=library.default_fields,
    )
    entry_id = library.add_entries([entry])[0]
    library.add_tags_to_entries(entry_id, [child.id, parent.id])

    # delete the child tag
    library.remove_tag(child.id)

    # parent tag should still be directly on the entry
    refreshed = unwrap(library.get_entry_full(entry_id))
    tag_ids = [t.id for t in refreshed.tags]
    assert parent.id in tag_ids
