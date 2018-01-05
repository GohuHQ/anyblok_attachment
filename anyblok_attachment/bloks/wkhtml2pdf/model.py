# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import Integer, DateTime, Selection, String, Boolean
from anyblok.relationship import Many2One
from datetime import datetime
from sqlalchemy import CheckConstraint
import tempfile
import os

register = Declarations.register
Attachment = Declarations.Model.Attachment


@register(Attachment)
class WkHtml2Pdf:

    id = Integer(primary_key=True, nullable=False)
    created_at = DateTime(nullable=False, default=datetime.now)
    updated_at = DateTime(nullable=False, default=datetime.now,
                          auto_update=True)

    margin_bottom = Integer(nullable=False, default=4)
    margin_left = Integer(nullable=False, default=4)
    margin_right = Integer(nullable=False, default=4)
    margin_top = Integer(nullable=False, default=4)
    orientation = Selection(
        selections={'Landscape': 'Landscape', 'Portrait': 'Portrait'},
        nullable=False, default='Portrait')
    page = Many2One(model='Model.Attachment.WkHtml2Pdf.Page',
                    nullable=False)
    background = Boolean(default=True)

    @classmethod
    def define_table_args(cls):
        table_args = super(WkHtml2Pdf, cls).define_table_args()
        return table_args + (
            CheckConstraint('margin_bottom >= 0',
                            name="marge_bottom_upper_than_0"),
            CheckConstraint('margin_left >= 0',
                            name="marge_left_upper_than_0"),
            CheckConstraint('margin_right >= 0',
                            name="marge_right_upper_than_0"),
            CheckConstraint('margin_top >= 0',
                            name="marge_top_upper_than_0"),
        )

    def convert2pdf(self, prefix, html_content):
        tmp_dir = tempfile.mkdtemp(prefix + '-html2pdf')
        html_path = os.path.join(tmp_dir, 'in.html')
        pdf_path = os.path.join(tmp_dir, 'out.pdf')

        with open(html_path, 'wb', encoding='utf-8') as fd:
            fd.write(html_content)


@register(Attachment.WkHtml2Pdf)
class Page:
    """Define the Page size"""

    label = String(primary_key=True, nullable=False)
    created_at = DateTime(nullable=False, default=datetime.now)
    updated_at = DateTime(nullable=False, default=datetime.now,
                          auto_update=True)

    size = String()
    height = Integer()
    width = Integer()

    @classmethod
    def define_table_args(cls):
        table_args = super(Page, cls).define_table_args()
        return table_args + (
            CheckConstraint(
                '(height is null and width is null) or '
                '(height > 0 and width > 0)',
                name="size_upper_than_0"),
        )

    def get_options(self):
        options = []
        for field in ('size', 'width', 'height'):
            val = getattr(self, field)
            if val:
                options.append('--page-' + field)
                options.append(str(val))

        return options

    def check_flush_validity(self):
        if not self.size and not self.height and not self.width:
            raise PageValidityException(
                "You must define a size or a height and width")

        if self.size:
            self.height = None
            self.width = None

    @classmethod
    def after_update_orm_event(cls, mapper, connection, target):
        target.check_flush_validity()

    @classmethod
    def after_insert_orm_event(cls, mapper, connection, target):
        target.check_flush_validity()
