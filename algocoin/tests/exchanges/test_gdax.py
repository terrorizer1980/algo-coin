from mock import patch, MagicMock


class TestExchange:
    def setup(self):
        pass
        # setup() before each test method

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        pass
        # setup_class() before any methods in this class

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test_init(self):
        from ...lib.config import ExchangeConfig
        from ...lib.exchanges.gdax import GDAXExchange

        with patch('os.environ'):
            ec = ExchangeConfig()
            e = GDAXExchange(ec)
            assert e

    def test_receive(self):
        from ...lib.config import ExchangeConfig
        from ...lib.exchanges.gdax import GDAXExchange
        from ...lib.enums import TickType

        with patch('os.environ'):
            ec = ExchangeConfig()
            e = GDAXExchange(ec)
            assert e

            e.ws = MagicMock()

            with patch('json.loads') as m1:
                for i, val in enumerate([TickType.MATCH,
                                         TickType.RECEIVED,
                                         TickType.OPEN,
                                         TickType.DONE,
                                         TickType.CHANGE,
                                         TickType.ERROR]):
                    m1.return_value = {'type': val, 'sequence': i}
                    e._receive()

    def test_seqnum_fix(self):
        from ...lib.config import ExchangeConfig
        from ...lib.exchanges.gdax import GDAXExchange
        from ...lib.enums import TickType

        with patch('os.environ'):
            ec = ExchangeConfig()
            e = GDAXExchange(ec)
            assert e

            e.ws = MagicMock()

            with patch('json.loads') as m1:
                m1.return_value = {'type': TickType.MATCH, 'sequence': 0}
                e._receive()
                for i, val in enumerate([TickType.MATCH,
                                         TickType.RECEIVED,
                                         TickType.OPEN,
                                         TickType.DONE,
                                         TickType.CHANGE,
                                         TickType.ERROR]):
                    m1.return_value = {'type': val, 'sequence': 6-i}
                    if i != 0:
                        assert e._missingseqnum
                    e._receive()
                assert e._missingseqnum == set()
