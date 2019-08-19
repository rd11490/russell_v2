import sqlalchemy
class Upsert(sqlalchemy.sql.expression.Insert):
    pass
from sqlalchemy.ext.compiler import compiles
@compiles(Upsert, "mysql")
def compile_upsert(insert_stmt, compiler, **kwargs):
    pks = [k.name for k in insert_stmt.table.primary_key]
    auto = None
    keys = insert_stmt.table.columns
    keys = [k.name for k in keys if k.name not in pks]
    insert = compiler.visit_insert(insert_stmt, **kwargs)
    ondup = 'ON DUPLICATE KEY UPDATE'
    updates = ', '.join(
        '{} = VALUES({})'.format(c.name, c.name)
        for c in insert_stmt.table.columns
        if c.name in keys
    )
    if auto is not None:
        last_id = '{} = LAST_INSERT_ID({})'.format(auto, auto)
        if updates:
            updates = ', '.join((last_id, updates))
        else:
            updates = last_id
    upsert = ' '.join((insert, ondup, updates))
    return upsert

