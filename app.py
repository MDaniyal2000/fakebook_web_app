import os
import json
from dateutil import parser
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/fakebook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SECRET_KEY'] = 'YMyqz0uWN0'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

db = SQLAlchemy(app)

# Models
#Users Table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    gender = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    profile_picture = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='post_owner', cascade="all,delete", lazy='dynamic')
    likes = db.relationship('Like', backref='liked_by', cascade="all,delete", lazy='dynamic')
    friends = db.relationship('Friend', backref='friend_of', cascade="all,delete", lazy='dynamic')
    sent_requests = db.relationship('SentRequest', backref='requested_by', cascade="all,delete", lazy='dynamic')
    recd_requests = db.relationship('ReceivedRequest', backref='requested_to', cascade="all,delete", lazy='dynamic')

#Posts Table
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.Text)
    post_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_photos = db.relationship('Photo', backref='of_post', cascade="all,delete", lazy='dynamic')
    post_likes = db.relationship('Like', backref='for_post', cascade="all,delete", lazy='dynamic')

#Likes Table
class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

#Photos Table
class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

#Friends Table
class Friend(db.Model):
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, nullable=False)

#Sent Requests Table
class SentRequest(db.Model):
    __tablename__ = 'sentrequest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_to = db.Column(db.Integer, nullable=False)

#Received Requests Table
class ReceivedRequest(db.Model):
    __tablename__ = 'receivedrequest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_by = db.Column(db.Integer, nullable=False)

# Routes
@app.route('/')
def index():
    try:
        if session['logged_in']:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            ids_included = [friend.friend_id for friend in user.friends]
            ids_included += [user_id]
            posts = Post.query.filter(Post.user_id.in_(ids_included)).order_by(Post.id.desc())
            return render_template('dashboard.html', user=user, posts=posts)
    except:
        return render_template('index.html')

@app.route('/get_posts')
def get_posts():
    try:
        if session['logged_in']:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            ids_included = [friend.friend_id for friend in user.friends]
            ids_included += [user_id]
            posts = Post.query.filter(Post.user_id.in_(ids_included)).order_by(Post.id.desc())
            return render_template('get_posts.html', user=user, posts=posts)
    except:
        return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    try:
        if session['logged_in']:
            return redirect('/')
    except:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginUser():
    try:
        email = request.form['loginemail']
        password = request.form['loginpass']

        user_true = User.query.filter_by(email_address=email, password=password).first()
        if user_true:
            session['user_name'] = email
            session['user_id'] = user_true.id
            session['logged_in'] = True
            return json.dumps({
                'message' : 'success'
            })
        else:
            return json.dumps({
                'message' : 'invalid login'
            })

    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/register', methods=['GET'])
def register():
    try:
        if session['logged_in']:
            return redirect('/')
    except:
        return render_template('register.html')

@app.route('/register', methods=['POST'])
def registerUser():
    try:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password1 = request.form['password1']
        gender = request.form['gender']
        dob = request.form['dob']
        pic = request.files['picture']

        user_exists = User.query.filter_by(email_address=email).first()
        if user_exists:
            return json.dumps({
                'message' : 'Email already exists'
            })

        filename = pic.filename
        if '.' not in filename:
            return json.dumps({
                'message' : 'File extension not allowed'
            })

        ext = filename.rsplit(".", 1)[1]
        if ext.upper() not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return json.dumps({
                'message' : 'File extension not allowed'
            })

        user = User(first_name=fname, last_name=lname, email_address=email, password=password1,  gender=gender, dob=dob, profile_picture='temp')
        db.session.add(user)
        db.session.commit()

        file_name = f'{user.id}-{user.first_name}.{(pic.filename).split(".")[-1]}' 

        path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        pic.save(path)

        user.profile_picture = file_name
        db.session.commit()

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/post', methods=['POST'])
def newpost():
    try:
        post_text = request.form['post_text']

        get_user = User.query.filter_by(id=session['user_id']).first()

        post = Post(post_content=post_text, post_owner=get_user)
        db.session.add(post)
        db.session.commit()

        photo = request.files['photo']
        if photo:
            file_name = f'{post.id}-photo.{(photo.filename).split(".")[-1]}' 
            path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            photo.save(path)

            photo = Photo(photo_name=file_name, of_post=post)
            db.session.add(photo)
            db.session.commit()

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/logout')
def logout():
    try:
        if session['logged_in']:
            session.pop('logged_in', None)
            session.pop('user_id', None)
            session.pop('user_name', None)
            return redirect('/')
    except:
        return redirect('/')

@app.route('/profile')
def profile():
    try:
        if session['logged_in']:
            user_id = request.args.get('id', default=0)
            user = User.query.filter_by(id=user_id).first()
            if user:
                dateobj = parser.parse(str(user.dob))
                dob = datetime.strftime(dateobj, '%d %b, %Y')
                dateobj = parser.parse(str(user.created_at))
                joined_date = datetime.strftime(dateobj, '%d %b, %Y')
                return render_template('profile.html', user=user, dob=dob, joined_date=joined_date)
            else:
                return render_template('profile.html', user=user)
    except:
        return redirect('/')

@app.route('/requests')
def requests():
    try:
        if session['logged_in']:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            sent_requests_found = user.sent_requests
            sent_requests = []
            for req in sent_requests_found:
                friend_id = req.requested_to
                friend = User.query.filter_by(id=friend_id).first()
                sent_requests.append([req, friend])
            recd_requests_found = user.recd_requests
            recd_requests = []
            for req in recd_requests_found:
                friend_id = req.requested_by
                friend = User.query.filter_by(id=friend_id).first()
                recd_requests.append([req, friend])
            else:
                return render_template('requests.html', sent=sent_requests, receive=recd_requests, user=user)
    except:
        return redirect('/')

@app.route('/posts')
def posts():
    try:
        if session['logged_in']:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            posts = user.posts.order_by(Post.id.desc())

            return render_template('posts.html', posts=posts, user=user)
    except Exception as e:
        return redirect('/')

@app.route('/new_friends')
def new_friends():
    try:
        if session['logged_in']:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            ids_excluded = [request.requested_to for request in user.sent_requests]
            ids_excluded += [request.requested_by for request in user.recd_requests]
            ids_excluded += [friend.friend_id for friend in user.friends]
            ids_excluded += [user_id]
            users_found = User.query.filter(User.id.notin_(ids_excluded))
            return render_template('explore.html', users_found=users_found, user=user)
    except Exception as e:
        return redirect('/')

@app.route('/friends')
def friends():
    try:
        if session['logged_in']:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            friends = []
            for friend_found in user.friends:
                user_friend = User.query.filter_by(id=friend_found.friend_id).first()
                friends.append(user_friend)
            return render_template('friends.html', friends=friends, user=user)
    except Exception as e:
        return redirect('/')

@app.route('/sent_request', methods=['POST'])
def sent_frequest():
    try:
        current_user = User.query.filter_by(id=session['user_id']).first()
        friend_id = request.form.get("friend_id","")
        to_user = User.query.filter_by(id=friend_id).first()
        sentRequest = SentRequest(requested_by=current_user, requested_to=friend_id)
        db.session.add(sentRequest)
        db.session.commit()

        recdRequest = ReceivedRequest(requested_to=to_user, requested_by=session['user_id'])
        db.session.add(recdRequest)
        db.session.commit()

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/cancel_request', methods=['POST'])
def cancel_request():
    try:
        request_id = request.form.get("request_id","")
        sent_req = SentRequest.query.filter_by(id=request_id).first()
        to_id = sent_req.requested_to
        db.session.delete(sent_req)
        db.session.commit()
        recd_req = ReceivedRequest.query.filter_by(requested_by=session['user_id'], user_id=to_id).first()
        db.session.delete(recd_req)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/remove_request', methods=['POST'])
def remove_request():
    try:
        request_id = request.form.get("request_id","")
        recd_req = ReceivedRequest.query.filter_by(id=request_id).first()
        by_id = recd_req.requested_by
        db.session.delete(recd_req)
        db.session.commit()
        sent_req = SentRequest.query.filter_by(requested_to=session['user_id'], user_id=by_id).first()
        db.session.delete(sent_req)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/delete_post', methods=['POST'])
def delete_post():
    try:
        post_id = request.form.get("post_id","")
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/accept_request', methods=['POST'])
def accept_request():
    try:
        request_id = request.form.get("request_id","")
        recd_req = ReceivedRequest.query.filter_by(id=request_id).first()
        by_id = recd_req.requested_by
        current_user = User.query.filter_by(id=session['user_id']).first()
        new_friend = Friend(friend_of=current_user, friend_id=by_id)
        db.session.add(new_friend)
        db.session.commit()
        other_user = User.query.filter_by(id=by_id).first()
        again_friend = Friend(friend_of=other_user, friend_id=session['user_id'])
        db.session.add(again_friend)
        db.session.commit()
        db.session.delete(recd_req)
        db.session.commit()
        sent_req = SentRequest.query.filter_by(requested_to=session['user_id'], user_id=by_id).first()
        db.session.delete(sent_req)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/remove_friend', methods=['POST'])
def remove_friend():
    try:
        user_id = session['user_id']
        friend_id = request.form.get("friend_id","")

        my_friend = Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        db.session.delete(my_friend)
        db.session.commit()

        his_friend = Friend.query.filter_by(user_id=friend_id,friend_id=user_id).first()
        db.session.delete(his_friend)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })


@app.route('/like_post', methods=['POST'])
def like_post():
    try:
        user_id = session['user_id']
        post_id = request.form.get("post_id","")
        post = Post.query.filter_by(id=post_id).first()
        user = User.query.filter_by(id=user_id).first()
        like = Like(liked_by=user, for_post=post)
        db.session.add(like)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/unlike_post', methods=['POST'])
def unlike_post():
    try:
        user_id = session['user_id']
        post_id = request.form.get("post_id","")
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        db.session.delete(like)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)