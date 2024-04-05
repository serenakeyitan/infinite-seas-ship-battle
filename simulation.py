import random

class Ship:
    def __init__(self, name, strategy, attack=3, protection=3, speed=3):
        self.name = name
        self.strategy = strategy
        self.hp = 20
        self.attack = attack
        self.protection = protection
        self.speed = speed

    def perform_attack(self, opponent):
        dodge_chance = opponent.calculate_dodge_chance(self.attack)
        if random.random() < dodge_chance:
            return False  # Attack was dodged
        damage = self.calculate_damage(opponent)
        damage, critical_result = self.apply_critical_outcome(damage)


    #    if critical_result != "normal":
    #         print(f"{self.name}'s attack on {opponent.name} is a {critical_result} hit, dealing {damage} damage.")
        

        opponent.hp -= damage
        return True

    def calculate_damage(self, opponent):
        if self.attack < opponent.protection:
            # change to 0.6 => 0.7, max 1
            return max(1, self.attack - (opponent.protection - self.attack) * 0.8)
        else:
            # change to 0.3 => 0.5
            return max(0, self.attack - opponent.protection * 0.5)

    def calculate_dodge_chance(self, attacker_attack):
        if self.protection >= attacker_attack:
            # 2 => 8
            return min(((self.protection - attacker_attack) * 8 + 15), 60) / 100.0
        return 0

    def apply_critical_outcome(self, damage):
        critical_hit_chance = 0.1  # 10% chance for a critical hit
        critical_miss_chance = 0.3  # 5% chance for a critical miss
        
        if random.random() < critical_miss_chance:
            return 0, "miss"  # Critical miss negates all damage
        elif random.random() < critical_hit_chance:
            return damage * 1.5, "critical"  # Critical hit doubles the damage
        return damage, "normal"  # No critical outcome, normal damage


def generate_turn_order(ships):
    turn_order = []
    for ship in ships:
        if ship.hp > 0:  # Only consider ships that are still active
        # speed 15 => 8
            initiative = random.randint(1, 8) + ship.speed
            turn_order.append((ship, initiative))
    # Sort ships by their initiative score, highest first
    turn_order.sort(key=lambda x: x[1], reverse=True)
    return [ship[0] for ship in turn_order]

def setup_ship_with_strategy(name, strategy):
    attributes = {
        "offensive": (9, 3, 3),
        "defensive": (3, 9, 3),
        "speedy": (3, 3, 9),
        "balanced-attack": (7, 4, 4),
        "balanced-defensive": (4, 7, 4),
        "balanced": (5, 5, 5)
    }
    attack, protection, speed = attributes.get(strategy, (3, 3, 3))
    return Ship(name, strategy, attack, protection, speed)

def simulate_battle(ship_a, ship_b):
    while ship_a.hp > 0 and ship_b.hp > 0:
        for ship in generate_turn_order([ship_a, ship_b]):
            if ship.hp <= 0:
                continue
            if ship == ship_a:
                ship.perform_attack(ship_b)
                if ship_b.hp <= 0:
                    return "a"
            else:
                ship.perform_attack(ship_a)
                if ship_a.hp <= 0:
                    return "b"






def simulate_matchups(num_simulations=1000):
    strategies = ["balanced", "offensive", "defensive", "speedy", "balanced-attack", "balanced-defensive"]
    results = {}

    for strategy_a in strategies:
        for strategy_b in strategies:
            if strategy_a == strategy_b:  # Skip matchups of the same strategy
                continue
            a_wins = 0
            for _ in range(num_simulations):
                ship_a = setup_ship_with_strategy("Ship A", strategy_a)
                ship_b = setup_ship_with_strategy("Ship B", strategy_b)
                winner = simulate_battle(ship_a, ship_b)
                if winner == "a":
                    a_wins += 1
            results[(strategy_a, strategy_b)] = a_wins

    return results

def print_results(results):
    for matchup, wins in results.items():
        print(f"{matchup[0]} vs {matchup[1]}: Strategy {matchup[0]} wins {wins} times out of 1000 battles")

if __name__ == "__main__":
    results = simulate_matchups()
    print_results(results)
