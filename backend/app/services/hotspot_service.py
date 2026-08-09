import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import Grievance
from app.db.connection import get_db
from sklearn.cluster import KMeans
import numpy as np

def detect_hotspots(limit=10, use_clustering=True):
    """Detect hotspot regions with or without clustering"""
    db = next(get_db())
    grievances = db.query(Grievance).all()

    if not grievances:
        return {"message": "No grievance data yet."}

    data = [
        {
            "region": g.region,
            "latitude": g.latitude,
            "longitude": g.longitude,
            "category": g.category
        }
        for g in grievances if g.latitude and g.longitude
    ]
    df = pd.DataFrame(data)
    if df.empty:
        return {"message": "No valid geolocation data yet."}

    #Basic Region Aggregation (for macro-hotspots)-----------
    region_hotspots = (
        df.groupby(["region", "latitude", "longitude"])
        .size()
        .reset_index(name="complaint_count")
        .sort_values(by="complaint_count", ascending=False)
        .head(limit)
    )

    result = {
        "region_hotspots": region_hotspots.to_dict(orient="records")
    }

    #Optional K-Means Micro-Hotspot Detection ---
    if use_clustering and len(df) >= 5:  # apply clustering only if enough data
        coords = df[["latitude", "longitude"]].values
        k = min(5, len(coords))  #avoid invalid K
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(coords)
        centers = kmeans.cluster_centers_

        cluster_points = [
            {
                "cluster_id": int(i),
                "latitude": float(lat),
                "longitude": float(lon),
                "complaint_density": int(sum(kmeans.labels_ == i))
            }
            for i, (lat, lon) in enumerate(centers)
        ]

        result["cluster_hotspots"] = cluster_points

    return result
