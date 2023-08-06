from typing import Optional, Union

from packaging.version import parse as vparse

from lnhub_rest import __version__ as installed_version
from lnhub_rest._sbclient import connect_hub_with_auth


def check_breaks_lndb(
    *,
    # replace with token-based approach!
    _email: Optional[str] = None,
    _password: Optional[str] = None,
) -> Union[bool, str]:
    """Check whether lndb client breaks because it's not up-to-date."""
    hub = connect_hub_with_auth(email=_email, password=_password)
    try:
        all_versions = (
            hub.table("version_cbwk").select("*").order("v", desc=True).execute().data
        )
        # starting with the latest version, loop through earlier
        # versions to find instances in which breaks_lndb is true
        # - recent versions might have breaks_lndb == False, these are OK!
        # - the first version that hits breaks_lndb == True, triggers a comparison
        # if the installed_version is smaller than the deployed version
        # signal that lndb breaks (True), otherwise everything is OK (False)
        for row in all_versions:
            # there was a breaking change for that version
            if row["breaks_lndb"]:
                # the installed version is not up to date, strictly smaller
                if vparse(installed_version) < vparse(row["v"]):
                    return True
                # the installed version is already up to date
                else:
                    return False
        return False
    except Exception as e:
        return str(e)
    finally:
        hub.auth.sign_out()
