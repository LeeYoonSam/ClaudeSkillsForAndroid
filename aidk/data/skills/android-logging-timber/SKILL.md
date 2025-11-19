---
name: android-logging-timber
description: Extensible logging library with customizable Tree implementations and automatic tagging. Use for structured logging in Debug/Release builds with different strategies.
---

# Timber Logging

Logging library built on top of Android's Log class with automatic tagging, custom trees, and environment-specific logging.

## When to Use
- Structured logging throughout the app
- Different logging behavior for Debug/Release
- Crash reporting integration (Crashlytics, Sentry)
- File logging for debugging
- Remote logging to analytics

## Dependencies

```kotlin
// libs.versions.toml
[versions]
timber = "5.0.1"

[libraries]
timber = { group = "com.jakewharton.timber", name = "timber", version.ref = "timber" }

// build.gradle.kts
dependencies {
    implementation(libs.timber)
}
```

## Setup in Application

```kotlin
import android.app.Application
import timber.log.Timber

class MyApplication : Application() {

    override fun onCreate() {
        super.onCreate()

        if (BuildConfig.DEBUG) {
            // Debug: Log everything with line numbers
            Timber.plant(Timber.DebugTree())
        } else {
            // Release: Log to Crashlytics only
            Timber.plant(CrashlyticsTree())
        }
    }
}
```

## Basic Logging

```kotlin
import timber.log.Timber

class UserRepository {

    fun getUser(id: String): User {
        Timber.d("Fetching user: $id")

        return try {
            val user = api.getUser(id)
            Timber.i("User fetched successfully: ${user.name}")
            user
        } catch (e: Exception) {
            Timber.e(e, "Failed to fetch user: $id")
            throw e
        }
    }
}

// Log levels
Timber.v("Verbose message")  // Detailed debug info
Timber.d("Debug message")    // Debug info
Timber.i("Info message")     // General information
Timber.w("Warning message")  // Warnings
Timber.e("Error message")    // Errors

// With exception
Timber.e(exception, "Error occurred while processing")

// Formatted strings
Timber.d("User %s logged in at %s", userId, timestamp)
```

## Custom Debug Tree

```kotlin
import timber.log.Timber

class CustomDebugTree : Timber.DebugTree() {

    override fun createStackElementTag(element: StackTraceElement): String {
        // Add line number to tag
        return String.format(
            "%s:%s",
            super.createStackElementTag(element),
            element.lineNumber
        )
    }

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        // Add timestamp
        val timestamp = System.currentTimeMillis()
        super.log(priority, tag, "[$timestamp] $message", t)
    }
}

// Usage
Timber.plant(CustomDebugTree())
```

## Crashlytics Tree (Release)

```kotlin
import android.util.Log
import com.google.firebase.crashlytics.FirebaseCrashlytics
import timber.log.Timber

class CrashlyticsTree : Timber.Tree() {

    private val crashlytics = FirebaseCrashlytics.getInstance()

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        // Only log warnings and errors to Crashlytics
        if (priority >= Log.WARN) {
            crashlytics.log("$priority/$tag: $message")

            t?.let {
                crashlytics.recordException(it)
            }
        }
    }
}

// Plant in release builds
if (!BuildConfig.DEBUG) {
    Timber.plant(CrashlyticsTree())
}
```

## File Logging Tree

```kotlin
import android.content.Context
import timber.log.Timber
import java.io.File
import java.io.FileWriter
import java.text.SimpleDateFormat
import java.util.*

class FileLoggingTree(context: Context) : Timber.Tree() {

    private val logFile = File(context.filesDir, "app_log.txt")
    private val dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.getDefault())

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        try {
            FileWriter(logFile, true).use { writer ->
                val timestamp = dateFormat.format(Date())
                val priorityLabel = when (priority) {
                    Log.VERBOSE -> "V"
                    Log.DEBUG -> "D"
                    Log.INFO -> "I"
                    Log.WARN -> "W"
                    Log.ERROR -> "E"
                    else -> "?"
                }

                writer.append("$timestamp $priorityLabel/$tag: $message\n")

                t?.let {
                    writer.append("${it.stackTraceToString()}\n")
                }
            }
        } catch (e: Exception) {
            Log.e("FileLoggingTree", "Error writing to log file", e)
        }
    }

    fun getLogFile(): File = logFile

    fun clearLogs() {
        logFile.delete()
    }
}

// Usage
val fileTree = FileLoggingTree(context)
Timber.plant(fileTree)

// Get logs for debugging
val logs = fileTree.getLogFile().readText()
```

## Analytics Tree

```kotlin
import timber.log.Timber
import com.google.firebase.analytics.FirebaseAnalytics

class AnalyticsTree(
    private val analytics: FirebaseAnalytics
) : Timber.Tree() {

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        // Log significant events to analytics
        if (priority >= Log.INFO && message.startsWith("EVENT:")) {
            val eventName = message.removePrefix("EVENT:").trim()
            analytics.logEvent(eventName, null)
        }
    }
}

// Usage
Timber.plant(AnalyticsTree(FirebaseAnalytics.getInstance(this)))

// Log analytics events
Timber.i("EVENT: user_login")
Timber.i("EVENT: purchase_completed")
```

## Multi-Tree Setup

```kotlin
class MyApplication : Application() {

    override fun onCreate() {
        super.onCreate()

        when {
            BuildConfig.DEBUG -> {
                // Debug: Console + File logging
                Timber.plant(CustomDebugTree())
                Timber.plant(FileLoggingTree(this))
            }
            else -> {
                // Release: Crashlytics + Analytics
                Timber.plant(CrashlyticsTree())
                Timber.plant(AnalyticsTree(FirebaseAnalytics.getInstance(this)))
            }
        }
    }
}
```

## Tagging

```kotlin
// Automatic tagging (class name)
class UserViewModel : ViewModel() {
    init {
        Timber.d("ViewModel initialized")  // Tag: UserViewModel
    }
}

// Manual tagging
Timber.tag("CustomTag").d("Message with custom tag")

// Tag with multiple loggers
Timber.tag("Network").d("API call started")
Timber.tag("Network").i("API call completed")
```

## Structured Logging

```kotlin
// Log with context
fun logUserAction(userId: String, action: String) {
    Timber.d("User action - userId: %s, action: %s", userId, action)
}

// Log method entry/exit
fun processData(data: Data) {
    Timber.d(">>> processData(data=%s)", data.id)

    try {
        // Processing logic
        val result = process(data)
        Timber.d("<<< processData() -> %s", result)
        return result
    } catch (e: Exception) {
        Timber.e(e, "<<< processData() failed")
        throw e
    }
}

// Log with JSON
fun logUserObject(user: User) {
    val json = Json.encodeToString(user)
    Timber.d("User object: %s", json)
}
```

## Performance Logging

```kotlin
class PerformanceTree : Timber.DebugTree() {

    private val timings = mutableMapOf<String, Long>()

    fun startTiming(key: String) {
        timings[key] = System.currentTimeMillis()
        Timber.d("⏱️ START: $key")
    }

    fun endTiming(key: String) {
        val startTime = timings.remove(key) ?: return
        val duration = System.currentTimeMillis() - startTime
        Timber.d("⏱️ END: $key took ${duration}ms")
    }
}

// Usage
val perfTree = PerformanceTree()
Timber.plant(perfTree)

perfTree.startTiming("api_call")
val result = api.fetchData()
perfTree.endTiming("api_call")  // Logs: "⏱️ END: api_call took 234ms"
```

## Filtering Tree

```kotlin
class FilteredTree(
    private val allowedTags: Set<String>
) : Timber.DebugTree() {

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        if (tag != null && tag in allowedTags) {
            super.log(priority, tag, message, t)
        }
    }
}

// Only log specific tags
Timber.plant(FilteredTree(setOf("Network", "Database", "Auth")))

Timber.tag("Network").d("This will be logged")
Timber.tag("UI").d("This will be ignored")
```

## Redacting Sensitive Data

```kotlin
class RedactingTree : Timber.DebugTree() {

    private val sensitivePatterns = listOf(
        Regex("password=\\S+"),
        Regex("token=\\S+"),
        Regex("api_key=\\S+"),
        Regex("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b")  // Email
    )

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        var redacted = message
        sensitivePatterns.forEach { pattern ->
            redacted = redacted.replace(pattern, "[REDACTED]")
        }
        super.log(priority, tag, redacted, t)
    }
}

// Usage
Timber.plant(RedactingTree())
Timber.d("Login with password=secret123")  // Logs: "Login with [REDACTED]"
```

## Testing with Timber

```kotlin
import timber.log.Timber
import org.junit.After
import org.junit.Before
import org.junit.Test

class UserRepositoryTest {

    private val testTree = TestTree()

    @Before
    fun setup() {
        Timber.plant(testTree)
    }

    @After
    fun tearDown() {
        Timber.uproot(testTree)
    }

    @Test
    fun `repository logs user fetch`() {
        val repository = UserRepository()

        repository.getUser("123")

        val logs = testTree.getLogs()
        assertTrue(logs.any { it.contains("Fetching user: 123") })
    }
}

class TestTree : Timber.DebugTree() {
    private val logs = mutableListOf<String>()

    override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
        logs.add("$priority/$tag: $message")
    }

    fun getLogs(): List<String> = logs.toList()

    fun clear() = logs.clear()
}
```

## Hilt Module

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object LoggingModule {

    @Provides
    @Singleton
    fun provideTimberTree(
        @ApplicationContext context: Context
    ): Timber.Tree {
        return if (BuildConfig.DEBUG) {
            CustomDebugTree()
        } else {
            CrashlyticsTree()
        }
    }
}

class MyApplication : Application() {

    @Inject
    lateinit var timberTree: Timber.Tree

    override fun onCreate() {
        super.onCreate()
        Timber.plant(timberTree)
    }
}
```

## Related Skills
- android-hilt-di: Dependency injection
- android-unit-testing: Testing with logs

## Best Practices

1. **Plant early**: Plant trees in `Application.onCreate()`
2. **Different trees for builds**: Use different logging strategies for debug/release
3. **Structured logging**: Use consistent format for log messages
4. **Tag consistently**: Use class names or functional tags
5. **Don't log sensitive data**: Redact passwords, tokens, PII
6. **Log levels**:
   - `v()`: Detailed debug info (rarely needed)
   - `d()`: Debug info (development only)
   - `i()`: Important info (keep in release)
   - `w()`: Warnings (should investigate)
   - `e()`: Errors (must fix)
7. **Performance**: Avoid expensive string operations in production logs
8. **File logging**: Limit file size, rotate logs
9. **Proguard**: Timber is safe, no special rules needed

## Common Patterns

### Request/Response Logging

```kotlin
class ApiLogger {
    fun logRequest(url: String, method: String, body: String?) {
        Timber.tag("API").d("→ $method $url")
        body?.let { Timber.tag("API").v("Body: $it") }
    }

    fun logResponse(url: String, code: Int, body: String?) {
        Timber.tag("API").d("← $code $url")
        body?.let { Timber.tag("API").v("Body: $it") }
    }
}
```

### User Action Logging

```kotlin
object UserLogger {
    fun logScreenView(screenName: String) {
        Timber.tag("Navigation").i("Screen: $screenName")
    }

    fun logButtonClick(buttonName: String) {
        Timber.tag("UI").d("Click: $buttonName")
    }

    fun logError(screen: String, error: String) {
        Timber.tag("Error").e("Screen: $screen, Error: $error")
    }
}
```

### Database Logging

```kotlin
class LoggingDao(private val delegate: UserDao) : UserDao {

    override suspend fun insert(user: User) {
        Timber.tag("DB").d("INSERT user: ${user.id}")
        delegate.insert(user)
    }

    override suspend fun getUser(id: String): User? {
        Timber.tag("DB").d("SELECT user: $id")
        return delegate.getUser(id)
    }
}
```

## Timber vs Android Log

| Feature | Timber | Android Log |
|---------|--------|-------------|
| Auto-tagging | ✅ Yes | ❌ Manual |
| Custom logging | ✅ Tree system | ❌ Fixed |
| Environment-specific | ✅ Easy | ⚠️ Manual |
| String formatting | ✅ Built-in | ❌ Manual |
| Crash reporting | ✅ Custom tree | ❌ Manual |
| Testing | ✅ Easy | ⚠️ Difficult |

**Recommendation**: Always use Timber over `android.util.Log`. It's more flexible, powerful, and prevents common mistakes (like logging in production).
