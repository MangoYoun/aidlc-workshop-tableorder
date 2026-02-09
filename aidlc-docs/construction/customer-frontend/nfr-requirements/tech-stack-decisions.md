# Tech Stack Decisions - Customer Frontend

## Overview

Customer Frontend의 기술 스택 선택 및 그 근거를 문서화합니다.

---

## 1. Frontend Framework

### 선택: Vue.js 3

**선택 이유**:
- **학습 곡선**: React보다 낮음, 초보자 친화적
- **성능**: Composition API로 최적화된 반응성
- **생태계**: 풍부한 라이브러리 및 도구
- **프로젝트 요구사항**: 단순한 SPA 구조에 적합

**대안**:
- React: 더 큰 생태계, 하지만 학습 곡선 높음
- Angular: 엔터프라이즈급, 하지만 과도한 복잡도
- Svelte: 빠른 성능, 하지만 생태계 작음

**버전**: Vue.js 3.4+ (최신 안정 버전)

---

## 2. Build Tool

### 선택: Vite

**선택 이유**:
- **빠른 개발 서버**: HMR (Hot Module Replacement) 즉시 반영
- **빠른 빌드**: esbuild 기반 번들링
- **Vue.js 공식 지원**: Vue 팀이 개발
- **간단한 설정**: 최소한의 설정으로 시작 가능

**대안**:
- Webpack: 더 많은 플러그인, 하지만 느린 빌드
- Parcel: 제로 설정, 하지만 Vue 지원 약함
- Rollup: 라이브러리 빌드에 적합, 앱 빌드는 Vite가 우수

**버전**: Vite 5.0+

---

## 3. State Management

### 선택: Pinia

**선택 이유**:
- **Vue.js 공식 상태 관리**: Vuex의 후속
- **간단한 API**: Composition API 스타일
- **TypeScript 지원**: 타입 안전성 (선택사항)
- **DevTools 지원**: Vue DevTools 통합

**대안**:
- Vuex: 레거시, Pinia가 공식 권장
- Zustand: React 전용
- MobX: 복잡한 학습 곡선

**Store 구조**:
- `authStore`: 인증 및 세션 관리
- `menuStore`: 메뉴 및 카테고리 관리
- `cartStore`: 장바구니 관리
- `orderStore`: 주문 관리

**버전**: Pinia 2.1+

---

## 4. Routing

### 선택: Vue Router

**선택 이유**:
- **Vue.js 공식 라우터**: 완벽한 통합
- **SPA 라우팅**: 클라이언트 측 라우팅 지원
- **네비게이션 가드**: 인증 체크 용이
- **간단한 설정**: 직관적인 API

**대안**:
- 없음 (Vue.js에서는 Vue Router가 표준)

**라우트 구조**:
```javascript
/login          → LoginView
/menu           → MenuView
/cart           → CartView
/orders         → OrderHistoryView
```

**버전**: Vue Router 4.2+

---

## 5. HTTP Client

### 선택: Axios

**선택 이유**:
- **널리 사용됨**: 검증된 라이브러리
- **Interceptor 지원**: 인증 토큰 자동 추가
- **에러 처리**: 일관된 에러 처리 가능
- **타임아웃 설정**: 네트워크 에러 대응

**대안**:
- Fetch API: 브라우저 내장, 하지만 Interceptor 없음
- ky: 경량, 하지만 생태계 작음

**설정**:
```javascript
// Axios 기본 설정
baseURL: process.env.VITE_API_URL
timeout: 10000 (10초)
headers: { 'X-Session-Token': sessionToken }
```

**버전**: Axios 1.6+

---

## 6. UI Framework

### 선택: Tailwind CSS

**선택 이유**:
- **유틸리티 우선**: 빠른 스타일링
- **커스터마이징**: 디자인 시스템 구축 용이
- **작은 번들 크기**: 사용하지 않는 클래스 제거 (PurgeCSS)
- **반응형**: 간단한 반응형 디자인

**대안**:
- Bootstrap: 컴포넌트 중심, 하지만 커스터마이징 어려움
- Vuetify: Material Design, 하지만 번들 크기 큼
- Element Plus: 엔터프라이즈급, 하지만 과도한 기능

**설정**:
```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: '#2196F3',
      secondary: '#FFC107',
      success: '#4CAF50',
      error: '#F44336'
    }
  }
}
```

**버전**: Tailwind CSS 3.4+

---

## 7. Icon Library

### 선택: Heroicons

**선택 이유**:
- **Tailwind CSS 제작사**: 완벽한 통합
- **SVG 아이콘**: 확장 가능, 커스터마이징 용이
- **무료**: MIT 라이선스
- **Vue 컴포넌트**: `@heroicons/vue` 패키지

**대안**:
- Font Awesome: 더 많은 아이콘, 하지만 유료
- Material Icons: Google 스타일, 하지만 Tailwind와 덜 어울림

**사용 예시**:
```vue
<ShoppingCartIcon class="w-6 h-6" />
```

**버전**: @heroicons/vue 2.1+

---

## 8. Form Validation

### 선택: 내장 HTML5 Validation

**선택 이유**:
- **간단한 구현**: 추가 라이브러리 불필요
- **브라우저 지원**: 모든 최신 브라우저 지원
- **충분한 기능**: 필수 필드, 타입 검증

**대안**:
- VeeValidate: 복잡한 검증, 하지만 과도한 기능
- Yup: 스키마 기반, 하지만 학습 곡선

**사용 예시**:
```vue
<input type="text" required minlength="4" />
```

---

## 9. Date/Time Handling

### 선택: JavaScript Date 객체

**선택 이유**:
- **내장 기능**: 추가 라이브러리 불필요
- **간단한 요구사항**: 날짜 표시만 필요
- **ISO 8601 형식**: Backend와 호환

**대안**:
- Day.js: 경량, 하지만 불필요
- Moment.js: 레거시, 권장하지 않음
- date-fns: 함수형, 하지만 과도한 기능

**사용 예시**:
```javascript
new Date().toISOString()
new Date(isoString).toLocaleString('ko-KR')
```

---

## 10. Image Optimization

### 선택: WebP 형식

**선택 이유**:
- **작은 파일 크기**: JPEG/PNG 대비 30% 감소
- **브라우저 지원**: 모든 최신 브라우저 지원
- **품질 유지**: 손실 압축이지만 품질 우수

**대안**:
- JPEG: 레거시, 더 큰 파일 크기
- PNG: 투명도 필요 시, 하지만 큰 파일 크기
- AVIF: 더 작은 크기, 하지만 브라우저 지원 약함

**설정**:
- 메뉴 이미지: WebP, 최대 800x600px
- 기본 이미지: WebP, 400x300px

---

## 11. Testing Framework

### 선택: Vitest

**선택 이유**:
- **Vite 통합**: 동일한 설정 공유
- **빠른 실행**: Vite의 빠른 빌드 활용
- **Jest 호환**: Jest API와 호환
- **Vue 지원**: @vue/test-utils 통합

**대안**:
- Jest: 널리 사용됨, 하지만 Vite와 통합 어려움
- Cypress: E2E 테스트, 하지만 Unit 테스트는 Vitest가 우수

**테스트 범위**:
- Unit Tests: Pinia Store, 유틸리티 함수
- Component Tests: Vue 컴포넌트
- Integration Tests: API 호출 (Mock)

**버전**: Vitest 1.0+

---

## 12. Linting & Formatting

### 선택: ESLint + Prettier

**선택 이유**:
- **ESLint**: 코드 품질 검사
- **Prettier**: 코드 포맷팅
- **Vue.js 지원**: eslint-plugin-vue
- **자동 수정**: IDE 통합

**설정**:
```javascript
// .eslintrc.js
extends: [
  'plugin:vue/vue3-recommended',
  'eslint:recommended',
  'prettier'
]
```

**버전**:
- ESLint 8.0+
- Prettier 3.0+
- eslint-plugin-vue 9.0+

---

## 13. Environment Variables

### 선택: Vite 환경 변수

**선택 이유**:
- **Vite 내장**: 추가 설정 불필요
- **타입 안전**: TypeScript 지원 (선택사항)
- **빌드 시 주입**: 런타임 오버헤드 없음

**파일 구조**:
```
.env.development    # 개발 환경
.env.production     # 프로덕션 환경
```

**사용 예시**:
```javascript
const apiUrl = import.meta.env.VITE_API_URL
```

---

## 14. Package Manager

### 선택: npm

**선택 이유**:
- **Node.js 기본**: 추가 설치 불필요
- **널리 사용됨**: 검증된 도구
- **충분한 성능**: 프로젝트 규모에 적합

**대안**:
- pnpm: 더 빠른 설치, 하지만 추가 학습 필요
- Yarn: 더 나은 워크스페이스, 하지만 불필요

**버전**: npm 10.0+

---

## Tech Stack Summary

| 카테고리 | 선택 | 버전 | 이유 |
|---------|------|------|------|
| Framework | Vue.js | 3.4+ | 초보자 친화적, 성능 우수 |
| Build Tool | Vite | 5.0+ | 빠른 개발 서버, 빠른 빌드 |
| State Management | Pinia | 2.1+ | Vue.js 공식, 간단한 API |
| Routing | Vue Router | 4.2+ | Vue.js 공식, SPA 라우팅 |
| HTTP Client | Axios | 1.6+ | Interceptor, 에러 처리 |
| UI Framework | Tailwind CSS | 3.4+ | 유틸리티 우선, 커스터마이징 |
| Icon Library | Heroicons | 2.1+ | Tailwind 통합, SVG |
| Form Validation | HTML5 | - | 간단한 구현, 충분한 기능 |
| Date/Time | JavaScript Date | - | 내장 기능, 간단한 요구사항 |
| Image Format | WebP | - | 작은 파일 크기, 품질 유지 |
| Testing | Vitest | 1.0+ | Vite 통합, 빠른 실행 |
| Linting | ESLint + Prettier | 8.0+ / 3.0+ | 코드 품질, 포맷팅 |
| Env Variables | Vite Env | - | 내장 기능, 타입 안전 |
| Package Manager | npm | 10.0+ | 기본 도구, 충분한 성능 |

---

## Dependencies

### Production Dependencies

```json
{
  "vue": "^3.4.0",
  "vue-router": "^4.2.0",
  "pinia": "^2.1.0",
  "axios": "^1.6.0",
  "@heroicons/vue": "^2.1.0"
}
```

### Development Dependencies

```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-vue": "^5.0.0",
  "tailwindcss": "^3.4.0",
  "autoprefixer": "^10.4.0",
  "postcss": "^8.4.0",
  "vitest": "^1.0.0",
  "@vue/test-utils": "^2.4.0",
  "eslint": "^8.0.0",
  "eslint-plugin-vue": "^9.0.0",
  "prettier": "^3.0.0"
}
```

---

## Project Structure

```
customer-frontend/
├── public/
│   └── images/
│       └── placeholder.png
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   └── index.js
│   ├── stores/
│   │   ├── auth.js
│   │   ├── menu.js
│   │   ├── cart.js
│   │   └── order.js
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── MenuView.vue
│   │   ├── CartView.vue
│   │   └── OrderHistoryView.vue
│   ├── components/
│   │   ├── CategoryTabs.vue
│   │   ├── MenuCard.vue
│   │   ├── CartItem.vue
│   │   └── shared/
│   │       ├── AppHeader.vue
│   │       ├── LoadingSpinner.vue
│   │       └── ErrorMessage.vue
│   ├── services/
│   │   └── api.js
│   └── assets/
│       └── main.css
├── tests/
│   ├── unit/
│   └── integration/
├── .env.development
├── .env.production
├── .eslintrc.js
├── .prettierrc
├── tailwind.config.js
├── vite.config.js
├── package.json
└── README.md
```

---

## Development Workflow

### 1. 개발 서버 실행
```bash
npm run dev
```

### 2. 빌드
```bash
npm run build
```

### 3. 프리뷰
```bash
npm run preview
```

### 4. 테스트
```bash
npm run test
```

### 5. 린트
```bash
npm run lint
```

---

## Browser Support

| 브라우저 | 최소 버전 | 지원 |
|---------|----------|------|
| Chrome | 최신 | ✅ |
| Firefox | 최신 | ✅ |
| Safari | 최신 | ✅ |
| Edge | 최신 | ✅ |
| IE 11 | - | ❌ |

---

## Performance Targets

| 메트릭 | 목표 | 측정 도구 |
|--------|------|----------|
| First Contentful Paint | < 2초 | Lighthouse |
| Time to Interactive | < 3초 | Lighthouse |
| Bundle Size (gzip) | < 500KB | Vite Build |
| API Response Time | < 1초 | Network Tab |
| Memory Usage | < 100MB | DevTools |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
