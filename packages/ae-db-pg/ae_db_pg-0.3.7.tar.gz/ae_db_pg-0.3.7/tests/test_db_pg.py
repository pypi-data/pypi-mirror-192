""" test ae.db_pg """
import datetime
import os
import time

import pytest

import psycopg2

from ae.console import ConsoleApp
from ae.sys_core import SystemBase
from ae.db_core import CHK_BIND_VAR_PREFIX
from ae.db_pg import PostgresDb


UPDATED_TEST_STRING = 'Updated Test String'
TEST_DATE = datetime.datetime(2018, 1, 21, 22, 33, 44)
TEST_TIME = datetime.time(hour=21, minute=39)
UPDATED_TIME = datetime.time(hour=18, minute=12)


@pytest.fixture(scope="session")
def pg_env():
    """ prepare a generic Postgres server depending on the environment (local or on gitlab CI) """
    pkg_name = os.environ.get('CI_PROJECT_NAME')
    if pkg_name:
        pg_host = 'postgres'
        pg_port = 5432
        print(f"GITLAB CI project name: {pkg_name}")
        print(f"GITLAB PG VARS usr={os.environ.get('POSTGRES_USER')} pwd={os.environ.get('POSTGRES_PASSWORD')}"
              f" db={os.environ.get('POSTGRES_DB')}")
    else:
        # we are on a local developer machine, so let docker run a Postgres server image
        pg_host = 'localhost'
        pg_port = 15432
        ec = os.system(f"docker run -d --rm --name=tst -p {pg_port}:5432 postgres -c fsync=off")
        print(f"DOCKER RUN exit code: {ec}")

    # while True:
    #     ec = os.system(f"pg_isready -U postgres -h {pg_host} -p {pg_port} -d postgres")
    #     print(f"READY {ec}")
    #     if ec == 0:
    #         break
    # #time.sleep(10)
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # while True:
    #     try:
    #         s.connect((pg_host, pg_port))
    #         s.close()
    #         print(f"SOCKET CONNECTED {s}")
    #         break
    #     except socket.error as ex:
    #         print(f"SOCKET FAILURE {ex}")
    #         time.sleep(0.1)

    system = SystemBase('Test', ConsoleApp(),
                        credentials=dict(User='postgres', host=pg_host, port=str(pg_port), database='postgres'))

    yield PostgresDb(system)

    if not pkg_name:
        os.system("docker stop tst")


@pytest.fixture(scope="session")
def pg_conn(pg_env):
    """ wait for Postgres server is ready to connect to it """
    retries = 36
    while retries:
        ec = pg_env.connect()
        print(f"POSTGRES CONNECT RETRY {retries} {ec}")
        if not ec:
            break
        time.sleep(0.3)
        retries -= 1

    yield pg_env


table_name = 'UT_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


@pytest.fixture(scope="session")
def pg_table(pg_conn):
    """ prepare pg_conn with test_table """
    pg_conn.execute_sql("CREATE TABLE " + table_name + " (col_int INTEGER, col_vc VARCHAR(69), col_dt TIMESTAMP"
                                                       ", col_ti TIME)",
                        commit=True)
    assert not pg_conn.last_err_msg
    yield pg_conn


class TestPostgresDb:
    def test_connect(self, pg_conn):
        assert not pg_conn.connect()
        assert not pg_conn.last_err_msg

        pg_invalid = PostgresDb(SystemBase('Invalid', ConsoleApp(app_name='InvalidApp'), {}))
        err_msg = pg_invalid.connect()
        assert err_msg
        assert pg_invalid.last_err_msg == err_msg

    def test_select(self, pg_conn):
        assert pg_conn
        assert not pg_conn.connect()
        assert not pg_conn.select(cols=["1"])
        assert pg_conn.fetch_value() == 1
        assert not pg_conn.select(cols=["version()"])
        version = pg_conn.fetch_value()
        print(version)
        assert version

    def test_insert(self, pg_table):
        assert not pg_table.insert(table_name,
                                   dict(col_int=1, col_vc='test string', col_dt=TEST_DATE, col_ti=TEST_TIME),
                                   commit=True)

    def test_update_char(self, pg_table):
        assert not pg_table.update(table_name, dict(col_vc=UPDATED_TEST_STRING), dict(col_int=1), commit=True)

    def test_update_time_as_char(self, pg_table):
        assert not pg_table.update(table_name, dict(col_ti='15:19'), dict(col_int=1), commit=True)
        assert not pg_table.select(table_name, cols=['col_ti'], chk_values=dict(col_int=1))
        assert pg_table.fetch_value() == datetime.time(hour=15, minute=19)

    def test_update_time(self, pg_table):
        assert not pg_table.update(table_name, dict(col_ti=UPDATED_TIME), dict(col_int=1), commit=True)

    def test_upd_if_empty(self, pg_table):
        assert not pg_table.update(table_name, dict(col_vc='WillNotBeChanged'), dict(col_int=1), commit=True,
                                   locked_cols=['col_vc'])

    def test_select_from_table(self, pg_table):
        assert not pg_table.select(table_name, cols=['col_int', 'col_vc', 'col_dt', 'col_ti'],
                                   chk_values=dict(col_int=1))
        rows = pg_table.fetch_all()
        assert rows
        assert rows[0][0] == 1
        assert rows[0][1] == UPDATED_TEST_STRING
        assert rows[0][2] == TEST_DATE
        assert rows[0][3] == UPDATED_TIME

    def test_in_clause(self, pg_table):
        assert not pg_table.select(table_name, cols=['col_int', 'col_vc', 'col_dt', 'col_ti'],
                                   where_group_order="col_int IN (:" + CHK_BIND_VAR_PREFIX + "yz)",
                                   bind_vars=dict(yz=[0, 1, 2, 3, 4]))
        rows = pg_table.fetch_all()
        assert rows
        assert rows[0][0] == 1
        assert rows[0][1] == UPDATED_TEST_STRING
        assert rows[0][2] == TEST_DATE
        assert rows[0][3] == UPDATED_TIME

    def test_autocommit_in_transaction(self, pg_table):
        with pytest.raises(psycopg2.ProgrammingError):
            # noinspection SqlNoDataSourceInspection,SqlResolve
            assert not pg_table.execute_sql(f"UPDATE {table_name} SET col_int=3 WHERE col_int=1", auto_commit=True)

    def test_autocommit_exec(self, pg_table):
        assert not pg_table.commit()    # needed to end transaction of previous tests
        # noinspection SqlNoDataSourceInspection,SqlResolve
        assert not pg_table.execute_sql(f"UPDATE {table_name} SET col_int=3 WHERE col_int=1", auto_commit=True)
        assert not pg_table.select(table_name, cols=['col_int', 'col_vc', 'col_dt', 'col_ti'],
                                   where_group_order="col_int IN (:" + CHK_BIND_VAR_PREFIX + "yz)",
                                   bind_vars=dict(yz=[0, 1, 2, 3, 4]))
        rows = pg_table.fetch_all()
        assert rows
        assert rows[0][0] == 3
        assert rows[0][1] == UPDATED_TEST_STRING
        assert rows[0][2] == TEST_DATE
        assert rows[0][3] == UPDATED_TIME

    def test_auto_rollback(self, pg_table):
        # noinspection SqlResolve,SqlNoDataSourceInspection
        assert pg_table.execute_sql("UPDATE invalid_table_name SET col_int='invalid' WHERE col_int=1")
        assert pg_table.last_err_msg
