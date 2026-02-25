// firebase-config.js에서 내보낸 변수들을 가져옵니다.
import { fetchMapboxToken } from './firebase-config.js';
import {
    REGION_MAP,
    REGION_COLORS,
    REGION_GROUPS,
    PROVINCE_TO_REGION,
    PROVINCE_KO_MAP,
    LABEL_ADJUSTMENTS
} from './map-data.js';

const MAPBOX_ACCESS_TOKEN = await fetchMapboxToken();
mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v11', // 현대적인 다크 스타일
    center: [133.5, 35.7], // 일본 중앙
    zoom: 5.9,
    bearing: -20,
    projection: 'mercator' // 평면(메르카토르) 투영법 적용
});

let castleData = [];
const markers = [];

async function init() {
    try {
        const response = await fetch('./data/castles.json');
        castleData = await response.json();

        // 지방별 통계 계산 (현재 미사용)
        // updateStats();
        // 마커 생성
        renderMarkers(castleData);
        // 필터 생성
        renderFilters();
        // 검색 및 토글 이벤트 리스너 등록
        initEventListeners();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function updateStats() {
    const totalCount = castleData.length;
    document.querySelector('.stat-card .value').textContent = totalCount.toLocaleString();
}

function renderMarkers(data) {
    // 기존 마커 제거
    markers.forEach(m => m.remove());
    markers.length = 0;

    data.forEach(castle => {
        if (!castle.좌표) return;

        const el = document.createElement('div');
        el.className = 'castle-marker';

        // 타입별 클래스 추가
        if (castle['성 타입'] === '산성') el.classList.add('type-mountain');
        else if (castle['성 타입'] === '평성') el.classList.add('type-flat');

        // 상단 레이블 추가 (줌 6.2 이상에서 표시)
        const koNamesList = castle['성 이름 (한국어)'].split('/').map(s => s.trim());
        const jaNamesList = castle['성 이름 (일본어)'].split(/[\n/]/).map(s => s.trim()).filter(s => s);
        const firstKo = koNamesList[0];
        const firstJa = jaNamesList[0] || '';

        const label = document.createElement('div');
        label.className = 'castle-label';
        label.innerHTML = `${firstJa}<br><span class="ko-name">(${firstKo})</span>`;
        el.appendChild(label);

        // 이름 분리 및 렌더링 로직 (팝업용)
        const koNames = castle['성 이름 (한국어)'].split('/').map(s => s.trim());
        const jaNames = castle['성 이름 (일본어)'].split(/[\n/]/).map(s => s.trim()).filter(s => s);

        // 이름들을 쌍으로 묶어서 HTML 생성
        let namesHtml = '';
        koNames.forEach((ko, idx) => {
            const ja = jaNames[idx] || '';
            namesHtml += `
                <div class="name-pair" style="margin-bottom: 8px;">
                    <h2 style="margin-bottom: 2px;">${ko}</h2>
                    <div class="ja-name" style="font-size: 13px; color: var(--text-secondary);">${ja}</div>
                </div>
            `;
        });

        // 팝업 내용 구성
        const popupHtml = `
            <div class="popup-header">
                ${namesHtml}
                ${castle['현재 명칭'] ? `<div class="current-name" style="font-size: 11px; color:#aaa; margin-top:4px; border-top: 1px solid var(--glass-border); padding-top:4px;">현: ${castle['현재 명칭']}</div>` : ''}
            </div>
            <div class="popup-body">
                <div class="item"><span class="label">지방</span><span class="val">${REGION_MAP[castle['지방']] || castle['지방']}</span></div>
                <div class="item"><span class="label">타입</span><span class="val">${castle['성 타입']}</span></div>
                <div class="item"><span class="label">고쿠다카</span><span class="val">${castle['고쿠다카'].toLocaleString()}</span></div>
                <div class="item"><span class="label">내구도</span><span class="val">${castle['내구도'].toLocaleString()}</span></div>
                <div class="item"><span class="label">군 수</span><span class="val">${castle['군 수']}</span></div>
            </div>
        `;

        const popup = new mapboxgl.Popup({
            offset: 17,
            closeButton: false // 닫기 버튼 제거
        })
            .setHTML(popupHtml)
            .on('open', updateMarkerStates)
            .on('close', () => {
                // 사용자가 검색창에 입력 중일 때는 타이핑을 방해하지 않기 위해 리셋하지 않음
                const searchInput = document.getElementById('castle-search');
                if (searchInput && document.activeElement !== searchInput) {
                    searchInput.value = '';
                    updateMarkerStates();
                }
            });

        const marker = new mapboxgl.Marker(el)
            .setLngLat([castle.좌표.lng, castle.좌표.lat])
            .setPopup(popup)
            .addTo(map);

        // 검색 및 제어를 위해 특정 데이터 연결
        marker.castleData = castle;
        markers.push(marker);
    });
}

function renderFilters() {
    const regions = [...new Set(castleData.map(c => c.지방))];
    const regionListEl = document.querySelector('.region-list');

    regionListEl.innerHTML = '';

    // '전체' 버튼 추가 (색상 배지 없음 또는 회색)
    const allBtn = createFilterBtn('전체', castleData.length, '#fff');
    allBtn.classList.add('active');
    allBtn.addEventListener('click', () => {
        setActiveFilter(allBtn);
        renderMarkers(castleData);
        map.flyTo({ center: [133.5, 35.7], zoom: 5.9 });
    });
    regionListEl.appendChild(allBtn);

    regions.forEach(region => {
        const count = castleData.filter(c => c.지방 === region).length;
        const color = REGION_COLORS[region] || '#ccc'; // 색상 설정에서 가져옴
        const btn = createFilterBtn(REGION_MAP[region] || region, count, color);

        btn.addEventListener('click', () => {
            setActiveFilter(btn);
            const filtered = castleData.filter(c => c.지방 === region);
            renderMarkers(filtered);

            // 필터링된 지역으로 지도 이동
            if (filtered.length > 0) {
                const lats = filtered.map(c => c.좌표 ? c.좌표.lat : null).filter(n => n);
                const lngs = filtered.map(c => c.좌표 ? c.좌표.lng : null).filter(n => n);
                if (lats.length > 0) {
                    const centerLat = lats.reduce((a, b) => a + b) / lats.length;
                    const centerLng = lngs.reduce((a, b) => a + b) / lngs.length;
                    map.flyTo({ center: [centerLng, centerLat], zoom: 7, duration: 1000 });
                }
            }
        });

        regionListEl.appendChild(btn);
    });
}

function createFilterBtn(label, count, color) {
    const btn = document.createElement('button');
    btn.className = 'region-btn';
    btn.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="color-dot" style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: ${color}; border: 1px solid rgba(255,255,255,0.2);"></span>
            <span>${label}</span>
        </div>
        <span class="count">${count}</span>
    `;
    return btn;
}

function setActiveFilter(activeBtn) {
    document.querySelectorAll('.region-btn').forEach(btn => btn.classList.remove('active'));
    activeBtn.classList.add('active');
}

// 기본 지도의 모든 레이블과 경계선을 숨기는 함수
function customizeMapLayers() {
    const layers = map.getStyle().layers;

    layers.forEach(layer => {
        // 1. 모든 텍스트/심볼 레이어 숨기기
        if (layer.type === 'symbol') {
            map.setLayoutProperty(layer.id, 'visibility', 'none');
        }

        // 2. 모든 경계선 및 도로 레이어 숨기기
        const isBoundary = layer.id.includes('admin') || layer.id.includes('boundary') || layer.id.includes('border');
        const isRoad = layer.id.includes('road') || (layer.source === 'composite' && layer['source-layer'] === 'road');

        if (isBoundary || isRoad) {
            map.setLayoutProperty(layer.id, 'visibility', 'none');
        }
    });
}

// 커스텀 GeoJSON 경계 데이터 로드 및 레이어 추가
async function loadProvincialBoundaries() {
    try {
        const response = await fetch('./data/yul_map.geojson');
        if (!response.ok) throw new Error('GeoJSON load failed');
        const data = await response.json();

        // 좌표계 변환 (EPSG:3857 -> EPSG:4326)
        const R = 20037508.34;
        const convertCoords = (coords) => {
            if (typeof coords[0] === 'number') {
                const lng = (coords[0] * 180) / R;
                const lat = (Math.atan(Math.exp((coords[1] * Math.PI) / R)) * 360) / Math.PI - 90;
                return [lng, lat];
            }
            return coords.map(convertCoords);
        };

        // 데이터 내부의 모든 좌표 변환 및 한국어 속성 주입
        const processedNames = new Map();

        data.features.forEach(feature => {
            if (feature.geometry && feature.geometry.coordinates) {
                feature.geometry.coordinates = convertCoords(feature.geometry.coordinates);
            }

            // 데이터 오염 방지를 위한 국명(nameKey) 정규화 (한자 단일화)
            let nameKey = feature.properties['国명'] || feature.properties['国名'] || '';
            const koNameCandidate = PROVINCE_KO_MAP[nameKey] || '';

            feature.properties['ja_name'] = nameKey ? nameKey + '国' : '';
            feature.properties['ko_name'] = koNameCandidate ? koNameCandidate + '국' : '';

            // 지방(Region) 및 색상 할당
            const region = PROVINCE_TO_REGION[nameKey] || '';
            feature.properties['region'] = region;
            feature.properties['color'] = REGION_COLORS[region] || '#ffffff';

            const jaName = nameKey;

            // 레이블 표시를 위한 메인 영역 식별 및 좌표 추출
            if (jaName) {
                // 좌표 가중치(면적 대용) 계산
                let pointCount = 0;
                let centerX = 0, centerY = 0;
                let mainCoords = [];

                if (feature.geometry.type === 'MultiPolygon') {
                    // MultiPolygon 중 가장 큰 조각 찾기
                    let maxP = 0;
                    feature.geometry.coordinates.forEach(poly => {
                        let pCount = 0;
                        poly[0].forEach(p => pCount++);
                        if (pCount > maxP) {
                            maxP = pCount;
                            mainCoords = poly[0];
                        }
                    });
                } else {
                    mainCoords = feature.geometry.coordinates[0];
                }

                // 선정된 메인 조각의 중심점 계산
                mainCoords.forEach(p => {
                    centerX += p[0];
                    centerY += p[1];
                });
                pointCount = mainCoords.length;

                if (!processedNames.has(jaName) || pointCount > processedNames.get(jaName).pointCount) {
                    let finalCoords = [centerX / pointCount, centerY / pointCount];

                    // 개별 보정값 적용
                    if (LABEL_ADJUSTMENTS[jaName]) {
                        finalCoords[0] += LABEL_ADJUSTMENTS[jaName][0];
                        finalCoords[1] += LABEL_ADJUSTMENTS[jaName][1];
                    }

                    processedNames.set(jaName, {
                        pointCount: pointCount,
                        coords: finalCoords,
                        properties: { ...feature.properties }
                    });
                }
            }
        });

        // 최종 확정된 각 국명의 단일 포인트들만 Feature로 생성
        const labelFeatures = Array.from(processedNames.values()).map(info => ({
            type: 'Feature',
            properties: info.properties,
            geometry: { type: 'Point', coordinates: info.coords }
        }));

        map.addSource('provincial-boundaries', {
            type: 'geojson',
            data: data
        });

        // 레이블 전용 포인트 소스 추가
        map.addSource('provincial-label-points', {
            type: 'geojson',
            data: { type: 'FeatureCollection', features: labelFeatures }
        });

        // 경계선 외곽선 추가
        map.addLayer({
            'id': 'provincial-line',
            'type': 'line',
            'source': 'provincial-boundaries',
            'layout': {},
            'paint': {
                'line-color': '#777',
                'line-width': 0.8,
                'line-opacity': 0.5
            }
        });

        // 영역 배경 살짝 추가 (라인 아래에 배치)
        map.addLayer({
            'id': 'provincial-fill',
            'type': 'fill',
            'source': 'provincial-boundaries',
            'paint': {
                'fill-color': ['get', 'color'],
                'fill-opacity': 0.18
            }
        }, 'provincial-line');

        // 영역 이름 레이블 추가 (단일 포인트 소스를 사용하여 중복 완벽 차단)
        map.addLayer({
            'id': 'provincial-labels',
            'type': 'symbol',
            'source': 'provincial-label-points',
            'layout': {
                'text-field': [
                    'format',
                    ['get', 'ja_name'], { 'font-scale': 1.2 },
                    '\n', {},
                    ['concat', '(', ['get', 'ko_name'], ')'], { 'font-scale': 0.8 }
                ],
                'text-font': ['Open Sans Regular', 'Arial Unicode MS Regular'],
                'text-size': [
                    'interpolate',
                    ['exponential', 1.5],
                    ['zoom'],
                    4, 4,
                    8, 18,
                    12, 48
                ],
                'text-allow-overlap': false,
                'text-anchor': 'center'
            },
            'paint': {
                'text-color': '#ddd',
                'text-opacity': 0.2
            }
        });

    } catch (error) {
        console.error('Error loading Provincial GeoJSON:', error);
    }
}

// 지도 로드 후 실행
map.on('load', () => {
    customizeMapLayers();
    loadProvincialBoundaries();
    init();

    // 줌 레벨에 따라 레이블 표시 여부 및 투명도, 크기 제어
    const toggleLabels = () => {
        const zoom = map.getZoom();
        const mapContainer = map.getContainer();

        let opacity = 0;
        let scale = 1;

        const labelToggle = document.getElementById('label-toggle');
        const isLabelEnabled = labelToggle ? labelToggle.checked : true;

        if (zoom >= 6.2 && isLabelEnabled) {
            // 줌 6.2부터 시작해서 7.5까지 서서히 투명도가 1이 됨
            opacity = Math.min(1, Math.max(0, (zoom - 6.2) / 1.3));
            // 줌 레벨에 따라 크기 조절 (최대 3배)
            scale = 0.5 + Math.max(0, (zoom - 6.2) * 0.6);
            if (scale > 16) scale = 16;
        }
        mapContainer.style.setProperty('--label-opacity', opacity);
        mapContainer.style.setProperty('--label-scale', scale);
    };

    map.on('zoom', toggleLabels);
    toggleLabels(); // 초기 체크

    // 외부에서 접근할 수 있도록 이벤트를 다시 연결하거나 전역 변수로 관리
    const labelToggle = document.getElementById('label-toggle');
    if (labelToggle) {
        labelToggle.addEventListener('change', toggleLabels);
    }
});

// 이벤트 리스너 등록 함수
function initEventListeners() {
    const searchInput = document.getElementById('castle-search');

    // 검색 입력 이벤트
    searchInput.addEventListener('input', (e) => {
        const keyword = e.target.value.toLowerCase().trim();

        // 검색어에 따른 팝업 자동 개폐만 처리
        markers.forEach(marker => {
            const castle = marker.castleData;
            const isMatched = keyword && (
                castle['성 이름 (한국어)'].toLowerCase().includes(keyword) ||
                castle['성 이름 (일본어)'].toLowerCase().includes(keyword) ||
                (castle['현재 명칭'] || '').toLowerCase().includes(keyword)
            );

            if (isMatched) {
                if (!marker.getPopup().isOpen()) marker.getPopup().addTo(map);
            } else if (keyword) { // 검색 중일 때만 검색 결과가 아닌 팝업 닫기
                if (marker.getPopup().isOpen()) marker.getPopup().remove();
            }
        });

        updateMarkerStates();
    });
}

// 마커들의 Dimmed 상태를 통합 관리하는 함수
function updateMarkerStates() {
    const searchInput = document.getElementById('castle-search');
    const keyword = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const anyPopupOpen = markers.some(m => m.getPopup().isOpen());
    const isAnythingActive = keyword !== '' || anyPopupOpen;

    markers.forEach(marker => {
        const el = marker.getElement();
        const castle = marker.castleData;
        const isMatchedSearch = keyword && (
            castle['성 이름 (한국어)'].toLowerCase().includes(keyword) ||
            castle['성 이름 (일본어)'].toLowerCase().includes(keyword) ||
            (castle['현재 명칭'] || '').toLowerCase().includes(keyword)
        );
        const isPopupOpen = marker.getPopup().isOpen();

        // 현재 검색어에 매칭되거나 팝업이 열려있는 마커는 강조
        if (isMatchedSearch || isPopupOpen) {
            el.classList.remove('dimmed');
        }
        // 무언가 활성화(검색 중이거나 팝업 열림)된 상태에서는 매칭되지 않은 것들 Dim
        else if (isAnythingActive) {
            el.classList.add('dimmed');
        }
        // 아무것도 활성화되지 않은 평상시에는 모두 정상 표시
        else {
            el.classList.remove('dimmed');
        }
    });
}
