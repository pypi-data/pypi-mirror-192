"""
Functions for creating SQL tables.
"""

import typing as _t
import decimal as _decimal
import datetime as _datetime

import sqlalchemy as _sa
import sqlalchemy.engine as _sa_engine
import sqlalchemy.schema as _sa_schema
import sqlalchemy.engine as _sa_engine
from sqlalchemy import create_engine
from tinytim.rows import row_dicts_to_data as _row_dicts_to_data
from tinytim.data import column_names as _column_names

import fullmetalalchemy.type_convert as _type_convert
import fullmetalalchemy.features as _features
import fullmetalalchemy.insert as _insert
from fullmetalalchemy.features import get_session

create_session = get_session

_Record = _t.Dict[str, _t.Any]


def create_table(
    table_name: str,
    column_names:  _t.Sequence[str],
    column_types:  _t.Sequence,
    primary_key: _t.Sequence[str],
    engine: _sa_engine.Engine,
    schema:  _t.Optional[str] = None,
    autoincrement:  _t.Optional[bool] = False,
    if_exists:  _t.Optional[str] = 'error'
) -> _sa.Table:
    """
    Create a sql table from specifications.

    Parameters
    ----------
    table_name : str
    column_names : Sequence[str]
    column_types : Sequence
    primary_key : Sequence[str]
    engine : SqlAlchemy Engine
    schema : Optional[str]
    autoincrement : Optional[bool] default, None
    if_exists : Optional[str] default, 'error

    Returns
    -------
    sqlalchemy.Table
    
    Example
    -------
    >>> import fullmetalalchemy as fa

    >>> engine = fa.create_engine('sqlite:///data/test.db')
    >>> fa.get_table_names(engine)
    []
    >>> fa.create.create_table(
    ...         table_name='xy',
    ...         column_names=['id', 'x', 'y'],
    ...         column_types=[int, int, int],
    ...         primary_key=['id'],
    ...         engine=engine)
    Table('xy', MetaData(bind=Engine(sqlite:///data/test.db)),
    ...         Column('id', INTEGER(), table=<xy>, primary_key=True, nullable=False),
    ...         Column('x', INTEGER(), table=<xy>),
    ...         Column('y', INTEGER(), table=<xy>), schema=None)
     >>> fa.get_table_names(engine)
     ['xy']
    """
    cols = []
    
    for name, python_type in zip(column_names, column_types):
        sa_type = _type_convert._type_convert[python_type]
        if type(primary_key) is str:
            primary_key = [primary_key]
        if name in primary_key:
            col = _sa.Column(name, sa_type,
                            primary_key=True,
                            autoincrement=autoincrement)
        else:
            col = _sa.Column(name, sa_type)
        cols.append(col)

    metadata = _sa.MetaData(engine)
    table = _sa.Table(table_name, metadata, *cols, schema=schema)
    if if_exists == 'replace':
        drop_table_sql = _sa_schema.DropTable(table, if_exists=True)
        with engine.connect() as con:
            con.execute(drop_table_sql)
    table_creation_sql = _sa_schema.CreateTable(table)
    with engine.connect() as con:
        con.execute(table_creation_sql)
    return _features.get_table(table_name, engine, schema=schema)


def create_table_from_records(
    table_name: str,
    records:  _t.Sequence[_Record],
    primary_key: _t.Sequence[str],
    engine: _sa_engine.Engine,
    column_types:  _t.Optional[ _t.Sequence] = None,
    schema:  _t.Optional[str] = None,
    autoincrement:  _t.Optional[bool] = False,
    if_exists:  _t.Optional[str] = 'error',
    columns:  _t.Optional[ _t.Sequence[str]] = None,
    missing_value:  _t.Optional[_t.Any] = None
) -> _sa.Table:
    """Create a sql table from specs and insert records.
    Returns
    -------
    sqlalchemy.Table
    
    Example
    -------
    >>> import fullmetalalchemy as fa

    >>> engine = fa.create_engine('sqlite:///data/test.db')
    >>> fa.get_table_names(engine)
    []
    >>> records = [
    ...        {'id': 1, 'x': 1, 'y': 2},
    ...        {'id': 2, 'x': 2, 'y': 4},
    ...        {'id': 3, 'x': 4, 'y': 8},
    ...        {'id': 4, 'x': 8, 'y': 11}]
    >>> fa.create.create_table_from_records(
    ...         table_name='xy',
    ...         records=records,
    ...         primary_key=['id'],
    ...         engine=engine,
    ...         if_exists='replace')
    Table('xy', MetaData(bind=Engine(sqlite:///data/test.db)),
    ...         Column('id', INTEGER(), table=<xy>, primary_key=True, nullable=False),
    ...         Column('x', INTEGER(), table=<xy>),
    ...         Column('y', INTEGER(), table=<xy>), schema=None)
     >>> fa.get_table_names(engine)
     ['xy']
    """
    data = _row_dicts_to_data(records, columns, missing_value)
    if column_types is None:
        column_types = [_column_datatype(values) for values in data.values()]
    col_names = _column_names(data)
    table = create_table(table_name, col_names, column_types, primary_key, engine, schema, autoincrement, if_exists)
    _insert.insert_records(table, records, engine)
    return table


def _column_datatype(values: _t.Iterable) -> type:
    dtypes = [
        int, str, (int, float), _decimal.Decimal, _datetime.datetime,
        bytes, bool, _datetime.date, _datetime.time, 
        _datetime.timedelta, list, dict
    ]
    for value in values:
        for dtype in list(dtypes):
            if not isinstance(value, dtype):
                dtypes.pop(dtypes.index(dtype))
    if len(dtypes) == 2:
        if set([int, _t.Union[float, int]]) == {int, _t.Union[float, int]}:
            return int
    if len(dtypes) == 1:
        if dtypes[0] == _t.Union[float, int]:
            return float
        return dtypes[0]
    return str
    
def copy_table(
    new_name: str,
    sa_table: _sa.Table,
    engine: _sa_engine.Engine,
    if_exists: str = 'replace'
) -> _sa.Table:
    """
    Create a copy of an existing table with new name.
    """
    src_engine = engine
    dest_engine = engine
    schema = sa_table.schema
    src_name = sa_table.name
    dest_schema = schema
    dest_name = new_name

    # reflect existing columns, and create table object for oldTable
    src_engine._metadata = _sa.MetaData(bind=src_engine, schema=schema)  # type: ignore
    src_engine._metadata.reflect(src_engine)  # type: ignore
    
    # get columns from existing table 
    srcTable = _sa.Table(src_name, src_engine._metadata, schema=schema)  # type: ignore

    # create engine and table object for newTable
    dest_engine._metadata = _sa.MetaData(bind=dest_engine, schema=dest_schema)  # type: ignore
    destTable = _sa.Table(dest_name, dest_engine._metadata, schema=dest_schema)  # type: ignore

    if if_exists == 'replace':
        drop_table_sql = _sa_schema.DropTable(destTable, if_exists=True)
        with engine.connect() as con:
            con.execute(drop_table_sql)

    # copy schema and create newTable from oldTable
    for column in srcTable.columns:
        destTable.append_column(column.copy())
    destTable.create()

    # insert records from oldTable
    _insert.insert_from_table(srcTable, destTable, engine)
    return destTable