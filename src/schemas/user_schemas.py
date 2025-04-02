from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
        description="Username",
    )
    email: EmailStr


class UserCreate(UserSchema):
    password: str = Field(min_length=6, max_length=20, description="Password")


class UserResponse(UserSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
