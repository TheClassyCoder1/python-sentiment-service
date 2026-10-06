import base64
import json
import logging
import os
import urllib.request

from config import LEXICON_CONTROLLER_URI, LEXICON_CONTROLLER_USER, LEXICON_CONTROLLER_PASSWORD

logger = logging.getLogger(__name__)


class LexiconSourceError(Exception):
    pass


class LexiconControllerClient:
    def __init__(self, controller_uri: str, username: str, password: str):
        self.controller_uri = controller_uri.rstrip("/")
        self.username = username
        self.password = password

    def _authorization(self) -> str:
        raw = f"{self.username}:{self.password}".encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    def get_metadata_from_controller(self, path):
        url = self.controller_uri + path
        request = urllib.request.Request(url, headers={"Accept": "application/json", "Authorization": self._authorization()})
        with urllib.request.urlopen(request) as r:
            body = r.read()
        try:
            result = json.loads(body)
            logger.debug("get_metadata_from_controller from path %s", path)
        except ValueError as e:
            raise LexiconSourceError(
                f"Got invalid json response from {self.controller_uri}:{path}"
            ) from e
        return result

    def get_schemas(self) -> list:
        return self.get_metadata_from_controller("/schemas")

    def get_files_from_container(self, container: str, names: list[str]) -> dict:
        listing = self.get_metadata_from_controller(f"/containers/{container}/files")
        return {name: content for name, content in listing.items() if not names or name in names}


def get_controller_client() -> LexiconControllerClient | None:
    if not LEXICON_CONTROLLER_URI:
        return None
    return LexiconControllerClient(LEXICON_CONTROLLER_URI, LEXICON_CONTROLLER_USER, LEXICON_CONTROLLER_PASSWORD)


def get_files_from_container(files_container, files=None):

    if files is None:
        files = {}
    else:
        files = files.copy()

    controller = get_controller_client()

    if not controller:
        raise LexiconSourceError("Lexicon controller is not configured")

    new_files = controller.get_files_from_container(files_container,
                                                    list(files.keys()))
    new_files.update(files)
    return new_files


def parse_lexicon_dict(data: dict | None) -> dict:
    if not data:
        return {"positive": [], "negative": []}
    return {
        "positive": [str(word).lower() for word in data.get("positive", [])],
        "negative": [str(word).lower() for word in data.get("negative", [])],
    }


def load_lexicon_file(path: str) -> dict:
    """
    Build a lexicon from a local file.

    :param path: Path to the file
    :return: a dict with positive and negative word lists
    """
    if os.path.exists(path):
        with open(path) as stream:
            lexicon = json.load(stream)
    else:
        lexicon = None
        logger.warning("Lexicon file %s does not exist", path)

    return parse_lexicon_dict(lexicon)
