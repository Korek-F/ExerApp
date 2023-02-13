

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