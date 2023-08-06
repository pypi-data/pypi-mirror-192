""" unit tests """
import datetime
import pytest

from typing import cast

from ae.parse_date import parse_date


class TestHelpers:
    def test_parse_date_only(self):
        assert parse_date('2033-12-24') == datetime.datetime(year=2033, month=12, day=24)
        assert parse_date('2033-12-24', ret_date=True) == datetime.date(year=2033, month=12, day=24)
        assert parse_date('2033-12-24', ret_date=None) == datetime.date(year=2033, month=12, day=24)

    def test_parse_date_hour_min(self):
        assert parse_date('2033-12-24 12:59') == datetime.datetime(year=2033, month=12, day=24, hour=12, minute=59)
        assert parse_date('2033-12-24 12:59', ret_date=True) == datetime.date(year=2033, month=12, day=24)
        assert parse_date('2033-12-24 12:59', ret_date=None) == datetime.datetime(year=2033, month=12, day=24,
                                                                                  hour=12, minute=59)

        assert parse_date('2033-12-24T12:59') == datetime.datetime(year=2033, month=12, day=24, hour=12, minute=59)
        assert parse_date('2033-12-24T12:59', ret_date=True) == datetime.date(year=2033, month=12, day=24)
        assert parse_date('2033-12-24T12:59', ret_date=None) == datetime.datetime(year=2033, month=12, day=24,
                                                                                  hour=12, minute=59)

    def test_parse_date_hour_min_sec(self):
        assert parse_date('2033-12-24 12:59:12') == datetime.datetime(year=2033, month=12, day=24, hour=12,
                                                                      minute=59, second=12)
        assert parse_date('2033-12-24 12:59:12', ret_date=True) == datetime.date(year=2033, month=12, day=24)
        assert parse_date('2033-12-24 12:59:12', ret_date=None) == datetime.datetime(year=2033, month=12, day=24,
                                                                                     hour=12, minute=59, second=12)

        assert parse_date('2033-12-24T12:59:12') == datetime.datetime(year=2033, month=12, day=24,
                                                                      hour=12, minute=59, second=12)
        assert parse_date('2033-12-24T12:59:12', ret_date=True) == datetime.date(year=2033, month=12, day=24)
        assert parse_date('2033-12-24T12:59:12', ret_date=None) == datetime.datetime(year=2033, month=12, day=24,
                                                                                     hour=12, minute=59, second=12)

        assert parse_date('2033-1-2 3:4:5') == datetime.datetime(year=2033, month=1, day=2, hour=3, minute=4, second=5)
        assert parse_date('2033-1-2 3:4:5', ret_date=True) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('2033-1-2 3:4:5', ret_date=None) == datetime.datetime(year=2033, month=1, day=2,
                                                                                hour=3, minute=4, second=5)

        assert parse_date('2033-1-2 3:4:5.6') == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)
        assert parse_date('2033-1-2 3:4:5.6', ret_date=True) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('2033-1-2 3:4:5.6', ret_date=None) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)

    def test_parse_date_format(self):
        alt_format = "%d.%m.%Y %H:%M:%S.%f+%z"
        assert parse_date('2033-1-2 3:4:5.6', alt_format, replace=dict(microsecond=0)) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5)
        assert parse_date('2033-1-2 3:4:5.6', alt_format, ret_date=True) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('2033-1-2 3:4:5.6', alt_format, ret_date=None) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)

        alt_format = "%d.%m.%Y %H:%M:%S.%f"
        assert parse_date('2.1.2033 3:4:5.6', alt_format) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)
        assert parse_date('2.1.2033 3:4:5.6', alt_format, ret_date=True) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('2.1.2033 3:4:5.6', alt_format, ret_date=None) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)

        assert parse_date('2.1.2033', alt_format) == datetime.datetime(year=2033, month=1, day=2)
        assert parse_date('2.1.2033', alt_format, ret_date=True) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('2.1.2033', alt_format, ret_date=None) == datetime.date(year=2033, month=1, day=2)

        alt_format = "%y.%m.%d_%H:%M:%S.%f"
        dts = ('_', )
        assert parse_date('33.1.2_3:4:5.6', alt_format) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)
        assert parse_date('33.1.2_3:4:5.6', alt_format, ret_date=True) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('33.1.2_3:4:5.6', alt_format, ret_date=None) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('33.1.2_3:4:5.6', alt_format, ret_date=None, dt_seps=dts) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)

        assert parse_date('33.1.2', alt_format) is None
        assert parse_date('33.1.2', alt_format, dt_seps=dts) == datetime.datetime(year=2033, month=1, day=2)
        assert parse_date('33.1.2', alt_format, ret_date=True, dt_seps=dts) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('33.1.2', alt_format, ret_date=None, dt_seps=dts) == datetime.date(year=2033, month=1, day=2)

        dts = ('T', ' ', 'x', '_', )
        assert parse_date('33.1.2_3:4:5.6', alt_format, ret_date=None, dt_seps=dts) == datetime.datetime(
            year=2033, month=1, day=2, hour=3, minute=4, second=5, microsecond=600000)
        assert parse_date('33.1.2', alt_format) is None
        assert parse_date('33.1.2', alt_format, dt_seps=dts) == datetime.datetime(year=2033, month=1, day=2)
        assert parse_date('33.1.2', alt_format, ret_date=True, dt_seps=dts) == datetime.date(year=2033, month=1, day=2)
        assert parse_date('33.1.2', alt_format, ret_date=None, dt_seps=dts) == datetime.date(year=2033, month=1, day=2)

        alt_format = '%Y%m%d %H%M%S.%f'
        assert parse_date('20330102 122748.69', alt_format) == datetime.datetime(
            year=2033, month=1, day=2, hour=12, minute=27, second=48, microsecond=690000)

    def test_parse_date_invalid(self):
        assert parse_date('2033-12-24 12:59:12:36') is None
        assert parse_date('xx-yy-zz a:b:c') is None

    def test_parse_date_exception(self):
        with pytest.raises(AttributeError):
            parse_date(cast(str, None))
