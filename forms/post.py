from .baseform import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import InputRequired,Length,DataRequired


class PublicPostForm(BaseForm):
  title = StringField(validators=[Length(min=2,max=100,message='input the ttitl！')])
  content = StringField(validators=[Length(min=2,message="input the content！")])
  board_id = IntegerField(validators=[InputRequired(message='input the id of class！')])
  credit= IntegerField(validators=[DataRequired(message='input the credit！')])

class PublicCommentForm(BaseForm):
  content = StringField(validators=[Length(min=2,message="input the comment！")])
  accept = IntegerField() #validators=[InputRequired(message='input the accept degree！')])