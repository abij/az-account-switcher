from typing import List
import click
from az.cli import az
from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-n", required=False, type=int, help="Switch to this subscription number directly.")
@click.option("-v", is_flag=True, help="Verbose: echo the azure-cli commands.")
def main(n: int = None, v: bool = False) -> None:
    """
    Show all Azure Subscriptions in current profile using the `az` command-line utility.
    Ask user input for switching to another subscription.
    """
    try:
        # Using --query to map subset of fields and sort by name (ascending)
        list_cmd = 'account list --all --output json ' \
                   '--query "sort_by([].{name:name, isDefault:isDefault, id:id, state:state}, &name)"'
        if v:
            click.echo(f'Issuing AZ CLI command: {list_cmd}')

        exit_code, subscriptions, logs = az(list_cmd)
        if exit_code != 0:
            raise ValueError(logs)

        current_nr = _print_options(subscriptions)

        if not n:
            n = click.prompt('Switch', type=int, default=current_nr)

        if n not in range(1, len(subscriptions) + 1):
            raise ValueError("Value not in range! Not changing subscription.")

        if n == current_nr:
            click.echo("Selection is same as current. Not changing subscription.")
        else:
            _select_subscription(n, v, subscriptions)

        for item in _get_subscriptions_list():
            subscription_id = item.subscription_id
            active = next(filter(lambda x: x['id'] == subscription_id, subscriptions))
            click.echo("Active: " + click.style(active['id'] + ": " + active['name'], fg='green', bold=True))

        if active['state'].lower() == 'disabled':
            click.echo(click.style("Subscription state is Disabled, requires: az login!", fg='yellow'))

    except click.exceptions.Abort:
        # No need to raise exception when CTRL-C out of the cli
        pass
    except ValueError as e:
        print(e)


def _select_subscription(n, v, subscriptions):
    subscription_id = subscriptions[n - 1]['id']
    # replaced shell=true variant, which is more vulnerable: https://stackoverflow.com/a/29023432
    switch_cmd = f'account set -s {subscription_id}'
    if v:
        click.echo(f'Issuing AZ CLI command: "{switch_cmd}"')

    exit_code, _, logs = az(switch_cmd)
    if exit_code != 0:
        raise ValueError(logs)


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

def _get_subscriptions_list():
    credential = AzureCliCredential()
    subscription_client = SubscriptionClient(credential)
    page_result = subscription_client.subscriptions.list()
    result = [item for item in page_result]
    return result


if __name__ == '__main__':
    main()
