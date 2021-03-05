import sqlite3
import datetime
import time
import smtplib
import imghdr
from email.message import EmailMessage

conn = sqlite3.connect('covid.db')
c = conn.cursor()

notify_group = list()

def enter_data():
    def create_table():
        c.execute('''CREATE TABLE IF NOT EXISTS
        covidTrack(
        name TEXT,
        email TEXT,
        ph_number INTEGER,
        datestamp TEXT,
        keyword TEXT)''')

    i_name = str(input('Please insert FULL NAME : \n ...'))

    i_email = str(input('Please insert EMAIL : \n ...'))

    i_number = int(input('Please insert PHONE NUMBER : \n ...'))


    print('Your data has been saved for acelerated contact, thank you. \n')
    time.sleep(1)


    def data_entry():
        date, keyword = dynamic_data_entry()
        c.execute('''INSERT INTO covidTrack
        VALUES(?, ?, ?, ?, ?)''', (i_name, i_email, i_number, date, keyword))
        conn.commit()


    def dynamic_data_entry():
        keyword = 'nameofvenue'
        date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        return date, keyword
        conn.commit()

    def read_from_db():
        c.execute('''SELECT * FROM covidTrack''')
        conn.commit()

    create_table()
    data_entry()
    read_from_db()
    menu()

def data_search():
    x = input('''Select desired search: \n
    Search by FULL NAME. \n
    Search by DATE AND TIME. \n
    Search by PHONE NUMBER. \n
    NOTIFY CASES. \n
    Exit.
    ~
    ''')

    if x.lower() == 'full name':
         specify_name = input('Please insert full name. \n ')
         select_query = c.execute('''SELECT * FROM covidTrack WHERE NAME ==(?) ''', (specify_name,))
         for row in c.fetchall():
             print('\n')
             print('Name:', row[0])
             print('Email:', row[1])
             print('Phone Number:', row[2])
             print('Date and Time:', row[3])
             print('Venue:', row[4])
             print('\n')
             c.execute('''SELECT *
             FROM covidTrack
             WHERE datestamp >= ?
             AND datestamp <= datetime(?, '+1 hours')  ''', (row[3],row[3]))
             print('Matching Results: \n ')
             for row2 in c.fetchall():
                 print(row2)
                 notify_group.append(row2[1])
                 print('\n')

             add_people = input('Would you like to notify this group?Y/N')

             if add_people.lower() == 'y':
                 SendMail()
                 print('All the people in this search has been advised.')
             if add_people.lower() == 'n':
              menu()


    if x.lower() == 'date and time':
        specify_datestamp = input('''Please insert full date as shown.
        \n
        Please follow this format...
        \n
        YYYY-MM-DD HH:MM:SS ''')

        c.execute('''SELECT * FROM covidTrack WHERE datestamp == ? ''', (specify_datestamp,))
        for row in c.fetchall():
             print('\nName:', row[0])
             print('Email:', row[1])
             print('Phone Number:', row[2])
             print('Date and Time:', row[3])
             print('Venue:', row[4])
             print('\n')
             d = row[3]

             c.execute('''SELECT *
             FROM covidTrack
             WHERE datestamp >= ?
             AND datestamp <= datetime(?, '+1 hours')  ''',(d,d))
             print('Matching Results: \n')
             for row2 in c.fetchall():
                 print(row2[0:4])
             menu()

    if x.lower() == 'exit':
        exit()

def SendMail():
    msg = EmailMessage()
    msg['Subject'] = 'covidTrack notification.'
    msg['From'] = '##########'
    msg['To'] = notify_group
    msg.set_content('It has been confirmed that you were a close contact in. Please contact us as soon as possible.')

    print(notify_group)

    with open('##########', 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('##########', '##########')

        smtp.send_message(msg)


def menu():
    choose_funtion = input('''Please choose action: \n
    A TO ENTER DATA. \n
    B TO SEARCH DATA. \n
    EXIT \n ''')

    if choose_funtion.lower() == 'a':
        print('You choose enter data.')
        enter_data()
    if choose_funtion.lower() == 'b':
        print('You choose search data.')
        data_search()
    if choose_funtion.lower() == 'exit':
        exit()
menu()
c.close()
conn.close()
