from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.group import Group

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'title',
        'institution_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            'group',
            0,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_group(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    institution_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['group']['create'],
        json={"title": title, "institution_id": institution_id},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance_id = response.json().get('id')
    instance = await db_session.get(Group, instance_id)

    assert instance.title == title
