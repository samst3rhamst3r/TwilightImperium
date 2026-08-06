from enum import StrEnum

class NotLowerCasedValueError(ValueError):
    pass

class MissingEnumMemberError(ValueError):
    pass

class GameStrEnum(StrEnum):

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

class ConfigEnum(GameStrEnum):

    @classmethod
    def _missing_(cls, value):
        if value.lower() in cls.__members__.values():
            raise NotLowerCasedValueError(f"'{value}' is not lower-cased for this configuration data enum type {cls.__name__}. All configuration data enum IDs must be lower-cased as read in from configuration files.")
        raise MissingEnumMemberError(f"Invalid value for {cls.__name__}: {value}. Valid values include: {list(cls.__members__.values())}")

