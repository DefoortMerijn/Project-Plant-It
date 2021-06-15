from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_log():
        sql = "SELECT * from DeviceLog"
        return Database.get_rows(sql)

    @staticmethod
    def create_log(Sensor, Value, Plant):
        sql = "INSERT INTO DeviceLog(Sensor,Value,Plant) VALUES(%s,%s,%s)"
        params = [Sensor, Value, Plant]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_log_today(SensorId):
        sql = "SELECT * FROM DeviceLog WHERE Sensor = %s AND DATE(Date) = CURDATE()"
        params = [SensorId]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_livefeed_sensors(SensorId):
        sql = "SELECT * FROM DeviceLog Where Sensor = %s ORDER BY Id DESC LIMIT 1 "
        params = [SensorId]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_name_plants():
        sql = "SELECT * FROM Plants"
        return Database.get_rows(sql)

    @staticmethod
    def read_moisture_plant(plant_id):
        sql = 'SELECT Moisture FROM Plants WHERE Id = %s'
        params = [plant_id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_last_timer():
        sql = 'SELECT Time, DayOfTheWeek FROM Alarm ORDER BY Id DESC LIMIT 1'
        return Database.get_one_row(sql)

    @staticmethod
    def add_timer(Name, Time, Day, Plant):
        sql = 'INSERT INTO Alarm(Name,Time,DayOfTheWeek,Plant) VALUES(%s,%s,%s,%s)'
        params = [Name, Time, Day, Plant]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_moisture_for_alarm():
        sql = 'SELECT p.Moisture FROM Alarm a INNER JOIN Plants p on a.Plant = p.id Order BY p.Id DESC LIMIT 1;'
        return Database.get_one_row(sql)
