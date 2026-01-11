import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine, Base
from app.models import User
from dotenv import load_dotenv


load_dotenv()

print("Testing database connection and models...\n")

print("Attempting to create tables....")
Base.metadata.create_all(bind=engine)
print("Tables created successfully! (or already exist)\n")

print("Tables in database:\n")
for table_name in Base.metadata.tables.keys():
    print(f" - {table_name}\n")

print("User table columns:")
for column in User.__table__.columns:
    print(f" - {column.name}: {column.type} \n")

print("All tests passed! Database and models are working.")






