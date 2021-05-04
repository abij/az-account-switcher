## Switch Azure subscriptions

| Type| Badge|
|---|---|
| Release workflow | ![!Workflow upload](https://github.com/abij/az-account-switcher/workflows/Upload%20Python%20Package/badge.svg) |
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
  -n INTEGER  Switch to this subscription number directly.
  -v          Verbose: echo the azure-cli commands.
  -h, --help  Show this message and exit.
```

### Example

![example_gif](az-switch-example.gif)

## CHANGELOG

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
