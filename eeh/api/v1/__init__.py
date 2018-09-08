from main import APP
from eeh.models import Harcerz, User
from flask import jsonify

@APP.route("/api/v1/harcerz/<identifier>/", methods=['GET'])
def harcerz(identifier):
    temp = Harcerz.query.filter_by(id=identifier).first()
    druzyna = Druzyna.query.filter_by(id=temp.druzyna).first()
    info = {
        'id' : temp.id,
        'name' : temp.first_name,
        'mid-name' : temp.second_name,
        'last-name' : temp.last_name,
        'birthdate' : temp.birthdate,
        'pesel' : temp.pesel,
        'adress' : temp.adres,
        'contact' : temp.nrkont,
        'function' : temp.funkcja,
        'druzyna' : druzyna.name
    }
    return jsonify(info)

@APP.route("/api/v1/user/<identifier>/", methods=['GET'])
def druzyna(identifier):
    druzyna = Druzyna.query.filter_by(id=identifier).first()
    info = {
        'id' : druzyna.id,
        'name' : druzyna.name,
        'email' : druzyna.email,
        'access' : {
            'admin' : druzyna.admin,
            'ban' : druzyna.ban
        }
    }
    return jsonify(info)
