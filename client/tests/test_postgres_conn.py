import pytest
from client.postgres import DatabaseSDKFacade
from models.user_info import EmployeeInfo
from models.message import CustomMessage, HealthMessage

def test_read_employee_attendance():
    db_client = DatabaseSDKFacade.database
    result = db_client.read_employee_attendance(employee_id="1")
    
    expected = EmployeeInfo(
        id="1",
        name="John Doe",
        status="Present",
        date="2023-01-01"
    )
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
    redis_status = "up"
    result, status_code = db_client.attendance_health()
    
    assert result.message == "Attendance API is running fine and ready to serve requests"
    assert status_code == 200
