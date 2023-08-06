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
    from smscx_client.model.inbound_sms import InboundSms
    from smscx_client.model.outbound_sms import OutboundSms
    from smscx_client.model.renew_cost import RenewCost
    globals()['InboundSms'] = InboundSms
    globals()['OutboundSms'] = OutboundSms
    globals()['RenewCost'] = RenewCost


class InfoRentStatus(ModelNormal):


    allowed_values = {
        ('number_type',): {
            'MOBILE': "mobile",
            'LANDLINE': "landline",
        },
        ('rent_period',): {
            '1': 1,
            '7': 7,
            '30': 30,
        },
        ('min_rent',): {
            '1': 1,
            '7': 7,
            '30': 30,
        },
    }

    validations = {
        ('rent_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
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
            'rent_id': (str,),  # noqa: E501
            'number_id': (str,),  # noqa: E501
            'phone_number': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'network_operator': (str,),  # noqa: E501
            'features': (int,),  # noqa: E501
            'number_type': (str,),  # noqa: E501
            'rent_cost': (float,),  # noqa: E501
            'setup_cost': (float,),  # noqa: E501
            'rent_period': (int,),  # noqa: E501
            'rent_start': (datetime,),  # noqa: E501
            'rent_end': (datetime,),  # noqa: E501
            'inbound_sms_cost': (float,),  # noqa: E501
            'outbound_sms_cost': (float, none_type,),  # noqa: E501
            'renew_cost': ([RenewCost],),  # noqa: E501
            'inbound_sms': (InboundSms,),  # noqa: E501
            'outbound_sms': (OutboundSms,),  # noqa: E501
            'min_rent': (int,),  # noqa: E501
            'callback_url': (str, none_type,),  # noqa: E501
            'auto_renew': (bool,),  # noqa: E501
            'active_rent': (bool,),  # noqa: E501
            'approved': (bool,),  # noqa: E501
            'datetime': (datetime,),  # noqa: E501
            'inbound_sms_sender': (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'rent_id': 'rentId',  # noqa: E501
        'number_id': 'numberId',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'network_operator': 'networkOperator',  # noqa: E501
        'features': 'features',  # noqa: E501
        'number_type': 'numberType',  # noqa: E501
        'rent_cost': 'rentCost',  # noqa: E501
        'setup_cost': 'setupCost',  # noqa: E501
        'rent_period': 'rentPeriod',  # noqa: E501
        'rent_start': 'rentStart',  # noqa: E501
        'rent_end': 'rentEnd',  # noqa: E501
        'inbound_sms_cost': 'inboundSmsCost',  # noqa: E501
        'outbound_sms_cost': 'outboundSmsCost',  # noqa: E501
        'renew_cost': 'renewCost',  # noqa: E501
        'inbound_sms': 'inboundSms',  # noqa: E501
        'outbound_sms': 'outboundSms',  # noqa: E501
        'min_rent': 'minRent',  # noqa: E501
        'callback_url': 'callbackUrl',  # noqa: E501
        'auto_renew': 'autoRenew',  # noqa: E501
        'active_rent': 'activeRent',  # noqa: E501
        'approved': 'approved',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
        'inbound_sms_sender': 'inboundSmsSender',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, rent_id, number_id, phone_number, country_iso, network_operator, features, number_type, rent_cost, setup_cost, rent_period, rent_start, rent_end, inbound_sms_cost, outbound_sms_cost, renew_cost, inbound_sms, outbound_sms, min_rent, callback_url, auto_renew, active_rent, approved, datetime, *args, **kwargs):  # noqa: E501
        """InfoRentStatus - a model

        Args:
            rent_id (str): Unique identifier of the rent operation
            number_id (str): Unique identifier of the phone number
            phone_number (str): Phone number that is rented in international E.164 format
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard. Eg. `DE`, `FR`, `IT`
            network_operator (str): Network operator of the phone number
            features (int): Sum of features of the phone number, in numerical value. The following are the corresponding values for each feature:  - `1` for receiving SMS (inbound SMS)  - `2` for sending SMS (outbound SMS)  - `4` for voice.      <br> <br>  A phone number with feature `1` can only receive SMS, with feature `2` can only send SMS, and with feature value `3` (1 + 2) cand send and receive SMS
            number_type (str): Type of phone number.
            rent_cost (float): Cost of renting the phone number for the current period
            setup_cost (float): The one time setup fee that was charged at the initial rent of the phone number (if applicable)
            rent_period (int): Current period of the phone number rent (in days)
            rent_start (datetime): Start date and time of the rent period (UTC)
            rent_end (datetime): End date and time of the rent period (UTC)
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this has value 0)
            outbound_sms_cost (float, none_type): Cost for sending a SMS from this phone number. If the number doesn't have outbound SMS as a feature, this parameter will be `null`
            renew_cost ([RenewCost]): Array of objects with cost for rent renewal. If the number has minimum rent period of 30 days, this array will contain only one object with 30 days
            inbound_sms (InboundSms):
            outbound_sms (OutboundSms):
            min_rent (int): Minimum period that this phone number can be rented/renewed (in days)
            callback_url (str, none_type): Callback URL (or webhook) to get the SMS received on the rented phone number (inbound SMS)
            auto_renew (bool): Automatically renews the rent for the number with the same period as the current subscription
            active_rent (bool): Indicates if the rent is active (not canceled or subscription not expired)
            approved (bool): If the phone number requires registration, this parameter indicates if the phone number was approved. Value `true` means number approved, `false` means processing
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

        self.rent_id = rent_id
        self.number_id = number_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.features = features
        self.number_type = number_type
        self.rent_cost = rent_cost
        self.setup_cost = setup_cost
        self.rent_period = rent_period
        self.rent_start = rent_start
        self.rent_end = rent_end
        self.inbound_sms_cost = inbound_sms_cost
        self.outbound_sms_cost = outbound_sms_cost
        self.renew_cost = renew_cost
        self.inbound_sms = inbound_sms
        self.outbound_sms = outbound_sms
        self.min_rent = min_rent
        self.callback_url = callback_url
        self.auto_renew = auto_renew
        self.active_rent = active_rent
        self.approved = approved
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
    def __init__(self, rent_id, number_id, phone_number, country_iso, network_operator, features, number_type, rent_cost, setup_cost, rent_period, rent_start, rent_end, inbound_sms_cost, outbound_sms_cost, renew_cost, inbound_sms, outbound_sms, min_rent, callback_url, auto_renew, active_rent, approved, datetime, *args, **kwargs):  # noqa: E501
        """InfoRentStatus - a model

        Args:
            rent_id (str): Unique identifier of the rent operation
            number_id (str): Unique identifier of the phone number
            phone_number (str): Phone number that is rented in international E.164 format
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard. Eg. `DE`, `FR`, `IT`
            network_operator (str): Network operator of the phone number
            features (int): Sum of features of the phone number, in numerical value. The following are the corresponding values for each feature:  - `1` for receiving SMS (inbound SMS)  - `2` for sending SMS (outbound SMS)  - `4` for voice.      <br> <br>  A phone number with feature `1` can only receive SMS, with feature `2` can only send SMS, and with feature value `3` (1 + 2) cand send and receive SMS
            number_type (str): Type of phone number.
            rent_cost (float): Cost of renting the phone number for the current period
            setup_cost (float): The one time setup fee that was charged at the initial rent of the phone number (if applicable)
            rent_period (int): Current period of the phone number rent (in days)
            rent_start (datetime): Start date and time of the rent period (UTC)
            rent_end (datetime): End date and time of the rent period (UTC)
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this has value 0)
            outbound_sms_cost (float, none_type): Cost for sending a SMS from this phone number. If the number doesn't have outbound SMS as a feature, this parameter will be `null`
            renew_cost ([RenewCost]): Array of objects with cost for rent renewal. If the number has minimum rent period of 30 days, this array will contain only one object with 30 days
            inbound_sms (InboundSms):
            outbound_sms (OutboundSms):
            min_rent (int): Minimum period that this phone number can be rented/renewed (in days)
            callback_url (str, none_type): Callback URL (or webhook) to get the SMS received on the rented phone number (inbound SMS)
            auto_renew (bool): Automatically renews the rent for the number with the same period as the current subscription
            active_rent (bool): Indicates if the rent is active (not canceled or subscription not expired)
            approved (bool): If the phone number requires registration, this parameter indicates if the phone number was approved. Value `true` means number approved, `false` means processing
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

        self.rent_id = rent_id
        self.number_id = number_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.features = features
        self.number_type = number_type
        self.rent_cost = rent_cost
        self.setup_cost = setup_cost
        self.rent_period = rent_period
        self.rent_start = rent_start
        self.rent_end = rent_end
        self.inbound_sms_cost = inbound_sms_cost
        self.outbound_sms_cost = outbound_sms_cost
        self.renew_cost = renew_cost
        self.inbound_sms = inbound_sms
        self.outbound_sms = outbound_sms
        self.min_rent = min_rent
        self.callback_url = callback_url
        self.auto_renew = auto_renew
        self.active_rent = active_rent
        self.approved = approved
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
