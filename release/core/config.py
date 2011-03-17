#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for loading/parsing configuration file.
Values are accessible in this way:
config.settings.section.value
or short form:
config.section.value
e.g
import config
config.settings.network.port
config.network.port

use 'from config import x' to import sections

from config import settings
settings.network.port
or
from config import network
network.port

Reload/store new configurations with load() and store():
import config
config.settings.exisitngsection.newoption = value
config.settings.store()
"""

import ConfigParser
import logging
import logging.handlers
import sys


class _Container(dict):
    """ A simple&lightweight container/struct class """

    def __getattr__(self, attr):
        """ Modifies method resolution to enable
        'config.foo.bar' syntax suggar."""
        try:
            return self[attr]
        except KeyError:
            return object.__getattribute__(self, attr)

    def __repr__(self):
        result = []
        for option, value in self.items():
            result.append(option + ' = ' + str(value))
        return "\n".join(result)

    def __setattr__(self, attr, value):
        """ Modifies attribute setting. Do not use python-like names for your
        options (or write more code/do it without 'syntax suggar') """

        if attr in dir(self):
            raise ValueError('Name clashing with python interna: %s' % attr)
        else:
            self[attr] = value


class Config(_Container):
    """ A configuration reader/parser/writer class """
    ignore = ['logger']

    def __init__(self, file_name='settings.cfg'):
        object.__setattr__(self, "file_name", file_name)
        self.load()
        self.setup_logger()
        _Container.__init__(self)

    def __repr__(self):
        result = []
        for setting in self:
            for option, value in self[setting].items():
                result.append(setting + "." + option + " = " + str(value))

        return "\n".join(result)

    def load(self):
        """ Loads a config file and creates for every section/option entry
        a dynamic accessible attribute """

        cfg = ConfigParser.SafeConfigParser()
        cfg.read(self.file_name)

        for section in cfg.sections():
            config_sect = _Container()
            setattr(self, section, config_sect)
            for option, value in cfg.items(section):
                try:
                    value = cfg.getint(section, option)
                except ValueError:
                    try:
                        value = cfg.getfloat(section, option)
                    except ValueError:
                        value = cfg.get(section, option)
                setattr(config_sect, option, value)
        # parse neighbours:
        try:
            for sect in [self.fallback_servers, self.last_known_neighbours]:
                for neighbour in sect:
                    ip_addr, port = sect[neighbour].split(':')
                    sect[neighbour] = (ip_addr.strip(), int(port))
        except ValueError, reason:
            raise ValueError("Error while reading %s!" %
                             self.file_name, reason)

    def store(self):
        """ Stores changed data in configuration file format """
        cfg = ConfigParser.SafeConfigParser()
        for setting in self:
            cfg.add_section(setting)
            if setting == 'last_known_neighbours':
                name = 'neighbour%s'
                i = 0
                try:
                    for ip_addr, port in self[setting]:
                        i += 1
                        cfg.set(setting, name % i, "%s:%s" % (ip_addr, port))
                except ValueError:
                    self.logs.logger.warning("Please pass a new/updated" +
                                            "neighbourlist!")
                    continue

            elif setting == 'fallback_servers':
                try:
                    for value in self[setting]:
                        cfg.set(setting, value, "%s:%s" % self[setting][value])
                except ValueError:
                    continue
            else:
                for option, value in self[setting].items():
                    if option not in Config.ignore:
                        cfg.set(setting, option, str(value))

        with open(self.file_name, "w") as cfg_file:
            cfg.write(cfg_file)

    def setup_logger(self, no_file = False):
        """ Creates a logger.Usage: settings.logs.logger.debug('x') """
        levels = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

        if self.logs.logfile != '' and not no_file:
            handler = logging.handlers.RotatingFileHandler(
                self.logs.logfile, maxBytes=100*1024, backupCount=3)
        else:
            handler = logging.StreamHandler(sys.stdout)
        frm = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")
        handler.setFormatter(frm)

        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(levels[self.logs.active_level])
        self.logs.levels = levels.keys()
        self.logs.logger = logger

# Initialises the module and creates 'virtual submodules'
# for short-form-access (e.g config.network)
locals()['settings'] = Config()
for _section, _options in locals()['settings'].items():
    locals()[_section] = _options
