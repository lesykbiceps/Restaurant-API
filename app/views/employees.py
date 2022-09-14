from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import EmployeeModel
from app.decorators import admin_group_required

employees_bp = Blueprint('employees', __name__)


@employees_bp.route("/employees", methods=["GET"])
@jwt_required()
@admin_group_required
def get_employees():
    """
        Get all employees from database. This function does not accept parameters and can be called only by admin
            Returns:
                All employees as list of dictionaries.
        """
    employees = EmployeeModel.return_all()
    return jsonify(employees)


@employees_bp.route("/employees/<int:id_>", methods=["GET"])
@jwt_required()
@admin_group_required
def get_employee(id_):
    """
        Get some specific employee from database. This function  accept id_ parameters.
        Only admin can get employee
            Args:
                id_: id of employee what you want to get
            Returns:
                Employee with bring id.
        """
    employee = EmployeeModel.find_by_id(id_)
    if not employee:
        return jsonify({"message": "Employee not found."}), 404

    return jsonify(employee)


@employees_bp.route("/employees", methods=["POST"])
@jwt_required()
@admin_group_required
def create_employee():
    """
        Create  employee with some fields. Only admins can create user. Password will store as hashed field.
        Admin should fill in all fields to create an employee. Default value for field "is_admin": false
            Example:
                >> {"name":'test',"username":'test_username', "password":'test_pass',
                "email":'test@gmail.com',"is_admin":True}
            Returns:
                "id":2, "name": 'test'
        """
    if not request.json:
        return jsonify({"message": 'Please, specify "username", "name","email" and "password".'}), 400

    name = request.json.get("name")
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    is_admin = request.json.get("is_admin", False)
    if not (name and username and email and password):
        return jsonify({"message": 'Please, specify "username", "name", "email", and "password".'}), 400

    employee = EmployeeModel(
        name=name, username=username, is_admin=is_admin, email=email,
        hashed_password=EmployeeModel.generate_hash(password))
    employee.save_to_db()

    return jsonify({"id": employee.id, "name": employee.name}), 201


@employees_bp.route("/employees/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_employee(id_):
    """
        Update some field in employee object or all fields. Only admins can update employee.
        If employee doesn't exist it will return message: "Employee not found"
            Example:
                >> {"name":'Bob'}
            Args:
                id_: id of employee what you want to update
            Returns:
                "message":"Updated"
        """
    name = request.json.get("name")
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    is_admin = request.json.get("is_admin")

    employee = EmployeeModel.find_by_id(id_, to_dict=False)
    if not employee:
        return jsonify({"message": "Employee not found."}), 404

    if isinstance(is_admin, bool):
        employee.is_admin = is_admin
    if name:
        employee.name = name
    if username:
        employee.username = username
    if email:
        employee.email = email
    if password:
        employee.hashed_password = EmployeeModel.generate_hash(password)
    employee.save_to_db()
    return jsonify({"message": "Updated"})


@employees_bp.route("/employees/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_employee(id_):
    """
        Delete employee object by id. Only admins can delete employee.
        If employee doesn't exist it will return message: "Employee not found"
            Args:
                id_: id of employee what you want to delete
            Returns:
                "message":"Employee was successfully deleted"
        """
    code = EmployeeModel.delete_by_id(id_)
    if code == 404:
        return jsonify({"message": "Employee not found."}), 404

    return jsonify({"message": "Deleted"})
