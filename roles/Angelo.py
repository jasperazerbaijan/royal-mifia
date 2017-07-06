from .Role import Role
import strings as s

class Angelo(Role):
    """L'angelo può proteggere una persona al giorno dalla Mifia.
       Se ha successo nella protezione, il suo ruolo sarà rivelato a tutti."""
    icon = s.angel_icon
    team = 'Good'
    name = s.angel_name
    powerdesc = s.angel_power_description
    value = 50

    def __init__(self, player):
        super().__init__(player)
        self.protecting = None  # La persona che questo angelo sta proteggendo

    def __repr__(self) -> str:
        if self.protecting is None:
            return "<Role: Angelo>"
        else:
            return "<Role: Angelo, protecting {target}>".format(target=self.protecting.tusername)

    def power(self, bot, game, arg):
        # Imposta qualcuno come protetto
        selected = game.findplayerbyusername(arg)
        if selected is None:
            self.player.message(bot, s.error_username)
            return

        # Controlla che l'angelo stia provando a proteggere sè stesso
        if selected is not self.player:
            # Togli la protezione a quello che stavi proteggendo prima
            if self.protecting is not None:
                self.protecting.protectedby = None
            # Aggiungi la protezione al nuovo giocatore selezionato
            selected.protectedby = self.player
            self.protecting = selected
            self.player.message(bot, s.angel_target_selected.format(target=self.protecting.tusername))
        else:
            self.player.message(bot, s.error_angel_no_selfprotect)

    def onendday(self, bot, game):
        # Resetta la protezione
        if self.protecting is not None:
            self.protecting.protectedby = None
        self.protecting = None