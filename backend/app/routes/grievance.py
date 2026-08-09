from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import models, schemas, connection
from app.services.nlp_processor import process_grievance
from app.auth.dependencies import get_current_user, require_admin


router = APIRouter(prefix="/grievance", tags=["Grievance"])


#Submit a new grievance (USER only)
@router.post("/submit", response_model=schemas.GrievanceResponse)
def submit_grievance(
    grievance: schemas.GrievanceCreate,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Allows a logged-in user to submit a grievance.
    Automatically processes it using the NLP module
    and links it to the user's ID.
    """
    try:
        # Run NLP pipeline for categorization, priority, and region extraction
        processed = process_grievance(grievance.description)

        # Link the grievance to the logged-in user
        new_grievance = models.Grievance(
            **processed,
            user_id=current_user.id
        )

        db.add(new_grievance)
        db.commit()
        db.refresh(new_grievance)

        return new_grievance

    except Exception as e:
        print(f"Error while submitting grievance: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit grievance")


#Get all grievances for the logged-in user
@router.get("/my-grievances", response_model=List[schemas.GrievanceResponse])
def get_my_grievances(
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Fetch all grievances submitted by the currently logged-in user.
    """
    grievances = db.query(models.Grievance).filter(models.Grievance.user_id == current_user.id).all()
    return grievances


#Admin-only: View all grievances
@router.get("/all", response_model=List[schemas.GrievanceResponse])
def get_all_grievances(
    db: Session = Depends(connection.get_db),
    admin=Depends(require_admin)
):
    """
    Allows admin to view all grievances in the system.
    """
    grievances = db.query(models.Grievance).order_by(models.Grievance.created_at.desc()).all()
    return grievances


#Admin-only: Update grievance status
@router.put("/{grievance_id}/status")
def update_grievance_status(
    grievance_id: int,
    status: str,
    db: Session = Depends(connection.get_db),
    admin=Depends(require_admin)
):
    """
    Allows admin to update the status of a specific grievance.
    e.g., Resolved, In Progress, Closed, etc.
    """
    grievance = db.query(models.Grievance).filter(models.Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    grievance.status = status
    db.commit()
    return {"message": f"Grievance ID {grievance_id} updated to status '{status}'."}
