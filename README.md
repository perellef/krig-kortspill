# Krig – et kjapt kortspill for den krigerlystne

Du står som general overfor en storskala *krig*. Mot tre andre nasjoner skal du lede hærene din ut i slag i håp om å vinne. Tiden er inne for å bevise at du virkelig er den strategen du har påstått at du er.

### Kom i gang

1. Installer avhengigheter:
```bash
pip install -r requirements.txt
``` 
2. Start spillet!
```bash
python start.py
```

*Tips: Spillet guider deg med visuelle hjelpeeffekter.*


## Spilleregler

*Ta gjerne en kjapp titt på spillet først. Det er ofte enklere å lære slik.*

Krig er et spill der målet er å vinne slag. Hver seier gir ett **seierpoeng**. Spillerne disponerer store hærstyrker, men hver hær kun brukes i ett slag. Spillets dilemma er hvordan styrkene skal fordeles. En knusende seier kan føre til store tap. 

### Spillets gang

1. **Oppsett**: Alle spillere begynner med **3** kort. Resten av kortene utgjør trekkbunken. En spiller velges til å begynne.
2. **Spillets midtfase**:  Spilleren i tur utfører de handlingene vedkommende ønsker. 
Spilleren kan også velge å ikke foreta seg noe. Til slutt trekker spilleren 2 spillekort, men maks slik at vedkommende hae 6 kort på hånden.
3. **Sluttfase**: At trekkbunken er tom markerer spillets sluttfase. Fra og med nå vil spillere som i løpet av turen ikke reduserer antall kort på hånden anses som ferdige. Dette var deres siste runde. Resten av spilleren fortsetter til alle er ferdige.
2. **Ved endt spill**:  Spilleren(e) med flest slagkort vinner. Slag som ligger igjen på bordet telles ikke med.

## Handlinger

I løpet av turen kan du foreta deg følgende handlinger:
 - **Innled slag**: Spill et *slagkort* på **slagmarken** din (foran hånda). Her vil den ligge inntil den er **vunnet**. En spiller kan maksimalt ha 3 pågående slag i slagmarken sin.<br>
 <br>
 ![slagkort](kort/gull.png)
 - **Angrip**, **Forsvar** eller **Forsterk**: Spill
   - et forsvarskort til et eget slag
   - et angrepskort til en motspillers slag
   - et forsterkningskort til et eget eller en motspillers slag
   
   Merk at du kan supplementere med flere kort, men kun hvis valøren er **mindre eller lik** den forrige.<br>
<br>
![forsvarskort](kort/forsvar_8.png)
![angrepskort](kort/angrep_8.png)
![forsterkningskort](kort/forsterkning_4.png)<br>
  - **Erklær seier**: Hvis du har flertall hærstyrker på et slag når turen din begynner, kan du erklære seier. Dette gjør du ved å ta slagkortet og legge den åpen ved siden av spillehånden din. Hærstyrkene som ligger igjen kastes i kastebunken.<br>
  <br>
  *NB*: Du kan kun ta slagkortet ved starten av din tur. Skulle du glemme å ta slagkortet må du vente til neste runde.
  - **Forkast kort**: Du kan forkaste et kort i kastebunken. Kortet er da helt ute av bruk.
