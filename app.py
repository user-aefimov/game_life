from flask import Flask, render_template, request, redirect, url_for, jsonify
from game_of_life import GameOfLife
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Обработчик WebSocket
@socketio.on('connect')
def handle_connect():
    game = GameOfLife()
    emit('game_update', {
        'world': game.world,
        'generation': game.generation,
        'game_over': bool(game.is_game_over())
    })

@socketio.on('next_generation')
def handle_next_generation():
    game = GameOfLife()
    if not game.is_game_over():
        game.form_new_generation()
        game.generation += 1
    emit('game_update', {
        'world': game.world,
        'generation': game.generation,
        'game_over': bool(game.is_game_over())
    }, broadcast=True)

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


@app.route('/reset', methods=['POST'])
def reset():
    game = GameOfLife()
    game.reset()  # выполняет сброс состояния
    return jsonify(success=True)

# Вспомогательная функция для расчета изменений
def get_world_changes(world, old_world):
    changes = []
    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] != old_world[i][j]:
                changes.append({
                    'x': i, 
                    'y': j, 
                    'state': world[i][j],
                    'was_alive': old_world[i][j] == 1
                })
    return changes

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
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
