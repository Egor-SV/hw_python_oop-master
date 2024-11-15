class InfoMessage:
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Шаг по умолчанию для бега и ходьбы
    M_IN_KM = 1000   # Метры в километре

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action      # Количество шагов/гребков
        self.duration = duration  # Продолжительность тренировки в часах
        self.weight = weight      # Вес пользователя в кг

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Требуется определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        mean_speed_m_s = mean_speed / 3.6  # Переводим км/ч в м/с
        height_in_meters = self.height / 100  # Переводим см в метры
        return ((0.035 * self.weight
                + (mean_speed_m_s**2 / height_in_meters)
                * 0.029 * self.weight)
                * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Гребок для плавания

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        count_pool: int,
        length_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return mean_speed * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    # Создаем неизменяемый словарь
    workout = ({
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    })

    if not isinstance(data, list):
        raise TypeError("Ожидается список данных.")

    if workout_type not in workout:
        raise ValueError(
            f"Тип тренировки '{workout_type}' не поддерживается. "
            f"Доступны следующие типы тренировок: {', '.join(workout.keys())}"
        )

    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except KeyError:
            print('Неизвестный тип терировки')
        except TypeError as t:
            if 'positional' in repr(t):
                print('Передано неверное количество аргументов')
            if 'NoneType' in repr(t):
                print('Передано пустое значение (NoneType)')
        except AttributeError:
            print('Данный класс не содержит нужного метода или атрибута')
