from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

destbp = Blueprint('event', __name__, url_prefix='/events')

@destbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm()    
    bform = BookingForm()

    if bform.validate_on_submit():
      ticketsbooked = bform.numTickets.data

      # calc total of tickets sold
      tickets_sold = db.session.query(db.func.sum(Order.tickets)).filter_by(events_id=id).scalar() or 0

      if tickets_sold + ticketsbooked > event.capacity:
        flash('Cannot purchase tickets capacity reached')

      else:
        order = Order(tickets = ticketsbooked, user_id=current_user.id, events_id = id)
        # add the object to the db session
        db.session.add(order)
        # commit to the database
        db.session.commit()
        flash('Tickets purchased!')
        return render_template('events/show.html', event=event, form=cform, bform=bform)
        
       
    return render_template('events/show.html', event=event, form=cform, bform=bform)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, 
    image = db_file_path, location=form.location.data, datetime=form.datetime.data,
    capacity=form.capacity.data)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    print('Successfully created new event!', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/img',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required  
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event, user=current_user) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))

@destbp.route('/booking-history', methods=['GET'])
@login_required
def booking_history():
    user_id = current_user.id
    bookings = db.session.query(Order).filter_by(user_id=user_id).all()
    event_data = []
    
    for booking in bookings:
        event = db.session.query(Event).filter_by(id=booking.events_id).first()
        event_data.append({
            'event': event,
            'tickets': booking.tickets
        })
    
    return render_template('events/booking_history.html', event_data=event_data)