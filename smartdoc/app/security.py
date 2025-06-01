from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
from jose import jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if token_type == "refresh" and payload.get("type") != "refresh":
            return None
        return payload.get("sub")
    except jwt.JWTError:
        return None
    
import smtplib
from email.mime.text import MIMEText

async def send_reset_email(email: str, reset_token: str):
    msg = MIMEText(f"Reset your password: http://localhost:8000/reset?token={reset_token}")
    msg["Subject"] = "Password Reset"
    msg["From"] = settings.EMAIL_USERNAME
    msg["To"] = email
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(msg)

# from twilio.rest import Client

# async def send_otp(phone: str):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     otp = secrets.token_digits(6)
#     client.messages.create(
#         body=f"Your OTP is {otp}",
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone
#     )
#     redis_client.setex(f"otp:{phone}", 300, otp)
#     return {"message": "OTP sent"}