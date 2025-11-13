---
name: android-mvvm-architecture
description: Create MVVM architecture pattern with ViewModel, StateFlow, and Unidirectional Data Flow for Android. Use when implementing UI logic and state management.
---

# MVVM Architecture for Android

Implement Model-View-ViewModel pattern with modern Android practices including StateFlow and Unidirectional Data Flow (UDF).

## When to Use
- Building new UI screens
- Managing UI state and logic
- Handling user interactions
- Implementing reactive UI updates
- Separating UI from business logic

## MVVM Components

```
┌──────────────┐
│     View     │  Composable/Activity/Fragment
│   (UI Layer) │  - Displays UI
└──────┬───────┘  - Observes State
       │          - Sends Actions
       │ observes StateFlow
       │ calls methods
       ▼
┌──────────────┐
│  ViewModel   │  - Manages UI State
│              │  - Handles user actions
└──────┬───────┘  - Calls Use Cases/Repository
       │
       │ accesses
       ▼
┌──────────────┐
│    Model     │  Repository/UseCase
│ (Data Layer) │  - Business logic
└──────────────┘  - Data access
```

## Unidirectional Data Flow (UDF)

```
     ┌─────────────────────────────┐
     │                             │
     │                             ▼
┌────────┐    Action    ┌────────────────┐
│   UI   │─────────────>│   ViewModel    │
│  View  │              │                │
└────────┘              └────────┬───────┘
     ▲                           │
     │         State             │ calls
     │                           ▼
     │                  ┌────────────────┐
     └──────────────────│  Repository    │
                        └────────────────┘
```

**Principles:**
- State flows down from ViewModel to UI
- Events/Actions flow up from UI to ViewModel
- ViewModel is the single source of truth for UI state

## ViewModel Implementation

### Basic ViewModel Structure

```kotlin
@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val getProductsUseCase: GetProductsUseCase,
    private val addToCartUseCase: AddToCartUseCase
) : ViewModel() {

    // Private mutable state (only ViewModel can modify)
    private val _state = MutableStateFlow(ProductListState())
    // Public immutable state (UI can only observe)
    val state: StateFlow<ProductListState> = _state.asStateFlow()

    // One-time events channel
    private val _events = Channel<ProductListEvent>()
    val events = _events.receiveAsFlow()

    init {
        loadProducts()
    }

    // Single entry point for user actions
    fun onAction(action: ProductListAction) {
        when (action) {
            is ProductListAction.LoadProducts -> loadProducts()
            is ProductListAction.RefreshProducts -> refreshProducts()
            is ProductListAction.AddToCart -> addToCart(action.productId)
            is ProductListAction.SearchProducts -> searchProducts(action.query)
            is ProductListAction.FilterByCategory -> filterByCategory(action.category)
        }
    }

    private fun loadProducts() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }

            getProductsUseCase()
                .onSuccess { products ->
                    _state.update {
                        it.copy(
                            products = products,
                            isLoading = false,
                            error = null
                        )
                    }
                }
                .onFailure { error ->
                    _state.update {
                        it.copy(
                            isLoading = false,
                            error = error.message ?: "Unknown error"
                        )
                    }
                }
        }
    }

    private fun refreshProducts() {
        viewModelScope.launch {
            _state.update { it.copy(isRefreshing = true) }

            getProductsUseCase(forceRefresh = true)
                .onSuccess { products ->
                    _state.update {
                        it.copy(
                            products = products,
                            isRefreshing = false
                        )
                    }
                    _events.send(ProductListEvent.ShowMessage("Products refreshed"))
                }
                .onFailure { error ->
                    _state.update { it.copy(isRefreshing = false) }
                    _events.send(ProductListEvent.ShowError(error.message))
                }
        }
    }

    private fun addToCart(productId: String) {
        viewModelScope.launch {
            addToCartUseCase(productId)
                .onSuccess {
                    _events.send(ProductListEvent.ShowMessage("Added to cart"))
                    _events.send(ProductListEvent.NavigateToCart)
                }
                .onFailure { error ->
                    _events.send(ProductListEvent.ShowError(error.message))
                }
        }
    }

    private fun searchProducts(query: String) {
        _state.update { it.copy(searchQuery = query) }

        viewModelScope.launch {
            delay(300) // Debounce
            // Perform search
        }
    }

    private fun filterByCategory(category: String) {
        _state.update { it.copy(selectedCategory = category) }
        loadProducts()
    }
}
```

### State Definition

```kotlin
data class ProductListState(
    val products: List<Product> = emptyList(),
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val error: String? = null,
    val searchQuery: String = "",
    val selectedCategory: String = "All"
)
```

### Action Definition

```kotlin
sealed interface ProductListAction {
    data object LoadProducts : ProductListAction
    data object RefreshProducts : ProductListAction
    data class AddToCart(val productId: String) : ProductListAction
    data class SearchProducts(val query: String) : ProductListAction
    data class FilterByCategory(val category: String) : ProductListAction
}
```

### Event Definition

```kotlin
sealed interface ProductListEvent {
    data class ShowMessage(val message: String) : ProductListEvent
    data class ShowError(val message: String?) : ProductListEvent
    data object NavigateToCart : ProductListEvent
}
```

## UI Implementation (Compose)

### Screen Composable

```kotlin
@Composable
fun ProductListScreen(
    viewModel: ProductListViewModel = hiltViewModel(),
    onNavigateToCart: () -> Unit
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    // Handle one-time events
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is ProductListEvent.ShowMessage -> {
                    // Show snackbar
                }
                is ProductListEvent.ShowError -> {
                    // Show error dialog
                }
                is ProductListEvent.NavigateToCart -> {
                    onNavigateToCart()
                }
            }
        }
    }

    ProductListContent(
        state = state,
        onAction = viewModel::onAction
    )
}

@Composable
private fun ProductListContent(
    state: ProductListState,
    onAction: (ProductListAction) -> Unit
) {
    Column(modifier = Modifier.fillMaxSize()) {
        SearchBar(
            query = state.searchQuery,
            onQueryChange = { query ->
                onAction(ProductListAction.SearchProducts(query))
            }
        )

        CategoryFilter(
            selectedCategory = state.selectedCategory,
            onCategorySelected = { category ->
                onAction(ProductListAction.FilterByCategory(category))
            }
        )

        when {
            state.isLoading -> {
                LoadingIndicator()
            }
            state.error != null -> {
                ErrorView(
                    message = state.error,
                    onRetry = { onAction(ProductListAction.LoadProducts) }
                )
            }
            state.products.isEmpty() -> {
                EmptyView()
            }
            else -> {
                ProductList(
                    products = state.products,
                    onProductClick = { product ->
                        // Navigate to detail
                    },
                    onAddToCart = { productId ->
                        onAction(ProductListAction.AddToCart(productId))
                    }
                )
            }
        }
    }
}
```

### State Collection in Compose

```kotlin
// Recommended: Lifecycle-aware collection
val state by viewModel.state.collectAsStateWithLifecycle()

// Alternative for simple cases
val state by viewModel.state.collectAsState()
```

## UI Implementation (XML + Fragment/Activity)

### Fragment Example

```kotlin
@AndroidEntryPoint
class ProductListFragment : Fragment() {

    private val viewModel: ProductListViewModel by viewModels()
    private var _binding: FragmentProductListBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProductListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupViews()
        observeState()
        observeEvents()
    }

    private fun setupViews() {
        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                query?.let { viewModel.onAction(ProductListAction.SearchProducts(it)) }
                return true
            }

            override fun onQueryTextChange(newText: String?): Boolean {
                newText?.let { viewModel.onAction(ProductListAction.SearchProducts(it)) }
                return true
            }
        })

        binding.swipeRefresh.setOnRefreshListener {
            viewModel.onAction(ProductListAction.RefreshProducts)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    updateUI(state)
                }
            }
        }
    }

    private fun observeEvents() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.events.collect { event ->
                    handleEvent(event)
                }
            }
        }
    }

    private fun updateUI(state: ProductListState) {
        binding.swipeRefresh.isRefreshing = state.isRefreshing
        binding.progressBar.isVisible = state.isLoading
        binding.errorView.isVisible = state.error != null
        binding.recyclerView.isVisible = !state.isLoading && state.error == null

        state.error?.let {
            binding.errorText.text = it
        }

        // Update adapter
        productAdapter.submitList(state.products)
    }

    private fun handleEvent(event: ProductListEvent) {
        when (event) {
            is ProductListEvent.ShowMessage -> {
                Snackbar.make(binding.root, event.message, Snackbar.LENGTH_SHORT).show()
            }
            is ProductListEvent.ShowError -> {
                Toast.makeText(context, event.message, Toast.LENGTH_SHORT).show()
            }
            is ProductListEvent.NavigateToCart -> {
                findNavController().navigate(R.id.action_list_to_cart)
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

## Advanced Patterns

### Complex State Management

```kotlin
@HiltViewModel
class CheckoutViewModel @Inject constructor(
    private val cartRepository: CartRepository,
    private val orderRepository: OrderRepository,
    private val paymentService: PaymentService
) : ViewModel() {

    private val _state = MutableStateFlow(CheckoutState())
    val state: StateFlow<CheckoutState> = _state.asStateFlow()

    // Derived state (computed from main state)
    val totalPrice: StateFlow<Double> = state
        .map { it.cartItems.sumOf { item -> item.price * item.quantity } }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = 0.0
        )

    val canProceed: StateFlow<Boolean> = state
        .map { it.shippingAddress != null && it.paymentMethod != null }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = false
        )

    fun onAction(action: CheckoutAction) {
        // Handle actions
    }
}
```

### SavedStateHandle for Process Death

```kotlin
@HiltViewModel
class FormViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _state = MutableStateFlow(
        savedStateHandle.get<FormState>("form_state") ?: FormState()
    )
    val state: StateFlow<FormState> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            state.collect { newState ->
                savedStateHandle["form_state"] = newState
            }
        }
    }

    fun onAction(action: FormAction) {
        when (action) {
            is FormAction.UpdateName -> {
                _state.update { it.copy(name = action.name) }
            }
            // ...
        }
    }
}
```

## Testing ViewModels

```kotlin
class ProductListViewModelTest {

    private lateinit var viewModel: ProductListViewModel
    private lateinit var getProductsUseCase: GetProductsUseCase
    private val testDispatcher = UnconfinedTestDispatcher()

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        getProductsUseCase = mock()
        viewModel = ProductListViewModel(getProductsUseCase)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `when products loaded successfully, state should contain products`() = runTest {
        // Given
        val products = listOf(Product("1", "Product 1"))
        whenever(getProductsUseCase()).thenReturn(Result.success(products))

        // When
        viewModel.onAction(ProductListAction.LoadProducts)

        // Then
        val state = viewModel.state.value
        assertFalse(state.isLoading)
        assertEquals(products, state.products)
        assertNull(state.error)
    }

    @Test
    fun `when products loading fails, state should contain error`() = runTest {
        // Given
        val errorMessage = "Network error"
        whenever(getProductsUseCase()).thenReturn(Result.failure(Exception(errorMessage)))

        // When
        viewModel.onAction(ProductListAction.LoadProducts)

        // Then
        val state = viewModel.state.value
        assertFalse(state.isLoading)
        assertTrue(state.products.isEmpty())
        assertEquals(errorMessage, state.error)
    }
}
```

## Related Skills
- **android-stateflow**: For detailed StateFlow patterns
- **android-one-time-events**: For handling one-time UI events
- **android-compose-ui**: For Compose UI implementation
- **android-clean-architecture**: For overall architecture structure
- **android-hilt-di**: For ViewModel injection
- **android-unit-testing**: For ViewModel testing

## Best Practices

1. **Single State Object**: Use one data class for all UI state
2. **Immutable State**: Expose `StateFlow<T>`, keep `MutableStateFlow<T>` private
3. **State Updates**: Use `update { }` for atomic state changes
4. **One-Time Events**: Use `Channel` or `SharedFlow` for navigation/toasts
5. **Single Action Method**: `onAction()` as single entry point
6. **ViewModelScope**: Use `viewModelScope` for coroutines
7. **No Android Dependencies**: Don't reference Context, Activity, View in ViewModel
8. **State Restoration**: Use SavedStateHandle for process death
9. **Derived State**: Use `map()` and `combine()` for computed properties
10. **Error Handling**: Always handle `Result` failures
11. **Loading States**: Include loading, error, empty states
12. **Lifecycle Awareness**: Use `collectAsStateWithLifecycle()` in Compose
