import json

data_to_update = {
    "大浦城": {"lat": 40.618556, "lng": 140.413306},
    "浪岡城": {"lat": 40.71694, "lng": 140.60444},
    "寺池城": {"lat": 38.6553972, "lng": 141.2816361},
    "相馬中村城": {"lat": 37.79806, "lng": 140.91444},
    "小高城": {"lat": 37.568333, "lng": 140.990556},
    "飯野平城": {"lat": 37.055806, "lng": 140.870889},
    "須賀川城": {"lat": 37.287361, "lng": 140.396778},
    "大宝寺城": {"lat": 38.7287389, "lng": 139.8245528},
    "大田原城": {"lat": 36.8683472, "lng": 140.0345972},
    "結城城": {"lat": 36.3080222, "lng": 139.8859556},
    "古河城": {"lat": 36.1868778, "lng": 139.6954861},
    "森山城": {"lat": 35.834556, "lng": 140.634694},
    "佐倉城": {"lat": 35.7219889, "lng": 140.2167167},
    "椎津城": {"lat": 35.4719611, "lng": 140.0357528},
    "大多喜城": {"lat": 35.2858833, "lng": 140.2393417},
    "久留里城": {"lat": 35.287556, "lng": 140.09000},
    "館山城": {"lat": 34.981556, "lng": 139.855306},
    "唐沢山城": {"lat": 36.3537806, "lng": 139.6008472},
    "新田金山城": {"lat": 36.317778, "lng": 139.377472},
    "沼田城": {"lat": 36.648722, "lng": 139.039028},
    "箕輪城": {"lat": 36.404944, "lng": 138.950972},
    "国峯城": {"lat": 36.222515, "lng": 138.894664},
    "鉢形城": {"lat": 36.1097333, "lng": 139.1959833},
    "河越城": {"lat": 35.9245139, "lng": 139.4915028},
    "岩付城": {"lat": 35.9513472, "lng": 139.7102389},
    "江戸城": {"lat": 35.68345, "lng": 139.75688},
    "小机城": {"lat": 35.5124472, "lng": 139.5937111},
    "玉縄城": {"lat": 35.353444, "lng": 139.51500},
    "津久井城": {"lat": 35.5830000, "lng": 139.2788000},
    "小田原城": {"lat": 35.2510472, "lng": 139.1534417},
    "岩殿城": {"lat": 35.6215861, "lng": 138.9498639},
    "坂戸城": {"lat": 37.059069, "lng": 138.8983917},
    "雑太城": {"lat": 37.975444, "lng": 138.360556},
    "安祥城": {"lat": 34.945309, "lng": 137.098330},
    "鳴海城": {"lat": 35.081583, "lng": 136.950361},
    "名古屋城": {"lat": 35.1855875, "lng": 136.8990919},
    "清須城": {"lat": 35.216583, "lng": 136.843564},
    "安濃津城": {"lat": 34.7177667, "lng": 136.5076583},
    "敦賀城": {"lat": 35.6541806, "lng": 136.0655194},
    "佐和山城": {"lat": 35.279474, "lng": 136.268888},
    "日野城": {"lat": 35.0180025, "lng": 136.2460433},
    "伏見城": {"lat": 34.939501, "lng": 135.77686},
    "高屋城": {"lat": 34.54889, "lng": 135.60961694},
    "大阪城": {"lat": 34.6857, "lng": 135.5222},
    "有岡城": {"lat": 34.7812944, "lng": 135.4208917},
    "花隈城": {"lat": 34.68805861, "lng": 135.18287556},
    "津山城": {"lat": 35.062778, "lng": 134.005},
    "比熊山城": {"lat": 34.81972, "lng": 132.84000},
    "徳島城": {"lat": 34.07519, "lng": 134.55527},
    "天霧城": {"lat": 34.23561, "lng": 133.73540},
    "秋月城": {"lat": 33.465849, "lng": 130.6953805},
    "柳川城": {"lat": 33.160722, "lng": 130.40083},
    "金石城": {"lat": 34.204194, "lng": 129.286111},
    "伊万里城": {"lat": 33.287956, "lng": 129.805791},
    "大村城": {"lat": 32.8971056, "lng": 129.9578833},
    "府内城": {"lat": 33.2406417, "lng": 131.6114333},
    "熊本城": {"lat": 32.806028, "lng": 130.7058972},
    "日野江城": {"lat": 32.6600111, "lng": 130.2527694},
    "加治木城": {"lat": 31.749694, "lng": 130.669306},
}

def main():
    json_path = r'e:\AJ\02_Coding\02_Personal Project\NubuCastleMap\castles.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        castles = json.load(f)

    updated_count = 0
    for castle in castles:
        if "좌표" in castle: continue
        
        ja_name_field = castle.get("성 이름 (일본어)", "")
        ja_names_to_search = [name.strip() for name in ja_name_field.split('\n') if name.strip()]
        
        found_coords = None
        for target_ja in ja_names_to_search:
            # Handle names like "A / B"
            parts = [p.strip() for p in target_ja.split('/')]
            for part in parts:
                if part in data_to_update:
                    found_coords = data_to_update[part]
                    break
            if found_coords: break
            
            if target_ja in data_to_update:
                found_coords = data_to_update[target_ja]
                break
        
        if found_coords:
            castle["좌표"] = found_coords
            updated_count += 1

    print(f"Updated {updated_count} castles using batch data.")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(castles, f, ensure_ascii=False, indent=2)
    print("Saved updated castles.json")

if __name__ == "__main__":
    main()
