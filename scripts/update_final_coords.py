import json

# 최종 22개 성에 대한 조사 결과
final_batch_details = [
    {"ko": "요네자와성", "ja": "米沢城", "current_name": "마쓰가사키 공원 (우에스기 신사)", "lat": 37.908611, "lng": 140.104444},
    {"ko": "오다성 / 시모쓰마성", "ja": "小田城\n下妻城", "current_name": "오다 성터 역사광장 / 다카야 성터 공원", "lat": 36.150556, "lng": 140.110833},
    {"ko": "만기성 / 오오키타성", "ja": "万喜城\n大喜多城", "current_name": "만기 성터 /大多喜城 (오오타키성)", "lat": 35.297222, "lng": 140.326667},
    {"ko": "니라야마성", "ja": "韮山城", "current_name": "니라야마 성터", "lat": 35.053611, "lng": 138.955556},
    {"ko": "마쓰나미성", "ja": "松波城", "current_name": "마쓰나미 성터 공원", "lat": 37.355833, "lng": 137.239444},
    {"ko": "아사쿠라야마성", "ja": "朝倉山城", "current_name": "아사쿠라야마 성터 (fukui)", "lat": 36.001667, "lng": 136.261111},
    {"ko": "나고야성", "ja": "那古野城", "current_name": "나고야성 니노마루 부근 (구 성터)", "lat": 35.184722, "lng": 136.8925},
    {"ko": "오키시오성", "ja": "置塩城", "current_name": "오키시오 성터", "lat": 34.9225, "lng": 134.681111},
    {"ko": "코노스미성", "ja": "此隅城", "current_name": "코노스미야마 성터", "lat": 35.487778, "lng": 134.872778},
    {"ko": "미토야성", "ja": "三刀屋城", "current_name": "미토야 성터 공원", "lat": 35.293611, "lng": 132.872222},
    {"ko": "야마부키성", "ja": "山吹城", "current_name": "야마부키 성터 (이와미 은광 부근)", "lat": 35.104167, "lng": 132.430833},
    {"ko": "요시다코오리야마성", "ja": "吉田郡山城", "current_name": "요시다 코오리야마 성터", "lat": 34.674167, "lng": 132.709444},
    {"ko": "사쿠라오성", "ja": "桜尾城", "current_name": "사쿠라오 성터 (가이진샤 부근)", "lat": 34.357222, "lng": 132.3425},
    {"ko": "스오타카모리성", "ja": "周防高森城", "current_name": "다카모리 성터", "lat": 34.208, "lng": 132.116944},
    {"ko": "야마구치관", "ja": "山口館", "current_name": "오우치씨 관터 (료운사)", "lat": 34.185278, "lng": 131.482778},
    {"ko": "쿠시자키성", "ja": "櫛崎城", "current_name": "쿠시자키 성터 (조후 공원)", "lat": 33.989444, "lng": 130.993889},
    {"ko": "하쿠치성", "ja": "白地城", "current_name": "하쿠치 성터 (아와노쇼 부근)", "lat": 34.015556, "lng": 133.781111},
    {"ko": "모토야마성", "ja": "本山城", "current_name": "모토야마 성터", "lat": 33.754444, "lng": 133.586667},
    {"ko": "아카타성", "ja": "縣城", "current_name": "노베오카 성터 (내야마 공원)", "lat": 32.582222, "lng": 131.664722},
    {"ko": "쿠마모토성", "ja": "隈本城", "current_name": "구마모토성 고시로 (구 성터)", "lat": 32.806389, "lng": 130.701111},
    {"ko": "히노에성", "ja": "日之江城", "current_name": "히노에 성터", "lat": 32.660278, "lng": 130.252778},
    {"ko": "이즈미성", "ja": "出水城", "current_name": "이즈미 성터 (가메가조)", "lat": 32.071111, "lng": 130.362222}
]

def main():
    json_path = r'e:\AJ\02_Coding\02_Personal Project\NubuCastleMap\castles.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        castles = json.load(f)

    updated_count = 0
    for castle in castles:
        if "좌표" in castle: continue
        
        ko_name = castle.get("성 이름 (한국어)", "")
        ja_names_field = castle.get("성 이름 (일본어)", "")
        
        found_item = None
        for item in final_batch_details:
            if item["ko"] == ko_name or item["ja"] == ja_names_field:
                found_item = item
                break
        
        if found_item:
            castle["좌표"] = {"lat": found_item["lat"], "lng": found_item["lng"]}
            castle["현재 명칭"] = found_item["current_name"]
            updated_count += 1

    print(f"Final update: {updated_count} castles updated.")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(castles, f, ensure_ascii=False, indent=2)
    print("All coordinates have been processed.")

if __name__ == "__main__":
    main()
