---
name: android-coroutines
description: Implement Kotlin Coroutines for asynchronous operations with proper scope and dispatcher management. Use when handling network calls, database operations, or background tasks.
---

# Kotlin Coroutines

Implement structured concurrency with Kotlin Coroutines.

## When to Use
- Asynchronous operations
- Network requests
- Database operations
- Background processing
- Sequential/parallel tasks

## Coroutine Scopes

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor() : ViewModel() {

    // viewModelScope - cancelled when ViewModel is cleared
    fun loadData() {
        viewModelScope.launch {
            // Coroutine code
        }
    }
}

// In Activity/Fragment
class HomeFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        // lifecycleScope - tied to lifecycle
        lifecycleScope.launch {
            // Coroutine code
        }

        // viewLifecycleOwner.lifecycleScope for fragments
        viewLifecycleOwner.lifecycleScope.launch {
            // Coroutine code
        }
    }
}
```

## Dispatchers

```kotlin
viewModelScope.launch {
    // Main dispatcher (default)
    updateUI()

    withContext(Dispatchers.IO) {
        // IO dispatcher - network, disk operations
        val data = fetchFromNetwork()
    }

    withContext(Dispatchers.Default) {
        // Default dispatcher - CPU-intensive work
        val result = processLargeData()
    }

    withContext(Dispatchers.Main) {
        // Main dispatcher - UI updates
        updateUI(result)
    }
}
```

## Async/Await

```kotlin
suspend fun loadData() = coroutineScope {
    // Parallel execution
    val user = async { getUserFromApi() }
    val products = async { getProductsFromApi() }
    val orders = async { getOrdersFromApi() }

    // Wait for all
    UserData(
        user = user.await(),
        products = products.await(),
        orders = orders.await()
    )
}
```

## Error Handling

```kotlin
viewModelScope.launch {
    try {
        val result = apiCall()
        _state.update { it.copy(data = result) }
    } catch (e: Exception) {
        _state.update { it.copy(error = e.message) }
    }
}

// With supervisorScope
supervisorScope {
    launch { task1() } // If fails, doesn't cancel other tasks
    launch { task2() }
}
```

## Flow Operations

```kotlin
repository.getUsers()
    .map { users -> users.filter { it.isActive } }
    .flowOn(Dispatchers.IO)
    .catch { e -> emit(emptyList()) }
    .collect { users -> 
        _state.update { it.copy(users = users) }
    }
```

## Best Practices
1. Use `viewModelScope` in ViewModels
2. Use appropriate dispatcher for task type
3. Handle exceptions with try-catch
4. Use `async/await` for parallel tasks
5. Don't use `GlobalScope`
6. Cancel coroutines when no longer needed
