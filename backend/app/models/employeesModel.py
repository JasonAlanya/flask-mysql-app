from pydantic import BaseModel

class EmployeePostModel(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class EmployeeUpdateModel(BaseModel):
    name: str
    datetime: str
    department_id: int
    job_id: int

def employees_file_types():
    return {
        "id": int,
        "name": str,
        "datetime": str,
        "department_id": int,
        "job_id": int
    }