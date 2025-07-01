import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(DATABASE_URL)

# List of your district files
districts = ["hyderabad", "medak", "nalgonda", "rangareddy", "warangal"]

for district in districts:
    df = pd.read_csv(f"data/{district}.csv")
    df.to_sql(district, con=engine, if_exists='replace', index=False)
    print(f"Uploaded data for {district} ✅")
