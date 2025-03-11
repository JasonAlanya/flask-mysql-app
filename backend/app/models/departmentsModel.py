from pydantic import BaseModel

class DepartmentPostModel(BaseModel):
    id: int
    department: str

class DepartmentUpdateModel(BaseModel):
    department: str

def departments_file_types():
    return {
        "id": int,
        "department": str,
    }