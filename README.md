# Telegram Guard Bot V7 — plusieurs groupes, VIP par invitations, pass 24 h et tirage

**Version de développement, non testée sur Telegram/Railway.** La V7 reprend la V6 (modération, hash photos/vidéos, horaires, panel propriétaire à boutons, trusted users, parrainage, publicités, catalogue VIP) et ajoute les modules ci-dessous. Les **31 tests unitaires** portent uniquement sur des fonctions locales ; ils ne prouvent pas le fonctionnement de l'API Telegram, des transactions PostgreSQL ou du déploiement Railway.

## Nouveautés demandées

| Fonction | Fonctionnement V7 |
|---|---|
| Plusieurs groupes principaux | `GROUP_IDS` accepte plusieurs IDs de supergroupes. Chaque groupe a **son propre schéma PostgreSQL**, ses règles, ses horaires, ses membres, son parrainage, ses VIP et son panneau. On choisit le groupe dans **/panel → 🌍 Choisir le groupe**. Chaque groupe autorisé doit être activé par un administrateur Telegram via **/setup** et un bouton de confirmation. Les groupes non autorisés sont refusés. |
| VIP par paiement **ou** invitations | Dans **/panel → 💎 VIP**, choisir **🎯 Invitations** sur une offre et définir un seuil (ex. 8). Le membre voit ses crédits dans **Mes invitations** et dans le catalogue VIP. Quand l'objectif est atteint et qu'il est encore membre du groupe principal, il peut cliquer sur **🎁 Débloquer**. Un bonus n'est accordé **qu'une fois par offre**, sans prolongation au clic suivant. |
| VIP 24 h | Durée **⏳ 24 heures** ajoutée à l'assistant de création d'offres. Le retrait est vérifié **chaque minute** ; une notification est tentée dans la dernière heure. L'expiration part de l'activation du droit (validation ou déblocage), et non de la première lecture des médias. |
| Groupe VIP 24/24 | Dans **/panel → 💎 VIP → ♾ 24/24**, permet de marquer un groupe VIP comme ouvert en permanence, distinct des groupes principaux à horaires. Le bot doit être administrateur avec droit de restriction ; un contrôle horaire réapplique les permissions de publication. |
| Lien d'accès sécurisé | Pour un achat approuvé **ou** un bonus débloqué, le bot crée un lien d'invitation personnel valable jusqu'à 24 h, avec **demande d'adhésion**. L'adhésion est approuvée seulement si l'ID Telegram correspond à celui du bénéficiaire ET si son abonnement est encore valide. Après approbation, le lien est révoqué. Les liens de parrainage restent distincts. |
| Tirage au sort | **/panel → 🏆 Tirage au sort** : définir le nombre minimum d'invitations validées, afficher le nombre de candidats encore membres et tirer uniformément **un candidat par participant éligible**. Historique des gagnants en base, notification propriétaire. L'attribution d'une récompense reste une action manuelle. |
| 🩺 Santé | Diagnostic par groupe : droits Telegram, scans médias en attente et anciens, livraisons VIP inachevées et abonnements expirés à retirer. |

**Pas de module « justice des inactifs », pas de pass gratuit historique, pas de cagnotte.** Les filtres de mots V6 sont conservés ; aucun second filtre concurrent n'est ajouté. Le classement TOP 10 et la comptabilisation après 5 minutes de présence sont conservés.

## Variables Railway

```dotenv
BOT_TOKEN=123456:CHANGE_ME
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/railway
# Remplace GROUP_ID pour utiliser plusieurs groupes. Le PREMIER doit être l'ancien GROUP_ID.
GROUP_IDS=-1001234567890,-1002345678901
OWNER_IDS=123456789
TRUSTED_USER_IDS=234567890,345678901
TZ=Europe/Paris
PAYMENT_CRYPTO_DETAILS=
PAYMENT_PAYSAFECARD_DETAILS=
PAYMENT_APPLE_PAY_DETAILS=
```

- Si tu avais un seul groupe dans la V6, `GROUP_ID` fonctionne toujours comme variable de secours. Pour plusieurs groupes, définis `GROUP_IDS`.
- **Ne change jamais l'ordre du premier ID dans `GROUP_IDS`** : la V6 utilisait le schéma SQL `public`. La V7 associe ce schéma au premier groupe et empêche le démarrage si on essaye de le changer après installation. Chaque groupe supplémentaire a son propre schéma `guard_<id>`.
- Garde **une seule instance Worker** sur Railway : plusieurs instances utilisant le même token avec `getUpdates` entrent en conflit. La V7 ne déploie pas un bot distinct par groupe.
- Les `OWNER_IDS` sont propriétaires dans tous les groupes gérés ; les trusted configurés via Railway sont trusted partout, ceux ajoutés dans le panneau via PostgreSQL sont propres au groupe sélectionné.
- Sauvegarde PostgreSQL **avant** tout redéploiement. Le fichier `schema.sql` applique des migrations additives à chaque schéma configuré.

## Procédure première activation d'un deuxième groupe

1. Dans Railway, ajouter son ID négatif dans `GROUP_IDS` **après** l'ID du groupe existant ; déployer.
2. Ajouter le bot au deuxième supergroupe avec les permissions administrateur de suppression, restriction, invitations et épinglage ; désactiver Privacy Mode dans BotFather.
3. Un **administrateur Telegram** du deuxième groupe utilise `/setup` ; le bot envoie la confirmation et contrôle ses droits. La modération n'est pas active avant cette confirmation.
4. En message privé au bot, le propriétaire utilise `/panel`, puis **🌍 Choisir le groupe** pour régler les horaires, publications, filtres, VIP et concours pour le deuxième groupe.
5. Pour les membres, `/groups` propose le groupe dont ils souhaitent consulter les VIP ou le parrainage. Les boutons publicitaires ajoutent aussi un lien profond vers le bon groupe. Le bot ne doit pas exposer les informations des groupes par les écrans d'un autre groupe.

## Ajouter un VIP et le rendre accessible via 8 invitations ou paiement

1. **/panel → 💎 VIP → ➕ Ajouter une offre** : saisir le chat ID du groupe VIP. La V7 **préautorise ce chat** avant de vérifier sa présence ; s'il indique qu'il n'est pas administrateur, ajouter le bot dans le VIP puis **renvoyer le même ID**. Un VIP préautorisé n'est pas traité comme groupe principal et n'est pas fermé automatiquement par les horaires.
2. Définir son titre, prix, durée (ex. **♾ À vie** ou **⏳ 24 heures**) et description.
3. Après création, cliquer sur **🎯 Invitations** et entrer `8`. Le prix reste possible, ou le membre atteint 8 invitations validées : **les deux parcours sont indépendants**.
4. Si ce VIP est un groupe toujours ouvert, activer **♾ 24/24** ; le groupe VIP doit être distinct des groupes principaux programmés dans `GROUP_IDS`.
5. Chaque membre reçoit son lien de parrainage depuis son tableau de bord. Un filleul doit être observé présent au-delà de cinq minutes avant le crédit. Cette vérification n'est pas révélée dans les écrans publics.
6. Une fois le seuil atteint, **🎁 Débloquer** crée un accès VIP ; le bot vérifie le compte demandeur lorsque l'utilisateur utilise son lien d'adhésion.

**Protection** : un lien de demande d'adhésion reste transférable, mais la demande de toute autre personne est refusée. L'adhésion nécessite le droit Telegram `can_invite_users`. L'ancienne V6 envoyait de simples liens limités à un membre : les nouveaux liens V7 passent par des demandes d'adhésion vérifiées.

## Tirage au sort

Un participant éligible dispose d'**une chance**, même s'il a 30 invitations et qu'un autre en a 8. Les invitations sont validées et le parrain doit toujours être membre observé du groupe principal. Le tirage utilise un générateur aléatoire cryptographique (`secrets.randbelow`) et inscrit le résultat en PostgreSQL. Les cadeaux ne sont **pas** distribués automatiquement.

## Fonctionnalités conservées de la V6

- Ouvertures programmées et manuelles, décompte/remplacement des messages, fermeture et suppression des messages suivis lorsque Telegram autorise l'effacement.
- Hash-ban `file_unique_id`, SHA-256, photos pHash 256 bits, vidéo multiframe FFmpeg ; liste noire, anti-repost, anti-join immédiat.
- Trusted users `/pedo`, `/mineur`, `/supprime`, `/pasfr`, `/clean`, `/info`, `/hashdemande`, et propriétaire via boutons.
- Publicités texte ou photo, posts programmés, règles épinglées, notifications et statistiques d'entrées/sorties.
- Catalogue VIP natif avec sélection multiple, paiement déclaré et vérification manuelle, et classement d'invitations anonymisé.

## Limites et précautions avant production

- **Les paiements externes existants de la V6 (crypto, Paysafecard, Apple Pay) sont conservés pour compatibilité, MAIS Telegram exige les Stars pour les biens et accès numériques vendus depuis un bot.** Ce parcours peut violer les règles de la plateforme et être restreint. Pour une vente conforme dans Telegram, remplacer le checkout par Telegram Stars (`XTR`). Une capture de paiement ne prouve pas qu'un règlement a eu lieu.
- **Un test local ne vaut pas un test Telegram.** Vérifier notamment `ChatJoinRequestHandler`, la gestion de plusieurs groupes actifs simultanément, les droits des bots dans VIP, l'expiration de 24 h et les transactions en PostgreSQL.
- **Les bans cross-groupes ne sont pas synchronisés** : chaque groupe garde une base de modération isolée. Il faut une fonctionnalité distincte de bannissements globaux si souhaitée. Les identifiants et hash bannis ne sont pas dupliqués automatiquement entre groupes.
- Les groupes VIP destinataires ne sont pas eux-mêmes soumis à la modération des messages principaux ; leur ouverture 24/24 concerne leurs permissions de publication. Aucune analyse des médias de ces VIP n'est introduite par la V7.
- L'ancien système A/B avec choix d'un groupe **unique** par soirée et bascule automatique en cas de panne **n'est pas repris**. La V7 gère plusieurs groupes **simultanément**, chacun avec sa propre planification.
- Pas de garantie d'analyse instantanée des gros médias, pas de connaissance des membres déjà présents avant l'installation, pas de suppression illimitée d'anciens messages avec l'API Telegram.
- Ne jamais utiliser le bot pour distribuer des contenus privés sans consentement ni du contenu sexuel impliquant des mineurs ; les empreintes servent à détecter et bloquer des contenus interdits, pas à les redistribuer.

## Tests locaux

```bash
python run_tests.py
python -m compileall -q .
```

La compilation et les 31 tests de logique ont été exécutés localement. **Les dépendances Telegram et asyncpg ne sont pas installées dans l'environnement de vérification ; le bot n'a pas été lancé contre une vraie API Telegram ou DB PostgreSQL.** Faire un déploiement de préproduction sur un groupe de test avant mise en service.
