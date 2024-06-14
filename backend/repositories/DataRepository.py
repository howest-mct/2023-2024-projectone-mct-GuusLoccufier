from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_history():
        sql = "SELECT h.id, d.name as device, a.name as action, h.session_id as session, h.parameters, h.timestamp FROM history h JOIN devices d ON h.device_id = d.id JOIN actions a ON h.action_id = a.id ORDER BY h.id DESC"
        return Database.get_rows(sql)

    @staticmethod
    def create_event(device_id, action_id, parameters, session_id):
        sql = "INSERT INTO history (device_id, action_id, parameters, session_id) VALUES (%s,%s,%s,%s)"
        params = [device_id, action_id, parameters, session_id]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def get_users():
        sql = "SELECT id, username FROM users"
        return Database.get_rows(sql)

    @staticmethod
    def get_courses():
        sql = "SELECT id, name FROM trainingcourses"
        return Database.get_rows(sql)

    @staticmethod
    def get_sequence(id):
        sql = "SELECT sequence from trainingcourses WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def start_session(user_id, training_course_id):
        sql = "INSERT INTO sessions (user_id, training_course_id) VALUES (%s, %s)"
        params = [user_id, training_course_id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def stop_session(session_id):
        sql = "UPDATE sessions SET end_time = NOW() WHERE id = %s"
        params = [session_id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def add_course(name, sequence):
        sql = "INSERT INTO trainingcourses (name, sequence) VALUES (%s,%s)"
        params = [name, sequence]
        return Database.execute_sql(sql, params)

    # @staticmethod
    # def read_status_lamp_by_id(id):
    #     sql = "SELECT * from lampen WHERE id = %s"
    #     params = [id]
    #     return Database.get_one_row(sql, params)
    #
    # @staticmethod
    # def update_status_lamp(id, status):
    #     sql = "UPDATE lampen SET status = %s WHERE id = %s"
    #     params = [status, id]
    #     return Database.execute_sql(sql, params)
    #
    # @staticmethod
    # def update_status_alle_lampen(status):
    #     sql = "UPDATE lampen SET status = %s"
    #     params = [status]
    #     return Database.execute_sql(sql, params)
