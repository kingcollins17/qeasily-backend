from io import StringIO
from typing import List, Tuple, Set, Union
import pandas as pd
import random

from app.v_models import Topic
from app.models.categories_models import Category


#
def select_random(count: int, integers: List[int]) -> List[int]:
    """Selects count random integers from a list of integers"""
    if count > len(integers):
        return integers
    # used set, so as not to repeat entries
    res: Set[int] = set()
    for _ in range(count):
        res.add(random.choice(integers))
    return list(res)



def parse_csv(contents: str, topic_id: int, user_id: int) -> List[Tuple]:
    """Reads and converts a string in memory into a
    list of tuples of questions that can be inserted into the database"""
    values = []
    data = pd.read_csv(StringIO(contents))
    headers = [
        "question",
        "a",
        "b",
        "c",
        "d",
        "correct",
        "explanation",
        "topic_id",
        "user_id",
    ]
    for col in data.columns:
        if not col.casefold() in headers:
            # Drop any column that is not in list of allowed headers
            data.drop(columns=col, axis=1, inplace=True)

    data = data.assign(topic_id=lambda args: topic_id).assign(
        user_id=lambda args: user_id
    )
    # Ensure that all the headers are included
    if not len(data.columns) == len(headers):
        raise Exception("CSV File is not valid (Problem most likely with the headers)")

    # Parse and return list of values
    for i in range(data.shape[0]):
        values.append(tuple(data.iloc[i]))

    return values


def parse_question_list(questions: str) -> List[int]:
    """Converts the string of int stored in database to a list of integers"""
    nres = questions.removesuffix("]").removeprefix("[").split(",")
    ls = [int(value) for value in nres]
    return ls
