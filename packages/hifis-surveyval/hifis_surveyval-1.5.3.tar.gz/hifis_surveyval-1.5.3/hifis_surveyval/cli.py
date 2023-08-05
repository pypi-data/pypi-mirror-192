#!/usr/bin/env python

# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/7/>`_.
    There is also a very helpful `tutorial video
    <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: hifis_surveyval.cli
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
import pathlib
from csv import reader

import click
import pkg_resources
import yaml

from hifis_surveyval.core import util
from hifis_surveyval.core.dispatch import Dispatcher
from hifis_surveyval.core.preprocess import Preprocessor
from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.hifis_surveyval import HIFISSurveyval

settings: Settings = Settings()


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    default=0,
    show_default=True,
    help="Enable verbose output. "
    "Increase verbosity by setting this option up to 3 times.",
)
def cli(verbose: int) -> None:
    """
    Analyze a given CSV file with a set of independent python scripts.

    Args:
        verbose (int): Indicates the verbosity level on the CLI.
    """
    # NOTE that click takes above documentation for generating help text
    # Thus the documentation refers to the application per se and not the
    # function (as it should)

    settings.set_verbosity(verbose)
    if not settings.VERBOSITY == logging.ERROR:
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )


@cli.command()
def version() -> None:
    """Get the library version."""
    version_string: str = pkg_resources.require("hifis_surveyval")[0].version
    click.echo(click.style(f"{version_string}", bold=True))


@cli.command()
@click.option(
    "--config",
    "-c",
    is_flag=True,
    show_default=True,
    default=False,
    help="Create a default config as file. "
    "Overwrites any existing configuration file.",
)
@click.option(
    "--example",
    "-e",
    is_flag=True,
    show_default=True,
    default=False,
    help="Create an example script in the given script folder. "
    "Overwrites any existing example script file.",
)
@click.option(
    "--preprocess",
    "-p",
    is_flag=True,
    show_default=True,
    default=False,
    help="Create an empty preprocessing script in the given location. "
    "Overwrites any existing preprocessing script.",
)
@click.option(
    "--template",
    "-t",
    is_flag=True,
    show_default=True,
    default=False,
    help="Create a pre-filled Matplotlib custom plot style template, "
         "if not already existing.",
)
def init(
        config: bool,
        example: bool,
        preprocess: bool,
        template: bool
) -> None:
    r"""
    Create all files with a basic configuration needed for an analysis run.

    Create a configuration file, a preprocessing script, an example script and
    a custom plot style template file in the default locations.
    It will overwrite any existing configuration, preprocessing and example
    script file despite the custom plot style template file.
    If none of the explicit options are given, the command create all files.
    \f

    Args:
        config (bool):
            Indicates whether to create a configuration file. (Default: False)
        example (bool):
            Indicates whether to create an example analysis script.
            (Default: False)
        preprocess (bool):
            Indicates whether to create an example preprocessing script.
            (Default: False)
        template (bool):
            Indicates whether to create a pre-filled Matplotlib custom plot
            style file. (Default: False)
    """
    all_files = not (config or example or preprocess or template)

    if config or all_files:
        settings.create_default_config_file()
    if example or all_files:
        util.create_example_script(settings)
    if preprocess or all_files:
        util.create_preprocessing_script(settings)
    if template or all_files:
        util.create_custom_plot_style_template()


@click.argument(
    "survey_data",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
)
@cli.command()
def analyze(survey_data: pathlib.Path) -> None:
    """
    Read the survey data and run all defined analysis scripts.

    The metadata are read from a file specified in the settings.

    Args:
        survey_data (click.File): File that contains all data for the analysis.
    """
    settings.load_config_file()

    if not survey_data.suffix.lower() == ".csv":
        logging.error("Loaded data file seems not to be a CSV file.")

    surveyval: HIFISSurveyval = HIFISSurveyval(settings=settings)
    raw_data: DataContainer = DataContainer(settings=settings)
    logging.info(f"Analyzing file {survey_data.name}")

    # Load the metadata
    logging.info(f"Attempt to load metadata from {settings.METADATA}")
    yaml_files = [file for file in settings.METADATA.iterdir()]
    # Filter out those files that do not have a YAML file extension
    yaml_files = list(filter(
        lambda file: file.suffix.lower() in [".yml", ".yaml"],
        yaml_files
    ))

    for file in yaml_files:
        logging.debug(f"Loading Metadata from {file}")
        with file.open(mode="r", encoding="utf-8-sig") as io_stream:
            metadata_yaml = yaml.safe_load(io_stream)
            raw_data.load_metadata(metadata_yaml)

    #  Load the actual survey data
    logging.info(f"Attempt to load survey data from {survey_data}")
    with survey_data.open(mode="r", encoding="utf-8-sig") as data_io_stream:
        csv_reader = reader(data_io_stream)
        raw_data.load_survey_data(csv_data=list(csv_reader))

    # preprocess the data
    preprocessed_data: DataContainer = Preprocessor.preprocess(
        settings=settings, data=raw_data
    )

    # run analysis scripts
    dispatcher: Dispatcher = Dispatcher(
        surveyval=surveyval, data=preprocessed_data
    )
    dispatcher.discover()
    dispatcher.load_all_modules()
