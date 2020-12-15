from flask import Flask, request, session, redirect, url_for, render_template, flash

from .models import User, db, Rooms, Room_type, Booked, Reservations, Payment
from .forms import PaymentForm, SignUpForm, SignInForm, AboutUserForm, CheckAvailForm, ReserveForm

from hotel import app
import datetime



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update/<rid>', methods=('GET', 'POST'))
def update_reservation(rid):
    if session['user_available']:
        cur_res = Reservations.query.get(rid)
        updated_res = ReserveForm(obj=cur_res)
        us = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            room_list = updated_res.room_numbers.data.split(",")
            d1 = datetime.datetime.combine(updated_res.checkin_date.data, datetime.time(0, 0))
            d2 = datetime.datetime.combine(updated_res.checkout_date.data, datetime.time(0, 0))
            num = updated_res.num_guests.data

            all_reserves = Reservations.query.all()
            all_bookings = Booked.query.all()
            all_rooms = Rooms.query.all()

            if d2 <= d1 or d1 < datetime.datetime.now() or d2 < datetime.datetime.now():
                flash("Please recheck your date! It has to be at least today! ")
                return redirect(url_for('update_reservation', rid=rid))
            total_num = 0
            for each in room_list:
                for each_reserves in all_reserves:
                    for each_booking in all_bookings:
                        c1 = each_reserves.checkin_date
                        c2 = each_reserves.checkout_date
                        if each_booking.room_id == int(each) and (
                                (c1 <= d1 and d2 <= c2) or (d1 <= c1 and d2 <= c2) or (c1 <= d1 and c2 <= d2) or (
                                d1 <= c1 and c2 <= d2)):
                            flash("The room you are reserving is not available at the time you selected!")
                            return redirect(url_for('update_reservation', rid=rid))
            for each in room_list:
                for each_room in all_rooms:
                    if int(each) == each_room.room_number:
                        total_num += each_room.capacity
            if num > total_num:
                flash(
                    "The rooms you selected can't fit the number of guests you entered. Please restart the reservation!")
                return redirect(url_for('update_reservation', rid=rid))
            cres = Reservations.query.get(rid)
            cres.ruid = us.uid
            cres.checkin_date = updated_res.checkin_date.data
            cres.checkout_date = updated_res.checkout_date.data
            cres.num_guests = updated_res.num_guests.data
            db.session.commit()

            cbooked = Booked.query.filter_by(brid=rid).all()
            for each in cbooked:
                db.session.delete(each)
                db.session.commit()

            for each in room_list:
                single_room = Booked(rid, each)
                db.session.add(single_room)
                db.session.commit()
            return redirect(url_for('show_rooms'))
        return render_template('update.html', updated_res=updated_res)

    flash('You are not a valid user to Edit this Post')
    return redirect(url_for('show_rooms'))


@app.route('/delete/<rid>', methods=('GET', 'POST'))
def delete_reservation(rid):
    if session['user_available']:
        cur_res = Reservations.query.get(rid)
        db.session.delete(cur_res)
        db.session.commit()
        cbooked = Booked.query.filter_by(brid=rid).all()
        for each in cbooked:
            db.session.delete(each)
            db.session.commit()
        return redirect(url_for('show_rooms'))
    flash('You are not a valid user to Delete this Reservation!')
    return redirect(url_for('show_rooms'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupform = SignUpForm(request.form)
    if request.method == 'POST':
        reg = User(signupform.firstname.data, signupform.lastname.data, \
                   signupform.username.data, signupform.password.data, \
                   signupform.email.data)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html', signupform=signupform)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    signinform = SignInForm()
    if request.method == 'POST':
        em = signinform.email.data
        log = User.query.filter_by(email=em).first()
        if log.password == signinform.password.data:
            current_user = log.username
            session['current_user'] = current_user
            session['user_available'] = True
            return redirect(url_for('show_rooms'))
    return render_template('signin.html', signinform=signinform)


@app.route('/about_user')
def about_user():
    aboutuserform = AboutUserForm()
    if session['user_available']:
        user = User.query.filter_by(username=session['current_user']).first()
        reservations = Reservations.query.filter_by(ruid=user.uid).all()
        payments = Payment.query.filter_by(puid=user.uid).all()
        booked = Booked.query.all()
        return render_template('about_user.html', user=user, reservations=reservations, booked=booked,
                               payments=payments,
                               aboutuserform=aboutuserform)
    flash('You are not a Authenticated User')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))

global_avail = None

@app.route('/rooms')
def show_rooms():
    if session['user_available']:
        all_reserves = Reservations.query.all()
        all_bookings = Booked.query.all()
        all_rooms = Rooms.query.all()
        all_room_type = Room_type.query.all()
        global global_avail
        if global_avail is None:
            return render_template('rooms.html', rooms=all_rooms, room_type=all_room_type)
        # If entered information on check availability page, only display rooms available at that point
        c_in = datetime.datetime.combine(global_avail.checkin_date.data, datetime.time(0, 0))
        c_out = datetime.datetime.combine(global_avail.checkout_date.data, datetime.time(0, 0))
        for each in all_rooms:
            for each_reserves in all_reserves:
                for each_booking in all_bookings:
                    c1 = each_reserves.checkin_date
                    c2 = each_reserves.checkout_date
                    if each_booking.room_id == each.room_number and (
                            (c_in <= c1 and c2 <= c_out) or (c1 <= c_in and c2 <= c_out) or (c_in <= c1 and c_out <= c2) or (
                            c1 <= c_in and c_out <= c2)) and (c_in < c_out):
                        all_rooms.remove(each)
        global_avail = None
        return render_template('rooms.html', rooms=all_rooms, room_type=all_room_type)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/available', methods=['GET', 'POST'])
def check_available():
    if session['user_available']:
        reservation = CheckAvailForm(request.form)
        us = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            global global_avail
            global_avail = reservation
            return redirect(url_for('show_rooms'))
        return render_template('add_room.html', reservation=reservation)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if session['user_available']:
        reservation = ReserveForm(request.form)
        us = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            room_list = reservation.room_numbers.data.split(",")
            d1 = datetime.datetime.combine(reservation.checkin_date.data, datetime.time(0, 0))
            d2 = datetime.datetime.combine(reservation.checkout_date.data, datetime.time(0, 0))
            num = reservation.num_guests.data

            all_reserves = Reservations.query.all()
            all_bookings = Booked.query.all()
            all_rooms = Rooms.query.all()

            if d2 <= d1 or d1 < datetime.datetime.now() or d2 < datetime.datetime.now():
                flash("Please recheck your date! It has to be at least today! ")
                return redirect(url_for('reserve'))
            total_num = 0
            for each in room_list:
                for each_reserves in all_reserves:
                    for each_booking in all_bookings:
                        c1 = each_reserves.checkin_date
                        c2 = each_reserves.checkout_date
                        if each_booking.room_id == int(each) and (
                                (c1 <= d1 and d2 <= c2) or (d1 <= c1 and d2 <= c2) or (c1 <= d1 and c2 <= d2) or (
                                d1 <= c1 and c2 <= d2)):
                            flash("The room you are reserving is not available at the time you selected!")
                            return redirect(url_for('reserve'))
            for each in room_list:
                for each_room in all_rooms:
                    if int(each) == each_room.room_number:
                        total_num += each_room.capacity
            if num > total_num:
                flash(
                    "The rooms you selected can't fit the number of guests you entered. Please restart the reservation!")
                return redirect(url_for('reserve'))
            reserve = Reservations(us.uid, reservation.checkin_date.data, reservation.checkout_date.data,
                                   reservation.num_guests.data, 0)
            db.session.add(reserve)
            db.session.commit()
            reservations_committed = Reservations.query.filter_by(ruid=us.uid).all()

            # Getting the most current reservation the user made
            current_id = 0
            for each in reservations_committed:
                if each.rid > current_id:
                    current_id = each.rid
            # Storing each rooms booked into the Booked table along with reservation id
            for each in room_list:
                single_room = Booked(current_id, each)
                db.session.add(single_room)
                db.session.commit()
            cur_res = Reservations.query.get(current_id)
            cur_res.costs = cal_cost(current_id)
            db.session.commit()
            return redirect(url_for('show_rooms'))
        return render_template('reservation.html', reservation=reservation)
    flash("User Not Authenticated !")
    return redirect(url_for('index'))


def cal_cost(rid):
    booked_room_list = Booked.query.filter_by(brid=rid).all()
    room_list = Rooms.query.all()
    cost_daily = 0
    for each in booked_room_list:
        each_room_id = each.room_id
        for e in room_list:
            if each_room_id == e.room_number:
                cost_daily += e.cost
    cur_res = Reservations.query.get(rid)
    checkin = cur_res.checkin_date
    checkout = cur_res.checkout_date
    dateRange = (checkout - checkin).days
    total_cost = cost_daily * dateRange
    return total_cost


@app.route('/payment/<rid>', methods=['GET', 'POST'])
def payment(rid):
    if session['user_available']:
        payment = PaymentForm(request.form)
        us = User.query.filter_by(username=session['current_user']).first()
        if request.method == "POST":
            pd = Payment(us.uid, rid, payment.cardname.data, payment.cardnumber.data, "Confirmed")
            db.session.add(pd)
            db.session.commit()
            return redirect(url_for('show_rooms'))
    return render_template('payment.html', payment=payment)


if __name__ == '__main__':
    app.run()
