from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from config import Config
from extensions import db
import models

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html', current_page='main')

# --- CLIENTS ---
@app.route('/clients')
def list_clients():
    clients = models.Client.query.all()
    return render_template('clients.html', clients=clients, current_page='clients')

@app.route('/clients/add', methods=['GET','POST'])
def add_client():
    if request.method == 'POST':
        c = models.Client(
            full_name=request.form['full_name'],
            contacts=request.form['contacts'],
            goal=request.form['goal']
        )
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('list_clients'))
    return render_template('client_form.html', client=None)

@app.route('/clients/edit/<int:id>', methods=['GET','POST'])
def edit_client(id):
    client = models.Client.query.get_or_404(id)
    if request.method == 'POST':
        client.full_name = request.form['full_name']
        client.contacts = request.form['contacts']
        client.goal = request.form['goal']
        db.session.commit()
        return redirect(url_for('list_clients'))
    return render_template('client_form.html', client=client)

@app.route('/clients/delete/<int:id>')
def delete_client(id):
    # удаляем абонементы
    models.Subscription.query.filter_by(client_id=id).delete()
    # удаляем клиента
    client = models.Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('list_clients'))

# --- TRAINERS ---
@app.route('/trainers')
def list_trainers():
    trainers = models.Trainer.query.all()
    return render_template('trainers.html', trainers=trainers, current_page='trainers')

@app.route('/trainers/add', methods=['GET','POST'])
def add_trainer():
    if request.method=='POST':
        t = models.Trainer(
            full_name=request.form['full_name'],
            specialization=request.form['specialization'],
            schedule=request.form['schedule']
        )
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('list_trainers'))
    return render_template('trainer_form.html', trainer=None)

@app.route('/trainers/edit/<int:id>', methods=['GET','POST'])
def edit_trainer(id):
    trainer = models.Trainer.query.get_or_404(id)
    if request.method=='POST':
        trainer.full_name = request.form['full_name']
        trainer.specialization = request.form['specialization']
        trainer.schedule = request.form['schedule']
        db.session.commit()
        return redirect(url_for('list_trainers'))
    return render_template('trainer_form.html', trainer=trainer)

@app.route('/trainers/delete/<int:id>')
def delete_trainer(id):
    trainer = models.Trainer.query.get_or_404(id)
    db.session.delete(trainer)
    db.session.commit()
    return redirect(url_for('list_trainers'))

# --- SUBSCRIPTIONS ---
@app.route('/subscriptions')
def list_subscriptions():
    subs = models.Subscription.query.order_by(models.Subscription.valid_until.desc()).all()
    clients = models.Client.query.all()
    return render_template('subscriptions.html', subscriptions=subs, clients=clients, current_page='subscriptions')

@app.route('/subscriptions/add', methods=['GET','POST'])
def add_subscription():
    clients = models.Client.query.all()
    if request.method=='POST':
        s = models.Subscription(
            client_id=request.form['client_id'],
            type=request.form['type'],
            valid_until=request.form['valid_until']
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('list_subscriptions'))
    return render_template('subscription_form.html', subscription=None, clients=clients)

@app.route('/subscriptions/edit/<int:id>', methods=['GET','POST'])
def edit_subscription(id):
    sub = models.Subscription.query.get_or_404(id)
    clients = models.Client.query.all()
    if request.method=='POST':
        sub.client_id = request.form['client_id']
        sub.type = request.form['type']
        sub.valid_until = request.form['valid_until']
        db.session.commit()
        return redirect(url_for('list_subscriptions'))
    return render_template('subscription_form.html', subscription=sub, clients=clients)

@app.route('/subscriptions/delete/<int:id>')
def delete_subscription(id):
    sub = models.Subscription.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()
    return redirect(url_for('list_subscriptions'))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)