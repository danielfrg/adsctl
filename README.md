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

Google Ads Interface for humans.

_This is a work in progress, please open an issue if you find any bugs or have any suggestions._

Features:

- A command line tool for executing GAQL queries against the Google Ads API.
  Like [psql](https://www.postgresql.org/docs/current/app-psql.html) for the Google Ads API.
- A command line tool for managing Google Ads resources.
  Like [kubectl](https://kubernetes.io/docs/reference/kubectl/) for the Google Ads API.
- Centralized configuration with multiple account management
- Automatically update refresh token
- Python API with Pandas integration

## Installation

```shell
pip install adsctl
```

## Getting started

Requirements:

- All the requirements to use the Google Ads API including a Developer Token and OAuth2 credentials
- See [Google Ads API Quickstart](https://developers.google.com/google-ads/api/docs/first-call/overview) for more details.

### Configuration

This project manages it's own configuration files.
To create the configuration file run:

```shell
adsctl config

# Open the location of the config files
adsctl config explore
```

Open the new default config file and fill it with your credentials:
Dev Token, Client ID, Client Secret and Customer ID.

To login and get a refresh token:

```shell
adsctl auth <path-to-secret.json>
```

The token is saved automatically in the config file.
You can see it by running:

```shell
# View config
adsctl config view
```

### Multiple Accounts

You can manage multiple accounts in the config file by adding TOML sections.

```toml
current_account = "default"

[... default account ...]

[accounts.another]
developer_token = ""
customer_id = ""
login_customer_id = ""

[accounts.another.oauth]
client_id = ""
client_secret = ""
```

Set the current account:

```shell
$ adsctl config set-account another
$ adsctl config get-account
another
```

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

By default it uses the it in `table` format but you can control the output
format with the `-o` option:

```shell
# Print the plain protobuf response
$ gaql -o plain

# Print the contents of a CSV file
$ gaql -o csv
```

You can also run a single inline command and redirect the output to a file:

```shell
gaql -c 'SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id' -o csv > my-query.csv
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

### Query variables

You can specify one or more variables using the jinja syntax, those
variables will be replaced with the values specified in the `-v` options.

```shell
gaql -c 'SELECT campaign.id, campaign.name FROM campaign WHERE campaign.id = {{ id }} ORDER BY campaign.id' -v id=123456789
```

You can also pass `-v` without a command and use this the variables in the prompt
queries:

```shell
$ gaql -v id=123456789 -v field=name

>>> SELECT campaign.id, campaign.{{ field }} FROM campaign WHERE campaign.id = {{ id }} ORDER BY campaign.id
```

### Other options

You can overwrite the account and customer ID using the `-a` and `-i` options.
See `gaql --help` for more details.

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

## Python API

You can also use the Python API to easily execute GAQL queries
and get the results as a Python dict or pandas DataFrame.

```python
import adsctl as ads

# Read config file and creates the Google Ads client
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
  AND campaign.status != '{{ status }}'
"""

tables = adsctl.query(get_campaigns_query, params={"status": "REMOVED"}})

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

Or directly get a client to use search_stream directly:

```python
gads_client = google_ads.create_client()
stream = self.search_stream(query, client=myclient)

for batch in stream:
    for row in batch.results:
        ...
```

## Disclaimer

_This is not an official Google product_.

This repository is maintained by a Googler but is not a supported Google product.
Code and issues here are answered by maintainers and other community members on GitHub on a best-effort basis.
