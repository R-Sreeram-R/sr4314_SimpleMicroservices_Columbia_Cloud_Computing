from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field


class AssignmentBase(BaseModel):
    title: str = Field(
        ...,
        description="The title of the assignment",
        json_schema_extra={"example": "Programming Assignment 1: Web Scraper"},
    )
    description: Optional[str] = Field(
        None,
        description="Description of the assignment",
        json_schema_extra={"example": "Build a web scraper using Python to collect data from specified websites."},
    )
    assignment_type: str = Field(
        ...,
        description="The type of assignment (homework, project, exam, quiz, etc.)",
        json_schema_extra={"example": "homework"},
    )
    course_id: UUID = Field(
        ...,
        description="ID of the course this assignment belongs to",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    assigned_date: date = Field(
        ...,
        description="Date when the assignment was assigned",
        json_schema_extra={"example": "2025-09-01"},
    )
    due_date: date = Field(
        ...,
        description="Date when the assignment is due",
        json_schema_extra={"example": "2025-09-15"},
    )
    max_points: Optional[int] = Field(
        None,
        description="Maximum points possible for this assignment",
        json_schema_extra={"example": 100},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Programming Assignment 1: Web Scraper",
                    "description": "Build a web scraper using Python to collect data from specified websites.",
                    "assignment_type": "homework",
                    "course_id": "11111111-1111",
                    "assigned_date": "2025-09-01",
                    "due_date": "2025-09-15",
                    "max_points": 100,
                }
            ]
        }
    }


class AssignmentCreate(AssignmentBase):
    """Creation payload for an Assignment."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Midterm Exam",
                    "description": "Comprehensive exam covering chapters 1-8",
                    "assignment_type": "exam",
                    "course_id": "11111111",
                    "assigned_date": "2025-10-01",
                    "due_date": "2025-10-15",
                    "max_points": 200,
                }
            ]
        }
    }


class AssignmentUpdate(BaseModel):
    """Partial update for an Assignment; supply only fields to change."""
    title: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Updated Assignment Title"},
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Updated assignment description."},
    )
    assignment_type: Optional[str] = Field(
        None,
        json_schema_extra={"example": "project"},
    )
    course_id: Optional[UUID] = Field(
        None,
        json_schema_extra={"example": "22222222"},
    )
    assigned_date: Optional[date] = Field(
        None,
        json_schema_extra={"example": "2025-09-05"},
    )
    due_date: Optional[date] = Field(
        None,
        json_schema_extra={"example": "2025-09-20"},
    )
    max_points: Optional[int] = Field(
        None,
        json_schema_extra={"example": 150},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Final Project", "max_points": 150},
                {"due_date": "2025-09-25"},
                {
                    "assignment_type": "project",
                    "description": "Updated project requirements",
                },
            ]
        }
    }


class AssignmentRead(AssignmentBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Assignment ID.",
        json_schema_extra={"example": "33333333"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-09-01T08:00:00Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-09-05T14:30:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "33333333-3333-4333-8333-333333333333",
                    "title": "Programming Assignment 1: Web Scraper",
                    "description": "Build a web scraper using Python.",
                    "assignment_type": "homework",
                    "course_id": "ABC 123",
                    "assigned_date": "2025-09-01",
                    "due_date": "2025-09-15",
                    "max_points": 100,
                    "created_at": "2025-09-01T08:00:00Z",
                    "updated_at": "2025-09-05T14:30:00Z",
                }
            ]
        }
    }