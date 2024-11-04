from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import List


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id, 
            "title": self.title
            }

    def generate_tasks_list(self):
        task_list=[]
        for task in self.tasks:
            task_dict = task.to_dict()
            task_dict["goal_id"] = self.id
            task_list.append(task_dict)
        return task_list
    