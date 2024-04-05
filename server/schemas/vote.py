from pydantic import BaseModel, conint

class Voting(BaseModel):
    post_id: int
    dir: conint(le=1)