Minimal-ActivityPub
===================

|Repo| |CI| |Downloads|

|Safety| |pip-audit| |Interrogate|

|Codestyle| |Version| |Wheel|

|AGPL|


Minimal-ActivityPub is a minimal Python implementation of the ActivityPub rest API used by
`Mastodon <https://joinmastodon.org/>`_,
`Pleroma <https://pleroma.social/>`_,
and others. This implementation makes use of asyncio where appropriate. It is intended to be used as a library by other
applications. No standalone functionality is provided.

Minimal refers to the fact that only API calls I need for my other projects;
`MastodonAmnesia <https://codeberg.org/MarvinsMastodonTools/mastodonamnesia>`_ and
`TootBot <https://codeberg.org/MarvinsMastodonTools/tootbot>`_ are implemented.

**DO NOT** expect a full or complete implementation of all `ActivityPub API <https://activitypub.rocks/>`_ functionality.

For more details have a look at the `Documentation`_

Contributing
==================================
Issues and pull requests are welcome.

Minimal-ActivityPub is using `pre-commit <https://pre-commit.com/>`_ and `Poetry <https://python-poetry.org/>`_.
Please install and use both pre-commit and Poetry if you'd like to contribute.

To make sure you have all required python modules installed with Poetry is as easy as ``poetry install`` in the root of the
project directory

Licensing
==================================
Minimal-ActivityPub is licences under licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_

Supporting Minimal-ActivityPub
==================================

There are a number of ways you can support Minimal-ActivityPub:

- Create an issue with problems or ideas you have with/for Minimal-ActivityPub
- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.
- You can send me small change in Monero to the address below:

Monero donation address:
----------------------------------
`8ADQkCya3orL178dADn4bnKuF1JuVGEG97HPRgmXgmZ2cZFSkWU9M2v7BssEGeTRNN2V5p6bSyHa83nrdu1XffDX3cnjKVu`


.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
    :alt: AGLP 3 or later
    :target:  https://codeberg.org/MarvinsMastodonTools/minimal-activitypub/src/branch/main/LICENSE.md

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
    :alt: Repo at Codeberg.org
    :target: https://codeberg.org/MarvinsMastodonTools/minimal-activitypub

.. |Downloads| image:: https://pepy.tech/badge/minimal-activitypub
    :alt: Download count
    :target: https://pepy.tech/project/minimal-activitypub

.. |Codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/psf/black

.. |Safety| image:: https://img.shields.io/badge/Safety--DB-checked-green
    :alt: Checked against PyUp Safety DB
    :target: https://pyup.io/safety/

.. |pip-audit| image:: https://img.shields.io/badge/pip--audit-checked-green
    :alt: Checked with pip-audit
    :target: https://pypi.org/project/pip-audit/

.. |Version| image:: https://img.shields.io/pypi/pyversions/minimal-activitypub
    :alt: PyPI - Python Version

.. |Wheel| image:: https://img.shields.io/pypi/wheel/minimal-activitypub
    :alt: PyPI - Wheel

.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/minimal-activitypub/status.svg
    :alt: CI / Woodpecker
    :target: https://ci.codeberg.org/MarvinsMastodonTools/minimal-activitypub

.. |Interrogate| image:: https://codeberg.org/MarvinsMastodonTools/minimal-activitypub/raw/branch/main/interrogate_badge.svg
    :alt: Doc-string coverage
    :target: https://interrogate.readthedocs.io/en/latest/

.. _Documentation: https://marvinsmastodontools.codeberg.page/minimal-activitypub/
