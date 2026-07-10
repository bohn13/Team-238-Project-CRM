from sqlalchemy.orm import configure_mappers

import database


def test_database_mappers_can_be_configured() -> None:
    assert database.Base is not None
    configure_mappers()
