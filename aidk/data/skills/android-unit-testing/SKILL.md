---
name: android-unit-testing
description: Create unit tests for ViewModels and business logic with JUnit, MockK, and Coroutine testing. Use when testing logic without Android dependencies.
---

# Unit Testing

Test ViewModels and business logic with JUnit and MockK.

## Dependencies

```kotlin
testImplementation("junit:junit:4.13.2")
testImplementation("io.mockk:mockk:1.13.8")
testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
testImplementation("app.cash.turbine:turbine:1.0.0")
```

## ViewModel Testing

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModelTest {

    private lateinit var viewModel: HomeViewModel
    private lateinit var repository: UserRepository
    private val testDispatcher = UnconfinedTestDispatcher()

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = mockk()
        viewModel = HomeViewModel(repository)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `loadUsers updates state with users on success`() = runTest {
        // Given
        val users = listOf(User("1", "John"))
        coEvery { repository.getUsers() } returns Result.success(users)

        // When
        viewModel.loadUsers()

        // Then
        assertEquals(users, viewModel.state.value.users)
        assertFalse(viewModel.state.value.isLoading)
    }

    @Test
    fun `loadUsers updates state with error on failure`() = runTest {
        // Given
        val error = "Network error"
        coEvery { repository.getUsers() } returns Result.failure(Exception(error))

        // When
        viewModel.loadUsers()

        // Then
        assertTrue(viewModel.state.value.users.isEmpty())
        assertEquals(error, viewModel.state.value.error)
    }
}
```

## Testing Flows

```kotlin
@Test
fun `state flow emits correct values`() = runTest {
    viewModel.state.test {
        // Initial state
        assertEquals(HomeState(), awaitItem())

        viewModel.loadData()

        // Loading state
        assertEquals(HomeState(isLoading = true), awaitItem())

        // Success state
        val successState = awaitItem()
        assertFalse(successState.isLoading)
        assertTrue(successState.data.isNotEmpty())
    }
}
```

## MockK Basics

```kotlin
// Create mock
val repository = mockk<UserRepository>()

// Stub method
coEvery { repository.getUsers() } returns Result.success(users)

// Verify call
coVerify { repository.getUsers() }
coVerify(exactly = 1) { repository.getUsers() }
coVerify(exactly = 0) { repository.deleteUser(any()) }

// Argument capture
val slot = slot<String>()
coEvery { repository.getUserById(capture(slot)) } returns Result.success(user)
viewModel.loadUser("123")
assertEquals("123", slot.captured)
```

## Repository Testing

```kotlin
class UserRepositoryImplTest {

    private lateinit var repository: UserRepositoryImpl
    private lateinit var api: UserApi
    private lateinit var dao: UserDao

    @Before
    fun setup() {
        api = mockk()
        dao = mockk()
        repository = UserRepositoryImpl(api, dao)
    }

    @Test
    fun `getUsers returns cached data when available`() = runTest {
        // Given
        val cachedUsers = listOf(UserEntity("1", "John"))
        coEvery { dao.getAllUsers() } returns cachedUsers

        // When
        val result = repository.getUsers()

        // Then
        assertTrue(result.isSuccess)
        coVerify(exactly = 0) { api.getUsers() }
    }
}
```

## Best Practices
1. Use `runTest` for suspend functions
2. Set test dispatcher with `Dispatchers.setMain()`
3. Mock dependencies with MockK
4. Test all branches (success, error, edge cases)
5. Use Turbine for Flow testing
6. Verify mock interactions
