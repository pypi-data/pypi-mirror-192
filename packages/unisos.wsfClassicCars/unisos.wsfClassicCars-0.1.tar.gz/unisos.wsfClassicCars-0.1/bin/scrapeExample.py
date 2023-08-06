#!/bin/env python
# -*- coding: utf-8 -*-
"""\
* A very simple example that shows how OldClassicCars App can be dispatched.
** Real command-line interface is: ./icmClassicCarsWebScraper.py
** The first two imports, load the class and config files.
"""

import classicCarsScraperParams
import scraperClassicCars

from unisos.wsf import wsf_parallelProc

if __name__ == '__main__':
    wsf_parallelProc.dispatchWorkersUsingParams()
