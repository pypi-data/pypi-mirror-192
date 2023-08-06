# -*- coding: utf-8 -*-
"""\
* Base Abstract Class For Multi-Paging Scrapers. Needs to be Sub-Classed.
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* Is dereived from wsf_scraperBasic.ScraperBasic.
** Needs to evolve so that in practice it can support multi-page urls.
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_scraperMultipage"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111212813"
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

from unisos.wsf import wsf_digestHtml
from unisos.wsf import wsf_common

from unisos.wsf import wsf_scraperBasic

from unisos import icm


class ScraperMultipage(wsf_scraperBasic.ScraperBasic):
    """Base Web Scraper Abstract Multipage Pricipal Class For multi-page Urls.

    This abstract class is based on the wsf_scraperBasic.ScraperBasic abstract class.

    This class is abstract and incomplete. It should be subClassed.

    Features provided by this pricipal class are:

    - Support for paging of multi-page urls.
    """

    def __init__(self,):

        super(ScraperMultipage, self).__init__()

        # make the first soup
        self.makeSoupForNewPage()
        self.moveToNextTag()

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def scrape(self):
        """Extracts relevant information."""
        wsf_common.log('Multi-page scraping started')
        while True:
            #self._num_mines += 1
            # End condition
            if self._isFinished:
                return

            if self._curTag is None or self._isEndOfUrl(self._curTag):
                self._isFinished = True
                return

            # Turn the page
            elif self._isEndOfPage(self._curTag):
                self._nextPage()
                self.makeSoupForNewPage()

            for i, attribute in enumerate(self.attributes):

                # Function that accepts a tag and returns a boolean
                tester = f'_is_{attribute}_tag'

                # Function that accedpts a tag and returns a string
                processor = f'_process_{attribute}'

                # Ensure proper methods are defined for tag testing
                if not hasattr(self, tester):
                    raise NotImplementedError(
                        f'SubClass must implement {tester}')

                tester = getattr(self, tester)

                if(tester(self._curTag)):
                    if i == 0 and not self._curResult.bare:
                        self._captureResultAndRenew

                    # Uses a processor if exists
                    if hasattr(self, processor):
                        processor = getattr(self, processor)
                        this_attribute = processor(self._curTag)
                    else:
                        this_attribute = str(self._curTag)
                        
                    setattr(self._curResult, attribute, this_attribute)

            # Move on
            if self._curResult.complete:
                self._captureResultAndRenew()
            self.moveToNextTag()

    def moveToNextTag(self):
        """Moves forward until another Tag or None is found."""
        self._curTag = self._curTag.next  #typing: ignore
        while not isinstance(self._curTag, bs4.element.Tag):
            self._curTag = self._curTag.next
            if self._curTag is None:
                break

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def makeSoupForNewPage(self):
        """Makes new soup from the current source."""
        self._soup = wsf_digestHtml.soupFromInput(self._curInputSrc, "https_url")

        # Make tag to mark the end of this page
        new_soup = bs4.BeautifulSoup()
        end_tag = new_soup.new_tag('div', attrs={'class': 'page-end'})
        self._soup.insert(-1, end_tag)
        
        self._curTag = self._soup.find('html')

    def _isEndOfPage(self, tag):
        """Returns True if `tag` signals the end of the page."""
        return wsf_common.tagHasClassname(tag, 'page-end')

    #
    # #####  Expected To Be SubClassed Methods #####
    #
    def _isEndOfUrl(self, tag):
        print(f"OOPS: MustBeOverridenException -- _isEndOfUrl: tag={tag}")

    def _nextPage(self):
        """Point to the next page."""
        print(f"OOPS: MustBeOverridenException -- _nextPage")

####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
