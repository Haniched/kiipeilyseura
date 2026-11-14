# Kiipeilyseura

Kiipeilyseura on kiipeilijoille tarkoitettu reittifoorumi. Sovelluksessa käyttäjät jakavat tietoa kiipeilyreiteistä ja -paikoista sekä vinkkejä niiden kiipeämiseen.

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan reittejä. Reitillä on nimi, paikka (esim. kiipeilyhalli tai kallio), kuvaus ja vaikeusaste.
- Käyttäjä näkee sovellukseen lisätyt reitit.
- Käyttäjä pystyy etsimään reittejä hakusanalla sekä kiipeilytyypin tai paikan perusteella.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja (esim. lisättyjen reittien määrä ja yleisin kiipeilytyyppi) sekä käyttäjän lisäämät reitit.
- Käyttäjä pystyy valitsemaan reitille yhden tai useamman luokittelun (kiipeilytyyppi, esim. boulderointi, köysikiipeily, trad). Mahdolliset luokat ovat tietokannassa.
- Käyttäjä pystyy lähettämään toisen käyttäjän lisäämään reittiin liittyviä lisätietoja (esim. vinkkejä, kokemuksia ja arvioita reitistä), jotka näkyvät reitin sivulla.

### Suunnitteilla

- Kiipeilyn lokikirja: käyttäjä pystyy kirjaamaan omia kiipeilysuorituksiaan (reitti, päivämäärä, vaikeusaste, muistiinpanot), ja suoritukset näkyvät käyttäjäsivun tilastoissa.

## Sovelluksen testaaminen

Sovellus vaatii Pythonin (3.10 tai uudempi) ja Flaskin.

1. Kloonaa repositorio ja siirry sen kansioon:

   ```
   git clone https://github.com/Haniched/kiipeilyseura.git
   cd kiipeilyseura
   ```

2. Luo virtuaaliympäristö ja asenna Flask:

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install flask
   ```

   Windowsissa virtuaaliympäristö aktivoidaan komennolla `venv\Scripts\activate`.

3. Luo tiedosto `config.py` ja lisää siihen salainen avain:

   ```python
   secret_key = "vaihda-tama-johonkin-satunnaiseen"
   ```

4. Luo tietokanta `schema.sql`-tiedoston pohjalta. Jos sovellus käyttää alkutietoja (esim. kiipeilytyypit), lisää myös ne:

   ```
   sqlite3 database.db < schema.sql
   sqlite3 database.db < init.sql
   ```

5. Käynnistä sovellus:

   ```
   flask run
   ```

6. Avaa selaimessa osoite `http://127.0.0.1:5000`.

### Testausohje

1. Luo uusi tunnus sivulla *Luo tunnus* ja kirjaudu sisään.
2. Lisää uusi reitti ja valitse sille yksi tai useampi kiipeilytyyppi.
3. Muokkaa reittiä ja poista se.
4. Kirjaudu toisella tunnuksella ja lisää reittiin lisätietoja.
5. Kokeile hakua hakusanalla ja kiipeilytyypin mukaan.
6. Avaa käyttäjäsivu ja tarkista tilastot sekä käyttäjän lisäämät reitit.
