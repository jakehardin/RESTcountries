import asyncio
import csv
import aiohttp

async def fetch_country_data(session, code):
    url = f'https://restcountries.com/v3.1/alpha/{code}'
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_countries(session, country_codes):
    tasks = [fetch_country_data(session, code) for code in country_codes]
    return await asyncio.gather(*tasks)

async def write_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'capital', 'currency', 'alt_spellings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for country_info_list in data:
            if isinstance(country_info_list, list) and country_info_list:
                country_info = country_info_list[0]
                writer.writerow({
                    'name': country_info.get('name', {}).get('common', ''),
                    'capital': ', '.join(country_info.get('capital', [])),
                    'currency': country_info.get('currencies', {}).get('USD', {}).get('name', ''),
                    'alt_spellings': ', '.join(country_info.get('altSpellings', [])),
                })
            else:
                print(f"Unexpected data structure for country: {country_info_list}")

async def main():
    country_codes = ['USA', 'GBR', 'AUS']

    async with aiohttp.ClientSession() as session:
        country_data = await fetch_all_countries(session, country_codes)

    # Print the entire JSON response for the USA
    # print(country_data)

    # Print data before writing to CSV
    for country_info_list in country_data:
        if country_info_list:
            country_info = country_info_list[0]
            print({
                'name': country_info.get('name', {}).get('common', ''),
                'capital': ', '.join(country_info.get('capital', [])),
                'currency': country_info.get('currencies', {}).get('USD', {}).get('name', ''),
                'alt_spellings': ', '.join(country_info.get('altSpellings', [])),
            })

    await write_to_csv('countries.csv', country_data)

if __name__ == '__main__':
    asyncio.run(main())
