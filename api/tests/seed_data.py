import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from seed_helper import *

engine = create_engine('postgresql://postgres:password@localhost:5432/sowingo_varma')
dbConnection = engine.connect()

employees = create_users(min=3, max=15)
managers = create_users(min=1, max=3, manager=True)
users = employees.append(managers)

users.to_sql(
    "users",
    con=engine,
    index=False,
    if_exists='append'
)

users = pd.read_sql("SELECT * FROM users;", dbConnection, index_col="id").reset_index()

vacations = create_vacations(min=2, max=4, users=users)
overlapping_vacations = create_overlapping_vacations(min=2, max=4, users=users, vacations=vacations)
vacations = vacations.append(overlapping_vacations)

vacations.to_sql(
    "vacations",
    con=engine,
    index=False,
    if_exists='append'
)


print(users)
df = pd.read_sql("SELECT * FROM vacations;", dbConnection)
print(df)

