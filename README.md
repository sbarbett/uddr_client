uddr_client
======================

A Python library for the UltraDDR API

## Installation

The package can be installed using pip

```bash
pip install uddr_client
```

## Setup

For ease of use, you can store your API key as an environment variable using the client's "setup" method.

```python
import uddr_client
uddr_client.connect.setup('<your API key>')
```

Alternatively, you can pass the API key directly to the connection.

```python
c = uddr_client.connect('<your API key>')
```

## Usage

```python
import uddr_client

c = uddr_client.connect() # Instantiates a new instance of the client which, by default, uses the API key
						  # stored in your environment

resp = c.reports()        # Call an endpoint
print(response)
```

### Available methods

The client currently supports the following endpoints:

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
help(c.logs)
```

### Response parsing

Aside from the `report()` endpoint (which returns an application/pdf), all methods produce a Response object which handles different outputs.

* `Response.xml()`: Outputs the response in XML
* `Response.csv()`: Outputs the response in CSV

The default is JSON.

## Dependencies

* pandas
* xmltodict

## License

This project is licensed under the terms of the MIT license. See LICENSE.md for more details.