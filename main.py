import datetime
from flask import Flask, render_template, redirect, url_for, flash
from forms import AddCafe, CafeReviews, AddWebsiteComments, EditCafe
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_gravatar import Gravatar
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['CKEDITOR_PKG_TYPE'] = 'full'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Gravatar Image
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)


class CafeDB(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.Text, unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    wifi = db.Column(db.Text, nullable=False)
    seating = db.Column(db.Text, nullable=False)
    food = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    reviews = relationship("CafeReviewsDB", back_populates="cafe")


class CafeReviewsDB(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    author_email = db.Column(db.Text, nullable=False)
    review = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    cafe = relationship("CafeDB", back_populates="reviews")
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"))


class FeedbackDB(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    commentator_name = db.Column(db.Text, nullable=False)
    commentator_email = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)


db.create_all()


@app.route("/", methods=["POST", "GET"])
def home():
    feedback_form = AddWebsiteComments()
    cafe_database = CafeDB.query.all()
    if feedback_form.validate_on_submit():
        new_entry = FeedbackDB(comment=feedback_form.comment.data,
                               commentator_name=feedback_form.commentator_name.data,
                               commentator_email=feedback_form.commentator_email.data,
                               date=datetime.datetime.now().strftime("on %d-%B-%Y at %H:%M:%S %p"))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('about'))
    return render_template("index.html", cafe_database=cafe_database, feedback_form=feedback_form)


@app.route("/about", methods=["POST", "GET"])
def about():
    feedback_form = AddWebsiteComments()
    feedback_display = FeedbackDB.query.all()
    if feedback_form.validate_on_submit():
        new_entry = FeedbackDB(comment=feedback_form.comment.data,
                               commentator_name=feedback_form.commentator_name.data,
                               commentator_email=feedback_form.commentator_email.data,
                               date=datetime.datetime.now().strftime("on %d-%B-%Y at %H:%M:%S %p"))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('about'))
    return render_template("about.html", feedback_form=feedback_form, feedback_display=feedback_display)


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    cafe_form = AddCafe()
    feedback_form = AddWebsiteComments()
    if cafe_form.validate_on_submit():
        new_cafe_name = cafe_form.cafe_name.data
        if CafeDB.query.filter_by(cafe_name=new_cafe_name).first():
            flash("Cafe name already registered. Please add with a different name")
            return redirect(url_for("add_cafe"))
        cafe_entry = CafeDB(cafe_name=cafe_form.cafe_name.data,
                            address=cafe_form.address.data,
                            wifi=cafe_form.wifi.data,
                            seating=cafe_form.seating.data,
                            food=cafe_form.food.data,
                            cost=cafe_form.cost.data,
                            description=cafe_form.description.data)
        db.session.add(cafe_entry)
        db.session.commit()
        return redirect(url_for('home'))
    if feedback_form.validate_on_submit():
        new_entry = FeedbackDB(comment=feedback_form.comment.data,
                               commentator_name=feedback_form.commentator_name.data,
                               commentator_email=feedback_form.commentator_email.data,
                               date=datetime.datetime.now().strftime("on %d-%B-%Y at %H:%M:%S %p"))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('about'))
    return render_template("add.html", form=cafe_form, feedback_form=feedback_form)


@app.route("/edit/<int:index>", methods=["POST", "GET"])
def edit_cafe(index):
    feedback_form = AddWebsiteComments()
    cafe_data = CafeDB.query.filter_by(id=index).first()
    cafe_edit_form = EditCafe(cafe_name=cafe_data.cafe_name,
                              address=cafe_data.address,
                              wifi=cafe_data.wifi,
                              seating=cafe_data.seating,
                              food=cafe_data.food,
                              cost=cafe_data.cost,
                              description=cafe_data.description)
    if cafe_edit_form.validate_on_submit():
        cafe_data.cafe_name = cafe_edit_form.cafe_name.data
        cafe_data.address = cafe_edit_form.address.data
        cafe_data.wifi = cafe_edit_form.wifi.data
        cafe_data.seating = cafe_edit_form.seating.data
        cafe_data.food = cafe_edit_form.food.data
        cafe_data.cost = cafe_edit_form.cost.data
        cafe_data.description = cafe_edit_form.description.data
        db.session.commit()
        return redirect(url_for('home'))
    if feedback_form.validate_on_submit():
        new_entry = FeedbackDB(comment=feedback_form.comment.data,
                               commentator_name=feedback_form.commentator_name.data,
                               commentator_email=feedback_form.commentator_email.data,
                               date=datetime.datetime.now().strftime("on %d-%B-%Y at %H:%M:%S %p"))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('about'))
    feedback_form = AddWebsiteComments()
    return render_template("edit.html", form=cafe_edit_form, feedback_form=feedback_form)


@app.route("/delete/<int:index>", methods=["POST", "GET"])
def delete_cafe(index):
    cafe_data = CafeDB.query.filter_by(id=index).first()
    db.session.delete(cafe_data)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/aboutcafe/<int:index>", methods=["POST", "GET"])
def about_cafe(index):
    cafe_data = CafeDB.query.filter_by(id=index).first()
    display_reviews = CafeReviewsDB.query.filter_by(cafe_id=index).all()
    user_review = CafeReviews()
    if user_review.validate_on_submit():
        cafe_entry = CafeReviewsDB(title=user_review.title.data,
                                   subtitle=user_review.subtitle.data,
                                   author=user_review.author.data,
                                   author_email=user_review.author_email.data,
                                   review=user_review.review.data,
                                   date=datetime.datetime.now().strftime("on %d-%B-%Y at %H:%M:%S %p"),
                                   cafe_id=index)
        db.session.add(cafe_entry)
        db.session.commit()
        return redirect(url_for('about_cafe', index=index))
    feedback_form = AddWebsiteComments()
    if feedback_form.validate_on_submit():
        new_entry = FeedbackDB(comment=feedback_form.comment.data,
                               commentator_name=feedback_form.commentator_name.data,
                               commentator_email=feedback_form.commentator_email.data,
                               date=datetime.datetime.now().strftime("on %d-%B-%Y at %H:%M:%S %p"))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('about'))
    return render_template("aboutcafe.html", data=cafe_data, display_reviews=display_reviews, user_review=user_review,
                           feedback_form=feedback_form)


if __name__ == "__main__":
    app.run(debug=True)
