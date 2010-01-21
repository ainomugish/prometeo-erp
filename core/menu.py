#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <zuck@fastwebnet.it>'
__copyright__ = 'Copyright (c) 2010 Emanuele Bertoldi'
__version__ = '$Revision$'

# Inspired by http://code.google.com/p/django-nav/

from django.core.urlresolvers import reverse

class MenuEntry(object):
    def __init__(self, name=u'', link=None, options=[]):
        self.name = name
        self.link = link
        self.options = options

class MenuOption(MenuEntry):
    template = 'menu/option.html'

class Menu(MenuEntry):
    template = 'menu/menu.html'
    
    def __init__(self, name=u'', link=None, group='main', options=[]):
        super(Menu, self).__init__(name, link, options)
        self.group = group

class MenuBar(object):
    def __init__(self, *args, **kwargs):
        self._groups = {}

    def register(self, menu):
        if not isinstance(menu, MenuEntry):
            raise TypeError("You can only register a <Menu> not a %r" % menu)
            
        print 'Registered %s in group %s' % (menu.name, menu.group)

        if not self._groups.has_key(menu.group):
            self._groups[menu.group] = []

        if menu not in self._groups[menu.group]:
            self._groups[menu.group].append(menu)

    def __getitem__(self, group):
        return self._groups.get(group, [])

    def __setitem__(self, *args):
        raise AttributeError
        
    def __str__(self):
        buff = ''
        for name, group in self._groups:
            buff += name + '\n'
        return buff

menubar = MenuBar()

def autodiscover():
    """
    Auto-discover INSTALLED_APPS 'menu.py' files.
    """
    import imp
    from django.conf import settings
    
    # Core links.
    global menubar
    menubar.register(Menu(u'start', '/'))
    menubar.register(Menu(u'accounts', '/accounts/'))
    
    # Other links.
    for app in settings.INSTALLED_APPS:
        if app == 'prometeo.core':
            continue
            
        # Step 1: find out the app's __path__.
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's 'menu'.
        try:
            imp.find_module('menu', app_path)
        except ImportError:
            continue

        # Step 3: import the app's 'menu' module.
        print 'Importing %s.menu...' % app
        __import__("%s.menu" % app)