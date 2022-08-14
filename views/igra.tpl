% rebase('base.tpl')

<h1>KVIZ</h1>


<p>Vaš rezultat je: {{igra.pravilni}}</p>

<p>VPRAŠANJE: {{igra.vprasanja[igra.stevilka_vprasanja].tekst}}</p>

<p>Možni odgovori so: (Klikni na tistega, za katerega meniš, da je pravilen)</p>

<form action="/igra/{{igra.id_igre}}" method="post">

<button type="submit" name="0">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[0]}}</button>


<button type="submit" name="1">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[1]}}</button>


<button type="submit" name="2">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[2]}}</button>


<button type="submit" name="3">{{igra.vprasanja[igra.stevilka_vprasanja].odgovori[3]}}</button>

</form>

%end