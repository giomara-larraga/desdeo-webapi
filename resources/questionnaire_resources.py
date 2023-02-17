from app import db
import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, reqparse
from models.questionnaire_models import Question, Answer, Questionnaire
from models.user_models import UserModel
import simplejson as json

class QuestionnaireDemographic(Resource):
    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            question_list = Question.query.filter_by(questionnaire_id=1).all()

            response = {
                "questions": [
                    {
                        "id": question.id,
                        "question_text": question.question_txt,
                        "question_type": question.question_type,
                        "show_solution": question.show_solution,
                    }
                    for question in question_list
                ]
            }

            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404

class QuestionnaireInit(Resource):
    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            question_list = Question.query.filter_by(questionnaire_id=2).all()

            response = {
                "questions": [
                    {
                        "id": question.id,
                        "question_text": question.question_txt,
                        "question_type": question.question_type,
                        "show_solution": question.show_solution,
                    }
                    for question in question_list
                ]
            }

            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404


class QuestionnaireEnd(Resource):
    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            question_list = Question.query.filter_by(questionnaire_id=3).all()

            response = {
                "questions": [
                    {
                        "id": question.id,
                        "question_text": question.question_txt,
                        "question_type": question.question_type,
                        "show_solution": question.show_solution,
                    }
                    for question in question_list
                ]
            }

            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404

class QuestionnaireSwitch(Resource):
    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            question_list = Question.query.filter_by(questionnaire_id=4).all()

            response = {
                "questions": [
                    {
                        "id": question.id,
                        "question_text": question.question_txt,
                        "question_type": question.question_type,
                        "show_solution": question.show_solution,
                    }
                    for question in question_list
                ]
            }

            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404