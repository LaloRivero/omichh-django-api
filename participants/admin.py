''' Participants admin config '''

# Django
from django.contrib import admin

# Models
from participants.models import Participant, School, Scores


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    ''' Display the participants data '''

    list_display = ['id',
                    'category',
                    'first_name',
                    'last_name',
                    'email',
                    'temp_user_name_omegaup']
    list_display_links = ['id','email']
    list_editable = ['first_name', 'last_name']
    search_fields = ['participant__category', 'email']
    list_filter = ['type_of_participant',
                   'category']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    ''' Display schools data '''

    list_display = ['id', 'name']
    list_display_links = ['id']
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Scores)
class ScoresAdmin(admin.ModelAdmin):
    ''' Display scores data '''

    list_display = ['id', 'test', 'score']
    list_display_links = ['id']
    list_editable = ['test', 'score']
    search_fields = ['test']