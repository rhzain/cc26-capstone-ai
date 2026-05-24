# Deploy to Railway (Frontend + Backend + AI Service)

Project structure:

```txt
repo/
├── frontend/
├── backend/
└── ai-service/
```

## 1. Create Railway Project

- Open Railway
- Click **New Project**
- Choose **Deploy from GitHub Repo**
- Select your repository

---

## 2. Create Services (Same Repo)

Add **3 services** using the **same GitHub repository**:

- Frontend
- Backend (Express)
- AI Service (FastAPI)

Go to:

```txt
+ New → GitHub Repo
```

Repeat until all 3 services exist.

---

## 3. Configure Each Service

### Frontend

Root Directory:

```txt
/frontend
```

Settings:
- Public Domain → **Enable**

Environment Variables:

```env
NEXT_PUBLIC_API_URL=https://<backend-public-domain>
```

---

### Backend (Express)

Root Directory:

```txt
/backend
```

Settings:
- Public Domain → **Enable**

Environment Variables:

```env
ML_SERVICE_URL=http://ai-service.railway.internal:8000
INTERNAL_API_TOKEN=<same-secret>
NEXT_APP_URL=https://<frontend-public-domain>
```

Backend can access FastAPI privately through:

```txt
http://ai-service.railway.internal:8000
```

---

### AI Service (FastAPI)

Root Directory:

```txt
/ai-service
```

Settings:
- Public Domain → **Disable**
  (AI service should not be accessible directly)

Environment Variables:

```env
PORT=8000
INTERNAL_API_TOKEN=<same-secret>
```

---

## 4. If Your Repo Has a Parent Folder

Example:

```txt
repo/
└── CuanSelor/
    ├── frontend/
    ├── backend/
    └── ai-service/
```

Use:

```txt
/CuanSelor/frontend
/CuanSelor/backend
/CuanSelor/ai-service
```

If folders are directly inside repo:

```txt
repo/
├── frontend/
├── backend/
└── ai-service/
```

Use:

```txt
/frontend
/backend
/ai-service
```

---

## Final Architecture

```txt
User
 ↓
Frontend (Public)
 ↓
Backend Express (Public)
 ↓ Railway Private Network
FastAPI AI Service (Private)
```

Flow:

```txt
Frontend → Backend → FastAPI
```

Users cannot access FastAPI directly.