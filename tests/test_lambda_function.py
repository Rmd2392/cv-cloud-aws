import json
import os
from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError

import backend.lambda_function as lf


def test_lambda_handler_ok_returns_count():
    os.environ["TABLE_NAME"] = "cv-visits"

    fake_table = MagicMock()
    fake_table.update_item.return_value = {"Attributes": {"count": 5}}

    with patch.object(lf.boto3, "resource") as mock_resource:
        mock_resource.return_value.Table.return_value = fake_table
        resp = lf.lambda_handler({}, None)

    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["count"] == 5


def test_lambda_handler_clienterror_returns_500():
    os.environ["TABLE_NAME"] = "cv-visits"

    fake_table = MagicMock()
    fake_table.update_item.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "fail"}},
        "UpdateItem",
    )

    with patch.object(lf.boto3, "resource") as mock_resource:
        mock_resource.return_value.Table.return_value = fake_table
        resp = lf.lambda_handler({}, None)

    assert resp["statusCode"] == 500
    body = json.loads(resp["body"])
    assert "error" in body
