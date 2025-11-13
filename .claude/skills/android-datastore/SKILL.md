---
name: android-datastore
description: Implement DataStore for preferences and simple key-value storage using Coroutines. Use when replacing SharedPreferences or storing app settings.
---

# DataStore

Implement DataStore for type-safe, async key-value storage.

## When to Use
- Storing app preferences
- User settings
- Replacing SharedPreferences
- Small amounts of data
- Type-safe storage

## Dependencies

```kotlin
// libs.versions.toml
[versions]
datastore = "1.1.1"

[libraries]
androidx-datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }
androidx-datastore-core = { group = "androidx.datastore", name = "datastore-core", version.ref = "datastore" }

// build.gradle.kts
dependencies {
    implementation(libs.androidx.datastore.preferences)
    // For Proto DataStore
    implementation(libs.androidx.datastore.core)
}
```

## Preferences DataStore

### Setup

```kotlin
private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(
    name = "app_preferences"
)

@Module
@InstallIn(SingletonComponent::class)
object DataStoreModule {

    @Provides
    @Singleton
    fun provideDataStore(
        @ApplicationContext context: Context
    ): DataStore<Preferences> {
        return context.dataStore
    }
}
```

### PreferencesManager

```kotlin
class PreferencesManager @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {
    // Define keys
    private object Keys {
        val IS_DARK_THEME = booleanPreferencesKey("is_dark_theme")
        val USER_NAME = stringPreferencesKey("user_name")
        val USER_AGE = intPreferencesKey("user_age")
        val LANGUAGE = stringPreferencesKey("language")
        val NOTIFICATION_ENABLED = booleanPreferencesKey("notification_enabled")
    }

    // Read preferences
    val isDarkTheme: Flow<Boolean> = dataStore.data
        .map { preferences ->
            preferences[Keys.IS_DARK_THEME] ?: false
        }
        .catch { exception ->
            if (exception is IOException) {
                emit(false)
            } else {
                throw exception
            }
        }

    val userName: Flow<String> = dataStore.data
        .map { preferences ->
            preferences[Keys.USER_NAME] ?: ""
        }

    // Write preferences
    suspend fun setDarkTheme(enabled: Boolean) {
        dataStore.edit { preferences ->
            preferences[Keys.IS_DARK_THEME] = enabled
        }
    }

    suspend fun setUserName(name: String) {
        dataStore.edit { preferences ->
            preferences[Keys.USER_NAME] = name
        }
    }

    suspend fun setLanguage(language: String) {
        dataStore.edit { preferences ->
            preferences[Keys.LANGUAGE] = language
        }
    }

    suspend fun clear() {
        dataStore.edit { preferences ->
            preferences.clear()
        }
    }

    // Complex object (JSON)
    suspend fun saveUser(user: User) {
        val json = Gson().toJson(user)
        dataStore.edit { preferences ->
            preferences[stringPreferencesKey("user")] = json
        }
    }

    val user: Flow<User?> = dataStore.data
        .map { preferences ->
            val json = preferences[stringPreferencesKey("user")]
            json?.let { Gson().fromJson(it, User::class.java) }
        }
}
```

### Usage in ViewModel

```kotlin
@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val preferencesManager: PreferencesManager
) : ViewModel() {

    val isDarkTheme: StateFlow<Boolean> = preferencesManager.isDarkTheme
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = false
        )

    fun toggleDarkTheme() {
        viewModelScope.launch {
            preferencesManager.setDarkTheme(!isDarkTheme.value)
        }
    }

    fun updateUserName(name: String) {
        viewModelScope.launch {
            preferencesManager.setUserName(name)
        }
    }
}
```

### Usage in Compose

```kotlin
@Composable
fun SettingsScreen(
    viewModel: SettingsViewModel = hiltViewModel()
) {
    val isDarkTheme by viewModel.isDarkTheme.collectAsStateWithLifecycle()

    Column {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Dark Mode")
            Switch(
                checked = isDarkTheme,
                onCheckedChange = { viewModel.toggleDarkTheme() }
            )
        }
    }
}
```

## Proto DataStore

For more complex, type-safe storage:

### Define Proto Schema (user_preferences.proto)

```protobuf
syntax = "proto3";

option java_package = "com.example.app";
option java_multiple_files = true;

message UserPreferences {
    bool is_dark_theme = 1;
    string user_name = 2;
    int32 user_age = 3;
    string language = 4;
    bool notification_enabled = 5;
}
```

### Serializer

```kotlin
object UserPreferencesSerializer : Serializer<UserPreferences> {
    override val defaultValue: UserPreferences = UserPreferences.getDefaultInstance()

    override suspend fun readFrom(input: InputStream): UserPreferences {
        try {
            return UserPreferences.parseFrom(input)
        } catch (exception: InvalidProtocolBufferException) {
            throw CorruptionException("Cannot read proto.", exception)
        }
    }

    override suspend fun writeTo(t: UserPreferences, output: OutputStream) {
        t.writeTo(output)
    }
}
```

### Setup Proto DataStore

```kotlin
private val Context.userPreferencesDataStore: DataStore<UserPreferences> by dataStore(
    fileName = "user_preferences.pb",
    serializer = UserPreferencesSerializer
)

@Provides
@Singleton
fun provideProtoDataStore(
    @ApplicationContext context: Context
): DataStore<UserPreferences> {
    return context.userPreferencesDataStore
}
```

### Proto DataStore Manager

```kotlin
class UserPreferencesManager @Inject constructor(
    private val dataStore: DataStore<UserPreferences>
) {
    val userPreferences: Flow<UserPreferences> = dataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(UserPreferences.getDefaultInstance())
            } else {
                throw exception
            }
        }

    suspend fun updateDarkTheme(enabled: Boolean) {
        dataStore.updateData { currentPreferences ->
            currentPreferences.toBuilder()
                .setIsDarkTheme(enabled)
                .build()
        }
    }

    suspend fun updateUserName(name: String) {
        dataStore.updateData { currentPreferences ->
            currentPreferences.toBuilder()
                .setUserName(name)
                .build()
        }
    }
}
```

## Migration from SharedPreferences

```kotlin
val sharedPrefsMigration = SharedPreferencesMigration(
    context = context,
    sharedPreferencesName = "old_shared_prefs"
) { sharedPrefs, currentData ->
    if (currentData[Keys.IS_DARK_THEME] == null) {
        currentData.toMutablePreferences().apply {
            this[Keys.IS_DARK_THEME] = sharedPrefs.getBoolean("dark_theme", false)
            this[Keys.USER_NAME] = sharedPrefs.getString("user_name", "") ?: ""
        }
    } else {
        currentData
    }
}

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(
    name = "app_preferences",
    produceMigrations = { context ->
        listOf(sharedPrefsMigration)
    }
)
```

## Advanced Patterns

### Multiple DataStores

```kotlin
// User preferences
private val Context.userDataStore: DataStore<Preferences> by preferencesDataStore(
    name = "user_preferences"
)

// App settings
private val Context.appDataStore: DataStore<Preferences> by preferencesDataStore(
    name = "app_settings"
)

@Module
@InstallIn(SingletonComponent::class)
object DataStoreModule {

    @Provides
    @Singleton
    @Named("user")
    fun provideUserDataStore(
        @ApplicationContext context: Context
    ): DataStore<Preferences> = context.userDataStore

    @Provides
    @Singleton
    @Named("app")
    fun provideAppDataStore(
        @ApplicationContext context: Context
    ): DataStore<Preferences> = context.appDataStore
}

class PreferencesManager @Inject constructor(
    @Named("user") private val userDataStore: DataStore<Preferences>,
    @Named("app") private val appDataStore: DataStore<Preferences>
) {
    // Use different datastores
}
```

### Encrypted DataStore

```kotlin
// Add dependency
implementation("androidx.security:security-crypto:1.1.0-alpha06")

private val Context.encryptedDataStore: DataStore<Preferences> by preferencesDataStore(
    name = "encrypted_preferences",
    produceMigrations = { context ->
        listOf()
    }
)

// For sensitive data, consider using EncryptedSharedPreferences
// or implementing custom encryption
```

## Testing

```kotlin
class PreferencesManagerTest {

    private lateinit var preferencesManager: PreferencesManager
    private lateinit var dataStore: DataStore<Preferences>

    @Before
    fun setup() {
        val testContext = InstrumentationRegistry.getInstrumentation().targetContext
        dataStore = PreferenceDataStoreFactory.create(
            scope = TestScope(UnconfinedTestDispatcher()),
            produceFile = {
                testContext.preferencesDataStoreFile("test_prefs")
            }
        )
        preferencesManager = PreferencesManager(dataStore)
    }

    @Test
    fun testSetDarkTheme() = runTest {
        // When
        preferencesManager.setDarkTheme(true)

        // Then
        val isDarkTheme = preferencesManager.isDarkTheme.first()
        assertTrue(isDarkTheme)
    }
}
```

## Related Skills
- **android-compose-theming**: For theme preference storage
- **android-hilt-di**: For DataStore injection

## Best Practices
1. **Use Flows**: DataStore returns Flows, not blocking calls
2. **Error Handling**: Use .catch() to handle IOExceptions
3. **Structured Concurrency**: Operations are cancellable
4. **Proto for Complex Data**: Use Proto DataStore for structured data
5. **Migration**: Migrate from SharedPreferences
6. **Don't store large data**: Use Room for large datasets
7. **Type Safety**: Use proper key types (stringPreferencesKey, etc.)
8. **Single Instance**: Use Singleton scope for DataStore
