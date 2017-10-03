from django.contrib import admin

# Register your models here.
from .models import User,Portfolio,Transaction,Pending,History,Stock_data,Old_Stock_data

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(Transaction)
admin.site.register(Pending)
admin.site.register(History)
admin.site.register(Stock_data)
admin.site.register(Old_Stock_data)