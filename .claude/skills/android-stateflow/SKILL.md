---
name: android-stateflow
description: Manage UI state with StateFlow and SharedFlow in ViewModels. Use when exposing observable state from ViewModel to UI with Coroutines.
---

# StateFlow State Management

Manage reactive UI state with StateFlow and SharedFlow.

## When to Use
- Exposing state from ViewModel
- Reactive UI updates
- Lifecycle-aware state collection
- Hot state streams

## StateFlow Basics

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor() : ViewModel() {

    // Private mutable state
    private val _state = MutableStateFlow(HomeState())
    // Public immutable state
    val state: StateFlow<HomeState> = _state.asStateFlow()

    fun updateState() {
        _state.update { currentState ->
            currentState.copy(isLoading = true)
        }
    }
}

data class HomeState(
    val isLoading: Boolean = false,
    val data: List<String> = emptyList(),
    val error: String? = null
)
```

## Collect in Compose

```kotlin
@Composable
fun HomeScreen(viewModel: HomeViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    // UI based on state
    if (state.isLoading) {
        LoadingIndicator()
    }
}
```

## Collect in Fragment/Activity

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            updateUI(state)
        }
    }
}
```

## SharedFlow for Events

```kotlin
private val _events = MutableSharedFlow<Event>()
val events: SharedFlow<Event> = _events.asSharedFlow()

fun sendEvent() {
    viewModelScope.launch {
        _events.emit(Event.ShowMessage("Hello"))
    }
}
```

## Derived State

```kotlin
val isButtonEnabled: StateFlow<Boolean> = state
    .map { it.name.isNotEmpty() && it.email.isNotEmpty() }
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = false
    )
```

## Combine Multiple Flows

```kotlin
val combinedState: StateFlow<CombinedState> = combine(
    flow1,
    flow2,
    flow3
) { a, b, c ->
    CombinedState(a, b, c)
}.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5000),
    initialValue = CombinedState()
)
```

## Best Practices
1. Use `StateFlow` for state, `SharedFlow` for events
2. Expose immutable `StateFlow`, keep `MutableStateFlow` private
3. Use `update { }` for thread-safe state updates
4. Use `collectAsStateWithLifecycle()` in Compose
5. Use `SharingStarted.WhileSubscribed(5000)` for derived state
