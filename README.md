# IOTA Sensor POC 

Attach sensor data to the IOTA Tangle.

## Configuration

Configuration options can be specified via CLI or 

- CLI arguments
- Configuration file

### CLI arguments

  --node NODE        node to connect to (defaults to http://localhost:14265/).
  --seed SEED        seed to use.
  --address ADDRESS  address to send the data to.
  --tag TAG          identifying Tag for the stream.
  --data DATA        data to send as part of the transaction(s).
  --file FILE        file to read data from.
  --config CONFIG    configuration file to read options from.
  --stdin            whether to read data from stdin.

### Config file format

Most of the options can be specified on an config file. You can tell the script
to read this file via the `--config` option.

Here's how your configuration file should look:

```
[default]
node=http://localhost:14265
seed=AAAAAAAA
address=BBBBBBBB
tag=STREAMID
```

### Environment variables

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
