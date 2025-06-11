# core/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['STAFF', 'ADMIN']

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'
