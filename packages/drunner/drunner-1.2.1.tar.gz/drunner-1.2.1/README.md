# Drunner


## Installation

```shell
$ pip install drunner
```


## Usage

### Server init

Run the following command in the terminal to initialize server.

```shell
drunner init --server <host> --server_name <name> --ukey <ukey>
```

### Deploy

Run the `deploy` subcommand to create job.

```shell
drunner deploy notebook <entrypoint> <args> <requirements.txt> --python_version <python_version> --server_name <name>
```


## Documentation

Please install the following version dependencies when send error: ['Click>=8.1.3', 'requests>=2.27.1']
