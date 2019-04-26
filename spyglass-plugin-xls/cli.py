# Copyright 2018 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import click
import spyglass
from spyglass.site_processors.site_processor import SiteProcessor

LOG = logging.getLogger(__name__)

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(name)s:' \
             '%(funcName)s [%(lineno)3d] %(message)s'


@click.option('-v',
              '--verbose',
              is_flag=True,
              default=False,
              help='Enable debug messages in log.')
@click.group()
def excel(*, verbose):
    """Plugin for extracting site data from Excel spreadsheets"""
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=log_level)


EXCEL_FILE_OPTION = click.option(
    '-x',
    '--excel-file',
    'excel_file',
    multiple=True,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    required=True,
    help='Path to the engineering Excel file. Required for '
    'spyglass-plugin-xls plugin.',
)

EXCEL_SPEC_OPTION = click.option(
    '-e',
    '--excel-spec',
    'excel_spec',
    type=click.Path(exists=True, readable=True, dir_okay=False),
    required=True,
    help='Path to the Excel specification YAML file for the engineering '
    'Excel file. Required for spyglass-plugin-xls plugin.',
)

SITE_CONFIGURATION_FILE_OPTION = click.option(
    '-c',
    '--site-configuration',
    'site_configuration',
    type=click.Path(exists=True, readable=True, dir_okay=False),
    required=False,
    help='Path to site specific configuration details YAML file.')

INTERMEDIARY_DIR_OPTION = click.option(
    '-idir',
    '--intermediary-dir',
    'intermediary_dir',
    type=click.Path(exists=True, file_okay=False, writable=True),
    default='./',
    help='Directory in which the intermediary file will be created.')

SITE_NAME_CONFIGURATION_OPTION = click.option(
    '-s',
    '--site-name',
    'site_name',
    type=click.STRING,
    required=False,
    help='Name of the site for which the intermediary is being generated.')

TEMPLATE_DIR_OPTION = click.option(
    '-tdir',
    '--template-dir',
    'template_dir',
    type=click.Path(exists=True, readable=True, file_okay=False),
    required=True,
    help='Path to the directory containing manifest J2 templates.')

MANIFEST_DIR_OPTION = click.option(
    '-mdir',
    '--manifest-dir',
    'manifest_dir',
    type=click.Path(exists=True, writable=True, file_okay=False),
    required=False,
    help='Path to place created manifest files.')


@excel.command('g',
               short_help='generate intermediary',
               help='Generates an intermediary file from passed excel data.')
@EXCEL_FILE_OPTION
@EXCEL_SPEC_OPTION
@SITE_CONFIGURATION_FILE_OPTION
@INTERMEDIARY_DIR_OPTION
@SITE_NAME_CONFIGURATION_OPTION
def generate_intermediary(*args, **kwargs):
    process_input_ob = \
        spyglass.cli.intermediary_processor('spyglass-plugin-xls', **kwargs)
    LOG.info("Generate intermediary yaml")
    process_input_ob.generate_intermediary_yaml()
    process_input_ob.dump_intermediary_file(kwargs['intermediary_dir'])


@excel.command('m',
               short_help='generates manifest and intermediary',
               help='Generates manifest and intermediary files.')
@click.option(
    '-g',
    '--generate-intermediary',
    'generate_intermediary',
    is_flag=True,
    default=False,
    help='Flag to save the generated intermediary file used for the manifests.'
)
@EXCEL_FILE_OPTION
@EXCEL_SPEC_OPTION
@SITE_CONFIGURATION_FILE_OPTION
@INTERMEDIARY_DIR_OPTION
@SITE_NAME_CONFIGURATION_OPTION
@TEMPLATE_DIR_OPTION
@MANIFEST_DIR_OPTION
def generate_manifests_and_intermediary(*args, **kwargs):
    process_input_ob = \
        spyglass.cli.intermediary_processor('spyglass-plugin-xls', **kwargs)
    LOG.info("Generate intermediary yaml")
    intermediary_yaml = process_input_ob.generate_intermediary_yaml()
    if generate_intermediary:
        LOG.debug("Dumping intermediary yaml")
        process_input_ob.dump_intermediary_file(kwargs['intermediary_dir'])
    else:
        LOG.debug("Skipping dump for intermediary yaml")

    LOG.info("Generating site Manifests")
    processor_engine = SiteProcessor(intermediary_yaml, kwargs['manifest_dir'])
    processor_engine.render_template(kwargs['template_dir'])
