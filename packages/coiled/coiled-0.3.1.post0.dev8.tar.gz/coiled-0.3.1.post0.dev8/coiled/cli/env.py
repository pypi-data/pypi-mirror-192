import click
from dask import config
from rich.console import Console
from rich.table import Table

from coiled._beta.core import setup_logging

from ..core import Cloud, create_software_environment, delete_software_environment
from ..utils import COILED_SERVER
from .utils import CONTEXT_SETTINGS, ENVIRON

console = Console()


@click.group(context_settings=CONTEXT_SETTINGS)
def env():
    """Commands for managing Coiled software environments"""
    setup_logging()


@env.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-n", "--name", help="Name of software environment, it must be lowercase."
)
@click.option("--container", default=None, help="Base docker image to use.")
@click.option(
    "--conda",
    default=None,
    help="Conda environment file.",
    type=click.Path(exists=True),
)
@click.option(
    "--pip", default=None, help="Pip requirements file.", type=click.Path(exists=True)
)
@click.option(
    "--post-build",
    default=None,
    help="Post-build script.",
    type=click.Path(exists=True),
)
@click.option(
    "--conda-env-name",
    default=None,
    help=(
        "Name of conda environment to install packages into. "
        "Only use when using `--container`, and the image expects commands to run in "
        'a conda environment not named "coiled"'
    ),
)
@click.option(
    "--private/--no-private",
    default=True,
    help="Flag to set software environment private.",
    is_flag=True,
)
@click.option(
    "--force-rebuild",
    default=False,
    help="Skip checks for an existing software environment build.",
    is_flag=True,
)
@click.option(
    "-e",
    "--environ",
    default=None,
    type=ENVIRON,
    multiple=True,
    help="Custom environment variable(s).",
)
@click.option(
    "--account",
    default=None,
    type=str,
    help="Account to use for creating this software environment.",
)
@click.option(
    "--new-build-backend/--no-new-build-backend",
    is_flag=True,
    show_default=True,
    default=True,
    help="Use the new build system",
)
def create(
    name,
    container,
    conda,
    pip,
    post_build,
    conda_env_name,
    private,
    force_rebuild,
    environ,
    account,
    new_build_backend,
):
    """Create a Coiled software environment"""
    create_software_environment(
        name=name,
        container=container,
        conda=conda,
        pip=pip,
        post_build=post_build,
        conda_env_name=conda_env_name,
        private=private,
        force_rebuild=force_rebuild,
        environ=dict(environ),
        account=account,
        new_build_backend=new_build_backend,
    )


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
@click.option("--new-build-backend/--no-new-build-backend", is_flag=True, default=True)
def delete(name: str, new_build_backend: bool):
    """Delete a Coiled software environment"""
    delete_software_environment(name, new_build_backend=new_build_backend)


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument("account", default=None, required=False)
@click.option("--new-build-backend/--no-new-build-backend", is_flag=True, default=True)
def list(account: str, new_build_backend: bool):
    """List the Coiled software environments in an account"""
    with Cloud(account=account) as cloud:
        environments = cloud.list_software_environments(
            account, new_build_backend=new_build_backend
        )
        account = cloud.default_account
    if not new_build_backend:
        console.print(environments)
    else:
        table = Table(title="Software Environments")
        table.add_column("Name", style="cyan")
        table.add_column("Updated", style="magenta")
        table.add_column("Link", style="magenta")
        table.add_column("Status", style="green")
        server = config.get("coiled.server", COILED_SERVER).replace("8000", "5173")
        account = account or config.get("coiled.account")
        for env_name, env_details in environments.items():
            latest_build = env_details["latest_spec"].get("latest_build")
            if latest_build:
                build_status = (
                    latest_build["state"]
                    if latest_build["state"] != "error"
                    else "[red]error[/red]"
                )
            else:
                build_status = "n/a"
            table.add_row(
                env_name,
                env_details["updated"],
                f"{server}/software/{env_details['id']}/latest?account={account}",
                build_status,
            )
        console.print(table)


@env.command(
    context_settings=CONTEXT_SETTINGS,
    help="View the details of a Coiled software environment",
)
@click.argument("name")
def inspect(name: str):
    """View the details of a Coiled software environment

    Parameters
    ----------
    name
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.

    Examples
    --------
    >>> import coiled
    >>> coiled.inspect("coiled/default")

    """
    with Cloud() as cloud:
        results = cloud.get_software_info(name)
        console.print(results)
