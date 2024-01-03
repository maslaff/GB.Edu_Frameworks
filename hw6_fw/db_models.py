from databases import Database
import sqlalchemy


DATABASE_URL = "sqlite:///tasks_db.sqlite"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks_table = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(200)),
    sqlalchemy.Column("done", sqlalchemy.Boolean()),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
