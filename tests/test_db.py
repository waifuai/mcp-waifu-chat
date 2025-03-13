import pytest

from mcp_waifu_api.db import (
    add_user_to_db,
    create_tables,
    delete_user_from_db,
    get_all_users,
    get_all_users_paged,
    get_old_dialog,
    get_user_count,
    get_user_dialog,
    get_user_last_modified_datetime,
    get_user_last_modified_timestamp,
    is_user_id_in_db,
    reset_user_chat,
    update_user_dialog,
)
from mcp_waifu_api.config import Config


@pytest.fixture
def test_config(database):
    # Use the database fixture to get the configuration
    return database


def test_create_tables(test_config: Config):
    # This test is now redundant as tables are created in the fixture.
    # We keep it to verify that create_tables doesn't raise exceptions.
    create_tables(test_config)  # Already called in the fixture, but test idempotency


def test_add_user(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    assert is_user_id_in_db("test_current_user", "test_user", test_config) is True


def test_get_old_dialog(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    update_user_dialog(
        "test_current_user", "test_user", "Test dialog", test_config
    )  # add some data
    dialog = get_old_dialog("test_current_user", "test_user", test_config)
    assert dialog == "Test dialog"
    dialog = get_old_dialog("test_current_user", "nonexistent_user", test_config)
    assert dialog == ""


def test_update_user_dialog(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)  # make sure it exists
    update_user_dialog(
        "test_current_user", "test_user", "Updated dialog", test_config
    )
    dialog = get_old_dialog("test_current_user", "test_user", test_config)
    assert dialog == "Updated dialog"


def test_reset_user_chat(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)  # make sure it exists
    update_user_dialog(
        "test_current_user", "test_user", "Initial dialog", test_config
    )
    reset_user_chat("test_current_user", "test_user", test_config)
    dialog = get_old_dialog("test_current_user", "test_user", test_config)
    assert dialog == ""


def test_is_user_id_in_db(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    assert is_user_id_in_db("test_current_user", "test_user", test_config) is True
    assert (
        is_user_id_in_db("test_current_user", "nonexistent_user", test_config) is False
    )


def test_delete_user_from_db(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    delete_user_from_db("test_current_user", "test_user", test_config)
    assert is_user_id_in_db("test_current_user", "test_user", test_config) is False


def test_get_user_count(test_config: Config):
    add_user_to_db("test_current_user", "test_user1", test_config)
    add_user_to_db("test_current_user", "test_user2", test_config)
    count = get_user_count("test_current_user", test_config)
    assert count == 2
    count = get_user_count("nonexistent_current_user", test_config)
    assert count == 0


def test_get_all_users(test_config: Config):
    add_user_to_db("test_current_user", "test_user1", test_config)
    add_user_to_db("test_current_user", "test_user2", test_config)
    users = get_all_users("test_current_user", test_config)
    assert len(users) == 2
    assert "test_user1" in users
    assert "test_user2" in users


def test_get_all_users_paged(test_config: Config):
    for i in range(150):
        add_user_to_db("test_current_user", f"test_user{i}", test_config)
    users_page_0 = get_all_users_paged("test_current_user", 0, test_config)
    assert len(users_page_0) == 100
    users_page_1 = get_all_users_paged("test_current_user", 1, test_config)
    assert len(users_page_1) == 50


def test_get_user_dialog(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    update_user_dialog(
        "test_current_user", "test_user", "Test dialog", test_config
    )  # add some data
    dialog = get_user_dialog("test_current_user", "test_user", test_config)
    assert dialog == "Test dialog"


def test_get_user_last_modified_datetime(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    datetime = get_user_last_modified_datetime(
        "test_current_user", "test_user", test_config
    )
    assert isinstance(datetime, str)
    assert (
        get_user_last_modified_datetime(
            "test_current_user", "nonexistent_user", test_config
        )
        == ""
    )


def test_get_user_last_modified_timestamp(test_config: Config):
    add_user_to_db("test_current_user", "test_user", test_config)
    timestamp = get_user_last_modified_timestamp(
        "test_current_user", "test_user", test_config
    )
    assert isinstance(timestamp, int)
    assert (
        get_user_last_modified_timestamp(
            "test_current_user", "nonexistent_user", test_config
        )
        == 0
    )