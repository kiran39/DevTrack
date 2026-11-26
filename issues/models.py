from django.db import models
from datetime import datetime
from abc import ABC, abstractmethod
from django.utils import timezone



class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }

class  Issue(BaseEntity):
    def __init__(self, id, title, description, status, priority, reporter_id ,created_at = None): 
        self.id =id
        self.title =title
        self.description =description
        self.status =status
        self.priority =priority   
        self.reporter_id =reporter_id
        self.created_at = created_at or timezone.now()


    def validate(self):
        if not self.title:
            raise ValueError('Title cannot be empty')
        if self.priority not in[ 'low', 'medium', 'high', 'critical']:
            raise ValueError('invalid priority')
        if self.status not in ['open', 'in_progress', 'resolved', 'closed']:
            raise ValueError('Invalid status')
        if not isinstance(self.created_at , datetime):
            raise ValueError('created_at must be a datetime object')
            
    def describe(self):
            return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} — low priority, handle when free"
        
