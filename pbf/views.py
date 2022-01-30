import json
from random import shuffle

from django.db import transaction
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import *

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['screenshot']

def with_log_trigger(response):
    response['HX-Trigger'] = 'newLog'
    return response

def home(request):
    games = Game.objects.all()
    return render(request, 'index.html', { 'games': games })

def view_screenshot(request, filename):
    with open(f'screenshot/{filename}', mode='rb') as f:
        return HttpResponse(f.read(), content_type='image/jpeg')

def new_game(request):
    game = Game(name='My Game')
    game.save()
    game.minor_deck.set(Card.objects.filter(type=Card.MINOR))
    game.major_deck.set(Card.objects.filter(type=Card.MAJOR))
    return redirect(reverse('view_game', args=[game.id]))

spirit_presence = {
        'Bringer': ((465,160,1.0), (535,160,1.0), (605,160,1.0), (675,160,1.0), (745,160,1.0), (815,160,1.0), (465,260,1.0), (535,260,1.0), (605,260,1.0), (675,260,1.0), (745,260,1.0)),
        'Downpour': ((449,210,1.0), (521,210,1.0), (593,210,1.0), (665,210,1.0), (735,210,1.0), (805,210,1.0), (875,210,1.0),
            (445,300,1.0), (515,300,1.0), (590,300,1.0), (660,300,1.0), (735,300,1.0)),
        'Earth': ((462,165,1.0), (528,165,1.0), (597,165,1.0), (664,165,1.0), (734,165,1.0),
            (460,260,1.0), (530,260,1.0), (595,260,1.0), (665,260,1.0), (735,260,1.0)),
        'Fangs': ((462,165,1.0), (528,165,1.0), (597,165,1.0), (664,165,1.0), (734,165,1.0), (804,165,1.0),
            (460,260,1.0), (530,260,1.0), (595,260,1.0), (665,260,1.0), (735,260,1.0)),
        'Finder': ((465,153,1.0), (597,153,1.0), (732,153,1.0), (864,153,1.0),
            (534,215,1.0), (664,215,1.0), (794,215,1.0),
            (464,280,1.0), (598,280,1.0), (731,280,1.0), (863,280,1.0)),
        'Fractured': ((462,210,1.0), (533,210,1.0), (607,210,1.0), (679,210,1.0), (754,210,1.0),
            (462,300,1.0), (536,300,1.0), (608,300,1.0), (680,300,1.0), (755,300,1.0),
            (0,0,0.0), (60,0,0.0), (120,0,0.0), (180,0,0.0), (240,0,0.0),
            (0,60,0.0), (60,60,0.0), (120,60,0.0), (180,60,0.0), (240,60,0.0),
            ),
        'Green': ((462,170,1.0), (528,170,1.0), (597,170,1.0), (664,170,1.0), (734,170,1.0), (804,170,1.0),
            (460,265,1.0), (530,265,1.0), (595,265,1.0), (665,265,1.0), (735,265,1.0)),
        'Lightning': ((460,163,1.0), (526,163,1.0), (595,163,1.0), (662,163,1.0), (730,163,1.0), (798,163,1.0), (866,163,1.0),
            (458,260,1.0), (528,260,1.0), (593,260,1.0), (663,260,1.0)),
        'Keeper': ((460,163,1.0), (526,163,1.0), (595,163,1.0), (662,163,1.0), (730,163,1.0), (798,163,1.0), (866,163,1.0),
            (458,260,1.0), (528,260,1.0), (593,260,1.0), (663,260,1.0), (733,260,1.0)),
        'Vengeance': ((462,153,1.0), (533,153,1.0), (607,153,1.0), (679,153,1.0),
            (462,257,1.0), (536,257,1.0), (607,257,1.0), (681,257,1.0), (753,257,1.0), (825,257,1.0)),
        'Lure': ((462,155,1.0), (532,155,1.0), (605,155,1.0), (676,155,1.0), (758,155,1.0),
            (462,255,1.0), (534,255,1.0), (605,255,1.0), (679,255,1.0), (751,255,1.0)),
        'Minds': ((463,155,1.0), (534,155,1.0), (608,155,1.0), (680,155,1.0), (753,155,1.0), (826,155,1.0),
            (463,258,1.0), (535,258,1.0), (606,258,1.0), (680,258,1.0), (752,258,1.0), (824,258,1.0), ),
        'Mist': ((446,155,1.0), (517,155,1.0), (591,155,1.0), (663,155,1.0),
            (446,258,1.0), (518,258,1.0), (589,258,1.0), (663,258,1.0), (735,258,1.0), (807,258,1.0), (880,258,1.0), ),
        'Ocean': ((460,240,1.0), (528,240,1.0), (595,240,1.0), (663,240,1.0), (733,240,1.0), (803,240,1.0),
            (456,325,1.0), (528,325,1.0), (599,325,1.0), (663,325,1.0), (730,325,1.0)),
        'River': ((452,165,1.0), (518,165,1.0), (587,165,1.0), (654,165,1.0), (722,165,1.0), (790,165,1.0),
            (450,260,1.0), (520,260,1.0), (585,260,1.0), (655,260,1.0), (723,260,1.0), (791,260,1.0)),
        'Shadows': ((462,165,1.0), (528,165,1.0), (597,165,1.0), (664,165,1.0), (732,165,1.0),
            (460,260,1.0), (530,260,1.0), (595,260,1.0), (665,260,1.0), (733,260,1.0)),
        'Shifting': ((445,157,1.0), (516,157,1.0), (588,157,1.0), (657,157,1.0), (728,157,1.0), (798,157,1.0), (868,157,1.0),
            (446,253,1.0), (517,253,1.0), (584,253,1.0), (656,253,1.0)),
        'Starlight': (
            (320,118,1.0),(400,118,0.0),(500,118,0.0),(580,118,0.0),
            (320,200,1.0),(400,200,0.0),(500,200,0.0),(580,200,0.0),
            (307,270,1.0),(381,270,1.0),(458,270,0.0),(532,270,0.0),(592,270,0.0),
            (307,360,1.0),(381,360,1.0),(458,360,0.0),(532,360,0.0),(592,360,0.0),
            (378,457,1.0),(450,457,1.0),(522,457,1.0),(594,457,1.0),
            (378,543,1.0),(450,543,1.0),(522,543,1.0),(594,543,1.0),

            ),
        'Stone': ((465,155,1.0), (538,155,1.0), (611,155,1.0), (684,155,1.0), (757,155,1.0), (830,155,1.0), (465,257,1.0), (538,257,1.0), (611,257,1.0), (684,257,1.0), (757,257,1.0)),
        'Thunderspeaker': ((458,162,1.0), (527,162,1.0), (598,162,1.0), (665,162,1.0), (734,162,1.0),
            (459,252,1.0), (528,252,1.0), (598,252,1.0), (665,252,1.0), (734,252,1.0), (802,252,1.0)),
        'Trickster': ((461,145,1.0), (533,145,1.0), (607,145,1.0), (678,145,1.0), (751,145,1.0),
            (462,234,1.0), (534,234,1.0), (607,234,1.0), (678,234,1.0), (751,234,1.0), (823,234,1.0)),
        'Volcano': ((443,147,1.0), (515,147,1.0), (589,147,1.0), (660,147,1.0), (733,147,1.0),
            (444,234,1.0), (516,234,1.0), (589,234,1.0), (660,234,1.0), (733,234,1.0), (805,234,1.0), (877,234,1.0)),
        'Wildfire': ((459,162,1.0), (528,162,1.0), (599,162,1.0), (668,162,1.0), (740,162,1.0),
            (458,260,1.0), (528,260,1.0), (599,260,1.0), (668,260,1.0), (739,260,1.0)),
        'Serpent': ((457,158,1.0), (527,158,1.0), (597,158,1.0), (732,158,1.0), (802,158,1.0), (872,158,1.0),
            (667,208,1.0), 
            (457,258,1.0), (527,258,1.0), (597,258,1.0), (742,258,1.0), (812,258,1.0),
            (83,487,0.0), (153,487,0.0), (223,487,0.0),
            (50,547,0.0), (120,547,0.0), (190,547,0.0),
            ),
        }


@transaction.atomic
def add_player(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    colors = {
            'red': '#fc3b5a',
            'peach': '#ffd585',
            'purple': '#715dff',
            'pink': '#e67bfe',
            'orange': '#d15a01',
            'green': '#0d9501',
            }
    color_values = list(colors.values())
    for player in game.gameplayer_set.all():
        color_values.remove(player.color)
    shuffle(color_values)
    spirit_id = int(request.POST['spirit'])
    spirit = get_object_or_404(Spirit, pk=spirit_id)
    gp = GamePlayer(game=game, spirit=spirit, notes="You can add notes here...\ntop:1 bottom:1", color=color_values[0])
    gp.save()
    try:
        for presence in spirit_presence[spirit.name]:
            gp.presence_set.create(left=presence[0], top=presence[1], opacity=presence[2])
    except:
        pass
    gp.hand.set(Card.objects.filter(spirit=spirit))
    return redirect(reverse('view_game', args=[game.id]))

def view_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    old_screenshot = game.screenshot
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            # file is saved
            form.save()
            #if old_screenshot is None:
            game.gamelog_set.create(text=f'New screenshot uploaded.')
            #else:
            #    game.gamelog_set.create(text=f'New screenshot uploaded. Old: {old_screenshot}')
            return redirect(reverse('view_game', args=[game.id]))
    else:
        form = GameForm(instance=game)

    spirits = Spirit.objects.order_by('name').all()
    logs = reversed(game.gamelog_set.order_by('-date').all()[:30])
    return render(request, 'game.html', { 'game': game, 'form': form, 'spirits': spirits, 'logs': logs })

@transaction.atomic
def draw_card(request, game_id, type):
    game = get_object_or_404(Game, pk=game_id)
    if type == 'minor':
        deck = game.minor_deck
    else:
        deck = game.major_deck

    cards = list(deck.all())
    shuffle(cards)
    card = cards[0]
    deck.remove(card)

    game.gamelog_set.create(text=f'Host drew {card.name}')

    return redirect(reverse('view_game', args=[game.id]))

@transaction.atomic
def gain_power(request, player_id, type, num):
    player = get_object_or_404(GamePlayer, pk=player_id)
    if type == 'minor':
        deck = player.game.minor_deck
    else:
        deck = player.game.major_deck

    cards = list(deck.all())
    shuffle(cards)
    selection = cards[:num]
    for c in selection:
        deck.remove(c)

    player.selection.set(selection)

    cards_str = ", ".join([str(card) for card in selection])
    player.game.gamelog_set.create(text=f'{player.spirit.name} gains a {type} power. Choices: {cards_str}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def choose_card(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    card = get_object_or_404(player.selection, pk=card_id)
    player.selection.clear()
    player.hand.add(card)

    player.game.gamelog_set.create(text=f'{player.spirit.name} gains {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def choose_card2(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    card = get_object_or_404(player.selection, pk=card_id)
    player.selection.remove(card)
    player.hand.add(card)

    player.game.gamelog_set.create(text=f'{player.spirit.name} gains {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def play_card(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    card = get_object_or_404(player.hand, pk=card_id)
    player.play.add(card)
    player.hand.remove(card)

    player.game.gamelog_set.create(text=f'{player.spirit.name} plays {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def unplay_card(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    card = get_object_or_404(player.play, pk=card_id)
    player.hand.add(card)
    player.play.remove(card)

    player.game.gamelog_set.create(text=f'{player.spirit.name} unplays {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def forget_card(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    try:
        card = player.hand.get(pk=card_id)
        player.hand.remove(card)
    except:
        pass
    try:
        card = player.play.get(pk=card_id)
        player.play.remove(card)
    except:
        pass
    try:
        card = player.discard.get(pk=card_id)
        player.discard.remove(card)
    except:
        pass

    player.game.gamelog_set.create(text=f'{player.spirit.name} forgets {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))


@transaction.atomic
def reclaim_card(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    card = get_object_or_404(player.discard, pk=card_id)
    player.hand.add(card)
    player.discard.remove(card)

    player.game.gamelog_set.create(text=f'{player.spirit.name} reclaims {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def reclaim_all(request, player_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    cards = list(player.discard.all())
    for card in cards:
        player.hand.add(card)
    player.discard.clear()

    player.game.gamelog_set.create(text=f'{player.spirit.name} reclaims all')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def discard_all(request, player_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    cards = list(player.play.all())
    for card in cards:
        player.discard.add(card)
    player.play.clear()

    player.game.gamelog_set.create(text=f'{player.spirit.name} discards all')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def discard_card(request, player_id, card_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    try:
        card = player.play.get(pk=card_id)
        player.discard.add(card)
        player.play.remove(card)
    except:
        pass
    try:
        card = player.hand.get(pk=card_id)
        player.discard.add(card)
        player.hand.remove(card)
    except:
        pass

    player.game.gamelog_set.create(text=f'{player.spirit.name} discards {card.name}')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def ready(request, player_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    player.ready = not player.ready
    player.save()

    if player.ready:
        player.game.gamelog_set.create(text=f'{player.spirit.name} is ready')
    else:
        player.game.gamelog_set.create(text=f'{player.spirit.name} is not ready')

    if player.game.gameplayer_set.filter(ready=False).count() == 0:
        player.game.gamelog_set.create(text=f'All spirits are ready!')

    return with_log_trigger(render(request, 'player.html', {'player': player}))

@transaction.atomic
def notes(request, player_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    player.notes = request.POST['notes']
    player.save()

    return HttpResponse("")

@transaction.atomic
def unready(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    for player in game.gameplayer_set.all():
        player.ready = False
        player.save()

    player.game.gamelog_set.create(text=f'All spirits marked not ready')

    return redirect(reverse('view_game', args=[game.id]))

@transaction.atomic
def time_passes(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    for player in game.gameplayer_set.all():
        player.ready = False
        player.save()
    game.turn += 1
    game.save()

    player.game.gamelog_set.create(text=f'Time passes...')
    player.game.gamelog_set.create(text=f'-- Turn {game.turn} --')

    return redirect(reverse('view_game', args=[game.id]))


@transaction.atomic
def change_energy(request, player_id, amount):
    amount = int(amount)
    player = get_object_or_404(GamePlayer, pk=player_id)
    player.energy += amount
    player.save()

    if amount > 0:
        player.game.gamelog_set.create(text=f'{player.spirit.name} gains {amount} energy (now: {player.energy})')
    else:
        player.game.gamelog_set.create(text=f'{player.spirit.name} pays {-amount} energy (now: {player.energy})')

    return with_log_trigger(render(request, 'energy.html', {'player': player}))

@transaction.atomic
def pay_energy(request, player_id):
    player = get_object_or_404(GamePlayer, pk=player_id)
    amount = player.get_play_cost()
    player.energy -= amount
    player.save()

    player.game.gamelog_set.create(text=f'{player.spirit.name} pays {amount} energy (now: {player.energy})')

    return with_log_trigger(render(request, 'energy.html', {'player': player}))

@transaction.atomic
def toggle_presence(request, player_id):
    j = json.loads(request.body)
    player = get_object_or_404(GamePlayer, pk=player_id)
    presence = get_object_or_404(player.presence_set, left=j['left'], top=j['top'])
    presence.opacity = abs(1.0 - presence.opacity)
    presence.save()

    return HttpResponse("")

@transaction.atomic
def add_element(request, player_id, element):
    player = get_object_or_404(GamePlayer, pk=player_id)
    if element == 'sun': player.temporary_sun += 1
    if element == 'moon': player.temporary_moon += 1
    if element == 'fire': player.temporary_fire += 1
    if element == 'air': player.temporary_air += 1
    if element == 'water': player.temporary_water += 1
    if element == 'earth': player.temporary_earth += 1
    if element == 'plant': player.temporary_plant += 1
    if element == 'animal': player.temporary_animal += 1
    player.save()

    return with_log_trigger(render(request, 'elements.html', {'player': player}))

@transaction.atomic
def remove_element(request, player_id, element):
    player = get_object_or_404(GamePlayer, pk=player_id)
    if element == 'sun': player.temporary_sun = 0
    if element == 'moon': player.temporary_moon = 0
    if element == 'fire': player.temporary_fire = 0
    if element == 'air': player.temporary_air = 0
    if element == 'water': player.temporary_water = 0
    if element == 'earth': player.temporary_earth = 0
    if element == 'plant': player.temporary_plant = 0
    if element == 'animal': player.temporary_animal = 0
    player.save()

    return with_log_trigger(render(request, 'elements.html', {'player': player}))


def tab(request, game_id, player_id):
    game = get_object_or_404(Game, pk=game_id)
    player = get_object_or_404(GamePlayer, pk=player_id)
    return render(request, 'tabs.html', {'game': game, 'player': player})

def game_logs(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    logs = reversed(game.gamelog_set.order_by('-date').all()[:30])
    return render(request, 'logs.html', {'game': game, 'logs': logs})

