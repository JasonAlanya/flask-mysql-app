from pydantic import BaseModel

class JobPostModel(BaseModel):
    id: int
    job: str

class JobUpdateModel(BaseModel):
    job: str

def jobs_file_types():
    return {
        "id": int,
        "job": str,
    }