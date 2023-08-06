import vaultdb
from pandas import DataFrame
import pandas as pd
import pytest


def is_dunder_method(method_name: str) -> bool:
    if (len(method_name) < 4):
        return False
    return method_name[:2] == '__' and method_name[:-3:-1] == '__'

# This file contains tests for VaultDBPyConnection methods,
# wrapped by the 'duckdb' module, to execute with the 'default_connection'


class TestVaultDBConnection(object):
    def test_append(self):
        vaultdb.execute("Create table integers (i integer)")
        df_in = pd.DataFrame({'numbers': [1, 2, 3, 4, 5], })
        vaultdb.append('integers', df_in)
        assert vaultdb.execute(
            'select count(*) from integers').fetchone()[0] == 5
        # cleanup
        vaultdb.execute("drop table integers")

    def test_arrow(self):
        pyarrow = pytest.importorskip("pyarrow")
        vaultdb.execute("select [1,2,3]")
        result = vaultdb.arrow()

    def test_begin_commit(self):
        vaultdb.begin()
        vaultdb.execute("create table tbl as select 1")
        vaultdb.commit()
        res = vaultdb.table("tbl")
        vaultdb.execute("drop table tbl")

    def test_begin_rollback(self):
        vaultdb.begin()
        vaultdb.execute("create table tbl as select 1")
        vaultdb.rollback()
        with pytest.raises(vaultdb.CatalogException):
            # Table does not exist
            res = vaultdb.table("tbl")

    def test_cursor(self):
        vaultdb.execute("create table tbl as select 3")
        duckdb_cursor = vaultdb.cursor()
        res = duckdb_cursor.table("tbl").fetchall()
        assert res == [(3,)]
        duckdb_cursor.execute("drop table tbl")
        with pytest.raises(vaultdb.CatalogException):
            # 'tbl' no longer exists
            vaultdb.table("tbl")

    def test_df(self):
        ref = [([1, 2, 3],)]
        vaultdb.execute("select [1,2,3]")
        res_df = vaultdb.fetch_df()
        res = vaultdb.query("select * from res_df").fetchall()
        assert res == ref

    def test_duplicate(self):
        vaultdb.execute("create table tbl as select 5")
        dup_conn = vaultdb.duplicate()
        dup_conn.table("tbl").fetchall()
        vaultdb.execute("drop table tbl")
        with pytest.raises(vaultdb.CatalogException):
            dup_conn.table("tbl").fetchall()

    def test_execute(self):
        assert [([4, 2],)] == vaultdb.execute("select [4,2]").fetchall()

    def test_executemany(self):
        # executemany does not keep an open result set
        # TODO: shouldn't we also have a version that executes a query multiple times with different parameters, returning all of the results?
        vaultdb.execute("create table tbl (i integer, j varchar)")
        vaultdb.executemany("insert into tbl VALUES (?, ?)", [
                            (5, 'test'), (2, 'duck'), (42, 'quack')])
        res = vaultdb.table("tbl").fetchall()
        assert res == [(5, 'test'), (2, 'duck'), (42, 'quack')]
        vaultdb.execute("drop table tbl")

    def test_fetch_arrow_table(self):
        # Needed for 'fetch_arrow_table'
        pyarrow = pytest.importorskip("pyarrow")

        vaultdb.execute("Create Table test (a integer)")

        for i in range(1024):
            for j in range(2):
                vaultdb.execute("Insert Into test values ('"+str(i)+"')")
        vaultdb.execute("Insert Into test values ('5000')")
        vaultdb.execute("Insert Into test values ('6000')")
        sql = '''
        SELECT  a, COUNT(*) AS repetitions
        FROM    test
        GROUP BY a
        '''

        result_df = vaultdb.execute(sql).df()

        arrow_table = vaultdb.execute(sql).fetch_arrow_table()

        arrow_df = arrow_table.to_pandas()
        assert result_df['repetitions'].sum() == arrow_df['repetitions'].sum()
        vaultdb.execute("drop table test")

    def test_fetch_df(self):
        ref = [([1, 2, 3],)]
        vaultdb.execute("select [1,2,3]")
        res_df = vaultdb.fetch_df()
        res = vaultdb.query("select * from res_df").fetchall()
        assert res == ref

    def test_fetch_df_chunk(self):
        vaultdb.execute("CREATE table t as select range a from range(3000);")
        query = vaultdb.execute("SELECT a FROM t")
        cur_chunk = query.fetch_df_chunk()
        assert (cur_chunk['a'][0] == 0)
        assert (len(cur_chunk) == 2048)
        cur_chunk = query.fetch_df_chunk()
        assert (cur_chunk['a'][0] == 2048)
        assert (len(cur_chunk) == 952)
        vaultdb.execute("DROP TABLE t")

    def test_fetch_record_batch(self):
        # Needed for 'fetch_arrow_table'
        pyarrow = pytest.importorskip("pyarrow")

        vaultdb.execute("CREATE table t as select range a from range(3000);")
        vaultdb.execute("SELECT a FROM t")
        record_batch_reader = vaultdb.fetch_record_batch(1024)
        chunk = record_batch_reader.read_all()
        assert (len(chunk) == 3000)

    def test_fetchall(self):
        assert [([1, 2, 3],)] == vaultdb.execute("select [1,2,3]").fetchall()

    def test_fetchdf(self):
        ref = [([1, 2, 3],)]
        vaultdb.execute("select [1,2,3]")
        res_df = vaultdb.fetchdf()
        res = vaultdb.query("select * from res_df").fetchall()
        assert res == ref

    def test_fetchmany(self):
        assert [(0,), (1,)] == vaultdb.execute(
            "select * from range(5)").fetchmany(2)

    def test_fetchnumpy(self):
        numpy = pytest.importorskip("numpy")
        vaultdb.execute("SELECT BLOB 'hello'")
        results = vaultdb.fetchall()
        assert results[0][0] == b'hello'

        vaultdb.execute("SELECT BLOB 'hello' AS a")
        results = vaultdb.fetchnumpy()
        assert results['a'] == numpy.array([b'hello'], dtype=object)

    def test_fetchone(self):
        assert (0,) == vaultdb.execute("select * from range(5)").fetchone()

    def test_from_arrow(self):
        assert None != vaultdb.from_arrow

    def test_from_csv_auto(self):
        assert None != vaultdb.from_csv_auto

    def test_from_df(self):
        assert None != vaultdb.from_df

    def test_from_parquet(self):
        assert None != vaultdb.from_parquet

    def test_from_parquet(self):
        assert None != vaultdb.from_parquet

    def test_from_query(self):
        assert None != vaultdb.from_query

    def test_from_substrait(self):
        assert None != vaultdb.from_substrait

    def test_get_substrait(self):
        assert None != vaultdb.get_substrait

    def test_get_substrait_json(self):
        assert None != vaultdb.get_substrait_json

    def test_get_table_names(self):
        assert None != vaultdb.get_table_names

    def test_install_extension(self):
        assert None != vaultdb.install_extension

    def test_load_extension(self):
        assert None != vaultdb.load_extension

    def test_query(self):
        assert [(3,)] == vaultdb.query("select 3").fetchall()

    def test_register(self):
        assert None != vaultdb.register

    def test_table(self):
        vaultdb.execute("create table tbl as select 1")
        assert [(1,)] == vaultdb.table("tbl").fetchall()
        vaultdb.execute("drop table tbl")

    def test_table_function(self):
        assert None != vaultdb.table_function

    def test_unregister(self):
        assert None != vaultdb.unregister

    def test_values(self):
        assert None != vaultdb.values

    def test_view(self):
        vaultdb.execute("create view vw as select range(5)")
        assert [([0, 1, 2, 3, 4],)] == vaultdb.view("vw").fetchall()
        vaultdb.execute("drop view vw")

    def test_description(self):
        assert None != vaultdb.description

    def test_close(self):
        assert None != vaultdb.close

    def test_wrap_coverage(self):
        con = vaultdb.default_connection
        assert str(con.__class__) == "<class 'vaultdb.VaultDBPyConnection'>"

        # Skip all of the initial __xxxx__ methods
        connection_methods = dir(con)
        filtered_methods = [
            method for method in connection_methods if not is_dunder_method(method)]
        for method in filtered_methods:
            # Assert that every method of VaultDBPyConnection is wrapped by the 'duckdb' module
            assert method in dir(vaultdb)


if __name__ == "__main__":
    import pytest
    import os
    test_file_path = os.path.abspath(__file__)
    pytest.main([test_file_path])
