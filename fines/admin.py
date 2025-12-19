from django.contrib import admin

from .models import Fine


# Fines admin is hidden from UI menu
# Uncomment below to show in admin again
# @admin.register(Fine)
# class MemberAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "borrowed_book",
#         "member_id",
#         "amount",
#     )
