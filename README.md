# Telegram Guard Bot — reconstruction V9

Bot Python pour Railway, Telegram et PostgreSQL. **Version de développement** : les tests locaux ne remplacent pas un essai réel sur un supergroupe isolé.

## Installer

1. Créer un bot avec BotFather et désactiver Privacy Mode pour recevoir tous les messages du groupe.
2. Ajouter PostgreSQL sur Railway ; configurer `BOT_TOKEN`, `DATABASE_URL`, `OWNER_IDS` et éventuellement `TZ=Europe/Paris` et `TRUSTED_USER_IDS`.
3. Installer `requirements.txt` et lancer un seul Worker avec `python -m app`. Ne pas lancer deux pollers avec le même token.
4. Ajouter le bot comme administrateur d'un supergroupe avec suppression, restriction, invitation et épinglage ; choisir son rôle depuis les boutons. Confirmer le groupe principal ; `/setup` reprend une installation interrompue.
5. Utiliser `/panel` en privé. Tester la fermeture et la suppression sur un groupe isolé avant la production.

## Architecture

- `app.py` : adaptateurs Telegram, configuration et orchestration périodique ; un verrou par groupe évite les transitions simultanées.
- `schedule_policy.py` et `logic.py` : décision pure des horaires, chevauchements, minuit, overrides et mode teaser OFF.
- `activity.py` : participation par ouverture, avertissement et purge.
- `media_guard.py` et `media_pipeline.py` : analyse bornée des téléchargements, hash exact et perceptuel, vidéos multi-images et sanctions.
- `multigroup.py` : routage par groupe ; `schema.sql` : tables par schéma PostgreSQL, migrations incrémentales.
- `commerce_ui.py`, `vip_rules.py`, `admin_ui.py`, `onboarding.py` : vues et règles métier.

## Comportement principal

- Mode automatique ON : décomptes horaires, puis 30, 15, 5, 3, 2 et 1 minutes ; ouverture et fermeture aux fenêtres configurées. Mode OFF : décompte promotionnel, groupe fermé et message « Restez branchés » au début du créneau.
- Ouverture manuelle : maximum deux heures, avertissement privé au propriétaire quinze minutes avant expiration. Fermeture manuelle : jusqu'au prochain créneau ; reprise des horaires par bouton.
- Chaque **décompte** remplace le précédent. Les règles ont leur propre message épinglé, remplacé toutes les trente minutes. Les publications texte ou photo ont leur propre cadence et remplacent chacune leur publication précédente. L'alerte de lien dure trente secondes.
- À la fermeture, le bot supprime les annonces qu'il connaît et tente de supprimer tous les messages du groupe suivis pendant l'ouverture, en parcourant toutes les pages. Les échecs restent en base pour une nouvelle tentative.
- Les entrées/sorties sont comptées depuis les événements reçus ; l'effectif réel est demandé à Telegram. L'historique antérieur à l'installation n'est pas reconstructible.
- Le panneau « Inactifs » peut avertir en privé après une ouverture sans participation, rendre éligible après une seconde ouverture sans message, puis exclure sur décision du propriétaire. Un membre ainsi exclu qui revient est banni.
- `/pedo`, `/mineur`, les signalements, filtres de mots/noms, anti-repost, invitations et VIP suivent le cahier des charges transmis.

## Paiements

Les méthodes manuelles Crypto/PayPal/Revolut s'affichent seulement si leurs instructions `PAYMENT_*_DETAILS` existent. La preuve est une image ; seul le propriétaire confirme la réception effective de fonds, puis le bot délivre un lien VIP personnel. **La capture ne prouve pas un paiement.** Pour les accès numériques vendus à l'intérieur de Telegram, les règles actuelles de la plateforme exigent Telegram Stars ; le flux manuel demandé ici doit être remplacé par Stars avant une exploitation conforme.

## Limites explicites

- Telegram refuse normalement la suppression d'un message âgé de plus de 48 heures. Un bot ne peut pas récupérer l'historique complet d'un groupe ou des mises à jour perdues pendant une panne. La fermeture ne peut donc pas promettre une suppression absolument exhaustive.
- Certains utilisateurs n'ont jamais ouvert le bot en privé : les avertissements privés d'inactivité échouent alors. Le panneau conserve leur statut d'inactivité.
- L'analyse perceptuelle d'une grosse vidéo est asynchrone ; un média peut être visible brièvement avant sanction. Le cloud Bot API limite les téléchargements des fichiers volumineux.
- Les fonctionnalités Telegram et les migrations PostgreSQL doivent être validées sur Railway. Les tests locaux vérifient seulement la logique et les scénarios simulés.

## Validation locale

```bash
python run_tests.py
python -m compileall -q .
```
