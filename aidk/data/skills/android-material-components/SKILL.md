---
name: android-material-components
description: Implement Material Design 3 components for consistent UI across Android apps. Use when adding buttons, cards, dialogs, and other standard UI elements.
---

# Material Design 3 Components

Use Material 3 components for consistent, accessible UI.

## Buttons

```kotlin
// Filled button (primary action)
Button(onClick = { }) {
    Text("Filled Button")
}

// Outlined button (secondary action)
OutlinedButton(onClick = { }) {
    Text("Outlined")
}

// Text button (low emphasis)
TextButton(onClick = { }) {
    Text("Text Button")
}

// FAB
FloatingActionButton(onClick = { }) {
    Icon(Icons.Default.Add, contentDescription = "Add")
}

// Extended FAB
ExtendedFloatingActionButton(
    onClick = { },
    icon = { Icon(Icons.Default.Add, contentDescription = null) },
    text = { Text("New Item") }
)
```

## Cards

```kotlin
// Filled card
Card(
    modifier = Modifier.fillMaxWidth(),
    onClick = { }
) {
    Text("Card Content", modifier = Modifier.padding(16.dp))
}

// Elevated card
ElevatedCard(
    modifier = Modifier.fillMaxWidth(),
    elevation = CardDefaults.cardElevation(6.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Title", style = MaterialTheme.typography.titleLarge)
        Text("Description")
    }
}

// Outlined card
OutlinedCard {
    Text("Outlined Card")
}
```

## Dialogs

```kotlin
@Composable
fun ConfirmDialog(
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Confirm Action") },
        text = { Text("Are you sure?") },
        confirmButton = {
            TextButton(onClick = onConfirm) {
                Text("Confirm")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
```

## Snackbar

```kotlin
val snackbarHostState = remember { SnackbarHostState() }

Scaffold(
    snackbarHost = { SnackbarHost(snackbarHostState) }
) { paddingValues ->
    Button(
        onClick = {
            scope.launch {
                snackbarHostState.showSnackbar(
                    message = "Item deleted",
                    actionLabel = "Undo",
                    duration = SnackbarDuration.Short
                )
            }
        }
    ) {
        Text("Show Snackbar")
    }
}
```

## Bottom Sheet

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BottomSheetExample() {
    val sheetState = rememberModalBottomSheetState()
    var showSheet by remember { mutableStateOf(false) }

    if (showSheet) {
        ModalBottomSheet(
            onDismissRequest = { showSheet = false },
            sheetState = sheetState
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Bottom Sheet Content")
            }
        }
    }
}
```

## Chips

```kotlin
// Filter chip
FilterChip(
    selected = isSelected,
    onClick = { },
    label = { Text("Filter") }
)

// Suggestion chip
SuggestionChip(
    onClick = { },
    label = { Text("Suggestion") }
)

// Input chip
InputChip(
    selected = false,
    onClick = { },
    label = { Text("Input") },
    trailingIcon = {
        Icon(Icons.Default.Close, contentDescription = "Remove")
    }
)
```

## Best Practices
1. Use semantic component variants (Filled, Outlined, Text)
2. Provide content descriptions for icons
3. Follow Material 3 guidelines
4. Use appropriate elevation levels
5. Maintain consistent spacing
