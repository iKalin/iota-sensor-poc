# IOTA Sensor POC

Attach arbitrary data to the IOTA Tangle. Ultimate goal is to provide a POC of how attaching sensor data to the Tangle would work.

## Installation

```
pip install -r requirements.txt
```

## Configuration

Configuration options can be specified via CLI or config file.

### CLI arguments

  - `--node`: node to connect to (defaults to http://localhost:14265/).
  - `--seed`: seed to use.
  - `--address`: address to send the data to.
  - `--tag`: identifying Tag for the stream.
  - `--data`: data to send as part of the transaction(s).
  - `--file`: file to read data from.
  - `--config`: configuration file to read options from.
  - `--stdin`: whether to read data from stdin.

### Config file format

Most of the options can be specified on an config file. You can tell the script to read this file via the `--config` option.

Here's how your configuration file should look:

```
[default]
node=http://localhost:14265
seed=AAAAAAAA
address=BBBBBBBB
tag=STREAMID
```

## Usage

### Send some data 

```
sender.py --seed XXXX --address YYYY --data '{"hi": "there"}'
```

### Send the contents of a file

```
sender.py --seed XXXX --address YYYY --file /path/to/file
```

### Send data read from stdin

```
echo 'some information' | sender.py --stdin --config
```
