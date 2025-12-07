# classification_pymetrics
## Zadání:
> Představ si modelovou situaci, kde nám výzkumný stážista vytvořil tenhle kousek "kódu" a chtěli bychom, abys mu na něj udělal velmi stručné review kritických nedostatků a následně zrefaktoroval kód do instalovatelného python balíčku produkční kvality.

## Hodnocení skriptu
### Obecně k project managementu při vývoji software (i pokud by se nejednalo o Python balíček)
- I menší projekty je dobré verzovat a jasně oddělit, co je zdroják, co vstup a co výstup.
  - Běžně se používá Git repozitory s `.gitignore` souborem.
  - Vstupy a výstupy nemají být verzované, pokud nejde o příklady použití.
- Pro lepší použitelnost pro další uživatele je nutné, aby bylo definované prostředí, ve kterém se software má pouštět (závislosti a verze Pythonu).
- Je hezké mít kód sformátovaný automatickým nástrojem - kód je přehlednější, sjednocený a lépe se čte i např. na příkazové řádce. Vhodný je např. nástroj `black`.
- Název skriptu `main.py` je velmi generický a neodpovídá funkci skriptu. Vhodnější by bylo použít něco jako `metrics_for_binary_classification.py`. Název může být i kratší kvůli praktickému používání na příkazové řádce, ale alespoň základně výstižný.
- Chybí testy. V tomto případě by navíc jednoduché jednotkové testy odhalily několik zásadních vad ve funkčnosti kódu.
```sh
conda create -n rai_hw python=3.13
conda activate rai_hw
pip install -r requirements.txt
```

### Poznámky ke struktuře skriptu a k jeho dokumentaci
- Pokud se počítá s tím, že skript bude použit z příkazové řádky, je vhodné zadávat vstupní a výstupní soubory jako argumenty a nemít je napevno zapsané ve skriptu. Pro použití skriptu jako balíčku jde o nutnost.
- Bylo by mnohem vhodnější předávat funkcím hodnoty pomocí argumentů a výsledek získávat pomocí návratové hodnoty namísto globálních proměnných.
- Je dobré si vybrat jeden styl komentářů a ten pak používat - např. sjednotit:
```py
# === BASIC METRICS ===
""" other metrics """
```
- I kvůli použití globálních proměnných názvů vstupních souborů ve funkcích jsou v kódu dvě téměř identické funkce - `_load_preds` a `_load_labels`. Toto bych určitě změnil na jednu funkci se vstupním argumentem.
- Pokud bychom chtěli získat alespoň základní znovupoužitelnost funkcí ve skriptu a někdy tyto funkce znovu nahrávat, je potřeba všechen kód, který by byl např. v Javě v metodě `main` dát do bloku s `if __name__ == "__main__":` - při importu funkcí ze skriptu by se jinak spustila i celá analýza dat.

### Poznámky k funkčnosti skriptu
- Při prvním spuštění skriptu na příkladech program selhal za běhu (KeyError při načítání sloupce s preds_df, řádek 67 (byla reference na 67 meme záměrná? :D). Stejně by kód selhal i na následujícím řádku.).
  - Problémem je, že v příkladových CSV souborech je použit středník jako separátor namísto defaultní čárky (`,`).
  - Sice středník není přímo vhodný k použití, ale pokud bychom ho opravdu chtěli používat, pak by měl být středník uvedený jako volitelný argument skriptu.
  - V globální proměnné `PRED_COL` je hodnota `y_pred`, ale kvůli středníkům je v DataFramu jako header hodnota `y_pred;;;;;;`

- S tím souvisí, že nejčastější typ chyb by měl být ošetřen speciálními chybovými hláškami, aby měl uživatel možnost problém vidět ihned, nebo tyto případy ošetřit try blokem ve svém vlastním kódu.
  - V tomto skriptu s jednoduchou funkcionalitou bych nechal defaultní chybovou hlášku Pandasu - `KeyError`.
- Skript vrací nesprávné výstupy a to kvůli chybnému použití multiprocessingu.
  - Nyní je to tak, že každý worker načte celý soubor dat a vloží jej načtený do proměnné `global_preds_chunks`/`global_labels_chunks`. Tím získáme 4x načtené identické DataFramy, které jsou následně spojené do jednoho. Na metriky, které jsou závislé na poměrech hodnot z confusion matrix to nemá vliv, ale všechny metriky v absolutích číslech (#TP, #TN, ..., `num_samples` a `num_correct`) jsou čtyřnásobky skutečných hodnot.
- V případě, že je opravdu nutné načítat vstupní soubory paralelizovaně, je potřeba zajistit, aby každé vlákno četlo jen část dat. Nicméně vzhledem k tomu, že R/W operace na souboru jsou omezené na přístup jednoho CPU v danou chvíli nám tento přístup nepomůže, pokud vstupní soubor není předem rozdělen na více částí/souborů. V případě zpracování takto jednoduchého CSV filu bude hrát větší roli overhead z multiprocessingu než výhoda skrze paralelizované čtení.
- Dalším zásadním problémem je špatná definice výpočtu accuracy. Dělitel je dvojnásobný oproti správnému výpočtu. Navíc, pokud ostatní metriky stejně používáme z sklearn, pak dává i accuracy použít z této knihovny - předejde se takto nešikovným chybám.
- Nikde se nekontroluje, že data, která dostáváme k sobě patří (řádek k řádku). Toto se sice nechává na uživateli, nicméně i tak by bylo vhodné alespoň zkontrolovat, že počet výsledků z preds a labels je stejný.

## Přepracovaný balíček
### Struktura kódu
- Jednotlivé funkcionality jsou rozdělené do příslušných souborů. Zdrojový kód je ve složce `src`
  - `cli.py` - zajišťuje práci s balíčkem z příkazové řádky
  - `io.py` - načítání souborů
  - `metrics.py` - výpočty výstupních metrik. Také obsahuje dataclass třídu pro snazší/objektově orientovanou práci s výstupy.
  - `exceptions.py` - výjimka pro náš balíček
  - `__init__.py` - nezbytnost pro vytvoření balíčku

### Instalace

### Příklad použití
Při použití z CLI