# PRD: ML Optimization Service

**Product Requirements Document**

| Field | Value |
|-------|-------|
| **Product Name** | AutoTune ML (placeholder) |
| **Status** | Draft |
| **Author** | [Your Name] |
| **Created** | 2026-03-13 |
| **Target Launch** | Q2 2026 (MVP) |

---

## 1. Executive Summary

### Vision

Enable anyone to train optimized machine learning models without ML expertise. Users upload their text data, and our service automatically runs dozens of experiments to find the best model configuration for their specific use case.

### Mission

Democratize ML model optimization by automating the tedious experimentation process that typically requires PhD-level knowledge and weeks of manual tuning.

### Success Metric

**Primary:** 1,000 models trained in first 3 months, with 70%+ user satisfaction rating.

---

## 2. Problem Statement

### Current State

| Pain Point | Who Suffers | Impact |
|------------|-------------|--------|
| ML expertise required | Startups, SMBs | Can't leverage custom models |
| Manual tuning takes weeks | Data scientists | Slow iteration, wasted time |
| Compute expensive | Researchers, students | Limited experimentation |
| No systematic approach | Teams | Inconsistent results, no reproducibility |
| Hiring ML engineers hard | Non-tech companies | Delayed or abandoned ML projects |

### User Quotes (Hypothetical)

> "We have years of customer support tickets but no idea how to build a model from them."
> — Startup founder

> "I spend 80% of my time tuning hyperparameters instead of building features."
> — Solo data scientist

> "We can't afford a full ML team but need domain-specific AI."
> — SMB CTO

### Market Opportunity

| Segment | Size | Pain Level |
|---------|------|------------|
| Startups without ML team | ~100K globally | High |
| SMBs wanting custom AI | ~1M+ in US | High |
| Individual data scientists | ~500K globally | Medium |
| Researchers/Students | ~5M globally | Medium |
| Enterprise teams | ~50K globally | Low (have resources) |

---

## 3. Target Users

### Primary Personas

#### Persona 1: Startup Founder (Alex)

| Attribute | Details |
|-----------|---------|
| **Role** | Founder/CEO of 5-person startup |
| **Technical** | Can code, not an ML expert |
| **Goal** | Add AI features to product quickly |
| **Constraint** | No budget for ML hire, limited time |
| **Use Case** | Train model on customer feedback for auto-categorization |
| **Willingness to Pay** | $50-200/month |

#### Persona 2: Solo Data Scientist (Jordan)

| Attribute | Details |
|-----------|---------|
| **Role** | Only data scientist at mid-size company |
| **Technical** | ML proficient, overworked |
| **Goal** | Ship models faster, reduce manual tuning |
| **Constraint** | Limited compute budget, many stakeholders |
| **Use Case** | Optimize existing model, find better architecture |
| **Willingness to Pay** | $100-500/month or per-experiment |

#### Persona 3: Researcher (Sam)

| Attribute | Details |
|-----------|---------|
| **Role** | PhD student or academic researcher |
| **Technical** | ML knowledgeable, compute-limited |
| **Goal** | Run many experiments for paper/research |
| **Constraint** | Grant budget, needs reproducibility |
| **Use Case** | Benchmark different approaches systematically |
| **Willingness to Pay** | $20-50/month (student budget) |

#### Persona 4: Enterprise ML Lead (Morgan)

| Attribute | Details |
|-----------|---------|
| **Role** | ML engineering lead at 500+ person company |
| **Technical** | Expert, manages team |
| **Goal** | Accelerate team's experimentation |
| **Constraint** | Needs auditability, compliance |
| **Use Case** | Standardize experimentation process |
| **Willingness to Pay** | $1,000+/month for team features |

### User Journey (Alex - Startup Founder)

```
1. Discover → Find AutoTune via search, Twitter, HN
2. Try → Upload sample dataset, run free experiment
3. Value → See better results than expected, get hooked
4. Convert → Subscribe for more experiments
5. Scale → Train production model, integrate into product
6. Expand → Add more datasets, invite team members
7. Advocate → Recommend to other founders
```

---

## 4. Solution Overview

### Core Value Proposition

**"Upload data → We run 100 experiments → You get the best model"**

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER JOURNEY                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. UPLOAD DATA          2. CONFIGURE         3. RUN EXPERIMENTS │
│  ┌─────────────┐        ┌─────────────┐       ┌─────────────┐   │
│  │ Drag & drop │───────▶│ Set budget  │──────▶│ Watch live  │   │
│  │ .txt, .csv  │        │ Pick GPU    │       │ progress    │   │
│  │ .json, .zip │        │ Set time    │       │ metrics     │   │
│  └─────────────┘        └─────────────┘       └─────────────┘   │
│                                                      │          │
│                                                      ▼          │
│  4. REVIEW RESULTS       5. DOWNLOAD MODEL                        │
│  ┌─────────────┐        ┌─────────────┐                         │
│  │ Best config │        │ .pt weights │                         │
│  │ All history │        │ Tokenizer   │                         │
│  │ Comparison  │        │ Config file │                         │
│  └─────────────┘        └─────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Differentiators

| Feature | Us | Competitors |
|---------|-----|-------------|
| **Setup time** | 5 minutes | Hours to days |
| **ML expertise required** | None | Significant |
| **Experiments run** | 50-100+ automatically | Manual, 5-10 |
| **Time to best model** | Hours | Weeks |
| **Price** | $0.50/experiment | $100s/month + compute |

---

## 5. Functional Requirements

### MVP Features (Phase 1)

#### F1: Data Upload

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Upload .txt files | P0 | Core functionality |
| Upload .csv with text column | P0 | Common format |
| Upload .json with text field | P1 | API data |
| Upload .zip of files | P1 | Bulk upload |
| Max file size 100MB | P0 | Free tier limit |
| Max file size 1GB | P1 | Paid tier |
| Data validation | P0 | Check format, warn on issues |
| PII detection warning | P1 | Privacy awareness |

#### F2: Experiment Configuration

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Simple mode (one click) | P0 | Sensible defaults |
| Advanced mode | P1 | Tune hyperparameters |
| Set compute budget | P0 | Time or cost limit |
| Choose GPU type | P1 | T4, A100, etc. |
| Set experiment count | P1 | How many experiments |
| Schedule runs | P2 | Run overnight |

#### F3: Experiment Execution

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Run autoresearch loop | P0 | Core engine |
| Real-time progress | P0 | User sees updates |
| Live metrics display | P0 | Loss, val_bpb, etc. |
| Early stopping | P1 | Kill bad experiments |
| Parallel experiments | P1 | Multiple GPUs |
| Resume interrupted runs | P2 | Handle failures |

#### F4: Results & Analysis

| Requirement | Priority | Notes |
|-------------|----------|-------|
| View all experiments | P0 | Table with key metrics |
| Sort by val_bpb | P0 | Find best model |
| Compare experiments | P1 | Side-by-side diff |
| Download results CSV | P0 | Export data |
| Experiment timeline | P2 | Visual progress |

#### F5: Model Export

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Download .pt weights | P0 | PyTorch format |
| Download tokenizer | P0 | Match model |
| Download config | P0 | Reproduce training |
| Export to ONNX | P1 | Cross-platform |
| Export to HuggingFace | P2 | One-click push |

#### F6: User Management

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Email signup | P0 | Basic auth |
| Google OAuth | P1 | Frictionless |
| Usage dashboard | P0 | Experiments run, remaining |
| Billing history | P1 | Invoice download |

### Phase 2 Features (Growth)

| Feature | Description | Priority |
|---------|-------------|----------|
| **Inference API** | Hosted endpoint for model | P1 |
| **Team workspaces** | Shared experiments | P1 |
| **Custom datasets** | Save datasets for reuse | P1 |
| **Experiment templates** | Save configurations | P2 |
| **Webhooks** | Notify on completion | P2 |
| **API access** | Programmatic control | P1 |
| **Model versioning** | Track model history | P2 |
| **Collaboration** | Comments, sharing | P2 |

### Phase 3 Features (Scale)

| Feature | Description | Priority |
|---------|-------------|----------|
| **Enterprise SSO** | SAML, Okta | P1 |
| **On-premise** | Self-hosted option | P1 |
| **Custom models** | Beyond GPT architecture | P2 |
| **Multi-modal** | Images, audio | P2 |
| **Auto-deployment** | Push to cloud providers | P2 |
| **White-label** | Resell under own brand | P2 |

---

## 6. Non-Functional Requirements

### Performance

| Requirement | Target |
|-------------|--------|
| Page load time | < 2 seconds |
| API response time | < 200ms (p99) |
| Experiment start time | < 30 seconds from submission |
| Concurrent users | 1,000 (MVP), 10,000+ (scale) |
| Concurrent experiments | 100 (MVP), 1,000+ (scale) |

### Reliability

| Requirement | Target |
|-------------|--------|
| Uptime | 99.5% (MVP), 99.9% (production) |
| Data durability | 99.99% (S3-level) |
| Experiment success rate | > 95% |
| Recovery time | < 1 hour |

### Security

| Requirement | Details |
|-------------|---------|
| Data encryption | At rest (AES-256), in transit (TLS 1.3) |
| Authentication | JWT with secure tokens |
| Authorization | Role-based access control |
| Data retention | User-configurable, default 30 days |
| GDPR compliance | Data deletion on request |
| SOC 2 | Target for enterprise |

### Scalability

| Component | Approach |
|-----------|----------|
| Frontend | Stateless, CDN |
| API | Horizontal scaling |
| Workers | Auto-scaling based on queue |
| Database | Read replicas, connection pooling |
| Storage | S3/GCS, unlimited |

---

## 7. Technical Architecture

### System Overview

```
                              ┌─────────────────┐
                              │   CloudFlare    │
                              │   (CDN/DDoS)    │
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │   Load Balancer │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
           ┌────────▼────────┐                ┌──────────▼────────┐
           │   API Servers   │                │   Web Frontend    │
           │   (FastAPI)     │                │   (React/Next.js) │
           └────────┬────────┘                └───────────────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
┌────▼────┐  ┌─────▼──────┐  ┌────▼────┐
│ PostgreSQL │  │   Redis    │  │  S3/GCS │
│  (Data)    │  │  (Queue)   │  │(Models) │
└───────────┘  └─────┬──────┘  └─────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌────▼────┐
    │ Worker  │ │ Worker │ │ Worker  │
    │ (GPU 1) │ │(GPU 2) │ │(GPU N)  │
    └─────────┘ └────────┘ └─────────┘
```

### Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Frontend** | Next.js + TypeScript | Fast, SEO-friendly, React ecosystem |
| **API** | FastAPI (Python) | Async, ML ecosystem, fast development |
| **Database** | PostgreSQL | Reliable, relational data, extensions |
| **Queue** | Redis + Celery | Proven, Python-native |
| **Storage** | S3 or GCS | Scalable, durable |
| **Workers** | Docker containers | Isolation, reproducibility |
| **GPU** | AWS/GCP spot instances | Cost optimization |
| **Monitoring** | Prometheus + Grafana | Industry standard |
| **Logging** | Loki or CloudWatch | Centralized logs |

### Data Model

```sql
-- Core tables
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    plan VARCHAR(50) DEFAULT 'free'
);

CREATE TABLE datasets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(255),
    file_path VARCHAR(500),
    size_bytes BIGINT,
    row_count INTEGER,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    dataset_id UUID REFERENCES datasets(id),
    status VARCHAR(50), -- pending, running, completed, failed
    config JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE experiments (
    id UUID PRIMARY KEY,
    job_id UUID REFERENCES jobs(id),
    commit_hash VARCHAR(50),
    val_bpb FLOAT,
    memory_gb FLOAT,
    status VARCHAR(50), -- keep, discard, crash
    description TEXT,
    config JSONB,
    metrics JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE models (
    id UUID PRIMARY KEY,
    experiment_id UUID REFERENCES experiments(id),
    storage_path VARCHAR(500),
    format VARCHAR(50), -- pytorch, onnx
    size_bytes BIGINT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Design (REST)

```
# Authentication
POST   /auth/signup
POST   /auth/login
POST   /auth/logout

# Datasets
GET    /datasets
POST   /datasets
GET    /datasets/{id}
DELETE /datasets/{id}

# Jobs
GET    /jobs
POST   /jobs
GET    /jobs/{id}
DELETE /jobs/{id}

# Experiments
GET    /jobs/{job_id}/experiments
GET    /experiments/{id}

# Models
GET    /models
GET    /models/{id}
GET    /models/{id}/download
DELETE /models/{id}

# User
GET    /user
GET    /user/usage
GET    /user/billing
```

---

## 8. Business Model

### Pricing Tiers

| Tier | Price | Includes | Target User |
|------|-------|----------|-------------|
| **Free** | $0 | 3 experiments/month, 10MB data limit | Trial, students |
| **Starter** | $29/month | 50 experiments, 100MB limit | Individuals |
| **Pro** | $99/month | 200 experiments, 1GB limit | Power users |
| **Team** | $299/month | 500 experiments, 5GB limit, 5 seats | Small teams |
| **Enterprise** | Custom | Unlimited, on-premise, SLA | Large companies |

### Per-Experiment Pricing (Alternative)

| Compute | Price per Experiment |
|---------|---------------------|
| T4 (5 min) | $0.50 |
| A100 (5 min) | $2.00 |
| H100 (5 min) | $5.00 |

### Revenue Projections (Conservative)

| Period | Free Users | Paid Users | MRR | Notes |
|--------|------------|------------|-----|-------|
| Month 3 | 500 | 20 | $1,000 | Early adopters |
| Month 6 | 2,000 | 100 | $5,000 | Word of mouth |
| Month 12 | 10,000 | 500 | $25,000 | Product-market fit |
| Year 2 | 50,000 | 2,000 | $100,000 | Scaling |
| Year 3 | 200,000 | 5,000 | $250,000+ | Mature |

### Unit Economics

| Metric | Target |
|--------|--------|
| CAC (Customer Acquisition Cost) | < $50 |
| LTV (Lifetime Value) | > $300 |
| LTV:CAC ratio | > 6:1 |
| Gross margin | > 60% |
| Churn (monthly) | < 5% |

---

## 9. Go-to-Market Strategy

### Launch Channels

| Channel | Strategy | Timeline |
|---------|----------|----------|
| **Product Hunt** | Launch day push | Week 1 |
| **Hacker News** | Show HN post | Week 1 |
| **Twitter/X** | ML community engagement | Ongoing |
| **Reddit** | r/MachineLearning, r/learnmachinelearning | Week 2 |
| **Content** | Blog posts, tutorials | Ongoing |
| **YouTube** | Demo videos, tutorials | Month 2 |
| **Partnerships** | ML course integrations | Month 3 |

### Messaging

**Tagline:** "Train better models while you sleep"

**Positioning:** For teams who want custom ML models without hiring a PhD

**Key Messages:**
1. No ML expertise required
2. 10x more experiments in same time
3. Pay only for what you use
4. Results in hours, not weeks

### Early Adopter Program

| Element | Details |
|---------|---------|
| **Target** | 50 beta users |
| **Offer** | 3 months free Pro plan |
| **Ask** | Feedback, testimonials, referrals |
| **Duration** | 4-6 weeks before public launch |

---

## 10. Success Metrics & KPIs

### North Star Metric

**Weekly Active Experiments Run**

### Key Performance Indicators

| Category | Metric | Target (MVP) | Target (Year 1) |
|----------|--------|--------------|-----------------|
| **Acquisition** | Signups/week | 50 | 500 |
| **Activation** | % who run first experiment | 60% | 70% |
| **Retention** | 30-day retained | 30% | 40% |
| **Revenue** | MRR | $1,000 | $25,000 |
| **Satisfaction** | NPS | > 30 | > 50 |
| **Productivity** | Experiments per user/week | 5 | 10 |

### Technical KPIs

| Metric | Target |
|--------|--------|
| Experiment success rate | > 95% |
| P95 latency (API) | < 500ms |
| Uptime | > 99.5% |
| Queue wait time (avg) | < 2 minutes |

---

## 11. Roadmap

### Phase 1: MVP (8 weeks)

| Week | Milestone |
|------|-----------|
| 1-2 | Core backend (auth, upload, queue) |
| 3-4 | Worker infrastructure, experiment runner |
| 5-6 | Frontend (upload, results, download) |
| 7 | Billing integration |
| 8 | Testing, bug fixes, launch prep |

**MVP Scope:**
- Data upload (.txt, .csv)
- Simple mode only
- T4 GPU only
- 5-minute experiments
- Download .pt model
- Free + Starter tiers

### Phase 2: Growth (12 weeks)

| Week | Milestone |
|------|-----------|
| 1-2 | Advanced configuration |
| 3-4 | Multiple GPU types |
| 5-6 | Team workspaces |
| 7-8 | API access |
| 9-10 | Inference API |
| 11-12 | Integrations (HF, etc.) |

### Phase 3: Scale (Ongoing)

- Enterprise features
- On-premise deployment
- Advanced model architectures
- Multi-modal support
- International expansion

---

## 12. Risks & Mitigations

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| GPU availability | Medium | High | Multi-cloud, spot instance fallbacks |
| Experiment failures | Medium | Medium | Robust error handling, retries |
| Data security breach | Low | Critical | Encryption, audit logs, penetration testing |
| Scalability issues | Medium | High | Load testing, auto-scaling, queue management |

### Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low adoption | Medium | High | Early user research, marketing investment |
| Competition (Big Tech) | Low | High | Focus on niche, superior UX |
| Price undercutting | Medium | Medium | Value-add features, stickiness |
| Churn | Medium | High | Onboarding, support, feature development |

### Legal/Compliance Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| GDPR violations | Medium | High | Clear data policies, deletion tools |
| User data misuse | Low | Critical | ToS, monitoring, abuse detection |
| IP issues | Low | Medium | Clear ownership terms |

---

## 13. Dependencies

### Internal

| Dependency | Owner | Status |
|------------|-------|--------|
| Autoresearch core | Engineering | ✅ Ready |
| Colab compatibility | Engineering | ✅ Ready |

### External

| Dependency | Provider | Status |
|------------|----------|--------|
| GPU compute | AWS/GCP | To provision |
| Payment processing | Stripe | To integrate |
| Email service | SendGrid/Resend | To integrate |
| Monitoring | Datadog/Grafana Cloud | To set up |

---

## 14. Open Questions

| Question | Options | Decision Needed By |
|----------|---------|-------------------|
| Cloud provider? | AWS vs GCP vs multi-cloud | Week 1 |
| Initial GPU type? | T4 only vs T4 + A100 | Week 2 |
| Pricing model? | Subscription vs per-experiment vs hybrid | Week 4 |
| Auth provider? | Custom vs Auth0 vs Clerk | Week 1 |
| Frontend framework? | Next.js vs Vite + React | Week 1 |
| Launch strategy? | Private beta vs public | Week 6 |

---

## 15. Appendix

### Competitive Analysis

| Competitor | Strengths | Weaknesses | Our Advantage |
|------------|-----------|------------|---------------|
| **HuggingFace AutoTrain** | Brand, ecosystem | Complex, expensive | Simpler, cheaper |
| **Google Vertex AI** | Infrastructure, scale | Enterprise-focused | Accessible to all |
| **AWS SageMaker** | Integration, features | Complex, AWS lock-in | Standalone, easy |
| **Weights & Biases** | Tracking, collaboration | No training | We do training |
| **Replicate** | Easy deployment | No optimization | We optimize |

### Glossary

| Term | Definition |
|------|------------|
| **val_bpb** | Validation bits per byte - lower is better |
| **Experiment** | Single training run with specific configuration |
| **Job** | Collection of experiments with shared dataset |
| **Model** | Trained weights ready for inference |
| **Worker** | GPU instance running experiments |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-13 | [Author] | Initial draft |

---

## Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| Product | | ⏳ Pending | |
| Engineering | | ⏳ Pending | |
| Design | | ⏳ Pending | |
| Executive | | ⏳ Pending | |
