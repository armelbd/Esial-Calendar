**Ca sert à quoi :**

Le but est de synchroniser ADE avec un compte Google Calendar (vous pouvez ensuite synchro Google Calendar avec votre téléphone ou configurer des alertes par SMS).
Une fois configuré Google updatera 2/3 fois par jour votre agenda, ce qui permet d'être toujours au courant des modifications d'emploi du temps (beaucoup plus pratique que de se connecter à ADE pour vérifier)  

**Comment le configurer :**

Pour configurer la synchronisation il suffit de vous rendre dans votre agenda google et de cliquer sur la flèche à côté de "Autres Agendas" puis sur "Ajouter par URL" et de rentrer cette url :
http://esialcalendar.appspot.com/num_etudiant/2012

**Comment ça marche :**

En fait il s'agit d'un service "proxy" entre Google Calendar et ADE.
A chaque fois que Google Calendar fait une requête sur l'URL que vous avez rentrée, mon service va faire une requête sur ADE pour récupérer l'agenda et le redonner à Google sous la bonne forme (avec un système de cache pour ne pas surcharger ADE et pour gérer les cas où ADE ne répond pas...)
