"""Functions related to the Cloud Meta Data API."""
import os
from uuid import UUID

import requests

from piscada_cloud.mappings import Tag


def _check_credentials(host: str | None = None, token: str | None = None) -> tuple[str, str]:
    if isinstance(host, str) and isinstance(token, str):
        return host, token
    if (host is None and token is not None) or (host is not None and token is None):
        raise RuntimeError("Both `host` and `token` must be provided when used as parameters.")
    host = os.getenv("CLOUD_META_DATA_HOST")
    token = os.getenv("CLOUD_META_DATA_TOKEN")
    if not host or not token:
        raise RuntimeError(
            "Both environment variables CLOUD_META_DATA_HOST and CLOUD_META_DATA_TOKEN need to be defined when host and token are not provided as parameters."
        )
    return host, token


def get_controllers(host: str | None = None, token: str | None = None) -> list[dict]:
    """Get list of accessible controllers.

    Returns
    -------
    list[dict]
        List of accessible controllers.

    Parameters
    ----------
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['CLOUD_META_DATA_HOST'].
    token: str, optional
        Access token accosiated with the host. Overrides the default, which is os.environ['CLOUD_META_DATA_TOKEN'].

    Raises
    ------
    RuntimeError
        If credentials are not provided or response status from Cloud Meta Data API is not 200.
    """
    host, token = _check_credentials(host, token)
    response = requests.request("GET", f"https://{host}/v0/controllers", headers={"Authorization": f"Bearer {token}"}, timeout=(5, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return response.json()


def get_tags(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None, name: str | None = None, path: str | None = None, uuid: UUID | None = None, host: str | None = None, token: str | None = None
) -> list[Tag]:
    """List accessible tags with filtering.

    Paraneters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    name: str | None
        Tag name
    path: str | None
        Tag path
    uuid: UUID | None
        Tag UUID
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['CLOUD_META_DATA_HOST'].
    token: str, optional
        Access token accosiated with the host. Overrides the default, which is os.environ['CLOUD_META_DATA_TOKEN'].

    Returns
    -------
    list[Tag]
        Tags matching provided filter

    Raises
    ------
    RuntimeError
        if Cloud Meta Data API does not respond with status 200
    """
    host, token = _check_credentials(host, token)
    if not (controller_uuid is None or isinstance(controller_uuid, UUID)):
        raise ValueError("controller_uuid must be of type UUID")
    if not (uuid is None or isinstance(uuid, UUID)):
        raise ValueError("uuid must be of type UUID")
    query_params = [f"{key}={value}" for key, value in {"controller-uuid": controller_uuid, "name": name, "path": path, "uuid": uuid}.items() if value is not None]
    url = f"https://{host}/v0/tags"
    if len(query_params) > 0:
        url += "?" + "&".join(query_params)
    response = requests.request("GET", url, headers={"Authorization": f"Bearer {token}"}, timeout=(5, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return [Tag(controller_id=meta_data["controller-uuid"], uuid=meta_data["uuid"], name=meta_data["name"], path=meta_data["path"]) for meta_data in response.json()]
