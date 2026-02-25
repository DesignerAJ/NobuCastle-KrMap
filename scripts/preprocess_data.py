import json
import re

def translate_region(region_jp):
    mapping = {
        "1東北": "도호쿠",
        "2関東": "칸토",
        "3甲信": "코신",
        "4北陸": "호쿠리쿠",
        "5東海": "토카이",
        "6近畿": "킨키",
        "6畿内": "키나이",
        "7中国": "주고쿠",
        "8四国": "시코쿠",
        "9九州": "규슈"
    }
    return mapping.get(region_jp, region_jp)

def translate_type(type_jp):
    mapping = {
        "平城": "평성",
        "山城": "산성"
    }
    return mapping.get(type_jp, type_jp)

# This is a sample mapping for names found in the file. 
# Since there are many, I'll use a dictionary for those I know and 
# might need to supplement or use a pattern.
# For simplicity in this task, I will provide the script that does the transformation.
# I'll include a more comprehensive mapping or use a general rule.

def get_korean_name(jp_name):
    # This is a simplified mapping. In a real scenario, this would be a larger DB.
    # I will populate this based on the common translations of Nobunaga's Ambition castles.
    name_map = {
        "松前城": "마쓰마에성",
        "大浦城": "오우라성",
        "浪岡城": "나미오카성",
        "三戸城": "산노헤성",
        "九戸城": "구노헤성",
        "高水寺城": "고스이지성",
        "寺池城": "데라이케성",
        "岩出山城": "이와데야마성",
        "利府城": "리후성",
        "丸森城": "마루모리성",
        "白石城": "시로이시성",
        "相馬中村城": "소마나카무라성",
        "小高城": "오다카성",
        "飯野平城": "이이노다이라성",
        "桑折西山城": "고오리니시야마성",
        "二本松城": "니혼마쓰성",
        "三春城": "미하루성",
        "須賀川城": "스카가와성",
        "檜山城": "히야마성",
        "湊城": "미나토성",
        "角館城": "가쿠노다테성",
        "横手城": "요코테성",
        "延沢城": "노베사와성",
        "山形城": "야마가타성",
        "大宝寺城": "다이호지성",
        "米沢城": "요네자와성",
        "黒川城": "쿠로카와성",
        "若松城": "와카마쓰성",
        "津川城": "쓰가와성",
        "大田原城": "오오타와라성",
        "宇都宮城": "우쓰노미야성",
        "烏山城": "가라스야마성",
        "太田城": "오오타성",
        "府中城": "후추성",
        "小田城": "오다성",
        "下妻城": "시모쓰마성",
        "結城城": "유키성",
        "古河御所": "코가고쇼",
        "古河城": "코가성",
        "森山城": "모리야마성",
        "佐倉城": "사쿠라성",
        "椎津城": "시이즈성",
        "万喜城": "만기성",
        "大喜多城": "오오키타성",
        "久留里城": "쿠루리성",
        "館山城": "다테야마성",
        "唐沢山城": "카라사와야마성",
        "新田金山城": "닛타가나야마성",
        "沼田城": "누마타성",
        "箕輪城": "미노와성",
        "国峯城": "쿠니미네성",
        "鉢形城": "하치가타성",
        "忍城": "오시성",
        "河越城": "카와고에성",
        "岩付城": "이와쓰키성",
        "江戸城": "에도성",
        "小机城": "코즈쿠에성",
        "玉縄城": "타마나와성",
        "三崎城": "미사키성",
        "滝山城": "타키야마성",
        "八王子城": "하치오지성",
        "津久井城": "쓰쿠이성",
        "小田原城": "오다와라성",
        "韮山城": "니라야마성",
        "岩殿城": "이와도노성",
        "躑躅ヶ崎館": "쓰쓰지가사키관",
        "甲府城": "고후성",
        "海津城": "카이즈성",
        "葛尾城": "카쓰라오성",
        "砥石城": "토이시성",
        "上田城": "우에다성",
        "小諸城": "코모로성",
        "深志城": "후카시성",
        "松本城": "마쓰모토성",
        "上原城": "우에하라성",
        "高島城": "타카시마성",
        "高遠城": "타카토성",
        "木曽福島城": "키소후쿠시마성",
        "飯田城": "이이다성",
        "松尾城": "마쓰오성",
        "飯山城": "이이야마성",
        "新発田城": "시바타성",
        "栃尾城": "토치오성",
        "蔵王堂城": "자오도성",
        "与板城": "요이타성",
        "北条城": "키타죠성",
        "坂戸城": "사카도성",
        "春日山城": "가스야마성",
        "雑太城": "사와타성",
        "七尾城": "나나오성",
        "松波城": "마쓰나미성",
        "魚津城": "우오즈성",
        "富山城": "도야마성",
        "増山城": "마수야마성",
        "金沢御坊": "카나자와고보",
        "金沢城": "카나자와성",
        "鳥越城": "토리고에성",
        "小松城": "코마쓰성",
        "大聖寺城": "다이쇼지성",
        "朝倉山城": "아사쿠라야마성",
        "一乗谷城": "이치조다니성",
        "北ノ庄城": "기타노쇼성",
        "大野城": "오오노성",
        "帰雲城": "카에루쿠모성",
        "荻町城": "오기마치성",
        "郡上八幡城": "구죠하치만성",
        "桜洞城": "사쿠라하자마성",
        "松倉城": "마쓰쿠라성",
        "興国寺城": "고코쿠지성",
        "蒲原城": "칸바라성",
        "駿府城": "순푸성",
        "掛川城": "카케가와성",
        "曳馬城": "히쿠마성",
        "浜松城": "하마마쓰성",
        "二俣城": "후타마타성",
        "長篠城": "나가시노성",
        "新城城": "신시로성",
        "吉田城": "요시다성",
        "岡崎城": "오카자키성",
        "安祥城": "안죠성",
        "刈谷城": "카리야성",
        "鳴海城": "나루미성",
        "那古野城": "나고야성",
        "清須城": "키요스성",
        "長島城": "나가시마성",
        "桑名城": "쿠와나성",
        "岩村城": "이와무라성",
        "金山城": "카나야마성",
        "犬山城": "이누야마성",
        "稲葉山城": "이나바야마성",
        "岐阜城": "기후성",
        "大垣城": "오오가키성",
        "亀山城": "카메야마성",
        "安濃津城": "아노쓰성",
        "大河内城": "오코치성",
        "田丸城": "타마루성",
        "鳥羽城": "토바성",
        "金ヶ崎城": "카나가사키성",
        "敦賀城": "쓰루가성",
        "後瀬山城": "이치노세야마성",
        "小谷城": "오다니성",
        "長浜城": "나가하마성",
        "佐和山城": "사와야마성",
        "観音寺城": "간논지성",
        "近江八幡城": "오미하치만성",
        "日野城": "히노성",
        "伊賀上野城": "이가우에노성",
        "朽木谷城": "쿠쓰키다니성",
        "坂本城": "사카모토성",
        "二条御所": "니죠고쇼",
        "伏見城": "후시미성",
        "勝龍寺城": "쇼류지성",
        "芥川山城": "아쿠타가와야마성",
        "高槻城": "타카쓰키성",
        "筒井城": "쓰쓰이성",
        "大和郡山城": "야마토코리야마성",
        "信貴山城": "시키산성",
        "高取城": "타카토리성",
        "高屋城": "타카야성",
        "石山御坊": "이시야마고보",
        "大坂城": "오사카성",
        "岸和田城": "키시와다성",
        "雑賀城": "사이카성",
        "和歌山城": "와카야마성",
        "新宮城": "신구성",
        "伊丹城": "이타미성",
        "有岡城": "아리오카성",
        "八木城": "야기성",
        "丹波亀山城": "단바카메야마성",
        "建部山城": "타케베야마성",
        "田辺城": "타나베성",
        "八上城": "야가미성",
        "黒井城": "쿠로이성",
        "福知山城": "후쿠치야마성",
        "花隈城": "하나쿠마성",
        "三木城": "미키성",
        "御着城": "코착성",
        "姫路城": "히메지성",
        "置塩城": "오키시오성",
        "竹田城": "타케다성",
        "此隅城": "코노스미성",
        "上月城": "코즈키성",
        "鳥取城": "돗토리성",
        "羽衣石城": "우에시성",
        "津山城": "쓰야마성",
        "天神山城": "텐진야마성",
        "岡山城": "오카야마성",
        "備中高松城": "빗추타카마쓰성",
        "高田城": "타카다성",
        "鶴首城": "쓰루쿠비성",
        "備中松山城": "빗추마쓰야마성",
        "神辺城": "칸나베성",
        "鞆城": "토모성",
        "月山富田城": "갓산토다성",
        "三刀屋城": "미토야성",
        "山吹城": "야마부키성",
        "比叡尾山城": "히에오야마성",
        "比熊山城": "히구마야마성",
        "新高山城": "니이다카야마성",
        "安芸高山城": "아기타카야마성",
        "吉田郡山城": "요시다코오리야마성",
        "鏡山城": "카가미야마성",
        "佐東銀山城": "사토긴잔성",
        "広島城": "히로시마성",
        "桜尾城": "사쿠라오성",
        "周防高森城": "스오타카모리성",
        "津和野城": "쓰와노성",
        "指月城": "시즈키성",
        "山口館": "야마구치관",
        "櫛崎城": "쿠시자키성",
        "洲本城": "스모토성",
        "勝瑞城": "쇼즈이성",
        "徳島城": "도쿠시마성",
        "十河城": "소고성",
        "高松城": "타카마쓰성",
        "天霧城": "아마기리성",
        "白地城": "하쿠치성",
        "川之江城": "카와노에성",
        "本山城": "모토야마성",
        "岡豊城": "오코성",
        "浦戸城": "우라도성",
        "安芸城": "아키성",
        "湯築城": "유즈키성",
        "黒瀬城": "쿠로세성",
        "宇和島城": "우와지마성",
        "中村御所": "나카무라고쇼",
        "中村城": "나카무라성",
        "門司城": "모지성",
        "小倉城": "고쿠라성",
        "城井谷城": "키이다니성",
        "中津城": "나카쓰성",
        "古処山城": "코쇼산성",
        "秋月城": "아키즈키성",
        "立花山城": "다치바나야마성",
        "名島城": "나지마성",
        "岩屋城": "이와야성",
        "久留米城": "쿠루메성",
        "勢福寺城": "세후쿠지성",
        "柳川城": "야나가와성",
        "佐賀城": "사가성",
        "佐嘉城": "사가성",
        "金石城": "카네이시성",
        "伊万里城": "이마리성",
        "平戸城": "히라도성",
        "大村城": "오오무라성",
        "府内館": "후나이관",
        "臼杵城": "우스키성",
        "岡城": "오카성",
        "縣城": "아카타성",
        "岩尾城": "이와오성",
        "隈本城": "쿠마모토성",
        "日之江城": "히노에성",
        "人吉城": "히토요시성",
        "出水城": "이즈미성",
        "加治木城": "카지키성",
        "内城": "우치성",
        "伊作城": "이사쿠성",
        "都於郡城": "토노코오리성",
        "佐土原城": "사도와라성",
        "飫肥城": "오비성",
        "高山城": "코우야마성"
    }
    
    # Handle composite names (joined by newline or something)
    parts = jp_name.split('\n')
    translated_parts = [name_map.get(p.strip(), p.strip()) for p in parts]
    return " / ".join(translated_parts)

def parse_castle_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    castles = []
    current_castle = None
    
    # Skip the header
    for line in lines[1:]:
        line = line.strip('\n')
        if not line.strip():
            continue
            
        columns = line.split('\t')
        
        # Check if this line starts with a region (e.g., "1東北")
        if re.match(r'^\d', columns[0]):
            # Start of a new castle entry
            current_castle = {
                "지방": translate_region(columns[0].strip()),
                "성 타입": translate_type(columns[1].strip()),
                "성 이름 (일본어)": columns[2].strip(),
                "성 이름 (한국어)": get_korean_name(columns[2].strip()),
                "고쿠다카": 0,
                "내구도": 0,
                "군 수": 0,
                "항구 수": 0
            }
            
            # Check if this line already contains numbers
            has_stats = False
            for i in range(3, len(columns)):
                col = columns[i].strip()
                if col.isdigit():
                    has_stats = True
                    break
            
            if has_stats:
                # Stats are on the same line (unusual based on preview but possible)
                if len(columns) > 3 and columns[3].strip().isdigit():
                    current_castle["고쿠다카"] = int(columns[3].strip())
                if len(columns) > 4 and columns[4].strip().isdigit():
                    current_castle["내구도"] = int(columns[4].strip())
                if len(columns) > 5 and columns[5].strip().isdigit():
                    current_castle["군 수"] = int(columns[5].strip())
                if len(columns) > 6 and columns[6].strip().isdigit():
                    current_castle["항구 수"] = int(columns[6].strip())
                castles.append(current_castle)
                current_castle = None
            else:
                # Stats might be on the next line
                pass
        else:
            # Continuation line
            if current_castle:
                # Add additional name if present before stats
                if columns[0].strip() and not columns[0].strip().isdigit():
                    orig_jp = current_castle["성 이름 (일본어)"]
                    new_jp = columns[0].strip()
                    current_castle["성 이름 (일본어)"] = f"{orig_jp}\n{new_jp}"
                    current_castle["성 이름 (한국어)"] = get_korean_name(current_castle["성 이름 (일본어)"])
                
                # Look for stats in columns
                found_stats = False
                # The stats might be offset if a name was present
                # Looking for the first digit column
                for i, col in enumerate(columns):
                    val = col.strip()
                    if val.isdigit():
                        found_stats = True
                        current_castle["고쿠다카"] = int(val)
                        if i + 1 < len(columns) and columns[i+1].strip().isdigit():
                            current_castle["내구도"] = int(columns[i+1].strip())
                        if i + 2 < len(columns) and columns[i+2].strip().isdigit():
                            current_castle["군 수"] = int(columns[i+2].strip())
                        if i + 3 < len(columns) and columns[i+3].strip().isdigit():
                            current_castle["항구 수"] = int(columns[i+3].strip())
                        break
                
                if found_stats:
                    castles.append(current_castle)
                    current_castle = None
            else:
                # Unexpected line, skip or log
                pass

    return castles

# Main execution
file_path = r'e:\AJ\02_Coding\02_Personal Project\NubuCastleMap\성 일람.txt'
castle_data = parse_castle_file(file_path)

# Save as JSON
with open(r'e:\AJ\02_Coding\02_Personal Project\NubuCastleMap\castles.json', 'w', encoding='utf-8') as f:
    json.dump(castle_data, f, ensure_ascii=False, indent=2)

print(f"Successfully processed {len(castle_data)} castles.")
