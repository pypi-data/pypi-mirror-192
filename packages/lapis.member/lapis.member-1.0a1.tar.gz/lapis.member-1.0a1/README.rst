.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

============
lapis.member
============

Content type and workflow for Plone

Features
--------

1) Forum Page is added, it is hidden for everyone but owner and admins
2) Forum page is ‘published’, it is visible for owner, admins and ALL MEMBERS
3) Comments can be enabled as usual
4) The content type does not show by default in menus (add it in the control panel, navigation settings if you want this
5) Content item should be hidden from ‘folder views’ for 'not members', I have not tested this test, but should work: (The permissions should be ‘access content information’, if I remember right



Installation
------------

Install lapis.member by adding it to your buildout::

    [buildout]

    ...

    eggs =
        lapis.member


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/lapis.member/issues
- Source Code: https://github.com/collective/lapis.member
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
