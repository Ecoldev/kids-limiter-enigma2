![CI](https://github.com/Ecoldev/kids-limiter-enigma2/actions/workflows/main.yml/badge.svg)

# KidsLimiter (Enigma2 Plugin)

**Status:** v0.1 – stable core (MVP)

KidsLimiter to plugin kontroli rodzicielskiej dla Enigma2, który ogranicza dzienny czas oglądania kanałów dziecięcych.

---

## Funkcje (v0.1)

* Limit dzienny oglądania (domyślnie: 1200 sekund / 20 minut)
* Wykrywanie kanałów dziecięcych:

  * po Service Reference
  * po nazwie kanału
* Blokada dotyczy tylko kanałów dziecięcych (inne kanały działają normalnie)
* Zapisywanie czasu do pliku (`/etc/enigma2/kids_time.json`)
* Automatyczny reset każdego dnia (startup + runtime, obsługa północy)
* Twarda blokada po osiągnięciu limitu (wymuszone przełączenie kanału)
* Komunikat po osiągnięciu limitu

---

## Jak to działa

1. Plugin nasłuchuje zmiany kanału (`ServiceEventTracker`)
2. Co 2 sekundy:

   * sprawdza aktualny kanał
   * jeśli to kanał dziecięcy → zwiększa licznik
3. Po osiągnięciu limitu:

   * pokazuje komunikat
   * wymusza zmianę kanału (np. TVP1)
4. Kanały inne niż dziecięce nigdy nie są blokowane

---

## Instalacja

Skopiuj plugin do:

```
/usr/lib/enigma2/python/Plugins/Extensions/KidsLimiter
```

Restart Enigma2:

```bash
killall -9 enigma2  
enigma2
```

---

## Konfiguracja

Edytuj w kodzie:

```python
LIMIT = 1200
CHANNEL_TO_SWITCH = "1:0:1:3ABD:514:13E:820000:0:0:0:"
```

---

## Ograniczenia (v0.1)

* Brak PIN-u
* Liczenie na timerze (nie jest w 100% dokładne)
* Częsty zapis do pliku
* Brak GUI

---

## Plan rozwoju

* v0.2 → PIN dla rodzica
* v0.3 → dokładniejsze liczenie czasu
* v0.4 → GUI w Enigma2

---

## Testy

Projekt zawiera prosty zestaw testów do weryfikacji logiki biznesowej bez potrzeby uruchamiania środowiska Enigma2.

### Zakres

Testy obejmują:

* normalizację formatu czasu (`time` → `time_seconds`)
* kompatybilność wsteczną ze starym formatem JSON
* obsługę uszkodzonego lub niepoprawnego JSON
* obsługę braku pliku z danymi
* logikę dziennego resetu
* migrację danych (stary → nowy format)

### Jak to działa

Testy znajdują się w pliku `test_time.py` i wykorzystują mocki modułów Enigma2.

### Uruchamianie testów lokalnie

```bash
python3 test_time.py
```

### Integracja z CI

Projekt wykorzystuje GitHub Actions do automatycznej walidacji kodu.

Pipeline uruchamia się przy każdym:

* pushu do repozytorium
* pull requeście do gałęzi `main`

CI wykonuje:

* sprawdzenie składni plików Python
* analizę jakości kodu (flake8)
* uruchomienie testów (`test_time.py`)
* weryfikację struktury projektu
* sprawdzenie obecności README
* walidację formatu JSON

Środowisko:

* Python 3.10
* Ubuntu (GitHub runner)

Konfiguracja workflow:

```
.github/workflows/main.yml
```

### Uwagi

* Testy nie obejmują działania w środowisku Enigma2
* Zachowanie pluginu należy przetestować na urządzeniu

---

# KidsLimiter (Enigma2 Plugin) - English version

**Status:** v0.1 – stable core (MVP)

KidsLimiter is a parental control plugin for Enigma2 that limits daily viewing time for children's TV channels.

---

## Features (v0.1)

* Daily viewing time limit (default: 1200 seconds / 20 minutes)
* Detection of children's channels:

  * by Service Reference
  * by channel name
* Blocking applies only to children's channels (other channels remain accessible)
* Persistent storage (`/etc/enigma2/kids_time.json`)
* Automatic daily reset (startup + runtime, handles midnight rollover)
* Hard block after reaching the limit (forced channel switch)
* Popup notification when limit is reached

---

## How it works

1. The plugin listens for channel changes using `ServiceEventTracker`
2. Every 2 seconds:

   * checks current channel
   * if it's a kids channel → increments time
3. When limit is reached:

   * shows popup
   * forces switch to predefined channel (e.g. TVP1)
4. Non-kids channels are never blocked

---

## Installation

Copy plugin to:

```
/usr/lib/enigma2/python/Plugins/Extensions/KidsLimiter
```

Restart Enigma2:

```bash
killall -9 enigma2  
enigma2
```

---

## Configuration

```python
LIMIT = 1200
CHANNEL_TO_SWITCH = "1:0:1:3ABD:514:13E:820000:0:0:0:"
```

---

## Limitations (v0.1)

* No PIN protection
* Timer-based counting (not perfectly accurate)
* Frequent disk writes
* No GUI

---

## Roadmap

* v0.2 → PIN protection
* v0.3 → accurate time tracking
* v0.4 → GUI configuration

---

## Testing

The project includes a lightweight test setup to validate core logic without requiring the Enigma2 runtime.

### Scope

Tests cover:

* time format normalization (`time` → `time_seconds`)
* backward compatibility with legacy JSON
* corrupted data handling
* missing file handling
* daily reset logic
* migration from legacy format

### Running tests

```bash
python3 test_time.py
```

### CI

Tests are executed automatically via GitHub Actions on push and pull requests.

### Notes

* Runtime behavior must be validated on actual device
* Enigma2 environment is mocked in tests

---

## Community / Społeczność

Projekt stosuje standardowe praktyki open-source.

* CONTRIBUTING.md
* CODE_OF_CONDUCT.md
* SECURITY.md

---

## License

MIT
