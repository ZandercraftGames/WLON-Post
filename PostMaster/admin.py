from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from PostMaster.models import Nation, Package, Tracking, Subscriber

# Admin Site Properties
admin.site.site_title = "WL Post"
admin.site.site_header = "WLON Postmaster's Centre"
admin.site.index_title = "Postmaster's Centre"


# Inline Classes
class TrackingInline(admin.TabularInline):
    model = Tracking


# Register customization of admin panel for Subscriber
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    # Set uuid to be a readonly field.
    readonly_fields = ('uuid',)


# Register customization of admin panel for Tracking
@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    # Set package to be a readonly field.
    readonly_fields = ('package',)


# Register customization of admin panel for Package
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    # Inline editing for associated tracking model
    inlines = [
        TrackingInline
    ]


# Register models without custom Admin classes
admin.site.register(Nation)
