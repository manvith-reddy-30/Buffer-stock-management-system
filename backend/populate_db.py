import pandas as pd
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.schemas import Hyderabad, Medak, Warangal, RangaReddy, Nalgonda

file_model_map = {
    'hyderabad.csv': Hyderabad,
    'medak.csv': Medak,
    'warangal.csv': Warangal,
    'rangareddy.csv': RangaReddy,
    'nalgonda.csv': Nalgonda,
}

def populate_table(file_name, model_class):
    db: Session = SessionLocal()
    df = pd.read_csv(f"data/{file_name}")
    for _, row in df.iterrows():
        entry = model_class(
            date=row['Date'],
            price=row['Price']
        )
        db.merge(entry)  
    db.commit()
    db.close()
    print(f"Inserted data for {file_name}")

if __name__ == "__main__":
    for file_name, model_class in file_model_map.items():
        populate_table(file_name, model_class)