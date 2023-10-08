from typing import Optional
from datetime import datetime
from pydantic import BaseModel, root_validator, ConfigDict

class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str]

    @root_validator(pre=True)
    def generate_slug(cls, values):
        if 'title' in values:
            values['slug'] = values.get("title").replace(" ","-").lower()
        return values


class ShowBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: Optional[str]
    created_at: datetime
    author_id: int


class UpdateBlog(CreateBlog):
    pass

