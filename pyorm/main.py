from uuid import UUID, uuid4

from pyorm.base import BaseModel


class Users(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    age: int | None = None
    middle_name: str | None = None
    suffix: str | None = None

    class Meta:
        unique = {"email"}


if __name__ == "__main__":
    Users.create_table()
    id = uuid4()
    Users.create(id=str(id), first_name="Christopher", last_name="Good", email="csgoodjr@gmail.com")
    users = Users.get(last_name="Good")
    print(users)
    user = users[0]
    print(user.first_name, user.last_name, user.email)
    user.delete()
    print(Users.get())
