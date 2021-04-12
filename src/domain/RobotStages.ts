export const RobotStages = {
    boot: {
        order: 0,
        description: "Attente du signal de départ"
    },
    start_cycle: {
        order: 1,
        description: "Démarrage d'un cycle de jeu"
    },
    go_to_ohmmeter: {
        order: 2,
        description: "Lecture de résistance en cours"
    },
    find_command_panel: {
        order: 3,
        description: "Lecture du panneau de commande en cours"
    },
    transport_puck: {
        order: 4,
        description: "Transport d'une rondelle"
    },
    go_park: {
        order: 5,
        description: "Confirmation de la fin du cycle de jeu"
    },
    stop: {
        order: 6,
        description: "STOP"
    }
}
