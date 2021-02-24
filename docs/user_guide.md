# User Guide

## Reason why

Essentially, in [BuildNN](https://www.buildnn.com) we use a custom full automation
in package release cycle. Therefore, we needed a tool to update package versions with
a minimal overhead.

We embrace the `config` paradigma for package metadata: take away metadata from setup.py and
move them to `setup.cfg` or `pyproject.toml`

> NOTE: full `pyproject.toml` and `poetry` support will come soon...


## Explore the CLI

```bash
$ pymetager --help
Usage: pymetager [OPTIONS] COMMAND [ARGS]...

Options:
  -q, --quiet       Flag for minimal output.
  --config_fp FILE  Custom path for setup.cfg.  [default: ./setup.cfg]
  --help            Show this message and exit.

Commands:
  echo-meta-elm
  increment
```

let's use info print function

```bash
$ pymetager echo-meta-elm --help
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Usage: pymetager echo-meta-elm [OPTIONS] [NAME]

Options:
  -s, --section TEXT
  --help              Show this message and exit
```

```bash
$ pymetager echo-meta-elm version
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
0.0.1
```

Or, concisely

```bash
$ pymetager -q echo-meta-elm version
0.0.1
```

## Increment Version

Strictly following Python's [PEP440 Guidelines](https://www.python.org/dev/peps/pep-0440/)

### [A] Increment micro version
```bash
$ pymetager increment micro
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.1` to `0.0.2`.
Writing back config...
```

### [B] Increment minor version
```bash
$ pymetager increment minor
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.1` to `0.1`.
Writing back config...
```

### [C] Increment major version
```bash
$ pymetager increment major
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.1` to `1.0`.
Writing back config...
```

> Major version increment will be visible in `setup.cfg` as you will see opening the file
> ```bash
>  $ cat setup.cfg
> ...
> [metadata]
> name = my-awesome-package
> version = 1.0
> ...
> ```

### [D] Increment version segment (dev, pre, post)

#### [D1] Increment dev
Let's say we are at version `0.0.1`.
```
$ pymetager echo-meta-elm version
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
0.0.1
```

The following attempt to pass to `dev` version segment will fail
(we can not move from full release back to dev)...
```bash
$ pymetager increment segment -s dev
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Traceback (most recent call last):
  ... <traceback stuff>
  File "<>/pymetager/src/pymetager/cli.py", line 64, in increment
    update_config_version(
  File "<>/pymetager/src/pymetager/version_manager.py", line 177, in update_config_version
    new_version = _version_ops[element](version, **kwargs)
  File "<>/pymetager/src/pymetager/version_manager.py", line 123, in increment_segment
    raise ValueError("Current version Segment is higher than the required one!")
ValueError: Current version Segment is higher than the required one!
```

What we can do, is to pass from current version to a new one (eg. incrementing the upstream `micro` version)
in dev segment:
```
$ pymetager increment segment -s dev -u micro
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.1` to `0.0.2.dev0`.
Writing back config...
```


#### [D2] Increment pre
> Note: `pre` segment is prior to release, thus from release on you cannot revert back to pre or dev. You can update to pre only dev.
```bash
$ pymetager increment segment -s pre
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.2.dev0` to `0.0.2rc0`.
Writing back config...
``` 
> Note: `rc` stands for release candidate :)


#### [D3] Increment --> Release
After release candidate validation or directly from dev, we can go with full release:
```
$ pymetager increment release
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.2rc0` to `0.0.2`.
Writing back config...
```

#### [D4] Increment post
> Note: you can increment to post from release and every other segment type. Once in post segment, you can go only to the next release (or to its dev, using `--increment_upstream`)
Post is used for small bugfix after release in prod
```bash
$ pymetager increment segment -s post
--- PYPACK-METAGER ---
A BuildNN Open Source project.
Reading/Writing from/to ./setup.cfg
Read config from ./setup.cfg
Updating version `0.0.2` to `0.0.2.post0`.
Writing back config...
```
