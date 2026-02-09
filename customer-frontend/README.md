# TableOrder Customer Frontend

테이블오더 서비스의 고객용 프론트엔드 애플리케이션입니다.

## Tech Stack

- **Framework**: Vue.js 3.4+
- **Build Tool**: Vite 5.0+
- **State Management**: Pinia 2.1+
- **Routing**: Vue Router 4.2+
- **HTTP Client**: Axios 1.6+
- **Styling**: Tailwind CSS 3.4+
- **Icons**: Heroicons
- **Testing**: Vitest 1.0+

## Features

- 테이블 자동 로그인 (LocalStorage 기반)
- 메뉴 조회 및 카테고리별 탐색
- 장바구니 관리 (LocalStorage 동기화)
- 주문 생성 및 확인
- 주문 내역 조회

## Project Structure

```
customer-frontend/
├── public/
│   └── images/
├── src/
│   ├── main.js                 # Entry point
│   ├── App.vue                 # Root component
│   ├── router/                 # Vue Router configuration
│   ├── stores/                 # Pinia stores
│   │   ├── auth.js
│   │   ├── menu.js
│   │   ├── cart.js
│   │   ├── order.js
│   │   └── toast.js
│   ├── views/                  # Page components
│   │   ├── LoginView.vue
│   │   ├── MenuView.vue
│   │   ├── CartView.vue
│   │   └── OrderHistoryView.vue
│   ├── components/             # Reusable components
│   │   ├── shared/
│   │   ├── CategoryTabs.vue
│   │   ├── MenuCard.vue
│   │   ├── CartItem.vue
│   │   └── OrderCard.vue
│   ├── services/               # API services
│   │   └── api.js
│   ├── composables/            # Composable functions
│   │   ├── useToast.js
│   │   └── useAuth.js
│   └── assets/                 # Static assets
│       └── main.css
├── tests/                      # Test files
├── .env.development            # Development environment variables
├── .env.production             # Production environment variables
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Setup

### Prerequisites

- Node.js 20.x or higher
- npm 10.x or higher

### Installation

```bash
# Install dependencies
npm install
```

### Environment Variables

Create `.env.development` and `.env.production` files based on `.env.example`:

```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

## Development

```bash
# Start development server
npm run dev

# Access at http://localhost:5173
```

## Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Testing

```bash
# Run tests
npm run test

# Run tests in watch mode
npm run test:watch
```

## Linting

```bash
# Run ESLint
npm run lint
```

## API Integration

The application communicates with the backend API at `VITE_API_URL`.

### API Endpoints

- `POST /api/auth/table-login` - Table login
- `GET /api/menus?store_id={storeId}` - Get menus
- `POST /api/orders` - Create order
- `GET /api/orders` - Get order history

### Authentication

Session token is stored in LocalStorage and automatically added to API requests via Axios interceptor.

## LocalStorage

The application uses LocalStorage for:

- `table_session` - Table session information
- `cart_items` - Shopping cart items

## Deployment

See `aidlc-docs/construction/customer-frontend/infrastructure-design/deployment-architecture.md` for deployment instructions.

### Quick Deploy (AWS S3 + CloudFront)

```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths "/*"
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
