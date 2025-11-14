# Contributing to Claude Skills - SPEC-First Development

환영합니다! 이 문서는 SPEC-First 개발 시스템에 기여하는 방법을 안내합니다.

## 목차

1. [개발 철학](#개발-철학)
2. [프로젝트 구조](#프로젝트-구조)
3. [기여 워크플로우](#기여-워크플로우)
4. [SPEC 작성 가이드](#spec-작성-가이드)
5. [Skill 작성 가이드](#skill-작성-가이드)
6. [코드 스타일](#코드-스타일)
7. [테스팅](#테스팅)
8. [Pull Request 가이드](#pull-request-가이드)

---

## 개발 철학

### SPEC-First 원칙

이 프로젝트는 **SPEC-First** 개발을 따릅니다:

1. **SPEC 먼저**: 코드를 작성하기 전에 항상 SPEC 문서를 작성합니다
2. **EARS 형식**: 구조화된 요구사항 명세(Easy Approach to Requirements Syntax) 사용
3. **추적성**: 모든 코드는 SPEC ID로 추적 가능해야 합니다
4. **문서 동기화**: 코드 변경 시 관련 문서도 함께 업데이트합니다

### TRUST 5 원칙

- **T**est-first: 테스트를 먼저 작성합니다
- **R**eadable: 읽기 쉬운 코드를 작성합니다
- **U**nified: 일관된 패턴을 따릅니다
- **S**ecured: 보안을 고려합니다
- **T**rackable: 추적 가능한 코드를 작성합니다

---

## 프로젝트 구조

```
cladue-skills/
├── .claude/
│   ├── settings.local.json          # Claude Code 설정
│   └── skills/                      # Android skills (36개)
│       └── android-*/               # 각 skill 디렉토리
│           └── SKILL.md             # Skill 문서
├── specs/                           # SPEC 문서
│   ├── templates/                   # SPEC 템플릿
│   │   ├── feature-spec.md         # 기능 명세 템플릿
│   │   ├── api-spec.md             # API 명세 템플릿
│   │   └── ui-spec.md              # UI 명세 템플릿
│   └── examples/                    # 예제 SPEC
├── tools/                           # Python 에이전트
│   ├── spec_builder.py             # SPEC 생성 도구
│   ├── code_builder.py             # 코드 생성 도구
│   └── doc_syncer.py               # 문서 동기화 도구
├── docs/                            # 문서
│   ├── guides/                      # 가이드
│   └── architecture/                # 아키텍처 문서
└── examples/                        # 샘플 프로젝트
```

---

## 기여 워크플로우

### 1. 이슈 생성

새로운 기능이나 버그 수정을 시작하기 전에 이슈를 생성합니다:

```markdown
**Title**: [SPEC/Skill/Bug] 간단한 설명

**Description**:
- 무엇을: [구체적인 내용]
- 왜: [필요성/문제점]
- 어떻게: [구현 방안]

**Type**: Feature / Bug / Improvement
**Priority**: High / Medium / Low
```

### 2. 브랜치 생성

```bash
# 기능 추가
git checkout -b feature/SPEC-001-user-authentication

# 버그 수정
git checkout -b fix/bug-description

# 문서 업데이트
git checkout -b docs/update-contributing-guide
```

**브랜치 명명 규칙**:
- `feature/SPEC-XXX-description`: 새 기능
- `fix/description`: 버그 수정
- `docs/description`: 문서 업데이트
- `refactor/description`: 리팩토링
- `test/description`: 테스트 추가

### 3. SPEC 작성 (기능 추가 시)

새로운 기능을 추가할 때는 **반드시 SPEC을 먼저 작성**합니다:

```bash
# SPEC 템플릿 복사
cp specs/templates/feature-spec.md specs/examples/my-feature/SPEC.md

# SPEC 작성
# - SPEC ID 부여 (예: SPEC-001)
# - EARS 형식으로 요구사항 작성
# - 관련 Android skills 명시
```

### 4. 코드 작성

SPEC을 기반으로 코드를 작성합니다:

```kotlin
// SPEC-001: User authentication feature
// REQ-001-U-01: The system shall validate user credentials
class AuthRepository @Inject constructor(
    private val authApi: AuthApi,
) {
    suspend fun login(email: String, password: String): Result<User> {
        // REQ-001-U-01: Validate credentials
        // Implementation...
    }
}
```

**코드 주석 규칙**:
- 파일 상단: `// SPEC-XXX: 기능 설명`
- 중요 메서드: `// REQ-XXX-Y-ZZ: 요구사항 설명`

### 5. 테스트 작성

모든 코드는 테스트를 포함해야 합니다:

```kotlin
// TEST-001-U-01: Test login with valid credentials
@Test
fun loginWithValidCredentialsReturnsSuccess() {
    // Given
    val email = "test@example.com"
    val password = "password123"

    // When
    val result = repository.login(email, password)

    // Then
    assertTrue(result.isSuccess)
}
```

### 6. 문서 업데이트

코드 변경에 따라 문서를 업데이트합니다:

- README.md: 새 skill 추가 시 목록에 추가
- SPEC.md: 구현 완료 후 Traceability Matrix 업데이트
- 관련 가이드: 필요 시 업데이트

### 7. 커밋

의미 있는 커밋 메시지를 작성합니다.

**Git Skills 참조:**
- `android-git-atomic-commits` - Atomic commit 작성법
- `android-git-spec-workflow` - SPEC-First git 워크플로우
- `android-git-conventional-commits` - Conventional commit 형식
- `android-git-multi-commit-feature` - 큰 기능을 작은 커밋으로 분할

**커밋 예시:**

```bash
# Layer별로 atomic commit 작성
git add domain/
git commit -m "feat(SPEC-001): Implement domain layer

- Add User model and AuthToken
- Create AuthRepository interface
- Add LoginUseCase and LogoutUseCase

Refs: SPEC-001, REQ-001-U-01, REQ-001-U-02"

git add data/
git commit -m "feat(SPEC-001): Implement data layer

- Add AuthApi for network calls
- Implement AuthRepositoryImpl
- Add JWT token storage with DataStore

Refs: SPEC-001, REQ-001-U-03"

git add presentation/
git commit -m "feat(SPEC-001): Implement presentation layer

- Create AuthViewModel with state management
- Define AuthActions and AuthEvents

Refs: SPEC-001, REQ-001-E-01"

git add test/
git commit -m "test(SPEC-001): Add authentication tests

- Unit tests for use cases and repository
- ViewModel tests with MockK and Turbine
- UI tests with Compose Test
- Coverage: 92%

Refs: SPEC-001"

git add docs/ specs/
git commit -m "docs(SPEC-001): Update documentation

- Sync traceability matrix
- Update README with authentication guide
- Add architecture diagram

Refs: SPEC-001

Refs: SPEC-001, REQ-001-U-01, REQ-001-U-02"
```

**커밋 메시지 형식**:
```
<type>(<spec-id>): <subject>

<body>

Refs: <SPEC IDs>, <REQ IDs>
```

**Types**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 업데이트
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `chore`: 기타 작업

### 8. Pull Request

PR을 생성하고 리뷰를 요청합니다:

```markdown
## Summary
SPEC-001 User Authentication 기능 구현

## Changes
- [ ] SPEC.md 작성 완료
- [ ] Domain layer 구현 (AuthRepository, LoginUseCase)
- [ ] Data layer 구현 (AuthApi, AuthRepositoryImpl)
- [ ] Presentation layer 구현 (LoginViewModel, LoginScreen)
- [ ] Unit tests 작성 (85% coverage)
- [ ] UI tests 작성
- [ ] Documentation 업데이트

## Traceability
- SPEC-001
- REQ-001-U-01: ✅ Implemented, ✅ Tested
- REQ-001-U-02: ✅ Implemented, ✅ Tested
- REQ-001-E-01: ✅ Implemented, ✅ Tested

## Related Skills
- android-clean-architecture
- android-mvvm-architecture
- android-compose-ui
- android-hilt-di
- android-networking-retrofit

## Testing
- Unit test coverage: 87%
- UI tests: All passing
- Manual testing: Completed

## Screenshots
[스크린샷 추가]

## Checklist
- [ ] SPEC 작성 완료
- [ ] 코드 구현 완료
- [ ] 테스트 작성 완료 (85%+ coverage)
- [ ] 문서 업데이트 완료
- [ ] Self-review 완료
- [ ] 로컬에서 모든 테스트 통과
```

---

## SPEC 작성 가이드

### SPEC ID 규칙

- **Feature SPEC**: `SPEC-XXX` (예: SPEC-001, SPEC-002)
- **API SPEC**: `API-XXX` (예: API-001)
- **UI SPEC**: `UI-XXX` (예: UI-001)

### EARS 형식 요구사항

모든 요구사항은 EARS 형식을 따릅니다:

#### 1. Ubiquitous (일반 요구사항)
```
The system shall [requirement]
```
예: "The system shall validate user email format"

#### 2. State-Driven (상태 기반)
```
WHILE [state], the system shall [requirement]
```
예: "WHILE user is authenticated, the system shall display user profile"

#### 3. Event-Driven (이벤트 기반)
```
WHEN [trigger], the system shall [requirement]
```
예: "WHEN user clicks login button, the system shall validate credentials"

#### 4. Optional (선택적)
```
WHERE [feature], the system shall [requirement]
```
예: "WHERE biometric is enabled, the system shall offer fingerprint login"

#### 5. Unwanted (원하지 않는 동작)
```
IF [condition], THEN the system shall NOT [behavior]
```
예: "IF password is incorrect, THEN the system shall NOT log in the user"

### 요구사항 ID 규칙

```
REQ-[SPEC-ID]-[TYPE]-[NUMBER]
```

- **SPEC-ID**: SPEC 번호 (예: 001)
- **TYPE**:
  - `U`: Ubiquitous
  - `S`: State-driven
  - `E`: Event-driven
  - `O`: Optional
  - `N`: Unwanted
- **NUMBER**: 순차 번호 (01, 02, ...)

예: `REQ-001-U-01`, `REQ-001-E-05`

---

## Skill 작성 가이드

### Skill 명명 규칙

```
android-[domain]-[feature]
```

예:
- `android-compose-ui`
- `android-hilt-di`
- `android-mvvm-architecture`

### Skill 파일 구조

```markdown
---
name: skill-name
description: One-line description
---

# Skill Title

Brief overview

## When to Use
- Use case 1
- Use case 2

## Implementation

### Setup
[Setup instructions]

### Code Example
[Kotlin code with comments]

## Related Skills
- related-skill-1
- related-skill-2

## Best Practices
1. Practice 1
2. Practice 2
```

### Skill 작성 원칙

1. **Small & Focused**: 각 skill은 500줄 이하
2. **Independent**: 다른 skill에 의존하지 않음
3. **Practical**: 실제 사용 가능한 코드 예제
4. **Modern**: 2025 최신 베스트 프랙티스

---

## 코드 스타일

### Python

```python
# Black 포맷터 사용
black .

# Ruff 린터 사용
ruff check .

# Type hints 사용
def build_spec(feature_name: str, requirements: list[str]) -> SpecDocument:
    """Build a SPEC document from requirements.

    Args:
        feature_name: Name of the feature
        requirements: List of requirement descriptions

    Returns:
        SpecDocument: Generated SPEC document
    """
    pass
```

### Kotlin

```kotlin
// 2025 Android 코딩 규칙 준수
// - Compose UI 사용
// - Kotlin 2.1.0+ 기능 활용
// - Clean Architecture 적용

// Good: Clear, readable function
fun validateEmail(email: String): Boolean {
    return email.matches(Regex("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"))
}

// Bad: Unclear function
fun v(e: String) = e.matches(Regex("..."))
```

### Markdown

- 헤더: `#`, `##`, `###` 사용
- 코드 블록: 언어 지정 (```kotlin, ```python)
- 리스트: 일관된 기호 사용 (`-` 또는 `*`)
- 링크: 명확한 텍스트 사용

---

## 테스팅

### 테스트 커버리지

- **최소 요구사항**: 85%
- **목표**: 90%+

### 테스트 작성

```kotlin
// TEST-XXX-U-01: Test description
@Test
fun testMethodName() {
    // Given: Setup test data
    val input = "test"

    // When: Execute method under test
    val result = methodUnderTest(input)

    // Then: Assert expected outcome
    assertEquals(expected, result)
}
```

### 테스트 실행

```bash
# Python tests
pytest --cov=tools tests/

# Android tests (in example project)
./gradlew test
./gradlew connectedAndroidTest
```

---

## Pull Request 가이드

### PR 체크리스트

PR 생성 전 확인:

- [ ] SPEC 문서 작성 완료
- [ ] 모든 요구사항 구현
- [ ] 테스트 커버리지 85% 이상
- [ ] 문서 업데이트 완료
- [ ] 코드 리뷰 준비 완료
- [ ] 모든 테스트 통과
- [ ] 커밋 메시지 규칙 준수
- [ ] Traceability Matrix 업데이트

### PR 리뷰 기준

리뷰어는 다음을 확인합니다:

1. **SPEC 완성도**
   - EARS 형식 준수
   - 모든 요구사항 명확히 정의
   - Related skills 정확히 명시

2. **코드 품질**
   - SPEC ID 주석 포함
   - Clean Architecture 준수
   - 읽기 쉬운 코드
   - 보안 이슈 없음

3. **테스트**
   - 모든 요구사항 테스트됨
   - Edge case 처리
   - 85%+ 커버리지

4. **문서**
   - SPEC-Code-Test 일치
   - README 업데이트
   - 예제 코드 작동

### 리뷰 프로세스

1. **Self-review**: PR 생성자가 먼저 자체 리뷰
2. **Peer review**: 동료 개발자 1-2명이 리뷰
3. **Approval**: 최소 1명 승인 필요
4. **Merge**: Squash merge 사용

---

## 질문 & 도움

### 도움이 필요하면

- **이슈 생성**: 질문이나 문제를 이슈로 등록
- **라벨 사용**: `question`, `help wanted`, `good first issue`

### 좋은 첫 기여

다음 작업은 초보자에게 적합합니다:

- 문서 오타 수정
- 예제 코드 추가
- 테스트 커버리지 향상
- `good first issue` 라벨 이슈

---

## 라이선스

이 프로젝트에 기여함으로써 MIT 라이선스에 동의합니다.

---

## 감사합니다!

여러분의 기여가 이 프로젝트를 더 좋게 만듭니다. 🙏
