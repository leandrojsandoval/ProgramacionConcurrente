MULTIPLIER_HEALT_INIT = 10


class Character:

    def __init__(self, name, health, attack, defense, sprites=None):
        self.name = name
        self.health = health * MULTIPLIER_HEALT_INIT
        self.attack = attack
        self.defense = defense
        self.vida_maxima = health * MULTIPLIER_HEALT_INIT
        self.defense_multiplier = 1.0  # Para controlar la defensa
        self.focused_attack_multiplier = 1.0  # Para controlar el ataque concentrado
        self.sprites = sprites  # Almacena las rutas locales de los sprites

    def attack_enemy(self, other):
        damage = self.attack * self.focused_attack_multiplier
        other.health -= damage
        # Reiniciar el multiplicador después de un ataque
        self.focused_attack_multiplier = 1.0
        return other.health

    def defend(self):
        self.defense_multiplier = 0.5  # Reduce el daño a la mitad en el próximo ataque

    def rest(self):
        # Recuperar el 20% de la salud actual
        recovery = int(self.vida_maxima * 0.2)
        if self.health + recovery < self.vida_maxima:
            self.health += recovery
        else:
            self.health = self.vida_maxima

    def focus(self):
        self.focused_attack_multiplier = 2.0  # Duplica el daño del próximo ataque

    def receive_damage(self, damage):
        # Aplica la defensa si está activa
        damage *= self.defense_multiplier
        self.health -= damage
        self.defense_multiplier = (
            1.0  # Reiniciar el multiplicador después de recibir daño
        )

    def to_string(self):
        print(self.name + "\t" + str(self.health) + "\t" + str(self.attack) + "\t" + str(self.defense) + "\t" + str(self.sprites))
