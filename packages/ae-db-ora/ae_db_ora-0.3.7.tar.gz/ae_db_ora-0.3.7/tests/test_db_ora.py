"""
The unit tests here are patching and mocking parts of the cx_Oracle package,
because gitlab CI does not provide a Oracle database server service.
"""
import datetime
import os
from unittest.mock import patch, MagicMock

from ae.console import ConsoleApp
from ae.sys_core import SystemBase
from ae.db_core import CHK_BIND_VAR_PREFIX
from ae.db_ora import OraDb


USER = 'oracleUser'
# noinspection HardcodedPassword
PASSWORD = 'oraclePassword'
DSN = 'oracleDSN'
APP_NAME = 'test_db-ora'
name_space = "CLIENTCONTEXT"
APP_CONTEXT = [
    (name_space, "APP", APP_NAME),
    (name_space, "LANG", "Python"),
    (name_space, "MOD", "ae.db_ora")
]
UPDATED_TEST_STRING = 'Updated Test String'
TEST_DATE = datetime.datetime(2018, 1, 21, 22, 33, 44)
TEST_TIME = datetime.time(hour=21, minute=39)
UPDATED_TIME = datetime.time(hour=18, minute=12)

test_table = 'UT_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

cae = ConsoleApp('test ae database layer for oracle', app_name=APP_NAME)
dsn_system_base = SystemBase('Oracle', cae, dict(User=USER, Password=PASSWORD, DSN=DSN))
dsn_db = OraDb(dsn_system_base)

host_system_base = SystemBase('Oracle', cae, dict(User=USER, Password=PASSWORD, Host='db_host', Port='db_port'))
host_db = OraDb(host_system_base)

sid_system_base = SystemBase('Oracle', cae, dict(User=USER, Password=PASSWORD, DSN='db_host:db_port/@SID'))
sid_db = OraDb(sid_system_base)

service_system_base = SystemBase('Oracle', cae, dict(User=USER, Password=PASSWORD, DSN='db_host:db_port/Service'))
service_db = OraDb(service_system_base)


class TestOraDbDsn:
    def test_db_init(self):
        assert os.environ['NLS_LANG'] == '.AL32UTF8'
        assert dsn_db.param_style == 'named'
        assert dsn_db.conn is None
        assert dsn_db.curs is None

    @patch('cx_Oracle.apilevel', create=True, return_value='api_level')
    @patch('cx_Oracle.clientversion', create=True, return_value='client_version')
    @patch('cx_Oracle.connect', return_value=MagicMock(name='conn_mock', encoding='encoding', nencoding='nencoding'))
    def test_prepare_connect_dsn(self, cx_connect, client_version, api_level):
        assert not dsn_db.connect()
        assert not dsn_db.last_err_msg
        assert cx_connect.called
        assert cx_connect.call_args[1] == dict(user=USER, password=PASSWORD, dsn=DSN, appcontext=APP_CONTEXT)
        assert client_version.return_value == 'client_version'
        assert api_level.return_value == 'api_level'
        assert dsn_db.conn
        assert dsn_db.curs

    @patch('cx_Oracle.apilevel', create=True, return_value='api_level')
    @patch('cx_Oracle.clientversion', create=True, return_value='client_version')
    @patch('cx_Oracle.connect', return_value=MagicMock(name='conn_mock', encoding='encoding', nencoding='nencoding'))
    def test_prepare_connect_oracle_v5(self, _cx_connect, _client_version, _api_level):
        with patch('cx_Oracle.__version__', '5'):
            assert not dsn_db.connect()

    def test_prepare_connect_oracle_exception(self):
        assert dsn_db.connect()

    def test_create_table(self):
        dsn_db.execute_sql("CREATE TABLE " + test_table + " (col_int INTEGER, col_vc VARCHAR(69), col_dt DATE)",
                           commit=True)
        assert not dsn_db.last_err_msg

    def test_insert(self):
        assert not dsn_db.insert(test_table,
                                 dict(col_int=1, col_vc='test string', col_dt=TEST_DATE),
                                 commit=True)

    def test_update(self):
        assert not dsn_db.update(test_table, dict(col_vc=UPDATED_TEST_STRING), dict(col_int=1), commit=True)

    def test_upd_if_empty(self):
        assert not dsn_db.update(test_table, dict(col_vc='WillNotBeChanged'), dict(col_int=1), commit=True,
                                 locked_cols=['col_vc'])

    def test_select(self):
        assert not dsn_db.select(test_table, cols=['col_int', 'col_vc', 'col_dt'],
                                 where_group_order="col_int >= :" + CHK_BIND_VAR_PREFIX + "xy", bind_vars=dict(xy=0))
        rows = dsn_db.fetch_all()
        assert rows

        assert not dsn_db.select(test_table, cols=['col_int', 'col_vc', 'col_dt'], chk_values=dict(col_int=1))
        rows = dsn_db.fetch_all()
        assert rows

    def test_in_clause(self):
        assert not dsn_db.select(test_table, cols=['col_int', 'col_vc', 'col_dt'],
                                 where_group_order="col_int IN (:" + CHK_BIND_VAR_PREFIX + "yz)",
                                 bind_vars=dict(yz=[0, 1, 2, 3, 4]))
        rows = dsn_db.fetch_all()
        assert rows


class TestOraDbHost:
    def test_db_init(self):
        assert os.environ['NLS_LANG'] == '.AL32UTF8'
        assert host_db.param_style == 'named'
        assert host_db.conn is None
        assert host_db.curs is None

    @patch('cx_Oracle.apilevel', create=True, return_value='api_level')
    @patch('cx_Oracle.clientversion', create=True, return_value='client_version')
    @patch('cx_Oracle.connect', return_value=MagicMock(name='conn_mock', encoding='encoding', nencoding='nencoding'))
    def test_prepare_connect_dsn(self, cx_connect, client_version, api_level):
        assert not host_db.connect()
        assert not host_db.last_err_msg
        assert cx_connect.called
        host_dsn = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db_host)(PORT=db_port))(CONNECT_DATA=))'
        assert cx_connect.call_args[1] == dict(user=USER, password=PASSWORD, dsn=host_dsn, appcontext=APP_CONTEXT)
        assert client_version.return_value == 'client_version'
        assert api_level.return_value == 'api_level'
        assert host_db.conn
        assert host_db.curs


class TestOraDbSID:
    def test_db_init(self):
        assert os.environ['NLS_LANG'] == '.AL32UTF8'
        assert sid_db.param_style == 'named'
        assert sid_db.conn is None
        assert sid_db.curs is None

    @patch('cx_Oracle.apilevel', create=True, return_value='api_level')
    @patch('cx_Oracle.clientversion', create=True, return_value='client_version')
    @patch('cx_Oracle.connect', return_value=MagicMock(name='conn_mock', encoding='encoding', nencoding='nencoding'))
    def test_prepare_connect_dsn(self, cx_connect, client_version, api_level):
        assert not sid_db.connect()
        assert not sid_db.last_err_msg
        assert cx_connect.called
        host_dsn = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db_host)(PORT=db_port))(CONNECT_DATA=(SID=SID)))'
        assert cx_connect.call_args[1] == dict(user=USER, password=PASSWORD, dsn=host_dsn, appcontext=APP_CONTEXT)
        assert client_version.return_value == 'client_version'
        assert api_level.return_value == 'api_level'
        assert sid_db.conn
        assert sid_db.curs


class TestOraDbServiceName:
    def test_db_init(self):
        assert os.environ['NLS_LANG'] == '.AL32UTF8'
        assert service_db.param_style == 'named'
        assert service_db.conn is None
        assert service_db.curs is None

    @patch('cx_Oracle.apilevel', create=True, return_value='api_level')
    @patch('cx_Oracle.clientversion', create=True, return_value='client_version')
    @patch('cx_Oracle.connect', return_value=MagicMock(name='conn_mock', encoding='encoding', nencoding='nencoding'))
    def test_prepare_connect_dsn(self, cx_connect, client_version, api_level):
        assert not service_db.connect()
        assert not service_db.last_err_msg
        assert cx_connect.called
        dsn = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db_host)(PORT=db_port))(CONNECT_DATA=(SERVICE_NAME=Service)))'
        assert cx_connect.call_args[1] == dict(user=USER, password=PASSWORD, dsn=dsn, appcontext=APP_CONTEXT)
        assert client_version.return_value == 'client_version'
        assert api_level.return_value == 'api_level'
        assert service_db.conn
        assert service_db.curs


class TestRefParamHelpers:
    def test_prepare_ref_param_int(self):
        ref_var = host_db.prepare_ref_param(6)
        assert ref_var

    def test_prepare_ref_param_str(self):
        ref_var = host_db.prepare_ref_param('6')
        assert ref_var

    def test_prepare_ref_param_date(self):
        ref_var = host_db.prepare_ref_param(datetime.datetime.now())
        assert ref_var

    def test_get_value(self):
        ref_var = host_db.prepare_ref_param('6')
        assert host_db.get_value(ref_var)

    def test_set_value(self):
        ref_var = host_db.prepare_ref_param('6')
        assert host_db.set_value(ref_var, '9') is None  # no return value
