#
"""
* Python Parameters Configuration For ClassicCarsApp.
* A series of intuitive functions that convey config params.
"""

from unisos.wsf import wsf_config

def classicCarsParams():

    wsf_config.scrapingName(
        name="OldClassicCars",
    )

    wsf_config.inputSources(
        urls=[
            "https://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591",
        ],
    )

    wsf_config.resultsSpec(
        baseDir="/tmp/RESULTS",
        resultsFormat="csv",
    )

    wsf_config.fieldsOfInterest(
        fields=[
            "id",
            "name",
            "date",
            "body"
        ]
    )

classicCarsParams()
