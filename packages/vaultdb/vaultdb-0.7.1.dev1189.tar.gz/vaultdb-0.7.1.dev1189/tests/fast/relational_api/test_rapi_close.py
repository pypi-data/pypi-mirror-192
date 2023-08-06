import vaultdb
import pytest

# A closed connection should invalidate all relation's methods


class TestRAPICloseConnRel(object):
    def test_close_conn_rel(self, duckdb_cursor):
        con = vaultdb.connect()
        con.execute(
            "CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
        con.execute(
            "INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")
        rel = con.table("items")
        con.close()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            print(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            len(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.filter("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.project("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.order("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.aggregate("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.sum("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.count("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.median("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.quantile("", "")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.apply("", "")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.min("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.max("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.mean("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.var("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.std("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.value_counts("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.unique("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.union(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.except_(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.intersect(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.join(rel, "")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.distinct()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            print(rel.limit(1))
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.query("", "")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.execute()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.write_csv("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.insert_into("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.insert("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.create("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.create_view("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.to_arrow_table()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.arrow()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.to_df()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.df()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.fetchone()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.fetchall()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.map(lambda df: df['col0'].add(42).to_frame())
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.mad("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.mode("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.abs("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.prod("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.skew("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.kurt("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.sem("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.cumsum("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.cumprod("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.cummax("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.cummin("")
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.describe()
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            rel.fetchnumpy()
        con = vaultdb.connect()
        con.execute(
            "CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
        con.execute(
            "INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")
        valid_rel = con.table("items")

        # Test these bad boys when left relation is valid
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            valid_rel.union(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            valid_rel.except_(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            valid_rel.intersect(rel)
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            valid_rel.join(rel, "rel.items = valid_rel.items")

    def test_del_conn(self, duckdb_cursor):
        con = vaultdb.connect()
        con.execute(
            "CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
        con.execute(
            "INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")
        rel = con.table("items")
        del con
        with pytest.raises(vaultdb.ConnectionException, match='Connection has already been closed'):
            print(rel)


if __name__ == "__main__":
    import pytest
    import os
    test_file_path = os.path.abspath(__file__)
    pytest.main([test_file_path])
