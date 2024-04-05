import random

class Ship:

    def __init__(self, name="Ship", team="1", attack=3, protection=3, speed=3):
        self.name = name
        self.team = team
        self.hp = 20
        self.attack = attack
        self.protection = protection
        self.speed = speed
        # Points will be distributed by the player.
    
    def distribute_extra_points(self):
        extra_points = 6  # Players can distribute a total of 6 extra points.
        print(f"\nDistributing extra points for {self.name}: (Total extra points: {extra_points})")
        for attr in ['attack', 'protection', 'speed']:
            while True:
                try:
                    points = int(input(f"Enter extra points to add to {attr} (Remaining points: {extra_points}): "))
                    if points <= extra_points:
                        setattr(self, attr, getattr(self, attr) + points)
                        extra_points -= points
                        break
                    else:
                        print("You don't have enough points. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        print(f"Final stats - HP: 20, Attack: {self.attack}, Protection: {self.protection}, Speed: {self.speed}")

    


    def perform_attack(self, opponent):
        # Dodge check
        dodge_chance = min(60, ((opponent.protection - self.attack) * 8 + 15)) if opponent.protection >= self.attack else 0
        if random.randint(1, 100) <= dodge_chance:
            print(f"{opponent.name} dodged the attack from {self.name}!")
            return

        # Damage calculation with base formula
        if self.attack < opponent.protection:
            damage = max(2, self.attack - (opponent.protection - self.attack) * 0.3)
        else:
            damage = self.attack - opponent.protection * 0.8

        damage = max(0, damage)  # Ensure damage is not negative
        
        # Critical hit and miss logic
        critical_hit_chance = 0.2  # 10% chance for a critical hit
        critical_miss_chance = 0.35  # 5% chance for a critical miss
        
        if random.random() < critical_miss_chance:
            # Critical miss negates all damage
            print(f"Critical miss! {self.name}'s attack on {opponent.name} does no damage.")
        else:
            if random.random() < critical_hit_chance:
                # Critical hit doubles the damage
                damage *= 1.5
                print(f"Critical hit! {self.name} attacks {opponent.name} for {damage} damage.")
            else:
                # Regular attack output
                print(f"{self.name} attacks {opponent.name} for {damage} damage.")
            
            opponent.hp -= damage  # Apply the calculated damage to the opponent's HP
            
            if opponent.hp <= 0:
                print(f"{opponent.name} has been destroyed!")  # Additional feedback if the opponent is destroyed



    def __str__(self):
        return f"{self.name} - HP: {self.hp}, Attack: {self.attack}, Protection: {self.protection}, Speed: {self.speed}"


def generate_turn_order(ships):
    turn_order = []
    for ship in ships:
        if ship.hp > 0:  # Only consider ships that are still active
            initiative = random.randint(1, 8) + ship.speed
            turn_order.append((ship, initiative))
    # Sort ships by their initiative score, highest first
    turn_order.sort(key=lambda x: x[1], reverse=True)
    return [ship[0] for ship in turn_order]


def setup_ships(team):
    ships = [Ship(name=f"Team {team} Ship {i+1}", team=team) for i in range(4)]
    for ship in ships:
        ship.distribute_extra_points()
    return ships

def get_front_ship(ships):
    return next((ship for ship in ships if ship.hp > 0), None)

def simulate_battle(team1_ships, team2_ships):
    print("\nBattle starts!")
    round = 1
    while True:
        print(f"\nRound {round}:")
        all_ships = team1_ships + team2_ships
        # Determine turn order for the current round
        turn_order = generate_turn_order(all_ships)

        for attacker in turn_order:
            if attacker.hp <= 0:
                continue  # Skip ships that have been destroyed
            
            defender_team = team2_ships if attacker.team == "1" else team1_ships
            defender = get_front_ship(defender_team)
            if defender:
                attacker.perform_attack(defender)
                if defender.hp <= 0:
                    print(f"{defender.name} has been destroyed!")
                    # Check if all ships in the defender team are destroyed
                    if all(s.hp <= 0 for s in defender_team):
                        winning_team = "1" if any(s.hp > 0 for s in team1_ships) else "2"
                        print(f"\nAll ships of one side have been destroyed. Team {winning_team} wins!")
                        return
        
        # report HP values after each round
        print(f"\nRound {round} HP Report:")
        for ship in all_ships:
            if ship.hp > 0:
                print(f"{ship.name} HP: {ship.hp}")
            else:
                print(f"{ship.name} has been destroyed.")

        round += 1
        if not any(s.hp > 0 for s in team2_ships) or not any(s.hp > 0 for s in team1_ships):
            break
        round += 1

    if all(s.hp <= 0 for s in team1_ships):
        print("Team 2 wins!")
    elif all(s.hp <= 0 for s in team2_ships):
        print("Team 1 wins!")
    else:
        print("Draw")



def main():
    print("Welcome to the Ship Battle Game!")
    print("Setting up Team 1's ships:")
    team1_ships = setup_ships("1")
    print("\nSetting up Team 2's ships:")
    team2_ships = setup_ships("2")
    simulate_battle(team1_ships, team2_ships)

if __name__ == "__main__":
    main()
