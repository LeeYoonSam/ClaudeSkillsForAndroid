---
name: android-hilt-di
description: Configure dependency injection with Hilt including modules, scopes, and ViewModelFactory. Use when setting up or adding DI to Android app for compile-time safe dependency management.
---

# Hilt Dependency Injection

Configure Hilt for compile-time safe dependency injection in Android apps.

## When to Use
- Setting up dependency injection
- Injecting dependencies into ViewModels
- Managing app-level and screen-level dependencies
- Testing with mock dependencies

## Setup

### Dependencies

```kotlin
// libs.versions.toml
[versions]
hilt = "2.51"
ksp = "2.1.0-1.0.29"

[libraries]
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }
androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version = "1.2.0" }

[plugins]
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }

// build.gradle.kts (app module)
plugins {
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
}

dependencies {
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.androidx.hilt.navigation.compose)
}
```

### Application Class

```kotlin
@HiltAndroidApp
class MyApplication : Application()
```

### AndroidManifest.xml

```xml
<application
    android:name=".MyApplication"
    ...>
</application>
```

## Injecting into Components

### Activity

```kotlin
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppTheme {
                AppNavigation()
            }
        }
    }
}
```

### ViewModel

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase,
    private val userRepository: UserRepository
) : ViewModel() {
    // ViewModel implementation
}

// Usage in Compose
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    // UI implementation
}
```

### Fragment

```kotlin
@AndroidEntryPoint
class HomeFragment : Fragment() {
    private val viewModel: HomeViewModel by viewModels()

    @Inject
    lateinit var analytics: AnalyticsService
}
```

## Providing Dependencies

### Module for Interfaces

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindUserRepository(
        impl: UserRepositoryImpl
    ): UserRepository

    @Binds
    @Singleton
    abstract fun bindProductRepository(
        impl: ProductRepositoryImpl
    ): ProductRepository
}
```

### Module for Concrete Types

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}
```

### Database Module

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(
        @ApplicationContext context: Context
    ): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }

    @Provides
    fun provideProductDao(database: AppDatabase): ProductDao {
        return database.productDao()
    }
}
```

### Providing Context

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    // ApplicationContext is automatically provided by Hilt
    @Provides
    @Singleton
    fun providePreferences(
        @ApplicationContext context: Context
    ): SharedPreferences {
        return context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    }
}
```

## Scopes

### Singleton (App-level)

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton  // Lives for entire app lifecycle
    fun provideUserRepository(): UserRepository {
        return UserRepositoryImpl()
    }
}
```

### ActivityRetainedScoped (ViewModel-level)

```kotlin
@Module
@InstallIn(ActivityRetainedComponent::class)
object ActivityRetainedModule {

    @Provides
    @ActivityRetainedScoped  // Survives configuration changes
    fun provideAnalytics(): Analytics {
        return AnalyticsImpl()
    }
}
```

### ActivityScoped

```kotlin
@Module
@InstallIn(ActivityComponent::class)
object ActivityModule {

    @Provides
    @ActivityScoped  // Lives for Activity lifecycle
    fun provideTracker(): Tracker {
        return TrackerImpl()
    }
}
```

## Qualifiers

### Define Qualifiers

```kotlin
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class IoDispatcher

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class MainDispatcher

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class DefaultDispatcher
```

### Provide with Qualifiers

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DispatcherModule {

    @Provides
    @IoDispatcher
    fun provideIoDispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Provides
    @MainDispatcher
    fun provideMainDispatcher(): CoroutineDispatcher = Dispatchers.Main

    @Provides
    @DefaultDispatcher
    fun provideDefaultDispatcher(): CoroutineDispatcher = Dispatchers.Default
}
```

### Inject with Qualifiers

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher,
    @MainDispatcher private val mainDispatcher: CoroutineDispatcher
) : ViewModel() {

    fun loadData() {
        viewModelScope.launch(ioDispatcher) {
            // Background work
        }
    }
}
```

## Testing with Hilt

### Test Module

```kotlin
@Module
@TestInstallIn(
    components = [SingletonComponent::class],
    replaces = [RepositoryModule::class]
)
abstract class TestRepositoryModule {

    @Binds
    @Singleton
    abstract fun bindUserRepository(
        impl: FakeUserRepository
    ): UserRepository
}
```

### Instrumentation Test

```kotlin
@HiltAndroidTest
class HomeScreenTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Before
    fun init() {
        hiltRule.inject()
    }

    @Test
    fun testHomeScreen() {
        composeTestRule.setContent {
            AppTheme {
                HomeScreen()
            }
        }

        composeTestRule.onNodeWithText("Welcome").assertIsDisplayed()
    }
}
```

### Unit Test with ViewModel

```kotlin
@HiltAndroidTest
class HomeViewModelTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @Inject
    lateinit var repository: UserRepository

    private lateinit var viewModel: HomeViewModel

    @Before
    fun setup() {
        hiltRule.inject()
        viewModel = HomeViewModel(repository)
    }

    @Test
    fun testLoadUsers() = runTest {
        // Test implementation
    }
}
```

## EntryPoint (Accessing from non-Android classes)

```kotlin
@EntryPoint
@InstallIn(SingletonComponent::class)
interface AnalyticsEntryPoint {
    fun analytics(): Analytics
}

// Usage in non-Android class
class SomeUtility {
    fun log(context: Context, message: String) {
        val entryPoint = EntryPointAccessors.fromApplication(
            context.applicationContext,
            AnalyticsEntryPoint::class.java
        )
        entryPoint.analytics().log(message)
    }
}
```

## Related Skills
- **android-mvvm-architecture**: For ViewModel patterns
- **android-repository-pattern**: For repository implementation
- **android-networking-retrofit**: For API service injection
- **android-database-room**: For database injection

## Best Practices

1. **Use @Singleton sparingly**: Only for truly app-scoped dependencies
2. **Prefer constructor injection**: Over field injection
3. **Use @Binds for interfaces**: More efficient than @Provides
4. **Qualify ambiguous types**: Use @Qualifier for multiple implementations
5. **Avoid @ApplicationContext abuse**: Don't leak contexts
6. **Test with Hilt**: Use @HiltAndroidTest for instrumentation tests
7. **Module organization**: Group related dependencies in same module
8. **Component selection**: Use appropriate component for dependency scope
