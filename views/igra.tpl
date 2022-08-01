% rebase('base.tpl')

<h1>KVIZ</h1>

%novo_vprasanje()
<p>Vaš rezultat je: {{igra.rezultat()}}</p>

<p>VPRAŠANJE: {{igra.vprasanje()}}</p>

<p>Možni odgovori so: (Klikni na tistega, za katerega meniš, da je pravilen)</p>


<button type="submit">{{igra.odgovorA}}</button>
%if {{igra.resitev() == 1}}
{{novo_vprasanje()}}
%else
<p>Vaš odgovor je žal napačen. Pravilen odgovor je bil {{igra.resitev()}}</p>

<button type="submit">{{igra.odgovorB}}</button>
%if {{igra.resitev() == 2}}
{{novo_vprasanje()}}
%else
<p>Vaš odgovor je žal napačen. Pravilen odgovor je bil {{igra.resitev()}}</p>

<button type="submit">{{igra.odgovorC}}</button>
%if {{igra.resitev()== 3}}
{{novo_vprasanje()}}
%else
<p>Vaš odgovor je žal napačen. Pravilen odgovor je bil {{igra.resitev()}}</p>

<button type="submit">{{igra.odgovorD}}</button>
%if {{igra.resitev()== 4}}
{{novo_vprasanje()}}
%else
<p>Vaš odgovor je žal napačen. Pravilen odgovor je bil {{igra.resitev()}}</p>

%if igra.zmaga():
<h1>ČESTITKE, PRAVILNO STE ODGOVORILI NA VSEH 24 VPRAŠANJ!</h1>

<p>Število pravilno odgovorjeni vprašanj: {{igra.rezultat()}}</p>

%end
