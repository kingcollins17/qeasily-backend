from typing import List
from pydantic import BaseModel, Field


debug = True


class QeasilyPlan(BaseModel):
    id: int
    name: str
    price: float
    features: List[str]
    quizzes: int
    admin_points: int
    admin_access: bool


free = QeasilyPlan(
    id=1,
    name="Free",
    price=0.00,
    features=["5 Quiz credits", "0 Admin credits"],
    quizzes=5,
    admin_points=0,
    admin_access=False,
)
scholar = QeasilyPlan(
    id=2,
    name="Scholar",
    price=300.00,
    features=["15 Quiz Credits", "0 Admin Credits"],
    quizzes=15,
    admin_points=0,
    admin_access=False,
)
genius = QeasilyPlan(
    id=3,
    name="Genius",
    price=600.00,
    features=["30 Quiz Credits", "0 Admin Credits"],
    quizzes=35,
    admin_points=0,
    admin_access=False,
)
admin = QeasilyPlan(
    id=4,
    name="Admin",
    price=1000.00,
    features=["500 Quiz Credits", "100 Admin Points", "Full Admin access"],
    quizzes=75,
    admin_points=110,
    admin_access=True,
)


class Paystackkeys(BaseModel):
    public: str
    secret: str


if debug == True:
    keys = Paystackkeys(
        public="pk_test_1467164089a777561173b627973b2349425a2131",
        secret="sk_test_ac44a7ca850f4bac82b8db3f7b8f62e1b1321c7d",
    )
else:
    keys = Paystackkeys(
        public="pk_test_1467164089a777561173b627973b2349425a2131",
        secret="sk_test_ac44a7ca850f4bac82b8db3f7b8f62e1b1321c7d",
    )
plans = [free, scholar, genius, admin]


def find_plan(search: int | str) -> QeasilyPlan | None:
    for plan in plans:
        if search == plan.id or plan.name == search:
            return plan
