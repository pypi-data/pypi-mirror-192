#!/bin/env python
# -*- coding: utf-8 -*-
"""\
* An Interactive Command Module (ICM): For running the ClassicCars Web Scraper.
"""

import typing

icmInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Description:* | ]]
**  This ICM is built on top of WSF (Web Scraping Framework)
**      [End-Of-Description]
"""], }

icmInfo['moduleUsage'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Usage:* | ]]

**      How-Tos: Run this icm as a command. Choose any of the presented lines
** which include -i scrape.
** Note: --load ./scraperClassicCars.py -- includes the scraper class code
** Note: --load ./classicCarsScraperParams.py  -- specifies run time parameters
**      [End-Of-Usage]
"""

icmInfo['moduleStatus'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  Current     :: Operational
**      [End-Of-Status]
"""

"""
*  [[elisp:(org-cycle)][| *ICM-INFO:* |]] :: Author, Copyleft and Version Information
"""
####+BEGIN: bx:icm:py:name :style "fileName"
icmInfo['moduleName'] = "icmClassicCarsWebScraper"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202110074450"
####+END:

####+BEGIN: bx:icm:py:status :status "Functional"
icmInfo['status']  = "Functional"
####+END:

icmInfo['credits'] = ""

####+BEGIN-NOT: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/icmInfo-mbNedaGplByStar.py"
icmInfo['authors'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
icmInfo['copyright'] = "Copyright 2021, [[http://www.neda.com][Neda Communications, Inc.]]"
icmInfo['licenses'] = "[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"
icmInfo['maintainers'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
icmInfo['contacts'] = "[[http://mohsen.1.banan.byname.net/contact]]"
icmInfo['partOf'] = "[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]"
####+END:

icmInfo['panel'] = "{}-Panel.org".format(icmInfo['moduleName'])
icmInfo['groupingType'] = "IcmGroupingType-pkged"
icmInfo['cmndParts'] = "IcmCmndParts[common] IcmCmndParts[param]"


####+BEGIN: bx:icm:python:top-of-file :partof "bystar" :copyleft "halaal+minimal"
"""
*  This file:/bisos/git/auth/bxRepos/bisos-pip/pals/py3/bin/aaRepoLiveParams.py :: [[elisp:(org-cycle)][| ]]
 is part of The Libre-Halaal ByStar Digital Ecosystem. http://www.by-star.net
 *CopyLeft*  This Software is a Libre-Halaal Poly-Existential. See http://www.freeprotocols.org
 A Python Interactively Command Module (PyICM).
 Best Developed With COMEEGA-Emacs And Best Used With Blee-ICM-Players.
 *WARNING*: All edits wityhin Dynamic Blocks may be lost.
"""
####+END:
####+BEGIN: bx:icm:python:topControls :partof "bystar" :copyleft "halaal+minimal"
"""
*  [[elisp:(org-cycle)][|/Controls/| ]] :: [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
"""
####+END:
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/pyWorkBench.org"
"""
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
"""
####+END:

####+BEGIN: bx:icm:python:icmItem :itemType "=Imports=" :itemTitle "*IMPORTS*"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Imports=  :: *IMPORTS*  [[elisp:(org-cycle)][| ]]
"""
####+END:


# import os
# import collections

from unisos.wsf import wsf_parallelProc

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmBleepG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
# G.icmLibsAppend = __file__
# G.icmCmndsLibsAppend = __file__

#from blee.icmPlayer import bleep
####+END:

g_importedCmndsModules = [       # Enumerate modules from which CMNDs become invokable
]


####+BEGIN: bx:dblock:python:section :title "Class Definitions"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Class Definitions*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "examples" :cmndType "ICM-Cmnd-FWrk"  :comment "FrameWrk: ICM Examples" :parsMand "" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd-FWrk :: /examples/ =FrameWrk: ICM Examples= parsMand= parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class examples(icm.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {}
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome

####+END:
        # def cpsInit(): return collections.OrderedDict()
        # def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
        # def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

        logControler = icm.LOG_Control()
        logControler.loggerSetLevel(20)

        icm.icmExampleMyName(G.icmMyName(), G.icmMyFullName())

        icm.G_commonBriefExamples()

        #bleep.examples_icmBasic()

        icm.cmndExampleMenuChapter(f"*Scrape Old Classic Cars*")

        examplesPlusLoads(
            loadFiles=[
                "classicCarsScraperParams.py",
                "scraperClassicCars.py",
            ],
        )

        return(cmndOutcome)


####+BEGIN: bx:icm:python:func :funcName "examplesPlusLoads" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "loadFiles"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-anyOrNone :: /examplesPlusLoads/ retType=bool argsList=(loadFiles)  [[elisp:(org-cycle)][| ]]
"""
def examplesPlusLoads(
    loadFiles,
):
####+END:
    """."""

    # def cpsInit(): return collections.OrderedDict()
    #def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
    # def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

    icm.cmndExampleMenuSection('/Load Files/ *scrape*')

    if loadFiles:
        loadArgs=""
        for each in loadFiles:
            loadArgs="""{loadArgs} --load {each}""".format(
                loadArgs=loadArgs,
                each=each,)
        thisCmndAction= " -i scrape"
        icm.cmndExampleMenuItem(format(f"{loadArgs} {thisCmndAction}"),
                                verbosity='none')
        icm.cmndExampleMenuItem(format(f"{loadArgs} {thisCmndAction}"),
                                verbosity='full')


####+BEGIN: bx:icm:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "scrape" :comment "" :parsMand "" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /scrape/ parsMand= parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class scrape(icm.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {}
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome

####+END:

        wsf_parallelProc.dispatchWorkersUsingParams()

        return cmndOutcome.set(
            opError=icm.OpError.Success,  #type: ignore
            opResults=None,
        )

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** TODO [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Place holder for this commands doc string.
"""



####+BEGIN: bx:icm:python:section :title "= =Framework::=   __main__ g_icmMain ="
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *= =Framework::=   __main__ g_icmMain =*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

if __name__ == "__main__":
    icm.g_icmMain(
        icmInfo=icmInfo,
        noCmndEntry=examples, # noCmndEntry=mainEntry,
        # extraParamsHook=g_paramsExtraSpecify,
        importedCmndsModules=g_importedCmndsModules,
    )

####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
