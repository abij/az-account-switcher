"""
Note: pytest creates new tmpdir with copy of .azure/test-azureProfile.json per test.
"""
from az_account_switcher.az_account_switcher import main


def test_cli_print_help(cli_runner):
    result = cli_runner.invoke(main, ["-h"])
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS]" in result.output
    assert "-h, --help" in result.output


def test_cli_list(cli_runner):
    result = cli_runner.invoke(main)
    assert result.exit_code == 0
    assert (
        "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee1: Subscription-1-enabled: [Tenant 1]"
        in result.output
    )
    assert (
        "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee2: Subscription-2-disabled: [Tenant 1]"
        in result.output
    )
    assert (
        "zzzzzzzzz-bbbb-cccc-dddd-xxxxxxxxxxxxx3: Subscription-3-default: [Tenant 2]"
        in result.output
    )


def test_cli_switch_direct_3(cli_runner):
    result = cli_runner.invoke(main, ["-n", 3])
    assert result.exit_code == 0
    assert (
        "Active: zzzzzzzzz-bbbb-cccc-dddd-xxxxxxxxxxxxx3: Subscription-3-default: [Tenant 2]"
        in result.output
    )


def test_cli_switch_choose_1(cli_runner):
    result = cli_runner.invoke(main, input="1\n")
    assert result.exit_code == 0
    assert (
        "Active: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee1: Subscription-1-enabled: [Tenant 1]"
        in result.output
    )


def test_cli_switch_choose_to_disabled(cli_runner):
    result = cli_runner.invoke(main, input="2\n")
    assert result.exit_code == 0
    assert (
        "Active: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee2: Subscription-2-disabled: [Tenant 1]"
        in result.output
    )
    assert "Subscription state is Disabled, requires: az login!" in result.output


def test_cli_switch_choose_not_in_range(cli_runner):
    result = cli_runner.invoke(main, input="4\n")
    assert result.exit_code == 0
    assert "Value not in range! Not changing subscription" in result.output


def test_cli_switch_direct_3_verbose_flag1(cli_runner):
    result = cli_runner.invoke(main, ["-n", 3, "-v"])
    assert result.exit_code == 0
    assert (
        "Issuing AZ CLI command: account list --all --output json --query "
        "'sort_by([].{name:name, isDefault:isDefault, id:id, state:state, tenant:tenantDisplayName}, &name)'"
        in result.output
    )
    assert (
        'Issuing AZ CLI command: "account set -s zzzzzzzzz-bbbb-cccc-dddd-xxxxxxxxxxxxx3"'
        in result.output
    )
    assert (
        "Active: zzzzzzzzz-bbbb-cccc-dddd-xxxxxxxxxxxxx3: Subscription-3-default: [Tenant 2]"
        in result.output
    )


def test_cli_switch_direct_3_verbose_flag2(cli_runner):
    result = cli_runner.invoke(main, ["-n", 3, "--verbose"])
    assert result.exit_code == 0
    assert (
        "Issuing AZ CLI command: account list --all --output json --query "
        "'sort_by([].{name:name, isDefault:isDefault, id:id, state:state, tenant:tenantDisplayName}, &name)'"
        in result.output
    )
    assert (
        'Issuing AZ CLI command: "account set -s zzzzzzzzz-bbbb-cccc-dddd-xxxxxxxxxxxxx3"'
        in result.output
    )
    assert (
        "Active: zzzzzzzzz-bbbb-cccc-dddd-xxxxxxxxxxxxx3: Subscription-3-default: [Tenant 2]"
        in result.output
    )
