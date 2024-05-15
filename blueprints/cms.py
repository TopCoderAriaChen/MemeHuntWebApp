from flask import Blueprint, g, redirect, render_template, request, flash, url_for
from models.user import PermissionEnum
from models.user import UserModel, RoleModel
from models.post import PostModel, CommentModel, BoardModel
from forms.cms import AddStaffForm, EditStaffForm, EditBoardForm
from exts import db
from decorators import permission_required
from utils import restful


bp = Blueprint("cms",__name__,url_prefix="/cms")

@bp.before_request
def cms_before_request():
  if not hasattr(g,"user") or g.user.is_staff == False:
    return redirect("/")


@bp.context_processor
def cms_context_processor():
  return {"PermissionEnum": PermissionEnum}


@bp.get("")
def index():
  return render_template("cms/index.html")


@bp.get("/staff/list")
@permission_required(PermissionEnum.CMS_USER)
def staff_list():
  users = UserModel.query.filter_by(is_staff=True).order_by(UserModel.join_time)
  return render_template("cms/staff_list.html", users=users)

@bp.get("/article/stat")
@permission_required(PermissionEnum.CMS_USER)
def article_stat():
  context = {}
  sql = """with poster1 as 
 (select  author_id from post p 
	group by author_id
   having count(id)>=2
  )
,admins as (select  id author_id from user u 
		where u.username = 'admin')
,target_user as (
select * from poster1 p
	where p.author_id not in (select author_id from admins)   
)
select u.username,p.title,length(content) lengths,rank() over (partition by p.author_id order by length(content) desc) rank_in_user
	,sum(length(content)) over (partition by p.author_id )/ count(p.id) over (partition by p.author_id ) avg_length
 from post p join user u on p.author_id=u.id
  where p.author_id in (select author_id from target_user)
 order by avg_length desc"""
  #sql=sql.replace("\n","").replace("\t","")
  result = db.engine.execute(sql)
  context["result"] = result
  # return render_template("index2.html", **context)
  return render_template("cms/result_list1.html", items=result)

@bp.route("/staff/add",methods=['GET','POST'])
@permission_required(PermissionEnum.CMS_USER)
def add_staff():
  if request.method == "GET":
    roles = RoleModel.query.all()
    return render_template("cms/add_staff.html",roles=roles)
  else:
    #form = AddStaffForm(request.form)
    form = AddStaffForm(request.form,meta={"csrf":False})
    if form.validate():
      email = form.email.data
      role_id = form.role.data
      user = UserModel.query.filter_by(email=email).first()
      if user: # not (user is None):
        flash("the user is already exists!")
        return redirect(url_for("cms.add_staff"))
      else:
        user=UserModel(username=email,email=email,password='111111')
        user.is_staff = True
        user.role = RoleModel.query.get(role_id)
        db.session.commit()
      return redirect(url_for("cms.staff_list"))


@bp.route("/staff/edit/<string:user_id>",methods=['GET','POST'])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff(user_id):
  user = UserModel.query.get(user_id)
  if user is not None:
    print("edit {}".format(user.username))
  if request.method == 'GET':
    roles = RoleModel.query.all()
    return render_template("cms/edit_staff.html",seluser=user,roles=roles)
  else:
    print(request.form)  # ????
    form = EditStaffForm(request.form, meta={"csrf":False})
    if form.validate():
      is_staff = form.is_staff.data
      role_id = form.role.data

      user.is_staff = is_staff
      if user.role_id != role_id:
        user.role = RoleModel.query.get(role_id)
      db.session.commit()
      return staff_list()
      #return redirect(url_for("cms.edit_staff",user_id=user_id))
    else:
      for message in form.messages:
        flash(message)
      return redirect(url_for("cms.edit_staff",user_id=user_id))

@bp.route("/staff/dele/<string:user_id>",methods=['GET','POST'])
@permission_required(PermissionEnum.CMS_USER)
def dele_staff(user_id):
  user = UserModel.query.get(user_id)
  print("delete {}".format(user.email))
  UserModel.query.filter_by(id = user.id).delete()
  db.session.delete(user)
  db.session.commit()
  return staff_list()


@bp.route("/users")
@permission_required(PermissionEnum.FRONT_USER)
def user_list():
  users = UserModel.query.filter_by(is_staff=False).all()
  return render_template("cms/users.html",users=users)


@bp.post("/users/active/<string:user_id>")
@permission_required(PermissionEnum.FRONT_USER)
def active_user(user_id):
  is_active = request.form.get("is_active",type=int)
  if is_active == None:
    return restful.params_error(message="must pass in the argument:is_active!")
  user = UserModel.query.get(user_id)
  user.is_active = bool(is_active)
  db.session.commit()
  return restful.ok()


@bp.get('/posts')
@permission_required(PermissionEnum.POST)
def post_list():
  posts = PostModel.query.all()
  return render_template("cms/posts.html",posts=posts)


@bp.post('/posts/active/<int:post_id>')
@permission_required(PermissionEnum.POST)
def active_post(post_id):
  is_active = request.form.get("is_active", type=int)
  if is_active == None:
    return restful.params_error(message="must pass in the argument:is_active!")
  post = PostModel.query.get(post_id)
  post.is_active = bool(is_active)
  db.session.commit()
  return restful.ok()


@bp.get('/comments')
@permission_required(PermissionEnum.COMMENT)
def comment_list():
  comments = CommentModel.query.all()
  return render_template("cms/comments.html",comments=comments)


@bp.post('/comments/active/<int:comment_id>')
@permission_required(PermissionEnum.COMMENT)
def active_comment(comment_id):
  is_active = request.form.get("is_active", type=int)
  if is_active == None:
    return restful.params_error(message="must pass in the argument:is_active!")
  comment = CommentModel.query.get(comment_id)
  comment.is_active = bool(is_active)
  db.session.commit()
  return restful.ok()


@bp.get("/boards")
@permission_required(PermissionEnum.BOARD)
def board_list():
  boards = BoardModel.query.all()
  return render_template("cms/boards.html",boards=boards)


@bp.post("/boards/edit")
@permission_required(PermissionEnum.BOARD)
def edit_board():
  form = EditBoardForm(request.form)
  if form.validate():
    board_id = form.board_id.data
    name = form.name.data
    board = BoardModel.query.get(board_id)
    board.name = name
    db.session.commit()
    return restful.ok()
  else:
    return restful.params_error(form.messages[0])


@bp.delete("/boards/active/<int:board_id>")
@permission_required(PermissionEnum.BOARD)
def active_board(board_id):
  is_active = request.form.get("is_active", int)
  if is_active == None:
    return restful.params_error("must pass in the argument:is_active!")
  board = BoardModel.query.get(board_id)
  board.is_active = bool(is_active)
  db.session.commit()
  return restful.ok()
