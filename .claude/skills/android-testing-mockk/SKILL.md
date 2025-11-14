---
name: android-testing-mockk
description: Mocking framework for Kotlin with concise DSL, coroutine support, and powerful verification. Use for unit testing ViewModels, Repositories, and Use Cases.
---

# MockK Testing Framework

Modern mocking library designed specifically for Kotlin with DSL syntax, coroutine support, and relaxed mocks.

## When to Use
- Unit testing with mocks
- Testing ViewModels and Use Cases
- Mocking dependencies (Repositories, APIs)
- Verifying function calls
- Testing suspend functions and coroutines

## Dependencies

```kotlin
// libs.versions.toml
[versions]
mockk = "1.13.13"
coroutines-test = "1.9.0"

[libraries]
mockk = { group = "io.mockk", name = "mockk", version.ref = "mockk" }
mockk-android = { group = "io.mockk", name = "mockk-android", version.ref = "mockk" }
coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "coroutines-test" }

// build.gradle.kts
dependencies {
    testImplementation(libs.mockk)
    androidTestImplementation(libs.mockk.android)
    testImplementation(libs.coroutines.test)
}
```

## Basic Mocking

```kotlin
import io.mockk.*
import org.junit.Test
import kotlin.test.assertEquals

class UserRepositoryTest {

    @Test
    fun `basic mock example`() {
        // Create mock
        val repository = mockk<UserRepository>()

        // Define behavior
        every { repository.getUser("123") } returns User(
            id = "123",
            name = "John Doe"
        )

        // Use mock
        val user = repository.getUser("123")

        // Verify
        assertEquals("John Doe", user.name)
        verify { repository.getUser("123") }
    }
}
```

## Mocking Suspend Functions

```kotlin
import io.mockk.*
import kotlinx.coroutines.test.runTest
import org.junit.Test

class UserUseCaseTest {

    @Test
    fun `mock suspend function`() = runTest {
        // Given
        val repository = mockk<UserRepository>()
        val useCase = GetUserUseCase(repository)

        coEvery { repository.getUser("123") } returns Result.success(
            User(id = "123", name = "John")
        )

        // When
        val result = useCase("123")

        // Then
        assertTrue(result.isSuccess)
        coVerify { repository.getUser("123") }
    }

    @Test
    fun `mock suspend function with delay`() = runTest {
        val repository = mockk<UserRepository>()

        coEvery { repository.getUser(any()) } coAnswers {
            delay(1000)
            Result.success(User(id = "123", name = "John"))
        }

        val result = repository.getUser("123")
        assertTrue(result.isSuccess)
    }
}
```

## Argument Matchers

```kotlin
@Test
fun `argument matchers`() {
    val repository = mockk<UserRepository>()

    // Any value
    every { repository.getUser(any()) } returns someUser

    // Specific value
    every { repository.getUser("123") } returns specificUser

    // Multiple conditions
    every {
        repository.searchUsers(
            query = any(),
            page = more(0),
            limit = range(1, 100)
        )
    } returns listOf(user1, user2)

    // Custom matcher
    every {
        repository.getUser(match { it.startsWith("user_") })
    } returns user

    // Null handling
    every { repository.getUserOrNull(isNull()) } returns null
    every { repository.getUserOrNull(isNull(inverse = true)) } returns user
}
```

## Verification

```kotlin
@Test
fun `verify function calls`() {
    val repository = mockk<UserRepository>()
    every { repository.getUser(any()) } returns user

    // Call function
    repository.getUser("123")
    repository.getUser("456")

    // Verify exact calls
    verify(exactly = 2) { repository.getUser(any()) }
    verify(exactly = 1) { repository.getUser("123") }

    // Verify call order
    verifyOrder {
        repository.getUser("123")
        repository.getUser("456")
    }

    // Verify no more calls
    confirmVerified(repository)
}

@Test
fun `verify with timeout`() = runTest {
    val repository = mockk<UserRepository>()
    coEvery { repository.getUser(any()) } returns Result.success(user)

    launch {
        delay(100)
        repository.getUser("123")
    }

    coVerify(timeout = 500) { repository.getUser("123") }
}
```

## Relaxed Mocks

```kotlin
@Test
fun `relaxed mock returns default values`() {
    // Relaxed mock - no need to define every behavior
    val repository = mockk<UserRepository>(relaxed = true)

    // Returns default values (null, 0, false, empty collections)
    val user = repository.getUser("123")  // Returns null
    val users = repository.getUsers()  // Returns emptyList()

    verify { repository.getUser("123") }
}

@Test
fun `relaxed unit fun mock`() {
    val repository = mockk<UserRepository>(relaxUnitFun = true)

    // Unit functions don't need mocking
    repository.deleteUser("123")  // Works without every

    verify { repository.deleteUser("123") }
}
```

## Spy (Partial Mocking)

```kotlin
class RealUserRepository : UserRepository {
    override fun getUser(id: String): User {
        return User(id, "Real User")
    }

    override fun saveUser(user: User) {
        // Real implementation
    }
}

@Test
fun `spy on real object`() {
    // Spy on real implementation
    val repository = spyk(RealUserRepository())

    // Use real implementation
    val user = repository.getUser("123")
    assertEquals("Real User", user.name)

    // Mock specific method
    every { repository.getUser("456") } returns User("456", "Mocked")

    assertEquals("Mocked", repository.getUser("456").name)
    assertEquals("Real User", repository.getUser("123").name)

    verify { repository.getUser("456") }
}
```

## Object and Companion Object Mocking

```kotlin
object ApiClient {
    fun fetchData(): String = "Real data"
}

class MyClass {
    companion object {
        fun create(): MyClass = MyClass()
    }
}

@Test
fun `mock object`() {
    mockkObject(ApiClient)

    every { ApiClient.fetchData() } returns "Mocked data"

    assertEquals("Mocked data", ApiClient.fetchData())

    unmockkObject(ApiClient)
}

@Test
fun `mock companion object`() {
    mockkObject(MyClass.Companion)

    val mockInstance = mockk<MyClass>()
    every { MyClass.create() } returns mockInstance

    val instance = MyClass.create()
    assertSame(mockInstance, instance)

    unmockkObject(MyClass.Companion)
}
```

## ViewModel Testing

```kotlin
class UserViewModel(
    private val getUserUseCase: GetUserUseCase
) : ViewModel() {

    private val _state = MutableStateFlow(UserState())
    val state: StateFlow<UserState> = _state.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }

            getUserUseCase(id)
                .onSuccess { user ->
                    _state.update {
                        it.copy(isLoading = false, user = user)
                    }
                }
                .onFailure { error ->
                    _state.update {
                        it.copy(isLoading = false, error = error.message)
                    }
                }
        }
    }
}

class UserViewModelTest {

    private lateinit var getUserUseCase: GetUserUseCase
    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        getUserUseCase = mockk()
        viewModel = UserViewModel(getUserUseCase)
    }

    @Test
    fun `loadUser updates state with user on success`() = runTest {
        // Given
        val user = User(id = "123", name = "John")
        coEvery { getUserUseCase("123") } returns Result.success(user)

        // When
        viewModel.loadUser("123")

        // Advance coroutines
        advanceUntilIdle()

        // Then
        val state = viewModel.state.value
        assertEquals(user, state.user)
        assertEquals(false, state.isLoading)
        assertNull(state.error)

        coVerify { getUserUseCase("123") }
    }

    @Test
    fun `loadUser updates state with error on failure`() = runTest {
        // Given
        val error = Exception("Network error")
        coEvery { getUserUseCase("123") } returns Result.failure(error)

        // When
        viewModel.loadUser("123")
        advanceUntilIdle()

        // Then
        val state = viewModel.state.value
        assertNull(state.user)
        assertEquals("Network error", state.error)
        assertEquals(false, state.isLoading)
    }
}
```

## Repository Testing

```kotlin
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao
) : UserRepository {

    override suspend fun getUser(id: String): Result<User> {
        return try {
            val response = api.getUser(id)
            val user = response.toDomain()
            dao.insertUser(user.toEntity())
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

class UserRepositoryImplTest {

    private lateinit var api: UserApi
    private lateinit var dao: UserDao
    private lateinit var repository: UserRepositoryImpl

    @Before
    fun setup() {
        api = mockk()
        dao = mockk(relaxUnitFun = true)  // Ignore insert calls
        repository = UserRepositoryImpl(api, dao)
    }

    @Test
    fun `getUser fetches from API and caches in DB`() = runTest {
        // Given
        val userDto = UserDto(id = "123", name = "John")
        coEvery { api.getUser("123") } returns userDto

        // When
        val result = repository.getUser("123")

        // Then
        assertTrue(result.isSuccess)
        assertEquals("John", result.getOrNull()?.name)

        coVerify { api.getUser("123") }
        verify { dao.insertUser(any()) }
    }

    @Test
    fun `getUser returns failure on API error`() = runTest {
        // Given
        coEvery { api.getUser("123") } throws IOException("Network error")

        // When
        val result = repository.getUser("123")

        // Then
        assertTrue(result.isFailure)

        coVerify { api.getUser("123") }
        verify(exactly = 0) { dao.insertUser(any()) }
    }
}
```

## Answer with Lambda

```kotlin
@Test
fun `answer with lambda`() {
    val repository = mockk<UserRepository>()

    every { repository.getUser(any()) } answers {
        val id = firstArg<String>()
        User(id = id, name = "User $id")
    }

    val user = repository.getUser("123")
    assertEquals("User 123", user.name)
}

@Test
fun `coAnswers for suspend functions`() = runTest {
    val repository = mockk<UserRepository>()

    coEvery { repository.getUser(any()) } coAnswers {
        delay(100)
        val id = firstArg<String>()
        Result.success(User(id = id, name = "User $id"))
    }

    val result = repository.getUser("123")
    assertTrue(result.isSuccess)
}
```

## Slot Capturing

```kotlin
@Test
fun `capture arguments with slot`() {
    val repository = mockk<UserRepository>(relaxUnitFun = true)
    val userSlot = slot<User>()

    // Capture argument
    every { repository.saveUser(capture(userSlot)) } just Runs

    // Call function
    repository.saveUser(User(id = "123", name = "John"))

    // Verify captured value
    assertEquals("123", userSlot.captured.id)
    assertEquals("John", userSlot.captured.name)
}

@Test
fun `capture multiple arguments`() {
    val repository = mockk<UserRepository>(relaxUnitFun = true)
    val users = mutableListOf<User>()

    every { repository.saveUser(capture(users)) } just Runs

    repository.saveUser(User("1", "John"))
    repository.saveUser(User("2", "Jane"))

    assertEquals(2, users.size)
    assertEquals("John", users[0].name)
    assertEquals("Jane", users[1].name)
}
```

## Related Skills
- android-unit-testing: Unit testing basics
- android-testing-turbine: Flow testing
- android-coroutines: Testing coroutines
- android-mvvm-architecture: ViewModel testing

## Best Practices

1. **Use `coEvery` for suspend functions**: Always use `coEvery` and `coVerify` for coroutines
2. **Relaxed mocks for complex dependencies**: Use `relaxed = true` for large interfaces
3. **Verify important calls**: Use `verify` for critical interactions
4. **Clean up**: Use `clearAllMocks()` in `@After` if needed
5. **Argument matchers**: Use matchers for flexible testing
6. **Spy sparingly**: Prefer pure mocks over spies when possible
7. **Test one thing**: Each test should verify one behavior
8. **Named arguments**: Use named arguments for clarity: `every { foo(id = "123") }`

## Common Patterns

### Testing Flow Emissions

```kotlin
@Test
fun `test flow emissions`() = runTest {
    val repository = mockk<UserRepository>()

    coEvery { repository.observeUser("123") } returns flow {
        emit(User("123", "John"))
        delay(100)
        emit(User("123", "John Updated"))
    }

    val emissions = mutableListOf<User>()
    repository.observeUser("123").collect {
        emissions.add(it)
    }

    assertEquals(2, emissions.size)
    assertEquals("John", emissions[0].name)
    assertEquals("John Updated", emissions[1].name)
}
```

### Testing Exceptions

```kotlin
@Test
fun `test exception handling`() = runTest {
    val repository = mockk<UserRepository>()

    coEvery { repository.getUser("123") } throws IOException("Network error")

    assertThrows<IOException> {
        repository.getUser("123")
    }
}
```

### Chaining Answers

```kotlin
@Test
fun `multiple answers in sequence`() {
    val repository = mockk<UserRepository>()

    every { repository.getStatus() } returnsMany listOf(
        "loading",
        "success",
        "done"
    )

    assertEquals("loading", repository.getStatus())
    assertEquals("success", repository.getStatus())
    assertEquals("done", repository.getStatus())
}
```

## MockK vs Mockito

| Feature | MockK | Mockito |
|---------|-------|---------|
| Kotlin Support | ✅ Excellent | ⚠️ Limited |
| Final Classes | ✅ No issue | ⚠️ Needs mockito-inline |
| Extension Functions | ✅ Supported | ❌ Not supported |
| Suspend Functions | ✅ `coEvery` | ⚠️ Complex workaround |
| DSL Syntax | ✅ Concise | ⚠️ Verbose |
| Relaxed Mocks | ✅ Built-in | ⚠️ Manual |

**Recommendation**: Use MockK for Kotlin projects. Only use Mockito for legacy Java codebases.
