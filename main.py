import random

from classes.game import Person, Bcolors
from classes.magic import Spell
from classes.inventory import Item

# Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")
curae = Spell("Curae", 50, 500, "white")

# Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100", 100)
superpotion = Item("Super Potion", "potion", "Heals 500", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Player items/magic
player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curae]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 3}]

# Player/Enemy number and stats
player1 = Person("Player 1:", 500, 65, 60, 34, player_magic, player_items)  # Tank
player2 = Person("Player 2:", 499, 65, 60, 34, player_magic, player_items)  # DPS
player3 = Person("PLayer 3:", 460, 99, 60, 34, player_magic, player_items)  # Heal

enemy1 = Person("Peon ", 400, 465, 45, 25, enemy_spells, [])
enemy2 = Person("Enemy", 1200, 265, 45, 25, enemy_spells, [])
enemy3 = Person("Peon ", 400, 465, 45, 25, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

# When false battle is over
running = True
i = 0

print(Bcolors.FAIL + Bcolors.BOLD + "AN ENEMY ATTACKS!" + Bcolors.ENDC)

while running:
    print("========================================================================")
    print("\n")
    print("NAME              HP                                  MP")
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose spell:")) - 1

            # If choice = 0, go back to the menu
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(Bcolors.FAIL + "\nYou don't have enough MP" + Bcolors.ENDC)
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                player.reduce_mp(spell.cost)
                print(Bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP.", Bcolors.ENDC)
            elif spell.type == "black":
                player.reduce_mp(spell.cost)
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + Bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            # If choice = 0, go back to the menu
            if item_choice == -1:
                continue

            if player.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "\n" + "You don't have enough items." + Bcolors.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + "healed for", str(item.prop), "HP" + Bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(Bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + Bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(Bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + Bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 3:
        print(Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)

    elif defeated_players == 3:
        print(Bcolors.FAIL + "Your enemies has defeated you!" + Bcolors.ENDC)
        running = False

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name + " for", enemy_dmg)

        elif enemy_choice == 1:
            spell = enemy.choose_enemy_spell()
            magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                enemy.reduce_mp(spell.cost)
                print(Bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for", str(magic_dmg), "HP.",
                      Bcolors.ENDC)
            elif spell.type == "black":
                enemy.reduce_mp(spell.cost)
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(Bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals",
                      str(magic_dmg),
                      "points of damage to " + players[target].name + Bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]
