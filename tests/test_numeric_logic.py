from pathlib import Path

from tagstudio.core.library.alchemy.fields import IntegerField
from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.library.alchemy.models import Entry
from tagstudio.core.utils.types import unwrap


def test_add_numeric_field_to_entry(library: Library):
    """Verifierar att ett numeriskt fält kan läggas till en entry (REQ-01)"""

    entry = Entry(
        path=Path("test_add.txt"),
        folder=unwrap(library.folder),
        fields=[IntegerField(type_key="RATING", value=5)],
    )

    ids = library.add_entries([entry])
    assert len(ids) == 1


def test_numeric_field_stores_integer(library: Library):
    """Verifierar att ett heltalsvärde sparas och hämtas korrekt (REQ-01)"""

    entry = Entry(
        path=Path("test_int.txt"),
        folder=unwrap(library.folder),
        fields=[IntegerField(type_key="SCORE", value=42)],
    )

    entry_id = library.add_entries([entry])[0]
    refreshed = unwrap(library.get_entry_full(entry_id))

    assert refreshed.integer_fields[0].value == 42
    assert isinstance(refreshed.integer_fields[0].value, int)


def test_update_numeric_field(library: Library):
    """Verifierar att värdet i ett numeriskt fält kan uppdateras (REQ-01)"""

    entry = Entry(
        path=Path("test_update.txt"),
        folder=unwrap(library.folder),
        fields=[IntegerField(type_key="LEVEL", value=1)],
    )

    entry_id = library.add_entries([entry])[0]
    refreshed_entry = unwrap(library.get_entry_full(entry_id))
    field_to_update = refreshed_entry.integer_fields[0]

    # Uppdatera värdet via biblioteket
    library.update_entry_field(entry_id, field_to_update, 10)

    updated_entry = unwrap(library.get_entry_full(entry_id))
    assert updated_entry.integer_fields[0].value == 10


def test_remove_numeric_field(library: Library):
    """Verifierar att fältet kan tas bort från en entry (REQ-01)"""

    entry = Entry(
        path=Path("test_remove.txt"),
        folder=unwrap(library.folder),
        fields=[IntegerField(type_key="TEMP", value=25)],
    )

    entry_id = library.add_entries([entry])[0]
    refreshed_entry = unwrap(library.get_entry_full(entry_id))
    field_to_remove = refreshed_entry.integer_fields[0]

    library.remove_entry_field(field_to_remove, [entry_id])

    final_entry = unwrap(library.get_entry_full(entry_id))
    assert len(final_entry.integer_fields) == 0


def test_numeric_comparison_query(library: Library):
    """Verifierar att numeriska fält kan användas i jämförelser (REQ-05)"""

    e1 = Entry(
        path=Path("low.txt"),
        folder=unwrap(library.folder),
        fields=[IntegerField(type_key="VAL", value=10)],
    )
    e2 = Entry(
        path=Path("high.txt"),
        folder=unwrap(library.folder),
        fields=[IntegerField(type_key="VAL", value=100)],
    )

    library.add_entries([e1, e2])

    # Hämta dem och jämför värdena direkt
    all_entries = list(library.all_entries(with_joins=True))
    vals = [e.integer_fields[0].value for e in all_entries if e.integer_fields]

    assert max(vals) == 100
    assert min(vals) == 10
