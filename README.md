# Friends Keeper

---

- [Friends Keeper](#friends-keeper)
  - [Installation and execution](#installation-and-execution)
    - [Docker usage.](#docker-usage)
  - [TODO:](#todo)

## Installation and execution

### Docker usage.

Building docker image

```console
docker build --tag friends_keeper .
```

Running the container passing the local database

```console
docker run -it --rm -v $PWD/friends_keeper.db:/friends_keeper/friends_keeper.db:rw -v $PWD/config.yaml:/friends_keeper/config.yaml:ro --name friend_keeper friends_keeper show friends
```

## TODO:

- Finish documentation.
- Add execution examples.
- Optional:
  - Enable API (Optional)
