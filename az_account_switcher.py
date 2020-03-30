from azure.common.credentials import get_azure_cli_credentials
import click
import subprocess
import json
from typing import List


@click.command()
@click.option("-p", "--profile", required=False, type=str, help="Target this Azure CLI profile")
def main(profile: str = None) -> None:
    """
    Show all Azure Subscriptions in current profile using the `az` command-line utility.
    Ask for number to which to another subscription.
    """
    try:
        subscriptions = _get_subscription_list(profile)

        active_subscription_nr = _print_options(subscriptions)

        user_input = click.prompt('Switch to', type=int, default=active_subscription_nr)

        if user_input not in range(1, len(subscriptions) + 1):
            raise ValueError("Value not in range! Not changing subscription.")

        selected_id = subscriptions[user_input - 1]['id']
        subprocess.check_output(f'az account set -s {selected_id}', shell=True)

        _, subscription_id = get_azure_cli_credentials()
        lookup = next(filter(lambda x: x['id'] == selected_id, subscriptions))

        click.echo("Active: " + click.style(subscription_id + ": " + lookup['name'], fg='green', bold=True))

    except subprocess.CalledProcessError:
        # Issue is already printed to stderr.
        pass
    except click.exceptions.Abort:
        # No need to raise exception when CTRL-C out of the cli
        pass
    except ValueError as e:
        print(e)


def _get_subscription_list(profile: str = None) -> List[dict]:
    command = 'az account list --output json'
    if profile:
        command += " --profile " + profile
    return json.loads(subprocess.check_output(command, shell=True, universal_newlines=True))


def _print_options(subscriptions: List[dict]) -> int:
    selected = 0
    for idx, s in enumerate(subscriptions):
        number = click.style(f"[{idx + 1}]", fg='yellow')

        if s['isDefault']:
            selected = idx + 1
            colored_info = click.style(f"{s['id']}: {s['name']}", fg='green', bold=True)
        else:
            colored_info = click.style(f"{s['id']}: {s['name']}")

        click.echo(number + ": " + colored_info)
    return selected
