from pydoc import locate
from uuid import UUID
import os


class Validator:
    def __init__(self, parameters: list, parameters_validation: dict = None):
        self.parameters = parameters
        self.parameters_validation = parameters_validation

    def validate(self, data: dict):
        if data is None or data is {}:
            return {
                "error": True,
                "message": "({}) is not exists".format(", ".join(self.parameters))
            }
        for p in self.parameters:
            if p not in data:
                return {"error": True, "message": "{} is not exists".format(p)}
            if self.parameters_validation is not None and p in self.parameters_validation:
                result = self.__run_validator__(p, data[p], self.parameters_validation[p])
                return result
        return {"error": False}

    def __run_validator__(self, key, value, validate_parameters: dict):
        if 'type' in validate_parameters:
            value_type = locate(validate_parameters['type'])
            if not isinstance(value, value_type):
                return {
                    "error": True,
                    "message": "{} should be {}".format(key, validate_parameters['type'])
                }

        if 'min' in validate_parameters:
            if isinstance(value, int) or isinstance(value, float):
                if int(value) < int(validate_parameters['min']):
                    return {
                        "error": True,
                        "message": "{} should be >= {}".format(key, validate_parameters['min'])
                    }
            else:
                if len(value) < int(validate_parameters['min']):
                    return {
                        "error": True,
                        "message": "len of {} should be >= {}".format(key, validate_parameters['min'])
                    }

        if 'max' in validate_parameters:
            if isinstance(value, int) or isinstance(value, float):
                if int(value) > int(validate_parameters['max']):
                    return {
                        "error": True,
                        "message": "{} should be < {}".format(key, validate_parameters['max'])
                    }
            else:
                if len(value) > int(validate_parameters['max']):
                    return {
                        "error": True,
                        "message": "len of {} should be < {}".format(key, validate_parameters['max'])
                    }

        if 'handler' in validate_parameters:
            result = validate_parameters['handler'](value)
            if not result:
                return {
                    "error": True,
                    "message": "{} is invalid format".format(key)
                }

        return {"error": False}

    @staticmethod
    def is_uuid(value):
        try:
            uuid_obj = UUID(value)
        except ValueError:
            return False

        return str(uuid_obj) == value

    @staticmethod
    def is_mobile_number(value):
        if len(value) is not 11:
            return False

        if not str(value).startswith('0'):
            return False

        start_number = int(value[1:4])

        if 935 <= start_number <= 939:
            return True

        if 910 <= start_number <= 919:
            return True
        if start_number == 991 or start_number == 990 or start_number == 931:
            return True
        if start_number == 934 or start_number == 933 or start_number == 930 or start_number == 932:
            return True
        if 901 <= start_number <= 905:
            return True

        if 920 <= start_number <= 922:
            return True

        return False

    @staticmethod
    def is_correct_path(value):
        return os.path.exists(value)




