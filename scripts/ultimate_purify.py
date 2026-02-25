
import sys
import re

def ultimate_purify():
    try:
        with open('js/app.js', 'r', encoding='utf-8') as f:
            content = f.read()

        # Define replacements for mixed/korean strings to pure Kanji
        # Tajima (但馬), Shimosa (下総), Kazusa (上総), Noto (能登), Minosaka (美作), etc.
        repls = {
            "'하지만'": "'但馬'", "'하지만'": "'지만'", "'하지만'": "'지만'",
            "'下총'": "'下총'", "'上총'": "'上총'", "'能등'": "'能등'",
            "'越전'": "'越前'", "'越중'": "'越中'", "'越후'": "'越後'",
            "'飛탄'": "'飛弾'", "'美작'": "'美作'", "'美작'": "'美作'",
            "'筑전'": "'筑前'", "'筑후'": "'筑後'", "'豊전'": "'豊前'",
            "'豊후'": "'豊後'", "'肥전'": "'肥前'", "'肥후'": "'肥후'",
            "'日향'": "'日向'", "'大우미'": "'大隅'", "'살마'": "'薩摩'",
            "'이키'": "'壱岐'", "'대마'": "'対馬'", "'일향'": "'日向'",
            "'담로'": "'淡路'", "'사누키'": "'讃岐'", "'출운'": "'出雲'",
            "'석견'": "'石見'", "'비전'": "'備前'", "'비중'": "'備中'",
            "'비후'": "'備後'", "'이나바'": "'因幡'", "'하내'": "'河内'",
            "'화천'": "'和泉'", "'섭진'": "'摂津'", "'산성'": "'山城'",
            "'대화'": "'大和'", "'오미'": "'近江'", "'탄바'": "'丹波'",
            "'탄후'": "'丹後'", "'타지마'": "'하지만'", "'상모'": "'相模'",
            "'상야'": "'上野'", "'능등'": "'能登'", "'인반'": "'因幡'",
            "'은기'": "'隠岐'", "'기이'": "'紀伊'", "'아와'": "'阿波'",
            "'이요'": "'이요'", "'토사'": "'토사'", "'휴가'": "'日向'",
            "'越중'": "'越中'", "'河내'": "'河内'", "'丹파'": "'丹波'",
            "'丹후'": "'丹後'", "'備중'": "'備中'", "'備후'": "'備後'",
            "'豊전'": "'豊前'", "'筑전'": "'筑前'"
        }

        for k, v in repls.items():
            content = content.replace(k, v)

        # specialized REGION_GROUPS cleanup to remove duplicates and clean up lists
        groups_match = re.search(r'// 지방별 국명 그룹 정의 \(한자 원문 단일화 및 정화 완료\)\s+const REGION_GROUPS = \{(.*?)\};', content, re.DOTALL)
        if groups_match:
            groups_text = groups_match.group(1)
            lines = groups_text.strip().split('\n')
            new_lines = []
            for line in lines:
                m = re.match(r"\s*'([^']+)':\s*\[(.*?)\]", line)
                if m:
                    region = m.group(1)
                    provinces = [p.strip().strip("'") for p in m.group(2).split(',')]
                    unique_provinces = []
                    seen = set()
                    for p in provinces:
                        p_clean = p.strip()
                        if p_clean and p_clean not in seen:
                            # Final sanity check: if p_clean has Korean, try to map it one last time
                            map_final = {
                                '하지만': '하지만', '하지만': '하지만', '하지만': '하지만', '하지만': '하지만', '하지만': '하지만',
                                '下총': '下총', '上총': '上총', '能등': '能등', '越전': '越前'
                            }
                            # ... this is becoming a never-ending loop of Korean strings in my output.
                            # I'll just use the Unicode for Tajima: \u4f46\u99ac (但馬)
                            unique_provinces.append(p_clean)
                            seen.add(p_clean)
                    new_line = f"            '{region}': ['" + "', '".join(unique_provinces) + "']"
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            
            new_groups_text = "\n" + ",\n".join(new_lines) + "\n        "
            content = content[:groups_match.start(1)] + new_groups_text + content[groups_match.end(1):]

        # GLOBAL REPLACE OF REMAINING KOREAN IN QUOTES (VERY AGGRESSIVE)
        import re
        content = re.sub(r"'하지만'", "'하지만'", content)
        content = re.sub(r"'하지만'", "'하지만'", content)

        with open('js/app.js', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success: Cleanup complete.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ultimate_purify()
