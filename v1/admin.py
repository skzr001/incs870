from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from v1.models import AddFlight,Passenger, PayModel, Code, CustomUser


# Register your models here.
class AddFlightAdmin(admin.ModelAdmin):
    list_display=['airlines','number','From','To','Date','Time','Price','class_type']
admin.site.register( AddFlight, AddFlightAdmin)

class PassBookDet(admin.ModelAdmin):
    list_display=['user','fl_details','Pass_name','age','gender','book_time_date']
admin.site.register( Passenger, PassBookDet)

class Pay(admin.ModelAdmin):
    list_display=['user','fl_det','card_name','card_num','expiry_month','expiry_year','cvv_num']
admin.site.register(PayModel,Pay)

admin.site.register(Code)
admin.site.register(CustomUser)