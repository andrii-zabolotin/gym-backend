from django_filters import rest_framework as filters


class StaffFilter(filters.FilterSet):
    group = filters.ChoiceFilter(field_name="groups", choices=[
        (1, "Тренери"),
        (2, "Масажисти"),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.data.copy()
        if 'group' not in self.data:
            self.data['group'] = 1
