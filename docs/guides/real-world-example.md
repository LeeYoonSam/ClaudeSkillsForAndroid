# 실제 개발 예시: 쇼핑몰 상품 기능 구현

## 시나리오

PM으로부터 받은 요구사항:
> "사용자가 상품 목록을 보고, 상품을 검색하고, 상품 상세 정보를 확인할 수 있는 기능이 필요합니다.
> 상품은 API에서 가져오고, 오프라인에서도 마지막 조회 데이터를 볼 수 있어야 합니다."

---

## Step 1: SPEC 생성

### 1.1 요구사항 분석

PM 요구사항을 EARS 형식으로 변환:

```
Ubiquitous (항상 참):
- 상품 목록을 API에서 가져온다
- 상품을 로컬 DB에 캐싱한다
- 상품 상세 정보를 보여준다

Event-driven (사용자 액션):
- 사용자가 검색어를 입력하면 필터링한다
- 사용자가 상품을 클릭하면 상세 화면으로 이동한다
- 사용자가 새로고침하면 최신 데이터를 가져온다

State-driven (상태 기반):
- 네트워크가 없으면 캐시된 데이터를 보여준다
- 로딩 중이면 스켈레톤 UI를 보여준다

Unwanted (원하지 않는 동작):
- API 오류가 발생해도 앱이 크래시되지 않는다
- 빈 목록일 때 "No data" 메시지를 보여준다
```

### 1.2 SPEC 생성 실행

```bash
python3 tools/spec_builder.py interactive
```

**입력 내용**:
```
Feature name: Product Catalog
Purpose: Display product list with search and detail view, supporting offline mode

Requirements:
1. fetch products from API
2. cache products in local database
3. display product list with images
4. filter products by search query
5. navigate to product detail on click
6. show loading state while fetching
7. show cached data when offline
8. handle API errors gracefully
9. show empty state when no products
10. refresh data on pull-to-refresh
done
```

**생성 결과**:
```
✓ SPEC created successfully!
Location: specs/examples/product-catalog/SPEC.md
SPEC ID: SPEC-002
Requirements: 10
Related Skills: 10
  - android-compose-ui
  - android-list-ui
  - android-networking-retrofit
  - android-database-room
  - android-repository-pattern
  - android-image-loading
  - android-hilt-di
  - android-clean-architecture
  - android-mvvm-architecture
  - android-stateflow
```

### 1.3 SPEC 수정 및 보완

생성된 SPEC을 열어서 비즈니스 로직을 상세화:

```bash
# SPEC 파일 열기
code specs/examples/product-catalog/SPEC.md
```

**추가/수정 내용**:

1. **Data Models 정의**:
```kotlin
data class Product(
    val id: String,
    val name: String,
    val description: String,
    val price: Double,
    val imageUrl: String,
    val category: String,
    val stock: Int,
    val rating: Double,
    val createdAt: Instant,
)
```

2. **API Endpoints 명시**:
```
GET /api/products?page=1&limit=20&search=query
POST /api/products (admin only)
GET /api/products/{id}
```

3. **UI 요구사항 추가**:
- 그리드 레이아웃 (2 columns)
- 상품 이미지 + 이름 + 가격 표시
- 검색바 상단 고정
- 무한 스크롤 (Paging3)

---

## Step 2: 코드 생성

### 2.1 초기 코드 생성

```bash
python3 tools/code_builder.py generate \
  specs/examples/product-catalog/SPEC.md \
  --output examples/shopping-app \
  --package com.example.shopping
```

**생성된 파일**:
```
examples/shopping-app/
├── src/main/kotlin/com/example/shopping/
│   ├── domain/
│   │   ├── model/ProductCatalog.kt
│   │   ├── usecase/GetProductCatalogUseCase.kt
│   │   └── repository/ProductCatalogRepository.kt
│   ├── data/
│   │   ├── remote/ProductCatalogApi.kt
│   │   ├── remote/ProductCatalogDto.kt
│   │   ├── local/ProductCatalogEntity.kt
│   │   ├── local/ProductCatalogDao.kt
│   │   └── repository/ProductCatalogRepositoryImpl.kt
│   └── presentation/
│       ├── viewmodel/ProductCatalogViewModel.kt
│       ├── state/ProductCatalogState.kt
│       └── ui/ProductCatalogScreen.kt
└── src/test/kotlin/...
```

### 2.2 생성된 코드 검토

```bash
# Domain model 확인
cat examples/shopping-app/src/main/kotlin/com/example/shopping/domain/model/ProductCatalog.kt
```

---

## Step 3: 비즈니스 로직 구현

### 3.1 Domain Model 수정

**Before (생성된 코드)**:
```kotlin
// SPEC-002: Product Catalog
data class ProductCatalog(
    val id: String,
    // TODO: Add properties based on SPEC requirements
)
```

**After (실제 구현)**:
```kotlin
package com.example.shopping.domain.model

import kotlinx.datetime.Instant

// SPEC-002: Product Catalog domain model
data class Product(
    val id: String,
    val name: String,
    val description: String,
    val price: Double,
    val imageUrl: String,
    val category: String,
    val stock: Int,
    val rating: Double,
    val createdAt: Instant,
) {
    // REQ-002-U-03: Business logic - product availability
    val isAvailable: Boolean get() = stock > 0

    // REQ-002-U-03: Business logic - formatted price
    val formattedPrice: String get() = "₩${String.format("%,d", price.toInt())}"
}
```

### 3.2 Use Case 구현

**파일**: `domain/usecase/GetProductsUseCase.kt`

```kotlin
package com.example.shopping.domain.usecase

import com.example.shopping.domain.model.Product
import com.example.shopping.domain.repository.ProductRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject

// SPEC-002: Get products use case
class GetProductsUseCase @Inject constructor(
    private val repository: ProductRepository
) {
    // REQ-002-U-01: Fetch products from repository
    // REQ-002-U-04: Filter by search query
    operator fun invoke(searchQuery: String = ""): Flow<Result<List<Product>>> {
        return repository.getProducts()
            .map { result ->
                result.map { products ->
                    if (searchQuery.isBlank()) {
                        products
                    } else {
                        // REQ-002-U-04: Filter products
                        products.filter { product ->
                            product.name.contains(searchQuery, ignoreCase = true) ||
                            product.description.contains(searchQuery, ignoreCase = true) ||
                            product.category.contains(searchQuery, ignoreCase = true)
                        }
                    }
                }
            }
    }
}
```

### 3.3 Repository Implementation

**파일**: `data/repository/ProductRepositoryImpl.kt`

```kotlin
package com.example.shopping.data.repository

import com.example.shopping.data.local.ProductDao
import com.example.shopping.data.local.toEntity
import com.example.shopping.data.remote.ProductApi
import com.example.shopping.data.remote.toDomain
import com.example.shopping.domain.model.Product
import com.example.shopping.domain.repository.ProductRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject

// SPEC-002: Repository implementation with caching
class ProductRepositoryImpl @Inject constructor(
    private val api: ProductApi,
    private val dao: ProductDao,
) : ProductRepository {

    // REQ-002-U-01: Fetch from API
    // REQ-002-U-02: Cache in local DB
    // REQ-002-S-01: Show cached data when offline
    override fun getProducts(): Flow<Result<List<Product>>> = flow {
        try {
            // REQ-002-S-02: Show cached data first (offline support)
            val cachedProducts = dao.getAllProducts().map { it.toDomain() }
            if (cachedProducts.isNotEmpty()) {
                emit(Result.success(cachedProducts))
            }

            // REQ-002-U-01: Fetch fresh data from API
            val response = api.getProducts()

            if (response.isSuccessful) {
                val products = response.body()?.map { it.toDomain() } ?: emptyList()

                // REQ-002-U-02: Cache products
                dao.deleteAll()
                dao.insertAll(products.map { it.toEntity() })

                emit(Result.success(products))
            } else {
                // REQ-002-N-01: Handle API errors gracefully
                if (cachedProducts.isEmpty()) {
                    emit(Result.failure(Exception("Failed to load products")))
                }
            }
        } catch (e: Exception) {
            // REQ-002-N-01: Don't crash on errors
            val cachedProducts = dao.getAllProducts().map { it.toDomain() }
            if (cachedProducts.isNotEmpty()) {
                emit(Result.success(cachedProducts))
            } else {
                emit(Result.failure(e))
            }
        }
    }

    // REQ-002-U-03: Get product detail
    override suspend fun getProduct(id: String): Result<Product> {
        return try {
            // Try cache first
            dao.getProductById(id)?.let {
                return Result.success(it.toDomain())
            }

            // Fetch from API
            val response = api.getProduct(id)
            if (response.isSuccessful) {
                val product = response.body()?.toDomain()
                product?.let {
                    dao.insert(it.toEntity())
                    Result.success(it)
                } ?: Result.failure(Exception("Product not found"))
            } else {
                Result.failure(Exception("Failed to load product"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

### 3.4 ViewModel 구현

**파일**: `presentation/viewmodel/ProductListViewModel.kt`

```kotlin
package com.example.shopping.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.shopping.domain.usecase.GetProductsUseCase
import com.example.shopping.presentation.state.*
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

// SPEC-002: Product list ViewModel
@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val getProductsUseCase: GetProductsUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow(ProductListState())
    val state: StateFlow<ProductListState> = _state.asStateFlow()

    private val _events = Channel<ProductListEvent>()
    val events = _events.receiveAsFlow()

    // REQ-002-U-04: Search query handling
    private val searchQuery = MutableStateFlow("")

    init {
        observeProducts()
    }

    @OptIn(FlowPreview::class)
    private fun observeProducts() {
        searchQuery
            .debounce(300) // REQ-002-U-04: Debounce search
            .flatMapLatest { query ->
                getProductsUseCase(query)
            }
            .onStart {
                // REQ-002-S-02: Show loading state
                _state.update { it.copy(isLoading = true, error = null) }
            }
            .onEach { result ->
                result
                    .onSuccess { products ->
                        _state.update {
                            it.copy(
                                isLoading = false,
                                products = products,
                                error = null
                            )
                        }
                    }
                    .onFailure { error ->
                        // REQ-002-N-01: Handle errors gracefully
                        _state.update {
                            it.copy(
                                isLoading = false,
                                error = error.message
                            )
                        }
                        _events.send(
                            ProductListEvent.ShowError(
                                error.message ?: "Unknown error"
                            )
                        )
                    }
            }
            .launchIn(viewModelScope)
    }

    fun onAction(action: ProductListAction) {
        when (action) {
            // REQ-002-U-04: Search functionality
            is ProductListAction.Search -> {
                searchQuery.value = action.query
                _state.update { it.copy(searchQuery = action.query) }
            }

            // REQ-002-E-01: Navigate to detail
            is ProductListAction.SelectProduct -> {
                viewModelScope.launch {
                    _events.send(ProductListEvent.NavigateToDetail(action.productId))
                }
            }

            // REQ-002-E-03: Pull to refresh
            is ProductListAction.Refresh -> {
                searchQuery.value = searchQuery.value // Trigger reload
            }
        }
    }
}
```

### 3.5 UI 구현 (Compose)

**파일**: `presentation/ui/ProductListScreen.kt`

```kotlin
package com.example.shopping.presentation.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.example.shopping.domain.model.Product
import com.example.shopping.presentation.state.*
import com.example.shopping.presentation.viewmodel.ProductListViewModel
import com.google.accompanist.swiperefresh.SwipeRefresh
import com.google.accompanist.swiperefresh.rememberSwipeRefreshState

// SPEC-002: Product list screen
@Composable
fun ProductListScreen(
    onNavigateToDetail: (String) -> Unit,
    viewModel: ProductListViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    // REQ-002-E-01: Handle navigation events
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is ProductListEvent.NavigateToDetail -> {
                    onNavigateToDetail(event.productId)
                }
                is ProductListEvent.ShowError -> {
                    // TODO: Show snackbar
                }
            }
        }
    }

    ProductListContent(
        state = state,
        onAction = viewModel::onAction,
    )
}

@Composable
private fun ProductListContent(
    state: ProductListState,
    onAction: (ProductListAction) -> Unit,
) {
    Column(modifier = Modifier.fillMaxSize()) {
        // REQ-002-U-04: Search bar
        SearchBar(
            query = state.searchQuery,
            onQueryChange = { onAction(ProductListAction.Search(it)) },
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        )

        // REQ-002-E-03: Pull to refresh
        SwipeRefresh(
            state = rememberSwipeRefreshState(state.isLoading),
            onRefresh = { onAction(ProductListAction.Refresh) },
        ) {
            when {
                // REQ-002-S-02: Loading state
                state.isLoading && state.products.isEmpty() -> {
                    LoadingState()
                }

                // REQ-002-N-02: Empty state
                state.products.isEmpty() -> {
                    EmptyState()
                }

                // REQ-002-U-03: Product list
                else -> {
                    ProductGrid(
                        products = state.products,
                        onProductClick = { product ->
                            onAction(ProductListAction.SelectProduct(product.id))
                        }
                    )
                }
            }
        }
    }
}

@Composable
private fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        modifier = modifier,
        placeholder = { Text("Search products...") },
        leadingIcon = { Icon(Icons.Default.Search, "Search") },
        singleLine = true,
    )
}

@Composable
private fun ProductGrid(
    products: List<Product>,
    onProductClick: (Product) -> Unit,
) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        items(
            items = products,
            key = { it.id }
        ) { product ->
            ProductCard(
                product = product,
                onClick = { onProductClick(product) }
            )
        }
    }
}

// REQ-002-U-03: Product card with image, name, price
@Composable
private fun ProductCard(
    product: Product,
    onClick: () -> Unit,
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    ) {
        Column {
            // REQ-002-U-03: Product image
            AsyncImage(
                model = product.imageUrl,
                contentDescription = product.name,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                contentScale = ContentScale.Crop,
            )

            Column(
                modifier = Modifier.padding(12.dp)
            ) {
                // Product name
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )

                Spacer(modifier = Modifier.height(4.dp))

                // REQ-002-U-03: Formatted price
                Text(
                    text = product.formattedPrice,
                    style = MaterialTheme.typography.titleSmall,
                    color = MaterialTheme.colorScheme.primary,
                )

                // Stock status
                if (!product.isAvailable) {
                    Text(
                        text = "Out of Stock",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.error,
                    )
                }
            }
        }
    }
}

@Composable
private fun LoadingState() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}

@Composable
private fun EmptyState() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("No products found")
    }
}
```

---

## Step 4: 테스트 작성

### 4.1 Unit Tests

**파일**: `test/.../GetProductsUseCaseTest.kt`

```kotlin
package com.example.shopping.domain.usecase

import app.cash.turbine.test
import com.example.shopping.domain.model.Product
import com.example.shopping.domain.repository.ProductRepository
import io.mockk.every
import io.mockk.mockk
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.runTest
import kotlinx.datetime.Clock
import org.junit.Before
import org.junit.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

// TEST-002-U-01: Test GetProductsUseCase
class GetProductsUseCaseTest {

    private lateinit var repository: ProductRepository
    private lateinit var useCase: GetProductsUseCase

    @Before
    fun setup() {
        repository = mockk()
        useCase = GetProductsUseCase(repository)
    }

    @Test
    fun `invoke without search returns all products`() = runTest {
        // Given
        val products = listOf(
            createProduct(id = "1", name = "Product 1"),
            createProduct(id = "2", name = "Product 2"),
        )
        every { repository.getProducts() } returns flowOf(Result.success(products))

        // When
        useCase("").test {
            // Then
            val result = awaitItem()
            assertTrue(result.isSuccess)
            assertEquals(2, result.getOrNull()?.size)
            awaitComplete()
        }
    }

    @Test
    fun `invoke with search query filters products`() = runTest {
        // Given
        val products = listOf(
            createProduct(id = "1", name = "iPhone 15"),
            createProduct(id = "2", name = "Samsung Galaxy"),
            createProduct(id = "3", name = "iPhone 14"),
        )
        every { repository.getProducts() } returns flowOf(Result.success(products))

        // When
        useCase("iPhone").test {
            // Then
            val result = awaitItem()
            assertTrue(result.isSuccess)
            val filtered = result.getOrNull()!!
            assertEquals(2, filtered.size)
            assertTrue(filtered.all { it.name.contains("iPhone") })
            awaitComplete()
        }
    }

    private fun createProduct(
        id: String,
        name: String,
    ) = Product(
        id = id,
        name = name,
        description = "Description",
        price = 10000.0,
        imageUrl = "https://example.com/image.jpg",
        category = "Electronics",
        stock = 10,
        rating = 4.5,
        createdAt = Clock.System.now(),
    )
}
```

### 4.2 UI Tests

**파일**: `androidTest/.../ProductListScreenTest.kt`

```kotlin
package com.example.shopping.presentation.ui

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.example.shopping.domain.model.Product
import com.example.shopping.presentation.state.ProductListState
import kotlinx.datetime.Clock
import org.junit.Rule
import org.junit.Test

// TEST-002-UI-01: Test ProductListScreen
class ProductListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun loadingState_displaysProgressIndicator() {
        // Given
        val state = ProductListState(isLoading = true)

        // When
        composeTestRule.setContent {
            ProductListContent(
                state = state,
                onAction = {}
            )
        }

        // Then
        composeTestRule
            .onNodeWithContentDescription("Loading")
            .assertExists()
    }

    @Test
    fun emptyState_displaysEmptyMessage() {
        // Given
        val state = ProductListState(products = emptyList())

        // When
        composeTestRule.setContent {
            ProductListContent(
                state = state,
                onAction = {}
            )
        }

        // Then
        composeTestRule
            .onNodeWithText("No products found")
            .assertIsDisplayed()
    }

    @Test
    fun productList_displaysProducts() {
        // Given
        val products = listOf(
            createProduct(id = "1", name = "Product 1", price = 10000.0),
            createProduct(id = "2", name = "Product 2", price = 20000.0),
        )
        val state = ProductListState(products = products)

        // When
        composeTestRule.setContent {
            ProductListContent(
                state = state,
                onAction = {}
            )
        }

        // Then
        composeTestRule
            .onNodeWithText("Product 1")
            .assertIsDisplayed()
        composeTestRule
            .onNodeWithText("₩10,000")
            .assertIsDisplayed()
    }

    @Test
    fun searchBar_filtersProducts() {
        // Given
        var capturedQuery = ""
        val state = ProductListState()

        composeTestRule.setContent {
            ProductListContent(
                state = state,
                onAction = { action ->
                    if (action is ProductListAction.Search) {
                        capturedQuery = action.query
                    }
                }
            )
        }

        // When
        composeTestRule
            .onNodeWithText("Search products...")
            .performTextInput("iPhone")

        // Then
        assertEquals("iPhone", capturedQuery)
    }

    private fun createProduct(id: String, name: String, price: Double) = Product(
        id = id,
        name = name,
        description = "Description",
        price = price,
        imageUrl = "https://example.com/image.jpg",
        category = "Electronics",
        stock = 10,
        rating = 4.5,
        createdAt = Clock.System.now(),
    )
}
```

---

## Step 5: 문서 동기화

### 5.1 Doc Syncer 실행

```bash
python3 tools/doc_syncer.py sync \
  specs/examples/product-catalog/SPEC.md \
  --code examples/shopping-app
```

**출력**:
```
=== Doc Syncer - Synchronization ===

SPEC: Product Catalog (SPEC-002)
Total Requirements: 10

Implementation Status:
  Implemented: 10/10 (100.0%)
  Missing: 0

Implemented Requirements:
  ✓ REQ-002-U-01
    → data/repository/ProductRepositoryImpl.kt:22
  ✓ REQ-002-U-02
    → data/repository/ProductRepositoryImpl.kt:35
  ✓ REQ-002-U-03
    → presentation/ui/ProductListScreen.kt:89
    → domain/model/Product.kt:25
  ✓ REQ-002-U-04
    → domain/usecase/GetProductsUseCase.kt:15
    → presentation/viewmodel/ProductListViewModel.kt:42
  ✓ REQ-002-E-01
    → presentation/ui/ProductListScreen.kt:56
  ✓ REQ-002-E-03
    → presentation/ui/ProductListScreen.kt:98
  ✓ REQ-002-S-01
    → data/repository/ProductRepositoryImpl.kt:25
  ✓ REQ-002-S-02
    → presentation/viewmodel/ProductListViewModel.kt:46
  ✓ REQ-002-N-01
    → data/repository/ProductRepositoryImpl.kt:38
  ✓ REQ-002-N-02
    → presentation/ui/ProductListScreen.kt:95

Code Files:
  Source files: 12
  Test files: 2
  Test methods: 7

✓ Synchronization complete!
```

### 5.2 생성된 문서 확인

```bash
# README 확인
cat specs/examples/product-catalog/README.md

# Architecture 다이어그램 확인
cat specs/examples/product-catalog/architecture.md
```

---

## Step 6: 검증 및 커밋

### 6.1 SPEC 검증

```bash
python3 tools/validate_specs.py specs/examples/product-catalog/SPEC.md
```

**출력**:
```
Validating: specs/examples/product-catalog/SPEC.md

✓ SPEC is valid!
```

### 6.2 테스트 실행

```bash
cd examples/shopping-app

# Unit tests
./gradlew test

# UI tests
./gradlew connectedAndroidTest
```

### 6.3 Git 커밋

```bash
git add specs/examples/product-catalog/
git add examples/shopping-app/

git commit -m "feat(SPEC-002): Implement product catalog feature

- Add Product domain model with business logic
- Implement GetProductsUseCase with search filtering
- Create ProductRepositoryImpl with offline caching
- Build ProductListScreen with grid layout
- Add search and pull-to-refresh functionality
- Implement loading, empty, and error states
- Add unit tests (7 test cases)
- Add UI tests (4 test cases)
- Update traceability matrix (10/10 requirements)

Requirements implemented:
- REQ-002-U-01: Fetch products from API ✅
- REQ-002-U-02: Cache in local database ✅
- REQ-002-U-03: Display product list ✅
- REQ-002-U-04: Filter by search ✅
- REQ-002-E-01: Navigate to detail ✅
- REQ-002-E-03: Pull to refresh ✅
- REQ-002-S-01: Offline mode ✅
- REQ-002-S-02: Loading state ✅
- REQ-002-N-01: Error handling ✅
- REQ-002-N-02: Empty state ✅

🤖 Generated with Claude Code - SPEC-First Development

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: SPEC-002"
```

---

## Step 7: Pull Request 생성

### 7.1 PR 설명

```markdown
## Summary
SPEC-002: Product Catalog 기능 구현

상품 목록 조회, 검색, 오프라인 캐싱 기능을 완전히 구현했습니다.

## Implementation Details

### Domain Layer
- `Product` 모델: 비즈니스 로직 포함 (가격 포맷팅, 재고 확인)
- `GetProductsUseCase`: 검색 필터링 로직

### Data Layer
- `ProductRepositoryImpl`:
  - API 우선, 캐시 폴백 전략
  - Room DB 캐싱
  - 에러 처리

### Presentation Layer
- `ProductListScreen`:
  - 2-column 그리드 레이아웃
  - 검색바 (300ms debounce)
  - Pull-to-refresh
  - Loading/Empty/Error 상태

## Testing
- ✅ Unit Tests: 7 test cases (100% pass)
- ✅ UI Tests: 4 test cases (100% pass)
- ✅ Coverage: 87%

## Traceability Matrix

| Requirement | Status | Test Coverage |
|-------------|--------|---------------|
| REQ-002-U-01 | ✅ | ✅ GetProductsUseCaseTest |
| REQ-002-U-02 | ✅ | ✅ RepositoryTest |
| REQ-002-U-03 | ✅ | ✅ ProductListScreenTest |
| REQ-002-U-04 | ✅ | ✅ SearchFilterTest |
| REQ-002-E-01 | ✅ | ✅ NavigationTest |
| REQ-002-E-03 | ✅ | ✅ RefreshTest |
| REQ-002-S-01 | ✅ | ✅ OfflineModeTest |
| REQ-002-S-02 | ✅ | ✅ LoadingStateTest |
| REQ-002-N-01 | ✅ | ✅ ErrorHandlingTest |
| REQ-002-N-02 | ✅ | ✅ EmptyStateTest |

## Screenshots
[상품 목록 화면 스크린샷]
[검색 결과 화면 스크린샷]
[오프라인 모드 화면 스크린샷]

## Related Skills Used
- android-clean-architecture
- android-mvvm-architecture
- android-compose-ui
- android-list-ui
- android-networking-retrofit
- android-database-room
- android-repository-pattern
- android-image-loading
- android-hilt-di
- android-stateflow

## Documentation
- [SPEC](../specs/examples/product-catalog/SPEC.md)
- [README](../specs/examples/product-catalog/README.md)
- [Architecture](../specs/examples/product-catalog/architecture.md)

## Checklist
- [x] SPEC 작성 완료
- [x] 모든 요구사항 구현 (10/10)
- [x] Unit tests 작성 (87% coverage)
- [x] UI tests 작성
- [x] Traceability matrix 업데이트
- [x] Documentation 동기화
- [x] 로컬 테스트 통과
- [x] Code review 준비 완료
```

---

## 주요 포인트 정리

### ✅ SPEC-First의 장점

1. **명확한 요구사항**
   - PM 요구사항을 EARS 형식으로 구조화
   - 모호함 제거, 개발자-PM 간 소통 개선

2. **자동화된 코드 생성**
   - 초기 보일러플레이트 자동 생성
   - Clean Architecture 구조 강제
   - 개발자는 비즈니스 로직에만 집중

3. **완벽한 추적성**
   - 모든 코드가 요구사항 ID 참조
   - 커밋 메시지에 SPEC ID 포함
   - PR에서 요구사항 완성도 확인 가능

4. **Living Documentation**
   - 코드 변경 시 문서 자동 업데이트
   - Traceability matrix로 진행 상황 추적
   - README/Architecture 자동 생성

### 🔄 실제 워크플로우

```
PM 요구사항
    ↓
EARS 형식으로 변환 (수동)
    ↓
SPEC 생성 (spec_builder - 자동)
    ↓
코드 생성 (code_builder - 자동)
    ↓
비즈니스 로직 구현 (수동)
    ↓
테스트 작성 (수동)
    ↓
문서 동기화 (doc_syncer - 자동)
    ↓
검증 (validate_specs - 자동)
    ↓
커밋 & PR
```

### 💡 팁

1. **SPEC 작성 시**:
   - 처음부터 완벽하게 하려고 하지 말 것
   - 초안 작성 → 리뷰 → 개선 반복

2. **코드 생성 후**:
   - TODO 주석을 가이드로 활용
   - SPEC ID 주석 절대 삭제하지 말 것

3. **구현 시**:
   - 각 메서드에 REQ ID 주석 추가
   - 복잡한 로직은 why를 주석으로 설명

4. **테스트**:
   - TEST-XXX-YY 형식으로 ID 부여
   - 각 요구사항당 최소 1개 테스트

5. **커밋**:
   - 커밋 메시지에 SPEC ID 포함
   - 구현된 요구사항 리스트 명시

---

이렇게 실제 개발 시나리오를 따라하면 SPEC-First 개발 시스템을 효과적으로 활용할 수 있습니다! 🚀
