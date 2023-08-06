from lnhub_rest import __version__
from lnhub_rest._get_migrations import get_migrations_latest_and_installed


def test_get_version():
    migrations = get_migrations_latest_and_installed(
        installed_version=__version__,
        _email="testuser2@lamin.ai",
        _password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz",
    )
    print(migrations)
    assert not isinstance(migrations, str)
    assert len(migrations["latest"]) == len("641d1508baab")
    assert len(migrations["installed"]) == len("641d1508baab")
