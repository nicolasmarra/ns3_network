# ns3_network


Ce depôt contient les scripts et les fichiers utilisés dans le cadre du TP Réseaux Sans-Fil dont le but était approfondir notre compréhension des technologies LoRaWAN et Wi-Fi.

**Description**
Dans le premier exercice, nous avons analysé l'impact de plusieurs paramètres de la technologie LoRaWAN, notamment le coding rate, le CRC et le mode de trafic, sur la consommation énergétique.

Dans le cadre de l'exercice 2, nous avons étudié la performance de la technologie LoRaWan et Wi-Fi en fonction du nombre de nœuds. Notre objectif était d’évaluer l’impact du nombre de nœuds sur plusieurs métriques telles que le taux de succès des paquets (PDR), la latence moyenne et la consommation énergétique. Nous avons détaillé nos méthodologies de simulation (les scripts que nous avons développés ou améliorés) et analysé les résultats obtenus.

**Structure de répertoires**
- **Exo1/** : Scripts et fichiers pour l'exercice 1 du TP
  - `exo1.cc`
  - `extract.py` : Script qui parse le fichier de log et trace des courbes sur la consommation énergétique en fonction du temps, utilisé pour étudier l'impact de paramètres de la technologie LoRa
  - `class-a-end-device-lorawan-mac.cc`
  - `lorawan-mac-helper.cc`
  - `exo1_6.cc`
- **Exo2/** : Scripts pour l'exercice 2 du TP
  - `exo2-wifi.cc`
  - `exo2-lora.cc`
  - `calculer_metriques.py` : Script qui permet de parser les fichiers de log et calculer les métriques pour LoRa
- **rapport.pdf** : Rapport du TP au format PDF.

**Instructions de Compilation**
1. Installer [ns3](https://www.nsnam.org/releases/ns-3-41/)
2. Cloner ce répertoire dans le répertoire scratch de ns3.
3. Pour compiler l'exercice 1 :
   ```
   ./ns3 run exo1.cc
   ./ns3 run exo1_6.cc
   ./ns3 run exo1_6.cc -- -- --coding_rate=1 crc=TRUE ou FALSE mode_trafic=0 (UNCONFIRMED_DATA_UP) ou 1 pour (CONFIRMED_DATA_UP)
   ```
4. Pour compiler l'exercice 2 :
   ```
   ./ns3 run exo2_wifi.cc sans arguments (nodes=10 par défaut)
   ./ns3 run exo2_wifi.cc -- num_nodes=20 pour lancer 200 nœuds
   ./ns3 run exo2_lora.cc sans arguments (nodes=100 par défaut)
   ./ns3 run exo2_lora.cc -- num_nodes=200 pour lancer 200 nœuds
   ```
5. Pour parser les métriques avec le script `calculer_metriques.py` :
   ```
   ./ns3 run exo2_lora.cc -- num_nodes=200 2>>log.txt
   python3 calculer_metriques.py log.txt
   ```

**Remarque**
Nous avons modifié les fichiers d'exemples disponibles sur [ce dépôt](https://github.com/signetlabdei/lorawan) ainsi que certains fichiers de LoRa pour ns3.
