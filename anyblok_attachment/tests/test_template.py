# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import DBTestCase
from anyblok import Declarations
from anyblok.column import UUID, String
from anyblok_attachment.bloks.report.exceptions import (
    TemplateException, PathException)
from os import urandom


def add_in_registry(file_=None):

    @Declarations.register(Declarations.Model.Attachment)
    class Template:

        def get_template_type(self):
            res = super(MyTemplate, self).get_template_type()
            res.update({'MyTemplate': 'My Template'})
            return res

    @Declarations.register(Declarations.Model.Attachment.Template,
                           tablename=Declarations.Model.Attachment.Template)
    class MyTemplate(Declarations.Model.Attachment.Template):
        TYPE = 'MyTemplate'

        def render(self, data):
            return file_


def add_in_registry_multi(file_=None):

    @Declarations.register(Declarations.Model.Attachment)
    class Template:

        def get_template_type(self):
            res = super(MyTemplate, self).get_template_type()
            res.update({'MyTemplate': 'My Template'})
            return res

    @Declarations.register(Declarations.Model.Attachment.Template)
    class MyTemplate(Declarations.Model.Attachment.Template):
        TYPE = 'MyTemplate'

        uuid = UUID(
            primary_key=True, nullable=False, binary=False,
            foreign_key=Declarations.Model.Attachment.Template.use('uuid'))
        other_option = String()

        def render(self, data):
            return file_


class TestTemplate(DBTestCase):

    def test_without_parser(self):
        file_ = urandom(10)
        registry = self.init_registry_with_bloks(
            ['report'], add_in_registry, file_=file_)
        with self.assertRaises(TemplateException):
            registry.Attachment.Template.MyTemplate.insert(
                parser_model="",
                template_path="report#=#common.py",
                model="Model.System.Blok"
            )

    def test_without_template(self):
        file_ = urandom(10)
        registry = self.init_registry_with_bloks(
            ['report'], add_in_registry, file_=file_)
        with self.assertRaises(PathException):
            registry.Attachment.Template.MyTemplate.insert(
                template_path="",
                model="Model.System.Blok"
            )

    def test_add_new_parser_type_single_table(self):
        file_ = urandom(10)
        registry = self.init_registry_with_bloks(
            ['report'], add_in_registry, file_=file_)
        template = registry.Attachment.Template.MyTemplate.insert(
            template_path="report#=#common.py",
            filename='test',
            model="Model.System.Blok"
        )
        document = registry.Attachment.Document.insert(template=template)
        get_file = document.get_file()
        wanted_file = {
            'filename': 'test',
            'file': file_,
            'filesize': len(file_),
            'contenttype': 'plain/text',
            'file_added_at': get_file['file_added_at'],
            'hash': get_file['hash']
        }
        self.assertEqual(get_file, wanted_file)
        self.assertTrue(get_file['hash'])
        self.assertTrue(get_file['file_added_at'])

    def test_add_new_parser_type_multi_table(self):
        file_ = urandom(10)
        registry = self.init_registry_with_bloks(
            ['report'], add_in_registry_multi, file_=file_)
        template = registry.Attachment.Template.MyTemplate.insert(
            template_path="report#=#common.py",
            filename='test',
            model="Model.System.Blok"
        )
        document = registry.Attachment.Document.insert(template=template)
        get_file = document.get_file()
        wanted_file = {
            'filename': 'test',
            'file': file_,
            'filesize': len(file_),
            'contenttype': 'plain/text',
            'file_added_at': get_file['file_added_at'],
            'hash': get_file['hash']
        }
        self.assertEqual(get_file, wanted_file)
        self.assertTrue(get_file['hash'])
        self.assertTrue(get_file['file_added_at'])
