from lnhub_rest._check_breaks_lndb import check_breaks_lndb


def test_check_breaks_lndb():
    breaks_lndb = check_breaks_lndb(
        _email="testuser2@lamin.ai",
        _password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz",
    )
    print(breaks_lndb)
    assert isinstance(breaks_lndb, bool)
