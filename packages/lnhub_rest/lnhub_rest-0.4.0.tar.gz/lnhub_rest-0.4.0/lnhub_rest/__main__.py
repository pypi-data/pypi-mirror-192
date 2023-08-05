import argparse
from subprocess import run

import sqlmodel as sqm
from lamin_logger import logger

description_cli = "Migrate hub."
parser = argparse.ArgumentParser(
    description=description_cli, formatter_class=argparse.RawTextHelpFormatter
)
subparsers = parser.add_subparsers(dest="command")

# migrate
migr = subparsers.add_parser("migrate")
aa = migr.add_argument
aa("action", choices=["generate", "deploy"], help="Generate migration.")

# parse args
args = parser.parse_args()


def generate():
    run(
        "alembic --config lnhub_rest/schema/alembic.ini --name cbwk revision"
        " --autogenerate -m 'vX.X.X.'",
        shell=True,
    )


def deploy():
    process = run(
        "alembic --config lnhub_rest/schema/alembic.ini --name cbwk upgrade head",
        shell=True,
    )
    if process.returncode == 0:
        from lndb import settings

        from lnhub_rest._engine import engine
        from lnhub_rest.schema import __version__, migration
        from lnhub_rest.schema.versions import version_cbwk

        with sqm.Session(engine) as ss:
            ss.add(
                version_cbwk(
                    v=__version__, migration=migration, user_id=settings.user.id
                )
            )
            ss.commit()

        logger.success("Successfully migrated hub.")


def main():
    if args.command == "migrate":
        if args.action == "generate":
            generate()
        if args.action == "deploy":
            deploy()
    else:
        logger.error("Invalid command. Try `lndb -h`.")
        return 1
