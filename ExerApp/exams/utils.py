from excercises.utils import render_checked_exercise

def check_session_answers(session):
    correct_items = []
    wrong_items = {}
    answers = session.sessionanswer_set.all()
    for i in answers:
        obj = i.item.item
        answer = i.user_answer.strip()
        if obj.is_correct(answer):
            correct_items.append(obj)
        else:
            wrong_items[obj]=answer
    return correct_items, wrong_items

def get_rendered_answers(session):
    correct_items, wrong_items = check_session_answers(session)
    checked_answers = []
    for exercise in session.exam.exercise_set.exercise_set.all():
        checked_exercise = render_checked_exercise(exercise, correct_items, wrong_items)
        checked_answers.append(checked_exercise)
    
    correct_ratio = (len(correct_items)/session.exam.exercise_set.number_of_points)*100

    return correct_items, checked_answers, correct_ratio
