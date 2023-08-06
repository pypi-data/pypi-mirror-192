# -*- coding: utf-8 -*-
"""\
* Capture results and write them out as needed
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* TODO support for more than cvs should also be included ...
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_results"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111212220"
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/bpfInfo-mbAgplShort.py"
bpfInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net/contact]]",],
}
####+END:

bpfInfo['credits'] = ""


import csv
import datetime
import os

from unisos.wsf import wsf_common
from unisos.wsf import wsf_config

class EachResult:
    """Data structure for holding "mined" attributes."""
    def __init__(self, attrs, attr_default=None):
        """Create instance attributes from `attrs` and defaults to `default`."""
        for attr in attrs:
            setattr(self, attr, attr_default)
        self._attr_names = attrs

    @property
    def attributes(self):
        """Returns a dictionary of the current attributes and values."""
        return {name: getattr(self, name) for name in self._attr_names}

    @property
    def complete(self):
        """Returns True if all attributes have a non-None value."""
        if all(self.attributes.values()):
            return True
        else:
            return False

    @property
    def bare(self):
        """Returns true if all attributes are None."""
        if not any(self.attributes.values()):
            return True
        else:
            return False

    def __repr__(self):
        val_list = ', '.join([f'{name}={self.attributes[name]}'
                              for name in self.attributes])
        return f'EachResult({val_list})'


def resultsWrite(
        resultsList: list,
        resultsSpec_format='csv'
):
    """Uses resultsList to write to file specified in configParams in specified format."""

    dateTag = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')

    targetFileDir = os.path.join(
        wsf_config.params.resultsSpec_baseDir,
        wsf_config.params.scrapingName,
    )

    try:
        os.makedirs(targetFileDir)
    except OSError:
        if not os.path.isdir(targetFileDir):
            raise

    targetFilePath = os.path.join(
        targetFileDir,
        f"{dateTag}.{wsf_config.params.resultsSpec_format}"
    )

    resultDict = []
    for each in resultsList:
        resultDict.append(each.attributes)

    if resultsSpec_format == 'csv':
        with open(targetFilePath, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=wsf_config.params.fieldsOfInterest,
            )
            writer.writerows(resultDict)
            print(f"{wsf_config.params.scrapingName}: Results written to: {targetFilePath}")
    else:
        wsf_common.log(f"UnSupported format: {resultsSpec_format}")


####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
