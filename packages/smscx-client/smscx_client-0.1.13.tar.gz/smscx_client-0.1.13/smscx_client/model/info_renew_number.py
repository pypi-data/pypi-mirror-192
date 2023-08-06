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



class InfoRenewNumber(ModelNormal):


    allowed_values = {
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
        return {
            'rent_id': (str,),  # noqa: E501
            'number_id': (str,),  # noqa: E501
            'phone_number': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'rent_start': (datetime,),  # noqa: E501
            'rent_end': (datetime,),  # noqa: E501
            'rent_cost': (float,),  # noqa: E501
            'auto_renew': (bool,),  # noqa: E501
            'callback_url': (str, none_type,),  # noqa: E501
            'datetime': (datetime,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'rent_id': 'rentId',  # noqa: E501
        'number_id': 'numberId',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'rent_start': 'rentStart',  # noqa: E501
        'rent_end': 'rentEnd',  # noqa: E501
        'rent_cost': 'rentCost',  # noqa: E501
        'auto_renew': 'autoRenew',  # noqa: E501
        'callback_url': 'callbackUrl',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, rent_id, number_id, phone_number, country_iso, rent_start, rent_end, rent_cost, auto_renew, callback_url, datetime, *args, **kwargs):  # noqa: E501
        """InfoRenewNumber - a model

        Args:
            rent_id (str): Unique identifier of the rent operation
            number_id (str): Unique identifier of phone number
            phone_number (str): Rented phone number in international E.164 format
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard. Eg. `DE`, `FR`, `IT`
            rent_start (datetime): Start date and time of the rent period (UTC)
            rent_end (datetime): End date and time of the rent period (UTC)
            rent_cost (float): Cost of renting the phone number
            auto_renew (bool): Automatically renews the rent for the number with the same period as the current subscription
            callback_url (str, none_type): Callback URL (or webhook) to get the SMS that is received on the rented phone number (inbound SMS)
            datetime (datetime):


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
        self.rent_start = rent_start
        self.rent_end = rent_end
        self.rent_cost = rent_cost
        self.auto_renew = auto_renew
        self.callback_url = callback_url
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
    def __init__(self, rent_id, number_id, phone_number, country_iso, rent_start, rent_end, rent_cost, auto_renew, callback_url, datetime, *args, **kwargs):  # noqa: E501
        """InfoRenewNumber - a model

        Args:
            rent_id (str): Unique identifier of the rent operation
            number_id (str): Unique identifier of phone number
            phone_number (str): Rented phone number in international E.164 format
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard. Eg. `DE`, `FR`, `IT`
            rent_start (datetime): Start date and time of the rent period (UTC)
            rent_end (datetime): End date and time of the rent period (UTC)
            rent_cost (float): Cost of renting the phone number
            auto_renew (bool): Automatically renews the rent for the number with the same period as the current subscription
            callback_url (str, none_type): Callback URL (or webhook) to get the SMS that is received on the rented phone number (inbound SMS)
            datetime (datetime):


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
        self.rent_start = rent_start
        self.rent_end = rent_end
        self.rent_cost = rent_cost
        self.auto_renew = auto_renew
        self.callback_url = callback_url
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
