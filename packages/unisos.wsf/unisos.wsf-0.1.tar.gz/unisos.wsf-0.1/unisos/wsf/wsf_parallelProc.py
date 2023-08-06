# -*- coding: utf-8 -*-
"""\
* A starting point for parallel dispatching.
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* This is really just a place holder. Right way of doing this is with something like celery
** Where workers are dispatched in a controlled manner.
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "wsf_parallelProc"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111211727"
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/bpfInfo-mbAgplShort.py"
bpfInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net/contact]]",],
}
####+END:

bpfInfo['credits'] = ""


from multiprocessing import Process

from unisos.wsf import wsf_common
from unisos.wsf import wsf_config
from unisos.wsf import wsf_results

from unisos import icm

@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dispatchWorkersUsingParams():
    wsf_common.log(wsf_config.params.inputSources)
    for eachInputSource in wsf_config.params.inputSources:
        wsf_common.log(f"Dispatching Processing Of: {eachInputSource}")
        p = Process(
            target=scrapeWithConfigParams,
            args=(),
        )
        p.start()

@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def scrapeWithConfigParams():
    scraperClass = wsf_config.params.scraperClass
    scraperInstance = scraperClass()
    scraperInstance.scrape()
    wsf_results.resultsWrite(
        scraperInstance.urlResultsList,
        resultsSpec_format=wsf_config.params.resultsSpec_format,
    )
