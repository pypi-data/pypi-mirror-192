import dask
import yaml
from click.testing import CliRunner

import coiled
from coiled.cli import env


def test_create_list_delete(sample_user):
    # No software environments initially
    assert not coiled.list_software_environments(new_build_backend=False)

    runner = CliRunner()
    name = "my-env"
    # Coiled env create creates a software environment
    result = runner.invoke(
        env.create,
        args=f"--name {name} --no-new-build-backend --container daskdev/dask:latest",
    )
    assert result.exit_code == 0

    result = coiled.list_software_environments(new_build_backend=False)
    assert f"{sample_user.account.name}/{name}" in result
    assert (
        result[f"{sample_user.account.name}/{name}"]["container"]
        == "daskdev/dask:latest"
    )

    # Coiled env list has similar output to coiled.list_software_environments
    result = runner.invoke(env.list, args="--no-new-build-backend", color=False)
    assert result.exit_code == 0
    output = yaml.safe_load(result.output)
    assert f"{sample_user.account.name}/{name}" in output
    assert (
        output[f"{sample_user.account.name}/{name}"]["container"]
        == "daskdev/dask:latest"
    )

    # Coiled delete removes software environments
    result = runner.invoke(env.delete, args=f"--no-new-build-backend {name}")
    assert result.exit_code == 0
    assert not coiled.list_software_environments(new_build_backend=False)


def test_inspect(sample_user, second_user, remote_access_url, sample_user_token):
    # Coiled inspect outputs software spec

    # Create software environment in sample_user's account
    with dask.config.set(
        {
            "coiled": {
                "user": f"{sample_user.user.username}",
                "token": sample_user_token,
                "server": remote_access_url,
                "account": sample_user.account.name,
                "backend-options": {"region": "us-east-2"},
                "no-minimum-version-check": True,
            }
        }
    ):
        coiled.create_software_environment(
            name="my-env", container="daskdev/dask:latest", new_build_backend=False
        )
        runner = CliRunner()
        result = runner.invoke(env.inspect, args=f"{sample_user.account.name}/my-env")
        assert result.exit_code == 0
        assert "daskdev/dask:latest" in result.output


def test_env_create(mocker):
    create_software_environment = mocker.patch(
        "coiled.cli.env.create_software_environment"
    )

    runner = CliRunner()
    result = runner.invoke(
        env.create,
        args=(
            "--name my-env "
            "--container daskdev/dask:latest "
            "--account my-account "
            "--environ ENV_VAR=VALUE "
            "--force-rebuild "
            "--private "
            "--no-new-build-backend "
        ),
    )

    assert result.exit_code == 0
    create_software_environment.assert_called_with(
        name="my-env",
        new_build_backend=False,
        container="daskdev/dask:latest",
        private=True,
        force_rebuild=True,
        environ={"ENV_VAR": "VALUE"},
        account="my-account",
        # Default values that we didn't change
        conda=None,
        pip=None,
        post_build=None,
        conda_env_name=None,
    )
