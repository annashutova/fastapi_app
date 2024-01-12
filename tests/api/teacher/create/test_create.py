from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.teacher import Teacher

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'first_name',
        'last_name',
        'surname',
        'user_id',
        'institution_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            'name',
            'last name',
            'surname',
            0,
            0,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.institution.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_teacher(
    client: AsyncClient,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    surname: str,
    user_id: int,
    institution_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['teacher']['create'],
        json={
            "first_name": first_name,
            "last_name": last_name,
            "surname": surname,
            "user_id": user_id,
            "institution_id": institution_id,
        },
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance_id = response.json().get('id')
    instance = await db_session.get(Teacher, instance_id)

    assert instance.first_name == first_name
    assert instance.last_name == last_name
    assert instance.surname == surname
