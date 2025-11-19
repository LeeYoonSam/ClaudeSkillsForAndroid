---
name: android-networking-retrofit
description: Configure Retrofit for REST API calls with OkHttp, Gson/Moshi, Coroutines, and error handling. Use when implementing network data sources and API integration.
---

# Retrofit Networking

Configure Retrofit for type-safe REST API calls with Kotlin Coroutines.

## When to Use
- REST API integration
- Network data source
- HTTP requests with type safety
- API authentication

## Dependencies

```kotlin
// libs.versions.toml
[versions]
retrofit = "2.11.0"
okhttp = "4.12.0"
gson = "2.10.1"

[libraries]
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-gson = { group = "com.squareup.retrofit2", name = "converter-gson", version.ref = "retrofit" }
okhttp = { group = "com.squareup.okhttp3", name = "okhttp", version.ref = "okhttp" }
okhttp-logging = { group = "com.squareup.okhttp3", name = "logging-interceptor", version.ref = "okhttp" }
gson = { group = "com.google.code.gson", name = "gson", version.ref = "gson" }

// build.gradle.kts
dependencies {
    implementation(libs.retrofit)
    implementation(libs.retrofit.gson)
    implementation(libs.okhttp)
    implementation(libs.okhttp.logging)
    implementation(libs.gson)
}
```

## API Service Interface

```kotlin
interface UserApi {

    @GET("users")
    suspend fun getUsers(): List<UserDto>

    @GET("users/{id}")
    suspend fun getUserById(@Path("id") id: String): UserDto

    @POST("users")
    suspend fun createUser(@Body user: UserDto): UserDto

    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") id: String,
        @Body user: UserDto
    ): UserDto

    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: String)

    @GET("users/search")
    suspend fun searchUsers(@Query("q") query: String): List<UserDto>

    @GET("users")
    suspend fun getUsersPaginated(
        @Query("page") page: Int,
        @Query("per_page") perPage: Int = 20
    ): List<UserDto>

    @Multipart
    @POST("users/{id}/avatar")
    suspend fun uploadAvatar(
        @Path("id") id: String,
        @Part avatar: MultipartBody.Part
    ): UserDto

    @FormUrlEncoded
    @POST("auth/login")
    suspend fun login(
        @Field("email") email: String,
        @Field("password") password: String
    ): AuthResponse
}
```

## Data Transfer Objects (DTOs)

```kotlin
data class UserDto(
    val id: String,
    val name: String,
    val email: String,
    val avatar_url: String?,
    val created_at: Long
)

data class AuthResponse(
    val token: String,
    val user: UserDto
)

data class ApiError(
    val message: String,
    val code: Int
)
```

## Retrofit Setup with Hilt

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideGson(): Gson {
        return GsonBuilder()
            .setDateFormat("yyyy-MM-dd'T'HH:mm:ss")
            .create()
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(
                HttpLoggingInterceptor().apply {
                    level = if (BuildConfig.DEBUG) {
                        HttpLoggingInterceptor.Level.BODY
                    } else {
                        HttpLoggingInterceptor.Level.NONE
                    }
                }
            )
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(
        okHttpClient: OkHttpClient,
        gson: Gson
    ): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }

    @Provides
    @Singleton
    fun provideProductApi(retrofit: Retrofit): ProductApi {
        return retrofit.create(ProductApi::class.java)
    }
}
```

## Authentication Interceptor

```kotlin
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()

        val token = tokenManager.getToken()
        if (token.isNullOrEmpty()) {
            return chain.proceed(original)
        }

        val request = original.newBuilder()
            .header("Authorization", "Bearer $token")
            .build()

        return chain.proceed(request)
    }
}

// Add to OkHttpClient
@Provides
@Singleton
fun provideOkHttpClient(
    authInterceptor: AuthInterceptor
): OkHttpClient {
    return OkHttpClient.Builder()
        .addInterceptor(authInterceptor)
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .build()
}
```

## Error Handling

### API Result Wrapper

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val exception: Throwable) : ApiResult<Nothing>()
    data class HttpError(val code: Int, val message: String) : ApiResult<Nothing>()
}

suspend fun <T> safeApiCall(
    apiCall: suspend () -> T
): ApiResult<T> {
    return try {
        ApiResult.Success(apiCall())
    } catch (e: HttpException) {
        ApiResult.HttpError(
            code = e.code(),
            message = e.message()
        )
    } catch (e: IOException) {
        ApiResult.Error(e)
    } catch (e: Exception) {
        ApiResult.Error(e)
    }
}

// Usage in Repository
override suspend fun getUsers(): Result<List<User>> {
    return when (val result = safeApiCall { userApi.getUsers() }) {
        is ApiResult.Success -> {
            val users = result.data.map { userMapper.toDomain(it) }
            Result.success(users)
        }
        is ApiResult.HttpError -> {
            Result.failure(Exception(result.message))
        }
        is ApiResult.Error -> {
            Result.failure(result.exception)
        }
    }
}
```

### Custom Error Response

```kotlin
data class ErrorResponse(
    val message: String,
    val errors: Map<String, List<String>>?
)

suspend fun <T> handleApiError(
    call: suspend () -> Response<T>
): ApiResult<T> {
    return try {
        val response = call()
        if (response.isSuccessful) {
            response.body()?.let {
                ApiResult.Success(it)
            } ?: ApiResult.Error(Exception("Empty response body"))
        } else {
            val errorBody = response.errorBody()?.string()
            val errorResponse = Gson().fromJson(errorBody, ErrorResponse::class.java)
            ApiResult.HttpError(
                code = response.code(),
                message = errorResponse?.message ?: "Unknown error"
            )
        }
    } catch (e: Exception) {
        ApiResult.Error(e)
    }
}
```

## Advanced Patterns

### Token Refresh

```kotlin
class TokenAuthenticator @Inject constructor(
    private val tokenManager: TokenManager,
    private val authApi: AuthApi
) : Authenticator {

    override fun authenticate(route: Route?, response: Response): Request? {
        // Don't retry if we've already attempted to refresh
        if (response.request.header("Authorization") != null) {
            val currentToken = tokenManager.getToken()
            val requestToken = response.request.header("Authorization")?.removePrefix("Bearer ")

            if (currentToken != requestToken) {
                // Token already refreshed, retry with new token
                return response.request.newBuilder()
                    .header("Authorization", "Bearer $currentToken")
                    .build()
            }
        }

        // Refresh token
        return synchronized(this) {
            val refreshToken = tokenManager.getRefreshToken()
            if (refreshToken.isNullOrEmpty()) {
                return null
            }

            try {
                val newToken = runBlocking {
                    authApi.refreshToken(refreshToken)
                }
                tokenManager.saveToken(newToken.accessToken)

                response.request.newBuilder()
                    .header("Authorization", "Bearer ${newToken.accessToken}")
                    .build()
            } catch (e: Exception) {
                null
            }
        }
    }
}

// Add to OkHttpClient
.authenticator(tokenAuthenticator)
```

### File Upload

```kotlin
suspend fun uploadImage(uri: Uri, context: Context): ApiResult<String> {
    val file = uriToFile(uri, context)

    val requestFile = file.asRequestBody("image/*".toMediaTypeOrNull())
    val body = MultipartBody.Part.createFormData("image", file.name, requestFile)

    return safeApiCall {
        userApi.uploadAvatar("userId", body)
    }
}

private fun uriToFile(uri: Uri, context: Context): File {
    val inputStream = context.contentResolver.openInputStream(uri)
    val file = File(context.cacheDir, "upload_${System.currentTimeMillis()}.jpg")
    inputStream?.use { input ->
        file.outputStream().use { output ->
            input.copyTo(output)
        }
    }
    return file
}
```

### Response Caching

```kotlin
@Provides
@Singleton
fun provideOkHttpClient(
    @ApplicationContext context: Context
): OkHttpClient {
    val cacheSize = 10 * 1024 * 1024 // 10 MB
    val cache = Cache(context.cacheDir, cacheSize.toLong())

    return OkHttpClient.Builder()
        .cache(cache)
        .addNetworkInterceptor { chain ->
            val response = chain.proceed(chain.request())
            val cacheControl = CacheControl.Builder()
                .maxAge(5, TimeUnit.MINUTES)
                .build()

            response.newBuilder()
                .header("Cache-Control", cacheControl.toString())
                .build()
        }
        .build()
}
```

## Testing

```kotlin
class UserApiTest {

    private lateinit var mockWebServer: MockWebServer
    private lateinit var userApi: UserApi

    @Before
    fun setup() {
        mockWebServer = MockWebServer()
        mockWebServer.start()

        val retrofit = Retrofit.Builder()
            .baseUrl(mockWebServer.url("/"))
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        userApi = retrofit.create(UserApi::class.java)
    }

    @After
    fun teardown() {
        mockWebServer.shutdown()
    }

    @Test
    fun `getUsers returns list of users`() = runTest {
        // Given
        val responseBody = """
            [
                {"id": "1", "name": "John", "email": "john@example.com", "avatar_url": null, "created_at": 0}
            ]
        """.trimIndent()

        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(responseBody)
        )

        // When
        val users = userApi.getUsers()

        // Then
        assertEquals(1, users.size)
        assertEquals("John", users[0].name)

        val request = mockWebServer.takeRequest()
        assertEquals("/users", request.path)
        assertEquals("GET", request.method)
    }
}
```

## Related Skills
- **android-repository-pattern**: For API integration in repository
- **android-hilt-di**: For Retrofit injection
- **android-coroutines**: For async API calls

## Best Practices
1. **Use suspend functions**: For Coroutines integration
2. **Error handling**: Always handle network errors
3. **Logging**: Use logging interceptor in debug only
4. **Timeouts**: Set reasonable timeout values
5. **Authentication**: Use interceptors for auth headers
6. **Token refresh**: Implement authenticator for token refresh
7. **DTOs**: Separate DTOs from domain models
8. **Testing**: Use MockWebServer for API tests
