import json
import re
import requests
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import unquote
import time

def fetch_all_castle_data():
    all_entries = []
    start_index = 1
    max_results = 150
    
    while True:
        url = f"https://www.japancastle.jp/feeds/posts/default?max-results={max_results}&start-index={start_index}"
        print(f"Fetching {url}...")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch feed: {response.status_code}")
                break
        except Exception as e:
            print(f"Request failed: {e}")
            break

        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'openSearch': 'http://a9.com/-/spec/opensearchrss/1.0/'}
        
        entries = root.findall('atom:entry', ns)
        if not entries:
            break
            
        for entry in entries:
            title = entry.find('atom:title', ns).text or ""
            content_elem = entry.find('atom:content', ns)
            content_html = content_elem.text if content_elem is not None and content_elem.text else ""
            content = unescape(content_html)
            content_decoded = unquote(content)
            
            combined_text = title + content_decoded
            
            coords = None
            # Location: lat, lng
            loc_match = re.search(r'Location:\s*([0-9.-]+),\s*([0-9.-]+)', content)
            # @lat,lng
            map_match_at = re.search(r'@([0-9.-]+),\s*([0-9.-]+)', content)
            # q=lat,lng or q=Label@lat,lng
            map_match_q = re.search(r'q=([0-9.-]+),\s*([0-9.-]+)', content)
            if not map_match_q:
                map_match_q = re.search(r'@([0-9.-]+),\s*([0-9.-]+)', content) # Retry common @ format

            if loc_match:
                coords = {"lat": float(loc_match.group(1)), "lng": float(loc_match.group(2))}
            elif map_match_at:
                coords = {"lat": float(map_match_at.group(1)), "lng": float(map_match_at.group(2))}
            elif map_match_q:
                coords = {"lat": float(map_match_q.group(1)), "lng": float(map_match_q.group(2))}

            all_entries.append({
                "title": title,
                "content": combined_text,
                "coords": coords
            })
        
        total_results_elem = root.find('openSearch:totalResults', ns)
        if total_results_elem is not None:
            total_results = int(total_results_elem.text)
            if start_index + len(entries) > total_results:
                break
        else:
            break
            
        start_index += len(entries)
        time.sleep(0.5)
        
    return all_entries

def main():
    print("Fetching data from japancastle.jp...")
    site_data = fetch_all_castle_data()
    print(f"Total entries collected: {len(site_data)}")

    json_path = r'e:\AJ\02_Coding\02_Personal Project\NubuCastleMap\castles.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        castles = json.load(f)

    updated_count = 0
    for castle in castles:
        ja_name_field = castle.get("성 이름 (일본어)", "")
        ja_names_to_search = [name.strip() for name in ja_name_field.split('\n') if name.strip()]
        
        found_coords = None
        for target_ja in ja_names_to_search:
            clean_ja = re.sub(r'\(.*?\)', '', target_ja).strip()
            if not clean_ja: continue
            
            for entry in site_data:
                # Match if the Japanese name appears anywhere in title or decoded content
                if clean_ja in entry['title'] or clean_ja in entry['content']:
                    if entry['coords']:
                        found_coords = entry['coords']
                        break
            if found_coords:
                break
        
        if found_coords:
            castle["좌표"] = found_coords
            updated_count += 1

    print(f"Updated {updated_count} out of {len(castles)} castles.")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(castles, f, ensure_ascii=False, indent=2)
    print("Saved updated castles.json")

if __name__ == "__main__":
    main()
