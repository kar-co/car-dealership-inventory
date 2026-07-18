from app.core.config import settings
from app.models.vehicle import Vehicle
from app.tests.conftest import bearer
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.orm import Session

VEHICLE = {
    "make": "Ford",
    "model": "Focus",
    "category": "Sedan",
    "price": "10000.00",
    "quantity": 3,
}


def test_registration_login_and_duplicate_email(client: TestClient) -> None:
    credentials = {"email": "driver@example.com", "password": "password123"}

    registered = client.post("/api/auth/register", json=credentials)
    login = client.post("/api/auth/login", json=credentials)
    duplicate = client.post("/api/auth/register", json=credentials)

    assert registered.status_code == 201
    assert registered.json()["email"] == credentials["email"]
    assert "access_token" in login.json()
    claims = jwt.decode(
        login.json()["access_token"],
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    assert claims["is_admin"] is False
    assert duplicate.status_code == 409


def test_invalid_login_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "unknown@example.com", "password": "password123"},
    )

    assert response.status_code == 401


def test_vehicle_crud_is_admin_only(
    client: TestClient, admin_token: str, user_token: str
) -> None:
    forbidden = client.post("/api/vehicles", json=VEHICLE, headers=bearer(user_token))
    created = client.post("/api/vehicles", json=VEHICLE, headers=bearer(admin_token))
    vehicle_id = created.json()["id"]
    updated_payload = {**VEHICLE, "price": "11000.00", "quantity": 5}
    updated = client.put(
        f"/api/vehicles/{vehicle_id}",
        json=updated_payload,
        headers=bearer(admin_token),
    )
    deleted = client.delete(f"/api/vehicles/{vehicle_id}", headers=bearer(admin_token))

    assert forbidden.status_code == 403
    assert created.status_code == 201
    assert updated.status_code == 200
    assert updated.json()["price"] == "11000.00"
    assert deleted.status_code == 204
    assert client.get("/api/vehicles", headers=bearer(user_token)).json() == []


def test_vehicle_reads_require_authentication(client: TestClient) -> None:
    assert client.get("/api/vehicles").status_code == 403
    assert client.get("/api/vehicles/search?query=ford").status_code == 403


def test_search_filters_vehicles(
    client: TestClient, db_session: Session, user_token: str
) -> None:
    db_session.add_all(
        [
            Vehicle(**VEHICLE),
            Vehicle(
                make="Toyota",
                model="Corolla",
                category="Hatchback",
                price="15000.00",
                quantity=2,
            ),
        ]
    )
    db_session.commit()

    response = client.get("/api/vehicles/search?query=toy", headers=bearer(user_token))

    assert response.status_code == 200
    assert [vehicle["model"] for vehicle in response.json()] == ["Corolla"]


def test_search_filters_by_price_range(
    client: TestClient, db_session: Session, user_token: str
) -> None:
    db_session.add_all(
        [
            Vehicle(**VEHICLE),
            Vehicle(
                make="Toyota",
                model="Corolla",
                category="Hatchback",
                price="15000.00",
                quantity=2,
            ),
            Vehicle(
                make="BMW",
                model="X5",
                category="SUV",
                price="45000.00",
                quantity=1,
            ),
        ]
    )
    db_session.commit()

    response = client.get(
        "/api/vehicles/search?min_price=12000&max_price=20000",
        headers=bearer(user_token),
    )

    assert response.status_code == 200
    assert [vehicle["model"] for vehicle in response.json()] == ["Corolla"]


def test_login_token_marks_admin_users(client: TestClient, admin_token: str) -> None:
    claims = jwt.decode(
        admin_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    assert claims["is_admin"] is True


def test_purchase_updates_stock_and_prevents_overselling(
    client: TestClient, db_session: Session, user_token: str
) -> None:
    vehicle = Vehicle(**VEHICLE)
    db_session.add(vehicle)
    db_session.commit()

    purchased = client.post(
        f"/api/vehicles/{vehicle.id}/purchase",
        json={"quantity": 2},
        headers=bearer(user_token),
    )
    oversold = client.post(
        f"/api/vehicles/{vehicle.id}/purchase",
        json={"quantity": 2},
        headers=bearer(user_token),
    )

    assert purchased.status_code == 200
    assert purchased.json()["quantity"] == 1
    assert oversold.status_code == 409


def test_restock_requires_admin_and_valid_quantity(
    client: TestClient, db_session: Session, admin_token: str, user_token: str
) -> None:
    vehicle = Vehicle(**VEHICLE)
    db_session.add(vehicle)
    db_session.commit()

    forbidden = client.post(
        f"/api/vehicles/{vehicle.id}/restock",
        json={"quantity": 2},
        headers=bearer(user_token),
    )
    invalid = client.post(
        f"/api/vehicles/{vehicle.id}/restock",
        json={"quantity": 0},
        headers=bearer(admin_token),
    )
    restocked = client.post(
        f"/api/vehicles/{vehicle.id}/restock",
        json={"quantity": 2},
        headers=bearer(admin_token),
    )

    assert forbidden.status_code == 403
    assert invalid.status_code == 422
    assert restocked.status_code == 200
    assert restocked.json()["quantity"] == 5
