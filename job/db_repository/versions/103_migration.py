from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
plan = Table('plan', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=200)),
    Column('description', Text),
    Column('status', SmallInteger, default=ColumnDefault(1)),
    Column('created_time', DateTime),
    Column('public', SmallInteger, default=ColumnDefault(1)),
    Column('clicks', Integer, default=ColumnDefault(0)),
    Column('comment_num', Integer, default=ColumnDefault(0)),
    Column('plan_comment_num', Integer, default=ColumnDefault(0)),
    Column('collection_num', Integer, default=ColumnDefault(0)),
    Column('u_id', Integer),
    Column('s_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['plan'].columns['s_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['plan'].columns['s_id'].drop()
