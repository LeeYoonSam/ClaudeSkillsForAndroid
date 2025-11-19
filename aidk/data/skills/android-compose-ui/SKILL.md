---
name: android-compose-ui
description: Build declarative UI with Jetpack Compose including composables, state management, recomposition, and Material3 components. Use when creating modern Android UI screens and components.
---

# Jetpack Compose UI Development

Build modern Android UI using declarative Jetpack Compose framework.

## When to Use
- Creating new UI screens
- Building custom UI components
- Implementing Material Design 3
- Developing modern Android apps

## Basic Composable Structure

### Simple Composable

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello, $name!",
        modifier = modifier,
        style = MaterialTheme.typography.headlineMedium
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    AppTheme {
        Greeting("Android")
    }
}
```

### Composable with State

```kotlin
@Composable
fun Counter(modifier: Modifier = Modifier) {
    var count by remember { mutableIntStateOf(0) }

    Column(
        modifier = modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Count: $count",
            style = MaterialTheme.typography.displayMedium
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}
```

## State Management in Compose

### remember vs rememberSaveable

```kotlin
@Composable
fun FormScreen() {
    // Lost on recomposition (orientation change, process death)
    var username by remember { mutableStateOf("") }

    // Survives configuration changes
    var email by rememberSaveable { mutableStateOf("") }

    Column {
        TextField(
            value = username,
            onValueChange = { username = it },
            label = { Text("Username") }
        )

        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") }
        )
    }
}
```

### State Hoisting

```kotlin
// Stateless composable (preferred)
@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    TextField(
        value = query,
        onValueChange = onQueryChange,
        modifier = modifier.fillMaxWidth(),
        placeholder = { Text("Search...") },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) }
    )
}

// Stateful wrapper (holds state)
@Composable
fun StatefulSearchBar(modifier: Modifier = Modifier) {
    var query by remember { mutableStateOf("") }

    SearchBar(
        query = query,
        onQueryChange = { query = it },
        modifier = modifier
    )
}
```

### Collect State from ViewModel

```kotlin
@Composable
fun ProductScreen(
    viewModel: ProductViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    ProductContent(
        state = state,
        onAction = viewModel::onAction
    )
}
```

## Common Layouts

### Column (Vertical Layout)

```kotlin
@Composable
fun VerticalList() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text("Item 1")
        Text("Item 2")
        Text("Item 3")
    }
}
```

### Row (Horizontal Layout)

```kotlin
@Composable
fun HorizontalButtons() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterHorizontally),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Button(onClick = { }) { Text("Cancel") }
        Button(onClick = { }) { Text("OK") }
    }
}
```

### Box (Stack Layout)

```kotlin
@Composable
fun OverlayExample() {
    Box(modifier = Modifier.fillMaxSize()) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Crop
        )
        Text(
            text = "Overlay Text",
            modifier = Modifier.align(Alignment.Center),
            color = Color.White,
            style = MaterialTheme.typography.headlineLarge
        )
    }
}
```

### LazyColumn (Scrollable List)

```kotlin
@Composable
fun ProductList(
    products: List<Product>,
    onProductClick: (Product) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(
            items = products,
            key = { it.id }
        ) { product ->
            ProductItem(
                product = product,
                onClick = { onProductClick(product) }
            )
        }
    }
}

@Composable
fun ProductItem(
    product: Product,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onClick() },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = product.imageUrl,
                contentDescription = product.name,
                modifier = Modifier.size(64.dp),
                contentScale = ContentScale.Crop
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = "$${product.price}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}
```

### LazyRow (Horizontal Scrollable List)

```kotlin
@Composable
fun CategoryChips(
    categories: List<String>,
    selectedCategory: String,
    onCategorySelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyRow(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(horizontal = 16.dp)
    ) {
        items(categories) { category ->
            FilterChip(
                selected = category == selectedCategory,
                onClick = { onCategorySelected(category) },
                label = { Text(category) }
            )
        }
    }
}
```

### LazyVerticalGrid (Grid Layout)

```kotlin
@Composable
fun ProductGrid(
    products: List<Product>,
    onProductClick: (Product) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(products, key = { it.id }) { product ->
            ProductCard(
                product = product,
                onClick = { onProductClick(product) }
            )
        }
    }
}
```

## Material 3 Components

### Buttons

```kotlin
@Composable
fun ButtonExamples() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Filled button (primary)
        Button(onClick = { }) {
            Text("Filled Button")
        }

        // Outlined button
        OutlinedButton(onClick = { }) {
            Text("Outlined Button")
        }

        // Text button
        TextButton(onClick = { }) {
            Text("Text Button")
        }

        // Icon button
        IconButton(onClick = { }) {
            Icon(Icons.Default.Favorite, contentDescription = "Favorite")
        }

        // FAB
        FloatingActionButton(onClick = { }) {
            Icon(Icons.Default.Add, contentDescription = "Add")
        }
    }
}
```

### Text Fields

```kotlin
@Composable
fun TextFieldExamples() {
    var text by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Standard text field
        TextField(
            value = text,
            onValueChange = { text = it },
            label = { Text("Label") },
            placeholder = { Text("Placeholder") },
            leadingIcon = { Icon(Icons.Default.Person, null) },
            supportingText = { Text("Helper text") }
        )

        // Outlined text field
        OutlinedTextField(
            value = text,
            onValueChange = { text = it },
            label = { Text("Email") },
            singleLine = true,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
        )

        // Password field
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            visualTransformation = if (passwordVisible)
                VisualTransformation.None else PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            trailingIcon = {
                IconButton(onClick = { passwordVisible = !passwordVisible }) {
                    Icon(
                        if (passwordVisible) Icons.Default.Visibility
                        else Icons.Default.VisibilityOff,
                        contentDescription = if (passwordVisible) "Hide" else "Show"
                    )
                }
            }
        )
    }
}
```

### Cards

```kotlin
@Composable
fun CardExamples() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Filled card
        Card(
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = "Filled Card",
                modifier = Modifier.padding(16.dp)
            )
        }

        // Outlined card
        OutlinedCard(
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = "Outlined Card",
                modifier = Modifier.padding(16.dp)
            )
        }

        // Elevated card
        ElevatedCard(
            modifier = Modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(defaultElevation = 6.dp)
        ) {
            Text(
                text = "Elevated Card",
                modifier = Modifier.padding(16.dp)
            )
        }

        // Clickable card
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .clickable { /* handle click */ }
        ) {
            Text(
                text = "Clickable Card",
                modifier = Modifier.padding(16.dp)
            )
        }
    }
}
```

### Dialogs

```kotlin
@Composable
fun AlertDialogExample() {
    var showDialog by remember { mutableStateOf(false) }

    Button(onClick = { showDialog = true }) {
        Text("Show Dialog")
    }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("Delete Item") },
            text = { Text("Are you sure you want to delete this item?") },
            confirmButton = {
                TextButton(onClick = {
                    // Handle confirm
                    showDialog = false
                }) {
                    Text("Delete")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}
```

### Scaffold with TopAppBar

```kotlin
@Composable
fun ScreenWithScaffold() {
    var showMenu by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Screen Title") },
                navigationIcon = {
                    IconButton(onClick = { /* handle back */ }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { showMenu = true }) {
                        Icon(Icons.Default.MoreVert, "Menu")
                    }
                    DropdownMenu(
                        expanded = showMenu,
                        onDismissRequest = { showMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Settings") },
                            onClick = { /* handle */ }
                        )
                        DropdownMenuItem(
                            text = { Text("About") },
                            onClick = { /* handle */ }
                        )
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { /* handle FAB */ }) {
                Icon(Icons.Default.Add, "Add")
            }
        }
    ) { paddingValues ->
        // Screen content
        Box(modifier = Modifier.padding(paddingValues)) {
            Text("Content goes here")
        }
    }
}
```

## Modifiers

### Common Modifiers

```kotlin
@Composable
fun ModifierExamples() {
    Box(
        modifier = Modifier
            .fillMaxSize()                    // Fill parent size
            .padding(16.dp)                   // Add padding
            .background(Color.Blue)            // Background color
            .border(2.dp, Color.Red)          // Border
            .clip(RoundedCornerShape(8.dp))   // Clip to shape
            .clickable { }                     // Make clickable
            .alpha(0.8f)                       // Transparency
    )
}
```

### Size Modifiers

```kotlin
Modifier.size(100.dp)                  // Fixed size
Modifier.width(200.dp)                 // Fixed width
Modifier.height(100.dp)                // Fixed height
Modifier.fillMaxWidth()                // Fill parent width
Modifier.fillMaxHeight()               // Fill parent height
Modifier.fillMaxSize()                 // Fill parent size
Modifier.wrapContentSize()             // Wrap content
Modifier.requiredSize(100.dp)          // Fixed size (ignores parent constraints)
```

## Side Effects

### LaunchedEffect

```kotlin
@Composable
fun TimerScreen() {
    var seconds by remember { mutableIntStateOf(0) }

    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            seconds++
        }
    }

    Text("Seconds: $seconds")
}
```

### DisposableEffect

```kotlin
@Composable
fun LifecycleAwareComposable() {
    val lifecycleOwner = LocalLifecycleOwner.current

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_RESUME -> { /* handle resume */ }
                Lifecycle.Event.ON_PAUSE -> { /* handle pause */ }
                else -> {}
            }
        }

        lifecycleOwner.lifecycle.addObserver(observer)

        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }
}
```

## Performance Optimization

### Remember Expensive Calculations

```kotlin
@Composable
fun ExpensiveScreen(data: List<Int>) {
    val processedData = remember(data) {
        data.filter { it > 0 }.sortedDescending()
    }

    LazyColumn {
        items(processedData) { item ->
            Text("$item")
        }
    }
}
```

### derivedStateOf

```kotlin
@Composable
fun ScrollableList() {
    val listState = rememberLazyListState()

    // Only recomposes when showButton changes
    val showButton by remember {
        derivedStateOf {
            listState.firstVisibleItemIndex > 0
        }
    }

    Box {
        LazyColumn(state = listState) {
            items(100) {
                Text("Item $it")
            }
        }

        if (showButton) {
            FloatingActionButton(
                onClick = { /* scroll to top */ },
                modifier = Modifier.align(Alignment.BottomEnd)
            ) {
                Icon(Icons.Default.ArrowUpward, "Scroll to top")
            }
        }
    }
}
```

## Related Skills
- **android-compose-navigation**: For navigation between screens
- **android-compose-theming**: For Material3 theming
- **android-mvvm-architecture**: For state management patterns
- **android-compose-testing**: For UI testing
- **android-list-ui**: For advanced list patterns
- **android-material-components**: For more Material components

## Best Practices

1. **State Hoisting**: Lift state up to make composables reusable
2. **Immutable Parameters**: Use immutable data classes for parameters
3. **Stable Types**: Mark complex types with `@Stable` or `@Immutable`
4. **Key in Lists**: Always provide `key` parameter in `items()`
5. **Avoid Side Effects**: Keep composables pure, use side-effect APIs when needed
6. **Preview**: Add `@Preview` to all composables
7. **Modifier Parameter**: Accept `Modifier` parameter with default value
8. **Remember Expensive Operations**: Use `remember` for heavy calculations
9. **collectAsStateWithLifecycle**: Use for collecting StateFlow
10. **Content Lambda**: Use content lambdas for flexible composables
