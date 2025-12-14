# IPv4 & IPv6 Fragmentation Simulation (Python)

##  Objectif du projet

Ce dépôt montre **comment simuler la fragmentation IPv4 et IPv6** entre :

*  **Host Windows** (machine réelle)
*  **VM Ubuntu** (machine virtuelle)

La simulation est faite **avec Python (Scapy)** et des **commandes exécutées dans le terminal de la VM Ubuntu**.

---

##  Rappels théoriques rapides

### IPv4

* La fragmentation peut être faite par **les routeurs ou l’hôte**
* Champs importants : `ID`, `MF (More Fragments)`, `Fragment Offset`

### IPv6

* Pas de fragmentation par les routeurs
* Fragmentation **uniquement par l’hôte source**
* Utilisation de l’**Extension Header: Fragment Header**

---

## Prérequis

### Sur la VM Ubuntu on a installé ces dépendances via ces commandes dans le terminal:

```bash
sudo apt update
sudo apt install python3 python3-pip tcpdump -y
pip3 install scapy
```

remarque: Ultérieurement, on a exécuté les scripts avec **sudo** (Scapy en a besoin).

---

## Structure du dépôt

```
ip-fragmentation-simulation/
│
├── ipv4_fragmentation.py
├── ipv6_fragmentation.py
├── packet_analysis.py
└── README.md
```

---

## Simulation IPv4 (Windows ⇄ Ubuntu)

**IPv4 est testé dans les deux sens dans notre cahier de tp et aussi dans notre code** :

* Windows ➜ Ubuntu
* Ubuntu ➜ Windows

Avant chaque test, un **test de connectivité (ping)** est effectué.

---

### Consultez le Script Python – `ipv4_fragmentation.py` pour voir le code detaillé


### Capture côté VM Ubuntu en utilisant tcpdump l'equivalent en ligne de commande de Wireshark en Windows

```bash
sudo tcpdump -i any -n ip and icmp
```

### Exécution

#### Simulation Windows → Ubuntu

**Sur la VM Ubuntu (réception), on doit capturer les paquets :**

```bash
sudo tcpdump -i any -n ip and icmp
```

**Depuis Windows (source), on doit envoyer les paquets :**

```bash
sudo python3 ipv4_fragmentation.py
```

=>Observation :
- Fragments ICMP avec offsets différents
- Paquet rejeté si DF activé et MTU dépassée

#### Simulation Ubuntu → Windows

**Sur Windows (réception, avec Wireshark), on doit capturer les paquets ( les captures Wireshark sont dans le cahier de tp ):**

- Lancez Wireshark et appliquez le filtre `ip and icmp`
- Capturez sur l'interface réseau appropriée

**Depuis la VM Ubuntu (source), on doit envoyer les paquets :**

```bash
sudo python3 ipv4_fragmentation.py
```

Observation :
- Même comportement : fragments ou rejet selon DF

---

## Simulation IPv6 (Ubuntu ➜ Windows uniquement)

**IPv6 est simulé dans un seul sens dans le code et aussi dans notre cahier de tp:**

* Ubuntu ➜ Windows

Rappel :

* Pas de fragmentation IPv6 par les routeurs
* Fragmentation uniquement par l’hôte source
**Note :** Windows ne peut pas fragmenter IPv6 en tant que source (la pile IPv6 de Windows ne gère pas la fragmentation sortante), d'où la simulation uniquement depuis Ubuntu vers Windows.
---

### consultez le Script Python – `ipv6_fragmentation.py` pour voir le code detaillé 

### Capture côté VM Ubuntu (de même)

```bash
sudo tcpdump -i any -n ip6
```

### Exécution

**Dans le terminal de la VM Ubuntu, on doit envoyer les paquets :**

```bash
sudo python3 ipv6_fragmentation.py
```

**Sur Windows, on a aussi visualisé les paquets sur Wireshark ( voir le cahier de tp ) :**

Observation :
- Plusieurs fragments IPv6 avec Extension Header Fragment (Next Header=44).
---

## Analyse des résultats avec `packet_analysis.py` 

Ce script Python utilise Scapy pour capturer et analyser les paquets en temps réel, en détectant la fragmentation IPv4/IPv6.

### Utilisation

**Pour analyser IPv4 :**

```bash
sudo python3 packet_analysis.py ipv4 [interface]
```

**Pour analyser IPv6 :**

```bash
sudo python3 packet_analysis.py ipv6 [interface]
```

Exemple : `sudo python3 packet_analysis.py ipv4 eth0`

Le script affiche :
- Adresses source/destination
- Taille du paquet
- Champs de fragmentation (ID, flags, offset pour IPv4 ; Fragment Header pour IPv6)
- Détection de fragments

Utile pour une analyse programmatique des captures, complémentaire à tcpdump/Wireshark.

---
## Ce qui a été simulé

- IPv4 fragmenté **dans les deux sens** (Windows ⇄ Ubuntu)
- IPv4 avec et sans **Don't Fragment (DF)**
- IPv6 fragmenté **dans un seul sens** (Ubuntu ➜ Windows)
- IPv6 avec et sans **Fragment Header**
- Tests de connectivité avant chaque envoi
- Captures de paquets via tcpdump / Wireshark

---

## Auteurs: 

Malek Azri - Amira Lahiani - Mohamed Abdelwahed \n
Tp: Fragmentations IPV4, IPv6 – Réseaux & Protocoles IP

---

