from django.contrib import admin
from .models import Subscription, Video

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'is_approved', 'payment_id')
    list_filter = ('is_approved',)
    actions = ['approve_subscriptions']

    def approve_subscriptions(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected subscriptions have been approved.")
    approve_subscriptions.short_description = "Approve selected subscriptions"

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
