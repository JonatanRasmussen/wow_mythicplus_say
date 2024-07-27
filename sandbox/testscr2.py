import re
from bs4 import BeautifulSoup
from typing import List, Dict

def parse_fight_data(html_content: str) -> List[Dict[str, str]]:
    """Parses HTML content to extract fight data."""
    soup = BeautifulSoup(html_content, 'html.parser')
    fight_entries = soup.find_all('a', class_='wipes-entry')
    fight_data: List[Dict[str, str]] = []

    for entry in fight_entries:
        data = {
            'id': '',
            'outcome': '',
            'duration': ''
        }

        # Extract ID
        class_name = entry.get('class', [])
        id_match = re.search(r'fight-grid-cell-(\d+)-', ' '.join(class_name))
        if id_match:
            data['id'] = id_match.group(1)

        # Extract outcome
        if 'kill' in class_name:
            data['outcome'] = 'kill'
        elif 'wipe' in class_name:
            data['outcome'] = 'wipe'

        # Extract duration
        duration_span = entry.find('span', class_='fight-grid-duration')
        if duration_span:
            data['duration'] = duration_span.text.strip('()')

        fight_data.append(data)

    return fight_data

def read_html_file(file_path: str) -> str:
    """Reads HTML content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return html_content

def main() -> None:
    html_content = read_html_file('test_html3.txt')
    fight_data = parse_fight_data(html_content)

    print("\nFight Data:")
    for data in fight_data:
        print(data)

if __name__ == "__main__":
    main()