# Projet-TDD


## IMPORTANT : 

```py
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../backend/function/userHandler/src") # Lambda GET
    )
)
import index as get_index
```

et 

```py
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../backend/function/userHandlerPost/src") # Lambda POST
    )
)
import index as get_index
```

Sont des imports de modules depuis des chemins, et donc même si les 2 `index.py` des lambdas sont dans des fichiers différents Pyhton récupère le 1er `index.py` qu'il trouve ce qui fait que mes tests "GET" appellaient en fait le `handler()` de la lambda POST, d'où le problème de "Missing name or email".

J'ai donc remplacé ces imports par des imports absolus, et par conséquent il faut ajouter une variable d'environnement avant de lancer la commande `pytest`

Pour lancer les tests voici la commande a executer : 

#### Changer \Chemin\Vers\Le Dossier\Du Repo\ par le chemin du dossier ou se trouve le clone du repo

```sh
$env:PYTHONPATH="C:\Chemin\Vers\Le Dossier\Du Repo\Projet-TDD\my-app\amplify"; pytest -v
```

## Installation

```sh
cd my-app
```

```sh
py -m venv .venv
```
WINDOWS :
```sh
.\.venv\Scripts\activate
```
MAC :

```bash
source .\.venv\Scripts\activate
```

```sh
pip install boto3
pip install moto==4.1.12
pip install pytest
```

```sh
cd amplify
```

#### Changer \Chemin\Vers\Le Dossier\Du Repo\ par le chemin du dossier ou se trouve le clone du repo

```sh
$env:PYTHONPATH="C:\Chemin\Vers\Le Dossier\Du Repo\Projet-TDD\my-app\amplify"; pytest -v
```

