from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from app.models import VoteModel, MenuModel, EmployeeModel, session
from app.decorators import admin_group_required

votes_bp = Blueprint('votes', __name__)


@votes_bp.route("/votes", methods=["GET"])
@jwt_required()
@admin_group_required
def get_votes():
    """
        Get all votes from database. This function does not accept parameters
            Returns:
                All votes as list of dictionaries.
    """
    votes = VoteModel.return_all()
    return jsonify(votes)


@votes_bp.route("/myvotes", methods=["GET"])
@jwt_required()
@admin_group_required
def get_my_votes():
    """
        User can view the history of votes. This function does not accept parameters
                Returns:
                    All user's votes as list of dictionaries.
        """
    jwt = get_jwt()
    name = jwt.get("sub")
    employee = session.query(EmployeeModel).filter(EmployeeModel.name == name).first()
    id_ = EmployeeModel.id
    votes = VoteModel.find_by_employee_id(id_, 0, 10)
    return jsonify(votes)


@votes_bp.route("/votes/<int:id_>", methods=["GET"])
@jwt_required()
@admin_group_required
def get_votes_by_menu_id(id_):
    """
        Admin can get some votes for specific menu from database.
        This function  accept id_ parameters - menu_id.
            Args:
                id_: id of menu what you want to get
            Returns:
                Votes with bring menu_id.
        """
    votes = VoteModel.find_by_menu_id(id_, 0, 75)
    if not votes:
        return jsonify({"message": "Votes not found."}), 404

    return jsonify(votes)


@votes_bp.route("/votes", methods=["POST"])
@jwt_required()
def create_vote():
    """
        The main method of this program is responsible for voting.
        Using the method above, you can vote.
            Example:
                >> {"menu_id":1,"employee_id":1}
            Returns:
                "id":1, "employee_id": 1
        """
    if not request.json:
        return jsonify({"message": 'Please, specify "menu_id", "employee_id".'}), 400
    menu_id = request.json.get("menu_id")
    employee_id = request.json.get("employee_id")
    if not (menu_id and employee_id):
        return jsonify({"message": 'Please, specify "menu_id", "employee_id".'}), 400


    menu = MenuModel.find_by_id(menu_id)
    employee = EmployeeModel.find_by_id(employee_id)
    votes = VoteModel.return_all()
    vote_lst =[]
    for elem in votes:
        vote_lst.append(elem['employee_id'])
    if employee_id in vote_lst:
        return jsonify({"message": 'An employee can vote only once a day.'}), 400
    if menu and employee:
        vote = VoteModel(
            menu_id=menu_id, employee_id=employee_id)
        vote.save_to_db()

        menu = MenuModel.find_by_id(menu_id, to_dict=False)
        menu.adjust_number_votes(menu_id)

        return jsonify({"id": vote.id, "employee_id": vote.employee_id}), 201
    else:
        return jsonify({"message": 'Such "menu_id" or(and) "employee_id" does not exist.'}), 400