import random
from threading import Lock
import copy

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameOfLife(metaclass=SingletonMeta):
    def __init__(self, width=15, height=15):
         # Ограничиваем размеры
        self.__width = max(10, min(width, 20))
        self.__height = max(10, min(height, 20))
        self.world = self.generate_universe()
        self.old_world = copy.deepcopy(self.world)
        self.generation = 0
        self.state_history = []  # Добавить в инициализатор, истории состояния игры
# Новые публичные методы

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def form_new_generation(self):
        curent_hash = hash(str(self.world))
        self.state_history.append(curent_hash)
        if len(self.state_history) > 10:
            self.state_history.pop(0)
        self.old_world = copy.deepcopy(self.world)
        universe = self.world
        new_world = [[0 for _ in range(self.__width)]
                     for _ in range(self.__height)]

        for i in range(len(universe)):
            for j in range(len(universe[0])):

                if universe[i][j]:
                    if self.__get_near(universe, [i, j]) not in (2, 3):
                        new_world[i][j] = 0
                        continue
                    new_world[i][j] = 1
                    continue

                if self.__get_near(universe, [i, j]) == 3:
                    new_world[i][j] = 1
                    continue
                new_world[i][j] = 0
        self.world = new_world
        
    def reset(self):
        """Сброс игры к начальному состоянию"""
        self.world = self.generate_universe()
        self.old_world = copy.deepcopy(self.world)
        self.generation = 0
        self.state_history = []  # Сбрасываем историю

    def generate_universe(self):
        return [[1 if random.random() > 0.7 else 0 for _ in range(self.__width)] for _ in range(self.__height)]

    @staticmethod
    def __get_near(universe, pos):
        """Подсчитывает количество живых соседей с учетом торической геометрии"""
        if not universe or not universe[0]:
            return 0  # Защита от пустой вселенной
    
        height = len(universe)
        width = len(universe[0])
        count = 0
        
        # Все 8 возможных направлений
        directions = [(-1,-1), (-1,0), (-1,1),
                    (0,-1),           (0,1),
                    (1,-1),  (1,0),   (1,1)]
        
        for dx, dy in directions:
            # Торические координаты (зацикленный мир)
            x = (pos[0] + dx) % height
            y = (pos[1] + dy) % width
            
            if universe[x][y]:
                count += 1
                
        return count
    
    def is_game_over(self):
        """Проверяет условия завершения игры с оптимизациями"""
        # Пропускаем проверку на 0-м поколении
        if self.generation == 0:
            return None
        
        # Условие 1: все клетки мертвы (оптимизировано)
        if self.is_all_dead():
            return "Все клетки вымерли! Игра окончена."
        
        # Условие 2: мир стабилизировался (не изменяется) с защитой от ранних срабатываний
        if self.generation > 3 and self.world == self.old_world:
            return "Мир стабилизировался! Игра окончена."
        
        # Условие 3: Проверка периодических состояний (осцилляторов)
        if self.generation > 10:
            # Проверяем последние 3 состояния
            current_hash = hash(str(self.world))
            if len(self.state_history) > 3 and current_hash in self.state_history[:-2]:
                return "Обнаружен осциллятор! Игра окончена."
            
            # Обновляем историю состояний
            self.state_history = (self.state_history + [current_hash])[-4:]
        
        # Условие 4: достигнуто максимальное число поколений
        if self.generation >= 100:
            return f"Достигнут предел в {self.generation} поколений!"
        
        return None


    def is_all_dead(self):
        """Проверяет, все ли клетки мертвы"""
        for row in self.world:
            if any(row):  # Если есть хоть одна живая клетка
                return False
        return True
    
