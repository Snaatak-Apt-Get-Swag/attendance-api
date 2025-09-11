# client/tests/test_postgres_conn.py
import pytest
from unittest.mock import patch, MagicMock

# ---------------- Patch psycopg2 and Redis BEFORE importing modules ----------------
patcher_db = patch("psycopg2.connect", return_value=MagicMock())
patcher_db.start()

patcher_redis = patch("redis.Redis", return_value=MagicMock())
patcher_redis.start()
patcher_strict_redis = patch("redis.StrictRedis", return_value=MagicMock())
patcher_strict_redis.start()

# Now import the modules safely (no real connections)
from client.postgres import DatabaseSDKFacade
from client.redis import MiddlewareSDKFacade
from models.user_info import EmployeeInfo
from models.message import CustomMessage, HealthMessage

# ---------------- Fixture to mock DB client methods ----------------
@pytest.fixture(autouse=True)
def mock_db_methods():
    mock_db_client = MagicMock()
    mock_db_client.read_employee_attendance.return_value = EmployeeInfo(
        id="1", name="John Doe", status="Present", date="2023-01-01"
    )
    mock_db_client.read_all_employee_attendance.return_value = [
        EmployeeInfo(id="1", name="John Doe", status="Present", date="2023-01-01"),
        EmployeeInfo(id="2", name="Jane Smith", status="Absent", date="2023-01-02"),
    ]
    mock_db_client.create_employee_attendance.return_value = CustomMessage(
        message="Successfully created the record for the employee id: 1"
    )
    mock_db_client.attendance_health.return_value = (
        CustomMessage(message="Attendance API is running fine and ready to serve requests"),
        200
    )

    # Patch the database attribute in DatabaseSDKFacade
    with patch.object(DatabaseSDKFacade, "database", mock_db_client):
        # Patch Redis status if needed
        with patch.object(MiddlewareSDKFacade.cache, "redis_status", return_value="up"):
            yield

# ---------------- Tests ----------------
def test_read_employee_attendance():
    db_client = DatabaseSDKFacade.database
    result = db_client.read_employee_attendance(employee_id="1")
    expected = EmployeeInfo(id="1", name="John Doe", status="Present", date="2023-01-01")
    assert result == expected

def test_read_all_employee_attendance():
    db_client = DatabaseSDKFacade.database
    result = db_client.read_all_employee_attendance()
    expected = [
        EmployeeInfo(id="1", name="John Doe", status="Present", date="2023-01-01"),
        EmployeeInfo(id="2", name="Jane Smith", status="Absent", date="2023-01-02"),
    ]
    assert result == expected

def test_create_employee_attendance():
    db_client = DatabaseSDKFacade.database
    result = db_client.create_employee_attendance(employee_id="1", status="Present")
    expected = CustomMessage(message="Successfully created the record for the employee id: 1")
    assert result.message == expected.message

def test_attendance_health():
    db_client = DatabaseSDKFacade.database
    result, status_code = db_client.attendance_health()
    assert result.message == "Attendance API is running fine and ready to serve requests"
    assert status_code == 200
