---
name: android-compose-testing
description: Write UI tests for Jetpack Compose using ComposeTestRule and semantics. Use when testing Compose screens, user interactions, and state changes.
---

# Compose UI Testing

Test Jetpack Compose UI with semantics and assertions.

## Dependencies

```kotlin
androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.6.0")
debugImplementation("androidx.compose.ui:ui-test-manifest:1.6.0")
```

## Basic Test

```kotlin
@RunWith(AndroidJUnit4::class)
class HomeScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun testHomeScreen_displaysTitle() {
        composeTestRule.setContent {
            AppTheme {
                HomeScreen()
            }
        }

        composeTestRule
            .onNodeWithText("Welcome")
            .assertIsDisplayed()
    }
}
```

## Finders

```kotlin
// By text
composeTestRule.onNodeWithText("Button")
composeTestRule.onNodeWithText("Button", substring = true)

// By content description
composeTestRule.onNodeWithContentDescription("Profile Icon")

// By tag
composeTestRule.onNodeWithTag("my_button")

// By multiple conditions
composeTestRule.onNode(
    hasText("Button") and isEnabled()
)

// All nodes
composeTestRule.onAllNodesWithText("Item")
```

## Actions

```kotlin
// Click
composeTestRule
    .onNodeWithText("Button")
    .performClick()

// Text input
composeTestRule
    .onNodeWithTag("email_field")
    .performTextInput("test@example.com")

// Scroll
composeTestRule
    .onNodeWithTag("list")
    .performScrollToIndex(10)

// Swipe
composeTestRule
    .onNodeWithTag("card")
    .performTouchInput { swipeLeft() }
```

## Assertions

```kotlin
// Displayed
composeTestRule
    .onNodeWithText("Hello")
    .assertIsDisplayed()

// Enabled/Disabled
composeTestRule
    .onNodeWithText("Button")
    .assertIsEnabled()
    .assertIsNotEnabled()

// Selected
composeTestRule
    .onNodeWithText("Option")
    .assertIsSelected()

// Text
composeTestRule
    .onNodeWithTag("username")
    .assertTextEquals("John")

// Exists
composeTestRule
    .onNodeWithText("Error")
    .assertDoesNotExist()
```

## Testing State

```kotlin
@Test
fun testCounter_incrementsOnClick() {
    composeTestRule.setContent {
        CounterScreen()
    }

    composeTestRule
        .onNodeWithText("Count: 0")
        .assertIsDisplayed()

    composeTestRule
        .onNodeWithText("Increment")
        .performClick()

    composeTestRule
        .onNodeWithText("Count: 1")
        .assertIsDisplayed()
}
```

## Semantic Properties

```kotlin
@Composable
fun MyButton() {
    Button(
        onClick = { },
        modifier = Modifier.testTag("my_button")
    ) {
        Text("Click me")
    }
}

@Composable
fun ProfileImage() {
    Image(
        painter = painterResource(R.drawable.profile),
        contentDescription = "Profile picture"
    )
}
```

## Best Practices
1. Use semantic properties (contentDescription, testTag)
2. Test user interactions, not implementation
3. Wait for async operations with `waitUntil`
4. Use meaningful test tags
5. Test accessibility
