# -*- coding: utf-8 -*-
"""\
* All of this modules configuration is done in python.
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* The external interface to this module is a set of functions. Not the _Config class.
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_config"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111213815"
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/bpfInfo-mbAgplShort.py"
bpfInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net/contact]]",],
}
####+END:

bpfInfo['credits'] = ""


class _Config(object):
    def __init__(self):
        pass

    @property
    def scrapingName(self) -> str:
        return self._scrapingName

    @scrapingName.setter
    def scrapingName(self,
                     value: str
                     ):
        self._scrapingName = value

    @property
    def inputSources(self):
        return self._inputSources

    @inputSources.setter
    def inputSources(self, urls):
        self._inputSources = urls

    @property
    def resultsSpec_baseDir(self):
        return self._resultsSpec_baseDir

    @resultsSpec_baseDir.setter
    def resultsSpec_baseDir(self, value):
        self._resultsSpec_baseDir = value

    @property
    def resultsSpec_format(self):
        return self._resultsSpec_format

    @resultsSpec_format.setter
    def resultsSpec_format(self, value):
        self._resultsSpec_format = value

    @property
    def scraperClass(self):
        return self._scraperClass

    @scraperClass.setter
    def scraperClass(self, value):
        self._scraperClass = value

    @property
    def fieldsOfInterest(self):
        return self._fieldsOfInterest

    @fieldsOfInterest.setter
    def fieldsOfInterest(self, value):
        self._fieldsOfInterest = value


params = _Config()

def scrapingName(
        name,
):
    params.scrapingName = name


def inputSources(
        urls,
):
    params.inputSources = urls


def resultsSpec(
        baseDir,
        resultsFormat,

):
    params.resultsSpec_baseDir = baseDir
    params.resultsSpec_format = resultsFormat

def scrapingProcessor(
        scraperClass,
):
    params.scraperClass = scraperClass

def fieldsOfInterest(
        fields,
):
    params.fieldsOfInterest = fields

####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
