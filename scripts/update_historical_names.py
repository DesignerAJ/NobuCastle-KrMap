import json

# 추가된 이름 변경 정보 및 좌표 데이터
# 'ko', 'ja', 'region'은 매칭용, 'current_name'은 변경된 이름, 'coords'는 좌표
additional_historical_data = [
    {"target_ja": "利府城", "current_name": "다테야마 공원 (館山公園)", "lat": 38.330833, "lng": 140.975556},
    {"target_ja": "湊城", "current_name": "쓰치자키 신메이사 (土崎神明社)", "lat": 39.756667, "lng": 140.068333},
    {"target_ja": "太田城", "current_name": "히타치오타 시청 부근 (사타케성)", "lat": 36.545833, "lng": 140.523333},
    {"target_ja": "府中城", "current_name": "이시요카 시청 부근 (이시요카성)", "lat": 36.191111, "lng": 140.2875},
    {"target_ja": "新発田城", "current_name": "아야메성 (菖蒲城)", "lat": 37.947917, "lng": 139.327278},
    {"target_ja": "魚津城", "current_name": "우오즈 시립 다이카이 초등학교 부근", "lat": 36.828611, "lng": 137.388889},
    {"target_ja": "鳴海城", "current_name": "네고야성 (根古屋城)", "lat": 35.081583, "lng": 136.950361},
    {"target_ja": "清須城", "current_name": "기요스성 공원", "lat": 35.216583, "lng": 136.843564},
    {"target_ja": "安濃津城", "current_name": "쓰성 (津城)", "lat": 34.717767, "lng": 136.507658},
    {"target_ja": "鶴ヶ城", "current_name": "아이즈와카마쓰성 (会津若松城)", "lat": 37.487778, "lng": 139.929722},
    {"target_ja": "佐和山城", "current_name": "사와야마 성터", "lat": 35.281389, "lng": 136.269444},
    {"target_ja": "二条御所", "current_name": "니조성 (二条城)", "lat": 35.014167, "lng": 135.748056},
    {"target_ja": "伏見城", "current_name": "모모야마성 (桃山城)", "lat": 34.939167, "lng": 135.78},
    {"target_ja": "石山御坊", "current_name": "오사카성 (大阪城) 부지", "lat": 34.687222, "lng": 135.526111},
    {"target_ja": "大阪城", "current_name": "오사카성 (大阪城)", "lat": 34.687222, "lng": 135.526111},
    {"target_ja": "大坂城", "current_name": "오사카성 (大阪城)", "lat": 34.687222, "lng": 135.526111},
    {"target_ja": "竹田城", "current_name": "호와성 (虎臥城)", "lat": 35.300556, "lng": 134.829167},
    {"target_ja": "府内館", "current_name": "후나이 성터 (府内城)", "lat": 33.240556, "lng": 131.611389},
    {"target_ja": "日野江城", "current_name": "히노에 성터", "lat": 32.660278, "lng": 130.252778},
    {"target_ja": "岸和田城", "current_name": "치키리성 (千亀利城)", "lat": 34.459167, "lng": 135.370556},
    {"target_ja": "角館城", "current_name": "가쿠노다테 무사 저택 거리 부근", "lat": 39.599167, "lng": 140.560833},
    {"target_ja": "指月城", "current_name": "하기성 (萩城)", "lat": 34.417778, "lng": 131.385556},
    {"target_ja": "天霧城", "current_name": "아마기리 성터", "lat": 34.235556, "lng": 133.735278},
    {"target_ja": "熊本城", "current_name": "긴조 (銀杏城)", "lat": 32.806111, "lng": 130.705833}
]

def main():
    json_path = r'e:\AJ\02_Coding\02_Personal Project\NubuCastleMap\castles.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        castles = json.load(f)

    updated_count = 0
    for castle in castles:
        ja_names_field = castle.get("성 이름 (일본어)", "")
        ja_names_list = [n.strip() for n in ja_names_field.replace('\n', '/').split('/') if n.strip()]
        
        found_data = None
        for target_ja in ja_names_list:
            for item in additional_historical_data:
                if target_ja == item['target_ja']:
                    found_data = item
                    break
            if found_data: break
            
        if found_data:
            # 좌표 추가
            if "좌표" not in castle:
                castle["좌표"] = {"lat": found_data['lat'], "lng": found_data['lng']}
            
            # 변경된 이름/현재 이름 항목 추가
            castle["현재 명칭"] = found_data['current_name']
            updated_count += 1

    print(f"Updated {updated_count} castles with historical/current names and coordinates.")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(castles, f, ensure_ascii=False, indent=2)
    print("Saved updated castles.json")

if __name__ == "__main__":
    main()
