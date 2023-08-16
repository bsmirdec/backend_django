from rest_framework import serializers


class ChoiceDisplayField(serializers.Field):
    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return dict(self.choices).get(value)

    def to_internal_value(self, data):
        reverse_choices = dict((v, k) for k, v in self.choices)
        return reverse_choices.get(data)
