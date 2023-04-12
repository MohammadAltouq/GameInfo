from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from GameInfo.models import db, User, Fav_games 
from GameInfo.forms import BasicSearch, Details, Profile_img, Fav, Fav_delete, UserDataForm
from GameInfo.helpers import f_rel, n_rel, best_, basic_search, get_detalis, tag_filter
import ast  
import cloudinary.uploader
from werkzeug.security import generate_password_hash
import base64

site = Blueprint('site', __name__, template_folder='site_templates') 

@site.route('/', methods =['GET', 'POST'])
def home():
    details_= Details()
    f = tag_filter(f_rel())
    n = tag_filter(n_rel())
    b = tag_filter(best_())
    if request.method == "POST" and details_.validate_on_submit():
        data = details_.id.data
        data_str = base64.b64encode(str(data).encode('utf-8')).decode('utf-8')
        return redirect(url_for('site.details',  data = data_str))
    
    return render_template('index.html', f_rel = f, n_rel = n, best = b, details_=details_)

@site.route('/profile', methods =['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by( token = current_user.token).first()
    fav_list = Fav_games.query.filter_by(user_token = current_user.token).all()
    form = Profile_img()
    delete = Fav_delete()
    info = UserDataForm()
    try:
        if request.method == "POST":
            if form.validate_on_submit():
                file = request.files['file']
                response = cloudinary.uploader.upload(file)
                url = response['secure_url']
                user.profile_img = url
                db.session.commit()
                return redirect(url_for('site.profile'))
            if delete.validate_on_submit():  
                Fav_games.query.filter_by(id = delete.id.data).delete()
                db.session.commit()
                return redirect(url_for('site.profile'))
            if info.validate_on_submit():
                user.first_name = info.first_name.data
                user.last_name = info.last_name.data
                user.email = info.email.data
                user.password = generate_password_hash(info.password.data)
                db.session.commit()
                return redirect(url_for('site.profile'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('profile.html',form=form,  user=user, fav_list=fav_list, delete=delete, info=info)

@site.route('/search', methods = ['GET','POST'])
@login_required
def search():
    form = BasicSearch()
    details_= Details()
    try:
        if request.method == "POST":
            if form.validate_on_submit():

                name = form.name.data
                result = tag_filter(basic_search(name))
                return render_template('search.html', form=form, data=result, details_=details_)
            elif details_.validate_on_submit():
                data = details_.id.data
                data_str = base64.b64encode(str(data).encode('utf-8')).decode('utf-8')
                return redirect(url_for('site.details',  data = data_str))
        else:
            result = tag_filter(basic_search(" "))
            return render_template('search.html', form=form, details_=details_, data=result)
    except Exception as e:
        raise Exception('Invalid Form Data: Please Check Your Form')

@site.route('/details', methods = ['GET','POST'])
@login_required
def details():
    form = Fav()
    data =  request.args.get('data')
    data = base64.b64decode(data).decode('utf-8')
    res_dict = get_detalis(data)
    fav_list = Fav_games.query.filter_by(user_token = current_user.token).all()
    if request.method == "POST" and form.validate_on_submit():
        form_data = form.data.data
        data_dict=ast.literal_eval(form_data)
        user_token = current_user.token
        for i in fav_list:
            if str(data_dict['id']) == i.rawg_id:
                return redirect(url_for('site.details', data = data))
        rawg_id = data_dict['id']
        name = data_dict['name']
        released = data_dict['released']
        genres = ','.join(i['name'] for i in data_dict['genres'])
        tags = ','.join(i['name'] for i in data_dict['tags'] if i['language'] == "eng")
        img = ','.join(i['image'] for i in data_dict['short_screenshots'])
        website = data_dict['website']
        platforms = ','.join(i['platform']['name'] for i in data_dict['platforms'])
        fav = Fav_games(user_token, rawg_id, name, released, genres, tags, img, website, platforms)
        db.session.add(fav)
        db.session.commit()
        return redirect(url_for('site.profile'))
    return render_template('details.html',form = form, data = res_dict)

@site.route('/test')
def test():
    details_= Details()
    f = tag_filter(f_rel())
    n = tag_filter(n_rel())
    b = tag_filter(best_())
    if request.method == "POST" and details_.validate_on_submit():
        data = details_.id.data
        return redirect(url_for('site.details',  data = data))
    return render_template('test.html', f_rel = f, n_rel = n, best = b, details_=details_)
