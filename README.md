# Google Ads API CLI and Prompt

<p align="center">
    <a href="https://pypi.org/project/adsctl/">
        <img src="https://img.shields.io/pypi/v/adsctl.svg">
    </a>
    <a href="https://pypi.org/project/mkdocs-jupyter">
        <img src="https://img.shields.io/pypi/pyversions/adsctl.svg">
    </a>
    <a href="https://github.com/danielfrg/adsctl/actions/workflows/test.yml">
        <img src="https://github.com/danielfrg/adsctl/workflows/test/badge.svg">
    </a>
    </a>
    <a href="https://github.com/danielfrg/adsctl/blob/main/LICENSE.txt">
        <img src="https://img.shields.io/:license-Apache%202-blue.svg">
    </a>
</p>

Features:

- A command line tool for executing GAQL queries against the Google Ads API.
  Like [psql](https://www.postgresql.org/docs/current/app-psql.html) for the Google Ads API.
- A command line tool for managing Google Ads resources.
  Like [kubectl](https://kubernetes.io/docs/reference/kubectl/) for the Google Ads API.
- Centralized configuration with _(soon)_ multiple config file management
- Automatically update refresh token
- Simple Python API with Pandas integration

Google Ads Interface for humans.

## Installation

```shell
pip install adsctl
```

## Getting started

Requirements:

- All the requirements to use the Google Ads API including Ads Developer Token and OAuth2 credentials
- See [Google Ads API Quickstart](https://developers.google.com/google-ads/api/docs/first-call/overview) for more details.

This project manages it's own configuration files.
To create the configuration file run:

```shell
adsctl config

# Open the location of the config files
adsctl config explore
```

Open the generated config file and fill it with your credentials:
Dev Token, Client ID, Client Secret and Customer ID.
Don't add the `refresh_token`.

To login and get a refresh token:

```shell
adsctl auth <path-to-secret.json>
```

The token is saved automatically in the configuration file.

## GAQL Prompt

An interactive shell for executing GAQL queries against the Google Ads API.

```shell
$ gaql

>>> SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id
+----+-----------------------------+---------+-------------+
|    | resourceName                | name    |          id |
|----+-----------------------------+---------+-------------|
|  0 | customers/XXX/campaigns/YYY | name1   | 10000000000 |
|  1 | customers/XXX/campaigns/YYY | name2   | 10000000000 |
|  2 | customers/XXX/campaigns/YYY | name3   | 10000000000 |
+----+-----------------------------+---------+-------------+
```

By default adsctl prints it in "table" format but you can control the output
format with the `-o` flag:

```shell
# Print the plain protobuf response
$ gaql -o plain

# Print a CSV response
$ gaql -o csv
```

You can also run a single commands and save the output to a file in the specified format:

```shell
$ gaql -c 'SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id' -o csv > my-query.csv
```

This assumes only table is returned but in more complex queries that include other
resources or when using metrics or segments multiple tables are created.
On those cases use the -o csv-files flag to save each table to a different file
based on the table name.

```shell
$ gaql -c 'SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id' -o csv-files

$ ls
campaign.csv
```

## CLI

### Campaign Management

#### Status management

```shell
adsctl campaign -i <campaign-id> status enabled
adsctl campaign -i <campaign-id> status paused
```

#### Update budget

```shell
adsctl campaign -i <campaign-id> budget <amount>
```

### Config

```shell
adsctl config show
```

## Programmatic API

You can also use the Python API to easily execute GAQL queries
and get the results as a Python dict or pandas DataFrame.

```python
import adsctl as ads

# Read config file and create client
google_ads = ads.GoogleAds()

# Execute GAQL query
get_campaigns_query = """
SELECT campaign.name,
  campaign_budget.amount_micros,
  campaign.status,
  campaign.optimization_score,
  campaign.advertising_channel_type,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  campaign.bidding_strategy_type
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status != 'REMOVED'
"""

tables = adsctl.query(get_campaigns_query)

# Print Pandas DataFrames
for table_name, table in tables.items():
    print(table_name)
    print(table, "\n")
```

```plain
campaign
                                 resourceName   status  ...                      name optimizationScore
0  customers/XXXXXXXXXX/campaigns/YYYYYYYYYYY  ENABLED  ...               my-campaign          0.839904
[1 rows x 6 columns]

metrics
  clicks costMicros       ctr    averageCpc impressions
0    210    6730050  0.011457  32047.857143       18330

campaignBudget
                                       resourceName amountMicros
0  customers/XXXXXXXXXX/campaignBudgets/ZZZZZZZZZZZ      1000000
```

Or just directly make a `search_stream` request:

```python
stream = app.search_stream(query)

for batch in stream:
    for row in batch.results:
        ...
```

## Disclaimer

_This is not an official Google product_.

This repository is maintained by a Googler but is not a supported Google product.
Code and issues here are answered by maintainers and other community members on GitHub on a best-effort basis.
