import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import Grievance
from app.db.connection import get_db

def fetch_aggregated_data(db: Session):
    grievances = db.query(Grievance).all()
    if not grievances:
        return None

    data = [
        {"date": g.created_at.date(), "region": g.region, "category": g.category}
        for g in grievances if g.created_at and g.category and g.region
    ]

    df = pd.DataFrame(data)
    if df.empty:
        return None

    df = df.groupby(["date", "region", "category"]).size().reset_index(name="count")
    return df
