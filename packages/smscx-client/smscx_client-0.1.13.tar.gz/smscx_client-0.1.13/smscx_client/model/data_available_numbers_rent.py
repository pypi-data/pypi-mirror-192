import re  # noqa: F401
import sys  # noqa: F401

from smscx_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    ApiModel
)
from smscx_client.exceptions import ApiAttributeError


def lazy_import():
    from smscx_client.model.rent_cost import RentCost
    globals()['RentCost'] = RentCost


class DataAvailableNumbersRent(ModelNormal):


    allowed_values = {
        ('number_type',): {
            'MOBILE': "mobile",
            'LANDLINE': "landline",
        },
        ('min_rent',): {
            '1': 1,
            '7': 7,
            '30': 30,
        },
        ('setup_time',): {
            'INSTANT': "instant",
            'DELAYED': "delayed",
        },
    }

    validations = {
        ('number_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
        ('country_iso',): {
            'max_length': 2,
            'min_length': 2,
        },
    }

    additional_properties_type = None

    _nullable = False

    @cached_property
    def api_types():
        """
        Returns
            api_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'number_id': (str,),  # noqa: E501
            'phone_number': (str, none_type,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'network_operator': (str,),  # noqa: E501
            'features': (int,),  # noqa: E501
            'number_type': (str,),  # noqa: E501
            'inbound_sms_cost': (float,),  # noqa: E501
            'outbound_sms_cost': (float, none_type,),  # noqa: E501
            'setup_cost': (float,),  # noqa: E501
            'rent_cost': ([RentCost],),  # noqa: E501
            'min_rent': (int,),  # noqa: E501
            'setup_time': (str,),  # noqa: E501
            'registration': (bool,),  # noqa: E501
            'datetime': (datetime,),  # noqa: E501
            'inbound_sms_sender': (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'number_id': 'numberId',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'network_operator': 'networkOperator',  # noqa: E501
        'features': 'features',  # noqa: E501
        'number_type': 'numberType',  # noqa: E501
        'inbound_sms_cost': 'inboundSmsCost',  # noqa: E501
        'outbound_sms_cost': 'outboundSmsCost',  # noqa: E501
        'setup_cost': 'setupCost',  # noqa: E501
        'rent_cost': 'rentCost',  # noqa: E501
        'min_rent': 'minRent',  # noqa: E501
        'setup_time': 'setupTime',  # noqa: E501
        'registration': 'registration',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
        'inbound_sms_sender': 'inboundSmsSender',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, number_id, phone_number, country_iso, network_operator, features, number_type, inbound_sms_cost, outbound_sms_cost, setup_cost, rent_cost, min_rent, setup_time, registration, datetime, *args, **kwargs):  # noqa: E501
        """DataAvailableNumbersRent - a model

        Args:
            number_id (str): Unique identifier of phone number
            phone_number (str, none_type): Phone number in international E.164 format. In some cases this value might be `null` as the phone number will be selected random from a pool of numbers
            country_iso (str): Two-letter country ISO of the phone number
            network_operator (str): Network operator of the phone number
            features (int): Sum of features of the phone number, in numerical value. The following are the corresponding values for each feature:  - `1` for receiving SMS (inbound SMS)  - `2` for sending SMS (outbound SMS)  - `4` for voice.      <br> <br>  A phone number with feature `1` can only receive SMS, with feature `2` can only send SMS, and with feature value `3` (1 + 2) cand send and receive SMS
            number_type (str): Type of phone number
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this has value 0)
            outbound_sms_cost (float, none_type): Cost for sending a SMS from this phone number. If the number doesn't have outbound SMS as a feature, this parameter will be `null`
            setup_cost (float): One time setup fee for the rented phone number (if applicable)
            rent_cost ([RentCost]): Array of objects with cost for every period (in days). If the phone number has a minimum rent period of 30 days, this array will contain only one object with cost for 30 days. If minimum rent is 1 day, then this array will contain 3 objects with cost for 1, 7, 30 days
            min_rent (int): Minimum period that this phone number must be rented (in days)
            setup_time (str): The time to setup the number. instant - the number is available immediately, delayed - the number will be available after a period of time (between 10 minutes and few days)
            registration (bool): Indicates if the phone number requires registration
            datetime (datetime):
            inbound_sms_sender (bool): Indicates if the phone number can receive SMS from alphanumeric sender ID. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(ApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.number_id = number_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.features = features
        self.number_type = number_type
        self.inbound_sms_cost = inbound_sms_cost
        self.outbound_sms_cost = outbound_sms_cost
        self.setup_cost = setup_cost
        self.rent_cost = rent_cost
        self.min_rent = min_rent
        self.setup_time = setup_time
        self.registration = registration
        self.datetime = datetime
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, number_id, phone_number, country_iso, network_operator, features, number_type, inbound_sms_cost, outbound_sms_cost, setup_cost, rent_cost, min_rent, setup_time, registration, datetime, *args, **kwargs):  # noqa: E501
        """DataAvailableNumbersRent - a model

        Args:
            number_id (str): Unique identifier of phone number
            phone_number (str, none_type): Phone number in international E.164 format. In some cases this value might be `null` as the phone number will be selected random from a pool of numbers
            country_iso (str): Two-letter country ISO of the phone number
            network_operator (str): Network operator of the phone number
            features (int): Sum of features of the phone number, in numerical value. The following are the corresponding values for each feature:  - `1` for receiving SMS (inbound SMS)  - `2` for sending SMS (outbound SMS)  - `4` for voice.      <br> <br>  A phone number with feature `1` can only receive SMS, with feature `2` can only send SMS, and with feature value `3` (1 + 2) cand send and receive SMS
            number_type (str): Type of phone number
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this has value 0)
            outbound_sms_cost (float, none_type): Cost for sending a SMS from this phone number. If the number doesn't have outbound SMS as a feature, this parameter will be `null`
            setup_cost (float): One time setup fee for the rented phone number (if applicable)
            rent_cost ([RentCost]): Array of objects with cost for every period (in days). If the phone number has a minimum rent period of 30 days, this array will contain only one object with cost for 30 days. If minimum rent is 1 day, then this array will contain 3 objects with cost for 1, 7, 30 days
            min_rent (int): Minimum period that this phone number must be rented (in days)
            setup_time (str): The time to setup the number. instant - the number is available immediately, delayed - the number will be available after a period of time (between 10 minutes and few days)
            registration (bool): Indicates if the phone number requires registration
            datetime (datetime):
            inbound_sms_sender (bool): Indicates if the phone number can receive SMS from alphanumeric sender ID. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.number_id = number_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.features = features
        self.number_type = number_type
        self.inbound_sms_cost = inbound_sms_cost
        self.outbound_sms_cost = outbound_sms_cost
        self.setup_cost = setup_cost
        self.rent_cost = rent_cost
        self.min_rent = min_rent
        self.setup_time = setup_time
        self.registration = registration
        self.datetime = datetime
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_api_data` to instantiate "
                                     f"class with read only attributes.")
