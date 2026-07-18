import pytest
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def client(db_session: Session) -> TestClient:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def user_token(client: TestClient) -> str:
    credentials = {"email": "customer@example.com", "password": "password123"}
    assert client.post("/api/auth/register", json=credentials).status_code == 201
    response = client.post("/api/auth/login", json=credentials)
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client: TestClient, db_session: Session) -> str:
    from app.models.user import User

    credentials = {"email": "admin@example.com", "password": "password123"}
    assert client.post("/api/auth/register", json=credentials).status_code == 201
    db_session.query(User).filter_by(email=credentials["email"]).update(
        {"is_admin": True}
    )
    db_session.commit()
    response = client.post("/api/auth/login", json=credentials)
    return response.json()["access_token"]


def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
