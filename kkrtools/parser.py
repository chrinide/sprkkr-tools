#!/usr/bin/env python3
"""Parser module."""
import os
import collections


def parse_settings(input_file='kkrtools.inp'):
    """Return settings from an input file along with the defaults."""
    block = False
    supported_blocks = ['kkrtools', 'scf', 'dos', 'pbs']
    settings = {b: {} for b in supported_blocks}
    line_num = 0
    templates_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
    default_file = os.path.join(templates_dir, 'kkrtools.default')

    def parse_setting(line):
        """Return the setting key and value from a string line."""
        nonlocal block
        nonlocal supported_blocks
        line = line.strip()
        Setting = collections.namedtuple('Setting', ['block', 'key', 'value'])

        # Check for comments
        if not line.startswith('#'):
            # Check for start of a block
            if not block and line.startswith('%block '):
                block = line.split()[1].lower()

                # Check if block name is actually supported
                if block not in supported_blocks:
                    print('Block ' + block +
                          ' in line ' + str(line_num) + ' not recognise')
                    block = False

            # Check for end of a block
            # This is regardless of the name
            if block is not False and line.startswith('%endblock'):
                block = False

            # If this is indeed inside a block
            # then get the key and value of the setting
            if block is not False:
                setting = line.split('=')

                if len(setting) >= 2:
                    key = setting[0].rstrip()
                    value = setting[1].lstrip()

                    # Check for comments in value
                    if '#' in value:
                        value = value.split('#')[0].rstrip()

                    return Setting(block, key, value)

        return Setting(False, False, False)

    def store_settings(input_file, default=False):
        """Store settings from input file."""
        nonlocal line_num

        with open(input_file) as f:
            for line in f:
                line_num += 1
                setting = parse_setting(line)

                if (setting.block is not False and
                        # Check whether the new setting is supported
                        (default or setting.key in settings[setting.block])):
                    settings[setting.block][setting.key] = setting.value

    # First load all the defaults
    # then override it with the user inputs
    store_settings(default_file, True)
    store_settings(input_file)

    return settings
