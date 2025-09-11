import pytest
from models.message import CustomMessage, HealthMessage
from models.user_info import EmployeeInfo
from client.redis import MiddlewareSDKFacade
from client.postgres import DatabaseSDKFacade

# -----------------------------
# Tests for Postgres
# -----------------------------

def test_read_employee_attendance():
    db = DatabaseSDKFacade.database
    # Replace with a valid employee_id from your database
    record = db.read_employee_attendance(employee_id="1")

    assert isinstance(record, EmployeeInfo)
    assert record.id == "1"
    assert record.name is not None
    assert record.status in ["Present", "Absent"]
    assert record.date is not None


def test_read_all_employee_attendance():
    db = DatabaseSDKFacade.database
    records = db.read_all_employee_attendance()

    assert isinstance(records, list)
    assert all(isinstance(r, EmployeeInfo) for r in records)
    assert len(records) > 0


def test_create_employee_attendance():
    db = DatabaseSDKFacade.database
    # Replace with valid employee data
    record = EmployeeInfo(id="999", name="Test User", status="Present", date="2025-09-11")
    response = db.create_employee_attendance(record)

    assert isinstance(response, CustomMessage)
    assert "Successfully created" in response.message


# -----------------------------
# Tests for Health / Redis
# -----------------------------

def test_attendance_detail_health():
    db = DatabaseSDKFacade.database
    redis_status = MiddlewareSDKFacade.cache.redis_status()

    result, status_code = HealthMessage(
        message="Attendance API is running fine and ready to serve requests",
        postgresql="up",
        redis=redis_status,
        status="up",
    ), 200

    assert isinstance(result, HealthMessage)
    assert result.postgresql == "up"
    assert result.redis == "up"
    assert result.status == "up"
    assert status_code == 200


def test_attendance_health():
    db = DatabaseSDKFacade.database
    result, status_code = db.attendance_health()

    assert isinstance(result, CustomMessage)
    assert "Attendance API is running fine" in result.message
    assert status_code == 200
