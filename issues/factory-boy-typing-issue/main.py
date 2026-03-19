import dataclasses
import factory


@dataclasses.dataclass
class User:
    name: str
    email: str


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")


def main():
    user = UserFactory()
    print(user)


if __name__ == "__main__":
    main()
