---
name: android-animation-lottie
description: Render Adobe After Effects animations natively on Android with Lottie. Use for high-quality animations, loading indicators, and onboarding experiences with Jetpack Compose support.
---

# Lottie Animations

Library for rendering Adobe After Effects animations exported as JSON with bodymovin, enabling complex animations without custom code.

## When to Use
- Complex animations (loading, success, error states)
- Onboarding screens with animations
- Empty states and illustrations
- Animated icons and buttons
- Micro-interactions
- Splash screens

## Dependencies

```kotlin
// libs.versions.toml
[versions]
lottie = "6.5.2"

[libraries]
lottie-compose = { group = "com.airbnb.android", name = "lottie-compose", version.ref = "lottie" }

// build.gradle.kts
dependencies {
    implementation(libs.lottie.compose)
}
```

## Finding Animations

Free Lottie animations:
- [LottieFiles](https://lottiefiles.com/) - Largest library
- [Iconscout](https://iconscout.com/lottie) - Premium and free
- [Motion Elements](https://www.motionelements.com/free/lottie-animations)

## Basic Usage (Compose)

```kotlin
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.airbnb.lottie.compose.*

@Composable
fun LoadingAnimation() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.loading)
    )

    LottieAnimation(
        composition = composition,
        iterations = LottieConstants.IterateForever,
        modifier = Modifier.size(200.dp)
    )
}

// From assets
@Composable
fun AnimationFromAssets() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.Asset("animations/success.json")
    )

    LottieAnimation(composition = composition)
}

// From URL
@Composable
fun AnimationFromUrl() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.Url("https://assets.lottiefiles.com/packages/lf20_xyz.json")
    )

    LottieAnimation(composition = composition)
}
```

## Controlling Playback

```kotlin
@Composable
fun ControlledAnimation() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.animation)
    )

    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = 1,
        isPlaying = true,
        speed = 1f,
        restartOnPlay = false
    )

    LottieAnimation(
        composition = composition,
        progress = { progress }
    )
}

@Composable
fun ManualControl() {
    var isPlaying by remember { mutableStateOf(false) }
    var speed by remember { mutableFloatStateOf(1f) }

    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.animation)
    )

    val progress by animateLottieCompositionAsState(
        composition = composition,
        isPlaying = isPlaying,
        speed = speed,
        restartOnPlay = true
    )

    Column {
        LottieAnimation(
            composition = composition,
            progress = { progress },
            modifier = Modifier.size(200.dp)
        )

        Button(onClick = { isPlaying = !isPlaying }) {
            Text(if (isPlaying) "Pause" else "Play")
        }

        Slider(
            value = speed,
            onValueChange = { speed = it },
            valueRange = 0.5f..2f
        )
    }
}
```

## Loading States

```kotlin
@Composable
fun LoadingState() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.loading)
    )

    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = LottieConstants.IterateForever
    )

    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        LottieAnimation(
            composition = composition,
            progress = { progress },
            modifier = Modifier.size(150.dp)
        )
    }
}

// With loading state
@Composable
fun DataScreen(viewModel: DataViewModel) {
    val state by viewModel.state.collectAsState()

    when {
        state.isLoading -> LoadingAnimation()
        state.error != null -> ErrorAnimation()
        else -> DataContent(state.data)
    }
}
```

## Success/Error Animations

```kotlin
@Composable
fun SuccessAnimation(
    onComplete: () -> Unit = {}
) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.success)
    )

    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = 1
    )

    LaunchedEffect(progress) {
        if (progress == 1f) {
            delay(500)  // Show complete animation briefly
            onComplete()
        }
    }

    LottieAnimation(
        composition = composition,
        progress = { progress },
        modifier = Modifier.size(200.dp)
    )
}

// Result feedback
@Composable
fun ResultFeedback(result: Result<Data>) {
    when {
        result.isSuccess -> SuccessAnimation()
        result.isFailure -> ErrorAnimation()
    }
}
```

## Empty States

```kotlin
@Composable
fun EmptyState(
    title: String,
    description: String,
    actionText: String,
    onActionClick: () -> Unit
) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.empty_box)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        LottieAnimation(
            composition = composition,
            iterations = LottieConstants.IterateForever,
            modifier = Modifier.size(250.dp)
        )

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = title,
            style = MaterialTheme.typography.titleLarge
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = description,
            style = MaterialTheme.typography.bodyMedium,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Spacer(modifier = Modifier.height(24.dp))

        Button(onClick = onActionClick) {
            Text(actionText)
        }
    }
}
```

## Onboarding Screens

```kotlin
data class OnboardingPage(
    val animation: Int,
    val title: String,
    val description: String
)

@Composable
fun OnboardingScreen() {
    val pages = listOf(
        OnboardingPage(
            R.raw.onboarding_1,
            "Welcome",
            "Get started with our app"
        ),
        OnboardingPage(
            R.raw.onboarding_2,
            "Features",
            "Discover amazing features"
        ),
        OnboardingPage(
            R.raw.onboarding_3,
            "Ready",
            "You're all set!"
        )
    )

    val pagerState = rememberPagerState(pageCount = { pages.size })

    Column(modifier = Modifier.fillMaxSize()) {
        HorizontalPager(
            state = pagerState,
            modifier = Modifier.weight(1f)
        ) { page ->
            OnboardingPage(pages[page])
        }

        HorizontalPagerIndicator(
            pagerState = pagerState,
            modifier = Modifier
                .align(Alignment.CenterHorizontally)
                .padding(16.dp)
        )

        Button(
            onClick = { /* Next or finish */ },
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(if (pagerState.currentPage == pages.size - 1) "Get Started" else "Next")
        }
    }
}

@Composable
fun OnboardingPage(page: OnboardingPage) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(page.animation)
    )

    Column(
        modifier = Modifier.fillMaxSize().padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        LottieAnimation(
            composition = composition,
            iterations = LottieConstants.IterateForever,
            modifier = Modifier.size(300.dp)
        )

        Spacer(modifier = Modifier.height(32.dp))

        Text(
            text = page.title,
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = page.description,
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
}
```

## Animated Buttons

```kotlin
@Composable
fun LikeButton(
    isLiked: Boolean,
    onToggle: () -> Unit
) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.like_animation)
    )

    var animationPlayed by remember { mutableStateOf(false) }

    val progress by animateLottieCompositionAsState(
        composition = composition,
        isPlaying = isLiked && !animationPlayed,
        iterations = 1,
        speed = 1.5f
    )

    LaunchedEffect(progress) {
        if (progress == 1f) {
            animationPlayed = true
        }
    }

    LaunchedEffect(isLiked) {
        if (!isLiked) {
            animationPlayed = false
        }
    }

    IconButton(onClick = onToggle) {
        LottieAnimation(
            composition = composition,
            progress = { if (isLiked) 1f else 0f },
            modifier = Modifier.size(48.dp)
        )
    }
}
```

## Dynamic Properties

```kotlin
@Composable
fun DynamicColorAnimation() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.animation)
    )

    val dynamicProperties = rememberLottieDynamicProperties(
        rememberLottieDynamicProperty(
            property = LottieProperty.COLOR,
            value = Color.Red.toArgb(),
            keyPath = arrayOf("Layer", "Shape", "Fill 1")
        )
    )

    LottieAnimation(
        composition = composition,
        dynamicProperties = dynamicProperties
    )
}
```

## Caching

```kotlin
// Preload animations
@Composable
fun PreloadAnimations() {
    // This will cache the composition
    val loading by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.loading)
    )
    val success by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.success)
    )
}

// Configure cache
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        // Set cache size (in bytes)
        L.setMaxCacheSize(50 * 1024 * 1024)  // 50MB
    }
}
```

## Splash Screen

```kotlin
@Composable
fun SplashScreen(onTimeout: () -> Unit) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.splash)
    )

    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = 1
    )

    LaunchedEffect(progress) {
        if (progress == 1f) {
            delay(500)
            onTimeout()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.primary),
        contentAlignment = Alignment.Center
    ) {
        LottieAnimation(
            composition = composition,
            progress = { progress },
            modifier = Modifier.size(300.dp)
        )
    }
}
```

## Performance Tips

```kotlin
// 1. Use appropriate size
LottieAnimation(
    composition = composition,
    modifier = Modifier.size(150.dp)  // Don't make it too large
)

// 2. Limit iterations
LottieAnimation(
    composition = composition,
    iterations = 3  // Instead of IterateForever if possible
)

// 3. Control when to play
var shouldPlay by remember { mutableStateOf(false) }

LaunchedEffect(Unit) {
    // Only play when screen is visible
    shouldPlay = true
}

animateLottieCompositionAsState(
    composition = composition,
    isPlaying = shouldPlay
)

// 4. Reduce complexity
// Use simpler animations (fewer layers, shapes)

// 5. Use hardware acceleration
// Already enabled by default in Compose
```

## Related Skills
- android-compose-ui: Jetpack Compose basics
- android-material-components: Material Design components
- android-compose-theming: Theming and colors

## Best Practices

1. **Animation size**: Keep files under 100KB when possible
2. **Performance**: Use simple animations for repeated elements
3. **Preload**: Cache frequently used animations
4. **Network**: Download animations from URLs with caching strategy
5. **Accessibility**: Provide content descriptions and respect reduced motion
6. **Dark mode**: Choose animations that work in both themes
7. **File organization**: Store in `res/raw/` or `assets/animations/`
8. **Testing**: Test on low-end devices
9. **Fallback**: Have static images as fallback

## Common Patterns

### Pull to Refresh

```kotlin
@Composable
fun PullToRefreshAnimation(isRefreshing: Boolean) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.pull_to_refresh)
    )

    val progress by animateLottieCompositionAsState(
        composition = composition,
        isPlaying = isRefreshing,
        iterations = LottieConstants.IterateForever
    )

    if (isRefreshing) {
        LottieAnimation(
            composition = composition,
            progress = { progress },
            modifier = Modifier.size(50.dp)
        )
    }
}
```

### Network Status

```kotlin
@Composable
fun NetworkStatusAnimation(isConnected: Boolean) {
    val animRes = if (isConnected) {
        R.raw.connected
    } else {
        R.raw.disconnected
    }

    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(animRes)
    )

    LottieAnimation(
        composition = composition,
        iterations = 1,
        modifier = Modifier.size(100.dp)
    )
}
```

## Lottie vs Other Animation Solutions

| Solution | Use Case | Complexity | Performance |
|----------|----------|------------|-------------|
| **Lottie** | Complex, designer-made animations | 🎨 Designer-friendly | ⚡ Good |
| **Compose Animation** | Simple, code-based animations | 💻 Developer-friendly | ⚡⚡ Excellent |
| **GIF** | Legacy, simple animations | 📦 Large files | ⚠️ Poor |
| **AnimatedVector** | Icon animations | 🔧 XML-based | ⚡ Good |

**Recommendation**:
- Use **Lottie** for complex, beautiful animations from designers
- Use **Compose animations** for simple UI state changes
- Avoid **GIF** in modern apps
- Use **AnimatedVector** for simple icon morphing

## Resources

- [LottieFiles](https://lottiefiles.com/) - Free animations
- [Lottie Docs](https://airbnb.io/lottie/) - Official documentation
- [Lottie Editor](https://lottiefiles.com/editor) - Edit animations online
