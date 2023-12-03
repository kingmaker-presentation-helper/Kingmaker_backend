from fastapi import APIRouter, Depends
from sqlmodel import select
from auth.authenticate import authenticate
from database.connetion import get_session
from models.users import Event, EventBase


event_router = APIRouter(
	tags=["Event"],
)

@event_router.get("/")
async def get_events(session=Depends(get_session), user: str=Depends(authenticate)):
	_event = session.exec(select(Event).filter(Event.user_email == user)).all()
	return _event

@event_router.post("/")
async def create_event(body: EventBase, session=Depends(get_session), user: str=Depends(authenticate)):
	new_event = Event(**body.dict(), user_email=user)
	session.add(new_event)
	session.commit()
	session.refresh(new_event)
	return {
			"message": f"The event for {user} was successfully created."
		}

@event_router.delete("/{event_id}")
async def delete_event(event_id: int, session=Depends(get_session), user: str=Depends(authenticate)):
	try:
		_event = session.exec(select(Event).filter(Event.id == event_id)).one()
		if (user == _event.user_email):
			session.delete(_event)
			session.commit()
			return {
				"message": f"The event for {_event.user_email} was successfully deleted."
			}
		return {
			"message": "Failed to delete an event. Not event owner"
		}
	except Exception as e:
		return {
			"message": f"Failed to delete an event {e}"
		}
