# -*- coding: utf-8 -*-
"""\
* A starting point for the process of converting html input to soup
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* TODO features='lxml' needs to be enhanced.
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_digestHtml"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111210802"
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

from unisos.wsf import wsf_inputs

def soupFromHtml(html):
    """Return soup, given html."""

    return bs4.BeautifulSoup(
        html,
        features='lxml'
    )

def soupFromInput(source, sourceType):
    """Return soup, given source input."""

    html = wsf_inputs.inputObtainAsHtml(source, sourceType)
    return soupFromHtml(html)


####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
