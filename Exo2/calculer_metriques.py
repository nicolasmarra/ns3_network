import re
import sys


# Fonction pour extraire les paquets envoyés et reçus, et aussi le délai de transmission à partir du fichier log
def extraire_paquet(fichier_log):

    paquet_envoyes = 0
    paquet_recus = 0
    envoie_heure = 0
    reception_heure = 0
    variation_envoi_reception = 0

    # Expression régulière pour vérifier si un paquet a été envoyé
    regex_envoi = re.compile(r'EndDeviceLorawanMac:DoSend\((0x[0-9a-fA-F]+)')

    with open(fichier_log, 'r') as fichier:


        for ligne in fichier:
            verifier_envoi = regex_envoi.search(ligne)
            
            # Si un paquet a été envoyé, on récupère l'heure d'envoi et on incrémente le nombre de paquets envoyés
            if verifier_envoi:
                envoie_heure = float(ligne.split()[0][1:-1])
                paquet_envoyes+=1

            # Si un paquet a été reçu, on récupère l'heure de réception et on incrémente le nombre de paquets reçus
            elif "GatewayLorawanMac:Receive(): Received packet" in ligne:
                reception_heure = float(ligne.split()[0][1:-1])
                variation_envoi_reception += reception_heure - envoie_heure
                paquet_recus+=1

    return paquet_envoyes, paquet_recus,variation_envoi_reception



# Fonction pour calculer le taux de succès des paquets (PDR)
# PDR = (nombre de paquets reçus / nombre de paquets envoyés) * 100
def calculer_pdr(paquet_envoyes, paquet_recus):
    nb_paquet_envoyes = paquet_envoyes
    nb_paquet_recus = paquet_recus

    if nb_paquet_envoyes == 0:
        return 0

    pdr = (nb_paquet_recus / nb_paquet_envoyes) * 100
    return pdr

def main():

    # On doit passer en argument le fichier log
    if len(sys.argv) != 2:
        print("Usage: python calculer_pdr.py fichier.log")
        sys.exit(1)


    fichier_log = sys.argv[1]
    paquet_envoyes, paquet_recus,variation_envoi_reception = extraire_paquet(fichier_log)
    pdr = calculer_pdr(paquet_envoyes, paquet_recus)
    print("Nombre total de paquets envoyés par les nœuds :", paquet_envoyes)
    print("Nombre total de paquets reçus par la passerelle :", paquet_recus)
    print("Packet Delivery Ratio (PDR) : {:.2f}%".format(pdr))
    print("Latence moyenne : {:.2f} s".format(variation_envoi_reception/paquet_recus))

if __name__ == "__main__":
    main()
