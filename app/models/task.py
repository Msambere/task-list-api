from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at:Mapped[datetime] = mapped_column(default=None, nullable=True)

    def to_dict(self):
        completed=False
        if self.completed_at:
            completed = True

        return {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete":completed
            }