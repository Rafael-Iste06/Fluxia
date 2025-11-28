
FLUXIA PROGRAMMING LANGUAGE DOCUMENTATION (Plain Text)

===============================================
1. Introduction
===============================================
Fluxia est un langage de programmation compilé vers une machine virtuelle dédiée (VM), conçu pour être polyvalent et moderne.
Il est idéal pour :
- Interfaces graphiques (desktop et mobile)
- Interfaces web (frontend et backend)
- Scraping et automatisation
- Intelligence artificielle et machine learning
- Data science et big data
- Cybersécurité et cryptographie

Philosophie :
- Syntaxe claire, intuitive et moderne
- Sécurité et performance
- Extensible et modulable
- Programmation orientée objet, fonctionnelle et réactive

===============================================
2. Installation et dépendances
===============================================
- Python 3.10+ requis
- Pour GUI : PySide6 (Qt) -> pip install PySide6
- Structure du projet :
  fluxia.py
  fluxia_lexer.py
  fluxia_parser.py
  fluxia_compiler.py
  fluxia_vm.py
  fluxia_gui.py
  examples/

===============================================
3. Syntaxe de base
===============================================
3.1 Variables
- Déclaration : let x = 10;
- Globale implicite : y = 20;

3.2 Types
- number : nombres (entiers et flottants)
- string : chaînes de caractères
- bool : true / false
- null : valeur nulle

3.3 Fonctions
- Déclaration : 
  fn add(a, b) {
      return a + b;
  }
- Appel : let r = add(2, 3);

- La fonction main() est appelée automatiquement

3.4 Expressions et opérateurs
- Arithmétiques : +, -, *, /
- Comparaison : >, <, >=, <=, ==, !=

3.5 Structures de contrôle
- If / Else :
  if (x > 0) { ... } else { ... }
- While :
  while (i < 5) { ... }

3.6 Appels et fonctions natives
- print(a, b, ...)
- Avec module gui : gui_app, gui_label, gui_button

===============================================
4. Modules natifs
===============================================
4.1 GUI (PySide6 / Qt)
- use gui;
- Fonctions disponibles :
  gui_app(title, builder_fn_name)
  gui_label(win, text)
  gui_button(win, text, callback_fn_name)
- Exemple :
  use gui;

  fn build_ui(win) {
      gui_label(win, "Hello!");
      gui_button(win, "Click me", "on_click");
  }

  fn on_click() {
      print("Button clicked!");
  }

  fn main() {
      gui_app("Fluxia Demo", "build_ui");
  }

4.2 Web, Scraping, IA/ML, Data Science, Cryptographie
- Modules futurs ou à ajouter comme extensions natives
- Exemple futur : use web; use ai; use crypto;

===============================================
5. Machine Virtuelle (VM)
===============================================
- Stack-based VM
- Frame par fonction
- Piles : stack (données), call_stack (frames)
- Environnements : variables locales et globals
- Instructions : PUSH_CONST, LOAD_VAR, STORE_VAR, POP, BINARY_*, JUMP, JUMP_IF_FALSE, CALL, RETURN

Cycle d'exécution :
1. fetch instruction
2. decode instruction
3. execute instruction
- Garbage collector automatique via Python
- Sandbox pour sécurité : accès restreint aux builtins et modules

===============================================
6. Interopérabilité
===============================================
- Python : fonctions natives (builtins) peuvent appeler Python
- C/C++ : extensions via bindings futurs
- JavaScript : export possible via WebAssembly ou serveur

===============================================
7. Exemples de code
===============================================
7.1 Hello World
let a = 10;
let b = 20;
print(a + b);

fn main() {
    print("Hello Fluxia");
}

7.2 GUI simple
use gui;

fn build_ui(win) {
    gui_label(win, "Hello from Fluxia GUI!");
    gui_button(win, "Click me", "on_click");
}

fn on_click() {
    print("Button clicked!");
}

fn main() {
    gui_app("Fluxia GUI Demo", "build_ui");
}

7.3 API Web basique (futur)
use web;
fn main() {
    http_get("https://example.com", "callback");
}

7.4 Script Scraping (futur)
use scrape;
fn main() {
    let data = scrape_html("<html>...</html>");
}

7.5 Mini modèle IA (futur)
use ai;
fn main() {
    let model = NeuralNet();
    model.train(dataset);
}

7.6 Analyse de données (futur)
use data;
fn main() {
    let df = load_csv("data.csv");
    print(df.mean());

7.7 Chiffrement / Déchiffrement (futur)
use crypto;
fn main() {
    let msg = "hello";
    let enc = encrypt(msg, "key");
    let dec = decrypt(enc, "key");
}

===============================================
8. Outils de développement
===============================================
- fluxia.py : CLI pour exécuter un fichier .fx
- fluxia_lexer.py : analyse lexicale
- fluxia_parser.py : parser AST
- fluxia_compiler.py : compilation AST -> bytecode
- fluxia_vm.py : machine virtuelle
- fluxia_gui.py : module GUI Qt
- Gestionnaire de paquets : futur
- IDE / plugin : futur

===============================================
9. Roadmap d'évolution
===============================================
- Ajout de types avancés, classes, objets
- Module web complet (HTTP, REST, WebSocket)
- Module IA complet (ML, NLP, vision)
- Système GUI réactif type Flutter / SwiftUI
- Optimisation VM et bytecode
- Extensions multi-langage et interop

===============================================
Fin de la documentation Fluxia v2.0
===============================================
