import random
from flask import Flask, url_for, render_template, redirect, request
from models.pokemonModels import availablePokemons

app = Flask(__name__)

availablePokemon = availablePokemons


class Choice():
    def __init__(self):
        self.yourPokemonHealth = 50
        self.opponentsPokemonHealth = 50
        self.turn = 0
        self.game_mode = "Single player"
        self.opponentsPokemonMove = 0


class NewGame(Choice):
    def __init__(self):
        self.yourPokemon = None
        self.opponentsPokemon = None
        super(NewGame, self).__init__()


class Game(NewGame):
    def __init__(self):
        self.shield_active = False
        self.took_potion = False
        self.yourPokemonHealthDisplay = 0
        self.opponentsPokemonHealthDisplay = 0
        super(Game, self).__init__()


choice_game = Choice()
newgame = NewGame()
game_start = Game()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/choice', methods=['GET', 'POST'])
def choice():
    choice_game.yourPokemonHealth = 50
    choice_game.opponentsPokemonHealth = 50
    choice_game.game_mode = request.form.get('comp_select')
    choice_game.turn = 0
    if choice_game.game_mode == "Single player":
        return render_template('choice.html', availablePokemon=availablePokemon)


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    newgame.yourPokemon
    newgame.opponentsPokemon
    newgame.game_mode
    for pokemon in availablePokemon:
        if pokemon["name"] == request.form.get('comp_select'):
            newgame.yourPokemon = pokemon
        else:
            pass
    if newgame.game_mode == "Single player":
        newgame.opponentsPokemon = random.choice(availablePokemon)
        while newgame.yourPokemon["name"] == newgame.opponentsPokemon["name"]:
            newgame.opponentsPokemon = random.choice(availablePokemon)
    print(newgame.yourPokemon)
    print(newgame.opponentsPokemon)
    return render_template('new_game.html',
                           availablePokemon=availablePokemon, yourPokemon=newgame.yourPokemon,
                           opponentsPokemon=newgame.opponentsPokemon)


@app.route('/game', methods=['GET', 'POST'])
def game():
    game_start.yourPokemon = newgame.yourPokemon
    game_start.opponentsPokemon = newgame.opponentsPokemon
    game_start.yourPokemonHealth
    game_start.opponentsPokemonHealth
    game_start.turn
    game_start.shield_active
    game_start.took_potion
    game_start.yourPokemonHealthDisplay
    game_start.opponentsPokemonHealthDisplay
    game_start.yourPokemonHealth = game_start.yourPokemonHealth
    game_start.opponentsPokemonHealth = game_start.opponentsPokemonHealth
    game_start.shield_active = False
    game_start.took_potion = False
    game_start.turn = game_start.turn + 1

    game_start.yourPokemonHealthDisplay = '*' * game_start.yourPokemonHealth
    game_start.opponentsPokemonHealthDisplay = '*' * game_start.opponentsPokemonHealth
    if game_start.yourPokemonHealth <= 0:
        return render_template('result.html', gameWinner=game_start.opponentsPokemon["name"])
    if game_start.opponentsPokemonHealth <= 0:
        return render_template('result.html', gameWinner=game_start.yourPokemon["name"])

    return render_template('game.html', yourPokemon=game_start.yourPokemon, yourPokemonHealth=game_start.yourPokemonHealth,
                           yourPokemonHealthDisplay=game_start.yourPokemonHealthDisplay,
                           opponentsPokemonHealthDisplay=game_start.opponentsPokemonHealthDisplay,
                           opponentsPokemon=game_start.opponentsPokemon, opponentsPokemonHealth=game_start.opponentsPokemonHealth)


@app.route('/attack', methods=['GET', 'POST'])
def attack():
    game_start.yourPokemon
    game_start.opponentsPokemon
    game_start.yourPokemonHealth
    game_start.opponentsPokemonHealth
    game_start.shield_active
    game_start.took_potion
    game_start.yourPokemonMove = request.form.get('comp_select')
    if game_start.yourPokemonMove == "Shield":
        game_start.shield_active = True
    if game_start.yourPokemonMove == "Potion":
        if game_start.yourPokemonHealth > 40:
            game_start.yourPokemonHealth = 50
        else:
            game_start.yourPokemonHealth += 10
        game_start.took_potion = True
    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if game_start.yourPokemon["type"] == k:
            if game_start.opponentsPokemon["type"] == k:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Napad nije baš uspješan...'
            if game_start.opponentsPokemon["type"] == version[(i + 1) % 3]:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Its super effective!'
                game_start.opponentsPokemon["EVs"]["ATTACK"] *= 2
                game_start.opponentsPokemon["EVs"]["DEFENSE"] *= 2
            if game_start.opponentsPokemon["type"] == version[(i + 2) % 3]:
                string_1_attack = 'Napad je super uspješan!'
                string_2_attack = 'Napad nije baš uspješan...'
                game_start.yourPokemon["EVs"]["ATTACK"] *= 2
                game_start.opponentsPokemon["EVs"]["DEFENSE"] *= 2

    if game_start.shield_active:
        string_1_attack = 'Tvoj pokemon je blokirao suparnički napad !'
    elif game_start.took_potion:
        string_1_attack = 'Životni bodovi tvoga pokemona su povećani!'
    else:
        game_start.opponentsPokemonHealth = game_start.opponentsPokemonHealth - \
            game_start.yourPokemon["EVs"]["ATTACK"]

    return render_template('attack.html', yourPokemonMove=game_start.yourPokemonMove, yourPokemon=game_start.yourPokemon,
                           opponentsPokemon=game_start.opponentsPokemon,
                           string_1_attack=string_1_attack, string_2_attack=string_2_attack)


@app.route('/opponents_turn', methods=['GET', 'POST'])
def opponents_turn():
    game_start.yourPokemon
    game_start.opponentsPokemon
    game_start.yourPokemonHealth
    game_start.opponentsPokemonHealth
    game_start.turn
    game_start.shield_active
    game_start.took_potion
    game_start.yourPokemonHealthDisplay
    game_start.opponentsPokemonHealthDisplay
    game_start.game_mode
    game_start.yourPokemonHealth
    game_start.opponentsPokemonHealth
    game_start.shield_active = False
    game_start.took_potion = False

    game_start.yourPokemonHealthDisplay = '*' * game_start.yourPokemonHealth
    game_start.opponentsPokemonHealthDisplay = '*' * \
        game_start.opponentsPokemonHealth
    if game_start.yourPokemonHealth <= 0:
        return render_template('result.html', gameWinner=game_start.opponentsPokemon["name"])
    if game_start.opponentsPokemonHealth <= 0:
        return render_template('result.html', gameWinner=game_start.yourPokemon["name"])
    if game_start.game_mode == "Single player":
        return redirect(url_for('attack2'))


@app.route('/attack2', methods=['GET', 'POST'])
def attack2():
    game_start.yourPokemon
    game_start.opponentsPokemonHealth
    game_start.opponentsPokemon
    game_start.yourPokemonHealth
    game_start.shield_active
    game_start.game_mode
    game_start.opponentsPokemonMove
    if game_start.game_mode == "Single player":
        key = random.choice(list(game_start.opponentsPokemon["moves"]))
        game_start.opponentsPokemonMove = game_start.opponentsPokemon["moves"][key]

    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if game_start.yourPokemon["type"] == k:
            if game_start.opponentsPokemon["type"] == k:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Napad nije baš uspješan...'
            if game_start.opponentsPokemon["type"] == version[(i + 1) % 3]:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Napad je super uspješan!'
            if game_start.opponentsPokemon["type"] == version[(i + 2) % 3]:
                string_1_attack = 'Napad je super uspješan!'
                string_2_attack = 'Napad nije baš uspješan...'

    if game_start.shield_active:
        pass
    else:
        game_start.yourPokemonHealth = game_start.yourPokemonHealth - \
            game_start.opponentsPokemon["EVs"]["ATTACK"]

    return render_template('attack2.html', yourPokemon=game_start.yourPokemon,
                           opponentsPokemon=game_start.opponentsPokemon, opponentsPokemonMove=game_start.opponentsPokemonMove,
                           string_1_attack=string_1_attack, string_2_attack=string_2_attack)


@app.route('/bag')
def bag():
    game_start.yourPokemon
    game_start.yourPokemonHealth
    game_start.yourPokemonHealthDisplay
    return render_template('bag.html', yourPokemon=game_start.yourPokemon, yourPokemonHealth=game_start.yourPokemonHealth,
                           yourPokemonHealthDisplay=game_start.yourPokemonHealthDisplay)


@app.route('/pokemon')
def pokemon():
    return render_template('pokemon.html')


@app.route('/result')
def result():
    return render_template('result.html')
