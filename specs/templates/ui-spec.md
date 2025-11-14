---
spec_id: UI-XXX
screen_name: [Screen Name]
version: 1.0.0
author: [Author Name]
date: [YYYY-MM-DD]
status: draft
traceability:
  parent_spec: SPEC-XXX
  requirements: [REQ-XXX, REQ-YYY]
  figma_url: [Figma Link]
---

# [Screen Name] UI Specification

## 1. Overview

**Screen Name**: [Screen Name]

**Purpose**: [What this screen allows users to accomplish]

**User Journey**: [Where this fits in the overall user flow]

**Entry Points**:
- From [Previous Screen] when user [action]
- From [Navigation Menu]
- Deep link: `app://[route]`

**Exit Points**:
- To [Next Screen] when user [action]
- Back to [Previous Screen]

---

## 2. Requirements (EARS Format)

### 2.1 Ubiquitous Requirements (Always True)

- **REQ-UI-XXX-U-01**: The screen shall display [primary content] to the user
- **REQ-UI-XXX-U-02**: The screen shall provide [key action] functionality
- **REQ-UI-XXX-U-03**: The screen shall show loading state while fetching data

### 2.2 State-Driven Requirements

- **REQ-UI-XXX-S-01**: WHILE data is loading, the screen shall display shimmer effect
- **REQ-UI-XXX-S-02**: WHILE user is offline, the screen shall show cached data
- **REQ-UI-XXX-S-03**: WHILE search is active, the screen shall filter displayed items

### 2.3 Event-Driven Requirements

- **REQ-UI-XXX-E-01**: WHEN user clicks [item], the screen shall navigate to detail view
- **REQ-UI-XXX-E-02**: WHEN user pulls to refresh, the screen shall reload data
- **REQ-UI-XXX-E-03**: WHEN error occurs, the screen shall display error message with retry option

### 2.4 Unwanted Behaviors

- **REQ-UI-XXX-N-01**: The screen shall NOT allow actions while data is loading
- **REQ-UI-XXX-N-02**: The screen shall NOT show stale data after successful refresh

---

## 3. Wireframes & Layout

### 3.1 Screen Layout (Desktop/Tablet)

```
┌─────────────────────────────────────────────┐
│  ← [Screen Title]              [Icon] [•••] │  ← TopAppBar
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ 🔍 Search...                          │ │  ← Search Bar
│  └───────────────────────────────────────┘ │
│                                             │
│  [Filter] [Sort ▼]                         │  ← Filter/Sort Controls
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ ┌─────┐                               │ │
│  │ │ IMG │  Title                        │ │  ← List Item
│  │ └─────┘  Subtitle                     │ │
│  │          Metadata      [Action →]    │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ ┌─────┐                               │ │
│  │ │ IMG │  Title                        │ │  ← List Item
│  │ └─────┘  Subtitle                     │ │
│  │          Metadata      [Action →]    │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  [Load More...]                            │  ← Pagination
│                                             │
├─────────────────────────────────────────────┤
│  [Home] [Search] [Profile]                 │  ← Bottom Navigation
└─────────────────────────────────────────────┘
```

### 3.2 Mobile Layout (Portrait)

```
┌─────────────────────┐
│ ← [Title]      [•••] │  ← TopAppBar
├─────────────────────┤
│                     │
│ ┌─────────────────┐ │
│ │ 🔍 Search...    │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ ┌───┐           │ │
│ │ │IMG│ Title     │ │
│ │ └───┘ Subtitle  │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ ┌───┐           │ │
│ │ │IMG│ Title     │ │
│ │ └───┘ Subtitle  │ │
│ └─────────────────┘ │
│                     │
└─────────────────────┘
```

### 3.3 Component Breakdown

| Component | Type | Purpose |
|-----------|------|---------|
| TopAppBar | Standard | Navigation, screen title, actions |
| SearchBar | Input | Filter content by search query |
| FilterChips | Selection | Filter by category/status |
| SortDropdown | Dropdown | Sort order selection |
| ItemCard | Card | Display individual item |
| LoadingShimmer | Skeleton | Loading state indicator |
| ErrorView | Message | Error state with retry |
| EmptyState | Message | No data available |
| FAB | Button | Primary action (create/add) |

---

## 4. UI Components Specification

### 4.1 TopAppBar

**Variant**: Small (scrolls with content)

**Elements**:
- Navigation Icon: Back arrow (if not root screen)
- Title: [Screen Title]
- Actions:
  - Search Icon (opens search)
  - More Options Menu (3-dot)

**Compose Code**:
```kotlin
@Composable
fun [Screen]TopBar(
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit,
    onMoreClick: () -> Unit,
) {
    TopAppBar(
        title = { Text("[Screen Title]") },
        navigationIcon = {
            IconButton(onClick = onNavigateBack) {
                Icon(Icons.Default.ArrowBack, "Back")
            }
        },
        actions = {
            IconButton(onClick = onSearchClick) {
                Icon(Icons.Default.Search, "Search")
            }
            IconButton(onClick = onMoreClick) {
                Icon(Icons.Default.MoreVert, "More")
            }
        }
    )
}
```

### 4.2 Search Bar

**Type**: Expanded search field

**Behavior**:
- Shows search icon on left
- Clear button appears when text entered
- Filters results as user types (debounced 300ms)
- Shows search suggestions below

**Compose Code**:
```kotlin
@Composable
fun [Screen]SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        modifier = modifier.fillMaxWidth(),
        placeholder = { Text("Search...") },
        leadingIcon = { Icon(Icons.Default.Search, null) },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { onQueryChange("") }) {
                    Icon(Icons.Default.Clear, "Clear")
                }
            }
        },
        singleLine = true,
    )
}
```

### 4.3 Item Card

**Layout**: Horizontal card with image, text, and action

**Content**:
- Thumbnail image (48x48 dp)
- Title (max 2 lines, ellipsis)
- Subtitle (max 1 line, ellipsis)
- Metadata (timestamp, status)
- Action button/icon

**Compose Code**:
```kotlin
@Composable
fun [Entity]Card(
    item: [Entity],
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            AsyncImage(
                model = item.imageUrl,
                contentDescription = null,
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape),
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    text = item.subtitle,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    text = item.formattedDate,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            IconButton(onClick = { /* action */ }) {
                Icon(Icons.Default.ChevronRight, "View details")
            }
        }
    }
}
```

### 4.4 Loading State (Shimmer)

**Type**: Skeleton screen with shimmer animation

**Behavior**: Shows placeholder cards with shimmer effect while loading

**Compose Code**:
```kotlin
@Composable
fun [Screen]LoadingState() {
    Column {
        repeat(5) {
            ShimmerCard()
            Spacer(modifier = Modifier.height(8.dp))
        }
    }
}

@Composable
fun ShimmerCard() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(80.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .shimmerEffect()
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.7f)
                        .height(16.dp)
                        .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(8.dp))
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.5f)
                        .height(14.dp)
                        .shimmerEffect()
                )
            }
        }
    }
}
```

### 4.5 Empty State

**Content**:
- Icon (illustrative)
- Title: "No [items] found"
- Subtitle: "Add your first [item] to get started"
- Action button: "Add [Item]"

**Compose Code**:
```kotlin
@Composable
fun [Screen]EmptyState(
    onActionClick: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(
            imageVector = Icons.Default.[EmptyIcon],
            contentDescription = null,
            modifier = Modifier.size(120.dp),
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "No [items] found",
            style = MaterialTheme.typography.titleLarge,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Add your first [item] to get started",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )
        Spacer(modifier = Modifier.height(24.dp))
        Button(onClick = onActionClick) {
            Text("Add [Item]")
        }
    }
}
```

### 4.6 Error State

**Content**:
- Error icon
- Error message
- Retry button

**Compose Code**:
```kotlin
@Composable
fun [Screen]ErrorState(
    error: String,
    onRetry: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(
            imageVector = Icons.Default.Error,
            contentDescription = null,
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.error,
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "Something went wrong",
            style = MaterialTheme.typography.titleLarge,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = error,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )
        Spacer(modifier = Modifier.height(24.dp))
        Button(onClick = onRetry) {
            Icon(Icons.Default.Refresh, null)
            Spacer(modifier = Modifier.width(8.dp))
            Text("Try Again")
        }
    }
}
```

---

## 5. Screen States

### 5.1 State Definition

```kotlin
data class [Screen]State(
    val items: List<[Entity]> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val searchQuery: String = "",
    val selectedFilter: Filter = Filter.ALL,
    val sortOrder: SortOrder = SortOrder.NEWEST,
    val isRefreshing: Boolean = false,
) {
    val isEmpty: Boolean
        get() = !isLoading && items.isEmpty() && error == null

    val isSearchActive: Boolean
        get() = searchQuery.isNotEmpty()
}
```

### 5.2 State Transitions

```
Initial State (Loading)
    ↓
[Success] → Content State (Items displayed)
    ↓ ← ← ← ← ← ← ← ← ← ← ← ← ← ←
[User Action: Refresh/Search/Filter] → Loading State
    ↓
[Success] → Updated Content
[Error] → Error State (with retry)
    ↓
[User: Retry] → Loading State
```

### 5.3 State Rendering Logic

```kotlin
@Composable
fun [Screen]Content(
    state: [Screen]State,
    onAction: ([Screen]Action) -> Unit,
) {
    when {
        state.isLoading && state.items.isEmpty() -> {
            [Screen]LoadingState()
        }
        state.error != null -> {
            [Screen]ErrorState(
                error = state.error,
                onRetry = { onAction([Screen]Action.Retry) }
            )
        }
        state.isEmpty -> {
            [Screen]EmptyState(
                onActionClick = { onAction([Screen]Action.Add) }
            )
        }
        else -> {
            [Screen]SuccessState(
                items = state.items,
                isRefreshing = state.isRefreshing,
                onRefresh = { onAction([Screen]Action.Refresh) },
                onItemClick = { id ->
                    onAction([Screen]Action.SelectItem(id))
                }
            )
        }
    }
}
```

---

## 6. Interactions & Gestures

### 6.1 Primary Interactions

| Action | Trigger | Response | Requirements |
|--------|---------|----------|--------------|
| View item detail | Tap on card | Navigate to detail screen | REQ-UI-XXX-E-01 |
| Search | Type in search bar | Filter items (debounced) | REQ-UI-XXX-S-03 |
| Refresh | Pull to refresh | Reload data | REQ-UI-XXX-E-02 |
| Add new | Tap FAB | Navigate to create screen | REQ-UI-XXX-U-02 |
| Filter | Tap filter chip | Show filtered items | REQ-UI-XXX-S-03 |
| Sort | Select from dropdown | Reorder items | REQ-UI-XXX-U-01 |

### 6.2 Gestures

- **Pull to Refresh**: Vertical swipe down from top
- **Scroll**: Vertical scroll through list
- **Swipe to Delete** (optional): Horizontal swipe left on item

### 6.3 Navigation

**Entry**:
- From bottom navigation: Home → This Screen
- From previous screen: Detail → Back to This Screen
- Deep link: `myapp://[screen]`

**Exit**:
- To detail: This Screen → Item Detail
- To create: This Screen → Create Screen
- Back navigation: This Screen → Previous Screen

**Compose Navigation**:
```kotlin
// UI-XXX: Navigation route
@Serializable
object [Screen]Route

// UI-XXX: Navigation composable
fun NavGraphBuilder.[screen]Screen(
    onNavigateToDetail: (String) -> Unit,
    onNavigateToCreate: () -> Unit,
    onNavigateBack: () -> Unit,
) {
    composable<[Screen]Route> {
        val viewModel = hiltViewModel<[Screen]ViewModel>()
        val state by viewModel.state.collectAsStateWithLifecycle()

        [Screen]Screen(
            state = state,
            onAction = viewModel::onAction,
            onNavigateToDetail = onNavigateToDetail,
            onNavigateToCreate = onNavigateToCreate,
            onNavigateBack = onNavigateBack,
        )
    }
}
```

---

## 7. Theming & Styling

### 7.1 Colors

| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| Background | surface | surface |
| Card | surfaceVariant | surfaceVariant |
| Primary text | onSurface | onSurface |
| Secondary text | onSurfaceVariant | onSurfaceVariant |
| Error | error | error |

### 7.2 Typography

| Element | Style |
|---------|-------|
| Screen title | titleLarge (22sp) |
| Card title | titleMedium (16sp) |
| Card subtitle | bodyMedium (14sp) |
| Metadata | bodySmall (12sp) |

### 7.3 Spacing

- Card padding: 16dp
- Item spacing: 8dp
- Content padding: 16dp
- Section spacing: 24dp

### 7.4 Elevation

- Cards: 2dp
- FAB: 6dp
- TopAppBar: 0dp (scrolls with content)

---

## 8. Accessibility

### 8.1 Semantic Labels

```kotlin
// UI-XXX: Accessibility - content descriptions
Icon(
    Icons.Default.Search,
    contentDescription = "Search [items]"
)

// UI-XXX: Accessibility - state descriptions
Text(
    text = "[item count] items",
    modifier = Modifier.semantics {
        contentDescription = "$itemCount items found"
    }
)
```

### 8.2 Touch Targets

- Minimum touch target: 48x48 dp
- Spacing between interactive elements: 8dp minimum

### 8.3 Screen Reader Support

- All images have content descriptions
- Interactive elements have semantic labels
- State changes announced to screen readers

---

## 9. Performance

### 9.1 Requirements

- Screen render time: < 200ms
- Scroll performance: 60 FPS
- Image loading: Lazy with placeholders
- List pagination: Load 20 items initially, 20 more on scroll

### 9.2 Optimizations

```kotlin
// UI-XXX: Performance - LazyColumn with keys
LazyColumn {
    items(
        items = state.items,
        key = { it.id } // Recomposition optimization
    ) { item ->
        [Entity]Card(item = item, onClick = { /* ... */ })
    }
}
```

---

## 10. Testing Requirements

### 10.1 UI Tests

```kotlin
// TEST-UI-XXX-01: Verify screen displays items
@Test
fun screenDisplaysItems() {
    composeTestRule.setContent {
        [Screen]Screen(state = successState, ...)
    }

    composeTestRule
        .onNodeWithText("Item 1")
        .assertIsDisplayed()
}

// TEST-UI-XXX-02: Verify click navigation
@Test
fun clickingItemNavigatesToDetail() {
    var navigatedId: String? = null

    composeTestRule.setContent {
        [Screen]Screen(
            state = successState,
            onNavigateToDetail = { navigatedId = it }
        )
    }

    composeTestRule
        .onNodeWithText("Item 1")
        .performClick()

    assertEquals("item-1", navigatedId)
}
```

### 10.2 State Tests

- [ ] TEST-UI-XXX-S-01: Loading state shows shimmer
- [ ] TEST-UI-XXX-S-02: Error state shows error message
- [ ] TEST-UI-XXX-S-03: Empty state shows empty message
- [ ] TEST-UI-XXX-S-04: Success state shows items

---

## 11. Related Skills

- `android-compose-ui`: Declarative UI components
- `android-compose-navigation`: Navigation implementation
- `android-compose-theming`: Material 3 theming
- `android-mvvm-architecture`: ViewModel and State
- `android-list-ui`: LazyColumn patterns
- `android-image-loading`: AsyncImage with Coil

---

## 12. Changelog

### v1.0.0 (2025-11-14)
- Initial UI specification
- Defined all screen states
- Created component specifications
- Added accessibility requirements
