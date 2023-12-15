from django import forms
from domain.models import *


class SelectReference(forms.Form):
    my_dropdown = forms.ChoiceField(
        choices=[
            ('OrganizationalLegalForm', 'Организационно-правовые формы'),
            ('Skill', 'Навыки'),
            ('Specialization', 'Специализации'),
            ('SoftwareAndHardwareTool', 'Программно-технические средства'),
            ('WorkSchedule', 'Графики работы')
        ]
    )
