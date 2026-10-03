from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, AliasChoices, field_validator, model_validator

class Register(BaseModel):
    username: str = Field(min_length=3, max_length=40, pattern=r'^[a-zA-Z0-9_-]+$')
    email: str = Field(max_length=254)
    password: str = Field(min_length=12, max_length=72)
    role: Literal['hacker', 'company']
    bio: str = Field(default='', max_length=2000)
    github: str = Field(default='', max_length=500)
    tryhackme: str = Field(default='', max_length=500)
    hackthebox: str = Field(default='', max_length=500)
    company_name: str = Field(default='', max_length=160)
    industry: str = Field(default='', max_length=100)
    website_url: str = Field(default='', max_length=500)

    @field_validator('password')
    @classmethod
    def password_bytes(cls, value):
        if len(value.encode()) > 72:
            raise ValueError('Password must not exceed 72 UTF-8 bytes.')
        return value

    @field_validator('github', 'tryhackme', 'hackthebox', 'website_url')
    @classmethod
    def url(cls, value):
        if value:
            return str(HttpUrl(value))
        return value

    @model_validator(mode='after')
    def company_fields(self):
        if self.role == 'company' and not all(s.strip() for s in (self.company_name, self.industry, self.website_url)):
            raise ValueError('Company name, industry and website are required.')
        return self

class Login(BaseModel):
    identifier: str = Field(min_length=1, max_length=254, validation_alias=AliasChoices('identifier', 'email'))
    password: str = Field(max_length=200)

class EmailCheck(BaseModel):
    email: str = Field(max_length=254)

class Verify(BaseModel):
    token: str = Field(min_length=20, max_length=200)

class ProgramCreate(BaseModel):
    title: str = Field(min_length=4, max_length=180)
    target_url: HttpUrl
    in_scope: str = Field(min_length=5, max_length=20000)
    out_of_scope: str = Field(min_length=5, max_length=20000)
    rules: str = Field(min_length=10, max_length=20000)
    bounty_type: Literal['points', 'cash']
    reward_low: int = Field(ge=0, le=1000000)
    reward_medium: int = Field(ge=0, le=1000000)
    reward_high: int = Field(ge=0, le=1000000)
    reward_critical: int = Field(ge=0, le=1000000)

    @model_validator(mode='after')
    def ordered_rewards(self):
        if not self.reward_low <= self.reward_medium <= self.reward_high <= self.reward_critical:
            raise ValueError('Rewards must increase or stay equal with severity.')
        return self

class Approval(BaseModel):
    approved: bool
    note: str = Field(default='', max_length=2000)

class StatusUpdate(BaseModel):
    severity: Literal['Low', 'Medium', 'High', 'Critical'] | None = None
    status: Literal['New', 'Triaged', 'Resolved', 'Duplicate', 'Informative', 'Not Applicable']
    note: str = Field(default='', max_length=5000)

class Note(BaseModel):
    note: str = Field(min_length=10, max_length=5000)

class ActiveUpdate(BaseModel):
    is_active: bool

class AccountUpdate(BaseModel):
    current_password: str = Field(min_length=1, max_length=200)
    username: str | None = Field(default=None, min_length=3, max_length=40, pattern=r'^[a-zA-Z0-9_-]+$')
    new_password: str | None = Field(default=None, min_length=8, max_length=72)

    @field_validator('new_password')
    @classmethod
    def password_bytes(cls, value):
        if value is not None and len(value.encode()) > 72:
            raise ValueError('Şifrə 72 UTF-8 baytından uzun olmamalıdır.')
        return value

    @model_validator(mode='after')
    def has_change(self):
        if self.username is None and self.new_password is None:
            raise ValueError('Yeni istifadəçi adı və ya şifrə daxil edin.')
        return self

class ResetPassword(BaseModel):
    token: str = Field(min_length=20, max_length=200)
    new_password: str = Field(min_length=12, max_length=72)

    @field_validator('new_password')
    @classmethod
    def password_bytes(cls, value):
        if len(value.encode()) > 72:
            raise ValueError('Şifrə 72 baytdan uzun olmamalıdır.')
        return value


class ProfileUpdate(BaseModel):
    model_config = {'extra': 'forbid'}
    bio: str = Field(default='', max_length=2000)
    github: str = Field(default='', max_length=500)
    tryhackme: str = Field(default='', max_length=500)
    hackthebox: str = Field(default='', max_length=500)

    @field_validator('github', 'tryhackme', 'hackthebox')
    @classmethod
    def profile_url(cls, value):
        value = value.strip()
        return str(HttpUrl(value)) if value else ''
