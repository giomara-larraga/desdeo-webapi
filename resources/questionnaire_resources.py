from app import db
import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, reqparse
from models.questionnaire_models import Question, Answer, Questionnaire
from models.user_models import UserModel
import simplejson as json
from sqlalchemy import and_

class QuestionnaireDemographic(Resource):
    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            question_list = Question.query.filter_by(questionnaire_id=1).all()

            response = {
                "elements": [
                    {
                        "name": question.id,
                        "title": question.question_txt,
                        "type": question.question_type,
                        "isRequired": True
                    }
                    for question in question_list
                ],
                "showQuestionNumbers" : True
            }
            for element in response["elements"]:
                if element["title"] == "Age":
                    element["inputType"] = "number"
                    element["min"] = 0
                    element["max"] = 100
                    element["defaultValue"] = 0
                if element["title"] == "Gender":
                    element["showNoneItem"] = False
                    element["showOtherItem"] = False
                    element["choices"] = [ "Male", "Female", "Non-binary", "Prefer not to disclose"]
                if element["type"]=="Boolean":
                    element["valueTrue"] = "Yes"
                    element["valueFalse"] = "No"
                    element["renderAs"] = "radio"
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
                "elements": [
                    {
                        "name": question.id,
                        "title": question.question_txt,
                        "type": question.question_type,
                        "isRequired": True
                    }
                    for question in question_list
                ],
                "showQuestionNumbers" : True
            }
            for element in response["elements"]:
                if element["type"] == "rating":
                    element["minRateDescription"] = "Not tired"
                    element["maxRateDescription"] = "Very tired"
            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404

class QuestionnaireEnd(Resource):
    def _get_rows(self, id_page):
        question_list = Question.query.filter(Question.questionnaire_id==3,Question.page==id_page, Question.question_type=="matrix").all()
        response = {
            "rows": [
                {
                    "value": question.id,
                    "text": question.question_txt,
                }
                for question in question_list
            ],
        }
        return response
    
    def _get_open(self, id_page):
        count = Question.query.filter(Question.questionnaire_id==3,Question.page==id_page, Question.question_type=="text").count()
        if count == 1:
            question = Question.query.filter(Question.questionnaire_id==3,Question.page==id_page, Question.question_type=="text").first()
            question_r= {
                "name": question.id,
                "type": "text",
                "title": question.question_txt,
                "isRequired": False
            }
        else:
            question_r=None
        return question_r
    
    def _compose_element(self, id_page):
        rows = self._get_rows(id_page)["rows"]
        text_question = self._get_open(id_page)
        element= [
        {
            "type": "matrix",
            "name": "page"+str(id_page),
            "title": "Please indicate if you agree or disagree with the following statements",
            "columns": [{
                "value": 5,
                "text": "Strongly agree"
            }, {
                "value": 4,
                "text": "Agree"
            }, {
                "value": 3,
                "text": "Neutral"
            }, {
                "value": 2,
                "text": "Disagree"
            }, {
                "value": 1,
                "text": "Strongly disagree"
            }],
            "rows":rows,
            "alternateRows": True,
            "isAllRowRequired": True
        }
        ]
        if text_question !=None:
            element.append(text_question)

        return element

    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            num_pages = 3            
            response = {
            "pages": [
            {
                "elements": self._compose_element(j+1), 
            } for j in range(0,num_pages)
            ] 
            }
            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404

class QuestionnaireSwitch(Resource):
    def _get_rows(self, id_page):
        question_list = Question.query.filter(Question.questionnaire_id==4,Question.page==id_page, Question.question_type=="matrix").all()
        response = {
            "rows": [
                {
                    "value": question.id,
                    "text": question.question_txt,
                }
                for question in question_list
            ],
        }
        return response
    
    def _get_open(self, id_page):
        count = Question.query.filter(Question.questionnaire_id==4,Question.page==id_page, Question.question_type=="text").count()
        if count == 1:
            question = Question.query.filter(Question.questionnaire_id==4,Question.page==id_page, Question.question_type=="text").first()
            question_r= {
                "name": question.id,
                "type": "text",
                "title": question.question_txt,
                "isRequired": False
            }
        else:
            question_r=None
        return question_r
    
    def _compose_element(self, id_page):
        rows = self._get_rows(id_page)["rows"]
        text_question = self._get_open(id_page)
        element= [
        {
            "type": "matrix",
            "name": "page"+str(id_page),
            "title": "Please indicate if you agree or disagree with the following statements",
            "columns": [{
                "value": 5,
                "text": "Strongly agree"
            }, {
                "value": 4,
                "text": "Agree"
            }, {
                "value": 3,
                "text": "Neutral"
            }, {
                "value": 2,
                "text": "Disagree"
            }, {
                "value": 1,
                "text": "Strongly disagree"
            }],
            "rows":rows,
            "alternateRows": True,
            "isAllRowRequired": True
        }
        ]
        if text_question !=None:
            element.append(text_question)

        return element

    def get(self):
        # TODO: remove try catch block and check the problems query
        try:
            num_pages = 3            
            response = {
            "pages": [
            {
                "elements": self._compose_element(j+1), 
            } for j in range(0,num_pages)
            ] 
            }
            return response, 200
        except Exception as e:
            print(f"DEBUG: {e}")
            return {"message": "Could not fetch questions!"}, 404