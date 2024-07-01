Aplikacja Czatowa z Transferem Plików
Repozytorium zawiera prostą aplikację czatową typu klient-serwer napisaną w Pythonie, wykorzystującą gniazdka (sockets). Aplikacja umożliwia podstawowe funkcje czatowania oraz bezpieczny transfer plików z weryfikacją sumy kontrolnej MD5.

Funkcje
Czat: Klienci mogą wysyłać i odbierać wiadomości tekstowe w pokoju czatowym.
Transfer Plików: Klienci mogą wysyłać pliki na serwer oraz pobierać pliki od innych klientów.
Suma Kontrolna MD5: Pliki są weryfikowane przy użyciu sumy kontrolnej MD5, aby zapewnić integralność danych.
Komponenty
Serwer (server.py):

Nasłuchuje na przychodzące połączenia od klientów.
Zarządza wiadomościami czatowymi pomiędzy klientami.
Obsługuje transfer plików, przechowując odebrane pliki i weryfikując integralność za pomocą MD5.
Klient (client.py):

Łączy się z serwerem po uruchomieniu.
Pozwala użytkownikowi podać pseudonim i uczestniczyć w czacie.
Obsługuje wysyłanie wiadomości tekstowych, żądanie plików (/getfile nazwapliku) oraz wysyłanie plików (/sendfile ścieżkadoPliku).
Użycie
Serwer:

Uruchom plik server.py, aby rozpocząć działanie serwera.
Serwer nasłuchuje na adresie HOST i porcie PORT, które są określone w skrypcie (domyślnie 127.0.0.1:12346).
Serwer przechowuje odebrane pliki w katalogu server_files.
Klient:

Uruchom plik client.py, aby uruchomić instancję klienta.
Podaj pseudonim użytkownika po zapytaniu.
Rozpocznij wysyłanie wiadomości w czacie lub rozpocznij transfer plików za pomocą poleceń (/sendfile i /getfile).
Wymagania
Python 3.x
hashlib (biblioteka standardowa)
socket (biblioteka standardowa)
threading (biblioteka standardowa)
os (biblioteka standardowa)
Uwagi
Upewnij się, że serwer i klient działają w tej samej sieci lub lokalnie (127.0.0.1).
Transfer plików używa podstawowego zarządzania błędami i weryfikacji poprzez sumy kontrolne MD5.
Aplikacja ta jest przeznaczona do celów edukacyjnych i może wymagać dodatkowych środków bezpieczeństwa do użycia w środowiskach produkcyjnych.
