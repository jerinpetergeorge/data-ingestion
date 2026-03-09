class EnumChoiceMixin:
    @classmethod
    def choices(cls) -> list[str]:
        return [item.name for item in cls]
