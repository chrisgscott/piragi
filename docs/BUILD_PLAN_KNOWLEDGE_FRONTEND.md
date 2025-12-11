# Build Plan: Knowledge Management Frontend

## Overview
Build a dedicated `knowledge/` section in the Next.js frontend for managing piragi RAG content and settings. This section is separate from the main application UI and serves as an admin interface for knowledge base management.

---

## Architecture

```
app/
├── auth/                      # Public auth routes (login, signup, etc.)
├── (authenticated)/           # Route group with sidebar layout
│   ├── layout.tsx             # Sidebar + auth check
│   ├── chat/                  # Main chat interface
│   └── knowledge/             # Piragi admin section
│       ├── page.tsx           # Dashboard
│       ├── documents/         # Document CRUD
│       ├── graph/             # Knowledge graph viz
│       ├── search/            # Search playground
│       └── settings/          # Configuration
```

---

## PR 1: Knowledge Layout & Dashboard
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/layout.tsx` with sidebar navigation
- [ ] Create `app/knowledge/page.tsx` dashboard with:
  - [ ] Document count card
  - [ ] Index health status card
  - [ ] Recent activity card
  - [ ] Quick actions (upload, search, settings)
- [ ] Add navigation links: Documents, Graph, Search, Settings
- [ ] Style with existing shadcn sidebar component

### Components Used
- `sidebar`, `card`, `badge`, `button`

### API Endpoints Needed
- `GET /api/knowledge/stats` — dashboard metrics

---

## PR 2: Document Management - List View
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/documents/page.tsx`
- [ ] Implement data table with columns:
  - [ ] Title/filename
  - [ ] Source type (file, URL, text)
  - [ ] Chunk count
  - [ ] Created date
  - [ ] Status (indexed, pending, error)
- [ ] Add search/filter functionality
- [ ] Add bulk selection for delete
- [ ] Add pagination

### Components Used
- `table`, `command`, `checkbox`, `badge`, `dropdown-menu`, `pagination`

### API Endpoints Needed
- `GET /api/knowledge/documents` — list with pagination/filters
- `DELETE /api/knowledge/documents` — bulk delete

---

## PR 3: Document Management - Upload & Create
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/documents/upload/page.tsx`
- [ ] Implement file upload dropzone:
  - [ ] Support PDF, TXT, MD, DOCX, HTML
  - [ ] Drag & drop + click to browse
  - [ ] Multi-file upload
  - [ ] Upload progress indicator
- [ ] Implement URL ingestion form:
  - [ ] Single URL input
  - [ ] Crawl depth option (if crawler enabled)
- [ ] Implement raw text input:
  - [ ] Textarea for pasting content
  - [ ] Title/metadata fields
- [ ] Show processing status after upload

### Components Used
- `dialog`, `tabs`, `input`, `textarea`, `progress`, `form`, `button`

### API Endpoints Needed
- `POST /api/knowledge/documents/upload` — file upload
- `POST /api/knowledge/documents/url` — URL ingestion
- `POST /api/knowledge/documents/text` — raw text

---

## PR 4: Document Management - View & Edit
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/documents/[id]/page.tsx`
- [ ] Display document details:
  - [ ] Original content preview
  - [ ] Metadata (source, dates, etc.)
  - [ ] Chunk list with content preview
- [ ] Edit metadata functionality
- [ ] Re-index single document action
- [ ] Delete document with confirmation

### Components Used
- `card`, `tabs`, `accordion`, `alert-dialog`, `badge`, `scroll-area`

### API Endpoints Needed
- `GET /api/knowledge/documents/:id` — single document with chunks
- `PATCH /api/knowledge/documents/:id` — update metadata
- `POST /api/knowledge/documents/:id/reindex` — re-index
- `DELETE /api/knowledge/documents/:id` — delete single

---

## PR 5: Knowledge Graph Visualization
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/graph/page.tsx`
- [ ] Implement graph visualization with @xyflow/react:
  - [ ] Nodes = entities (documents, concepts, etc.)
  - [ ] Edges = relationships
  - [ ] Color coding by entity type
- [ ] Add node click to show details popover
- [ ] Add zoom/pan controls
- [ ] Add filter by entity type
- [ ] Add search to highlight specific nodes
- [ ] Handle empty state (graph not enabled)

### Components Used
- `@xyflow/react`, `popover`, `card`, `select`, `input`, `empty`

### API Endpoints Needed
- `GET /api/knowledge/graph` — nodes and edges data
- `GET /api/knowledge/graph/entity/:id` — entity details

---

## PR 5b: Graph Entity & Relationship Management
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/graph/entities/page.tsx`:
  - [ ] List all entities in table view
  - [ ] Filter by entity type
  - [ ] Search by name/content
  - [ ] Bulk delete for cleanup
  - [ ] Edit entity name/type
  - [ ] Merge duplicate entities
- [ ] Create `app/knowledge/graph/relationships/page.tsx`:
  - [ ] List all relationships in table view
  - [ ] Filter by relationship type
  - [ ] Filter by source/target entity
  - [ ] Delete individual relationships
  - [ ] Bulk delete for cleanup
  - [ ] Edit relationship type/weight
- [ ] Add navigation tabs: Visualization | Entities | Relationships

### Components Used
- `table`, `tabs`, `command`, `dialog`, `alert-dialog`, `dropdown-menu`, `badge`, `checkbox`

### API Endpoints Needed
- `GET /api/knowledge/graph/entities` — list with filters
- `PATCH /api/knowledge/graph/entities/:id` — update entity
- `DELETE /api/knowledge/graph/entities` — bulk delete
- `POST /api/knowledge/graph/entities/merge` — merge duplicates
- `GET /api/knowledge/graph/relationships` — list with filters
- `PATCH /api/knowledge/graph/relationships/:id` — update relationship
- `DELETE /api/knowledge/graph/relationships` — bulk delete

---

## PR 6: Search Playground
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/search/page.tsx`
- [ ] Implement search interface:
  - [ ] Query input with submit
  - [ ] Top-K slider (1-20)
  - [ ] Search type toggle (semantic, hybrid, keyword)
- [ ] Display raw results:
  - [ ] Content snippet
  - [ ] Similarity score
  - [ ] Source document link
  - [ ] Metadata
- [ ] Show query timing/performance
- [ ] Export results option

### Components Used
- `prompt-input`, `slider`, `toggle-group`, `card`, `sources`, `inline-citation`, `badge`

### API Endpoints Needed
- `POST /api/knowledge/search` — search with options

---

## PR 7: Settings - General & Embeddings
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/settings/page.tsx` with tabs layout
- [ ] Create `app/knowledge/settings/embeddings/page.tsx`:
  - [ ] Model selection (local, OpenAI, custom)
  - [ ] Model name input
  - [ ] Dimension display
  - [ ] Test embedding button
- [ ] General settings:
  - [ ] Persist directory path
  - [ ] Auto-update toggle
  - [ ] Change detection interval

### Components Used
- `tabs`, `form`, `select`, `input`, `switch`, `button`, `card`

### API Endpoints Needed
- `GET /api/knowledge/settings` — current config
- `PATCH /api/knowledge/settings` — update config

---

## PR 8: Settings - Chunking & Stores
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Create `app/knowledge/settings/chunking/page.tsx`:
  - [ ] Strategy selection (fixed, semantic, sentence)
  - [ ] Chunk size slider
  - [ ] Overlap slider
  - [ ] Preview chunking on sample text
- [ ] Create `app/knowledge/settings/stores/page.tsx`:
  - [ ] Store type selection (lance, supabase, pinecone, postgres)
  - [ ] Connection config per store type
  - [ ] Test connection button
  - [ ] Migration tools (if switching stores)

### Components Used
- `form`, `select`, `slider`, `textarea`, `button`, `alert`, `card`

### API Endpoints Needed
- `POST /api/knowledge/settings/chunking/preview` — preview chunks
- `POST /api/knowledge/settings/stores/test` — test connection

---

## PR 9: API Routes Implementation
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Implement all API routes in FastAPI backend:
  - [ ] `/api/knowledge/stats`
  - [ ] `/api/knowledge/documents` (CRUD)
  - [ ] `/api/knowledge/graph`
  - [ ] `/api/knowledge/search`
  - [ ] `/api/knowledge/settings`
- [ ] Add proper error handling
- [ ] Add request validation with Pydantic
- [ ] Connect to piragi library

### Files to Modify
- `api/routes/` — add knowledge routes
- `api/services/` — add knowledge service

---

## PR 10: Integration & Polish
**Suggested Model:** Claude Sonnet 4

### Tasks
- [ ] Add loading states to all pages
- [ ] Add error boundaries
- [ ] Add empty states with helpful CTAs
- [ ] Add toast notifications for actions
- [ ] Add keyboard shortcuts (cmd+k for search)
- [ ] Responsive design for mobile
- [ ] Add breadcrumbs navigation

### Components Used
- `skeleton`, `sonner`, `empty`, `breadcrumb`, `command`

---

## Dependencies

### Frontend (already installed)
- `@xyflow/react` — graph visualization
- `recharts` — charts for dashboard
- `ai` — streaming support
- All shadcn/ui components

### Backend (already in pyproject.toml)
- `fastapi`, `uvicorn`
- `piragi` (lib/)

---

## Notes
- All knowledge/ routes should be protected (admin only)
- Consider adding role-based access later
- Graph visualization only shows if `graph` extra is enabled in piragi
- Settings changes may require re-indexing — warn user

