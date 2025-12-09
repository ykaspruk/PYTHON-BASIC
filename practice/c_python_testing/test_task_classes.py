"""
Write tests for classes in b_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""


import pytest
import datetime
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys


current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
target_file_path = project_root / 'b_python_part_2'

if str(target_file_path) not in sys.path:
    sys.path.insert(0, str(target_file_path))

from task_classes import Teacher, Student, Homework

FIXED_NOW = datetime.datetime(2025, 12, 12, 12, 0, 0)

class MockDateTimeModule:
    @staticmethod
    def now():
        return FIXED_NOW

    datetime = MagicMock(now=staticmethod(now))
    timedelta = datetime.timedelta

@pytest.fixture
def teacher():
    return Teacher('Smith', 'Alice')


@pytest.fixture
def student():
    return Student('Jones', 'Bob')


@pytest.fixture
def mock_now():
    FULL_MODULE_PATH = 'practice.b_python_part_2.task_classes'

    with patch(f'{FULL_MODULE_PATH}.datetime', new=MockDateTimeModule) as mock_dt:
        yield mock_dt


def test_teacher_creation(teacher):
    assert teacher.last_name == 'Smith'
    assert teacher.first_name == 'Alice'


def test_teacher_create_homework_returns_homework(teacher, mock_now):
    homework = teacher.create_homework('Test task', 3)
    assert isinstance(homework, Homework)
    assert homework.text == 'Test task'
    assert homework.days_to_complete == 3


def test_teacher_create_homework_sets_dates(teacher, mock_now):
    homework = teacher.create_homework('Test task', 5)
    assert homework.created == FIXED_NOW

    expected_deadline = FIXED_NOW + datetime.timedelta(days=5)
    assert homework.deadline == expected_deadline


def test_homework_initialization_with_positive_days(mock_now):
    hw = Homework('Future task', 2)
    assert hw.created == FIXED_NOW
    assert hw.deadline == FIXED_NOW + datetime.timedelta(days=2)


def test_homework_initialization_with_zero_days(mock_now):
    hw = Homework('Immediate task', 0)
    assert hw.deadline == FIXED_NOW


def test_homework_is_active_active(mock_now):
    hw = Homework('Active task', 1)
    assert hw.is_active() is True


def test_homework_is_active_expired(mock_now):
    past_deadline = FIXED_NOW - datetime.timedelta(days=1)

    hw = MagicMock(spec=Homework)
    hw.deadline = past_deadline

    assert hw.is_active() is False


def test_homework_corner_case_negative_days(mock_now):
    hw = Homework('Expired task', -2)
    assert hw.deadline == FIXED_NOW - datetime.timedelta(days=2)
    assert hw.is_active() is False


def test_student_creation(student):
    assert student.last_name == 'Jones'
    assert student.first_name == 'Bob'


def test_student_do_homework_active(student, mock_now):
    active_homework = Homework('Active task', 2)

    result = student.do_homework(active_homework)

    assert result is active_homework


def test_student_do_homework_expired(student, mock_now, capsys):
    expired_homework = Homework('Expired task', -1)

    result = student.do_homework(expired_homework)

    assert result is None

    captured = capsys.readouterr()
    assert captured.out.strip() == 'You are late'


def test_student_do_homework_just_expired(student, mock_now, capsys):
    hw = Homework('Just expired', 0)

    expired_time = FIXED_NOW + datetime.timedelta(seconds=1)

    FULL_MODULE_PATH = 'practice.b_python_part_2.task_classes'

    with patch(f'{FULL_MODULE_PATH}.datetime.datetime.now', return_value=expired_time):
        result = student.do_homework(hw)

    assert result is None
    captured = capsys.readouterr()
    assert captured.out.strip() == 'You are late'