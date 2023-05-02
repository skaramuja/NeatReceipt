from accounts.models import Account


class EmailAuthBackEnd:
    def authenticate(self, request, username=None, password=None):
        """
        Method for authenticating a user.
        :param request: The HTTP request.
        :param username: The username.
        :param password: The password.
        :return: Returns the User if they provide valid credentials.
        """
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except(Account.DoesNotExist, Account.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Method for getting a user with the provided identifier.
        :param user_id: The unique identifier for the user to retrieve.
        :return: The User, if one exists with the provided identifier.
        """
        print('Attempting to get user')
        print(user_id)
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None