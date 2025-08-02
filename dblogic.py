# The Entire Database Code is Written Here.
import mysql.connector as msc

from crud import curobj


class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conobj = msc.connect(host = "localhost",
                                 user = "root",
                                 passwd = "dinox",
                                 database = 'flights2')
            # creating cursor object
            self.curobj = self.conobj.cursor()
        except msc.DatabaseError as dbe:
            print(f"The Problem In DB: {dbe}")

    # method to get unique names of cities for whenever user selects "source" and "destination" then to show
    # city names as dropdown.
    def fetch_city_names(self):
        cities = []
        self.curobj.execute("""
        SELECT DISTINCT(source) FROM flights
        UNION
        SELECT DISTINCT(destination) FROM flights
        """ )
        # fetching records from cursor object
        data = self.curobj.fetchall()
        for item in data:
            cities.append(item[0])
        return cities # ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai', 'New Delhi', 'Cochin', 'Hyderabad']

    # method to get flights based on source and destination which is selected by user.
    def get_all_flights(self,src_city,des_city):
        col_list = []
        self.curobj.execute(f"""
        SELECT * FROM flights
        WHERE source = '{src_city}' AND destination = '{des_city}' AND Date_of_Journey >= CURRENT_DATE()
        """)
        # ************ Getting Meta Data of Our Table which is stored in Mysql DB ************
        columnsinfo = self.curobj.description  # List of tuples
        for eachcolumninfo in columnsinfo:
            # print(eachcolumninfo) --> ('EID', <DbType DB_TYPE_NUMBER>, 6, None, 5, 0, False)
            col_list.append(eachcolumninfo[0])  # displaying only column names

        # fetching records from cursor object
        data = self.curobj.fetchall()
        # getting number of rows we got
        row_count = self.curobj.rowcount
        # returning all columns, result set data and row_count to method call
        return col_list,data,row_count

    # method to get airlines and its frequency
    def fetch_airline_frequency(self):
        airlines = []
        frequency = []
        self.curobj.execute('''
        SELECT airline, COUNT(*) 
        FROM flights
        WHERE Date_of_Journey <= current_date() 
        GROUP BY airline;
        ''')

        # fetching records from cursor object
        data = self.curobj.fetchall()

        # The above data contains 2 columns data which is airline and frequency,
        # now we can add this data to 2 different lists, one is airlines and other is frequency list
        for item in data:
            airlines.append(item[0])
            frequency.append(item[1])
        # finally return this 2 list to calling method.
        return airlines, frequency

    # method to get busiest airport cities
    def get_busiest_airports(self):
        cities = []
        tot_io_flights = []
        self.curobj.execute ('''
        SELECT cities,sum(num_of_flights) AS 'total_in_out_flights'
        FROM (select source as cities,count(*) AS 'num_of_flights'
              FROM flights WHERE Date_of_Journey <= current_date() 
              GROUP BY source
              UNION ALL
              SELECT destination, count(*) 
              FROM flights WHERE Date_of_Journey <= current_date()
              GROUP BY destination) t
        GROUP BY t.cities
        ORDER BY sum(num_of_flights) DESC;
        ''')

        # fetching records from cursor object
        data = self.curobj.fetchall()

        # The above data contains 2 columns data which is cities and total_in_out_flights,
        # now we can add this data to 2 different lists, one is cities and other is tot_io_flights list
        for item in data:
            cities.append(item[0])
            tot_io_flights.append(item[1])
        # finally return this 2 list to calling method.
        return cities, tot_io_flights

    # method to get total_flights per day irrespective of any airlines just want
    # total_flights per day.
    def get_daily_frequency(self):
        dates = []
        frequency1 = []
        self.curobj.execute ('''
        SELECT Date_of_Journey, count(*)
        FROM flights
        WHERE Date_of_Journey <= current_date()
        GROUP BY Date_of_Journey;
        ''')

        # fetching records from cursor object
        data = self.curobj.fetchall()

        # The above data contains 2 columns data which is dates and frequency1,
        # now we can add this data to 2 different lists, one is datres and other is frequency1 list
        for item in data:
            dates.append(item[0])
            frequency1.append(item[1])
        # finally return this 2 list to calling method.
        return dates, frequency1