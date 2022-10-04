# Forbes-web-scraping
Place to store my work on web scraping task

04.10.2022
[PL]
Spis przesłanych plików wraz z krótkim opisem do czego słuzyły oraz jakie problemy rozwązywały, (wg mnie w kolejności od najbardzej kluczowych do tychpobocznych)  Nazwy plików nie opisują odpowiendnio działanie proramu, lecz w przyszłości zostaną zaktualizowane, aby były jasne. 

## Do tego kilka plików będących rezultatem wykonania programu:
- **forbesFixed.csv** - dane ściągnięte ze stron zawierających listy firm nalezacych do diamentów Forbesa w latach 2016-2022. Dane zostały poprawione po wychwyceniu błędów u źródła i zawierają poprawne dane w odpowiednich kolumnach
- **sprawdzam.csv** - dane ściągnięte ze strony ekrs.gov.pl, lista firm nie jest pełna z powodu problemów podczas procesu ich sciągania, zawieraja poprawne dane w odpowiednich kolumnach
- **czlonkowie.csv** - dane ściągnięte ze strony ekrs.gov.pl, zawierają listę członków zarządu firmy, wykorzystane zostaną podczas końcowego etapu łączenia danych z róźnych zestawień

## Programy:
- **headless.py** - zaktualizowana wersja programu, scrapowanie danych dotyczących konkretnej firmy z eKRSu, próba skozystania z: headless mode - strona nie pozwalała na to, user-agent. Poniewaz strona po 30 zapytaniach blokowała czasowo uzytkownika, zawiera mechanizm który na bierząco dopisuje wynik scrapingu do odpowiedniego pliku - zabezpeiczenie przed pojawieniem się błędu. W momencie braku wyniku w wyszukiwaniu podmiotu lub ich większa ilość, nazwa takej firmy jest zapisywana do odpowiedniego pliku tekstowego i jest obsługiwana w inny sposób
- **test.py**, **ekrs.py** - pierwsza wersja sciągania numeru KRS firmy, mająca na celu dokładniejsze wyszukiwanie danych KRS firmy na stronie ekrs, jeśli w nagłówku pojawia się numer KRS, to zostaje on przypisany do firmy, jeśli nie, sterownik przechodzi na stronę krs-online.com.pl i stamtąd go ściąga, (juz wiem ze da się od razu go sciągnąć z krótkiego opisu)
- **test2.py** - wykozystanie wyszukiwania wyników tylko z jedenej strony (np. site:krs-online.com.pl), cel: firma-KRS
- **google.py** - próby uniknięcia wykrycia: user-agent, nieregularne wysyłanie zapytań
- **googleAPI** - wykozystanie biblioteki ecommercetools, jedna z funkcji zwraca w przytępnej formie wyniki wyszukiwań danej frazy z google, jednak nie jest zapewnia niewykrywalności, implementacja srodków zaradczych 
- **gpw.py** - sciągnięcie ze stron gpw i newconnect listy firm obecnych w tych serwisach, pomysł był taki aby porównać te listy z listą firm z forbesa i odnaleźć powtarzące się firmy poniewaz wyszukiwanie na tych stronach jest bardzo dokładne (nieelastyczne)
- **scrapeData** - sciąganie danych firmy ze strony gpw.pl, (w trakcje implementacji do newconnect)

[ENG]
maybe some day
