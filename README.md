# CobApp

Définissons ici l'architecture et les principales fonctionnalités attendues de l'API *(interface de programmation d'application - logique serveur)* de l'application CobApp

editer planning avec jalons
liste des fonctionnalités
définition des premiers besoins
faire cahier des charges du prototype
faire toute lcd ..a chaine, de la commande d'un produit à la livraison en passant par les validations (ou non suivant le type de matériel), le chargement (avec bon de livraison)

faire toute la structure avec 5 produits, 2 chantiers, 5 utilisateurs, ....


## Roles
 --- 
Travaux - sur site - version mobile :
 - Chef Chantier
 - Conducteur Travaux
 - Directeur Travaux
 - Chauffeur

 Bureau - version web :
 - Conducteur Travaux
 - Directeur Travaux
 - Patrons
 - Responsable études
 - Administrateur

 Dépôt - web & mobile :
 - Gestionnaire dépôt
 - Ouvrier dépôt
 - Chauffeur

Appel Matériaux (pour chargement des camions uniquement):
 - GestionnaireAM
 - Ouvrier AM
 - Chauffeur

A voir pour plus tard :
 - Services support

---
## Chantier
---

### Chef de chantier:
Il est affecté à un et un seul chantier. 

**Responsable** : Directeur Travaux

**Lire** : toutes les infos du chantier

**Écrire** : aucun droit (sauf demande benne, et pointage personnel quand on y viendra)

**Modifier** : aucun droit

**Supprimmer** : aucun droit

---
### Conduc
Il est affecté à plusieurs chantiers

**Responsable** : Directeur Travaux

**Lire** : toutes les infos des chantiers

**Écrire** : aucun droit

**Modifier** : peut tout modifier (sauf infos bloquées par Administrateur)

**Supprimmer** : peut supprimer les erreurs

---
### Directeur de travaux
Il est affecté à 10/15 chantiers
**Responsable** : Directeur Travaux

**Lire** : toutes les infos des chantiers

**Écrire** : peut tout faire, en particulier remplir la fiche de démarrage chantier

**Modifier** : peut tout modifier (sauf infos bloquées par Administrateur)

**Supprimmer** : peut supprimer les erreurs

---
### Patron
Il peut voir tous les chantier

 **TOUT...**

...en lecture uniquement

---
### Responsable études
A accès à tous les chantiers en lecture

**Écrire** / **Supprimer** : Est en charge de l'écriture et création des nouveaux chantier

**Faire apparaitre la fiche démarrage chantier ici**

---
### Administrateur
**Peut tout faire**

---
### Utilisateurs Dépôt

Même principe que les utilisateurs chantier mais dépôt uniquement

- Responsable : tout
- Logistique : éventuellement modification stock
- Ouvrier : lecture seule

---
## Commande
---
### Chef de chantier:
Commande de son chantier uniquement

**Valideur** : Conducteur Travaux / Directeur Travaux

**Lire** : peut voir tout ce qui se passe concernant son chantier

**Écrire** : uniquement rédaction des commandes et validation déchargement

**Modifier** : aucun droit

**Supprimmer** : aucun droit

---
### Conduc
Commandes de ses chantiers uniquement

**Valideur** : Directeur Travaux

**Lire** : peut voir tout ce qui se passe concernant ses chantiers

**Écrire** : peut tout faire

**Modifier** : modifier ses commandes

**Supprimer** : supprimer ses erreurs

---
### Directeur de travaux
Commandes de ses chantiers uniquement

**Valideur** : (Patrons si litiges)

**Lire** : peut voir tout ce qui se passe concernant ses chantiers

**Écrire** : aucun droit, si ce n'est valider

**Modifier** : aucun droit

**Supprimmer** : aucun droit

---
### Patron
Est amené à résoudre les litiges, à voir si c'est nécessaire de mettre ça sur l'appli

---
### Administrateur
**Peut tout faire**

---
### Responsable Dépôt
Réceptionne l'ensemble des commandes et les traite par ordre chronologique

**Valideur** : (Patrons si litiges)

**Lire** : peut tout voir

**Écrire** : aucun droit, si ce n'est valider

**Modifier** : modifier selon disponibilités stock, et arbitrage - en particulier **date & heure**

**Supprimmer** : peut tout supprimer - soumis à validation conduc

---
### Logistique Dépôt
Chargement/Déchargement des camions

**Valideur** : Responsable Dépôt

**Lire** : peut tout voir

**Écrire** : aucun droit, si ce n'est valider

**Modifier** : modifier selon disponibilités stock, et arbitrage - en particulier **date & heure**

**Supprimmer** : peut tout supprimer - soumis à validation conduc

---
## Validation
---

Les chaines de validation sont définies plus haut.

A prendre en compte :
- Validation de plusieurs supérieur ? ex: chef chantier, conduc, conduc principal, chef de groupe, directeur tvx...
- Créer un système de suppléant en cas d'absence

---
## Chargement / Déchargement
---

Le système visé sera le suivant :
- Edition d'un bon de commande lors de la validation de la commande chantier par le responsable dépôt
- Création d'un planning de livraison / Retour sur base des bons de commandes édités
- Chargement du camion sur la base du bon de commande
- Edition d'un bon de livraison une fois le camion chargé : idéalement identique au bon de commande, mais être modifié si camion plein
- Livraison sur site - notification au chef de chantier
- Déchargement : validation du bon de livraison par chef de chantier et signature, doit pouvoir être modifié si il manque quelque chose, ou s'il y a du matériel en plus

**l'objectif principal est que tout le matériel soit affecté à un stock** que ce soit le stock du dépôt ou le stock chantier

---
## Cas des matériaux et consommables
---
Besoin de faire réunion avec Appel Mat sur :
- utilisation Dolibarr
- autorisation CRUD à définir
- API Dolibarr à récupérer chez nous
- Système de bons de commandes et chargement à valider avec eux

---
## Facturation
---
Facturation sur la base des stocks chantiers pour la location du matériel

Facturation sur la base des bons de livraison pour les matériaux et consommables

---
## Bennes
---
A voir avec CCP, a priori voilà les quelques fonctionnalités à implémenter ici :
- commande benne : nombre et type
- planning du chauffeur sur base des demandes
- visualisation des bennes sur les chantiers (ex: crépy - 1 DIB, 1 Bois, 1 Ferraille)
- validation dépôt/récupération par chef et chauffeur + photo

---
## Gestion personnel
---
A voir avec service RH

A priori :
- récupération liste personnel/chantier
- pointages par le chef
- validation par conduc Tvx
- partage des infos au service RH

---
## Administration
---
L'administration est aujourd'hui gérée sur l'API directement
A terme, il faudra développer un module pour l'application, sur lequel les adminstateurs pourront gérer : 
- Les utilisateurs
- Les salariés
- Les chantiers
- Les affectations


---
## Pour aller plus loin
---
- Intégration des fonctionnalités QSE à l'application : 1/4h sécurité, autocontroles, visites sécurités, diffusion informations
- Développement d'une application spécifique au dépôt
- Développement de fonctionnalités supplémentaires en liaison avec les autres services du bureau - pseudo ERP : demande congés, validation factures
