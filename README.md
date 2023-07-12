uddr_client
======================

A Python SDK for UltraDDR

## Installation

The package can be installed using pip

```bash
pip install uddr_client
```

## Setup

For ease of use, you can store your API key and client ID in an environment file using the client's "setup" method.

```python
import uddr_client
uddr_client.connect.setup()
```

Alternatively, you can pass the key or ID directly to the connection using keyword arguments.

```python
c = uddr_client.connect('api_key=<your API key>, client_id=<your client ID>')
```

## API Usage

```python
import uddr_client

c = uddr_client.connect() # Instantiates a new instance of the client which, by default, uses the API key stored in your .env

resp = c.api().reports()        # Call an endpoint
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

Use Python's help function for more in-depth documentation on each method.

```python
help(c.api().logs)
```

### Response parsing

Aside from the `report()` endpoint (which returns an application/pdf), all methods produce a Response object which handles different outputs.

* `Response.xml()`: Outputs the response in XML
* `Response.csv()`: Outputs the response in CSV

The default is JSON.

## DoH Usage

The DNS over HTTPS (DoH) client provides an interface for directly querying the UDDR resolvers.

```python
import uddr_client

c = uddr_client.connect() # Instantiates a new instance of the client
doh = c.doh('google.com') # Creates a DOHClient instance for google.com
print(doh)                # This will return the full json response
```

### Record Types

The client stores the response for various DNS record types as properties. The following are supported.

```python
doh.A      # For A records
doh.AAAA   # For AAAA records
doh.CNAME  # For CNAME records
doh.NS     # For NS records
doh.MX     # For MX records
doh.TXT    # For TXT records
doh.SOA    # For SOA records
doh.SRV    # For SRV records
doh.CAA    # For CAA records
doh.DS     # For DS records
doh.DNSKEY # For DNSKEY records
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
