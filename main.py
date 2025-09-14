from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.course import CourseCreate, CourseRead, CourseUpdate
from models.assignment import AssignmentCreate, AssignmentRead, AssignmentUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
courses: Dict[UUID, CourseRead] = {}
assignments: Dict[UUID, AssignmentRead] = {}

app = FastAPI(
    title="Person/Address/Course/Assignment API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Course, and Assignment",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

@app.delete("/addresses/{address_id}", status_code=204)
def delete_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    del addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------

@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------

@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    course_read = CourseRead(**course.model_dump())
    courses[course_read.id] = course_read
    return course_read

@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    course_code: Optional[str] = Query(None, description="Filter by course code"),
    title: Optional[str] = Query(None, description="Filter by course title"),
    instructor: Optional[str] = Query(None, description="Filter by instructor"),
    credits: Optional[int] = Query(None, description="Filter by number of credits"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
):
    results = list(courses.values())

    if course_code is not None:
        results = [c for c in results if c.course_code == course_code]
    if title is not None:
        results = [c for c in results if c.title == title]
    if instructor is not None:
        results = [c for c in results if c.instructor == instructor]
    if credits is not None:
        results = [c for c in results if c.credits == credits]
    if semester is not None:
        results = [c for c in results if c.semester == semester]

    return results

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.patch("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    courses[course_id] = CourseRead(**stored)
    return courses[course_id]

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]

# -----------------------------------------------------------------------------
# Assignment endpoints
# -----------------------------------------------------------------------------

@app.post("/assignments", response_model=AssignmentRead, status_code=201)
def create_assignment(assignment: AssignmentCreate):
    assignment_read = AssignmentRead(**assignment.model_dump())
    assignments[assignment_read.id] = assignment_read
    return assignment_read

@app.get("/assignments", response_model=List[AssignmentRead])
def list_assignments(
    title: Optional[str] = Query(None, description="Filter by assignment title"),
    assignment_type: Optional[str] = Query(None, description="Filter by assignment type"),
    course_id: Optional[UUID] = Query(None, description="Filter by course ID"),
    due_date: Optional[str] = Query(None, description="Filter by due date (YYYY-MM-DD)"),
    assigned_date: Optional[str] = Query(None, description="Filter by assigned date (YYYY-MM-DD)"),
):
    results = list(assignments.values())

    if title is not None:
        results = [a for a in results if a.title == title]
    if assignment_type is not None:
        results = [a for a in results if a.assignment_type == assignment_type]
    if course_id is not None:
        results = [a for a in results if a.course_id == course_id]
    if due_date is not None:
        results = [a for a in results if str(a.due_date) == due_date]
    if assigned_date is not None:
        results = [a for a in results if str(a.assigned_date) == assigned_date]

    return results

@app.get("/assignments/{assignment_id}", response_model=AssignmentRead)
def get_assignment(assignment_id: UUID):
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignments[assignment_id]

@app.patch("/assignments/{assignment_id}", response_model=AssignmentRead)
def update_assignment(assignment_id: UUID, update: AssignmentUpdate):
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    stored = assignments[assignment_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    assignments[assignment_id] = AssignmentRead(**stored)
    return assignments[assignment_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address/Course/Assignment API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)