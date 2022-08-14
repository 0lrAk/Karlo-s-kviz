% rebase('base.tpl')

<h1>KVIZ</h1>


<p>Vaš rezultat je: {{igra.pravilni}}</p>

<h3>VPRAŠANJE: {{igra.vprasanja[igra.stevilka_vprasanja].tekst}}</h3>

<p>Možni odgovori so: (Klikni na tistega, za katerega meniš, da je pravilen)</p>

<form action="/igra/{{igra.id_igre}}" method="post">

<button type="submit" name="0">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[0]}}</button><br>


<button type="submit" name="1">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[1]}}</button><br>


<button type="submit" name="2">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[2]}}</button><br>


<button type="submit" name="3">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[3]}}</button><br>

</form>

%end