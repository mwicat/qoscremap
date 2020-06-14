# -*- coding: utf-8 -*-

"""Console script for qoscremap."""

import logging
import os
import sys

from .qoscremap import start_osc_ui

import yaml

import click


def get_config_path():
    return os.path.expanduser('~/.oscremap.yaml')


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('-l', '--loglevel', help='Logging level')
@click.pass_context
def cli(ctx, debug, loglevel):
    ctx.obj['DEBUG'] = debug
    if loglevel is not None:
        loglevel = getattr(logging, loglevel.upper(), None)
    else:
        loglevel = logging.INFO
    logging.basicConfig(level=loglevel)


@cli.command()
@click.option('-c', '--config', default='default',
              help='Configuration name to use')
def start(config):
    """
    Start proxy between application and device.
    """

    config_path = get_config_path()
    if os.path.exists(config_path):
        cfg = yaml.safe_load(open(config_path))
        current_config = cfg.get(config)
    else:
        current_config = None

    if current_config is None:
        click.fail(
            'Configuration "{}" does not exist.'
            ' Please run command "oscremap generate-config" first.')

    start_osc_ui(current_config)


def main():
    sys.exit(cli(obj={}))


if __name__ == '__main__':
    main()
