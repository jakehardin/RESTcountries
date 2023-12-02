import asyncio
import csv
import aiohttp

async def fetch_country_data(session, code):
    """Fetch country data from the RESTCountries API for a given country code."""
    url = f'https://restcountries.com/v3.1/alpha/{code}'
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_countries(session, country_codes):
    """Fetch data for multiple countries asynchronously using aiohttp."""
    tasks = [fetch_country_data(session, code) for code in country_codes]
    return await asyncio.gather(*tasks)

async def write_to_csv(filename, data):
    """Write country data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'capital', 'currency', 'alt_spellings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for country_info_list in data:
            if isinstance(country_info_list, list) and country_info_list:
                country_info = country_info_list[0]
                currency_info = country_info.get('currencies', {})
                currency_code = next(iter(currency_info), None)  # Get the first currency code
                currency_name = currency_info.get(currency_code, {}).get('name', '')

                writer.writerow({
                    'name': country_info.get('name', {}).get('common', ''),
                    'capital': ', '.join(country_info.get('capital', [])),
                    'currency': currency_name,
                    'alt_spellings': ', '.join(country_info.get('altSpellings', [])),
                })
            else:
                print(f"Unexpected data structure for country: {country_info_list}")

async def main():
    """Main function to orchestrate the asynchronous tasks."""
    country_codes = ['USA', 'CAN', 'DEU']  # Add more countries as needed

    async with aiohttp.ClientSession() as session:
        country_data = await fetch_all_countries(session, country_codes)

    # Print data before writing to CSV
    for country_info_list in country_data:
        if country_info_list:
            country_info = country_info_list[0]
            currency_info = country_info.get('currencies', {})
            currency_code = next(iter(currency_info), None)  # Get the first currency code
            currency_name = currency_info.get(currency_code, {}).get('name', '')

            print({
                'name': country_info.get('name', {}).get('common', ''),
                'capital': ', '.join(country_info.get('capital', [])),
                'currency': currency_name,
                'alt_spellings': ', '.join(country_info.get('altSpellings', [])),
            })

    await write_to_csv('countries.csv', country_data)

if __name__ == '__main__':
    asyncio.run(main())
