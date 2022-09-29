from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:0000@localhost:5432/website"
db = SQLAlchemy(app)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    position = db.Column(db.String(150))

    def __init__(self, firstName, lastName, position):
        self.firstName = firstName
        self.lastName = lastName
        self.position = position

    def __repr__(self):
        return '<Employee %r>' % self.id


class EmployeesSchema(Schema):
    id = fields.Integer()
    firstName = fields.String()
    lastName = fields.String()
    position = fields.String()


# db.create_all()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello'})


@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employees.query.all()
    return jsonify(EmployeesSchema(many=True).dump(employees))


@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    employee = Employees(
        firstName=data.get('firstName'),
        lastName=data.get('lastName'),
        position=data.get('position')
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(EmployeesSchema().dump(employee)), 201


@app.route('/employees/<int:id>', methods=['GET'])
def get_employeeby_id(id):
    employees = Employees.query.get_or_404(id)
    return jsonify(EmployeesSchema().dump(employees)), 200


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employees.query.get_or_404(id)
    data = request.get_json()
    employee.firstName = data.get('firstName')
    employee.lastName = data.get('lastName')
    employee.position = data.get('position')

    db.session.commit()
    return jsonify(EmployeesSchema().dump(employee)), 200


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employees.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Deleted"}), 204


if __name__ == '__main__':
    app.run(debug=True)
