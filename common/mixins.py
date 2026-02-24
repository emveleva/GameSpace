class DisableFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "fields"):
            for field in self.fields.values():
                field.disabled = True