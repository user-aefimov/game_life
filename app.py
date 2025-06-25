from flask import Flask, render_template, request, redirect, url_for, jsonify
from game_of_life import GameOfLife


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем параметры из формы
        width = int(request.form.get('width', 15))
        height = int(request.form.get('height', 15))
        # Ограничиваем размеры для безопасности
        width = max(10, min(width, 20))
        height = max(10, min(height, 20))
        # Создаем экземпляр с пользовательскими размерами
        GameOfLife(width, height)
        return redirect(url_for('live'))
    
    # Для GET-запроса просто отображаем форму   
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

@app.route('/api/game-state')
def game_state():
    game = GameOfLife()
    return jsonify({
        'world': game.world,
        'old_world': game.old_world,
        'generation': game.generation,
        'game_over': bool(game.is_game_over()),
        'message': game.is_game_over() or ""
    })

@app.route('/api/next-generation')
def next_generation():
    game = GameOfLife()
    if not game.is_game_over():
        game.form_new_generation()
        game.generation += 1
    return jsonify({
        'world': game.world,
        'old_world': game.old_world,
        'generation': game.generation,
        'game_over': bool(game.is_game_over()),
        'message': game.is_game_over() or ""
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
