from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.journal import Journal

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'journal_id',
        'new_grade',
        'class_date',
        'student_id',
        'subject_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            4,
            '2023-12-12',
            0,
            0,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.teacher.json',
                FIXTURES_PATH / 'sirius.subject.json',
                FIXTURES_PATH / 'sirius.group.json',
                FIXTURES_PATH / 'sirius.student.json',
                FIXTURES_PATH / 'sirius.journal.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_journal(
    client: AsyncClient,
    username: str,
    password: str,
    journal_id: int,
    new_grade: int,
    class_date: str,
    student_id: int,
    subject_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.put(
        URLS['journal']['update'] + '/' + str(journal_id),
        json={"student_id": student_id, "subject_id": subject_id, "grade": new_grade, 'class_date': class_date},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance = await db_session.get(Journal, journal_id)

    assert instance.grade == new_grade
