from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.db_singleton import get_db
from backend.model.Robot import Robot

router = APIRouter(prefix="/robots", tags=["robots"])

@router.get("/", response_model=list[Robot.Schema])
def get_robots(db: Session = Depends(get_db)):
    robots = db.query(Robot).all()
    return [r.to_schema() for r in robots]
