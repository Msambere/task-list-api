from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    # completed_at:Mapped[datetime] = mapped_column(default=None, nullable=True)
    completed_at:Mapped[Optional[datetime]]
    goal_id:Mapped[Optional[str]]=mapped_column(ForeignKey("goal.id"))
    goal: Mapped["Goal"] = relationship(back_populates="tasks")
    
    def to_dict(self):
        completed=False
        if self.completed_at:
            completed = True

        return {
            "id": self.id, 
            # "goal_id": self.goal_id,
            "title": self.title, 
            "description": self.description, 
            "is_complete":completed
            }