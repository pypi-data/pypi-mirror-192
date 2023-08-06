from typing import Mapping, Optional, Union

from lnhub_rest._sbclient import connect_hub_with_auth


def get_migrations_latest_and_installed(
    *,
    installed_version: str,
    # replace with token-based approach!
    _email: Optional[str] = None,
    _password: Optional[str] = None,
) -> Union[str, Mapping[str, str]]:
    """Return dict of latest and installed migration ids."""
    hub = connect_hub_with_auth(email=_email, password=_password)
    try:
        latest = (
            hub.table("version_cbwk")
            .select("*")
            .order("v", desc=True)
            .limit(1)
            .execute()
            .data[0]
        )
        installed = (
            hub.table("version_cbwk")
            .select("*")
            .eq("v", installed_version)
            .execute()
            .data[0]
        )
        migrations = {
            "latest": latest["migration"],
            "installed": installed["migration"],
        }
        return migrations
    except Exception as e:
        return str(e)
    finally:
        hub.auth.sign_out()
