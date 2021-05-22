from typing import Dict


class SerializerPerActionMixin:

    serializer_classes: Dict = {}

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, super().get_serializer_class())  # type:ignore
