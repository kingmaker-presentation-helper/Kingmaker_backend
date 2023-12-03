from pydantic import BaseModel, BaseConfig, Field


class UserLoginSchema(BaseModel):
    email: str = Field(title="사용자 이메일")
    password: str = Field(title="사용자 비밀번호")
    class Config(BaseConfig):
        schema_extra = {
            "example":{
                "email": "admin@admin.com",
                "password": "1234",
            }
        }