# Google Ads Control CLI

[![PyPI - Version](https://img.shields.io/pypi/v/adsctl.svg)](https://pypi.org/project/adsctl)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/adsctl.svg)](https://pypi.org/project/adsctl)

A command line tool for executing GAQL queries against the Google Ads API.
Like [psql](https://www.postgresql.org/docs/current/app-psql.html) for the Google Ads API.

## Installation

```console
pip install adsctl
```

## Usage

### Shell

```
gaql.py -f path-to-google-ads.yaml -c <customer-id>

>>> SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id
+--------------------------------+-------------+
|              name              |      id     |
+--------------------------------+-------------+
| campaign 1                     | 18273300000 |
| campaign 2                     | 18319200001 |
| campaign 3                     | 18319300002 |
+--------------------------------+-------------+
```
