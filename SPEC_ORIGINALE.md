# Cahier des charges de référence — groupe Telegram

Ce fichier traduit la demande originale de l'utilisateur en comportements vérifiables. Il prime sur les anciennes interprétations « message unique » : seuls les décomptes et les publications d'un même emplacement se remplacent ; les règles et les pubs photo restent des messages séparés pendant l'ouverture.

## Installation et comptage

- Un seul Worker Railway, PostgreSQL, un token Telegram. Activation explicite par un administrateur réel du groupe, après vérification des droits du bot. Supergroupes principaux et VIP distincts, enregistrés par sélection de rôle au moment de l'ajout.
- Compter entrées et sorties observées et afficher le nombre de membres réel fourni par Telegram. Ne pas présenter le solde observé comme un recensement exhaustif des anciens membres.
- Bannir à l'entrée les noms contenant des lettres non latines si le filtre est activé ; bannir les noms contenant un motif interdit complet, sans distinction de casse.

## Horaires

- Créneaux multiples et chevauchants ; franchissement de minuit ; zone horaire configurable.
- Mode ON : ouverture à l'heure prévue, fermeture à l'heure effective de fin de l'union des créneaux. Décompte chaque heure et à 30, 15, 5, 3, 2 et 1 minutes avant les transitions. Supprimer l'ancien décompte avant le nouveau.
- Mode OFF : décompte avant la fenêtre prévue pour susciter l'intérêt, mais ne pas ouvrir ; afficher « Restez branchés jusqu'à la prochaine ouverture » à l'heure du début.
- Ouverture manuelle : deux heures maximum et avertissement privé quinze minutes avant expiration ; fermeture manuelle, retour au calendrier et priorité claire entre les overrides.
- À la fermeture : bloquer les publications, supprimer les messages suivis de l'ouverture et les publications du bot connues, puis annoncer la prochaine ouverture avec une vraie date/heure.

## Modération

- Pendant l'ouverture : seuls texte, photo et vidéo passent. Forward ON/OFF ; si refusé, suppression sans sanction. Lien ou story : ban immédiat, alerte publique supprimée après 30 secondes.
- Mot interdit : suppression silencieuse, mute 1 jour, puis 2 jours, puis 7 jours. Noms interdits vérifiés à l'entrée.
- Identifiants Telegram, SHA-256, pHash photo 256 bits et empreinte vidéo sur plusieurs images ; comparaison d'abord par identifiant, puis analyse asynchrone bornée. Un média interdit entraîne un ban.
- Trusted : `/pedo` en réponse à n'importe quel message du membre cible bannit ses médias connus, supprime ses messages récents et le bannit ; `/mineur` supprime et mute 3 jours puis bannit à la récidive. La commande du trusted disparaît.
- Commande slash d'un non trusted : suppression et mute 3 jours. Signalement `@admin` en réponse à un média : agrégation de signalements distincts, sanction et remerciement public sans dévoiler le seuil.

## Publications, règles, invitations

- Règles configurables : envoyer et épingler à l'ouverture ; remplacer toutes les 30 minutes ; supprimer à la fermeture.
- Plusieurs pubs texte ou photo légendée, avec bouton facultatif ; fréquences 30 min, 2 h, 3 h, 6 h pour les pubs ordinaires ; chaque pub remplace sa précédente publication. Pub VIP : 2 h, 3 h, 5 h, 10 h.
- Lien personnel d'invitation, crédit après présence vérifiée de cinq minutes, tableau de bord, TOP 10 anonymisé, tirage au sort.
- Option inactifs : avertir après une ouverture sans publication, rendre éligible après une autre ouverture sans publication ; l'admin voit nombre et ancienneté moyenne et peut purger (exclure sans laisser un ban actif). Si la personne revient après purge, bannissement.

## VIP et paiements

- Détecter le groupe VIP après ajout du bot administrateur ; proposer le groupe détecté dans le panneau. Configurer offre, description, prix, durée et activation. Plusieurs offres possibles, dont 30 jours ou accès à vie ; lien personnel de demande d'adhésion vérifié contre le compte Telegram.
- Commande manuelle Crypto/PayPal/Revolut selon configuration ; image justificative ; approbation par le seul propriétaire après contrôle réel des fonds ; livraison réessayable ; notification et retrait de l'accès expiré.
- Le flux demandé de paiement externe n'est pas conforme aux règles Telegram sur les biens numériques vendus dans les bots. Une migration vers Telegram Stars est requise avant l'exploitation commerciale conforme.

## Contraintes de l'API et validation

- L'API Bot ne fournit pas la liste complète des anciens membres ni l'historique complet du chat. Une panne peut perdre des événements. `deleteMessage` impose une fenêtre de suppression généralement inférieure à 48 heures. L'analyse de gros fichiers et les droits admin dépendent de Telegram réel.
- Tester sur un groupe isolé avec PostgreSQL : installation, droits, horaires ON/OFF, chevauchements, manuel, décompte, règles, pubs photo, modération, hash, suppression à la fermeture, inactifs, invitations, VIP, paiement, expiration et redémarrage. Les tests locaux ne prouvent pas ces interactions réseau.
