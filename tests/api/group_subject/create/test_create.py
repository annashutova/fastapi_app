from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.group_subject import GroupSubject

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'group_id',
        'subject_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            0,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.teacher.json',
                FIXTURES_PATH / 'sirius.subject.json',
                FIXTURES_PATH / 'sirius.group.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_group_subject(
    client: AsyncClient,
    username: str,
    password: str,
    group_id: int,
    subject_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['group_subject']['create'],
        json={"group_id": group_id, "subject_id": subject_id},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance_id = response.json().get('id')
    instance = await db_session.get(GroupSubject, instance_id)

    assert instance is not None
