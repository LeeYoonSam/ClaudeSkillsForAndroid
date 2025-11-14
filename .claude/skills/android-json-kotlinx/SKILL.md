---
name: android-json-kotlinx
description: Type-safe JSON serialization with Kotlin Serialization library. Use when you need compile-time safety, multiplatform support, and modern Kotlin features.
---

# Kotlin Serialization

Official Kotlin JSON serialization library with compile-time code generation, type safety, and multiplatform support.

## When to Use
- Type-safe JSON parsing with compile-time validation
- Kotlin Multiplatform projects
- Modern Kotlin features (sealed classes, inline classes)
- Compile-time safety over runtime reflection
- Alternative to Moshi/Gson with better Kotlin integration

## Dependencies

```kotlin
// libs.versions.toml
[versions]
kotlinx-serialization = "1.7.3"
retrofit = "2.11.0"

[libraries]
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinx-serialization" }
retrofit-kotlinx-serialization = { group = "com.jakewharton.retrofit", name = "retrofit2-kotlinx-serialization-converter", version = "1.0.0" }

// build.gradle.kts (app level)
plugins {
    kotlin("plugin.serialization") version "2.1.0"
}

dependencies {
    implementation(libs.kotlinx.serialization.json)

    // For Retrofit integration
    implementation(libs.retrofit.kotlinx.serialization)
}
```

## Basic Serializable Classes

```kotlin
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName
import kotlinx.serialization.Transient

// Simple serializable data class
@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,

    // Map JSON field names to Kotlin properties
    @SerialName("avatar_url")
    val avatarUrl: String? = null,

    @SerialName("created_at")
    val createdAt: Long,

    // Exclude from serialization
    @Transient
    val localCache: String? = null,

    // Default values
    val isActive: Boolean = true
)

// Nested objects
@Serializable
data class Post(
    val id: String,
    val title: String,
    val content: String,
    val author: User,  // Nested serializable object
    val tags: List<String> = emptyList(),
    val metadata: Map<String, String> = emptyMap()
)

// Generic wrapper
@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: String? = null
)
```

## Json Instance Configuration

```kotlin
import kotlinx.serialization.json.Json

// Default configuration
val json = Json

// Custom configuration
val json = Json {
    prettyPrint = true  // Pretty JSON output
    isLenient = true  // Accept non-standard JSON
    ignoreUnknownKeys = true  // Ignore unknown JSON fields
    coerceInputValues = true  // Coerce null to default values
    encodeDefaults = false  // Don't encode default values
    explicitNulls = false  // Omit null fields from output
}

// Parsing JSON
fun parseUser(jsonString: String): User {
    return json.decodeFromString<User>(jsonString)
}

// Converting to JSON
fun userToJson(user: User): String {
    return json.encodeToString(user)
}

// Safe parsing with Result
fun parseUserSafe(jsonString: String): Result<User> {
    return runCatching {
        json.decodeFromString<User>(jsonString)
    }
}
```

## Sealed Classes (Polymorphism)

```kotlin
@Serializable
sealed class Message {
    abstract val id: String
    abstract val timestamp: Long

    @Serializable
    @SerialName("text")
    data class Text(
        override val id: String,
        override val timestamp: Long,
        val content: String
    ) : Message()

    @Serializable
    @SerialName("image")
    data class Image(
        override val id: String,
        override val timestamp: Long,
        val url: String,
        val caption: String? = null
    ) : Message()

    @Serializable
    @SerialName("video")
    data class Video(
        override val id: String,
        override val timestamp: Long,
        val url: String,
        val duration: Int
    ) : Message()
}

// JSON example
/*
{
    "type": "text",
    "id": "msg_123",
    "timestamp": 1699876800000,
    "content": "Hello"
}
*/

// Usage
val json = """
    {
        "type": "text",
        "id": "msg_123",
        "timestamp": 1699876800000,
        "content": "Hello"
    }
""".trimIndent()

val message = Json.decodeFromString<Message>(json)
when (message) {
    is Message.Text -> println(message.content)
    is Message.Image -> println(message.url)
    is Message.Video -> println("Duration: ${message.duration}s")
}
```

## Custom Serializers

### Instant Serializer

```kotlin
import kotlinx.serialization.KSerializer
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.SerialDescriptor
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder
import java.time.Instant

object InstantSerializer : KSerializer<Instant> {
    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("Instant", PrimitiveKind.STRING)

    override fun serialize(encoder: Encoder, value: Instant) {
        encoder.encodeString(value.toString())
    }

    override fun deserialize(decoder: Decoder): Instant {
        return Instant.parse(decoder.decodeString())
    }
}

// Usage
@Serializable
data class Event(
    val id: String,
    val name: String,
    @Serializable(with = InstantSerializer::class)
    val timestamp: Instant
)
```

### UUID Serializer

```kotlin
import java.util.UUID

object UUIDSerializer : KSerializer<UUID> {
    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("UUID", PrimitiveKind.STRING)

    override fun serialize(encoder: Encoder, value: UUID) {
        encoder.encodeString(value.toString())
    }

    override fun deserialize(decoder: Decoder): UUID {
        return UUID.fromString(decoder.decodeString())
    }
}

@Serializable
data class Product(
    @Serializable(with = UUIDSerializer::class)
    val id: UUID,
    val name: String,
    val price: Double
)
```

### Enum Serializer (Custom)

```kotlin
enum class UserRole {
    ADMIN,
    USER,
    GUEST
}

object UserRoleSerializer : KSerializer<UserRole> {
    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("UserRole", PrimitiveKind.STRING)

    override fun serialize(encoder: Encoder, value: UserRole) {
        encoder.encodeString(value.name.lowercase())
    }

    override fun deserialize(decoder: Decoder): UserRole {
        val value = decoder.decodeString()
        return UserRole.entries.find {
            it.name.equals(value, ignoreCase = true)
        } ?: UserRole.GUEST
    }
}
```

## Retrofit Integration

```kotlin
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit

val json = Json {
    ignoreUnknownKeys = true
    coerceInputValues = true
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(
        json.asConverterFactory("application/json".toMediaType())
    )
    .build()

// API interface with serializable responses
interface UserApi {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): User

    @POST("users")
    suspend fun createUser(@Body user: User): User

    @GET("users")
    suspend fun getUsers(): ApiResponse<List<User>>

    @GET("messages")
    suspend fun getMessages(): List<Message>  // Sealed class support
}
```

## Hilt/Koin Module

### Hilt

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideJson(): Json {
        return Json {
            prettyPrint = true
            ignoreUnknownKeys = true
            coerceInputValues = true
        }
    }

    @Provides
    @Singleton
    fun provideRetrofit(json: Json): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(
                json.asConverterFactory("application/json".toMediaType())
            )
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
        Json {
            prettyPrint = true
            ignoreUnknownKeys = true
            coerceInputValues = true
        }
    }

    single {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(
                get<Json>().asConverterFactory("application/json".toMediaType())
            )
            .build()
    }

    single { get<Retrofit>().create(UserApi::class.java) }
}
```

## Testing

```kotlin
import kotlinx.serialization.json.Json
import org.junit.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

class UserSerializationTest {

    private val json = Json {
        ignoreUnknownKeys = true
    }

    @Test
    fun `deserialize user from JSON`() {
        // Given
        val jsonString = """
            {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com",
                "avatar_url": "https://example.com/avatar.jpg",
                "created_at": 1699876800000
            }
        """.trimIndent()

        // When
        val user = json.decodeFromString<User>(jsonString)

        // Then
        assertEquals("123", user.id)
        assertEquals("John Doe", user.name)
        assertEquals("john@example.com", user.email)
        assertEquals("https://example.com/avatar.jpg", user.avatarUrl)
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
        val jsonString = json.encodeToString(User.serializer(), user)

        // Then
        assert(jsonString.contains("\"id\":\"123\""))
        assert(jsonString.contains("\"name\":\"John Doe\""))
    }

    @Test
    fun `ignore unknown JSON fields`() {
        // Given
        val jsonString = """
            {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": 1699876800000,
                "unknown_field": "should be ignored"
            }
        """.trimIndent()

        // When
        val user = json.decodeFromString<User>(jsonString)

        // Then
        assertNotNull(user)
        assertEquals("123", user.id)
    }

    @Test
    fun `deserialize sealed class`() {
        // Given
        val jsonString = """
            {
                "type": "text",
                "id": "msg_123",
                "timestamp": 1699876800000,
                "content": "Hello World"
            }
        """.trimIndent()

        // When
        val message = json.decodeFromString<Message>(jsonString)

        // Then
        assert(message is Message.Text)
        assertEquals("Hello World", (message as Message.Text).content)
    }
}
```

## DataStore Integration

```kotlin
import androidx.datastore.core.DataStore
import androidx.datastore.core.Serializer
import androidx.datastore.dataStore
import kotlinx.serialization.SerializationException
import java.io.InputStream
import java.io.OutputStream

@Serializable
data class UserPreferences(
    val theme: String = "system",
    val language: String = "en",
    val notificationsEnabled: Boolean = true
)

object UserPreferencesSerializer : Serializer<UserPreferences> {
    override val defaultValue: UserPreferences = UserPreferences()

    override suspend fun readFrom(input: InputStream): UserPreferences {
        return try {
            Json.decodeFromString(
                UserPreferences.serializer(),
                input.readBytes().decodeToString()
            )
        } catch (e: SerializationException) {
            defaultValue
        }
    }

    override suspend fun writeTo(t: UserPreferences, output: OutputStream) {
        output.write(
            Json.encodeToString(UserPreferences.serializer(), t)
                .encodeToByteArray()
        )
    }
}

// Context extension
val Context.userPreferencesStore: DataStore<UserPreferences> by dataStore(
    fileName = "user_preferences.json",
    serializer = UserPreferencesSerializer
)
```

## Related Skills
- android-networking-retrofit: Retrofit API integration
- android-repository-pattern: Data layer architecture
- android-datastore: DataStore with serialization
- android-unit-testing: Testing serialization

## Best Practices

1. **Compile-Time Safety**: Use `@Serializable` for compile-time validation
2. **Ignore Unknown Keys**: Set `ignoreUnknownKeys = true` for API flexibility
3. **Default Values**: Use default parameters for optional fields
4. **Sealed Classes**: Leverage for polymorphic JSON handling
5. **Custom Serializers**: Create for complex types (Date, UUID, etc.)
6. **Proguard Rules**: Add rules for production builds
   ```
   -keep class kotlinx.serialization.** { *; }
   -keepattributes *Annotation*, InnerClasses
   -dontnote kotlinx.serialization.SerializationKt
   -keep,includedescriptorclasses class com.yourpackage.**$$serializer { *; }
   -keepclassmembers class com.yourpackage.** {
       *** Companion;
   }
   -keepclasseswithmembers class com.yourpackage.** {
       kotlinx.serialization.KSerializer serializer(...);
   }
   ```
7. **Multiplatform**: Leverage Kotlin Multiplatform Mobile (KMM) support
8. **Error Handling**: Wrap parsing in try-catch or use `runCatching`

## Common Patterns

### Paginated Response

```kotlin
@Serializable
data class PaginatedResponse<T>(
    val items: List<T>,
    @SerialName("current_page") val currentPage: Int,
    @SerialName("total_pages") val totalPages: Int,
    @SerialName("total_items") val totalItems: Int,
    @SerialName("has_next") val hasNext: Boolean
)
```

### Error Response

```kotlin
@Serializable
data class ErrorResponse(
    val code: String,
    val message: String,
    val details: Map<String, String>? = null
)

// Handle in Repository
suspend fun getUser(id: String): Result<User> {
    return try {
        val user = api.getUser(id)
        Result.success(user)
    } catch (e: HttpException) {
        val errorBody = e.response()?.errorBody()?.string()
        val error = errorBody?.let {
            json.decodeFromString<ErrorResponse>(it)
        }
        Result.failure(Exception(error?.message ?: "Unknown error"))
    } catch (e: Exception) {
        Result.failure(e)
    }
}
```

## Kotlinx Serialization vs Others

| Feature | Kotlinx Serialization | Moshi | Gson |
|---------|----------------------|-------|------|
| Compile-Time Safety | ✅ Yes | ⚠️ Partial | ❌ No |
| Multiplatform | ✅ Yes | ❌ No | ❌ No |
| Sealed Classes | ✅ Excellent | ⚠️ Custom | ❌ Limited |
| Default Values | ✅ Native | ✅ Yes | ⚠️ Limited |
| Performance | ✅ Fast | ✅ Fast | ⚠️ Slower |
| Learning Curve | ⚠️ Moderate | ⚠️ Moderate | ✅ Easy |
| Community | ✅ Growing | ✅ Mature | ✅ Large |

**Recommendation**:
- Use **Kotlinx Serialization** for new Kotlin-first projects, especially with KMM
- Use **Moshi** if you need reflection support and aren't using KMM
- Use **Gson** for legacy Java projects or when simplicity is priority

## Advanced: Contextual Serialization

```kotlin
import kotlinx.serialization.modules.SerializersModule
import kotlinx.serialization.modules.contextual

val module = SerializersModule {
    contextual(InstantSerializer)
    contextual(UUIDSerializer)
}

val json = Json {
    serializersModule = module
    ignoreUnknownKeys = true
}

@Serializable
data class Event(
    val id: @Contextual UUID,
    val timestamp: @Contextual Instant,
    val name: String
)
```
