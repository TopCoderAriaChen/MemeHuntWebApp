from models.user import PermissionModel,RoleModel,PermissionEnum,UserModel
from models.post import BoardModel,PostModel
import click
from exts import db
from faker import Faker
import random


def create_permission():
  for permission_name in dir(PermissionEnum):
    if permission_name.startswith("__"):
      continue
    permission = PermissionModel(name=getattr(PermissionEnum,permission_name))
    db.session.add(permission)
  db.session.commit()
  click.echo("role added in！")


def create_role():
  # 稽查员
  inspector = RoleModel(name="checker",desc="check message！")
  inspector.permissions = PermissionModel.query.filter(PermissionModel.name.in_([PermissionEnum.POST,PermissionEnum.COMMENT])).all()

  # 运营
  operator = RoleModel(name="runner",desc="maintain to run the web")
  operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
    PermissionEnum.POST,
    PermissionEnum.COMMENT,
    PermissionEnum.BOARD,
    PermissionEnum.FRONT_USER
  ])).all()

  # administrator
  administrator = RoleModel(name="administrator",desc="web development！")
  administrator.permissions = PermissionModel.query.all()

  db.session.add_all([inspector,operator,administrator])
  db.session.commit()
  click.echo("role added in！")


def create_test_user():
  admin_role = RoleModel.query.filter_by(name="administrator").first()
  zhangsan = UserModel(username="zhang",email="zhangsan@zlkt.net",password="111111",is_staff=True,role=admin_role)

  operator_role = RoleModel.query.filter_by(name="runnier").first()
  lisi = UserModel(username="li",email="lisi@zlkt.net",password="111111",is_staff=True,role=operator_role)

  inspector_role = RoleModel.query.filter_by(name="checker").first()
  wangwu = UserModel(username="wang",email="wangwu@zlkt.net",password="111111",is_staff=True,role=inspector_role)

  db.session.add_all([zhangsan,lisi,wangwu])
  db.session.commit()
  click.echo("test add in user！")


@click.option("--username",'-u')
@click.option("--email",'-e')
@click.option("--password",'-p')
def create_admin(username,email,password):
  admin_role = RoleModel.query.filter_by(name="administrator").first()
  admin_user = UserModel(username=username, email=email, password=password, is_staff=True, role=admin_role)
  db.session.add(admin_user)
  db.session.commit()
  click.echo("Administrator created！")


def create_board():
  board_names = ['cat', 'celebrities', 'monday', 'lol', 'life']
  for board_name in board_names:
    board = BoardModel(name=board_name)
    db.session.add(board)
  db.session.commit()
  click.echo("class added in successfully！")


def create_test_post():
  fake = Faker(locale="zh_CN")
  author = UserModel.query.first()
  boards = BoardModel.query.all()

  click.echo("test post message...")
  for x in range(98):
    title = fake.sentence()
    content = fake.paragraph(nb_sentences=10)
    random_index = random.randint(0,4)
    board = boards[random_index]
    post = PostModel(title=title, content=content, board=board, author=author)
    db.session.add(post)
  db.session.commit()
  click.echo("test post message done ！")

