from utils.admin_permissions_tester import AdminPermissionsTester


class ForumUserRightsTest(AdminPermissionsTester):
    fixtures = ['forum/tests/admin_permissions_fixtures.json']
    app = "forum"
    model = 'forumuser'
    right_to_add = False
    right_to_list = True
    right_to_change = True
    right_to_delete = False


class CategoryRightsTest(AdminPermissionsTester):
    fixtures = ['forum/tests/admin_permissions_fixtures.json']
    app = "forum"
    model = 'forumcategory'
    right_to_add = False
    right_to_list = True
    right_to_change = True
    right_to_delete = False


class SubCategoryRightsTest(AdminPermissionsTester):
    fixtures = ['forum/tests/admin_permissions_fixtures.json']
    app = "forum"
    model = 'forumsubcategory'
    right_to_add = False
    right_to_list = True
    right_to_change = True
    right_to_delete = False


class TopicRightsTest(AdminPermissionsTester):
    fixtures = ['forum/tests/admin_permissions_fixtures.json']
    app = "forum"
    model = 'forumtopic'
    right_to_add = True
    right_to_list = True
    right_to_change = True
    right_to_delete = True


class PostRightsTest(AdminPermissionsTester):
    fixtures = ['forum/tests/admin_permissions_fixtures.json']
    app = "forum"
    model = 'forumpost'
    right_to_add = True
    right_to_list = True
    right_to_change = True
    right_to_delete = True
