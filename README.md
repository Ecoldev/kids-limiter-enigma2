KidsLimiter (Enigma2 Plugin)

KidsLimiter to plugin kontroli rodzicielskiej dla Enigma2, który ogranicza dzienny czas oglądania kanałów dziecięcych.


Funkcje (v0.1)

- Limit dzienny oglądania (domyślnie: 20 minut)

- Wykrywanie kanałów dziecięcych:
  - po Service Reference
  - po nazwie kanału

- Zapisywanie czasu do pliku (`/etc/enigma2/kids_time.json`)

- Automatyczny reset każdego dnia

- Twarda blokada po osiągnięciu limitu (wymuszone przełączenie kanału)

- Komunikat po osiągnięciu limitu



Jak to działa

1. Plugin nasłuchuje zmiany kanału (`ServiceEventTracker`)

2. Co 2 sekundy:
   - sprawdza aktualny kanał
   - jeśli to kanał dziecięcy → zwiększa licznik

3. Po osiągnięciu limitu:
   - pokazuje komunikat
   - wymusza zmianę kanału (np. TVP1)



Instalacja

Skopiuj plugin do:

/usr/lib/enigma2/python/Plugins/Extensions/KidsLimiter

Restart Enigma2:

killall -9 enigma2  
enigma2  


Konfiguracja

Edytuj w kodzie:

LIMIT = 1200  
TVP1_REF = „1:0:1:3ABD:514:13E:820000:0:0:0:”



Ograniczenia (v0.1)

- Brak PIN-u  
- Liczenie na timerze (niedokładne)  
- Częsty zapis do pliku  
- Brak GUI  



Plan rozwoju

- v0.2 → PIN dla rodzica  
- v0.3 → dokładniejsze liczenie czasu  
- v0.4 → GUI w Enigma2  



License

MIT 



KidsLimiter (Enigma2 Plugin)

KidsLimiter is a parental control plugin for Enigma2 that limits daily viewing time for children’s TV channels.


Features (v0.1)

- Daily viewing time limit (default: 20 minutes)

- Detection of children’s channels:
  - by Service Reference
  - by channel name

- Persistent storage (`/etc/enigma2/kids_time.json`)

- Automatic daily reset

- Hard block after reaching the limit (forced channel switch)

- Popup notification when limit is reached



How it works

1. The plugin listens for channel changes using `ServiceEventTracker`

2. Every 2 seconds:
   - checks current channel
   - if it’s a kids channel → increments time

3. When limit is reached:
   - shows popup
   - forces switch to predefined channel (e.g. TVP1)


Installation

Copy plugin to:

/usr/lib/enigma2/python/Plugins/Extensions/KidsLimiter

Restart Enigma2:

killall -9 enigma2  
enigma2  


Configuration

Edit in code:

LIMIT = 1200  
TVP1_REF = „1:0:1:3ABD:514:13E:820000:0:0:0:”



Limitations (v0.1)

- No PIN protection  
- Timer-based counting (not perfectly accurate)  
- Frequent disk writes  
- No GUI  


Roadmap

- v0.2 → PIN protection  
- v0.3 → accurate time tracking  
- v0.4 → GUI configuration  



License

MIT
