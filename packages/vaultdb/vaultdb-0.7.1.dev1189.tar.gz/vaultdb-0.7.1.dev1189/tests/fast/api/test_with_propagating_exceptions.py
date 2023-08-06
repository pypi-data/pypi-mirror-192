import pytest
import vaultdb

class TestWithPropagatingExceptions(object):

    def test_with(self):
        # Should propagate exception raised in the 'with vaultdb.connect() ..'
        with pytest.raises(vaultdb.ParserException, match="syntax error at or near *"):
            with vaultdb.connect() as con:
                print('before')
                con.execute('invalid')
                print('after')

        # Does not raise an exception
        with vaultdb.connect() as con:
            print('before')
            con.execute('select 1')
            print('after')
