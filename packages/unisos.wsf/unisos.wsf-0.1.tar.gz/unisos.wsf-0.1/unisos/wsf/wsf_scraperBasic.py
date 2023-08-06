# -*- coding: utf-8 -*-
"""\
* Basic Web Scraper Abstract Pricipal Class, From Which All Scrapers Are Derived.
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* This is the root class for all scrapers. It is incomplete and needs to be subclassed.
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_scraperBasic"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111212711"
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/bpfInfo-mbAgplShort.py"
bpfInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net/contact]]",],
}
####+END:

bpfInfo['credits'] = ""


import bs4

from unisos.wsf import wsf_results
from unisos.wsf import wsf_config

class ScraperBasic(object):
    """Basic Web Scraper Abstract Pricipal Class.
    From which other Scraper Classes are to be derived.

    This class is abstract and incomplete. It should be subClassed.

    Features provided by this pricipal class are:

    - Capturing of Config parameters.
    - Facilities for simple state transition.
    - Facilities for maintinaing results.
    - Facilities for traversing tags.

    - subclasses are expected to:
        - implement predicate methods of the following form:

        def _is_<attribute>_tag(self, tag: bs4.element.Tag) -> bool

        - implement process methods of the following form:

        def _process_<attribute>(self, tag: bs4.element.Tag) -> str
    """
    def __init__(self):

        self.root_source = wsf_config.params.inputSources[0]
        self.attributes = wsf_config.params.fieldsOfInterest

        # State variables
        self._curInputSrc = wsf_config.params.inputSources[0]
        self._curTag = None
        self._curResult = wsf_results.EachResult(self.attributes)
        self._soup = None
        self._isFinished = False
        self._curPage = 0

        #
        self._urlResultsList = []

    @property
    def state(self):
        """Returns the current value of all dynamic state variables."""
        return {
            'curInputSrc': self._curInputSrc,
            'curTag': self._curTag,
            'curResult': self._curResult,
            'curPage': self._curPage,
            'soup': self._soup,
            'is_finished': self._isFinished,
        }

    def stateSet(self, varName, value):
        """Sets the state of `varName` to `value`.

        The only state variables that can be set are:
          - 'curInputSrc',
          - 'curTag',
          - 'curPage'
        """
        state_types = {'curInputSrc': type('foobar'),
                       'curTag': type(bs4.element.Tag(name='a')),
                       'curPage': type(5)}

        if varName not in state_types:
            raise ValueError(f'Cannot set the state of {varName}')

        if type(value) != state_types[varName]:
            raise TypeError(f'{varName} expected type {state_types[varName]}. Got '
                            f'type {type(value)}')

        setattr(self, f'_{varName}', value)

    @property
    def urlResultsList(self):
        return self._urlResultsList

    def _captureResultAndRenew(self):
        """Add curResult to ResultsList and create a new one."""
        if not self._curResult.bare:
            self._urlResultsList.append(self._curResult)
            self._curResult = wsf_results.EachResult(self.attributes)


    def scrape(self):
        """Main exposed method of this class which goes through the url."""
        print(f"OOPS: MustBeOverridenException -- scrape")

####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
