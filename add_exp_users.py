import argparse
import csv
import json
import random
import string

import dill
import numpy as np
import pandas as pd

# from desdeo_problem.problem import _ScalarObjective
from desdeo_problem.problem import DiscreteDataProblem

# from desdeo_problem.surrogatemodels.lipschitzian import LipschitzianRegressor
# from desdeo_problem.problem import Variable

from app import app, db
from models.problem_models import Problem as ProblemModel
from models.user_models import UserModel
from models.questionnaire_models import Question, Questionnaire

parser = argparse.ArgumentParser(
    description="Add N new user to the database with a pre-defined groupID and a given username prefix."
)
parser.add_argument(
    "--N", type=int, help="The number of usernames to be added.", required=True
)

dill.settings["recurse"] = True

# db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

args = vars(parser.parse_args())


def create_questionnaire(id: int, type: str, group: int):
    return {"id": id, "type": type, "group": group}


def create_question(
    question_id: int,
    questionnaire_id: int,
    question_txt: str,
    question_type: str,
    page: int,
):
    return {
        "id": question_id,
        "questionnaire_id": questionnaire_id,
        "question_txt": question_txt,
        "question_type": question_type,
        "page": page,
    }


def main():
    with app.app_context():
        letters = string.ascii_lowercase
        args = vars(parser.parse_args())
        methods = ["stratus", "nemo"]
        ids = [1, 2]
        usernames = [
            [f"{method}_{n}" for n in range(1, args["N"] + 1)] for method in methods
        ]
        usernames = sum(usernames, [])
        passwords = [
            ("".join(random.choice(letters) for i in range(6)))
            for j in range(len(usernames))
        ]
        groupIds = np.array([])
        # id1 = np.ones(N * len(ids)) * ids[1]
        for i in range(0, len(ids)):
            groupIds = np.append(groupIds, np.ones(args["N"]) * ids[i], axis=0)

        usernames.append("giomara")
        passwords.append("123456")
        usernames.append("kaisa")
        passwords.append("123456")
        usernames.append("aruiz")
        passwords.append("123456")
        usernames.append("fruiz")
        passwords.append("123456")
        usernames.append("bsaini")
        passwords.append("123456")
        groupIds = np.append(groupIds, [2]*5).tolist()
        # print(usernames)
        # print(groupIds)

        problemGroups = np.array(range(len(usernames)), dtype=int)
        problemGroups = (
            problemGroups % 6
        )  # One of {0, 1, 2}. Decides the version of the sustainability problem.
        problemGroups = problemGroups.tolist()

        try:
            for username, password, groupId, problemGroup in zip(
                usernames, passwords, groupIds, problemGroups
            ):
                add_user(username, password, groupId, problemGroup)
            print(f"Added users {usernames} to the database succesfully.")
            for problemGroup in problemGroups:
                add_sus_problem(problemGroup)
        except Exception as e:
            print("something went wrong...")
            print(e)
            exit()

        with open("users_and_pass.csv", "w", newline="") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            list(
                map(
                    lambda x: writer.writerow(x),
                    zip(usernames, passwords, groupIds, problemGroups),
                )
            )

        questionnaires = []
        questionnaires.append(
            create_questionnaire(1, "Demographic", 0)
        )  # 0 = both groups 1= one method 2= switch method
        questionnaires.append(create_questionnaire(2, "Init", 0))
        questionnaires.append(create_questionnaire(3, "End", 0))
        questionnaires.append(create_questionnaire(4, "End", 2))

        questions = []

        # Questions for demographic survey
        questions.append(create_question(1, 1, "Age", "text", 1))
        questions.append(create_question(2, 1, "Gender", "dropdown", 1))
        questions.append(create_question(3, 1, "Nationality", "text", 1))
        questions.append(
            create_question(
                4,
                1,
                "Did you have any prior knowledge about these methods other than what you have learnt in this course?",
                "Boolean",
                1,
            )
        )

        # Questions initial survey
        questions.append(create_question(6, 2, "How tired are you now?", "rating", 1))
        # questions.append(
        #    create_question(
        #        7,
        #        2,
        #        "What objective function values do you think you can achieve as your final solution?",
        #        "text",
        #        1,
        #    )
        # )

        questions.append(
            create_question(
                7,
                2,
                "Social",
                "text",
                1,
            )
        )
        questions.append(
            create_question(
                8,
                2,
                "Economic",
                "text",
                1,
            )
        )
        questions.append(
            create_question(
                9,
                2,
                "Environmental",
                "text",
                1,
            )
        )

        # Questions final survey (both groups)
        questions.append(create_question(10, 3, "I am now feeling tired.", "matrix", 1))
        questions.append(
            create_question(
                11, 3, "I am satisfied with my final solution. ", "matrix", 1
            )
        )
        questions.append(
            create_question(
                12, 3, "I think that the solution I found is the best one.", "matrix", 1
            )
        )
        questions.append(
            create_question(
                13,
                3,
                "Please describe why you are satisfied/disatisfied with your final solution.",
                "text",
                1,
            )
        )
        questions.append(
            create_question(
                14,
                3,
                "Interacting with this decision support tool helped me to understand more about the tradeoffs in this problem.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                15,
                3,
                "What did you find new or unexpected compared to what you knew or expected before starting the solution process? Please specify. ",
                "text",
                2,
            )
        )
        questions.append(
            create_question(
                16,
                3,
                "A lot of mental activity (e.g., thinking, deciding, and remembering) was required to find my final solution.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                17,
                3,
                "The process of finding the final solution was difficult.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                18,
                3,
                "It was easy to learn to use this decision support tool.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                19,
                3,
                "I felt I was in control during the solution process.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                20,
                3,
                "I felt comfortable using this decision support tool.  ",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                21,
                3,
                "I felt frustrated in the solution process (e.g., insecure, discouraged, irritated, stressed).",
                "matrix",
                3,
            )
        )
        questions.append(
            create_question(22, 3, "Please, explain why or why not. ", "text", 3)
        )
        questions.append(
            create_question(
                23,
                3,
                "Overall, I am satisfied with the ease of completing this task.",
                "matrix",
                3,
            )
        )
        questions.append(
            create_question(
                24,
                3,
                "Overall, I am satisfied with the amount of time it took to complete this task.",
                "matrix",
                3,
            )
        )

        # Questions final survey (second group)
        questions.append(
            create_question(
                25,
                4,
                "Phase 1 enabled exploring solutions with different conflicting values of the objective functions.",
                "matrix",
                1,
            )
        )
        questions.append(
            create_question(
                26,
                4,
                "Phase 1 enabled me to learn about the conflict degrees among the objectives.",
                "matrix",
                1,
            )
        )
        questions.append(
            create_question(
                27,
                4,
                "Phase 1 enabled me to direct the search toward  a set of interesting solutions.",
                "matrix",
                1,
            )
        )
        questions.append(
            create_question(
                28,
                4,
                "Phase 1 played an important role in fine-tuning the final solution.",
                "matrix",
                1,
            )
        )
        questions.append(
            create_question(
                29,
                4,
                "Phase 1 increased my confidence in the final solution.",
                "matrix",
                1,
            )
        )
        questions.append(
            create_question(
                30,
                4,
                "Do you have other comments about Phase 1? If so, please specify.",
                "text",
                1,
            )
        )
        questions.append(
            create_question(
                31,
                4,
                "Phase 2 enabled exploring solutions with different conflicting values of the objective functions. ",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                32,
                4,
                "Phase 2 enabled me to learn about the conflict degrees among the objectives.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                33,
                4,
                "Phase 2 enabled me to direct the search toward  a set of interesting solutions.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                34,
                4,
                "Phase 2 played an important role in fine-tuning the final solution.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                35,
                4,
                "Phase 2 increased my confidence in the final solution.",
                "matrix",
                2,
            )
        )
        questions.append(
            create_question(
                36,
                4,
                "Do you have other comments about Phase 2? If so, please specify.",
                "text",
                2,
            )
        )
        questions.append(
            create_question(
                37,
                4,
                "Using the two phases supported me in finding the final solution.",
                "matrix",
                3,
            )
        )
        questions.append(
            create_question(
                38,
                4,
                "The types of preference information required in the  two phases were different. Switching between these types of preference information was easy.",
                "matrix",
                3,
            )
        )
        questions.append(
            create_question(
                39,
                4,
                "I feel that the final solution is better than the one obtained at the end of Phase 1.",
                "matrix",
                3,
            )
        )
        questions.append(
            create_question(
                40,
                4,
                "I feel that Phase 1 made it easier to find a good solution at the end of the solution process.",
                "matrix",
                3,
            )
        )

        try:
            for questionnaire in questionnaires:
                add_questionaire(
                    id=questionnaire["id"],
                    type=questionnaire["type"],
                    group=questionnaire["group"],
                )
            for question in questions:
                add_question(
                    id=question["id"],
                    questionnaire_id=question["questionnaire_id"],
                    question_txt=question["question_txt"],
                    question_type=question["question_type"],
                    page=question["page"],
                )

        except Exception as e:
            print("something went wrong...")
            print(e)
            exit()

        print("Added questions to the database succesfully.")


def add_user(username, password, groupId, problemGroup):
    # print(problemGroup)
    with app.app_context():
        db.session.add(
            UserModel(
                username=username,
                password=UserModel.generate_hash(password),
                groupId=groupId,
                problemGroup=int(problemGroup),
            )
        )
        db.session.commit()


def add_sus_problem(problemGroup):
    # print(type(problemGroup))
    with app.app_context():
        user_query = UserModel.query.filter_by(problemGroup=int(problemGroup)).first()
        # print(type(user_query.problemGroup))
        if user_query is None:
            print(f"No users in group {problemGroup}.")
            return
        # else:
        #    id = user_query.id

        file_name = "./tests/data/sustainability_spanish.csv"

        data = pd.read_csv(file_name)
        # minus because all are to be maximized
        data[["social", "economic", "environmental"]] = -data[
            ["social", "economic", "environmental"]
        ]

        obj_order = {
            0: ["social", "economic", "environmental"],
            1: ["economic", "environmental", "social"],
            2: ["environmental", "social", "economic"],
            3: ["social", "environmental", "economic"],
            4: ["economic", "social", "environmental"],
            5: ["environmental", "economic", "social"],
        }

        var_names = [f"x{i}" for i in range(1, 12)]
        obj_names = obj_order[problemGroup]

        data = data[obj_names + var_names]  # Reorder objectives based on problemGroup
        ideal = data[obj_names].min().values
        nadir = data[obj_names].max().values

        # define the sus problem
        problem = DiscreteDataProblem(data, var_names, obj_names, ideal, nadir)

        db.session.add(
            ProblemModel(
                name=f"Spanish sustainability problem {problemGroup}",
                problem_type="Discrete",
                problem_pickle=problem,
                minimize=json.dumps([-1, -1, -1]),
                problemGroup=problemGroup,
            )
        )
        db.session.commit()
        print(f"Sustainability problem added for problem group '{problemGroup}'")


def add_question(id, questionnaire_id, question_txt, question_type, page):
    with app.app_context():
        db.session.add(
            Question(
                id=id,
                questionnaire_id=questionnaire_id,
                question_txt=question_txt,
                question_type=question_type,
                page=page,
            )
        )
        db.session.commit()


def add_questionaire(id, type, group):
    with app.app_context():
        db.session.add(Questionnaire(id=id, type=type, group=group))
        db.session.commit()


if __name__ == "__main__":
    main()
