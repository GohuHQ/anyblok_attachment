# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import Integer

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class DocumentTest(Mixin.LatestDocument):

    id = Integer(primary_key=True, nullable=False)


@register(Model)
class DocumentTest2(Mixin.VersionedDocument):

    id = Integer(primary_key=True, nullable=False)
