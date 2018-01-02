# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import DBTestCase
from anyblok import Declarations
from os import urandom


class TestTemplate(DBTestCase):

    def test_add_new_parser_type(self):
        file_ = urandom(10)

        def add_in_registry():

            @Declarations.register(Declarations.Model.Attachment.Template)
            class MyTemplate(Declarations.Model.Attachment.Template,
                             Declarations.Mixin.AttachmentTemplateType):
                TYPE = 'MyTemplate'

                def get_template_type(self):
                    res = super(MyTemplate, self).get_template_type()
                    res.update({self.TYPE: 'My Template'})
                    return res

                def render(self, data):
                    return file_

        registry = self.init_registry_with_bloks(['report'], add_in_registry)
        template = registry.Attachment.Template.MyTemplate.insert(
            template_path="report#=#common.py",
            filename='test',
            model="Model.System.Blok"
        )
        document = registry.Attachment.Document.insert(template=template)
        self.assertEqual(
            document.get_file(),
            {
                'filename': 'test',
                'file': file_,
                'filesize': len(file_),
                'contenttype': 'plain/text',
            }
        )
