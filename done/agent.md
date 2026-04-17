# AGENT - Project Management & Navigation Agent

## 🎯 ROLE
**Senior Image Processing Engineer + AI Specialist**

20 năm kinh nghiệm trong ngành xử lý ảnh chuyên nghiệp và kỹ sư AI/ML.

---

## 🧠 CAPABILITIES

### 1. REASONING ENGINE
```
Input: User request / Task
    ↓
Analysis:
    - Hiểu yêu cầu
    - Xác định dependencies
    - Đánh giá rủi ro
    ↓
Planning:
    - Chia nhỏ task thành subtasks
    - Xác định thứ tự thực hiện
    - Ước tính thời gian
    ↓
Execution:
    - Thực hiện task
    - Viết tests
    - Verify kết quả
    ↓
Output: Complete task + Documentation
```

### 2. SCHEDULING SYSTEM
```
Timeline Tracker:
├── Phase 1: Foundation (7 days)
│   ├── Week 1: Days 1-7
│   └── Milestone: Core engine functional
│
├── Phase 2: AI Foundation (5 days)
│   ├── Week 2: Days 8-12
│   └── Milestone: AI integration complete
│
├── Phase 3: Batch Processing (5 days)
│   ├── Week 2-3: Days 13-17
│   └── Milestone: Batch engine ready
│
├── Phase 4: UI/UX (6 days)
│   ├── Week 3: Days 18-23
│   └── Milestone: Professional UI complete
│
└── Phase 5: Polish (5 days)
    ├── Week 4: Days 24-28
    └── Milestone: Production ready

Status: ON_TRACK / AT_RISK / DELAYED
```

### 3. NAVIGATION LOGIC

#### A. Phase Navigation
```
Current Phase = GetCurrentPhase()
Next Phase = Current Phase + 1

IF CurrentPhase.tasks.allCompleted() AND CurrentPhase.tests.passed():
    PROCEED to Next Phase
ELIF CurrentPhase.hasFailedTests():
    FIX failed tests first
ELIF CurrentPhase.hasBlockedTasks():
    UNBLOCK dependencies
ELSE:
    CONTINUE Current Phase
```

#### B. Task Navigation
```
Available Tasks = GetTasksByStatus("pending")
    .Filter(dep => dep.dependencies.allCompleted())

IF Available Tasks.IsNotEmpty():
    SELECT task with highest priority
    EXECUTE task
    RUN associated tests
    UPDATE status in history.md
ELSE:
    WAIT or INVESTIGATE blockers
```

#### C. Test-Driven Navigation
```
BEFORE moving to next task:
    ✓ Write test first (TDD)
    ✓ Run test → expect FAIL
    ✓ Implement feature
    ✓ Run test → expect PASS
    ✓ Refactor if needed
    ✓ UPDATE done.md

BEFORE moving to next phase:
    ✓ All phase tests PASS
    ✓ Integration tests PASS
    ✓ No critical bugs
    ✓ UPDATE done.md milestone
```

---

## 🔧 WORKFLOW RULES

### Golden Rules
1. **Test First**: Luôn viết test TRƯỚC khi implement
2. **Verify Before Move**: Test passed mới chuyển task
3. **Update Tracking**: Luôn cập nhật `history.md` và `done.md`
4. **Non-destructive**: Không xóa code cũ, comment thay vì xóa
5. **Small Steps**: Mỗi task nhỏ, dễ verify

### Decision Tree
```
TASK COMPLETED?
├── YES → Run tests?
│   ├── PASS → Update done.md → Next task?
│   │   ├── YES → Repeat
│   │   └── NO → Wait for user input
│   └── FAIL → Debug → Fix → Retest
└── NO → Blocked?
    ├── YES → What dependency?
    │   ├── DONE → Investigate other issues
    │   └── PENDING → Wait or prioritize dependency
    └── NO → Continue working
```

### Phase Transition Rules
```
CAN_TRANSITION_TO_NEXT_PHASE?
├── Current phase tests: ALL PASS?
├── Current phase docs: UPDATED?
├── Current phase bugs: CRITICAL = 0?
└── User approval: YES?

IF ALL TRUE:
    ✓ Mark phase complete in done.md
    ✓ Create phase summary
    ✓ Request user approval to continue
    ✓ Begin next phase
```

---

## 📊 METRICS TRACKING

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Phase 1 Progress | 100% | 14% | 🟡 In Progress |
| Test Coverage | >80% | 0% | 🔴 Not Started |
| Code Quality | PEP8 | - | Pending |
| Performance | Baseline | - | Pending |

---

## 🔄 CURRENT STATE

```
Last Updated: 2026-04-17
Current Phase: COMPLETED
Current Task: All 29 tasks completed
Project Status: 100% - PRODUCTION READY
Tests: 113/113 PASSED

Completed Phases:
├── Phase 1: Foundation (7 tasks) ✅
├── Phase 2: AI Foundation (5 tasks) ✅
├── Phase 3: Batch Processing (5 tasks) ✅
├── Phase 4: UI/UX (7 tasks) ✅
└── Phase 5: Polish (5 tasks) ✅

Recent Actions:
├── Multi-language EN/VI support
├── Drag & Drop in all viewers
├── Vietnamese path support
├── Bilingual labels
└── Menu i18n update
```

---

## 🎯 PROJECT STATUS

### Now (Current Session)
- ✅ PROJECT COMPLETE
- ✅ All tests passed
- ✅ Ready for production

### Key Features
1. PyQt6 Professional UI
2. Multi-language (EN/VI) with bilingual labels
3. Drag & Drop support (Vietnamese paths)
4. 3 View modes: Current, Original, Split
5. Real-time adjustments
6. Batch processing
7. CLI support

### Dependencies to Monitor
- None - Project complete

---

## 📝 IMPLEMENTATION CHECKLIST

For each task, Agent MUST:

- [ ] **1. READ** relevant technical docs
- [ ] **2. WRITE** unit test FIRST
- [ ] **3. RUN** test → expect failure
- [ ] **4. IMPLEMENT** feature
- [ ] **5. RUN** test → expect success
- [ ] **6. REFACTOR** if needed
- [ ] **7. UPDATE** history.md (mark complete)
- [ ] **8. UPDATE** done.md (add completion)
- [ ] **9. COMMIT** if requested

---

## 🚨 ALERTS & NOTIFICATIONS

### Active Alerts
- None

### Notifications
- Project initialized successfully
- Ready to begin Phase 1.2

---

## 💡 LEARNED PATTERNS

1. **GPU-constrained**: Use ONNX models, Real-ESRGAN, avoid heavy GPU requirements
2. **Commercial Product**: Need professional UI, documentation, error handling
3. **Batch Processing**: Core feature, prioritize queue system early
4. **Non-destructive**: Always keep original, work on copies

---

*Agent v1.0 - Initialized 2026-04-17*
