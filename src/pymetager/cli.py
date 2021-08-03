#!/usr/bin/python

import sys
import click
import os
import configparser
import toml

from .version_manager import (
    _version_ops,
    _main_version_components,
    _segment_version_components,
    update_config_version,
)


DEFAULT_SETUP_CFG = os.path.join(os.curdir, "setup.cfg")
DEFAULT_PYPROJECT_TOML = os.path.join(os.curdir, "pyproject.toml")


if os.path.isfile(DEFAULT_PYPROJECT_TOML):
    DEFAULT_CONFIG = DEFAULT_PYPROJECT_TOML
else:
    DEFAULT_CONFIG = DEFAULT_SETUP_CFG


def get_config(config_fp=DEFAULT_CONFIG):
    _, extension = os.path.splitext(config_fp)
    if extension == ".cfg":
        config = configparser.ConfigParser()
        config.read(config_fp)
        return config, config_fp, extension
    elif extension == ".toml":
        config = toml.load(config_fp)
        return config, config_fp, extension
    else:
        raise NotImplementedError(
            "File extension not recognized. Shoud be `.toml` or `.cfg`."
        )


@click.group("pypack-metager")
@click.option("-q", "--quiet", is_flag=True, help="Flag for minimal output.")
@click.option(
    "--config_fp",
    default=DEFAULT_CONFIG,
    show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Custom path for setup.cfg.",
)
@click.pass_context
def cli(ctx, quiet, config_fp):
    ctx.ensure_object(dict)
    ctx.obj["QUIET"] = quiet

    config, config_fp, config_type = get_config(config_fp=config_fp)
    ctx.obj["CONFIG"] = config
    ctx.obj["CONFIG_FP"] = config_fp
    ctx.obj["CONFIG_TYPE"] = config_type

    if not quiet:
        click.secho("--- PYPACK-METAGER ---", fg="green")
        click.secho("A BuildNN Open Source project.", fg="green")
        click.secho("Reading/Writing from/to {}".format(config_fp))


# fmt: off
@cli.command()
@click.pass_context
@click.argument("element", type=click.Choice(list(_version_ops.keys())))
@click.option("-s", "--segment", type=click.Choice(_segment_version_components),
              default="dev", show_default=True,
              help="If element == 'segment', which segment type to increase.")
@click.option("-u", "--increment_upstream", type=click.Choice(_main_version_components),
              default=None, show_default=True,
              help="If element == 'segment', which upstream to increase "
              "if version is not already in that segment type.")
@click.option("-v", "--custom_version", default=None, show_default=True,
              help="If element == 'custom' reverts version to custom string.")
@click.option("--force", is_flag=True,
              help="If element == 'custom', flag to force version change "
              "(eg if custom is lower).")
# fmt: on
def increment(ctx, element, segment, increment_upstream, custom_version, force):
    update_config_version(
        config=ctx.obj["CONFIG"],
        config_fp=ctx.obj["CONFIG_FP"],
        config_type=ctx.obj["CONFIG_TYPE"],
        element=element,
        segment=segment,
        increment_upstream=increment_upstream,
        custom_version=custom_version,
        force=force,
    )


@cli.command()
@click.pass_context
@click.argument("name", type=click.STRING, default="version")
@click.option("-s", "--section", type=click.STRING, default="metadata")
def echo_meta_elm(ctx, name, section):
    config = ctx.obj["CONFIG"]
    config_fp = ctx.obj["CONFIG_FP"]

    try:
        _section = config
        for s in section.split("."):
            _section = _section[s]
    except KeyError:
        raise KeyError(f"Section '{section}' does not exist in `{config_fp}`.")
    try:
        sys.stdout.write(str(_section[name]) + "\n")
    except KeyError:
        raise KeyError(f"Tag '{name}' does not exist in `{config_fp}`/'{section}'.")


if __name__ == "__main__":
    cli()
