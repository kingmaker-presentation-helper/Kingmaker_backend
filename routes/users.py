from fastapi import APIRouter, Depends, HTTPException, status
from auth.jwt import create_access_token
from database.connetion import get_session
from models.users import Signup, TokenResponse, User


user_router = APIRouter(
	tags=["User"],
)

@user_router.post("/login", response_model=TokenResponse)
async def login(body: Signup, session=Depends(get_session)) -> dict:
	existing_user = session.get(User , body.email)
	try:
		if existing_user:
			access_token = create_access_token(body.email, body.exp)
		else:
			_user = User(email=body.email, username=body.username)
			session.add(_user)
			session.commit()
			session.refresh(_user)
			access_token = create_access_token(body.email, body.exp)
		return {
				"access_token": access_token,
				"token_type": "Bearer"
			}
	except:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Bad Parameter",
		)
