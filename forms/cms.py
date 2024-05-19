from .baseform import BaseForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import Email, InputRequired, Length


class AddStaffForm(BaseForm):
  email = StringField(validators=[Email(message="input email as user name！")])
  role = IntegerField(validators=[InputRequired(message="choose the role！")])


class EditStaffForm(BaseForm):
  is_staff = IntegerField(validators=[InputRequired(message="Is the use is in staff！")])
  role = IntegerField(validators=[InputRequired(message="choose the role！")])


class EditBoardForm(BaseForm):
  board_id = IntegerField(validators=[InputRequired(message="Class ID！")])
  name = StringField(validators=[Length(min=1,max=20,message="must be 1-20 characters！")])