from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, StringConstraints


class CourseBase(BaseModel):
    course_code: str = Field(
        ...,
        description="The course code of the course (e.g., COMS W4153)",
        json_schema_extra={"example": "COMS W4153"},
    )
    title: str = Field(
        ...,
        description="The title of the course",
        json_schema_extra={"example": "Cloud Computing"},
    )
    description: str = Field(
        ...,
        description="The description of the course",
        json_schema_extra={"example": "An introduction to cloud computing concepts, architectures, and technologies."},
    )
    credits: int = Field(
        ...,
        description="The number of credits for the course (typically 0-6)",
        json_schema_extra={"example": 3},
    )
    instructor: str = Field(
        ...,
        description="The primary instructor of the course",
        json_schema_extra={"example": "Professor Ferguson"},
    )
    schedule: str = Field(
        ...,
        description="The schedule of the course",
        json_schema_extra={"example": "MWF 10:00-11:15"},
    )
    semester: Optional[str] = Field(
        None,
        description="The semester when the course is offered",
        json_schema_extra={"example": "Fall 2025"},
    )
    location: Optional[str] = Field(
        None,
        description="The location where the course is held",
        json_schema_extra={"example": "Hamilton Hall 302"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "COMS W4153",
                    "title": "Cloud Computing",
                    "description": "An introduction to cloud computing concepts, architectures, and technologies.",
                    "credits": 3,
                    "instructor": "Professor Ferguson",
                    "schedule": "MWF 10:00-11:15",
                    "semester": "Fall 2025",
                    "location": "Hamilton Hall 302",
                }
            ]
        }
    }


class CourseCreate(CourseBase):
    """Creation payload for a Course."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "COMS W4111",
                    "title": "Introduction to Databases",
                    "description": "The fundamentals of database design and application development.",
                    "credits": 3,
                    "instructor": "Professor Gravano",
                    "schedule": "TTh 2:40-3:55",
                    "semester": "Spring 2025",
                    "location": "Mudd 233",
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Partial update for a Course; supply only fields to change."""
    course_code: Optional[str] = Field(
        None,
        description="The course code",
        json_schema_extra={"example": "COMS W4156"},
    )
    title: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Advanced Software Engineering"},
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Advanced topics in software engineering and system design."},
    )
    credits: Optional[int] = Field(
        None,
        json_schema_extra={"example": 3},
    )
    instructor: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Professor Kaiser"},
    )
    schedule: Optional[str] = Field(
        None,
        json_schema_extra={"example": "TTh 4:10-5:25"},
    )
    semester: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Spring 2025"},
    )
    location: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Mudd 644"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Advanced Cloud Computing", "credits": 4},
                {"instructor": "Professor Smith"},
                {
                    "schedule": "MW 2:40-3:55",
                    "location": "Schermerhorn 501",
                },
            ]
        }
    }


class CourseRead(CourseBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Course ID.",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "course_code": "COMS W4153",
                    "title": "Cloud Computing",
                    "description": "An introduction to cloud computing concepts, architectures, and technologies.",
                    "credits": 3,
                    "instructor": "Professor Ferguson",
                    "schedule": "MWF 10:00-11:15",
                    "semester": "Fall 2025",
                    "location": "Hamilton Hall 302",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }