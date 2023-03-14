# Google Ads Control CLI and Prompt

[![PyPI - Version](https://img.shields.io/pypi/v/adsctl.svg)](https://pypi.org/project/adsctl)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/adsctl.svg)](https://pypi.org/project/adsctl)

Features:

- Command line tool for managing Google Ads accounts.
  Like [kubectl](https://kubernetes.io/docs/reference/kubectl/) for Google Ads.
- A command line tool for executing GAQL queries against the Google Ads API.
  Like [psql](https://www.postgresql.org/docs/current/app-psql.html) for the Google Ads API.

## Installation

```shell
pip install adsctl
```

## CLI

### Authentication

```shell
adsctl auth <path-to-secret.json>
```

### Campaign Management

#### Update budget

```shell
adsctl -c <customer-id> campaign -i <campaign-id> budget <amount>
```

## Prompt

An interactive shell for executing GAQL queries against the Google Ads API.

```shell
gaql -f path-to-google-ads.yaml -c <customer-id>

>>> SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id
+--------------------------------+-------------+
|              name              |      id     |
+--------------------------------+-------------+
| campaign 1                     | 18273300000 |
| campaign 2                     | 18319200001 |
| campaign 3                     | 18319300002 |
+--------------------------------+-------------+
```
