from flask import Flask, render_template, redirect, url_for
from game_of_life import GameOfLife


app = Flask(__name__)


@app.route('/')
def index():
    # Создаем экземпляр без сохранения в переменную (как требует задание)
    GameOfLife(25, 25)
    return render_template("index.html")


@app.route('/live/')
def live():
    # Получаем экземпляр (создаем переменную game)
    game = GameOfLife()
    game_over_message = None

    # Проверяем состояние игры ДО обновления поколения
    game_over_message = game.is_game_over()
    # Обновляем только если игра активна
    if not game_over_message:
        if game.generation > 0:
        # Генерируем новое поколение
            game.form_new_generation()
    # Увеличиваем счётчик в представлении
        game.generation += 1
    # Проверяем состояние игры ПОСЛЕ обновления
        game_over_message = game.is_game_over()
    # Передаем объект в шаблон
    return render_template("live.html",
                           game=game,
                           game_over_message=game_over_message)


@app.route('/reset/')
def reset():
    game = GameOfLife()
    game.reset()  # выполняет сброс состояния
    return redirect(url_for ('live')) # Перенаправляет на live.html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
