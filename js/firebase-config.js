// firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBM1-k4FaGCMEJAmnug6GfON7PgQRvwjJ0",
  authDomain: "worldtour-record-page.firebaseapp.com",
  projectId: "worldtour-record-page",
  storageBucket: "worldtour-record-page.firebasestorage.app",
  messagingSenderId: "860103680756",
  appId: "1:860103680756:web:29528ef71a459f1a55b4a1",
  measurementId: "G-696GR5GSE6"
};

// 파이어베이스 초기화
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const tokenFunctionUrl = 'https://asia-northeast3-manage-dev-tokens.cloudfunctions.net/getMapboxToken';

let cachedToken = null;

async function fetchMapboxToken() {
  if (cachedToken) return cachedToken;
  try {
    const response = await fetch(tokenFunctionUrl);
    if (!response.ok) throw new Error('서버 응답이 올바르지 않습니다.');
    const data = await response.json();
    cachedToken = data.token;
    return cachedToken;
  } catch (error) {
    console.error('맵박스 토큰을 가져오는 데 실패했습니다:', error);
    return null;
  }
}

// 에러 해결의 핵심: 모든 필요한 변수들을 export 해줍니다.
export { firebaseConfig, db, auth, provider, fetchMapboxToken };
