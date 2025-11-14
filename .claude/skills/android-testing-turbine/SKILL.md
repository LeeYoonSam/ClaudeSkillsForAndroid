---
name: android-testing-turbine
description: Small testing library for Kotlin Flows with awaitItem(), awaitComplete(), and awaitError(). Use when testing Flow emissions in ViewModels and Repositories.
---

# Turbine Flow Testing

Fluent testing library for Kotlin Flows with simple, readable assertions.

## When to Use
- Testing Flow emissions in ViewModels
- Testing StateFlow/SharedFlow updates
- Verifying Flow completion and errors
- Testing Flow transformations
- Asserting emission order and timing

## Dependencies

```kotlin
// libs.versions.toml
[versions]
turbine = "1.1.0"
coroutines-test = "1.9.0"

[libraries]
turbine = { group = "app.cash.turbine", name = "turbine", version.ref = "turbine" }
coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "coroutines-test" }

// build.gradle.kts
dependencies {
    testImplementation(libs.turbine)
    testImplementation(libs.coroutines.test)
}
```

## Basic Testing

```kotlin
import app.cash.turbine.test
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.test.runTest
import org.junit.Test
import kotlin.test.assertEquals

class FlowTest {

    @Test
    fun `test basic flow emissions`() = runTest {
        // Given
        val flow = flow {
            emit(1)
            emit(2)
            emit(3)
        }

        // When/Then
        flow.test {
            assertEquals(1, awaitItem())
            assertEquals(2, awaitItem())
            assertEquals(3, awaitItem())
            awaitComplete()
        }
    }

    @Test
    fun `test flow with error`() = runTest {
        val flow = flow<Int> {
            emit(1)
            throw Exception("Error occurred")
        }

        flow.test {
            assertEquals(1, awaitItem())
            val error = awaitError()
            assertEquals("Error occurred", error.message)
        }
    }
}
```

## Testing StateFlow

```kotlin
class UserViewModel : ViewModel() {
    private val _state = MutableStateFlow(UserState())
    val state: StateFlow<UserState> = _state.asStateFlow()

    fun loadUser() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            delay(100)
            _state.update { it.copy(isLoading = false, user = loadedUser) }
        }
    }
}

class UserViewModelTest {

    @Test
    fun `loadUser emits loading then success states`() = runTest {
        // Given
        val viewModel = UserViewModel()

        viewModel.state.test {
            // Initial state
            assertEquals(UserState(), awaitItem())

            // Trigger load
            viewModel.loadUser()

            // Loading state
            val loadingState = awaitItem()
            assertTrue(loadingState.isLoading)

            // Success state
            val successState = awaitItem()
            assertFalse(successState.isLoading)
            assertNotNull(successState.user)
        }
    }
}
```

## Testing ViewModel Actions

```kotlin
class ProductViewModel(
    private val repository: ProductRepository
) : ViewModel() {

    private val _state = MutableStateFlow(ProductState())
    val state: StateFlow<ProductState> = _state.asStateFlow()

    fun search(query: String) {
        viewModelScope.launch {
            _state.update { it.copy(isSearching = true) }

            repository.search(query)
                .collect { products ->
                    _state.update {
                        it.copy(
                            isSearching = false,
                            products = products
                        )
                    }
                }
        }
    }
}

class ProductViewModelTest {

    @Test
    fun `search emits searching then results`() = runTest {
        // Given
        val repository = mockk<ProductRepository>()
        coEvery { repository.search(any()) } returns flowOf(
            listOf(Product("1", "Product 1"))
        )

        val viewModel = ProductViewModel(repository)

        viewModel.state.test {
            // Skip initial state
            awaitItem()

            // Trigger search
            viewModel.search("test")

            // Searching state
            val searchingState = awaitItem()
            assertTrue(searchingState.isSearching)

            // Results state
            val resultsState = awaitItem()
            assertFalse(resultsState.isSearching)
            assertEquals(1, resultsState.products.size)
        }
    }
}
```

## Advanced Patterns

### Skip Initial Emission

```kotlin
@Test
fun `skip initial value and test updates`() = runTest {
    val viewModel = UserViewModel()

    viewModel.state.test {
        // Skip initial state
        skipItems(1)

        viewModel.updateName("New Name")

        val state = awaitItem()
        assertEquals("New Name", state.name)
    }
}
```

### Test with Timeout

```kotlin
@Test
fun `test emission with timeout`() = runTest {
    val flow = flow {
        delay(500)
        emit("value")
    }

    flow.test(timeout = 1000.milliseconds) {
        assertEquals("value", awaitItem())
        awaitComplete()
    }
}
```

### Expect Most Recent Item

```kotlin
@Test
fun `test most recent emission`() = runTest {
    val viewModel = UserViewModel()

    viewModel.state.test {
        awaitItem()  // Initial

        // Rapid updates
        viewModel.update1()
        viewModel.update2()
        viewModel.update3()

        // Skip intermediate states, get most recent
        val state = expectMostRecentItem()
        assertEquals(3, state.updateCount)
    }
}
```

### Cancel and Ignore Remaining

```kotlin
@Test
fun `test cancellation`() = runTest {
    val flow = flow {
        emit(1)
        emit(2)
        // More emissions that we don't care about
        emit(3)
        emit(4)
    }

    flow.test {
        assertEquals(1, awaitItem())
        assertEquals(2, awaitItem())

        // Cancel and ignore remaining
        cancelAndIgnoreRemainingEvents()
    }
}
```

## Testing Repository Flows

```kotlin
class UserRepository(
    private val api: UserApi,
    private val dao: UserDao
) {
    fun observeUser(id: String): Flow<User> = flow {
        // Emit cached data first
        dao.getUser(id)?.let { emit(it) }

        // Fetch from API
        try {
            val user = api.getUser(id)
            dao.insertUser(user)
            emit(user)
        } catch (e: Exception) {
            // Ignore, keep cached data
        }
    }.distinctUntilChanged()
}

class UserRepositoryTest {

    @Test
    fun `observeUser emits cache then API data`() = runTest {
        // Given
        val dao = mockk<UserDao>()
        val api = mockk<UserApi>()
        every { dao.getUser("123") } returns cachedUser
        coEvery { api.getUser("123") } returns freshUser
        every { dao.insertUser(any()) } just Runs

        val repository = UserRepository(api, dao)

        // When/Then
        repository.observeUser("123").test {
            // Cached data
            val cached = awaitItem()
            assertEquals("Cached Name", cached.name)

            // Fresh data
            val fresh = awaitItem()
            assertEquals("Fresh Name", fresh.name)

            awaitComplete()
        }
    }
}
```

## Testing SharedFlow Events

```kotlin
class UserViewModel : ViewModel() {
    private val _events = MutableSharedFlow<UserEvent>()
    val events: SharedFlow<UserEvent> = _events.asSharedFlow()

    fun deleteUser() {
        viewModelScope.launch {
            // Delete logic
            _events.emit(UserEvent.Deleted)
        }
    }
}

class UserViewModelTest {

    @Test
    fun `deleteUser emits Deleted event`() = runTest {
        val viewModel = UserViewModel()

        viewModel.events.test {
            // Trigger action
            viewModel.deleteUser()

            // Verify event
            val event = awaitItem()
            assertTrue(event is UserEvent.Deleted)
        }
    }

    @Test
    fun `multiple events in order`() = runTest {
        val viewModel = UserViewModel()

        viewModel.events.test {
            viewModel.deleteUser()
            viewModel.refreshList()

            assertEquals(UserEvent.Deleted, awaitItem())
            assertEquals(UserEvent.Refreshed, awaitItem())
        }
    }
}
```

## Testing Flow Transformations

```kotlin
@Test
fun `test map transformation`() = runTest {
    val source = flowOf(1, 2, 3)

    source.map { it * 2 }.test {
        assertEquals(2, awaitItem())
        assertEquals(4, awaitItem())
        assertEquals(6, awaitItem())
        awaitComplete()
    }
}

@Test
fun `test filter transformation`() = runTest {
    val source = flowOf(1, 2, 3, 4, 5)

    source.filter { it % 2 == 0 }.test {
        assertEquals(2, awaitItem())
        assertEquals(4, awaitItem())
        awaitComplete()
    }
}

@Test
fun `test combine flows`() = runTest {
    val flow1 = flowOf("A", "B")
    val flow2 = flowOf(1, 2)

    combine(flow1, flow2) { a, b -> "$a$b" }.test {
        awaitItem()  // First combination
        awaitItem()  // Second combination
        awaitItem()  // Third combination
        awaitComplete()
    }
}
```

## Testing with Delays

```kotlin
@Test
fun `test flow with debounce`() = runTest {
    val flow = flow {
        emit("a")
        delay(100)
        emit("b")
        delay(100)
        emit("c")
    }.debounce(50)

    flow.test {
        assertEquals("a", awaitItem())
        assertEquals("b", awaitItem())
        assertEquals("c", awaitItem())
        awaitComplete()
    }
}

@Test
fun `test polling flow`() = runTest {
    var counter = 0
    val flow = flow {
        while (counter < 3) {
            emit(counter++)
            delay(100)
        }
    }

    flow.test {
        assertEquals(0, awaitItem())
        assertEquals(1, awaitItem())
        assertEquals(2, awaitItem())
        awaitComplete()
    }
}
```

## Testing Error Handling

```kotlin
@Test
fun `test retry on error`() = runTest {
    var attempts = 0
    val flow = flow {
        attempts++
        if (attempts < 3) {
            throw Exception("Retry")
        }
        emit("Success")
    }.retry(2)

    flow.test {
        assertEquals("Success", awaitItem())
        awaitComplete()
    }

    assertEquals(3, attempts)
}

@Test
fun `test catch and emit default`() = runTest {
    val flow = flow<String> {
        throw Exception("Error")
    }.catch { emit("Default") }

    flow.test {
        assertEquals("Default", awaitItem())
        awaitComplete()
    }
}
```

## Related Skills
- android-testing-mockk: Mocking dependencies
- android-stateflow: StateFlow/SharedFlow
- android-coroutines: Coroutines testing
- android-mvvm-architecture: ViewModel patterns

## Best Practices

1. **Use `test` block**: Always wrap Flow testing in `.test {}`
2. **Assert order**: Use `awaitItem()` to verify emission order
3. **Complete or error**: Always end with `awaitComplete()` or `awaitError()`
4. **Skip unwanted emissions**: Use `skipItems()` for intermediate values
5. **Timeout**: Set appropriate timeout for slow flows
6. **Cancel properly**: Use `cancelAndIgnoreRemainingEvents()` when needed
7. **Test scope**: Use `runTest` for proper coroutine testing

## Common Patterns

### Pagination Testing

```kotlin
@Test
fun `test paginated flow`() = runTest {
    val viewModel = ProductListViewModel()

    viewModel.products.test {
        val page1 = awaitItem()
        assertEquals(20, page1.size)

        viewModel.loadNextPage()

        val page2 = awaitItem()
        assertEquals(40, page2.size)
    }
}
```

### Search with Debounce

```kotlin
@Test
fun `test search debounce`() = runTest {
    val viewModel = SearchViewModel()

    viewModel.results.test {
        awaitItem()  // Empty initial

        viewModel.onQueryChanged("a")
        viewModel.onQueryChanged("ab")
        viewModel.onQueryChanged("abc")

        // Only last query emits after debounce
        val results = awaitItem()
        assertTrue(results.isNotEmpty())
    }
}
```

### Loading State Testing

```kotlin
@Test
fun `test loading states`() = runTest {
    val viewModel = DataViewModel()

    viewModel.state.test {
        // Initial
        val initial = awaitItem()
        assertFalse(initial.isLoading)

        // Start loading
        viewModel.load()

        // Loading
        val loading = awaitItem()
        assertTrue(loading.isLoading)

        // Loaded
        val loaded = awaitItem()
        assertFalse(loaded.isLoading)
        assertNotNull(loaded.data)
    }
}
```

## Turbine vs Manual Testing

| Approach | Code |
|----------|------|
| **Manual** | `val emissions = mutableListOf<T>()` <br> `flow.collect { emissions.add(it) }` <br> `assertEquals(expected, emissions[0])` |
| **Turbine** | `flow.test {` <br> `  assertEquals(expected, awaitItem())` <br> `}` |

**Advantage**: Turbine provides:
- ✅ Cleaner, more readable syntax
- ✅ Built-in timeout handling
- ✅ Automatic completion verification
- ✅ Better error messages

**Recommendation**: Always use Turbine for Flow testing. It's concise, powerful, and catches common mistakes.
