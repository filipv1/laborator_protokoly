"""
Testovací skript pro ARES API - načtení dat podle IČO

DOKUMENTACE: https://ares.gov.cz/stranky/vyvojar-info
ENDPOINT: https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}

POUŽITÍ:
    python test_ares_api.py 12345678

Tento skript načte data z ARES API podle zadaného IČO a vypíše JSON strukturu.
"""
import sys
import json
import requests


def fetch_ares_data(ico):
    """
    Načte data z ARES API podle IČO.

    Args:
        ico: IČO firmy (string nebo int)

    Returns:
        dict: JSON data z ARES API nebo None při chybě
    """
    # ARES API endpoint
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"

    print(f"→ Dotazuji ARES API pro IČO: {ico}")
    print(f"→ URL: {url}")
    print()

    try:
        # HTTP GET request
        response = requests.get(url, timeout=10)

        # Zkontroluj HTTP status code
        if response.status_code == 200:
            print(f"✓ Úspěch! HTTP 200 OK")
            return response.json()

        elif response.status_code == 404:
            print(f"⚠ Chyba: IČO {ico} nenalezeno v ARES databázi (HTTP 404)")
            return None

        else:
            print(f"⚠ Chyba: HTTP {response.status_code}")
            print(f"  Odpověď: {response.text[:500]}")
            return None

    except requests.exceptions.Timeout:
        print(f"⚠ Chyba: Timeout (server neodpověděl do 10 sekund)")
        return None

    except requests.exceptions.ConnectionError:
        print(f"⚠ Chyba: Nepodařilo se připojit k ARES serveru")
        return None

    except Exception as e:
        print(f"⚠ Neočekávaná chyba: {e}")
        return None


def print_json_structure(data, indent=0):
    """
    Vypíše strukturu JSON dat (klíče a typy hodnot).

    Args:
        data: JSON data (dict nebo list)
        indent: Úroveň odsazení (pro rekurzivní výpis)
    """
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{prefix}{key}: {{")
                print_json_structure(value, indent + 1)
                print(f"{prefix}}}")
            elif isinstance(value, list):
                print(f"{prefix}{key}: [")
                if value:
                    print_json_structure(value[0], indent + 1)
                    if len(value) > 1:
                        print(f"{prefix}  ... ({len(value)} položek celkem)")
                print(f"{prefix}]")
            else:
                value_type = type(value).__name__
                value_preview = str(value)[:50]
                print(f"{prefix}{key}: {value_type} = {value_preview}")

    elif isinstance(data, list):
        if data:
            print_json_structure(data[0], indent)
            if len(data) > 1:
                print(f"{prefix}... ({len(data)} položek celkem)")


def main():
    """Hlavní funkce"""
    # Získej IČO z argumentů
    if len(sys.argv) < 2:
        print("⚠ Chyba: Nezadal jsi IČO!")
        print()
        print("Použití:")
        print("  python test_ares_api.py <ICO>")
        print()
        print("Příklad:")
        print("  python test_ares_api.py 12345678")
        sys.exit(1)

    ico = sys.argv[1].strip()

    # Validace IČO (musí být 8 číslic)
    if not ico.isdigit() or len(ico) != 8:
        print(f"⚠ Varování: IČO by mělo být 8 číslic, zadal jsi: {ico}")
        print("  Pokračuji dále...")
        print()

    # Načti data z ARES
    data = fetch_ares_data(ico)

    if data is None:
        sys.exit(1)

    # Ulož JSON do souboru
    output_file = f"ares_response_{ico}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print()
    print(f"✓ JSON uložen do souboru: {output_file}")
    print()

    # Vypíš strukturu JSON
    print("=" * 80)
    print("STRUKTURA JSON ODPOVĚDI:")
    print("=" * 80)
    print_json_structure(data)
    print("=" * 80)

    # Vypíš nejdůležitější pole (pokud existují)
    print()
    print("=" * 80)
    print("KLÍČOVÉ ÚDAJE (pokud jsou dostupné):")
    print("=" * 80)

    # Pokus se vytáhnout základní údaje
    if "obchodniJmeno" in data:
        print(f"Obchodní jméno: {data['obchodniJmeno']}")

    if "ico" in data:
        print(f"IČO: {data['ico']}")

    if "sidlo" in data:
        sidlo = data["sidlo"]
        print(f"Sídlo:")
        for key, value in sidlo.items():
            print(f"  {key}: {value}")

    print("=" * 80)
    print()
    print(f"✓ Hotovo! Pro detaily si prohlédni soubor: {output_file}")


if __name__ == "__main__":
    main()
