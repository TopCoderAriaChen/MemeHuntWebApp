from flask import Blueprint, request, render_template, jsonify, current_app, url_for, send_from_directory, g, abort, session,redirect,flash
from werkzeug.utils import secure_filename
import os
from models.post import PostModel, BoardModel, CommentModel
from exts import csrf, db
from decorators import login_required
from forms.post import PublicPostForm, PublicCommentForm
from utils import restful
from flask_paginate import Pagination

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


bp = Blueprint("front", __name__, url_prefix="")

@bp.route("/")
def in_root():
  context = {
    'current_user':None   # session['user_id']
  }
  if 'user_id' in session.keys():
    return redirect("/index")
  else:
    return render_template("front/introductory.html", **context)


@bp.post("/search")
def search():
  context = { }
  if 'user_id' in session.keys():
    context = {
      'current_user': session['user_id'],
      'key':request.form["key"]
    }
    if session['current_url'] is not None and len(session['current_url'])>0:
      session['key']=request.form["key"]
      return redirect(session['current_url']) #,**context)
  else:
    return redirect("user/login")
    #return render_template("front/introductory.html", **context)

@bp.route("/introductory")
def introductory():
  context = { }
  return render_template("front/introductory.html", **context)

@bp.route("/index")
def index():

  if 'user_id' in session.keys():
    context = {
      'current_user': session['user_id']
    }
    if 'key' in session.keys():
      key = "%" + session['key'] + "%"
    else:
      key = ''
    session['key']=''
    boards = BoardModel.query.filter_by(is_active=True).all()

    page = request.args.get("page", type=int, default=1)

    board_id = request.args.get("board_id",type=int,default=0)

    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")

    end = start + current_app.config.get("PER_PAGE_COUNT")

    query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())

    if len(key) > 0:
      query_obj = query_obj.filter(PostModel.title.like(key))
    if board_id:
      query_obj = query_obj.filter_by(board_id=board_id)

    total = query_obj.count()


    posts = query_obj.slice(start, end)


    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
      "posts": posts,
      "boards": boards,
      "pagination": pagination,
      "current_board": board_id
    }
    current_app.logger.info("index is requested")
    session['current_url'] = '/index'
    return render_template("front/index.html", **context)
  else:
    session['current_url'] = ''
    return redirect("user/login")
    #return render_template("front/introductory.html")


@bp.route("/mypost")
def mypost():
  context = { }
  if 'user_id' in session.keys():
    context = {
      'current_user': session['user_id']
    }
    if 'key' in session.keys():
      key="%"+session['key']+"%"
    else:
      key=''
    session['key'] = ''
    boards = BoardModel.query.filter_by(is_active=True).all()

    page = request.args.get("page", type=int, default=1)

    board_id = request.args.get("board_id", type=int, default=0)

    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")

    end = start + current_app.config.get("PER_PAGE_COUNT")

    query_obj = (PostModel.query
                 .filter_by(is_active=True)
                 .filter_by(author_id=context['current_user'])
                 .order_by(PostModel.create_time.desc()))
    if len(key)>0:
      query_obj = query_obj.filter(PostModel.title.like(key))
    if board_id:
      query_obj = query_obj.filter_by(board_id=board_id)

    total = query_obj.count()

    posts = query_obj.slice(start, end)

    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
      "posts": posts,
      "boards": boards,
      "pagination": pagination,
      "current_board": board_id
    }
    current_app.logger.info("mypost is requested")
    session['current_url']='/mypost'
    return render_template("front/mypost.html", **context)
  else:
    session['current_url'] = ''
    return redirect("user/login")
    #return render_template("front/introductory.html", **context)


@bp.route("/mycomment")
def mycomment():
  context = { }
  if 'user_id' in session.keys():
    context = {
      'current_user': session['user_id']
    }
    if 'key' in session.keys():
      key="%"+session['key']+"%"
    else:
      key=''
    session['key'] = ''
    boards = BoardModel.query.filter_by(is_active=True).all()

    page = request.args.get("page", type=int, default=1)

    board_id = request.args.get("board_id", type=int, default=0)

    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")

    end = start + current_app.config.get("PER_PAGE_COUNT")

    '''query_obj = db.session.query(PostModel,CommentModel).filter(CommentModel.post_id == PostModel.id).filter(
      CommentModel.author_id == context['current_user'])
    '''

    query_obj=db.session.query(PostModel).join(CommentModel,CommentModel.post_id==PostModel.id).filter(CommentModel.author_id==context['current_user'])
    '''query_obj0 = (PostModel.query
                 .filter_by(is_active=True)
                 #.filter(stmt)
                 .order_by(PostModel.create_time.desc()))'''
    if len(key)>0:
      query_obj = query_obj.filter(PostModel.title.like(key))
    if board_id:
      query_obj = query_obj.filter_by(board_id=board_id)

    total = query_obj.count()

    posts = query_obj.slice(start, end)

    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
      "posts": posts,
      "boards": boards,
      "pagination": pagination,
      "current_board": board_id
    }
    current_app.logger.info("mycomment is requested")
    session['current_url'] = '/mycomment'
    return render_template("front/mypost.html", **context)
  else:
    session['current_url'] = ''
    return redirect("user/login")
    #return render_template("front/introductory.html", **context)



@bp.route("/myrank")
def myrank():
  context = { }
  if 'user_id' in session.keys():
    context = {
      'current_user': session['user_id']
    }
    page = request.args.get("page", type=int, default=1)

    board_id = request.args.get("board_id", type=int, default=0)

    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")

    end = start + current_app.config.get("PER_PAGE_COUNT")

    query_obj=execute_sql("select username,number_of_post,number_of_comment,credits,id from view_comment_rank")
    #query_obj=db.session.query(PostModel).join(CommentModel,CommentModel.post_id==PostModel.id).filter(CommentModel.author_id==context['current_user'])

    #total = query_obj.count()
    #ranks = query_obj.slice(start, end)
    total = len(query_obj)
    ranks = query_obj[start:end]
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
      "ranks": ranks,
      "pagination": pagination,
      "current_board": board_id
    }
    current_app.logger.info("myrank is requested")
    session['current_url'] = ''
    return render_template("front/myrank.html", **context)
  else:
    session['current_url'] = ''
    return redirect("user/login")
    #return render_template("front/introductory.html", **context)


@bp.route("/post/public", methods=['GET', 'POST'])
@login_required
def public_post():
  if request.method == 'GET':
    boards = BoardModel.query.all()
    return render_template("front/public_post.html", boards=boards)
  else:
    form = PublicPostForm(request.form)
    if form.validate():
      title = form.title.data
      content = form.content.data
      board_id = form.board_id.data
      credit= form.credit.data
      post = PostModel(id=0,title=title, content=content, board_id=board_id, author=g.user,credit=credit)
      db.session.add(post)
      db.session.commit()
      return restful.ok()
    else:
      message = form.messages[0]
      return restful.params_error(message=message)


@bp.route('/image/<path:filename>')
def uploaded_image(filename):
  path = current_app.config.get("UPLOAD_IMAGE_PATH")
  print("uploading image to :{}".format(path))
  return send_from_directory(path, filename)


@bp.post("/upload/image")
@csrf.exempt
@login_required
def upload_image():
  f = request.files.get('image')
  extension = f.filename.split('.')[-1].lower()
  if extension not in ['jpg', 'gif', 'png', 'jpeg']:
    return jsonify({
      "errno": 400,
      "data": []
    })
  filename = secure_filename(f.filename)
  f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"), filename))
  url = url_for('front.uploaded_image', filename=filename)
  return jsonify({
    "errno": 0,
    "data": [{
      "url": url,
      "alt": "",
      "href": ""
    }]
  })


@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
  post = PostModel.query.get(post_id)
  if not post.is_active:
    return abort(404)
  post.read_count += 1
  db.session.commit()
  if post.author_id==session["user_id"]:
    return render_template("front/post_detail_me.html", post=post,current_user=session["user_id"])
  else:
    return render_template("front/post_detail.html",post=post)


@bp.post("/post/<int:post_id>/comment")
@login_required
def public_comment(post_id):
  form = PublicCommentForm(request.form)
  if form.validate():
    content = form.content.data
    accept= form.accept.data
    comment = CommentModel(id=0,content=content, post_id=post_id, author=g.user,accept=accept)
    db.session.add(comment)
    db.session.commit()
  else:
    for message in form.messages:
      flash(message)

  return redirect(url_for("front.post_detail", post_id=post_id))


#@bp.route("/post/public", methods=['GET', 'POST'])

@bp.post("/post/accept/<int:post_id>")
@login_required
def comment_accept(post_id):
  register_dict = request.form
  comment_id = register_dict['comment_id']

  #query_obj = CommentModel.query.filter_by(id=comment_id)
  #comment = CommentModel.query.get(comment_id)
  print(comment_id)
  star=0
  if 'star5' in register_dict.keys():
    star=5
  if 'star4' in register_dict.keys():
    star=4
  if 'star3' in register_dict.keys():
    star=3
  if 'star2' in register_dict.keys():
    star=2
  if 'star1' in register_dict.keys():
    star = 1
  if star>0:
    star=6-star
    CommentModel.query.filter_by(id=comment_id).update({"accept": star})
    db.session.commit()

  return redirect(url_for("front.post_detail", post_id=post_id))

def execute_sql(sql:str):
  result = db.session.execute(sql)
  rows = []
  for row in result:
    rows.append(row)

  return rows