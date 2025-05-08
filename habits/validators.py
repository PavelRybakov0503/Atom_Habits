from rest_framework import serializers

class ValidateReward:
    """
    Валидатор для проверки полей награды (reward) и связанной приятной привычки (related_habit).

    Проверяет, что заполнено только одно из полей: либо награда, либо связанная привычка,
    но не оба варианта одновременно и не оба пустые.
    """

    def init(self, reward, related_habit):
        """
        Инициализирует валидатор с названиями полей для награды и связанной привычки.

        Аргументы
        - reward: название поля для награды
        - related_habit: название поля для связанной приятной привычки
        """
        self.reward = reward
        self.related_habit = related_habit

    def call(self, value):
        """
        Выполняет валидацию данных.

        Проверяет, что заполнено только одно из полей: reward или related_habit.
        """
        reward = dict(value).get(self.reward)
        related_habit = dict(value).get(self.related_habit)
        if reward is None and related_habit is None:
            raise serializers.ValidationError('Нужно указать награду или приятную привычку')
        elif reward and related_habit:
            raise serializers.ValidationError(
                'Нужно указать только награду или только приятную привычку, но не оба варианта.'
            )

class ValidateRewardForUpdate(ValidateReward):
    """
    Валидатор для проверки обновления полей награды и связанной привычки.

    Не позволяет указывать оба поля одновременно при обновлении объекта.
    """

    def call(self, value):
        """
        Выполняет валидацию данных для обновления.

        Запрещает одновременное указание полей reward и related_habit.
        """
        if 'reward' in dict(value) and 'related_habit' in dict(value):
            raise serializers.ValidationError(
                'Нужно указать только награду или только приятную привычку, но не оба варианта.'
            )

class ValidateTimeRequired:
    """
    Валидатор для проверки времени, необходимого для выполнения привычки.

    Не допускает значение больше 120 секунд.
    """

    def init(self, time_required):
        """
        Инициализирует валидатор с названием поля времени.

        Аргументы
        - time_required: название поля для времени выполнения
        """
        self.time_required = time_required

    def call(self, value):
        """
        Выполняет валидацию значения времени.

        Генерирует ошибку, если время превышает 120 секунд.
        """
        if 'time_required' in dict(value):
            time_required = dict(value).get(self.time_required)
            if time_required > 120:
                raise serializers.ValidationError(
                    'Время для выполнения привычки не может быть больше 120 секунд'
                )
