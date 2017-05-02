# ping-pong-Raspberry-Intensity-Shuttle
Jouer ping-pong sur raspeberry contre un ordinateur qui reçoit la console de jeu via Intensity Shuttle et en faisant un traitement d'images il renvoie des commande pour faire bouger sa raquette.

# Description 
Le but de ce projet est de controler le jeu ping-pong entre deux joueurs (homme vs machine) qui tourne sur un raspberry.
ping-pong est un jeu qui a pour seul objectif, déplacer sa raquette de haut en bas pour faire rebondir la balle.

La console du jeu est transmise depuis le Raspberry via un Blackmagicdesign Intensity Shuttle connecté à l'ordinateur (la machine) via un port USB. 
Blackmagicdesign Intensity Shuttle est une solution de capture et de lecture en SD et en HD dont les signaux HDMI et la vidéo composant analogique sont d’une qualité spectaculaire. [détails](https://www.blackmagicdesign.com/fr/products/intensity)

# Comment le jeu est - il développé ?
Le jeu est developpé en Python à l'aide de la librarie Pygame.il utilise les sockets TCP pour créer une communication entre le raspberry et la machine distante pour que cette dernier puisse envoyer les commandes pour controler le jeu.
la machine distante utilise un script pour envoyer des commandes. Ce script permet de récuperer le flux video fourni par l'Intensity Shuttle et faire du traitement d'image pour comparer la posiion de raquette par rapport au pong ( en utilisant OpenCV avec Python) et ainsi envoyer des commandes au raspberry pour faire bouger la raquette.

à ce stade là, le projet offre la posibilté de faire bouger la raquette apartir de la machine distante en envoyant manuellement des commandes de jeu.la machine disttante peremt de comparere la position de la raquette par rapport au pong via un traitement d'image basé sur les couleurs.
Dans le script detect_circle_paddles_positions j'utilise la fonction cv2.HoughCircles pour detecter la positions de la pong (ball) en donnant comme parametre le rayon de cercle, et par detection des contours suivi d'un filtrage en se basant sur l'aire des contours je peux detecter la positions de deux paddles (raquettes).
