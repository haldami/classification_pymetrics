# Zadání:
> Představ si modelovou situaci, kde nám výzkumný stážista vytvořil tenhle kousek "kódu" a chtěli bychom, abys mu na něj udělal velmi stručné review kritických nedostatků a následně zrefaktoroval kód do instalovatelného python balíčku produkční kvality.

# Hodnocení skriptu
## Obecně k project managementu při vývoji software (i pokud by se nejednalo o Python balíček)
- I menší projekty je dobré verzovat a jasně oddělit, co je zdroják, co vstup a co výstup.
  - Běžně se používá Git repozitory s `.gitignore` souborem.
  - Vstupy a výstupy nemají být verzované, pokud nejde o příklady použití.
- Pro lepší použitelnost pro další uživatele je nutné, aby bylo definované prostředí, ve kterém se software má pouštět (závislosti a verze Pythonu).
- Je hezké mít kód sformátovaný automatickým nástrojem - kód je přehlednější, sjednocený a lépe se čte i např. na příkazové řádce.


```sh
conda create -n rai_hw python=3.13
conda activate rai_hw
pip install -r requirements.txt
```

## Poznámky k fungování skriptu
- Pokud se počítá s tím, že skript bude použit z příkazové řádky, je vhodné zadávat vstupní a výstupní soubory jako argumenty a nemít je napevno zapsané ve skriptu. Pro použití skriptu jako balíčku jde o nutnost.
- 