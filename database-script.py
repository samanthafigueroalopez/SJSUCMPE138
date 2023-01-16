# SJSU CMPE 138 FALL 2022 TEAM1

import sqlite3
#import os
from cryptography.fernet import Fernet

import sqlite3
connection = sqlite3.connect('235fitness.db')
cursor = connection.cursor()

def encrypt(pw):
    with open('key.txt', 'r') as f:
        key =f.read()
        f = Fernet(key)

        return str(f.encrypt(bytes(pw, encoding='utf-8')).decode('utf-8'))

# creating gym table
# add later-foreign key mgr_ssn references manager m_ssn on delete cascade
cursor.execute("""create table gym
(
    gym_id int(8) not null,
    gym_address varchar,
    gym_phone varchar(10),
    mgr_ssn varchar(9) not null,
    primary key (gym_id)
)
""")

# creating equipment table
cursor.execute("""create table equipment
(
    eq_id int(8) not null,
    eq_name varchar,
    gym_id int(8),
    primary key (eq_id),
    foreign key (gym_id) references gym(gym_id) on delete cascade
)
""")

# creating facility table
cursor.execute("""create table facility
(
    fc_id int(8) not null,
    fc_name varchar,
    gym_id int(8),
    primary key (fc_id),
    foreign key (gym_id) references gym(gym_id) on delete cascade
)
""")

# creating employee table
# password not null
cursor.execute("""create table employee
(
    ssn varchar(9) not null,
    e_id int(8) not null,
    e_name varchar,
    e_hours int,
    salary decimal(10,2),
    e_phone varchar(10),
    e_email varchar,
    password nvarchar,
    gym_id int(8),
    primary key(ssn),
    foreign key (gym_id) references gym(gym_id) on delete cascade
)
""")

# creating manager table
cursor.execute("""create table manager
(
    m_ssn varchar(9) not null,
    ma_password nvarchar not null,
    e_id int(8) not null,
    primary key(m_ssn,e_id),
    foreign key (m_ssn) references employee(ssn) on delete cascade,
    foreign key (e_id) references employee(e_id) on delete cascade
)
""")

# creating receptionist table
cursor.execute("""create table receptionist
(
    r_ssn varchar(9) not null,
    primary key(r_ssn),
    foreign key (r_ssn) references employee(ssn) on delete cascade
)
""")

# creating trainer table
cursor.execute("""create table trainer
(
    t_ssn varchar(9) not null,
    primary key(t_ssn),
    foreign key (t_ssn) references employee(ssn) on delete cascade
)
""")

# creating class table
cursor.execute("""create table class
(
    cl_id int(8) not null,
    cl_name varchar,
    gym_id int(8) not null,
    rating int,
    trainer_ssn varchar(9),
    primary key (cl_id),
    foreign key (trainer_ssn) references trainer(t_ssn) on delete cascade
    foreign key (gym_id) references gym(gym_id) on delete cascade
)
""")

# creating host table
cursor.execute("""create table host
(
    cl_id int(8) not null,
    gym_id int(8) not null,
    primary key(cl_id,gym_id),
    foreign key (cl_id) references class(cl_id) on delete cascade
    foreign key (gym_id) references gym(gym_id) on delete cascade
)
""")

# creating member table
cursor.execute("""create table member
(
    m_id int(8) not null,
    m_type char,
    m_name varchar,
    start_date date,
    end_date date,
    payment decimal(10,2),
    m_email varchar,
    m_phone varchar(10),
    password nvarchar,
    trainer_ssn varchar(9),
    primary key(m_id),
    foreign key (trainer_ssn) references trainer(t_ssn) on delete cascade
)
""")

# creating edit table
cursor.execute("""create table edit
(
    receptionist_ssn varchar(9) not null,
    m_id int(8) not null,
    primary key (receptionist_ssn, m_id),
    foreign key (receptionist_ssn) references receptionist(r_ssn) on delete cascade
    foreign key (m_id) references member(m_id) on delete cascade
)
""")

# creating has table
cursor.execute("""create table has
(
    gym_id int(8) not null,
    m_id int(8) not null,
    primary key (gym_id,m_id),
    foreign key (gym_id) references gym(gym_id) on delete cascade
    foreign key (m_id) references member(m_id) on delete cascade
)
""")

# creating use table
cursor.execute("""create table use
(
    m_id int(8) not null,
    fc_id int(8) not null,
    primary key (m_id,fc_id),
    foreign key (m_id) references member(m_id) on delete cascade
    foreign key (fc_id) references facility(fc_id) on delete cascade
)
""")

pw = encrypt('root')
pw2 = encrypt('test')
# inserting dummy data
cursor.execute(
    """insert into gym values(1,'99 ALAMEDA SAN JOSE', 408408401, 123456781)""")

cursor.execute("""insert into equipment values(1,'Treadmill', 1)""")

cursor.execute("""insert into facility values(1,'Cardio', 1)""")

cursor.execute(
    "insert into employee values(123456781, 1, 'John Smith', 40, 100000, 408408402, 'john@gym.com', '"+pw+"' , 1)")
cursor.execute(
    "insert into employee values(123456782, 2, 'Tiffany Rhodes', 40, 70000, 408408403, 'tiffany@gym.com', '"+pw+"', 1)")
cursor.execute(
    "insert into employee values(123456783, 2, 'Roger Penn', 40, 95000, 408408404, 'roger@gym.com', '"+pw+"', 1)")

cursor.execute("insert into manager values(123456781, '"+pw2+"', 1)")
cursor.execute("""insert into receptionist values(123456782)""")
cursor.execute("""insert into trainer values(123456783)""")

cursor.execute(
    """insert into class values(1,'Strength Training', 1, 4, 123456783)""")

cursor.execute("""insert into host values(1, 1)""")

cursor.execute("insert into member values(1, 'member', 'Grace Matilda', '2022-01-01', '2022-12-31', 999, 'grace@gmail.com', 669669661, '"+pw+"', 123456783)")

cursor.execute("""insert into edit values(123456782, 1)""")

cursor.execute("""insert into has values(1, 1)""")

cursor.execute("""insert into use values(1, 1)""")


connection.commit()
connection.close()
