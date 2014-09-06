gExtractWinIcons
================
**Descrizione:** Estrae cursori e icone da file di risorse per MS Windows

**Copyright:** 2009-2014 Fabio Castelli <webreg(at)vbsimple.net>

**Licenza:** GPL-2+

**Codice sorgente:** https://github.com/muflone/gextractwinicons

**Documentazione:** http://url.muflone.com/gextractwinicons

Requisiti di sistema
--------------------

* Python 2.x (sviluppato e testato per Python 2.7.5)
* Libreria XDG per Python 2
* Libreria GTK+3.0 per Python 2
* Libreria GObject per Python 2
* Libreria Distutils per Python 2 (generalmente fornita col pacchetto Python)
* Pacchetto IcoUtils (comandi wrestool e icotool)

Installazione
-------------

E' disponibile uno script di installazione distutils per installare da sorgenti.

Per installare nel tuo sistema utilizzare:

    cd /percorso/alla/cartella
    python2 setup.py install

Per installare i files in un altro percorso invece del prefisso /usr standard
usare:

    cd /percorso/alla/cartella
    python2 setup.py install --root NUOVO_PERCORSO

Utilizzo
--------

Se l'applicazione non è stata installata utilizzare:

    cd /path/to/folder
    python2 gextractwinicons.py

Se l'applicazione è stata installata utilizzare semplicemente il comando
gextractwinicons.
