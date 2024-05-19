from wtforms import Form,StringField,ValidationError,BooleanField,FileField
from wtforms.validators import Email,EqualTo,Length
from flask_wtf.file import FileAllowed
from exts import cache
from models.user import UserModel
from .baseform import BaseForm

class RegisterForm(BaseForm):
  email = StringField(validators=[Email(message="input the email！")])
  #captcha = StringField(validators=[Length(min=4,max=4,message="input the verification！")])
  username = StringField(validators=[Length(min=2,max=20,message="input the user name！")])
  password = StringField(validators=[Length(min=6,max=20,message="input the password！6-20 chars")])
  confirm_password = StringField(validators=[EqualTo("password",message="Two passwords do not match！")])

  def validate_email(self,field):
    email = field.data
    user = UserModel.query.filter_by(email=email).first()
    if user:
      raise ValidationError(message="Email already exists")

  '''
  def validate_captcha(self,field):
    captcha = field.data
    email = self.email.data
    cache_captcha = cache.get(email)
    #if cache_captcha is None:
    #  cache.set(email,email)
    if not cache_captcha or captcha != cache_captcha:
      raise ValidationError(message="Verification code error！")
  '''

class LoginForm(BaseForm):
  email = StringField(validators=[Email(message="input the email！")])
  password = StringField(validators=[Length(min=6, max=20, message="input the password！")])
  remember = BooleanField()


class EditProfileForm(BaseForm):
  username = StringField(validators=[Length(min=2,max=20,message="input the user name！")])
  avatar = FileField(validators=[FileAllowed(['jpg','jpeg','png'],message="file type error！")])
  signature = StringField()

  def validate_signature(self,field):
    signature = field.data
    if signature and len(signature) > 100:
      raise ValidationError(message="signature must not be longer then 100 characters")