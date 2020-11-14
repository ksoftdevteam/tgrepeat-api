from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    """
    Модель пользователя
    """

    id = fields.IntField(pk=True)
    #: Id телеграм-аккаунта
    telegram_id = fields.IntField(unique=True)
    #: Имя
    first_name = fields.CharField(max_length=50, null=True)
    #: Фамилия
    last_name = fields.CharField(max_length=50, null=True)
    #: Университет
    university = fields.CharField(max_length=100, null=True)
    #: Электронная почта
    email = fields.CharField(max_length=60, null=True)
    #: Ссылка на профиль ВКонтакте
    vk = fields.CharField(max_length=60, null=True)
    #: О себе
    about_me = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.telegramid

    class PydanticMeta:
        computed = ["full_name"]


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)


class Tasks(models.Model):
    """
    Модель пользователя
    """

    id = fields.IntField(pk=True)
    #: Тема
    theme = fields.TextField()
    #: Ссылка на тему
    link_theme = fields.TextField()
    #: Вопрос
    question = fields.TextField()
    #: Верный ответ
    right_ans = fields.TextField()
    #: Фидбек на вопрос
    feedback = fields.TextField()


Task_Pydantic = pydantic_model_creator(Tasks, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Tasks, name="TaskIn", exclude_readonly=True)


class Questions(models.Model):
    """
    Модель пользователя
    """

    id = fields.IntField(pk=True)
    #: Телеграм-id владельца
    telegram_id = fields.IntField()
    #: ID задачи
    task_id = fields.IntField()
    #: Кол-во оставшихся повторов
    repeats = fields.IntField()


Question_Pydantic = pydantic_model_creator(Questions, name="Question")
QuestionIn_Pydantic = pydantic_model_creator(Questions, name="QuestionIn", exclude_readonly=True)