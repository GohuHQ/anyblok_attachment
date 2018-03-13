# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from os import urandom

from anyblok.tests.testcase import DBTestCase


class TestFieldFunction(DBTestCase):
    blok_entry_points = ('bloks', 'test_bloks')

    def test_get_latest_document(self):
        registry = self.init_registry(None)
        registry.upgrade(install=('test_report_4',))
        file_ = urandom(100)
        doc = registry.Attachment.Document.insert(file=file_)
        t = registry.DocumentTest.insert()
        t.latest_document = doc
        self.assertEqual(t.latest_document.uuid, doc.uuid)
        self.assertEqual(t.latest_document.version, doc.version)
        doc.historize_a_copy()
        self.assertEqual(t.latest_document.uuid, doc.uuid)
        self.assertEqual(t.latest_document.version, doc.version)
