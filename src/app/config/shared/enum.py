import enum

@enum.unique
class App_StrEnum(enum.StrEnum):

  @classmethod
  def _missing_(cls, value: str):
    adj_val = '_'.join(s.upper() for s in value.split())
    if adj_val not in cls._member_names_:
        raise ValueError(f"Invalid value '{value}' for enum '{cls.__name__}'")
    return cls(adj_val)