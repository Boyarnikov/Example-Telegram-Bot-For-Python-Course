from Model import *
from typing import Tuple, Union
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def main():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = User()
        data_list = DataList(name="MyGreatPlans2", users=[user])

        session.add(user)
        session.add(data_list)

        lines = [Line(is_done=False, list=data_list, text=f"my {i}th line") for i in range(5)]
        for line in lines:
            session.add(line)

        session.commit()


def create_lines(list_id) -> Union[bool, Exception]:
    with Session(engine) as session:
        data_list = None
        lines = [Line(is_done=False, list=data_list, text=f"my {i}th line") for i in range(5)]
        for line in lines:
            session.add(line)

        session.commit()

    return True


if __name__ == "__main__":
    main()
