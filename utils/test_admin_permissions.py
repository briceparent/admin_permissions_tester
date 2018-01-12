from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPermissionsTester(TestCase):
    """
    Unit tests for permissions in the admin site. Requires to be applied to a SharedBaseTest instance.

    Example: class MyModelRightsTest(AdminPermissionsFixture, SharedBaseTest):
        fixtures = ['appname/tests/admin_permissions_fixtures.json']  # A fixture creating 1 instance of myapp.mymodel
        app: "myapp"  # The name of the app you want to test
        model: "myapp.mymodel"  # The name of the model you want to test, in lowercase (as the db table)
        instance_to_check: 1  # The pk of an instance existing in the db (created by the fixture)
        user:  None  # The user object that should be checked
        username:  None  # The username of the user that should be checked (if `user` is not set only)

        right_to_add: False  # Set to True if you want to grant this access, False (default) otherwise.
        right_to_list: True  # Set to True if you want to grant this access, False (default) otherwise.
        right_to_change: True  # Set to True if you want to grant this access, False (default) otherwise.
        right_to_delete: False  # Set to True if you want to grant this access, False (default) otherwise.
    """
    fixtures = None
    app = "your_app_name"
    model = 'your_model_name_in_db'
    instance_to_check = 1
    user = None
    username = "staff_user"

    right_to_add = False
    right_to_list = False
    right_to_change = False
    right_to_delete = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.user is None and cls.fixtures is not None:
            cls.user = get_user_model().objects.get(username=cls.username)

    def test_check_right_to_add(self):
        self._check_one_right('add', granted=self.right_to_add)

    def test_check_right_to_list(self):
        self._check_one_right('changelist', granted=self.right_to_list)

    def test_check_right_to_change(self):
        self._check_one_right('change', granted=self.right_to_change)

    def test_check_right_to_delete(self):
        self._check_one_right('delete', granted=self.right_to_delete)

    def _check_one_right(self, right, granted=False):
        if self.fixtures is None:
            # There are no test to launch here, the class should be extended
            return

        if granted:
            self._assert_has_access_to_admin(right)
        else:
            self._assert_has_no_access_to_admin(right)

    def _assert_has_access_to_admin(self, right):
        response, redirected_to_connect_page = self._get_admin_page_response(right)

        self.assertFalse(redirected_to_connect_page, 'A manager should not have been redirected to connection page.')
        if not redirected_to_connect_page:
            self.assertEqual(response.status_code, 200, 'A manager should have {}.'.format(
                self._last_checked_right))

    def _assert_has_no_access_to_admin(self, right):
        response, redirected_to_connect_page = self._get_admin_page_response(right)

        if not redirected_to_connect_page:
            self.assertIn(response.status_code, [403, 404], 'A manager should not have {}.'.format(
                self._last_checked_right))

    def _get_admin_page_response(self, right):
        self._last_checked_right = '"{}" access on {}:{}'.format(right, self.app, self.model)
        self.assertIn(right, ['changelist', 'add', 'history', 'delete', 'change'], 'Right not recognized')
        self.client.force_login(self.user)

        page_code = "admin:{}_{}_{}".format(self.app, self.model, right)
        if right in ['changelist', 'add']:
            page = reverse(page_code)
        else:
            page = reverse(page_code, args=(self.instance_to_check,))

        connect_page = False
        response = self.client.get(page, follow=True)
        if response.wsgi_request.path != page and response.wsgi_request.path == "/admin/login/":
            connect_page = True

        return response, connect_page
