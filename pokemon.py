class Pokemon:
    def __init__(self, name, health, attack_power, defense, sprites):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.defense_multiplier = 1.0  # Para controlar la defensa
        self.focused_attack_multiplier = 1.0  # Para controlar el ataque concentrado
        self.sprites = sprites  # Almacena las rutas locales de los sprites

    @classmethod
    def from_json(cls, pokemon_data):
        # Extraer el nombre
        name = pokemon_data.get('name', 'No disponible')
        
        # Inicializar stats
        stats = {'hp': 0, 'attack': 0, 'defense': 0}  # Valores por defecto

        # Manejo de errores
        try:
            # Suponiendo que 'stats' contiene las estadísticas necesarias
            for stat in pokemon_data.get('stats', []):
                stat_name = stat['stat_name']  # Acceso a 'stat_name'
                stat_value = stat['base_stat']
                if stat_name in stats:  # Solo guardamos lo que necesitamos
                    stats[stat_name] = stat_value
        except KeyError as e:
            print(f"Error al procesar estadísticas para {name}: {e}")

        # Crear el objeto Pokemon usando la defensa del stat
        health = stats.get('hp', 0)
        attack_power = stats.get('attack', 0)
        defense = stats.get('defense', 0)
        
        # Aquí se almacenan las rutas locales de los sprites
        sprites = {
            'front_default': f'sprites/{name.lower()}_front_default.png',
            'back_default': f'sprites/{name.lower()}_back_default.png'
        }

        return cls(name.capitalize(), health, attack_power, defense, sprites)  # Capitaliza el nombre

    def attack(self, other):
        damage = self.attack_power * self.focused_attack_multiplier
        other.health -= damage
        # Reiniciar el multiplicador después de un ataque
        self.focused_attack_multiplier = 1.0
        return other.health

    def defend(self):
        self.defense_multiplier = 0.5  # Reduce el daño a la mitad en el próximo ataque

    def rest(self):
        # Recuperar el 20% de la salud actual
        recovery = int(self.health * 0.2)
        self.health += recovery

    def focus(self):
        self.focused_attack_multiplier = 2.0  # Duplica el daño del próximo ataque

    def receive_damage(self, damage):
        # Aplica la defensa si está activa
        damage *= self.defense_multiplier
        self.health -= damage
        self.defense_multiplier = 1.0  # Reiniciar el multiplicador después de recibir daño
