# admin_permissions_tester
Simple class helping to check permissions on Django's models

## What is it ?
In most of the projects I work on, I have multiple levels of admin rights. As I work with the TDD methodology, I try to always check the rights with automatic tests. But as the number of models and the number of admin levels grow, it can be unnecessarily time-consuming, pretty hard to maintain, and quite the opposite of DRY.
So I came up with this little class that I now use on every project, and it helps ensure the rights are what I want for one kind of user, on a specific model, for the 4 rights we may have (add, list, change, delete).

## How to use it ?
To use it, the easiest way is to create a fixture which creates an instance of the model we want to check the rights on (will be needed to check the "change" and the "delete" rights), and a user (with all the groups, "is_staff", "is_superuser", specific permission, etc., that you want).
Then, just use it like this :

`
from utils.admin_permissions_tester import AdminPermissionsTester


class ForumUserRightsTest(AdminPermissionsTester):
    fixtures = ['path/to/fixture.json']
    app = "my_app"
    model = 'my_model'
    right_to_add = False
    right_to_list = True
    right_to_change = True
    right_to_delete = False
`
This will work as is, as long as there is a model instance with 1 as pk, and the user's username is "staff_user".
If not, you can also write this:

`
class ForumUserRightsTest(AdminPermissionsTester):
    fixtures = ['path/to/fixture.json']
    app = "my_app"
    model = 'my_model'
    instance_to_check = 5
    username = "normal_user"
    right_to_add = False
    right_to_list = True
    right_to_change = False
    right_to_delete = False
`

Last possibility, if you prefer, you can make your class select the user instance directly, in a setUp or a setUpClass method (remember to call the super() method in that case).

Hope it will help someone !

Comments and improvements are welcome !

## Side note
As the class extends TestCase and has methods which names start with "test", it adds 4 ghost tests that are of no use. It doesn't really matter to me, but you can workaround it by making the class extend `object` instead of `TestCase`, and use the class like this : 
class ForumUserRightsTest(AdminPermissionsTester, TestCase):

Brice
