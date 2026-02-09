# NFR Design Patterns - Customer Frontend

## Overview

Customer Frontend의 NFR 요구사항을 충족하기 위한 설계 패턴을 정의합니다.

---

## 1. Performance Patterns (성능 패턴)

### Pattern 1.1: Synchronous Component Loading
**목적**: 간단한 컴포넌트 로딩으로 개발 복잡도 최소화

**구현**:
```javascript
// router/index.js
import LoginView from '@/views/LoginView.vue'
import MenuView from '@/views/MenuView.vue'
import CartView from '@/views/CartView.vue'
import OrderHistoryView from '@/views/OrderHistoryView.vue'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/menu', component: MenuView },
  { path: '/cart', component: CartView },
  { path: '/orders', component: OrderHistoryView }
]
```

**장점**:
- 간단한 구현
- 예측 가능한 동작
- 디버깅 용이

**단점**:
- 초기 번들 크기 증가 (허용 가능 - 프로젝트 규모 작음)

---

### Pattern 1.2: Eager Image Loading
**목적**: 이미지 로딩 로직 단순화

**구현**:
```vue
<template>
  <img 
    :src="menu.imageUrl || '/images/placeholder.png'" 
    :alt="menu.name"
    @error="handleImageError"
  />
</template>

<script setup>
const handleImageError = (event) => {
  event.target.src = '/images/placeholder.png'
}
</script>
```

**장점**:
- 간단한 구현
- 이미지 수가 적어 성능 영향 미미

**단점**:
- 초기 로딩 시간 증가 (허용 가능)

---

### Pattern 1.3: Simple List Rendering
**목적**: 메뉴 목록 렌더링 단순화

**구현**:
```vue
<template>
  <div v-for="menu in filteredMenus" :key="menu.id">
    <MenuCard :menu="menu" />
  </div>
</template>

<script setup>
const filteredMenus = computed(() => {
  return menus.value.filter(m => m.categoryId === selectedCategoryId.value)
})
</script>
```

**장점**:
- 간단한 구현
- 100개 정도는 성능 문제 없음

**최적화**:
- `v-show` 대신 `v-if` 사용 (DOM 노드 최소화)
- `key` 속성으로 재사용 최적화

---

## 2. Availability Patterns (가용성 패턴)

### Pattern 2.1: Individual Loading States
**목적**: 각 API 호출의 로딩 상태를 독립적으로 관리

**구현**:
```javascript
// stores/menu.js
export const useMenuStore = defineStore('menu', () => {
  const menus = ref([])
  const loading = ref(false)
  const error = ref(null)

  const loadMenus = async (storeId) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/menus?store_id=${storeId}`)
      menus.value = response.data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return { menus, loading, error, loadMenus }
})
```

**장점**:
- 세밀한 로딩 상태 제어
- 각 화면별 독립적 로딩 표시

---

### Pattern 2.2: Global Error Handler
**목적**: 모든 Vue 에러를 중앙에서 처리

**구현**:
```javascript
// main.js
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err)
  console.error('Component:', instance)
  console.error('Info:', info)
  
  // 사용자 친화적 메시지 표시
  // (Toast 컴포넌트 사용)
}
```

**장점**:
- 중앙 집중식 에러 처리
- 일관된 에러 로깅

---

### Pattern 2.3: Axios Interceptor for Network Errors
**목적**: 네트워크 에러 자동 재시도 및 처리

**구현**:
```javascript
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000
})

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    const session = JSON.parse(localStorage.getItem('table_session') || '{}')
    if (session.sessionToken) {
      config.headers['X-Session-Token'] = session.sessionToken
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response Interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // 401 Unauthorized: 세션 만료
    if (error.response?.status === 401) {
      localStorage.removeItem('table_session')
      localStorage.removeItem('cart_items')
      window.location.href = '/login'
      return Promise.reject(new Error('세션이 만료되었습니다'))
    }

    // Network Error: 자동 재시도 1회
    if (!error.response && !error.config._retry) {
      error.config._retry = true
      await new Promise(resolve => setTimeout(resolve, 1000))
      return api.request(error.config)
    }

    // 사용자 친화적 에러 메시지
    const message = error.response?.data?.message || '네트워크 연결을 확인해주세요'
    return Promise.reject(new Error(message))
  }
)

export default api
```

**장점**:
- 자동 세션 토큰 추가
- 자동 재시도 (1회)
- 일관된 에러 처리

---

## 3. Security Patterns (보안 패턴)

### Pattern 3.1: Vue.js Auto-Escaping
**목적**: XSS 공격 방어

**구현**:
```vue
<!-- 안전: Vue.js가 자동으로 이스케이핑 -->
<div>{{ userInput }}</div>

<!-- 위험: v-html 사용 금지 -->
<!-- <div v-html="userInput"></div> -->
```

**규칙**:
- `v-html` 사용 금지
- 모든 사용자 입력은 `{{ }}` 또는 `:attribute`로 바인딩
- Vue.js의 자동 이스케이핑 신뢰

---

### Pattern 3.2: LocalStorage Security
**목적**: 세션 토큰 안전하게 저장

**구현**:
```javascript
// 저장
const saveSession = (session) => {
  localStorage.setItem('table_session', JSON.stringify(session))
}

// 로드
const loadSession = () => {
  try {
    const data = localStorage.getItem('table_session')
    return data ? JSON.parse(data) : null
  } catch (err) {
    console.error('Failed to load session:', err)
    return null
  }
}

// 삭제
const clearSession = () => {
  localStorage.removeItem('table_session')
  localStorage.removeItem('cart_items')
}
```

**보안 고려사항**:
- HTTPS 환경에서만 사용
- 민감 정보 암호화 안 함 (HTTPS로 충분)
- 세션 만료 시 자동 삭제

---

## 4. Usability Patterns (사용성 패턴)

### Pattern 4.1: Custom Toast Component
**목적**: 사용자 피드백 제공

**구현**:
```vue
<!-- components/shared/Toast.vue -->
<template>
  <Transition name="toast">
    <div v-if="visible" :class="toastClass">
      {{ message }}
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  message: String,
  type: { type: String, default: 'info' } // 'success', 'error', 'info'
})

const visible = ref(true)

const toastClass = computed(() => ({
  'toast': true,
  'toast-success': props.type === 'success',
  'toast-error': props.type === 'error',
  'toast-info': props.type === 'info'
}))

// 2초 후 자동 닫기 (success, info만)
if (props.type !== 'error') {
  setTimeout(() => { visible.value = false }, 2000)
}
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 9999;
}

.toast-success { background: #4CAF50; color: white; }
.toast-error { background: #F44336; color: white; }
.toast-info { background: #2196F3; color: white; }

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
```

**사용 예시**:
```javascript
// Composable
export const useToast = () => {
  const showToast = (message, type = 'info') => {
    // Toast 컴포넌트 동적 생성 및 표시
  }
  return { showToast }
}
```

---

### Pattern 4.2: Touch-Friendly UI
**목적**: 터치 디바이스 사용성 향상

**구현**:
```css
/* Tailwind CSS 설정 */
/* 모든 버튼 최소 44x44px */
.btn {
  @apply min-w-[44px] min-h-[44px] px-4 py-2;
}

/* 터치 영역 확대 */
.touch-target {
  @apply relative;
}

.touch-target::before {
  content: '';
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
}
```

**적용**:
- 모든 버튼, 링크, 카드
- 최소 44x44px 크기 보장

---

## 5. Maintainability Patterns (유지보수성 패턴)

### Pattern 5.1: Independent Pinia Stores
**목적**: Store 간 의존성 최소화

**구현**:
```javascript
// stores/auth.js
export const useAuthStore = defineStore('auth', () => {
  const session = ref(null)
  // 독립적 동작
  return { session }
})

// stores/cart.js
export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  // 독립적 동작, authStore 참조 안 함
  return { items }
})
```

**장점**:
- 간단한 구조
- 순환 참조 없음
- 테스트 용이

---

### Pattern 5.2: Composition API with `<script setup>`
**목적**: 간결한 컴포넌트 작성

**구현**:
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMenuStore } from '@/stores/menu'

const menuStore = useMenuStore()
const selectedCategory = ref(1)

const filteredMenus = computed(() => {
  return menuStore.menus.filter(m => m.categoryId === selectedCategory.value)
})

onMounted(() => {
  menuStore.loadMenus()
})
</script>
```

**장점**:
- 간결한 코드
- 타입 추론 우수
- 성능 최적화

---

## NFR Design Patterns Summary

| 카테고리 | 패턴 수 | 패턴 |
|---------|--------|------|
| Performance | 3 | Synchronous Loading, Eager Images, Simple Rendering |
| Availability | 3 | Individual Loading, Global Error Handler, Axios Interceptor |
| Security | 2 | Auto-Escaping, LocalStorage Security |
| Usability | 2 | Custom Toast, Touch-Friendly UI |
| Maintainability | 2 | Independent Stores, Composition API |
| **총계** | **12** | |

---

## Implementation Priority

### Priority 1 (필수)
1. Axios Interceptor (세션 토큰, 에러 처리)
2. Global Error Handler
3. LocalStorage Security
4. Independent Pinia Stores

### Priority 2 (권장)
5. Individual Loading States
6. Custom Toast Component
7. Touch-Friendly UI
8. Composition API

### Priority 3 (선택)
9. Synchronous Component Loading
10. Eager Image Loading
11. Simple List Rendering

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
