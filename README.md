## Switch Azure subscriptions

Switching subscriptions using the [Azure CLI](https://docs.microsoft.com/cli/azure/manage-azure-subscriptions-azure-cli) involves too much typing

```bash
# Type a lot...
az account list --output table

# Use mouse to select the subscription-id in the console
# Use ctrl-c to copy the text, this might be optional 
 
# Type a lot...
az account set --subscription-id <paste subscription-id>
```

So, I have simplified this task with the command-line utility **az-switch** with colors! The active subscription is bold and green and selected as default argument. Just select the subscription you want to activate.

> Optionally you can pass: --profile/-p myprofile  

```bash
#
az-switch
[1]: 5ddxxc0-xxxx-44c1-b12a-xxxb5dexxx: CompanyY PayAsYouGo
[2]: 882xx6c-xxxx-4121-912a-xxx25c8xxx: PersonalSubscription
[3]: d3fxx79-xxxx-4b11-812d-xxx974axxx: CompanyX INNOVATION
[4]: 8c1xx9e-xxxx-4e91-912c-xxx1842xxx: CompanyX Production
[5]: 26axxfb-xxxx-4ad1-8128-xxxf0eexxx: CompanyZ - staging
[6]: 463xx72-xxxx-4cf1-8125-xxxa803xxx: CompanyZ - prod
[7]: 29dxxe9-xxxx-4461-9123-xxxd5d5xxx: CompanyZ - dev
Switch to [4]: 5
Active: 26axxfb-xxxx-4ad1-8128-xxxf0eexxx: CompanyZ - staging
``` 

### Install

`pip install git+git://github.com/abij/az-account-switcher`