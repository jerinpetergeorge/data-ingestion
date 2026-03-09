class EnumChoiceMixin:
    """
    Mixin class for enum to provide a method to get the list of choices.
    """

    @classmethod
    def choices(cls) -> list[str]:
        return [item.name for item in cls]
