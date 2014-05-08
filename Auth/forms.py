from wtforms import form, fields, validators
from shared.models import db
from models import User
from diceldap import ldap_login, AuthInvalidCredentialsException, AuthLdapServerErrorException

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])
    remember_me = fields.BooleanField('Remember me')

    def validate_login(self, field):
        try:
            user = self.get_user()    
            print(user)

        except AuthInvalidCredentialsException:
            raise validators.ValidationError('Wrong username or password')

        except AuthLdapServerErrorException as e:
            raise validators.ValidationError(str(e))

    def get_user(self):
        ldap_uname = ldap_login(self.login.data, self.password.data)
        return create_get_user_entry(ldap_uname, self.login.data)

class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')

def create_get_user_entry(ldap_uname, ldap_email):
    user = db.session.query(User).filter_by(login=ldap_uname, email=ldap_email).first()
    if not user:
        user = User()
        user.login = ldap_uname
        user.email = ldap_email
        
        db.session.add(user)
        db.session.commit()
        
    return user
    
