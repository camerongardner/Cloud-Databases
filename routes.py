# routes.py

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from extensions import db
from models import User, Degree, Enrollment
from forms import RegistrationForm, LoginForm, EnrollmentForm, DegreeForm
from decorators import admin_required
from werkzeug.urls import url_parse

# Define a Blueprint named 'main'
main = Blueprint('main', __name__)

# Public Routes
@main.route('/')
@main.route('/index')
def index():
    degrees = Degree.query.all()
    return render_template('index.html', title='Home', degrees=degrees)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # Security check for redirection
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/enroll/<int:degree_id>', methods=['GET', 'POST'])
@login_required
def enroll(degree_id):
    degree = Degree.query.get_or_404(degree_id)
    form = EnrollmentForm()
    form.degree.choices = [(degree.id, degree.degree_name)]
    if form.validate_on_submit():
        # Check if already enrolled
        existing_enrollment = Enrollment.query.filter_by(user_id=current_user.id, degree_id=degree.id).first()
        if existing_enrollment:
            flash('You are already enrolled in this degree.')
            return redirect(url_for('main.index'))
        enrollment = Enrollment(user_id=current_user.id, degree_id=degree.id)
        db.session.add(enrollment)
        db.session.commit()
        flash('You have successfully enrolled in the degree.')
        return redirect(url_for('main.index'))
    return render_template('enroll.html', title='Enroll', degree=degree, form=form)

# Admin Routes for Managing Degrees
@main.route('/admin/degrees')
@login_required
@admin_required
def admin_degrees():
    degrees = Degree.query.all()
    return render_template('admin_degrees.html', degrees=degrees)

@main.route('/admin/degrees/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_degree():
    form = DegreeForm()
    if form.validate_on_submit():
        degree = Degree(
            degree_name=form.degree_name.data,
            description=form.description.data,
            duration=form.duration.data,
            requirements=form.requirements.data
        )
        db.session.add(degree)
        db.session.commit()
        flash('Degree created successfully.')
        return redirect(url_for('main.admin_degrees')) 
    return render_template('create_degree.html', form=form)

@main.route('/admin/degrees/edit/<int:degree_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_degree(degree_id):
    degree = Degree.query.get_or_404(degree_id)
    form = DegreeForm(obj=degree)
    if form.validate_on_submit():
        degree.degree_name = form.degree_name.data
        degree.description = form.description.data
        degree.duration = form.duration.data
        degree.requirements = form.requirements.data
        db.session.commit()
        flash('Degree updated successfully.')
        return redirect(url_for('main.admin_degrees'))
    return render_template('edit_degree.html', form=form, degree=degree)

@main.route('/admin/degrees/delete/<int:degree_id>', methods=['POST'])
@login_required
@admin_required
def delete_degree(degree_id):
    degree = Degree.query.get_or_404(degree_id)
    db.session.delete(degree)
    db.session.commit()
    flash('Degree deleted successfully.')
    return redirect(url_for('main.admin_degrees'))

# Error Handler for 403 Forbidden
@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# Route to View User's Enrollments
@main.route('/my_enrollments')
@login_required
def my_enrollments():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    return render_template('my_enrollments.html', enrollments=enrollments)
