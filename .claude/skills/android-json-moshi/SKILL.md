---
name: android-json-moshi
description: JSON parsing with Moshi library, including custom adapters and Retrofit integration. Use when you need type-safe, efficient JSON serialization with Kotlin support.
---

# Moshi JSON Parsing

Modern JSON parsing library for Android with Kotlin support, null-safety, and efficient code generation.

## When to Use
- Type-safe JSON parsing
- Retrofit API responses
- Custom JSON adapters
- Kotlin data classes with default values
- Alternative to Gson with better Kotlin support

## Dependencies

```kotlin
// libs.versions.toml
[versions]
moshi = "1.15.1"

[libraries]
moshi = { group = "com.squareup.moshi", name = "moshi", version.ref = "moshi" }
moshi-kotlin = { group = "com.squareup.moshi", name = "moshi-kotlin", version.ref = "moshi" }
moshi-codegen = { group = "com.squareup.moshi", name = "moshi-kotlin-codegen", version.ref = "moshi" }
retrofit-moshi = { group = "com.squareup.retrofit2", name = "converter-moshi", version.ref = "retrofit" }

// build.gradle.kts
plugins {
    id("com.google.devtools.ksp") version "2.1.0-1.0.29"
}

dependencies {
    implementation(libs.moshi)
    implementation(libs.moshi.kotlin)
    ksp(libs.moshi.codegen)

    // For Retrofit integration
    implementation(libs.retrofit.moshi)
}
```

## Basic Data Classes

```kotlin
import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

// Simple data class with Moshi code generation
@JsonClass(generateAdapter = true)
data class User(
    val id: String,
    val name: String,
    val email: String,

    // Map JSON field names to Kotlin properties
    @Json(name = "avatar_url")
    val avatarUrl: String?,

    @Json(name = "created_at")
    val createdAt: Long,

    // Optional fields with default values
    val isActive: Boolean = true
)

// Nested objects
@JsonClass(generateAdapter = true)
data class Post(
    val id: String,
    val title: String,
    val content: String,
    val author: User,  // Nested object
    val tags: List<String> = emptyList(),  // Lists
)

// API response wrapper
@JsonClass(generateAdapter = true)
data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: String?
)
```

## Moshi Instance Configuration

```kotlin
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory

// Basic Moshi instance
val moshi = Moshi.Builder()
    .add(KotlinJsonAdapterFactory())  // Kotlin reflection support
    .build()

// With custom adapters
val moshi = Moshi.Builder()
    .add(DateAdapter())  // Custom date adapter
    .add(EnumAdapter())  // Custom enum adapter
    .add(KotlinJsonAdapterFactory())
    .build()

// Parsing JSON
fun parseUser(json: String): User? {
    val adapter = moshi.adapter(User::class.java)
    return adapter.fromJson(json)
}

// Converting to JSON
fun userToJson(user: User): String {
    val adapter = moshi.adapter(User::class.java)
    return adapter.toJson(user)
}
```

## Custom Adapters

### Date Adapter (ISO 8601)

```kotlin
import com.squareup.moshi.FromJson
import com.squareup.moshi.ToJson
import java.time.Instant
import java.time.format.DateTimeFormatter

class InstantAdapter {
    @FromJson
    fun fromJson(value: String): Instant {
        return Instant.parse(value)
    }

    @ToJson
    fun toJson(value: Instant): String {
        return DateTimeFormatter.ISO_INSTANT.format(value)
    }
}

// Usage
@JsonClass(generateAdapter = true)
data class Event(
    val id: String,
    val name: String,
    val timestamp: Instant  // Automatically converted
)
```

### Enum Adapter

```kotlin
enum class UserRole {
    ADMIN,
    USER,
    GUEST
}

class UserRoleAdapter {
    @FromJson
    fun fromJson(value: String): UserRole {
        return try {
            UserRole.valueOf(value.uppercase())
        } catch (e: IllegalArgumentException) {
            UserRole.GUEST  // Default fallback
        }
    }

    @ToJson
    fun toJson(value: UserRole): String {
        return value.name.lowercase()
    }
}
```

### Polymorphic Adapter (Sealed Classes)

```kotlin
sealed class Message {
    @JsonClass(generateAdapter = true)
    data class Text(val content: String) : Message()

    @JsonClass(generateAdapter = true)
    data class Image(val url: String, val caption: String?) : Message()

    @JsonClass(generateAdapter = true)
    data class Video(val url: String, val duration: Int) : Message()
}

class MessageAdapter {
    @FromJson
    fun fromJson(reader: JsonReader): Message {
        val map = reader.readJsonValue() as Map<*, *>
        val type = map["type"] as? String

        return when (type) {
            "text" -> moshi.adapter(Message.Text::class.java)
                .fromJsonValue(map)!!
            "image" -> moshi.adapter(Message.Image::class.java)
                .fromJsonValue(map)!!
            "video" -> moshi.adapter(Message.Video::class.java)
                .fromJsonValue(map)!!
            else -> throw JsonDataException("Unknown message type: $type")
        }
    }

    @ToJson
    fun toJson(writer: JsonWriter, value: Message) {
        when (value) {
            is Message.Text -> {
                writer.beginObject()
                writer.name("type").value("text")
                writer.name("content").value(value.content)
                writer.endObject()
            }
            is Message.Image -> {
                writer.beginObject()
                writer.name("type").value("image")
                writer.name("url").value(value.url)
                writer.name("caption").value(value.caption)
                writer.endObject()
            }
            is Message.Video -> {
                writer.beginObject()
                writer.name("type").value("video")
                writer.name("url").value(value.url)
                writer.name("duration").value(value.duration)
                writer.endObject()
            }
        }
    }
}
```

## Retrofit Integration

```kotlin
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory

// Configure Retrofit with Moshi
val moshi = Moshi.Builder()
    .add(InstantAdapter())
    .add(KotlinJsonAdapterFactory())
    .build()

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(MoshiConverterFactory.create(moshi))
    .build()

// API interface
interface UserApi {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): User

    @POST("users")
    suspend fun createUser(@Body user: User): User

    @GET("users")
    suspend fun getUsers(): ApiResponse<List<User>>
}
```

## Hilt/Koin Module

### Hilt

```kotlin
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideMoshi(): Moshi {
        return Moshi.Builder()
            .add(InstantAdapter())
            .add(UserRoleAdapter())
            .add(KotlinJsonAdapterFactory())
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(moshi: Moshi): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}
```

### Koin

```kotlin
val networkModule = module {
    single {
        Moshi.Builder()
            .add(InstantAdapter())
            .add(UserRoleAdapter())
            .add(KotlinJsonAdapterFactory())
            .build()
    }

    single {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(MoshiConverterFactory.create(get()))
            .build()
    }

    single { get<Retrofit>().create(UserApi::class.java) }
}
```

## Testing with Moshi

```kotlin
import org.junit.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

class UserJsonTest {

    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    private val adapter = moshi.adapter(User::class.java)

    @Test
    fun `parse user from JSON`() {
        // Given
        val json = """
            {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com",
                "avatar_url": "https://example.com/avatar.jpg",
                "created_at": 1699876800000
            }
        """.trimIndent()

        // When
        val user = adapter.fromJson(json)

        // Then
        assertNotNull(user)
        assertEquals("123", user.id)
        assertEquals("John Doe", user.name)
        assertEquals("john@example.com", user.email)
    }

    @Test
    fun `serialize user to JSON`() {
        // Given
        val user = User(
            id = "123",
            name = "John Doe",
            email = "john@example.com",
            avatarUrl = null,
            createdAt = 1699876800000L
        )

        // When
        val json = adapter.toJson(user)

        // Then
        assert(json.contains("\"id\":\"123\""))
        assert(json.contains("\"name\":\"John Doe\""))
    }

    @Test
    fun `handle missing optional fields`() {
        // Given
        val json = """
            {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": 1699876800000
            }
        """.trimIndent()

        // When
        val user = adapter.fromJson(json)

        // Then
        assertNotNull(user)
        assertEquals(null, user.avatarUrl)
        assertEquals(true, user.isActive)  // Default value
    }
}
```

## Related Skills
- android-networking-retrofit: Retrofit API integration
- android-repository-pattern: Data layer architecture
- android-unit-testing: Testing JSON parsing

## Best Practices

1. **Use Code Generation**: Always use `@JsonClass(generateAdapter = true)` for better performance
2. **Null Safety**: Leverage Kotlin's null safety with Moshi
3. **Default Values**: Use default parameter values for optional fields
4. **Custom Adapters**: Create adapters for dates, enums, and complex types
5. **Proguard Rules**: Add Moshi-specific Proguard rules in production
   ```
   -keep class com.squareup.moshi.** { *; }
   -keep @com.squareup.moshi.JsonQualifier interface *
   -keepclassmembers class ** {
       @com.squareup.moshi.FromJson *;
       @com.squareup.moshi.ToJson *;
   }
   ```
6. **Error Handling**: Wrap JSON parsing in try-catch for robustness
7. **Immutability**: Use immutable data classes for thread-safety
8. **KSP over KAPT**: Use KSP for faster compilation (as shown in dependencies)

## Common Patterns

### API Response Wrapper

```kotlin
@JsonClass(generateAdapter = true)
data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val message: String?,
    val code: Int?
)

// Handle in Repository
suspend fun getUsers(): Result<List<User>> {
    return try {
        val response = api.getUsers()
        if (response.success && response.data != null) {
            Result.success(response.data)
        } else {
            Result.failure(Exception(response.message ?: "Unknown error"))
        }
    } catch (e: Exception) {
        Result.failure(e)
    }
}
```

### Paginated Response

```kotlin
@JsonClass(generateAdapter = true)
data class PaginatedResponse<T>(
    val items: List<T>,
    @Json(name = "current_page") val currentPage: Int,
    @Json(name = "total_pages") val totalPages: Int,
    @Json(name = "total_items") val totalItems: Int
)
```

## Moshi vs Gson

| Feature | Moshi | Gson |
|---------|-------|------|
| Kotlin Support | ✅ Excellent | ⚠️ Limited |
| Code Generation | ✅ KSP/KAPT | ❌ Reflection only |
| Null Safety | ✅ Built-in | ⚠️ Manual |
| Performance | ✅ Faster | ⚠️ Slower |
| File Size | ✅ Smaller | ⚠️ Larger |
| Learning Curve | ⚠️ Moderate | ✅ Easy |

**Recommendation**: Use Moshi for new projects with Kotlin. Gson is fine for legacy code or Java projects.
