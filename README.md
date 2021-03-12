## Switch Azure subscriptions

![Upload Python Package](https://github.com/abij/az-account-switcher/workflows/Upload%20Python%20Package/badge.svg)

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
  -n INTEGER          Switch to this subscription number directly.
  --help              Show this message and exit.
```

### Example

![example_gif](az-switch-example.gif)

## CHANGELOG

### v0.0.6 (25-03-2021):

Add support for disabled subscriptions.
