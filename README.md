uddr_client
======================

A Python SDK for UltraDDR

## Installation

The package can be installed using pip

```bash
pip install uddr_client
```

## Setup

For ease of use, you can store your API key in an environment file using the client's "setup" method.

```python
import uddr_client
uddr_client.connect.setup()
```

Alternatively, you can pass the key directly to the connection using keyword arguments.

```python
c = uddr_client.connect('api_key=<your API key>')
```

If your API key is associated with more than one organization, you can specify which one to use by passing the organization name as a keyword argument or by setting it in your environment.

```python
import uddr_client
client = uddr_client.connect()
doh_client = client.doh()
doh_client.setup()
```

## API Usage

```python
import uddr_client

c = uddr_client.connect() # Instantiates a new instance of the client which, by default, uses the API key stored in your .env
api_client = c.api()      # Creates an API client instance
resp = api_client.reports()        # Call an endpoint
print(resp)
```

### Available methods

The API client currently supports the following endpoints:

* `aggregates()`
* `bar()`
* `histogram()`
* `summary()`
* `report()`
* `reports()`
* `histogram_artifact()`
* `logs()`
* `passthrough()`
* `category()`
* `account()`
  * `organization()`
    * `settings()`
    * `products()`
    * `packages()`
  * `user()`
    * `organizations()`
* `decision()`
  * `baseline()`
    * `countries()`

Use Python's help function for more in-depth documentation on each method.

```python
help(c.api().logs)
```

### Response parsing

Aside from the `report()` _(application/pdf)_ and `category()` _(list)_ endpoints, all methods produce a Response object which handles different outputs.

* `Response.xml()`: Outputs the response in XML
* `Response.csv()`: Outputs the response in CSV

The default is JSON.

## DoH Usage

The DNS over HTTPS (DoH) client provides an interface for directly querying the UDDR resolvers.

```python
import uddr_client

client = uddr_client.connect()
doh = client.doh() # Creates a DoH client instance
lookup = doh.lookup('google.com') # Perform a lookup on google.com
print(lookup)  # This will return the full json response for the lookup
```

### Record Types

The client stores the response for various DNS record types as properties. The following are supported.

```python
lookup.A      # For A records
lookup.AAAA   # For AAAA records
lookup.CNAME  # For CNAME records
lookup.NS     # For NS records
lookup.MX     # For MX records
lookup.TXT    # For TXT records
lookup.SOA    # For SOA records
lookup.SRV    # For SRV records
lookup.CAA    # For CAA records
lookup.DS     # For DS records
lookup.DNSKEY # For DNSKEY records
```

### Reverse Lookups

If you pass an IP to the client, it will automatically perform a reverse lookup (PTR).

### IoC Parsing

This concept is borrowed from Michael Smith's [DDR-IOC-Checker](https://github.com/rybolov/DDR-IOC-Checker).

Indicators of compromise passed to the DOHClient as a positional argument will be run through a parser. The parser accepts the following:

1. Domain names
2. URLs by means of stripping the protocol and path
3. "Defanged" URLs which are intentionally obfuscated for security reasons
4. Emails - the parser will remove the prefix and @
5. IP addresses

### Additional Methods

The following methods return information about the DoH query or specific parts of the response.

* `status()` - Returns an object with information about the status of the response. DoH provides a numerical code, this expands with a message and description.
* `block_info()` - Returns a string stating whether the domain is blocked (by checking if the A record resolves to the UDDR block page).
* `answer()` - Returns the answer section of the response, if one exists.
* `authority()` - Returns the authority section of the response, if one exists.

## Dependencies

* pandas
* xmltodict
* python-decouple
* requests

## License

This project is licensed under the terms of the MIT license. See LICENSE.md for more details.
