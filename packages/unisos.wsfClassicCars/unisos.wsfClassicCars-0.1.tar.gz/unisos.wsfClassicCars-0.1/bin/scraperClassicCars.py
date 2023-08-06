# -*- coding: utf-8 -*-
"""\
* ClassicCars concrete class, derived from the abstract wsf_scraperMultipage.ScraperMultipage.
"""

import typing

bpfInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
* Implements paging methods and Tags Predicates and Processors used by
* wsf_scraperMultipage.ScraperMultipage.scraper
"""], }

####+BEGIN: bx:bpf:py:name :style "fileName"
bpfInfo['moduleName'] = "scraperClassicCars"
####+END:

####+BEGIN: bx:bpf:py:version-timestamp :style "date"
bpfInfo['version'] = "202111215433"
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/bpfInfo-mbAgplShort.py"
bpfInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net/contact]]",],
}
####+END:

bpfInfo['credits'] = ""


import re

from unisos.wsf import wsf_common
from unisos.wsf import wsf_scraperMultipage

from unisos.wsf import wsf_config

class ClassicCarsParams:
    RegExp_PostDate = (
        '[a-zA-Z]{3} (?P<month>[a-zA-Z]{3}) (?P<day>[0-9]{1,2}), '
        '(?P<year>[0-9]{4}) (?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2}) (?P<ampm>am|pm)'
    )
    RegExp_PostEnd = 'No posts exist for this topic'


class ClassicCars(wsf_scraperMultipage.ScraperMultipage):
    """ClassicCars class for processing the likes of:
    https://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591

    This is a concrete class which is based on:
        - Abstract wsf_scraperMultipage.ScraperMultipage
        which is based on:
            -Abstract wsf_scraperBasic.ScraperBasic

    Provided methods are of type types:

    - Implementation Of Super Class Expected Methods
        _nextPage and _isEndOfUrl

    - Implementation Of Tags Predicates and Processors
        id, name, date, body
    """

    #
    # Implementation Of Super Class Expected Methods
    #
    def _nextPage(self):
        curPage = self.state['curPage']
        wsf_common.log(f'Processing page {curPage + 1}')
        self.stateSet('curPage', curPage + 1)
        self.stateSet('curInputSrc',
                       f'{self.root_source}&start={curPage * 15}')
        self.makeSoupForNewPage()

    def _isEndOfUrl(self, tag):
        condition1 = re.search(ClassicCarsParams.RegExp_PostEnd, tag.text)
        condition2 = tag.name == 'span'
        condition3 = wsf_common.tagHasClassname(tag, 'gen')
        return (condition1 and condition2 and condition3)

    #
    # Implementation Of Tags Predicates and Processors
    #
    def _is_id_tag(self, tag):
        condition1 = tag.name == 'span'
        condition2 = wsf_common.tagHasClassname(tag, 'name')
        return (condition1 and condition2)

    def _process_id(self, id_tag):
        return id_tag.find('a').attrs['name']

    def _is_name_tag(self, tag):
        # Same tag as id tag
        return self._is_id_tag(tag)

    def _process_name(self, name_tag):
        #return str(name_tag)
        return name_tag.find('b').text

    def _is_date_tag(self, tag):
        condition1 = tag.text.startswith('Posted')
        condition2 = tag.name == 'span'
        condition3 = wsf_common.tagHasClassname(tag, 'postdetails')
        return (condition1 and condition2 and condition3)

    def _process_date(self, date_tag):
        """Capture date."""
        try:
            result = re.search(ClassicCarsParams.RegExp_PostDate, date_tag.text)
        except TypeError:
            breakpoint()

        return result.group(0)

    def _is_body_tag(self, tag):
        condition1 = tag.name == 'span'
        condition2 = wsf_common.tagHasClassname(tag, 'postbody')
        condition3 = tag.text != ''
        return (condition1 and condition2 and condition3)

    def _process_body(self, body_tag):
        return body_tag.text


wsf_config.scrapingProcessor(
    scraperClass=ClassicCars,
)

####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
