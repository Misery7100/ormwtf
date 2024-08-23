from typing import Optional

from pydantic import BaseModel

# ----------------------- #


class FirebaseUserInfo(BaseModel):
    kind: str
    localId: str
    email: str
    displayName: Optional[str] = None
    idToken: str
    registered: Optional[bool] = None
    refreshToken: str
    expiresIn: str
    expiresAt: Optional[int] = None


# ....................... #


class FirebaseAccessCredentials(BaseModel):
    sub: str
    email: str
    name: str
    email_verified: bool
    exp: int
    iat: int
    auth_time: int
    uid: str


# ....................... #


class FirebaseRefreshCredentials(BaseModel):
    localId: str
    idToken: str
    refreshToken: str
    expiresIn: str
    expiresAt: int
