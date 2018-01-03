# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from uuid import uuid1
from anyblok.column import UUID, DateTime, String, Selection
from datetime import datetime
from .exceptions import RenderException, PathException
from .common import format_path
import os


Model = Declarations.Model
Attachment = Model.Attachment
register = Declarations.register


@register(Attachment)
class Template:
    """Base Model template to define the main configuration between templating
    system"""
    TYPE = 'invalid'

    uuid = UUID(primary_key=True, nullable=False, default=uuid1, binary=False)

    created_at = DateTime(nullable=False, default=datetime.now)
    updated_at = DateTime(nullable=False, default=datetime.now,
                          auto_update=True)

    model = String(foreign_key=Model.System.Model.use('name'), nullable=False)
    filename = String(nullable=False,
                      default="{doc.uuid}-{doc.version}-{date}")
    type = Selection(selections="get_template_type", nullable=False)

    def get_template_type(self):
        """Give the tempate type"""
        return {
            'invalid': 'Invalid template'
        }

    template_from = Selection(selections="get_template_from", nullable=False,
                              default='path')
    template_path = String()

    def get_template_from(self):
        """Give the location of the template"""
        return {
            'path': 'From path on file system',
        }

    parser_from = Selection(selections="get_parser_from", nullable=False,
                            default='model')
    parser_model = String(default="Model.Attachment.Parser")

    def get_parser_from(self):
        """Give the location of the parser"""
        return {
            'model': 'From model',
        }

    @classmethod
    def define_mapper_args(cls):
        mapper_args = super(Template, cls).define_mapper_args()
        if cls.__registry_name__ == 'Model.Attachment.Template':
            mapper_args.update({
                'polymorphic_identity': cls.TYPE,
                'polymorphic_on': cls.type,
            })
        else:
            mapper_args.update({
                'polymorphic_identity': cls.TYPE,
            })

        return mapper_args

    def get_template(self):
        """return the template file to compute"""
        if self.template_from == 'path':
            if not self.template_path:
                raise PathException("No path define for %r", self)

            path = format_path(self.template_path)
            if not os.path.isfile(path):
                raise PathException("%r must be a file", self.template_path)

            with open(path, 'r', encoding='utf-8') as fd:
                return fd.read()

    def get_parser(self):
        """return the template file to compute"""
        if self.parser_from == 'model':
            if self.parser_model:
                return self.registry.get(self.parser_model)

    def render(self, data):
        """Return the file create by the templating engine"""
        raise RenderException("No render defined by %r", self.__class__)
