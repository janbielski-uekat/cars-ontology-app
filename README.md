## Projekt zaliczeniowy - Technologie semantyczne
<i>Jan Bielski, Paweł Krawczyk</i><br>
<i>Informatyka, stopień II, ADZD, sem. 3</i>
<p>To repozytorium zawiera cały projekt zaliczeniowy z przedmiotu technologie semantyczne. Składa się on z aplikacji webowej w django, autorskiej ontologii (plik cars_ont.ttl) oraz Fuseki Servera pełniącego funkcję "triple store".</p>
<p>Aby uruchomić projekt lokalnie (wymaga loklanej instalcji dockera):</p>

```powershell
  git clone https://github.com/janbielski-uekat/cars-ontology-app/
  cd cars-ontology-app
  docker-compose up
```
<p>Aplikacja jest dostępna na porcie 8000 a UI Fuseki Servera na porcie 3030</p>
