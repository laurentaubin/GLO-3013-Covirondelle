# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import struct

import serial
import time

# Doit definir ces parametres pour l'identification
DEFINE_SPEED1 = 0.6
DEFINE_SPEED2 = 0.9
DEFINE_FILE1 = "AVANVER_RECULER.txt"
DEFINE_FILE2 = "DROITE_GAUCHE.txt"
DEFINE_FILE3 = "TOURNER.txt"
DEFINE_DURATION_OF_COMMAND = 3  # le robot_movement avance pendant 3 seconde
DEFINE_DURATION_OF_STOP = 0.5

# define les differentes commandes possibles
DEFINE_COMMANDE_MOTEUR_STOP = 0
DEFINE_COMMANDE_MOTEUR_AVANCER = 1
DEFINE_COMMANDE_MOTEUR_RECULER = 2
DEFINE_COMMANDE_MOTEUR_DROITE = 3
DEFINE_COMMANDE_MOTEUR_GAUCHE = 4
DEFINE_COMMANDE_MOTEUR_TOURNER_HORRAIRE = 5
DEFINE_COMMANDE_MOTEUR_TOURNER_ANTI_HORRAIRE = 6
DEFINE_COMMANDE_OHMMETRE_LECTURE = 7
DEFINE_COMMANDE_DEMANDE_CONSOMMATION = 8
DEFINE_COMMANDE_DEMANDE_RONDELLE_EST_DANS_PREHENSEUR = 9


# En ce moment, le payload est un float representant la vitesse derire
# Celui-ci doit se trouver entre 0 et 1, 1 etant la vitesse maximale
# si le chiffre est plus haut que 1, il va juste alle a la vitesse maximal
# Si le chiffre est negatif, ben... yo no se... ca va marche en tout cas, juste pas a une vitesse connu

# Le payload est ignore pour les commande 7, 8 et 9 (lecture ohmmetre, demande consommation et demande rondelle)
# Pour ces commandes, une retroaction est demande de la part du stm
# Chaque communication du stm vers le rpi sera fait sous forme de ligne.
# Donc, la reception devrait se faire avec Serial.readline
# On va se dire quelle format est preferable pour la reponse du stm dans les trois cas
def send_command(ser, command, payload):
    ser.write(bytes(chr(command), "utf-8") + struct.pack("f", payload))


# En ce moment, lorsqu'on envoit une comande, il y a un timer qui part sur le stm et qui fait des interruption au 10ms
# A chaque 10 ms, le stm envoit le temps et la position des differents encodeurs
# on utilise ca pour l'identification, mais ce comportement sera retire au release
def read_encoder_value(ser, file, read_time):
    timeout = time.time() + read_time
    while True:
        received_data = ser.readline()
        print(str(received_data.decode("utf-8")))
        file.write(str(received_data.decode("utf-8")))
        if time.time() > timeout:
            break


# Le reste du code c'est juste pour l'identification des moteurs, mais si ca peut vous inspirer pourquoi pas


def identification(ser, file, command, speed, name_of_command):
    file.write(
        "\n\n\n********************************"
        + name_of_command
        + "********************************\n\n\n"
    )
    send_command(ser, command, speed)
    read_encoder_value(ser, file, DEFINE_DURATION_OF_COMMAND)
    file.write(
        "\n\n\n******************************** STOP ********************************\n\n\n"
    )
    send_command(ser, DEFINE_COMMANDE_MOTEUR_STOP, speed)
    read_encoder_value(ser, file, DEFINE_DURATION_OF_STOP)


def main():
    # Dans le cas du rpi, le nom du port comment par /dev/tty...
    ser = serial.Serial("COM7", 115200)  # Open port with baud rate\
    f1 = open(DEFINE_FILE1, "w")
    f2 = open(DEFINE_FILE2, "w")
    f3 = open(DEFINE_FILE3, "w")
    f1.write(
        "format : time ( en milliseconde), motor 1 encoder, motor 2 encoder, motor 3 encoder, motor 4 encoder,"
    )

    identification(
        ser,
        f1,
        DEFINE_COMMANDE_MOTEUR_AVANCER,
        DEFINE_SPEED1,
        "AVANCER " + str(DEFINE_SPEED1),
    )
    identification(
        ser,
        f1,
        DEFINE_COMMANDE_MOTEUR_RECULER,
        DEFINE_SPEED1,
        "RECULER " + str(DEFINE_SPEED1),
    )
    identification(
        ser,
        f1,
        DEFINE_COMMANDE_MOTEUR_AVANCER,
        DEFINE_SPEED2,
        "AVANCER " + str(DEFINE_SPEED2),
    )
    identification(
        ser,
        f1,
        DEFINE_COMMANDE_MOTEUR_RECULER,
        DEFINE_SPEED2,
        "RECULER " + str(DEFINE_SPEED2),
    )

    identification(
        ser,
        f2,
        DEFINE_COMMANDE_MOTEUR_DROITE,
        DEFINE_SPEED1,
        "DROITE " + str(DEFINE_SPEED1),
    )
    identification(
        ser,
        f2,
        DEFINE_COMMANDE_MOTEUR_GAUCHE,
        DEFINE_SPEED1,
        "GAUCHE " + str(DEFINE_SPEED1),
    )
    identification(
        ser,
        f2,
        DEFINE_COMMANDE_MOTEUR_DROITE,
        DEFINE_SPEED2,
        "DROITE " + str(DEFINE_SPEED2),
    )
    identification(
        ser,
        f2,
        DEFINE_COMMANDE_MOTEUR_GAUCHE,
        DEFINE_SPEED2,
        "GAUCHE " + str(DEFINE_SPEED2),
    )

    identification(
        ser,
        f3,
        DEFINE_COMMANDE_MOTEUR_TOURNER_HORRAIRE,
        DEFINE_SPEED1,
        "TOURNER HORAIRE " + str(DEFINE_SPEED1),
    )
    identification(
        ser,
        f3,
        DEFINE_COMMANDE_MOTEUR_TOURNER_ANTI_HORRAIRE,
        DEFINE_SPEED1,
        "TOURNER ANTI-HORAIRE " + str(DEFINE_SPEED1),
    )
    identification(
        ser,
        f3,
        DEFINE_COMMANDE_MOTEUR_TOURNER_HORRAIRE,
        DEFINE_SPEED2,
        "TOURNER HORAIRE " + str(DEFINE_SPEED2),
    )
    identification(
        ser,
        f3,
        DEFINE_COMMANDE_MOTEUR_TOURNER_ANTI_HORRAIRE,
        DEFINE_SPEED2,
        "TOURNER ANTI-HORAIRE " + str(DEFINE_SPEED2),
    )


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
