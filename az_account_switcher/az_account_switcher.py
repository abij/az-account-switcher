import json
import subprocess
from typing import List

import click
from azure.common.credentials import get_azure_cli_credentials


@click.command()
@click.option("-n", required=False, type=int, help="Switch to this subscription number directly.")
def main(n: int = None) -> None:
    """
    Show all Azure Subscriptions in current profile using the `az` command-line utility.
    Ask user input for switching to another subscription.
    """
    try:
        subscriptions = json.loads(subprocess.getoutput('az account list --output json'))

        current_nr = _print_options(subscriptions)

        if not n:
            n = click.prompt('Switch', type=int, default=current_nr)

        if n not in range(1, len(subscriptions) + 1):
            raise ValueError("Value not in range! Not changing subscription.")

        _select_subscription(n, subscriptions)

        _, subscription_id = get_azure_cli_credentials()
        active = next(filter(lambda x: x['id'] == subscription_id, subscriptions))
        click.echo("Active: " + click.style(active['id'] + ": " + active['name'], fg='green', bold=True))

    except subprocess.CalledProcessError:
        # Issue is already printed to stderr.
        pass
    except click.exceptions.Abort:
        # No need to raise exception when CTRL-C out of the cli
        pass
    except ValueError as e:
        print(e)


def _select_subscription(n, subscriptions):
    subscription_id = subscriptions[n - 1]['id']
    subprocess.check_output(f'az account set -s {subscription_id}', shell=True)


def _print_options(subscriptions: List[dict]) -> int:
    selected = -1

    for idx, s in enumerate(subscriptions):
        number = click.style(f"[{idx + 1}]", fg='yellow')

        if s['isDefault']:
            selected = idx + 1
            colored_info = click.style(f"{s['id']}: {s['name']}", fg='green', bold=True)
        else:
            colored_info = click.style(f"{s['id']}: {s['name']}")

        click.echo(number + ": " + colored_info)
    return selected
