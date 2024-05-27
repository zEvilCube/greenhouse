from . import get_session
from .models import Auth


# Utils

def create(model, **params):
    with get_session() as session:
        instance = model(**params)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance


def read_all(model, **params) -> list:
    with get_session() as session:
        result = session.query(model).filter_by(**params).all()
        return result


def read_first(model, **params):
    with get_session() as session:
        result = session.query(model).filter_by(**params).first()
        return result


def update(model, **params):
    with get_session() as session:
        instance = model(**params)
        session.merge(instance)
        session.commit()


# Auth

def read_auth(tg_id: int) -> Auth or None:
    return read_first(Auth, tg_id=tg_id)


def update_auth(tg_id: int, api_key: str) -> Auth or None:
    update(Auth, tg_id=tg_id, api_key=api_key)
    return read_auth(tg_id)
