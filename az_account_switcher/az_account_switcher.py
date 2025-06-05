from typing import List
import click
from .azure_cli import az

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-n", required=False, type=int, help="Switch to this subscription number directly."
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Verbose: echo the azure-cli commands."
)
def main(n: int = None, verbose: bool = False) -> None:
    """
    Show all Azure Subscriptions in current profile using the `az` command-line utility.
    Ask user input for switching to another subscription.
    """
    try:
        # Since Azure-CLI 2.61.0 there is build-in support for subscription selection.
        exit_code, versions, logs = az("version --output json")
        if exit_code != 0:
            raise ValueError(logs)

        if versions["azure-cli"] >= "2.61.0":
            click.echo(
                click.style(
                    "Azure CLI version is 2.61.0 or higher, it has build-in support to switch subscription. Just use 'az login' and uninstall this package.",
                    fg="yellow",
                )
            )

        # Using --query to map subset of fields and sort by name (ascending)
        list_cmd = (
            "account list --all --output json "
            "--query 'sort_by([].{name:name, isDefault:isDefault, id:id, state:state, tenant:tenantDisplayName}, &name)'"
        )
        if verbose:
            click.echo(f"Issuing AZ CLI command: {list_cmd}")

        exit_code, subscriptions, logs = az(list_cmd)
        if exit_code != 0:
            raise ValueError(logs)

        if len(subscriptions) == 0:
            click.echo(
                click.style("No subscriptions found, requires: az login!", fg="yellow")
            )
            return

        current_nr = _print_options(subscriptions)

        if not n:
            n = click.prompt("Switch", type=int, default=str(current_nr))

        if n not in range(1, len(subscriptions) + 1):
            raise ValueError("Value not in range! Not changing subscription.")

        if n == current_nr:
            click.echo("Selection is same as current. Not changing subscription.")
        else:
            _select_subscription(n, subscriptions, verbose)

        active = subscriptions[n - 1]
        click.echo(
            "Active: "
            + click.style(
                f'{active["id"]}: {active["name"]}: [{active["tenant"]}]',
                fg="green",
                bold=True,
            )
        )

        if active["state"].lower() == "disabled":
            click.echo(
                click.style(
                    "Subscription state is Disabled, requires: az login!", fg="yellow"
                )
            )
    except FileNotFoundError as e:
        if "az" not in str(e):  # only raise when 'az' is not found.
            raise e
        click.echo(click.style('Error: missing "az" on PATH.', bold=True, fg="red"))
        click.echo(
            "  Please install Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli"
        )
    except click.exceptions.Abort:
        # No need to raise exception when CTRL-C out of the cli
        pass
    except ValueError as e:
        print(e)


def _select_subscription(n: int, subscriptions: List[dict], verbose=False):
    subscription_id = subscriptions[n - 1]["id"]
    # replaced shell=true variant, which is more vulnerable: https://stackoverflow.com/a/29023432
    switch_cmd = f"account set -s {subscription_id}"

    if verbose:
        click.echo(f'Issuing AZ CLI command: "{switch_cmd}"')

    exit_code, _, logs = az(switch_cmd)
    if exit_code != 0:
        raise ValueError(logs)


def _print_options(subscriptions: List[dict]) -> int:
    selected = -1

    for idx, s in enumerate(subscriptions):
        number = click.style(f"[{idx + 1}]", fg="yellow")

        if s["isDefault"]:
            selected = idx + 1
            colored_info = click.style(
                f"{s['id']}: {s['name']}: [{s['tenant']}]", fg="green", bold=True
            )
        else:
            colored_info = click.style(f"{s['id']}: {s['name']}: [{s['tenant']}]")

        click.echo(number + ": " + colored_info)
    return selected


if __name__ == "__main__":
    main()
