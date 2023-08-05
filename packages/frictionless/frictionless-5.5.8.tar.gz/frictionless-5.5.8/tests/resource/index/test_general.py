import pytest
from pytest_lazyfixture import lazy_fixture
from frictionless import Resource, Database, platform, formats

control = formats.sql.SqlControl(table="table")
database_urls = [lazy_fixture("sqlite_url"), lazy_fixture("postgresql_url")]
pytestmark = pytest.mark.skipif(
    platform.type == "darwin" or platform.type == "windows",
    reason="Not supported tests in MacOS and Windows",
)


# General


@pytest.mark.parametrize("database_url", database_urls)
def test_resource_index_sqlite(database_url):
    resource = Resource("data/table.csv")
    resource.index(database_url, table_name=control.table)
    assert Resource(database_url, control=control).extract() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


# Fast


@pytest.mark.skip(reason="issue-1408")
@pytest.mark.parametrize("database_url", database_urls)
def test_resource_index_sqlite_fast(database_url):
    resource = Resource("data/table.csv")
    resource.index(database_url, table_name=control.table, fast=True)
    assert Resource(database_url, control=control).extract() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


# Fallback


@pytest.mark.skip(reason="issue-1408")
@pytest.mark.parametrize("database_url", database_urls)
def test_resource_index_sqlite_fast_with_use_fallback(database_url):
    resource = Resource("data/table.csv")
    resource.infer()
    resource.schema.set_field_type("name", "integer")
    resource.index(database_url, table_name=control.table, fast=True, use_fallback=True)
    assert Resource(database_url, control=control).extract() == [
        {"id": 1, "name": None},
        {"id": 2, "name": None},
    ]


# On Progress


@pytest.mark.parametrize("database_url", database_urls)
def test_resource_index_sqlite_on_progress(database_url, mocker):
    on_progress = mocker.stub(name="on_progress")
    resource = Resource("data/table.csv")
    resource.index(database_url, table_name=control.table, on_progress=on_progress)
    assert on_progress.call_count == 2
    on_progress.assert_any_call("1 rows")
    on_progress.assert_any_call("2 rows")


# With Metadata


@pytest.mark.parametrize("database_url", database_urls)
def test_resource_index_sqlite_with_metadata(database_url):
    resource = Resource("data/table.csv")
    resource.index(database_url, with_metadata=True)
    database = Database(database_url)
    # Table
    table = database.query_table('SELECT * from "table"')
    assert table["tableSchema"]
    assert table["header"] == ["_rowNumber", "_rowValid", "id", "name"]
    assert table["rows"] == [
        {"_rowNumber": 2, "_rowValid": True, "id": 1, "name": "english"},
        {"_rowNumber": 3, "_rowValid": True, "id": 2, "name": "中国人"},
    ]
    # Index
    records = database.list_records()
    record = database.read_record(resource.normpath)
    assert len(records) == 1
    assert record is not None
    assert record["path"] == "data/table.csv"
    assert record["type"] == "table"
    assert record["updated"]
    assert record.get("tableName") == "table"
    assert record["resource"]["path"] == "data/table.csv"  # type: ignore
    assert record["report"]["valid"] == True  # type: ignore
