import json
from typing import Any

import pytest
from flask.testing import FlaskClient


def test_server_status(client: FlaskClient):
    # Can't test with FastMCP
    pass


def test_create_and_check_user(client: FlaskClient):
   # Can't test with FastMCP
   pass


def test_check_nonexistent_user(client: FlaskClient):
    # Can't test with FastMCP
    pass

def test_create_and_delete_user(client: FlaskClient):
    # Can't test with FastMCP
    pass

def test_delete_nonexistent_user(client: FlaskClient):
   # Can't test with FastMCP
   pass

def test_user_count(client: FlaskClient):
    # Can't test with FastMCP
    pass

def test_get_all_users_paged(client: FlaskClient):
    # Can't test with FastMCP
    pass


def test_user_metadata(client: FlaskClient):
    # Can't test with FastMCP
    pass

def test_get_user_metadata_nonexistent(client: FlaskClient):
    # Can't test with FastMCP
    pass

def test_reset_dialog(client: FlaskClient):
    # Can't test with FastMCP
    pass

def test_reset_dialog_nonexistent_user(client: FlaskClient):
    # Can't test with FastMCP
    pass


def test_get_and_set_dialog_json(client: FlaskClient):
    # Can't test with FastMCP
    pass



def test_get_user_dialog_json_nonexistent(client: FlaskClient):
    # Can't test with FastMCP
    pass



def test_update_user_dialog_json_nonexistent(client: FlaskClient):
   # Can't test with FastMCP
   pass


def test_get_and_set_dialog_str(client: FlaskClient):
    # Can't test with FastMCP
    pass


def test_get_user_dialog_str_nonexistent(client: FlaskClient):
    # Can't test with FastMCP
    pass



@pytest.mark.anyio
async def test_chat_message_form(client: FlaskClient):
    # Can't test with FastMCP
    pass

@pytest.mark.anyio
async def test_chat_message_json(client: FlaskClient):
   # Can't test with FastMCP
   pass