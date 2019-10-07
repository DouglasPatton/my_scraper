"""
Precipitation Details
"""


class Precipitation:

    # Current module version
    version = 0.1

    # HMS module description
    description = "Precipitation is one of the main processes in the global hydrological cycle, thus integral for " \
                  "modeling purposes. Precipitation is highly variable and influences vegetation, droughts, floods, " \
                  "and the movement of minerals and chemicals. In agriculture and urban areas, precipitation is the " \
                  "driver in contaminant and nutrient transport in water systems due to runoff. Precipitation data is " \
                  "an integral input for many watershed, air, erosion, and agricultural models as well as climate " \
                  "predicting projects. This data is used to determine flood/drought conditions, hydrologic " \
                  "transportation of contaminants, best management practices, and regulations. Precipitation data is " \
                  "generated through direct observation as well as model simulation."

    # Data source algorithms and brief description
    algorithms = {
        "NCDC Precipitation": "The National Climatic Data Center (NCDC) provides precipitation data recorded at rain "
                              "gauge stations. Stations are identified by their Station ID which includes the type of "
                              "station and the station number. Some stations have been recording data as far back as "
                              "1901 to present day.",
        "NLDAS Precipitation": "The North American Land Data Assimilation System (NLDAS) combines North American radar "
                               "data and satellite data from CMORPH. NLDAS has an hourly time step on a 0.125 -degree "
                               "grid of North America and has a maximum time lag of four days for data retrieval. Data "
                               "is available from January 2, 1979 to present",
        "GLDAS Precipitation": "The Global Land Data Assimilation System (GLDAS) combines satellite data and ground-based "
                               "observational data to provide precipitation and other variables on a spatial resolution of "
                               "0.25-degrees covering the Earth between December 2016.",
        "DAYMET Precipitation": "Daymet is a daily dataset of rain gauge data that has been interpolated and extrapolated. "
                                "Daymet uses ground station data with their model algorithm to produce gridded estimates "
                               "of daily weather parameters. The interpolated spatial resolution is about a 0.009-degree "
                                "grid over North America. Data is accessible since 1980 to the latest full year.",
        "PRISM Precipitation": "The Parameter-elevation Relationship on Independent Slopes Model (PRISM) is a combined "
                               "dataset consisting of ground gauge station and RADAR products. The data is on a 4km grid "
                               "resolution covering the contiguous United States. Data is available from 1981 to present.",
        "WGEN Precipitation": "WGEN is a stochastic weather generator that statistically simulates precipitation. WGEN "
                              "uses a Markov Chain Model to determine the probability of precipitation occurrence. The "
                              "Markov Chain Model determines precipitation by finding  the probability of a wet day "
                              "following a dry dat. Then an equation using mean daily rainfall, standard deviation of "
                              "daily rainfall, and skew coefficients give the amount of rainfall on a given wet day."
    }

    # Capabilities are provided as a list of capability descriptions, all html formatting must be included
    capabilities = ["Capability 1.", "Capability 2.", "Capability 3.", "Capability 4.", "Capability 5."]

    # Usage scenarios are structure as a key/value pair: the key is the title, and the value is a list containing
    # three elements: 0=Problem statement, 1=Desired Information, 2=Information Returned from Service
    usage = {"Usage Title 1": ["Problem Statement: NA 1.", "Desired Information: NA 1.", "Information Returned from Service: NA 1."]}

    # Sample Code are provided as a key/value pair: key is the code language, and value is the url to the code sample github
    samples = {
        "Python": "https://github.com/quanted/hms_api_samples/blob/master/python-sample/hms-api-simple-sample.py",
        "Java": "https://github.com/quanted/hms_api_samples/blob/master/java-sample/src/com/hms/JavaSample.java",
        "C#": "https://github.com/quanted/hms_api_samples/blob/master/csharp-sample/csharp-sample/HMSSample.cs"
    }

    # Input Parameters are provided as a list of lists, each list contains 4 elements: the parameter name, type,
    # description and any child elements.
    input_parameters = [
        ["source", "String", "Time-series data source (valid sources: nldas, gldas, daymet, ncei, prism, wgen, nwm)"],
        ["dateTimeSpan", "Dictionary", "Object holding the timeseries temporal input parameters "
                                       "(startDate, endDate, dateTimeFormat)"],
        ["startDate", "String", "Start date for the output timeseries."],
        ["endDate", "String", "End date for the output timeseries."],
        ["dateTimeFormat", "String", "Format of the datetime stamp of the output timeseries. Valid options can be found "
                                        "here: <a href=\"https://docs.microsoft.com/en-us/dotnet/api/system.datetime.tostring?view=netcore-2.2\" target=\"_blank\">Microsoft Documentation</a>"],
        ["geometry", "Dictionary", "Object holding the timeseries spatial input parameters. (point, stationID)"],
        ["point", "Dictionary", "Object holding point coordinate parameters. (latitude, longitude)"],
        ["latitude", "Number", "Latitude coordinate for the output timeseries."],
        ["longitude", "Number", "Longitude coordinate for the output timeseries."],
        ["stationID", "String", "NOAA NCEI station identification number.(Requires source to be set to 'ncei'."],
        ["dataValueFormat", "String", "Format of the output timeseries data values. Valid options can be found here: "
                                      "<a href=\"https://docs.microsoft.com/en-us/dotnet/api/system.double.tostring?view=netcore-2.2\" target=\"_blank\">Microsoft Documentation</a>"],
        ["temporalResolution", "String", "Temporal resolution/timestep of the output timeseries. Options are limited by the "
                                     "default timestep of the data source. All options are: 'default', 'daily', 'weekly', 'monthly'."],
        ["localTime", "Boolean", "Specify if the timestamp on the output timeseries is set to the timezone of the spatial area of interest."],
        ["units", "String", "Units of the output timeseries. Valid options are: 'default', 'metric', 'imperial'"],
        ["outputFormat", "String", "Format of the returned API object. Valid options are: 'json'."]
    ]

    # Output return object are provided as a list of lists, each list containing 3 elements: column,
    # datatype and description.
    output_object = [
        ["dataset", "String", "Primary dataset of the requested timeseries. Some API calls return more than one dataset, "
                             "either for a workflow API or other relevent dataset."],
        ["dataSource", "String", "Primary source of the requested timeseries."],
        ["metaData", "Dictionary", "Metadata for the output timeseries, includes metadata from the source as well "
                                   "as HMS metadata."],
        ["data", "Dictionary", "Output timeseries data is returned as a dictionary, where the key is the datetime stamp "
                               "and value is a list of values for the source/dataset."]
    ]

    # HTTP API endpoint
    http_API = [
        ["POST", "/hms/rest/api/v3/meteorology/precipitation/"]
    ]

    # Changelog is provided as a list of lists, where each list contains 3 elements: title, date, and a list of changes.
    changelog = [
        ["Version: 0.1 Beta", "May 29, 2019", ["Production UI and documentation initial setup."]]
    ]
