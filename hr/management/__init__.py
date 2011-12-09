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

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    hr_menu, is_new = Menu.objects.get_or_create(
        slug="hr_menu",
        description=_("Main menu for human resources")
    )

    timesheet_menu, is_new = Menu.objects.get_or_create(
        slug="timesheet_menu",
        description=_("Main menu for timesheet")
    )
    
    # Links.
    hr_link, is_new = Link.objects.get_or_create(
        title=_("Human resources"),
        slug="hr",
        description=_("Human resources management"),
        url="{% url timesheet_list %}",
        submenu=hr_menu,
        menu=main_menu
    )

    timesheets_link, is_new = Link.objects.get_or_create(
        title=_("Timesheets"),
        slug="timesheets",
        url="{% url timesheet_list %}",
        menu=hr_menu
    )

    timesheet_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="timesheet-details",
        url="{% url timesheet_detail object.object_id %}",
        menu=timesheet_menu
    )

    timesheet_hard_copies_link, is_new = Link.objects.get_or_create(
        title=_("Hard copies"),
        slug="timesheet-hard-copies",
        url="{% url timesheet_hardcopies object.object_id %}",
        menu=timesheet_menu
    )

    timesheet_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="timesheet-timeline",
        url="{% url timesheet_timeline object.object_id %}",
        menu=timesheet_menu
    )

    # Signatures.
    timesheet_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Timesheet created"),
        slug="timesheet-created"
    )

    timesheet_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Timesheet changed"),
        slug="timesheet-changed"
    )

    timesheet_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Timesheet deleted"),
        slug="timesheet-deleted"
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)