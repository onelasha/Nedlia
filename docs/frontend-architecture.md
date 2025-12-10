# Frontend Architecture

Clean Architecture implementation for Nedlia's web portal (React + TypeScript).

## Principles

1. **Dependency Rule**: Dependencies point inward (UI → Application → Domain)
2. **Domain Independence**: Business logic has no framework dependencies
3. **Testability**: Each layer can be tested in isolation
4. **Consistency**: Mirrors backend Clean Architecture for unified mental model

---

## Layer Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         UI Layer                            │
│         (React components, pages, hooks, styles)            │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                        │
│           (Use cases, state management, DTOs)               │
├─────────────────────────────────────────────────────────────┤
│                  Infrastructure Layer                       │
│         (API clients, storage, auth providers)              │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                           │
│      (Entities, value objects, business rules)              │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Direction

```
UI → Application → Domain ← Infrastructure
                     ↑
            Infrastructure implements
            interfaces defined in Domain
```

---

## Folder Structure

```
nedlia-front-end/portal/src/
├── domain/                    # Pure business logic (no React, no external deps)
│   ├── placement/
│   │   ├── Placement.ts       # Entity type/interface
│   │   ├── PlacementStatus.ts # Value object (enum)
│   │   ├── TimeRange.ts       # Value object
│   │   ├── placementRules.ts  # Business rules, validation
│   │   └── index.ts           # Public exports
│   ├── video/
│   ├── campaign/
│   ├── user/
│   └── shared/                # Cross-domain types
│       ├── Entity.ts          # Base entity interface
│       ├── Result.ts          # Result type for error handling
│       └── index.ts
│
├── application/               # Use cases, orchestration
│   ├── placement/
│   │   ├── useCases/
│   │   │   ├── createPlacement.ts
│   │   │   ├── updatePlacement.ts
│   │   │   ├── deletePlacement.ts
│   │   │   └── validatePlacement.ts
│   │   ├── queries/
│   │   │   ├── getPlacement.ts
│   │   │   └── listPlacements.ts
│   │   ├── dto/               # Data Transfer Objects
│   │   │   ├── PlacementCreateDTO.ts
│   │   │   └── PlacementResponseDTO.ts
│   │   └── index.ts
│   ├── video/
│   ├── campaign/
│   ├── auth/
│   │   ├── useCases/
│   │   │   ├── login.ts
│   │   │   ├── logout.ts
│   │   │   └── refreshToken.ts
│   │   └── index.ts
│   └── ports/                 # Interfaces for infrastructure
│       ├── PlacementRepository.ts
│       ├── VideoRepository.ts
│       ├── AuthService.ts
│       └── StorageService.ts
│
├── infrastructure/            # External world implementations
│   ├── api/
│   │   ├── client.ts          # HTTP client setup (axios/fetch)
│   │   ├── interceptors.ts    # Auth, error handling
│   │   ├── placementApi.ts    # Implements PlacementRepository
│   │   ├── videoApi.ts
│   │   └── campaignApi.ts
│   ├── auth/
│   │   └── cognitoAuth.ts     # Implements AuthService
│   ├── storage/
│   │   └── localStorage.ts    # Implements StorageService
│   └── index.ts
│
├── ui/                        # React layer
│   ├── components/            # Reusable UI components
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Modal/
│   │   ├── DataTable/
│   │   └── index.ts
│   ├── pages/                 # Route-level components
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DashboardStats.tsx
│   │   │   └── index.ts
│   │   ├── Placements/
│   │   │   ├── PlacementList.tsx
│   │   │   ├── PlacementDetail.tsx
│   │   │   ├── PlacementForm.tsx
│   │   │   └── index.ts
│   │   ├── Videos/
│   │   └── Campaigns/
│   ├── layouts/
│   │   ├── MainLayout.tsx
│   │   ├── AuthLayout.tsx
│   │   └── index.ts
│   ├── hooks/                 # React hooks (UI-specific)
│   │   ├── usePlacements.ts   # Wraps application layer
│   │   ├── useVideos.ts
│   │   ├── useAuth.ts
│   │   └── useToast.ts
│   ├── providers/             # React context providers
│   │   ├── AuthProvider.tsx
│   │   ├── QueryProvider.tsx
│   │   └── ThemeProvider.tsx
│   ├── router/
│   │   ├── routes.tsx
│   │   └── ProtectedRoute.tsx
│   └── styles/
│       └── globals.css
│
├── shared/                    # Cross-cutting concerns
│   ├── utils/
│   │   ├── formatDate.ts
│   │   ├── formatCurrency.ts
│   │   └── cn.ts              # Tailwind class merge
│   ├── constants/
│   │   └── routes.ts
│   ├── types/
│   │   └── api.ts             # Generic API types
│   └── config/
│       └── env.ts
│
├── App.tsx
├── main.tsx
└── index.css
```

---

## Layer Details

### Domain Layer

**Purpose**: Pure business logic with zero external dependencies.

**Contains**:

- Entity types and interfaces
- Value objects
- Business rules and validation
- Domain errors

**Rules**:

- No React imports
- No external library imports (except pure utilities like `uuid`)
- No API calls or side effects
- Can be shared with backend if needed

```typescript
// domain/placement/Placement.ts
export interface Placement {
  id: string;
  videoId: string;
  productId: string;
  timeRange: TimeRange;
  status: PlacementStatus;
  description: string;
  createdAt: Date;
  updatedAt: Date;
}

// domain/placement/TimeRange.ts
export interface TimeRange {
  startTime: number;
  endTime: number;
}

export function isValidTimeRange(range: TimeRange): boolean {
  return range.startTime >= 0 && range.endTime > range.startTime;
}

// domain/placement/PlacementStatus.ts
export enum PlacementStatus {
  Draft = 'draft',
  Active = 'active',
  Archived = 'archived',
}

// domain/placement/placementRules.ts
import { Placement, TimeRange, isValidTimeRange } from './index';

export function canActivatePlacement(placement: Placement): boolean {
  return (
    placement.status === PlacementStatus.Draft &&
    isValidTimeRange(placement.timeRange) &&
    placement.description.length > 0
  );
}

export function doTimeRangesOverlap(a: TimeRange, b: TimeRange): boolean {
  return a.startTime < b.endTime && b.startTime < a.endTime;
}
```

### Application Layer

**Purpose**: Orchestrates use cases, manages application state.

**Contains**:

- Use cases (commands)
- Queries
- DTOs (Data Transfer Objects)
- Port interfaces (for infrastructure)

**Rules**:

- Can import from Domain
- Cannot import from UI or Infrastructure implementations
- Defines interfaces (ports) that Infrastructure implements

```typescript
// application/ports/PlacementRepository.ts
import { Placement } from '../../domain/placement';

export interface PlacementRepository {
  findById(id: string): Promise<Placement | null>;
  findByVideoId(videoId: string): Promise<Placement[]>;
  save(placement: Placement): Promise<Placement>;
  delete(id: string): Promise<void>;
}

// application/placement/useCases/createPlacement.ts
import { Placement, PlacementStatus, isValidTimeRange } from '../../../domain/placement';
import { PlacementRepository } from '../../ports/PlacementRepository';
import { PlacementCreateDTO } from '../dto/PlacementCreateDTO';

export class CreatePlacementUseCase {
  constructor(private repository: PlacementRepository) {}

  async execute(dto: PlacementCreateDTO): Promise<Placement> {
    // Validate business rules
    if (!isValidTimeRange(dto.timeRange)) {
      throw new Error('Invalid time range');
    }

    // Check for overlapping placements
    const existing = await this.repository.findByVideoId(dto.videoId);
    const hasOverlap = existing.some(p => doTimeRangesOverlap(p.timeRange, dto.timeRange));

    if (hasOverlap) {
      throw new Error('Time range overlaps with existing placement');
    }

    // Create and save
    const placement: Placement = {
      id: crypto.randomUUID(),
      ...dto,
      status: PlacementStatus.Draft,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    return this.repository.save(placement);
  }
}

// application/placement/dto/PlacementCreateDTO.ts
import { TimeRange } from '../../../domain/placement';

export interface PlacementCreateDTO {
  videoId: string;
  productId: string;
  timeRange: TimeRange;
  description: string;
}
```

### Infrastructure Layer

**Purpose**: Implements interfaces defined in Application layer.

**Contains**:

- API clients
- Authentication providers
- Storage implementations
- External service integrations

**Rules**:

- Implements ports from Application layer
- Can import from Domain and Application
- Cannot import from UI

```typescript
// infrastructure/api/client.ts
import axios from 'axios';
import { env } from '../../shared/config/env';

export const apiClient = axios.create({
  baseURL: env.API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// infrastructure/api/placementApi.ts
import { Placement } from '../../domain/placement';
import { PlacementRepository } from '../../application/ports/PlacementRepository';
import { apiClient } from './client';

export class PlacementApiRepository implements PlacementRepository {
  async findById(id: string): Promise<Placement | null> {
    try {
      const response = await apiClient.get<Placement>(`/placements/${id}`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) return null;
      throw error;
    }
  }

  async findByVideoId(videoId: string): Promise<Placement[]> {
    const response = await apiClient.get<Placement[]>(`/videos/${videoId}/placements`);
    return response.data;
  }

  async save(placement: Placement): Promise<Placement> {
    if (placement.id) {
      const response = await apiClient.put<Placement>(`/placements/${placement.id}`, placement);
      return response.data;
    }
    const response = await apiClient.post<Placement>('/placements', placement);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/placements/${id}`);
  }
}
```

### UI Layer

**Purpose**: React components, pages, and UI-specific logic.

**Contains**:

- React components
- Pages (route-level components)
- Layouts
- React hooks
- Context providers
- Router configuration

**Rules**:

- Can import from all layers
- Components should be thin (delegate to hooks)
- Hooks bridge UI and Application layers

```typescript
// ui/hooks/usePlacements.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PlacementApiRepository } from '../../infrastructure/api/placementApi';
import { CreatePlacementUseCase } from '../../application/placement/useCases/createPlacement';
import { PlacementCreateDTO } from '../../application/placement/dto/PlacementCreateDTO';

const repository = new PlacementApiRepository();
const createUseCase = new CreatePlacementUseCase(repository);

export function usePlacements(videoId: string) {
  return useQuery({
    queryKey: ['placements', videoId],
    queryFn: () => repository.findByVideoId(videoId),
  });
}

export function useCreatePlacement() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (dto: PlacementCreateDTO) => createUseCase.execute(dto),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['placements', variables.videoId] });
    },
  });
}

// ui/pages/Placements/PlacementList.tsx
import { usePlacements } from '../../hooks/usePlacements';
import { DataTable } from '../../components/DataTable';
import { PlacementStatus } from '../../../domain/placement';

interface PlacementListProps {
  videoId: string;
}

export function PlacementList({ videoId }: PlacementListProps) {
  const { data: placements, isLoading, error } = usePlacements(videoId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading placements</div>;

  return (
    <DataTable
      data={placements}
      columns={[
        { key: 'description', header: 'Description' },
        { key: 'status', header: 'Status' },
        {
          key: 'timeRange',
          header: 'Time Range',
          render: p => `${p.timeRange.startTime}s - ${p.timeRange.endTime}s`,
        },
      ]}
    />
  );
}
```

---

## Dependency Injection

### Simple Approach (Recommended for Start)

```typescript
// infrastructure/index.ts
import { PlacementApiRepository } from './api/placementApi';
import { VideoApiRepository } from './api/videoApi';
import { CognitoAuthService } from './auth/cognitoAuth';

// Create singleton instances
export const placementRepository = new PlacementApiRepository();
export const videoRepository = new VideoApiRepository();
export const authService = new CognitoAuthService();
```

```typescript
// ui/hooks/usePlacements.ts
import { placementRepository } from '../../infrastructure';
import { CreatePlacementUseCase } from '../../application/placement/useCases/createPlacement';

const createUseCase = new CreatePlacementUseCase(placementRepository);
```

### Context-Based DI (For Testing)

```typescript
// ui/providers/RepositoryProvider.tsx
import { createContext, useContext, ReactNode } from 'react';
import { PlacementRepository } from '../../application/ports/PlacementRepository';
import { placementRepository } from '../../infrastructure';

interface Repositories {
  placement: PlacementRepository;
}

const RepositoryContext = createContext<Repositories | null>(null);

export function RepositoryProvider({
  children,
  overrides = {},
}: {
  children: ReactNode;
  overrides?: Partial<Repositories>;
}) {
  const repositories: Repositories = {
    placement: overrides.placement ?? placementRepository,
  };

  return <RepositoryContext.Provider value={repositories}>{children}</RepositoryContext.Provider>;
}

export function useRepositories() {
  const context = useContext(RepositoryContext);
  if (!context) throw new Error('Must be used within RepositoryProvider');
  return context;
}
```

---

## Testing Strategy

### Domain Layer (Unit Tests)

```typescript
// domain/placement/__tests__/placementRules.test.ts
import { canActivatePlacement, doTimeRangesOverlap } from '../placementRules';

describe('placementRules', () => {
  describe('doTimeRangesOverlap', () => {
    it('returns true for overlapping ranges', () => {
      expect(
        doTimeRangesOverlap({ startTime: 0, endTime: 10 }, { startTime: 5, endTime: 15 })
      ).toBe(true);
    });

    it('returns false for non-overlapping ranges', () => {
      expect(
        doTimeRangesOverlap({ startTime: 0, endTime: 10 }, { startTime: 10, endTime: 20 })
      ).toBe(false);
    });
  });
});
```

### Application Layer (Unit Tests with Mocks)

```typescript
// application/placement/useCases/__tests__/createPlacement.test.ts
import { CreatePlacementUseCase } from '../createPlacement';
import { PlacementRepository } from '../../../ports/PlacementRepository';

describe('CreatePlacementUseCase', () => {
  const mockRepository: PlacementRepository = {
    findById: jest.fn(),
    findByVideoId: jest.fn().mockResolvedValue([]),
    save: jest.fn().mockImplementation(p => Promise.resolve(p)),
    delete: jest.fn(),
  };

  it('creates placement when no overlap exists', async () => {
    const useCase = new CreatePlacementUseCase(mockRepository);

    const result = await useCase.execute({
      videoId: 'video-1',
      productId: 'product-1',
      timeRange: { startTime: 0, endTime: 10 },
      description: 'Test placement',
    });

    expect(result.status).toBe('draft');
    expect(mockRepository.save).toHaveBeenCalled();
  });
});
```

### UI Layer (Integration Tests)

```typescript
// ui/pages/Placements/__tests__/PlacementList.test.tsx
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RepositoryProvider } from '../../../providers/RepositoryProvider';
import { PlacementList } from '../PlacementList';

const mockRepository = {
  findByVideoId: jest
    .fn()
    .mockResolvedValue([
      { id: '1', description: 'Test', status: 'draft', timeRange: { startTime: 0, endTime: 10 } },
    ]),
};

test('renders placements', async () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <RepositoryProvider overrides={{ placement: mockRepository }}>
        <PlacementList videoId="video-1" />
      </RepositoryProvider>
    </QueryClientProvider>
  );

  expect(await screen.findByText('Test')).toBeInTheDocument();
});
```

---

## Import Rules

Enforce with ESLint `import/no-restricted-paths`:

```javascript
// eslint.config.js
{
  rules: {
    'import/no-restricted-paths': ['error', {
      zones: [
        // Domain cannot import from other layers
        {
          target: './src/domain',
          from: './src/application',
          message: 'Domain cannot import from Application',
        },
        {
          target: './src/domain',
          from: './src/infrastructure',
          message: 'Domain cannot import from Infrastructure',
        },
        {
          target: './src/domain',
          from: './src/ui',
          message: 'Domain cannot import from UI',
        },
        // Application cannot import from UI or Infrastructure implementations
        {
          target: './src/application',
          from: './src/ui',
          message: 'Application cannot import from UI',
        },
        {
          target: './src/application',
          from: './src/infrastructure',
          message: 'Application cannot import from Infrastructure (use ports)',
        },
        // Infrastructure cannot import from UI
        {
          target: './src/infrastructure',
          from: './src/ui',
          message: 'Infrastructure cannot import from UI',
        },
      ],
    }],
  },
}
```

---

## State Management

### Recommended: React Query + Context

| Concern         | Solution                     |
| --------------- | ---------------------------- |
| Server state    | React Query (TanStack Query) |
| Global UI state | React Context + useReducer   |
| Form state      | React Hook Form              |
| URL state       | React Router                 |

```typescript
// ui/providers/index.tsx
export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <ToastProvider>{children}</ToastProvider>
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

---

## Related Documentation

- [Architecture Overview](../ARCHITECTURE.md) – System-wide architecture
- [TypeScript Style Guide](typescript-style-guide.md) – Coding standards
- [Testing Strategy](testing-strategy.md) – Testing patterns
- [Dependency Injection](dependency-injection.md) – DI patterns
- [API Standards](api-standards.md) – Backend API contracts
