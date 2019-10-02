"""
HMS Workflow submodule Input form parameters
"""

from django import forms

# Sources for Precipitation
PRECIP_SOURCE_OPTIONS = (
('nldas', 'nldas'), ('gldas', 'gldas'), ('daymet', 'daymet'), ('wgen', 'wgen'), ('prism', 'prism'), ('ncdc', 'ncdc'), ('nwm', 'nwm'))

# Sources for Temperature
TEMP_SOURCE_OPTIONS = (('nldas', 'nldas'), ('gldas', 'gldas'), ('daymet', 'daymet'), ('prism', 'prism'))

# Sources for Wind
WIND_SOURCE_OPTIONS = (('nldas', 'nldas'), ('gldas', 'gldas'), ('ncei', 'ncei'))

# Sources for Radiation
RAD_SOURCE_OPTIONS = (('nldas', 'nldas'), ('gldas', 'gldas'), ('daymet', 'daymet'))

# Sources for Humidity
HUMID_SOURCE_OPTIONS = (('prism', 'prism'),)

# Standard List of sources
STANDARD_SOURCE_OPTIONS = (('nldas', 'nldas'), ('gldas', 'gldas'))

# Allowed Date formats for django form
DATE_INPUT_FORMATS = ('%Y-%m-%d', '%m-%d-%Y', '%m-%d-%y', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y',
                      '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y', '%d %B, %Y')


class HydrologyFormInput(forms.Form):
    source = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Data source of the dataset.'
        }),
        label='Source',
        choices=STANDARD_SOURCE_OPTIONS,
        initial='NLDAS'
    )
    startDate = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'datepicker'
        }),
        label='Start Date',
        input_formats=DATE_INPUT_FORMATS,
        initial='01/01/2010'
    )
    endDate = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'datepicker'
        }),
        label='End Date',
        input_formats=DATE_INPUT_FORMATS,
        initial='12/31/2010'
    )
    latitude = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'title': 'Latitude value for area of interest.'
        }),
        label='Latitude',
        initial=33.925575,
        required=False
    )
    longitude = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'title': 'Longitude value for area of interest.'
        }),
        label='Longitude',
        initial=-83.356893,
        required=False
    )
    # geometrymetadata = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'title': 'Metadata for the area of interest. Provide key-value "," separated list using ":" to separate key'
    #                  ' and value.',
    #     }),
    #     label='Geometry Metadata',
    #     required=False
    # )
    timelocalized = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Set date/time timezone to local, specified by latitude and longitude values, or to GMT.'
        }),
        label='Local Time',
        choices=(('false', 'no'), ('true', 'yes')),
        initial='true'
    )
    temporalresolution = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Temporal resolution of the output time series data.'
        }),
        label='Temporal Resolution',
        choices=(
        ("default", "default"), ("hourly", "hourly"), ("daily", "daily"), ("weekly", "weekly"), ("monthly", "monthly")),
        initial="default"
    )
    datetimeformat = forms.CharField(
        widget=forms.TextInput(attrs={
            'title': 'Valid date format strings can be found here https://docs.microsoft.com/en-us/dotnet/standard/'
                     'base-types/custom-date-and-time-format-strings'
        }),
        label='Output Date Format',
        initial="yyyy-MM-dd HH"
    )
    outputformat = forms.CharField(
        widget=forms.TextInput(attrs={
            'title': 'Valid data format string can be found here https://docs.microsoft.com/en-us/dotnet/standard/'
                     'base-types/standard-numeric-format-strings'
        }),
        label='Output Data Format',
        initial="E3"
    )


class PrecipitationFormInput(HydrologyFormInput):
    """
    Input form fields for precipitation data.
    default fields taken from HydrologyFormInput
    """
    source = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Data source of the dataset.'
        }),
        label='Source',
        choices=PRECIP_SOURCE_OPTIONS,
        initial='NLDAS'
    )
    stationID = forms.CharField(
        widget=forms.TextInput(attrs={
            'title': 'NCEI station ID.'
        }
        ),
        label='NCEI StationID',
        initial='GHCND:USW00013874'
    )
    field_order = ['source', 'startDate', 'endDate', 'latitude', 'longitude', 'stationID',
                   'geometrymetadata', 'timelocalized', 'temporalresolution', 'datetimeformat', 'outputformat']


class WindFormInput(HydrologyFormInput):
    """
    Input form fields for wind data.
    default fields taken from HydrologyFormInput
    """
    source = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Data source of the dataset.'
        }),
        label='Source',
        choices=WIND_SOURCE_OPTIONS,
        initial='NLDAS'
    )
    stationID = forms.CharField(
        widget=forms.TextInput(attrs={
            'title': 'NCEI station ID.'
        }
        ),
        label='NCEI StationID',
        initial='GHCND:USW00013874'
    )
    component = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Desired component of wind.'
        }),
        label='Component',
        choices=(('u/v', 'u/v'), ('vel/deg', 'vel/deg'), ('all', 'all')),
        initial='all'
    )


class TemperatureFormInput(HydrologyFormInput):
    """
    Input form fields for temperature data.
    default fields taken from HydrologyFormInput
    """
    source = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Data source of the dataset.'
        }),
        label='Source',
        choices=TEMP_SOURCE_OPTIONS,
        initial='NLDAS'
    )


class RadiationFormInput(HydrologyFormInput):
    """
    Input form fields for radiation data.
    default fields taken from HydrologyFormInput
    """
    source = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Data source of the dataset.'
        }),
        label='Source',
        choices=RAD_SOURCE_OPTIONS,
        initial='NLDAS'
    )


class HumidityFormInput(HydrologyFormInput):
    """
    Input form fields for humidity data.
    default fields taken from HydrologyFormInput
    """
    source = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Data source of the dataset.'
        }),
        label='Source',
        choices=HUMID_SOURCE_OPTIONS,
        initial='prism'
    )
    component = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Parameter: Relative Humidity/Dew Point Temperature'
        }),
        choices=(('relative', 'relative  humidity'), ('dewpoint', 'dew point')),
        initial='relative',
        label='Parameter',
    )
    field_order = ['source', 'component', 'startDate', 'endDate', 'latitude', 'longitude',
                   'geometrymetadata', 'timelocalized', 'temporalresolution', 'datetimeformat', 'outputformat']


class SolarcalculatorFormInput(forms.Form):
    model = forms.ChoiceField(
        widget=forms.Select(attrs={
            'title': 'Calculate for a year or day.'
        }),
        label='Model',
        choices=(('year', 'year'), ('day', 'day')),
        initial='year'
    )
    latitude = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'title': 'Latitude value for area of interest.'
        }),
        label='Latitude',
        initial=33.925575,
        required=False
    )
    longitude = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'title': 'Longitude value for area of interest.'
        }),
        label='Longitude',
        initial=-83.356893,
        required=False
    )
    timezone = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'title': 'Timezone for the specified location.'
        }),
        label='Time Zone',
        initial=-7,
        required=False
    )
    local_time = forms.CharField(
        widget=forms.TextInput(attrs={
            'title': 'Local time in hh:mm:ss format for the local time to use in the solar calculator.',
        }),
        label='Local Time',
        initial='12:00:00',
        required=False
    )
    year = forms.CharField(
        widget=forms.TextInput(attrs={
            'title': 'Year to run solar calculator.'
        }),
        label='Year',
        initial='2010',
        required=False
    )
    date = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'datepicker'
        }),
        label='Date',
        input_formats=DATE_INPUT_FORMATS,
        initial='2010-06-10'
    )
