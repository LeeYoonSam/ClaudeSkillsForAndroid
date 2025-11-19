---
name: android-koin-di
description: Configure dependency injection with Koin using Kotlin DSL for lightweight runtime DI. Use when preferring simpler setup over compile-time validation.
---

# Koin Dependency Injection

Configure Koin for lightweight, Kotlin-DSL based dependency injection.

## When to Use
- Simpler DI setup preferred over Hilt
- Learning DI concepts
- Smaller projects
- Kotlin-first projects

## Setup

### Dependencies

```kotlin
// libs.versions.toml
[versions]
koin = "4.0.0"

[libraries]
koin-android = { group = "io.insert-koin", name = "koin-android", version.ref = "koin" }
koin-androidx-compose = { group = "io.insert-koin", name = "koin-androidx-compose", version.ref = "koin" }

// build.gradle.kts
dependencies {
    implementation(libs.koin.android)
    implementation(libs.koin.androidx.compose)
}
```

### Application Class

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        startKoin {
            androidLogger()
            androidContext(this@MyApplication)
            modules(
                appModule,
                networkModule,
                databaseModule,
                repositoryModule,
                viewModelModule
            )
        }
    }
}
```

## Defining Modules

### ViewModel Module

```kotlin
val viewModelModule = module {
    viewModel { HomeViewModel(get(), get()) }
    viewModel { (userId: String) ->
        ProfileViewModel(userId, get())
    }
    viewModel { ProductListViewModel(get()) }
}
```

### Repository Module

```kotlin
val repositoryModule = module {
    single<UserRepository> { UserRepositoryImpl(get(), get()) }
    single<ProductRepository> { ProductRepositoryImpl(get(), get()) }
    factory { CartRepository(get()) }
}
```

### Network Module

```kotlin
val networkModule = module {
    single {
        OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .build()
    }

    single {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(get())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    single { get<Retrofit>().create(UserApi::class.java) }
    single { get<Retrofit>().create(ProductApi::class.java) }
}
```

### Database Module

```kotlin
val databaseModule = module {
    single {
        Room.databaseBuilder(
            androidContext(),
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    single { get<AppDatabase>().userDao() }
    single { get<AppDatabase>().productDao() }
}
```

### Use Case Module

```kotlin
val useCaseModule = module {
    factory { GetUsersUseCase(get()) }
    factory { GetUserByIdUseCase(get()) }
    factory { CreateUserUseCase(get()) }
}
```

## Injection

### In ViewModel

```kotlin
class HomeViewModel(
    private val getUsersUseCase: GetUsersUseCase,
    private val analytics: Analytics
) : ViewModel() {
    // Implementation
}
```

### In Compose

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    // UI implementation
}

// With parameters
@Composable
fun ProfileScreen(
    userId: String,
    viewModel: ProfileViewModel = koinViewModel { parametersOf(userId) }
) {
    // UI implementation
}
```

### In Activity

```kotlin
class MainActivity : ComponentActivity() {

    private val analytics: Analytics by inject()

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

### In Fragment

```kotlin
class HomeFragment : Fragment() {

    private val viewModel: HomeViewModel by viewModel()
    private val repository: UserRepository by inject()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        // Use viewModel and repository
    }
}
```

## Scopes and Qualifiers

### Named Qualifiers

```kotlin
val module = module {
    single(named("io")) { Dispatchers.IO }
    single(named("main")) { Dispatchers.Main }
    single(named("default")) { Dispatchers.Default }
}

// Usage
class HomeViewModel(
    @Named("io") private val ioDispatcher: CoroutineDispatcher
) : ViewModel()
```

### Scoped Instances

```kotlin
val appModule = module {
    // Singleton - one instance for entire app
    single<UserRepository> { UserRepositoryImpl(get()) }

    // Factory - new instance each time
    factory { GetUsersUseCase(get()) }

    // Scoped - one instance per scope
    scope<HomeActivity> {
        scoped { HomePresenter() }
    }
}
```

## Testing

### Test Module

```kotlin
val testModule = module {
    single<UserRepository> { FakeUserRepository() }
    single<ProductRepository> { FakeProductRepository() }
}

class HomeViewModelTest {

    @Before
    fun setup() {
        startKoin {
            modules(testModule)
        }
    }

    @After
    fun tearDown() {
        stopKoin()
    }

    @Test
    fun testLoadUsers() {
        val viewModel: HomeViewModel = get()
        // Test implementation
    }
}
```

### Override in Tests

```kotlin
@Test
fun testWithMock() {
    val mockRepository = mockk<UserRepository>()

    startKoin {
        modules(module {
            single<UserRepository> { mockRepository }
        })
    }

    // Test with mock
}
```

## Related Skills
- **android-mvvm-architecture**: For ViewModel patterns
- **android-repository-pattern**: For repository implementation
- **android-hilt-di**: Alternative DI framework

## Best Practices

1. **Module Organization**: Group related dependencies
2. **single vs factory**: Use `single` for stateful, `factory` for stateless
3. **Lazy Injection**: Use `by inject()` for lazy initialization
4. **Named Qualifiers**: Use for multiple implementations
5. **Test Modules**: Create separate modules for testing
6. **Start Early**: Initialize Koin in Application.onCreate()
7. **Check Modules**: Use `checkModules()` to verify at compile time (with koin-test)

## Koin vs Hilt

**Choose Koin when:**
- Simpler setup preferred
- Kotlin-only project
- Learning DI
- Runtime flexibility needed

**Choose Hilt when:**
- Compile-time validation required
- Large team/codebase
- Android-specific optimizations needed
- Following Google recommendations
