# GAQL (Google Ads Query Language) Shell

A command line tool for executing GAQL queries against the Google Ads API.
Like [psql](https://www.postgresql.org/docs/current/app-psql.html) for the Google Ads API.

## Usage

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
