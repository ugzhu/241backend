import re
from flask import Flask, redirect, request
from flask_restful import Resource, Api
from mysql_connector import Database
from flask_cors import CORS

__author__ = 'Yujie Zhu'

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return "Backend service is up and ready for API calls!"


class ListAll(Resource):
    @staticmethod
    def get():
        events = []
        sql = "SELECT * FROM Event;"
        res = Database(sql).execute()
        for r in res:
            eid = r[0]
            name = r[1]
            date = r[2]
            place = r[3]
            sport = r[4]
            # user_list = []
            # sql = f"SELECT user_name FROM EventHasUser WHERE EID={eid}"
            # user = Database(sql).execute()
            # for u in user:
            #     user_list.append(u[0])
            event = {'eid': eid, 'event_name': name, 'date': date,
                     'place': place, 'sport': sport}
            events.append(event)
        return events


class GetEvent(Resource):
    @staticmethod
    def get(eid):
        event_sql = f"SELECT * FROM Event WHERE EID = {eid};"
        event_res = Database(event_sql).execute()
        # print(event_res)
        if not event_res:
            return "Requested event does not exist.", 404

        user_sql = f"SELECT user_name FROM EventHasUser WHERE EID={eid}"
        user_res = Database(user_sql).execute()
        user_list = []
        for u in user_res:
            user_list.append(u[0])
        event = {'eid': eid, 'event_name': event_res[0][1], 'date': event_res[0][2],
                 'place': event_res[0][3], 'sport': event_res[0][4], 'user_list': user_list}

        return event


class NewEvent(Resource):
    @staticmethod
    def post():
        json_req = request.get_json(force=True)
        try:
            event_name = str(json_req['event_name'])
            date = str(json_req['date'])
            place = str(json_req['place'])
            sport = str(json_req['sport'])
            user_name = str(json_req['user_name'])
        except KeyError:
            return "Required keys do not exist in request.", 400

        if not re.match("^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$", date):
            return "Incorrect date format, required MM/DD/YYYY", 400

        new_event_sql = f"INSERT INTO Event(event_name, event_date, event_place, event_sport) " \
                        f"VALUES ('{event_name}', '{date}', '{place}', '{sport}');"
        try:
            Database(new_event_sql).execute()
        except Exception as e:
            return str(e), 400

        get_eid_sql = f"SELECT EID FROM Event WHERE event_name = '{event_name}' AND event_date = '{date}' " \
                      f"AND event_place = '{place}' AND event_sport = '{sport}';"
        try:
            eid = Database(get_eid_sql).execute()[-1][0]
        except Exception as e:
            return str(e), 400

        add_user_sql = f"INSERT INTO EventHasUser(EID, user_name) " \
                       f"VALUES({eid},'{user_name}');"
        try:
            Database(add_user_sql).execute()
        except Exception as e:
            return str(e), 400

        return redirect(f'/api/get_event/{eid}')


class AddUser(Resource):
    @staticmethod
    def post():
        json_req = request.get_json(force=True)
        try:
            eid = int(json_req['eid'])
            user_name = str(json_req['user_name'])
        except KeyError:
            return "Required keys do not exist in request.", 400

        sql = f"INSERT INTO EventHasUser(user_name, EID) " \
              f"VALUES('{user_name}', {eid});"

        try:
            Database(sql).execute()
        except Exception as e:
            return str(e), 400

        return f"User {user_name} added to Event {eid}", 200


class DeleteUser(Resource):
    @staticmethod
    def delete():
        json_req = request.get_json(force=True)
        try:
            eid = int(json_req['eid'])
            user_name = str(json_req['user_name'])
        except KeyError:
            return "Required keys do not exist in request.", 400

        sql = f"DELETE FROM EventHasUser WHERE EID = {eid} AND user_name = '{user_name}';"

        try:
            Database(sql).execute()
        except Exception as e:
            return str(e), 400

        return f"User {user_name} deleted from event {eid}"


class DeleteEvent(Resource):
    @staticmethod
    def delete():
        json_req = request.get_json(force=True)
        try:
            eid = int(json_req['eid'])
        except KeyError:
            return "Required keys do not exist in request.", 400

        sql = f"DELETE FROM EventHasUser WHERE EID = {eid};"

        try:
            Database(sql).execute()
        except Exception as e:
            return str(e), 400

        sql = f"DELETE FROM Event WHERE EID = {eid};"

        try:
            Database(sql).execute()
        except Exception as e:
            return str(e), 400

        return f"Event {eid} deleted."




# class SendSql(Resource):
#     @staticmethod
#     def post():
#         try:
#             json_req = request.get_json(force=True)
#             if 'sql' in json_req:
#                 sql = json_req['sql']
#             else:
#                 return "400 Bad Request", 400
#             db = Database(sql)
#             res = db.execute()
#             del db
#             print(res)
#             return res
#         except Exception:
#             return "500 SQL Error", 500


# api.add_resource(SendSql, '/api/send_sql')
api.add_resource(ListAll, '/api/list_all')
api.add_resource(GetEvent, '/api/get_event/<int:eid>')
api.add_resource(NewEvent, '/api/new_event')
api.add_resource(AddUser, '/api/add_user')
api.add_resource(DeleteUser, '/api/delete_user')
api.add_resource(DeleteEvent, '/api/delete_event')

if __name__ == '__main__':
    app.run(debug=False)
