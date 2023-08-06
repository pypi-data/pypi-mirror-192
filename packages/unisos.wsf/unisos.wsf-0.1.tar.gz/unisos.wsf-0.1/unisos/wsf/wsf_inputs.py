# -*- coding: utf-8 -*-
"""\
* Process Inputs: Given a source URL, obtain it as html.
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* TODO Needs to support other forms of input and properly error handle.
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_inputs"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111211402"
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/bpfInfo-mbAgplShort.py"
bpfInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net/contact]]",],
}
####+END:

bpfInfo['credits'] = ""


import requests

def inputObtainAsHtml(source, sourceType):
    """Return html, given sourceType"""

    html = None

    if sourceType == 'https_url':
        # NOTYET, do this with exception handling
        html = requests.get(source).text
    else:
        print(f"Unknown sourceType={sourceType}")

    return html



####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
