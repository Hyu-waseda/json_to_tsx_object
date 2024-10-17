# translateのoriginalフォルダの作成
prepare-original:
	cp -r translate/en/* translate/original/
	find translate/original -type f -name "*_en.tsx" -exec sh -c 'for file; do mv "$$file" "$$(echo "$$file" | sed "s/_en.tsx$$/_original.tsx/")"; done' sh {} +

# translateの"ZH-CN"を"ZH_CN"に置換
replace-zh-cn:
	find translate -type f -name "*_zh-cn.tsx" -exec sed -i '' 's/ZH-CN/ZH_CN/g' {} +

# translateの"ZH-CN"を"ZH_CN"に置換
replace-zh-tw:
	find translate -type f -name "*_zh-tw.tsx" -exec sed -i '' 's/ZH-TW/ZH_TW/g' {} +

# translateの補完
fix_translate_to_multi_bbs: prepare-original replace-zh-cn replace-zh-tw

.PHONY: prepare-original replace-zh-cn replace-zh-tw fix_translate_to_multi_bbs