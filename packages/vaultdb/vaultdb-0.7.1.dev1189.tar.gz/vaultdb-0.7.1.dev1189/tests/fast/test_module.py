import vaultdb


class TestModule:
    def test_paramstyle(self):
        assert vaultdb.paramstyle == "qmark"

    def test_threadsafety(self):
        assert vaultdb.threadsafety == 1

    def test_apilevel(self):
        assert vaultdb.apilevel == "1.0"
