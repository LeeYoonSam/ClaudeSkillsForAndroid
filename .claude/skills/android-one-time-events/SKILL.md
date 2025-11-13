---
name: android-one-time-events
description: Handle one-time UI events like navigation or toasts using Channels or SharedFlow. Use when triggering actions that shouldn't repeat on recomposition.
---

# One-Time Events

Handle one-time UI events that shouldn't repeat on configuration changes.

## When to Use
- Navigation events
- Show toast/snackbar
- Show dialog
- Trigger animations
- Events that shouldn't replay

## Using Channel

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor() : ViewModel() {

    private val _events = Channel<HomeEvent>()
    val events = _events.receiveAsFlow()

    fun onAction() {
        viewModelScope.launch {
            _events.send(HomeEvent.Navigate("detail"))
        }
    }
}

sealed interface HomeEvent {
    data class Navigate(val route: String) : HomeEvent
    data class ShowMessage(val message: String) : HomeEvent
    data class ShowError(val error: String) : HomeEvent
}
```

## Collect Events in Compose

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigate: (String) -> Unit
) {
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is HomeEvent.Navigate -> onNavigate(event.route)
                is HomeEvent.ShowMessage -> {
                    // Show snackbar
                }
                is HomeEvent.ShowError -> {
                    // Show error dialog
                }
            }
        }
    }
}
```

## Using SharedFlow

```kotlin
private val _events = MutableSharedFlow<Event>(
    replay = 0,
    extraBufferCapacity = 1,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
val events: SharedFlow<Event> = _events.asSharedFlow()
```

## Best Practices
1. Use `Channel` for one-time events
2. Handle events in UI layer, not ViewModel
3. Use sealed interface for type-safe events
4. Don't use StateFlow for events
5. Collect in `LaunchedEffect` in Compose
