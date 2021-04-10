export const RobotStages = {
    boot: {
        order: 0,
        description: "Attente du signal de départ"
    },
    START_GAME_CYCLE: {
        order: 1,
        description: "Démarrage d'un cycle de jeu"
    },
    READ_RESISTANCE: {
        order: 2,
        description: "Mesure de la valeur de résistance en cours"
    },
    READ_COMMAND_PANEL: {
        order: 3,
        description: "Lecture du panneau de commande en cours"
    },
    TRANSPORT_PUCK: {
        order: 4,
        description: "Transport d'une rondelle"
    },
    GO_PARK: {
        order: 5,
        description: "Confirmation de la fin du cycle de jeu"
    },
    STOP: {
        order: 6,
        description: "STOP"
    }
}
