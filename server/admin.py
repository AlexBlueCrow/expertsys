from django.contrib import admin

# Register your models here.

from .models import AppUser,Domain,ExpertInfo,Project,Group,ExpertToGroup,CredentialImage,Key

admin.site.register([AppUser,Domain,ExpertInfo,Project,Group,ExpertToGroup,CredentialImage,Key])
