# Friends Keeper

Application to help you (or at least try) to keep your friends :raising_hand: by reminding you to contact (text :love_letter:, call :iphone:, whatsapp or anything you use to communicate) them.

---

- [Friends Keeper](#friends-keeper)
  - [Installation and execution](#installation-and-execution)
    - [Docker usage. :package:](#docker-usage-package)
    - [Local execution :computer:](#local-execution-computer)
  - [FAQ :raising_hand_woman::raising_hand_man:](#faq-raising_hand_womanraising_hand_man)
  - [Support :mechanic:](#support-mechanic)
  - [Contributing](#contributing)
  - [License](#license)
  - [TODO:](#todo)

---

## Installation and execution

### Docker usage. :package:

- Building docker image

  ```console
  docker build --tag friends_keeper .
  ```

  <details>
    <summary>Console output</summary>
    
    ```console
    (.venv) yeyeto2788@juan-thinkbook:~/workspace/own_workspace/friends_keeper$ docker build --tag friends_keeper .
    Sending build context to Docker daemon  395.8kB
    Step 1/5 : FROM python:3.9-buster
    ---> 1b33974176a3
    Step 2/5 : COPY ./ /friends_keeper/
    ---> 5443b99733cc
    Step 3/5 : WORKDIR /friends_keeper
    ---> Running in e1f551917b5e
    Removing intermediate container e1f551917b5e
    ---> 6f3f9bc74dee
    Step 4/5 : RUN pip install poetry &&     poetry install --no-dev
    ---> Running in 4ac0a7c185ae
    Collecting poetry
      Downloading poetry-1.1.13-py2.py3-none-any.whl (175 kB)
    Collecting requests<3.0,>=2.18
      Downloading requests-2.27.1-py2.py3-none-any.whl (63 kB)
    Collecting pexpect<5.0.0,>=4.7.0
      Downloading pexpect-4.8.0-py2.py3-none-any.whl (59 kB)
    Collecting packaging<21.0,>=20.4
      Downloading packaging-20.9-py2.py3-none-any.whl (40 kB)
    Collecting requests-toolbelt<0.10.0,>=0.9.1
      Downloading requests_toolbelt-0.9.1-py2.py3-none-any.whl (54 kB)
    Collecting virtualenv<21.0.0,>=20.0.26
      Downloading virtualenv-20.13.1-py2.py3-none-any.whl (8.6 MB)
    Collecting keyring>=21.2.0
      Downloading keyring-23.5.0-py3-none-any.whl (33 kB)
    Collecting pkginfo<2.0,>=1.4
      Downloading pkginfo-1.8.2-py2.py3-none-any.whl (26 kB)
    Collecting cachy<0.4.0,>=0.3.0
      Downloading cachy-0.3.0-py2.py3-none-any.whl (20 kB)
    Collecting html5lib<2.0,>=1.0
      Downloading html5lib-1.1-py2.py3-none-any.whl (112 kB)
    Collecting tomlkit<1.0.0,>=0.7.0
      Downloading tomlkit-0.10.0-py3-none-any.whl (33 kB)
    Collecting crashtest<0.4.0,>=0.3.0
      Downloading crashtest-0.3.1-py3-none-any.whl (7.0 kB)
    Collecting clikit<0.7.0,>=0.6.2
      Downloading clikit-0.6.2-py2.py3-none-any.whl (91 kB)
    Collecting shellingham<2.0,>=1.1
      Downloading shellingham-1.4.0-py2.py3-none-any.whl (9.4 kB)
    Collecting poetry-core<1.1.0,>=1.0.7
      Downloading poetry_core-1.0.7-py2.py3-none-any.whl (424 kB)
    Collecting cleo<0.9.0,>=0.8.1
      Downloading cleo-0.8.1-py2.py3-none-any.whl (21 kB)
    Collecting cachecontrol[filecache]<0.13.0,>=0.12.9
      Downloading CacheControl-0.12.10-py2.py3-none-any.whl (20 kB)
    Collecting msgpack>=0.5.2
      Downloading msgpack-1.0.3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (322 kB)
    Collecting lockfile>=0.9
      Downloading lockfile-0.12.2-py2.py3-none-any.whl (13 kB)
    Collecting pastel<0.3.0,>=0.2.0
      Downloading pastel-0.2.1-py2.py3-none-any.whl (6.0 kB)
    Collecting pylev<2.0,>=1.3
      Downloading pylev-1.4.0-py2.py3-none-any.whl (6.1 kB)
    Collecting webencodings
      Downloading webencodings-0.5.1-py2.py3-none-any.whl (11 kB)
    Collecting six>=1.9
      Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
    Collecting jeepney>=0.4.2
      Downloading jeepney-0.7.1-py3-none-any.whl (54 kB)
    Collecting importlib-metadata>=3.6
      Downloading importlib_metadata-4.11.1-py3-none-any.whl (17 kB)
    Collecting SecretStorage>=3.2
      Downloading SecretStorage-3.3.1-py3-none-any.whl (15 kB)
    Collecting zipp>=0.5
      Downloading zipp-3.7.0-py3-none-any.whl (5.3 kB)
    Collecting pyparsing>=2.0.2
      Downloading pyparsing-3.0.7-py3-none-any.whl (98 kB)
    Collecting ptyprocess>=0.5
      Downloading ptyprocess-0.7.0-py2.py3-none-any.whl (13 kB)
    Collecting idna<4,>=2.5
      Downloading idna-3.3-py3-none-any.whl (61 kB)
    Collecting certifi>=2017.4.17
      Downloading certifi-2021.10.8-py2.py3-none-any.whl (149 kB)
    Collecting urllib3<1.27,>=1.21.1
      Downloading urllib3-1.26.8-py2.py3-none-any.whl (138 kB)
    Collecting charset-normalizer~=2.0.0
      Downloading charset_normalizer-2.0.12-py3-none-any.whl (39 kB)
    Collecting cryptography>=2.0
      Downloading cryptography-36.0.1-cp36-abi3-manylinux_2_24_x86_64.whl (3.6 MB)
    Collecting cffi>=1.12
      Downloading cffi-1.15.0-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (444 kB)
    Collecting pycparser
      Downloading pycparser-2.21-py2.py3-none-any.whl (118 kB)
    Collecting filelock<4,>=3.2
      Downloading filelock-3.6.0-py3-none-any.whl (10.0 kB)
    Collecting platformdirs<3,>=2
      Downloading platformdirs-2.5.1-py3-none-any.whl (14 kB)
    Collecting distlib<1,>=0.3.1
      Downloading distlib-0.3.4-py2.py3-none-any.whl (461 kB)
    Installing collected packages: pycparser, urllib3, idna, charset-normalizer, cffi, certifi, zipp, requests, pylev, pastel, msgpack, jeepney, cryptography, crashtest, webencodings, six, SecretStorage, pyparsing, ptyprocess, platformdirs, lockfile, importlib-metadata, filelock, distlib, clikit, cachecontrol, virtualenv, tomlkit, shellingham, requests-toolbelt, poetry-core, pkginfo, pexpect, packaging, keyring, html5lib, cleo, cachy, poetry
    Successfully installed SecretStorage-3.3.1 cachecontrol-0.12.10 cachy-0.3.0 certifi-2021.10.8 cffi-1.15.0 charset-normalizer-2.0.12 cleo-0.8.1 clikit-0.6.2 crashtest-0.3.1 cryptography-36.0.1 distlib-0.3.4 filelock-3.6.0 html5lib-1.1 idna-3.3 importlib-metadata-4.11.1 jeepney-0.7.1 keyring-23.5.0 lockfile-0.12.2 msgpack-1.0.3 packaging-20.9 pastel-0.2.1 pexpect-4.8.0 pkginfo-1.8.2 platformdirs-2.5.1 poetry-1.1.13 poetry-core-1.0.7 ptyprocess-0.7.0 pycparser-2.21 pylev-1.4.0 pyparsing-3.0.7 requests-2.27.1 requests-toolbelt-0.9.1 shellingham-1.4.0 six-1.16.0 tomlkit-0.10.0 urllib3-1.26.8 virtualenv-20.13.1 webencodings-0.5.1 zipp-3.7.0
    WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
    WARNING: You are using pip version 21.2.2; however, version 22.0.3 is available.
    You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
    Creating virtualenv friends-keeper-VJBQmwGX-py3.9 in /root/.cache/pypoetry/virtualenvs
    Updating dependencies
    Resolving dependencies...
    Writing lock file
    Package operations: 15 installs, 0 updates, 0 removals
      • Installing certifi (2021.10.8)
      • Installing charset-normalizer (2.0.12)
      • Installing idna (3.3)
      • Installing urllib3 (1.26.8)
      • Installing attrs (21.4.0)
      • Installing greenlet (1.1.2)
      • Installing pyrsistent (0.18.1)
      • Installing requests (2.27.1)
      • Installing wcwidth (0.2.5)
      • Installing click (8.0.4)
      • Installing gotify (0.2.2)
      • Installing jsonschema (4.4.0)
      • Installing prettytable (3.1.1)
      • Installing pyyaml (6.0)
      • Installing sqlalchemy (1.4.31)
    Installing the current project: friends_keeper (0.1.0)
    Removing intermediate container 4ac0a7c185ae
    ---> 5a076d11311a
    Step 5/5 : ENTRYPOINT [ "poetry", "run", "friends_keeper" ]
    ---> Running in 57fff1b46b57
    Removing intermediate container 57fff1b46b57
    ---> cb3f827a9809
    Successfully built cb3f827a9809
    Successfully tagged friends_keeper:latest
    ```
  </details>

- Running the container passing the local database

  ```console
  docker run -it --rm -v $PWD/friends_keeper.db:/friends_keeper/friends_keeper.db:rw -v $PWD/config.yaml:/friends_keeper/config.yaml:ro --name friend_keeper friends_keeper show friends
  ```

  <details>
    <summary>Console output</summary>
    
    ```console
    (.venv) yeyeto2788@juan-thinkbook:~/workspace/own_workspace/friends_keeper$ docker run -it --rm -v $PWD/friends_keeper.db:/friends_keeper/friends_keeper.db:rw -v $PWD/config.yaml:/friends_keeper/config.yaml:ro --name friend_keeper friends_keeper show friends
    Using debug level 20
    2022-02-22 09:12:40,643 [friends_keeper.utils] - [INFO] Loading configuration from '/friends_keeper/config.yaml'
    2022-02-22 09:12:40,645 [friends_keeper.utils] - [DEBUG] Validating configuration file content.
    2022-02-22 09:12:40,653 [friends_keeper.utils] - [DEBUG] Config file schema is valid.
    2022-02-22 09:12:40,653 [friends_keeper.utils] - [INFO] Using './friends_keeper.log' for logging
    2022-02-22 09:12:40,653 [friends_keeper.utils.orm.friends] - [INFO] Querying database for friends
    2022-02-22 09:12:40,655 [friends_keeper.utils.orm] - [DEBUG] Executing query: 'SELECT friends.id, friends.name, friends.last_name, friends.nickname, friends.relationship, friends.min_days, friends.max_days, friends.active 
    FROM friends 
    WHERE friends.active = true ORDER BY friends.id'
    2022-02-22 09:12:40,660 [friends_keeper.utils.orm] - [DEBUG] Query executed!
    2022-02-22 09:12:40,660 [friends_keeper.utils.orm.friends] - [INFO] Found friends: '1, 2, 3, 4, 5'
    Friends in database
    +-----------+---------------+-----------+-----------+--------+
    | Friend ID |    Nickname   | Min. days | Max. days | Active |
    +-----------+---------------+-----------+-----------+--------+
    |     1     |   Pedro Mata  |     15    |     30    |  True  |
    |     2     |  Maria Teresa |     15    |     30    |  True  |
    |     3     |Roberto Mijares|     20    |     30    |  True  |
    |     4     |    Ma.Gaby    |     15    |     30    |  True  |
    |     5     |Sofia Rodriguez|     20    |     30    |  True  |
    +-----------+---------------+-----------+-----------+--------+
    ```
  </details>

### Local execution :computer:

This step is not mandatory as we'll be heavily using docker for development and for executing the code on this repository.

- Clone this repository
  - `git clone https://github.com/yeyeto2788/friends_keeper.git`
- Create the virtual environment and activate it
  - `poetry shell`
- Install dependencies
  - `poetry install`
- Instantiate the pre-commit plugin
  - `poetry run pre-commit install`

---

<!-- Frequently asked questions -->

## FAQ :raising_hand_woman::raising_hand_man:

No frequently asked question yet. :neutral_face:

---

<!-- Support -->

## Support :mechanic:

Reach out to me at one of the following places!

- Website at [juanbiondi.com](https://www.juanbiondi.com) (Work In Progess)
- Create an [issue](https://github.com/yeyeto2788/friends_keeper/issues/new/choose) on this repository. :pirate_flag:
- Send me an [email](mailto:jebp.freelance@gmail.com) :email:

---

<!-- Contributing -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/super_awesome_feature`)
3. Commit your Changes (`git commit -m 'Add some awesome feature'`)
4. Push to the Branch (`git push origin feature/super_awesome_feature`)
5. Open a Pull Request

---

<!-- License -->

## License

See [**`LICENSE`**](./LICENSE) for more information.

## TODO:

- Finish tests
