import random
from flask import Flask, url_for, render_template, redirect, request
from models.pokemonModels import availablePokemons

app = Flask(__name__)

availablePokemon = availablePokemons

game_mode = None
yourPokemonHealth = 0
opponentsPokemonHealth = 0
turn = 0
yourPokemon = None
opponentsPokemon = None
shield_active = False
took_potion = False
yourPokemonHealthDisplay = 0
opponentsPokemonHealthDisplay = 0
opponentsPokemonMove = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/choice', methods=['GET', 'POST'])
def choice():
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global game_mode
    yourPokemonHealth = 50
    opponentsPokemonHealth = 50
    game_mode = request.form.get('comp_select')
    turn = 0
    if game_mode == "Single player":
        return render_template('choice.html', availablePokemon=availablePokemon)


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    global yourPokemon
    global opponentsPokemon
    global game_mode
    for pokemon in availablePokemon:
        if pokemon["name"] == request.form.get('comp_select'):
            yourPokemon = pokemon
        else:
            pass
    if game_mode == "Single player":
        opponentsPokemon = random.choice(availablePokemon)
        while yourPokemon["name"] == opponentsPokemon["name"]:
            opponentsPokemon = random.choice(availablePokemon)
    return render_template('new_game.html',
                           availablePokemon=availablePokemon, yourPokemon=yourPokemon,
                           opponentsPokemon=opponentsPokemon)


@app.route('/game', methods=['GET', 'POST'])
def game():
    global yourPokemon
    global opponentsPokemon
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global shield_active
    global took_potion
    global yourPokemonHealthDisplay
    global opponentsPokemonHealthDisplay
    yourPokemonHealth = yourPokemonHealth
    opponentsPokemonHealth = opponentsPokemonHealth
    shield_active = False
    took_potion = False
    turn = turn + 1

    yourPokemonHealthDisplay = '*' * yourPokemonHealth
    opponentsPokemonHealthDisplay = '*' * opponentsPokemonHealth
    if yourPokemonHealth <= 0:
        return render_template('result.html', gameWinner=opponentsPokemon["name"])
    if opponentsPokemonHealth <= 0:
        return render_template('result.html', gameWinner=yourPokemon["name"])

    return render_template('game.html', yourPokemon=yourPokemon, yourPokemonHealth=yourPokemonHealth,
                           yourPokemonHealthDisplay=yourPokemonHealthDisplay,
                           opponentsPokemonHealthDisplay=opponentsPokemonHealthDisplay,
                           opponentsPokemon=opponentsPokemon, opponentsPokemonHealth=opponentsPokemonHealth)


@app.route('/attack', methods=['GET', 'POST'])
def attack():
    global yourPokemon
    global opponentsPokemonHealth
    global yourPokemonHealth
    global opponentsPokemon
    global shield_active
    global took_potion
    yourPokemonMove = request.form.get('comp_select')
    if yourPokemonMove == "Shield":
        shield_active = True
    if yourPokemonMove == "Potion":
        if yourPokemonHealth > 40:
            yourPokemonHealth = 50
        else:
            yourPokemonHealth += 10
        took_potion = True
    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if yourPokemon["type"] == k:
            if opponentsPokemon["type"] == k:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Napad nije baš uspješan...'
            if opponentsPokemon["type"] == version[(i + 1) % 3]:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Its super effective!'
                opponentsPokemon["EVs"]["ATTACK"] *= 2
                opponentsPokemon["EVs"]["DEFENSE"] *= 2
            if opponentsPokemon["type"] == version[(i + 2) % 3]:
                string_1_attack = 'Napad je super uspješan!'
                string_2_attack = 'Napad nije baš uspješan...'
                yourPokemon["EVs"]["ATTACK"] *= 2
                opponentsPokemon["EVs"]["DEFENSE"] *= 2

    if shield_active:
        string_1_attack = 'Tvoj pokemon je blokirao suparnički napad !'
    elif took_potion:
        string_1_attack = 'Životni bodovi tvoga pokemona su povećani!'
    else:
        opponentsPokemonHealth = opponentsPokemonHealth - \
            yourPokemon["EVs"]["ATTACK"]

    return render_template('attack.html', yourPokemonMove=yourPokemonMove, yourPokemon=yourPokemon,
                           opponentsPokemon=opponentsPokemon,
                           string_1_attack=string_1_attack, string_2_attack=string_2_attack)


@app.route('/opponents_turn', methods=['GET', 'POST'])
def opponents_turn():
    global yourPokemon
    global opponentsPokemon
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global shield_active
    global took_potion
    global yourPokemonHealthDisplay
    global opponentsPokemonHealthDisplay
    global game_mode
    yourPokemonHealth = yourPokemonHealth
    opponentsPokemonHealth = opponentsPokemonHealth
    shield_active = False
    took_potion = False

    yourPokemonHealthDisplay = '*' * yourPokemonHealth
    opponentsPokemonHealthDisplay = '*' * opponentsPokemonHealth
    if yourPokemonHealth <= 0:
        return render_template('result.html', gameWinner=opponentsPokemon["name"])
    if opponentsPokemonHealth <= 0:
        return render_template('result.html', gameWinner=yourPokemon["name"])
    if game_mode == "Single player":
        return redirect(url_for('attack2'))


@app.route('/attack2', methods=['GET', 'POST'])
def attack2():
    global yourPokemon
    global opponentsPokemonHealth
    global opponentsPokemon
    global yourPokemonHealth
    global shield_active
    global game_mode
    global opponentsPokemonMove
    if game_mode == "Single player":
        key = random.choice(list(opponentsPokemon["moves"]))
        opponentsPokemonMove = opponentsPokemon["moves"][key]

    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if yourPokemon["type"] == k:
            if opponentsPokemon["type"] == k:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Napad nije baš uspješan...'
            if opponentsPokemon["type"] == version[(i + 1) % 3]:
                string_1_attack = 'Napad nije baš uspješan...'
                string_2_attack = 'Napad je super uspješan!'
            if opponentsPokemon["type"] == version[(i + 2) % 3]:
                string_1_attack = 'Napad je super uspješan!'
                string_2_attack = 'Napad nije baš uspješan...'

    if shield_active:
        pass
    else:
        yourPokemonHealth = yourPokemonHealth - \
            opponentsPokemon["EVs"]["ATTACK"]

    return render_template('attack2.html', yourPokemon=yourPokemon,
                           opponentsPokemon=opponentsPokemon, opponentsPokemonMove=opponentsPokemonMove,
                           string_1_attack=string_1_attack, string_2_attack=string_2_attack)


@app.route('/bag')
def bag():
    global yourPokemon
    global yourPokemonHealth
    global yourPokemonHealthDisplay
    return render_template('bag.html', yourPokemon=yourPokemon, yourPokemonHealth=yourPokemonHealth,
                           yourPokemonHealthDisplay=yourPokemonHealthDisplay)


@app.route('/pokemon')
def pokemon():
    return render_template('pokemon.html')


@app.route('/result')
def result():
    return render_template('result.html')
