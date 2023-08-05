"""
Functions for droping SQL tables.
"""

import typing as _t

import sqlalchemy as _sa
import sqlalchemy.engine as _sa_engine
import sqlalchemy.schema as _sa_schema

import fullmetalalchemy.features as _features
import fullmetalalchemy.exceptions as _ex


def drop_table(
    table: _t.Union[_sa.Table, str],
    engine: _t.Optional[_sa_engine.Engine] = None,
    if_exists: bool = True,
    schema: _t.Optional[str] = None
) -> None:
    """
    Example
    -------
    >>> import sqlalchemize as sz

    >>> engine, table = sz.get_engine_table('sqlite:///test.db', 'xy')
    >>> sz.get_table_names(engine)
    ['xy']

    >>> sz.drop.drop_table(table, engine)
    >>> sz.get_table_names(engine)
    []
    """
    if isinstance(table, str):
        if table not in _sa.inspect(engine).get_table_names(schema=schema):
            if if_exists:
                return
        if engine is None:
            raise ValueError('Must pass engine if table is str.')
        table = _features.get_table(table, engine, schema=schema)
    sql = _sa_schema.DropTable(table, if_exists=if_exists)
    engine = _ex.check_for_engine(table, engine)
    with engine.connect() as con:
        con.execute(sql)