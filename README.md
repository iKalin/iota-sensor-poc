# IOTA Sensor POC

Read sensor data from the public NetAtmo API and attach it to the IOTA Tangle.

## Installation

```
pip install -r requirements.txt
```

## Configuration

Configuration options can be specified via CLI or config file. CLI options have higher precendence than the ones specified in configuration file and can be use to override them.

### CLI arguments

  `--config`: configuration file to read options from.
  `--node`: node to connect to (defaults to http://localhost:14265/).
  `--seed`: seed to use.
  `--address`: address to send the data to.
  `--tag`: identifying Tag for the stream
  `--price`: price value to attach to the data.
  `--client_id`: client_id to used to connect to the NetAtmo API.
  `--client_secret`: client_secret used to connect to the NetAtmo API.
  `--username`: username used to connect to the NetAtmo API.
  `--password`: password used to connect to the NetAtmo API.


### Config file format

Most of the options can be specified on an config file. You can tell the script to read this file via the `--config` option.

Here's how your configuration file should look (`config.ini.dist`):

```
[iota]
node=http://localhost:14265
seed=AAAAAAAA
address=BBBBBBBB
tag=STREAMID
price=1234.5678
[sensor]
client_id=abcabcaabc
client_secret=defdefdef
username=name@localhost
password=123456
```

## Usage

```
python poc.py --config configuration-file.ini
```

## TODO

- Offer a way to read sensor data several times and attaching it as a chunk to the Tangle.
- Handle expired NetAtmo tokens
- Validate tag's length
- Add more NetAtmo API methods
- Better errors for invalid characters in ini files.
