#!/usr/local/python35/bin/python3
#-*- coding: utf-8 -*-

from flask_script import Manager, Shell
from app import create_app, db
from app.models import Customer
from flask_migrate import Migrate,MigrateCommand
from werkzeug.security import generate_password_hash
import random
import string


from app.model.execute_command import command_ready
from app.model.settings import Tables

def create_table():
    connectdb = command_ready()
    connectdb.create_raw_table()
    connectdb.create_rule_table()
    connectdb.create_customer_system_table()
    connectdb.operation_close()


app=create_app()
migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db)

#@manager.command
def add_system_auth(sys_id, asys_id, asys_key):
    customer = Customer(system_id=sys_id,access_system_id=asys_id,access_system_key=generate_password_hash(asys_key))
    db.session.add(customer)
    db.session.commit()
    db.session.close()

def generate_string():
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    print (ran_str)
 

def add_customer(cust_system_code, customer_code, customer_name, monitor_code, monitor_name, monitor_version, active_flg):
    connectdb = command_ready()
    connectdb.insert_customer_system(cust_system_code, customer_code, customer_name, monitor_code, monitor_name, monitor_version, active_flg)


def update_customer(cust_system_code, customer_code, monitor_code, monitor_version, active_flg):
    connectdb = command_ready()
    connectdb.update_customer_system(cust_system_code, customer_code, monitor_code, monitor_version, active_flg)


#def select_customer_system(


#manager.add_command("shell", Shell(make_context=make_shell_context))
if __name__ == '__main__':
    create_table()
    manager.run()
