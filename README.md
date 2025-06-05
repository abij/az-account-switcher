## Switch Azure subscriptions

> [!WARNING]
> The new version of the Azure-CLI, since 2.61.0, has build-in support for switching subscriptions, so this package is no longer needed. You can use the command `az login` to switch subscriptions directly. See: https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli-interactively?view=azure-cli-latest#subscription-selector.

[![License](https://img.shields.io/pypi/l/az-account-switcher.svg)](

| Type| Badge|
|---|---|
| Workflow | [![Test](https://github.com/abij/az-account-switcher/actions/workflows/test.yml/badge.svg)](https://github.com/abij/az-account-switcher/actions/workflows/test.yml) ![!Workflow upload](https://github.com/abij/az-account-switcher/workflows/Upload%20Python%20Package/badge.svg)|
|Latest|![!PyPI](https://img.shields.io/pypi/v/az-account-switcher.svg)|
|Activity|![!PyPI](https://img.shields.io/pypi/dm/az-account-switcher)|
| DeepSource | [![DeepSource](https://deepsource.io/gh/abij/az-account-switcher.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/abij/az-account-switcher/?ref=repository-badge) |

Problem: Switching subscriptions using the [Azure CLI](https://docs.microsoft.com/cli/azure/manage-azure-subscriptions-azure-cli) involves too much typing.

```bash
# Type a lot...
az account list --output table

# Use mouse to select the subscription-id in the console
# Use ctrl-c to copy the text, this might be optional

# Type a lot...
az account set --subscription-id <paste subscription-id>
```

Solution: I simplified this task with the command-line utility **az-switch**! The active subscription is bold and green and selected as default argument. Just select the subscription you want to activate.

### Install

`pip install az-account-switcher`

### Usage

```bash
Usage: az-switch [OPTIONS]

  Show all Azure Subscriptions in current profile using the `az` command-
  line utility. Ask user input for switching to another subscription.

Options:
  -n INTEGER     Switch to this subscription number directly.
  -v, --verbose  Verbose: echo the azure-cli commands.
  -h, --help     Show this message and exit.
```

### Example

![example_gif](https://raw.githubusercontent.com/abij/az-account-switcher/master/az-switch-example.gif)

## CHANGELOG

### v1.5.0 (05-05-2025):

- Display tenant name in the subscription list.
- Show warning when AzureCLI 2.61.0 or newer is detected, no need for this package anymore.
- Drop support for Python 3.8 and 3.9 since Click 8.2.0 requires Python 3.10+.

### v1.4.0 (28-12-2023):

- Removed `az.cli` with `azure-cli` dependencies in favor subprocess call to have a small installation. Assuming `az` in on your PATH.
- Drop Python 3.7 support, due to minimal version supported by (dev) dependency `commitizen`.
- Switch to [poetry](https://python-poetry.org/) for dependency management.

### v1.3.0 (25-02-2022):

- Fixed: [issue-8](https://github.com/abij/az-account-switcher/issues/8) **NotImplementedError** by removing deprecated `get_azure_cli_credentials` in [PR-6](https://github.com/abij/az-account-switcher/pull/6).
- **Speed-up switching** by removing the online interaction pulling the Subscriptions through the Azure-CLI. [PR-7](https://github.com/abij/az-account-switcher/pull/7)
- Add `--verbose` flag as an alias to the `-v` flag.

### v1.2.0 (31-05-2021):

- Support Windows by changing interaction with Azure-CLI using Python package 'az.cli' instead of POpen
- Drop Python 3.6 support, due to dependent package 'az.cli'
- Unit tests running on latest versions of Unix, Windows and MacOs
- Depend on `azure-cli` instead of `azure-cli-core` to auto include `packaging`to fix [issue-3](https://github.com/abij/az-account-switcher/issues/3)

### v1.1.0 (04-05-2021):

- Don't switch when same subscription is selected.
- Add `-v` verbose flag to print Azure-CLI sub-commands.
- Add `-h` as alias for `--help`

Thanks to @tqorange for contributing.

### v1.0.0 (08-04-2021):

- Include Python 3.6, not only greater than.
- Add DeepSource code checker and resolve found issue (related to shell=true)
- Add aliases for command-line next to az-switch: + az-account-switch + az-account-switcher _(the package name)_
- Dump to v1.0.0, since it's working fine for a while and looks better!

### v0.0.6 (25-03-2021):

Add support for disabled subscriptions.
