# PI2C : Quoridor Game

Ce projet a pour but de créer une intelligence artificielle capable de jouer de façon autonome à un jeu de plateau qui dans notre cas est le jeu du quoridor. 

## Fonctionnalités de l'IA

- Connexion TCP à un serveur 
- Communication serveur/client
- Déplacement automatique du joueur 
- Placement automatique de murs en fonction de la position de l'adversaire

## Stratégie utilisée 

La stratégie utilisée pour notre IA est assez simple. Le choix du mouvement se base sur un calcule de distance entre chaque joueur et le bord opposé du plateau. 

La fonction distance_to_win calcule la distance entre notre IA et le bord du plateau en fonction de si nous sommes le joueur un 0 ou 1. La fonction distance_player2_to_win effectue le même calcul mais elle commence par relever la position de l'adversaire afin de voir quelle est la distance qu'il lui reste à parcourir pour gagner et toujours en prenant en compte le fait qu'il peut être le joueur 0 ou le joueur 1. 

Ces distances permettent ensuite de décider du mouvement à jouer. Pour ce faire, nous avons posé certaines conditions. 

Dans le cas où l'adversaire est plus proche de gagner, on place un mur devant lui. Si notre IA est plus proche de gagner, on continue d'avancer vers notre objectif. Et si notre IA est plus proche de gagner mais que notre adversaire n'est pas bloqué, on le bloque quand même. 

Dans le cas où on se déplace, le mouvement est choisi via la fonction heuristic qui trie les mouvements possibles et en ressort celui qui nous permettra d'atteindre le bord du plateau au plus vite. 

## Bibliothèques utilisées

- Bibliothèque socket : utilisée pour la création et la gestion des connexions réseaux sur une même machine ou entre des machines distances via une communication TCP (ou IP)
- Bibliothèqe json : utilisée pour encoder et décoder des données en format json en python
- Bibliothèque random : utilisée dans un cas spécifique où seul un déplacement à gauche ou à droite est possible
- Bibliothèqe simpleai : utilisée pour implémenter notre mini algorithme de recherche (fonction heuristic)

## Utilisation 

Afin de pouvoir utiliser cette IA, il faut commencer par démarrer correctement le serveur se trouvant dans le dossier PI2CChampionshipRunner en spécifiant convenablement le nom du jeu. Mais avant ça, il faut s'assurer que tous les bibliothèques sont installées dans la version python utilisée. Les bibliothèques nécessaires au lancement de serveur sont disponibles dans le fichier requierements.txt du dossier PI2C. 

Les modules peuvent directement être installés depuis le terminal via la commande 'pip -r install requirements.txt'

Ensuite, il ne reste qu'à lancer les codes de deux joueurs. Une fois la requête de connexion acceptée et la réponse au ping convenablement envoyée, la partie peut commencer. 

Afin de pouvoir jouer, il est essentiel de pouvoir recevoir des requêtes de jeu, et de répondre à ces requêtes avec un format correct. Autrement, les mouvements de type pawn ou blocker ne seront pas reconnus. 

Pour information, chacun des échanges entre le serveur et le client se font via des fichiers json. 

## Auteur 

Ce projet a été développé par Onya Pierrot et Mournin Ibtihal.
