# 🤖 Android AI Development Kit (AIDK)

A comprehensive SPEC-First Android development framework with 36 specialized skills, AI-powered automation tools, and seamless Claude Code integration.

## Overview

**Android AI Development Kit**은 현대적인 Android 개발을 위한 완전한 개발 프레임워크입니다:

- **36개 전문 스킬**: Jetpack Compose, Clean Architecture, MVVM, DI, Testing 등
- **SPEC-First 개발**: AI 기반 자동 SPEC 생성 및 검증
- **자동 코드 생성**: Clean Architecture 코드 자동 생성
- **문서 동기화**: SPEC-코드-문서 자동 동기화
- **Claude Code 통합**: 완벽한 IDE 통합

## 🚀 Quick Start

### Installation

#### Option 1: Install from PyPI (Recommended)

```bash
# Install globally
pip install android-ai-devkit

# Install skills to your Android project
cd your-android-project
aidk install --local
```

#### Option 2: Install from Source

```bash
# Clone repository
git clone https://github.com/yourusername/android-ai-devkit.git
cd android-ai-devkit

# Install
pip install -e .

# Or use installation script
./install.sh        # Unix/Mac
# or
install.ps1         # Windows
```

### First Steps

1. **Create your first SPEC:**
```bash
aidk spec create "User Authentication Feature"
```

2. **Generate code from SPEC:**
```bash
aidk code generate specs/SPEC-001/SPEC.md --output ./src --package com.example.app
```

3. **Synchronize documentation:**
```bash
aidk docs sync specs/SPEC-001/SPEC.md --code ./src
```

4. **List available skills:**
```bash
aidk skills
```

## 📚 CLI Commands

### Installation & Updates
```bash
aidk install --local              # Install skills to current project
aidk install --local --with-examples  # Include example SPECs
aidk update                       # Check for and install updates
aidk version                      # Show version information
aidk info                         # Display system information
```

### SPEC Management
```bash
aidk spec create "Feature Name"   # Create new SPEC (quick mode)
aidk spec create -i               # Interactive SPEC creation
aidk spec validate SPEC.md        # Validate SPEC document
```

### Code Generation
```bash
aidk code generate SPEC.md                     # Generate code
aidk code generate SPEC.md -o ./app -p com.app  # Custom output & package
```

### Documentation
```bash
aidk docs sync SPEC.md --code ./src   # Sync documentation
aidk docs verify SPEC.md --code ./src # Verify SPEC-code alignment
```

### Skills
```bash
aidk skills                       # List all available skills
```

## 📦 What's Included

### Python Automation Tools
- **spec_builder.py**: AI-powered SPEC generation with EARS format
- **code_builder.py**: Clean Architecture code generation
- **doc_syncer.py**: Documentation synchronization
- **validate_specs.py**: SPEC validation

### SPEC Templates
- Feature specification template
- API specification template
- UI specification template

### Example Projects
- User Authentication (complete SPEC + generated code)
- Product Catalog (complete SPEC + generated code)

## Skills Catalog

### 🏗️ Core Architecture (3 skills)

| Skill | Description |
|-------|-------------|
| **android-project-setup** | 프로젝트 초기 설정, Gradle 구성, 디렉토리 구조 |
| **android-clean-architecture** | 3레이어 Clean Architecture (Presentation, Domain, Data) |
| **android-mvvm-architecture** | MVVM 패턴, StateFlow, Unidirectional Data Flow |

### 🎨 UI Development (4 skills)

| Skill | Description |
|-------|-------------|
| **android-compose-ui** | Jetpack Compose 기본, Composable, State 관리 |
| **android-compose-navigation** | Navigation 3, 타입 세이프 라우팅, Deep Linking |
| **android-compose-theming** | Material3 테마, 컬러, 타이포그래피, 다크모드 |
| **android-xml-views** | XML 레이아웃, ViewBinding, RecyclerView (레거시) |

### 💉 Dependency Injection (2 skills)

| Skill | Description |
|-------|-------------|
| **android-hilt-di** | Hilt 의존성 주입, 모듈, 스코프, 컴파일타임 검증 |
| **android-koin-di** | Koin 의존성 주입, Kotlin DSL, 런타임 DI |

### 📦 Data Layer (4 skills)

| Skill | Description |
|-------|-------------|
| **android-repository-pattern** | Repository 패턴, 캐싱 전략, 데이터 소스 추상화 |
| **android-database-room** | Room 로컬 DB, Entity, DAO, 마이그레이션 |
| **android-networking-retrofit** | Retrofit API 통신, OkHttp, 에러 핸들링 |
| **android-datastore** | DataStore 설정 저장, Preferences, Proto DataStore |

### 📄 JSON Parsing (2 skills)

| Skill | Description |
|-------|-------------|
| **android-json-moshi** | Moshi JSON 파싱, 커스텀 어댑터, Retrofit 통합 |
| **android-json-kotlinx** | Kotlin Serialization, 컴파일타임 안전성, 멀티플랫폼 지원 |

### 🔄 State Management (2 skills)

| Skill | Description |
|-------|-------------|
| **android-stateflow** | StateFlow, SharedFlow, 리액티브 상태 관리 |
| **android-one-time-events** | 일회성 이벤트 처리 (Navigation, Toast) |

### ⚡ Async & Background (3 skills)

| Skill | Description |
|-------|-------------|
| **android-coroutines** | Kotlin Coroutines, Dispatcher, 구조적 동시성 |
| **android-workmanager** | WorkManager 백그라운드 작업, 주기적 동기화 |
| **android-paging3** | Paging 3 페이지네이션, 무한 스크롤 |

### 🧪 Testing (4 skills)

| Skill | Description |
|-------|-------------|
| **android-compose-testing** | Compose UI 테스트, Semantics, ComposeTestRule |
| **android-unit-testing** | Unit 테스트, JUnit, Coroutine 테스트 |
| **android-testing-mockk** | MockK 모킹 프레임워크, 코루틴 지원, DSL 문법 |
| **android-testing-turbine** | Turbine Flow 테스팅, awaitItem(), StateFlow 테스트 |

### ⚙️ Build Configuration (1 skill)

| Skill | Description |
|-------|-------------|
| **android-gradle-config** | Gradle Kotlin DSL, Build Types, Flavors, Version Catalog |

### 🔧 Common Features (5 skills)

| Skill | Description |
|-------|-------------|
| **android-permissions** | 런타임 권한 처리, Android 13+ 권한 |
| **android-image-loading** | Coil (Compose), Glide (Views) 이미지 로딩 |
| **android-forms-validation** | 폼 검증, 실시간 유효성 검사 |
| **android-list-ui** | LazyColumn, LazyGrid, RecyclerView 리스트 UI |
| **android-material-components** | Material Design 3 컴포넌트 (Button, Card, Dialog 등) |

### 🛠️ Utilities (1 skill)

| Skill | Description |
|-------|-------------|
| **android-logging-timber** | Timber 로깅 라이브러리, 커스텀 Tree, 환경별 로깅 전략 |

### 🎬 Animation (1 skill)

| Skill | Description |
|-------|-------------|
| **android-animation-lottie** | Lottie 애니메이션, Adobe After Effects 통합, JSON 애니메이션 |

### 🔀 Git Workflow (4 skills)

| Skill | Description |
|-------|-------------|
| **android-git-atomic-commits** | Atomic commit 작성, Conventional commit 형식, SPEC 추적성 |
| **android-git-spec-workflow** | SPEC-First git 워크플로우, 브랜치 전략, PR 생성 |
| **android-git-conventional-commits** | Conventional commit 검증, Changelog 자동 생성, Semantic versioning |
| **android-git-multi-commit-feature** | 큰 기능을 논리적 커밋으로 분할, 코드 리뷰 최적화 |

## How It Works

### 자동 스킬 조합

Claude는 작업 내용에 따라 필요한 스킬들을 자동으로 로드하고 조합합니다.

**예시 1: 새로운 기능 화면 개발**
```
사용자 요청: "사용자 목록을 보여주는 화면을 만들어줘. MVVM과 Compose를 사용하고,
             API에서 데이터를 가져와서 Room에 캐싱해줘."

Claude가 자동으로 로드하는 스킬:
→ android-mvvm-architecture (ViewModel, State 관리)
→ android-compose-ui (화면 UI 구현)
→ android-repository-pattern (데이터 레이어)
→ android-networking-retrofit (API 호출)
→ android-database-room (로컬 캐싱)
→ android-hilt-di (의존성 주입)
→ android-coroutines (비동기 처리)
→ android-list-ui (리스트 표시)
```

**예시 2: 프로젝트 초기 설정**
```
사용자 요청: "새로운 Android 프로젝트를 Hilt와 Compose로 설정해줘."

Claude가 자동으로 로드하는 스킬:
→ android-project-setup (프로젝트 구조)
→ android-hilt-di (DI 설정)
→ android-compose-theming (테마 설정)
→ android-gradle-config (빌드 설정)
```

## Technology Stack (2025)

이 스킬들은 2025년 기준 최신 안드로이드 개발 모범 사례를 따릅니다:

- **Language**: Kotlin 2.1.0
- **UI**: Jetpack Compose (Material3)
- **Architecture**: MVVM + Clean Architecture
- **DI**: Hilt 2.51
- **Database**: Room 2.6.1
- **Networking**: Retrofit 2.11.0 + OkHttp 4.12.0
- **JSON**: Moshi 1.15.1, Kotlinx Serialization 1.7.3
- **Async**: Kotlin Coroutines + StateFlow
- **Navigation**: Navigation Compose 2.8.5
- **Image Loading**: Coil 3.0.4
- **Animation**: Lottie 6.5.2
- **Logging**: Timber 5.0.1
- **Build**: Gradle Kotlin DSL 8.7.3
- **Testing**: JUnit, MockK 1.13.13, Turbine 1.1.0, Compose Test

## Project Structure

```
.claude/skills/
├── android-project-setup/
│   └── SKILL.md
├── android-clean-architecture/
│   └── SKILL.md
├── android-mvvm-architecture/
│   └── SKILL.md
├── android-compose-ui/
│   └── SKILL.md
├── android-compose-navigation/
│   └── SKILL.md
├── android-compose-theming/
│   └── SKILL.md
├── android-xml-views/
│   └── SKILL.md
├── android-hilt-di/
│   └── SKILL.md
├── android-koin-di/
│   └── SKILL.md
├── android-repository-pattern/
│   └── SKILL.md
├── android-database-room/
│   └── SKILL.md
├── android-networking-retrofit/
│   └── SKILL.md
├── android-datastore/
│   └── SKILL.md
├── android-stateflow/
│   └── SKILL.md
├── android-one-time-events/
│   └── SKILL.md
├── android-coroutines/
│   └── SKILL.md
├── android-workmanager/
│   └── SKILL.md
├── android-paging3/
│   └── SKILL.md
├── android-compose-testing/
│   └── SKILL.md
├── android-unit-testing/
│   └── SKILL.md
├── android-gradle-config/
│   └── SKILL.md
├── android-permissions/
│   └── SKILL.md
├── android-image-loading/
│   └── SKILL.md
├── android-forms-validation/
│   └── SKILL.md
├── android-list-ui/
│   └── SKILL.md
├── android-material-components/
│   └── SKILL.md
├── android-json-moshi/
│   └── SKILL.md
├── android-json-kotlinx/
│   └── SKILL.md
├── android-testing-mockk/
│   └── SKILL.md
├── android-testing-turbine/
│   └── SKILL.md
├── android-logging-timber/
│   └── SKILL.md
├── android-animation-lottie/
│   └── SKILL.md
├── android-git-atomic-commits/
│   └── SKILL.md
├── android-git-spec-workflow/
│   └── SKILL.md
├── android-git-conventional-commits/
│   └── SKILL.md
└── android-git-multi-commit-feature/
    └── SKILL.md
```

## Installation

### 프로젝트 스킬로 설치 (팀 공유)

```bash
# 이 저장소를 프로젝트 루트에 클론
cd your-android-project
git clone <this-repo> .claude/skills
```

### 개인 스킬로 설치 (모든 프로젝트에서 사용)

```bash
# 홈 디렉토리에 복사
cp -r .claude/skills ~/.claude/skills/
```

## Usage Examples

### 새 프로젝트 시작

```
"Hilt와 Compose를 사용하는 새 Android 프로젝트를 설정해줘.
Clean Architecture 구조로 만들고, Retrofit과 Room을 포함해줘."
```

### 화면 구현

```
"제품 목록 화면을 만들어줘. LazyColumn으로 리스트를 보여주고,
각 아이템을 클릭하면 상세 화면으로 이동하게 해줘."
```

### 데이터 레이어 구현

```
"User 엔티티를 위한 Repository를 만들어줘.
네트워크 우선 전략으로 API에서 데이터를 가져오고 Room에 캐싱해줘."
```

### 폼 구현

```
"로그인 화면을 만들어줘. 이메일과 비밀번호 입력 필드에
실시간 유효성 검사를 추가하고, 폼이 유효할 때만 버튼을 활성화해줘."
```

### 테스트 작성

```
"HomeViewModel에 대한 유닛 테스트를 작성해줘.
성공 케이스와 에러 케이스 모두 테스트해줘."
```

## Skill Design Principles

### 1. 작은 단위 (Small & Focused)
- 각 스킬은 하나의 명확한 목적
- 500줄 이하의 SKILL.md
- 핵심만 담고 불필요한 설명 제거

### 2. 독립성 (Independent)
- 각 스킬은 독립적으로 사용 가능
- 명시적 의존성 없음
- Claude가 자동으로 필요한 스킬 조합

### 3. 중복 제거 (DRY)
- 공통 내용은 참조로 연결
- Related Skills로 관련 스킬 안내
- 중복 없이 효율적

### 4. 실용성 (Practical)
- 실제 프로젝트에서 바로 사용 가능한 코드
- 2025년 최신 모범 사례
- 실전 예제 중심

## Best Practices

### ✅ Do
- 작업에 필요한 정보를 명확히 전달
- Claude가 자동으로 스킬을 선택하도록 신뢰
- 구체적인 요구사항 제시

### ❌ Don't
- 수동으로 스킬 이름을 지정하지 말 것
- 너무 구체적인 구현 방법을 강제하지 말 것
- 여러 개념을 한 번에 요청하지 말 것

## Benefits

### 개발자
- 🚀 빠른 프로젝트 설정
- 📚 최신 베스트 프랙티스 학습
- 🎯 일관된 코드 품질
- ⏱️ 반복 작업 자동화

### 팀
- 🤝 일관된 아키텍처
- 📖 문서화된 패턴
- 🔄 쉬운 온보딩
- 🛠️ 유지보수성 향상

## Contributing

새로운 스킬 추가나 기존 스킬 개선을 환영합니다!

### 스킬 추가 가이드라인
1. 하나의 명확한 목적
2. YAML frontmatter 필수 (name, description)
3. 500줄 이하 유지
4. 실전 예제 포함
5. Related Skills 명시
6. Best Practices 섹션 포함

## License

MIT License

## Acknowledgments

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Android Developer Guide](https://developer.android.com/)
- [Kotlin Documentation](https://kotlinlang.org/docs/home.html)
- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose)

---

**Made with ❤️ for Android Developers**

*이 스킬 컬렉션은 Claude Code의 Progressive Disclosure 원칙을 따라 설계되었습니다.*
