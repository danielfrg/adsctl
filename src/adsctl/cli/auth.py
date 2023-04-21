import hashlib
import os
import re
import socket
import sys
from urllib.parse import unquote

import click
from google_auth_oauthlib.flow import Flow

from adsctl.application import Application

_SCOPE = "https://www.googleapis.com/auth/adwords"
_SERVER = "127.0.0.1"
_PORT = 8080
_REDIRECT_URI = f"http://{_SERVER}:{_PORT}"


@click.command()
@click.argument(
    "secrets_file",
    type=click.Path(exists=True),
)
@click.pass_obj
def auth(app: Application, secrets_file):
    """Authenticate with Google Ads API."""

    # Load config
    app.load_config()

    current_account = app.config.current_account
    click.echo("Getting new refresh token for account: " + current_account)

    new_refresh_token = oauth_flow(secrets_file)

    if new_refresh_token is None:
        click.echo("Authentication failed.")
        sys.exit(1)

    click.echo(f"Your new refresh token is: {new_refresh_token}\n")
    click.echo("Updating config file to include refresh token.")

    with open(app.config_file.path, "r") as f:
        current_contents = f.read()

    with open(app.config_file.path, "w") as f:
        new_content = current_contents
        current_token = app.config.accounts[current_account].oauth.refresh_token

        # None means the refresh_token field not found in the account header
        if current_token is None:
            # Add the refresh token to the config file below the account.oauth header

            account_header_str = f"[accounts.{current_account}.oauth]"

            header_occurrences = current_contents.count(account_header_str)

            if header_occurrences == 1:
                # Found the right header, so append the refresh token
                appended_line = (
                    account_header_str + f'\nrefresh_token = "{new_refresh_token}"'
                )
                new_content = new_content.replace(account_header_str, appended_line)
            else:
                f.write(current_contents)
                click.echo(
                    "Error updating the config file:\n"
                    "Could't find the right account group."
                    "Please add the refresh token above to the config file:\n"
                    f"{app.config_file.path}"
                )
                sys.exit(1)
        else:
            # See how many matches of the refresh_token find in the file

            current_token_str = f'refresh_token = "{current_token}"'
            current_token_occurrences = current_contents.count(current_token_str)

            if current_token_occurrences == 1:
                # We found one match, so replace it
                new_token_str = rf'refresh_token = "{new_refresh_token}"'
                new_content = current_contents.replace(current_token_str, new_token_str)
            else:
                f.write(current_contents)
                click.echo(
                    "Error updating the config file:\n"
                    "The current refresh_token was found multiple times in the file. "
                    "Please add the refresh token above to the config file:\n"
                    f"{app.config_file.path}"
                )
                sys.exit(1)

        f.write(new_content)

    click.echo("Done! You can now run adsctl commands.")


def oauth_flow(secrets_file: str) -> str | None:
    """Do the OAuth flow to get a refresh token."""

    # if args.additional_scopes:
    #     configured_scopes.extend(args.additional_scopes)

    configured_scopes = [_SCOPE]

    flow = Flow.from_client_secrets_file(secrets_file, scopes=configured_scopes)
    flow.redirect_uri = _REDIRECT_URI

    # Create an anti-forgery state token as described here:
    # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        state=passthrough_val,
        prompt="consent",
        include_granted_scopes="true",
    )

    # Prints the authorization URL so you can paste into your browser. In a
    # typical web application you would redirect the user to this URL, and they
    # would be redirected back to "redirect_url" provided earlier after
    # granting permission.
    click.echo("Paste this URL into your browser:\n")
    click.echo(authorization_url)
    click.echo(f"\nWaiting for authorization and callback to: {_REDIRECT_URI}\n")

    # Retrieves an authorization code by opening a socket to receive the
    # redirect request and parsing the query parameters set in the URL.
    code = unquote(get_authorization_code(passthrough_val))

    # Pass the code back into the OAuth module to get a refresh token.
    flow.fetch_token(code=code)

    refresh_token = flow.credentials.refresh_token
    return refresh_token


def get_authorization_code(passthrough_val):
    """Opens a socket to handle a single HTTP request containing auth tokens.
    Args:
        passthrough_val: an anti-forgery token used to verify the request
          received by the socket.
    Returns:
        a str access token from the Google Auth service.
    """
    # Open a socket at _SERVER:_PORT and listen for a request
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((_SERVER, _PORT))
    sock.listen(1)
    connection, address = sock.accept()
    data = connection.recv(1024)
    # Parse the raw request to retrieve the URL query parameters.
    params = parse_raw_query_params(data)

    message = ""
    try:
        if not params.get("code"):
            # If no code is present in the query params then there will be an
            # error message with more details.
            error = params.get("error")
            message = f"Failed to retrieve authorization code. Error: {error}"
            raise ValueError(message)
        elif params.get("state") != passthrough_val:
            message = "State token does not match the expected state."
            raise ValueError(message)
        else:
            message = "Authorization code was successfully retrieved."
    except ValueError as error:
        print(error)
        sys.exit(1)
    finally:
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html\n\n"
            f"<b>{message}</b>"
            "<p>Please check the console output.</p>\n"
        )

        connection.sendall(response.encode())
        connection.close()

    return params.get("code")


def parse_raw_query_params(data):
    """Parses a raw HTTP request to extract its query params as a dict.
    Note that this logic is likely irrelevant if you're building OAuth logic
    into a complete web application, where response parsing is handled by a
    framework.
    Args:
        data: raw request data as bytes.
    Returns:
        a dict of query parameter key value pairs.
    """
    # Decode the request into a utf-8 encoded string
    decoded = data.decode("utf-8")
    # Use a regular expression to extract the URL query parameters string
    match = re.search("GET\\s\\/\\?(.*) ", decoded)
    params = match.group(1)
    # Split the parameters to isolate the key/value pairs
    pairs = [pair.split("=") for pair in params.split("&")]
    # Convert pairs to a dict to make it easy to access the values
    return dict(pairs)
