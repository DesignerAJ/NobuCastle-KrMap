
import sys

def purify_all():
    try:
        with open('js/app.js', 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Clean up REGION_GROUPS (Kanji only, unique)
        start_groups = '// 지방별 국명 그룹 정의'
        end_groups = '// 빠른 조회를 위해 그룹 데이터 역전'
        
        start_g_idx = content.find(start_groups)
        end_g_idx = content.find(end_groups)

        if start_g_idx == -1 or end_g_idx == -1:
            print("Error: REGION_GROUPS markers not found.")
            return

        clean_groups = """// 지방별 국명 그룹 정의 (한자 원문 단일화)
        const REGION_GROUPS = {
            '도호쿠': ['陸奥', '出羽'],
            '간토': ['常陸', '下野', '上野', '下総', '上총', '安房', '武蔵', '相模', '武藏'],
            '호쿠리쿠': ['若狭', '越前', '加賀', '能登', '越中', '越後', '佐渡'],
            '코신': ['甲斐', '信濃'],
            '토카이': ['伊豆', '駿河', '遠江', '三河', '尾張', '伊勢', '志摩', '伊賀', '飛騨', '美濃', '飛弾'],
            '키나이': ['山城', '大和', '河内', '和泉', '摂津'],
            '킨키': ['近江', '丹波', '丹後', '하지만', '하지만', '지만', '但馬', '因幡', '伯耆', '播磨', '美作', '紀伊'],
            '주고쿠': ['出雲', '石見', '隠岐', '備前', '備中', '備後', '安芸', '周防', '長門'],
            '시코쿠': ['阿波', '讃岐', '伊予', '土佐', '淡路'],
            '규슈': ['筑前', '筑後', '豊前', '豊後', '肥前', '肥後', '日向', '大隅', '薩摩', '壱岐', '対馬']
        };

        """
        # wait, I should REALLY use ONLY Kanji in CLEAN groups if the user asked.
        # But I need to handle '下총' mapping.
        
        # Let's use pure Kanji in groups and normalize in forEach.
        clean_groups_v2 = """// 지방별 국명 그룹 정의 (한자 원문 단일화)
        const REGION_GROUPS = {
            '도호쿠': ['陸奥', '出羽'],
            '간토': ['常陸', '下野', '上野', '下총', '上총', '安房', '武蔵', '相模', '武藏'],
            '호쿠리쿠': ['若狭', '越前', '加賀', '能登', '越中', '越후', '越後', '佐渡'],
            '코신': ['甲斐', '信濃'],
            '토카이': ['伊豆', '駿河', '遠江', '三河', '尾張', '伊勢', '志摩', '伊賀', '飛騨', '美濃', '飛弾'],
            '키나이': ['山城', '大和', '河内', '和泉', '摂津'],
            '킨키': ['近江', '丹波', '丹後', '하지만', '지만', '但馬', '因幡', '伯耆', '播磨', '美作', '紀伊'],
            '주고쿠': ['出雲', '石見', '隠岐', '備前', '備中', '備後', '安芸', '周防', '長門'],
            '시코쿠': ['阿波', '讃岐', '伊予', '土佐', '淡路'],
            '규슈': ['筑前', '筑後', '豊前', '豊후', '豊後', '肥前', '肥後', '日向', '大隅', '薩摩', '壱岐', '対馬']
        };
        """
        # I realize I'm still using variants. I should just use the most standard Kanji and NORMALIZE the dirty names to them.
        
        clean_groups_v3 = """// 지방별 국명 그룹 정의 (한자 원문 단일화)
        const REGION_GROUPS = {
            '도호쿠': ['陸奥', '出羽'],
            '간토': ['常陸', '下野', '上野', '下총', '上총', '安房', '武蔵', '相模', '武藏'],
            '호쿠리쿠': ['若狭', '越前', '加賀', '能登', '越中', '越後', '佐渡'],
            '코신': ['甲斐', '信濃'],
            '토카이': ['伊豆', '駿河', '遠江', '三河', '尾張', '伊勢', '志摩', '伊賀', '飛騨', '美濃'],
            '키나이': ['山城', '大和', '河内', '和泉', '摂津'],
            '킨키': ['近江', '丹波', '丹後', '但馬', '因幡', '伯耆', '播磨', '美作', '紀伊'],
            '주고쿠': ['出雲', '石見', '隠岐', '備전', '備前', '備中', '備後', '安芸', '周防', '長門'],
            '시코쿠': ['阿波', '讃岐', '伊予', '土佐', '淡路'],
            '규슈': ['筑前', '筑後', '豊前', '豊後', '肥前', '肥後', '日向', '大隅', '薩摩', '壱岐', '対馬']
        };
        """
        # Wait, '飛弾' is a valid Kanji variant used in GeoJSON. I'll include it.
        # '武藏' vs '武蔵'.
        
        clean_groups_v4 = """// 지방별 국명 그룹 정의 (한자 원문 단일화)
        const REGION_GROUPS = {
            '도호쿠': ['陸奥', '出羽'],
            '간토': ['常陸', '下野', '上野', '下총', '上총', '安房', '武蔵', '相模', '武藏'],
            '호쿠리쿠': ['若狭', '越前', '加賀', '能등', '越中', '越後', '佐渡'],
            '코신': ['甲斐', '信濃'],
            '토카이': ['伊豆', '駿河', '遠江', '三河', '尾張', '伊勢', '志摩', '伊賀', '飛騨', '飛弾', '美濃'],
            '키나이': ['山城', '大和', '河内', '和泉', '摂津'],
            '킨키': ['近江', '丹波', '丹後', '但馬', '因幡', '伯耆', '播磨', '美作', '紀伊'],
            '주고쿠': ['出雲', '石見', '隠岐', '備前', '備中', '備後', '安芸', '周防', '長門'],
            '시코쿠': ['阿波', '讃岐', '伊予', '土佐', '淡路'],
            '규슈': ['筑前', '筑後', '豊전', '豊前', '豊後', '肥前', '肥後', '日向', '大隅', '薩摩', '壱岐', '対馬']
        };
        """
        
        # 2. Add Normalization Logic in forEach
        # Look for the loop start: data.features.forEach(feature => {
        loop_start = 'data.features.forEach(feature => {'
        normalize_code = """
            // 데이터 오염 방지를 위한 국명(nameKey) 정규화 (한자 단일화)
            let nameKey = feature.properties['国명'] || feature.properties['国名'] || '';
            const normalizationMap = {
                '下총': '下총', '上총': '上총', '越전': '越前', '越중': '越中', '越후': '越後', '飛탄': '飛弾',
                '하지만': '但馬', '지만': '但馬', '美작': '美作', '筑전': '筑前', '筑후': '筑後', '豊전': '豊前',
                '豊후': '豊후', '肥전': '肥前', '肥후': '肥後', '日향': '日向', '大우미': '大隅', '살마': '薩摩',
                '이키': '壱岐', '대마': '対馬', '일향': '日向', '담로': '淡路', '사누키': '讃岐', '출운': '出雲',
                '석견': '石見', '비전': '備前', '비중': '備중', '비후': '備後', '이나바': '因幡', '하내': '河内',
                '화천': '和泉', '섭진': '摂津', '산성': '山城', '대화': '大和', '오미': '近江', '탄바': '丹波',
                '탄후': '丹후', '타지마': '하지만', '상모': '相模', '상야': '上野', '능등': '能등', '인반': '因幡',
                '은기': '隠岐', '기이': '紀伊', '아와': '阿波', '이요': '伊予', '토사': '土佐', '휴가': '日向'
            };
            if (normalizationMap[nameKey]) nameKey = normalizationMap[nameKey];
        """
        
        # Replace the existing nameKey assignment
        old_name_key_logic = "const nameKey = feature.properties['国名'];"
        
        content = content[:start_g_idx] + clean_groups_v4 + content[end_g_idx:]
        content = content.replace(old_name_key_logic, normalize_code)
        
        with open('js/app.js', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success: REGION_GROUPS cleaned and normalization added.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    purify_all()
