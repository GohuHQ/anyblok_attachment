.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Memento
~~~~~~~

Simple python templating formatage

template file exemple::

    <!doctype html>
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            {description}
        </body>
    </html>

add the documment and create file::

    template = registry.Attachment.Template.Format.insert(
        template_path='path/of/the/python.template',
        contenttype='text/html',
        filename='mypage.html')
    document = registry.Attachment.Document.insert(
        template=template,
        data={'title': 'My page', 'description': 'Hello world !!'}
    )
    document.get_file()

>>>::

    {
        filename: 'mypage.html',
        file: '''
            <!doctype html>
            <html>
                <head>
                    <title>My page</title>
                </head>
                <body>
                    Hello world !!
                </body>
            </html>
        ''',
        contenttype: 'text/html',
        ...
    }
