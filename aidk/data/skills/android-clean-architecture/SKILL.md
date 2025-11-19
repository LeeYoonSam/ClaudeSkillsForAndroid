---
name: android-clean-architecture
description: Implement Clean Architecture with three layers (presentation, domain, data) for Android apps. Use when structuring a new feature or refactoring code for better maintainability and testability.
---

# Clean Architecture for Android

Implement Clean Architecture principles with clear layer separation and dependency rules.

## When to Use
- Structuring a new Android feature
- Refactoring existing code for better maintainability
- Building scalable applications
- Improving testability and separation of concerns

## Architecture Overview

```
┌─────────────────────────────────────────┐
│        Presentation Layer               │
│  (UI, ViewModel, Compose/XML Views)     │
└──────────────┬──────────────────────────┘
               │ depends on
               ▼
┌─────────────────────────────────────────┐
│          Domain Layer                   │
│    (Use Cases, Domain Models)           │
└──────────────┬──────────────────────────┘
               │ depends on
               ▼
┌─────────────────────────────────────────┐
│           Data Layer                    │
│  (Repository, API, Database, Cache)     │
└─────────────────────────────────────────┘
```

## Dependency Rule
**Inner layers should never depend on outer layers**
- Presentation depends on Domain
- Domain depends on Data (abstractions only)
- Data implements interfaces defined in Domain

## Layer Responsibilities

### 1. Presentation Layer (`presentation/`)

**Responsibilities:**
- Display UI to users
- Handle user interactions
- Observe state changes
- Navigate between screens

**Components:**
- **UI**: Composable functions or Activities/Fragments
- **ViewModel**: Manages UI state, handles user events
- **State**: UI state data classes
- **Event**: One-time UI events (navigation, toasts)

**Package Structure:**
```
presentation/
├── ui/
│   ├── home/
│   │   ├── HomeScreen.kt
│   │   ├── HomeViewModel.kt
│   │   ├── HomeState.kt
│   │   └── HomeEvent.kt
│   ├── detail/
│   │   ├── DetailScreen.kt
│   │   └── DetailViewModel.kt
│   └── components/
│       └── SharedComponents.kt
└── theme/
    ├── Color.kt
    ├── Theme.kt
    └── Type.kt
```

**Example ViewModel:**
```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase,
    private val deleteUserUseCase: DeleteUserUseCase
) : ViewModel() {

    private val _state = MutableStateFlow(HomeState())
    val state: StateFlow<HomeState> = _state.asStateFlow()

    private val _events = Channel<HomeEvent>()
    val events = _events.receiveAsFlow()

    init {
        loadUsers()
    }

    fun onAction(action: HomeAction) {
        when (action) {
            is HomeAction.LoadUsers -> loadUsers()
            is HomeAction.DeleteUser -> deleteUser(action.userId)
            is HomeAction.NavigateToDetail -> navigateToDetail(action.userId)
        }
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            getUsersUseCase()
                .onSuccess { users ->
                    _state.update { it.copy(users = users, isLoading = false) }
                }
                .onFailure { error ->
                    _state.update { it.copy(error = error.message, isLoading = false) }
                }
        }
    }

    private fun deleteUser(userId: String) {
        viewModelScope.launch {
            deleteUserUseCase(userId)
                .onSuccess {
                    loadUsers()
                    _events.send(HomeEvent.ShowSuccess("User deleted"))
                }
                .onFailure { error ->
                    _events.send(HomeEvent.ShowError(error.message))
                }
        }
    }

    private fun navigateToDetail(userId: String) {
        viewModelScope.launch {
            _events.send(HomeEvent.NavigateToDetail(userId))
        }
    }
}

data class HomeState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

sealed interface HomeAction {
    data object LoadUsers : HomeAction
    data class DeleteUser(val userId: String) : HomeAction
    data class NavigateToDetail(val userId: String) : HomeAction
}

sealed interface HomeEvent {
    data class ShowSuccess(val message: String) : HomeEvent
    data class ShowError(val message: String?) : HomeEvent
    data class NavigateToDetail(val userId: String) : HomeEvent
}
```

### 2. Domain Layer (`domain/`)

**Responsibilities:**
- Define business logic
- Define data models
- Define repository interfaces
- Execute use cases

**Components:**
- **Model**: Domain entities (pure Kotlin classes)
- **UseCase**: Single business operation
- **Repository Interface**: Data access abstraction

**Package Structure:**
```
domain/
├── model/
│   ├── User.kt
│   ├── Product.kt
│   └── Order.kt
├── repository/
│   ├── UserRepository.kt
│   ├── ProductRepository.kt
│   └── OrderRepository.kt
└── usecase/
    ├── GetUsersUseCase.kt
    ├── GetUserByIdUseCase.kt
    ├── CreateUserUseCase.kt
    └── DeleteUserUseCase.kt
```

**Example Domain Model:**
```kotlin
data class User(
    val id: String,
    val name: String,
    val email: String,
    val avatarUrl: String?,
    val createdAt: Long
)
```

**Example Repository Interface:**
```kotlin
interface UserRepository {
    suspend fun getUsers(): Result<List<User>>
    suspend fun getUserById(id: String): Result<User>
    suspend fun createUser(user: User): Result<User>
    suspend fun updateUser(user: User): Result<User>
    suspend fun deleteUser(id: String): Result<Unit>
}
```

**Example Use Case:**
```kotlin
class GetUsersUseCase @Inject constructor(
    private val userRepository: UserRepository,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend operator fun invoke(): Result<List<User>> {
        return withContext(dispatcher) {
            userRepository.getUsers()
        }
    }
}

class DeleteUserUseCase @Inject constructor(
    private val userRepository: UserRepository,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend operator fun invoke(userId: String): Result<Unit> {
        return withContext(dispatcher) {
            userRepository.deleteUser(userId)
        }
    }
}
```

### 3. Data Layer (`data/`)

**Responsibilities:**
- Implement repository interfaces
- Handle data sources (API, Database, Cache)
- Map between data models and domain models
- Manage data caching strategy

**Components:**
- **Repository Implementation**: Implements domain repository interface
- **Data Source**: API, Database, Cache implementations
- **DTO (Data Transfer Object)**: Network/Database models
- **Mapper**: Convert between DTOs and Domain models

**Package Structure:**
```
data/
├── local/
│   ├── dao/
│   │   └── UserDao.kt
│   ├── entity/
│   │   └── UserEntity.kt
│   └── database/
│       └── AppDatabase.kt
├── remote/
│   ├── api/
│   │   └── UserApi.kt
│   └── dto/
│       └── UserDto.kt
├── mapper/
│   ├── UserMapper.kt
│   └── ProductMapper.kt
└── repository/
    └── UserRepositoryImpl.kt
```

**Example Repository Implementation:**
```kotlin
class UserRepositoryImpl @Inject constructor(
    private val userApi: UserApi,
    private val userDao: UserDao,
    private val userMapper: UserMapper
) : UserRepository {

    override suspend fun getUsers(): Result<List<User>> {
        return try {
            // Try to get from cache first
            val cachedUsers = userDao.getAllUsers()
            if (cachedUsers.isNotEmpty()) {
                Result.success(cachedUsers.map { userMapper.toDomain(it) })
            } else {
                // Fetch from network
                val response = userApi.getUsers()
                val users = response.map { userMapper.toDomain(it) }

                // Cache in database
                userDao.insertUsers(response.map { userMapper.toEntity(it) })

                Result.success(users)
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getUserById(id: String): Result<User> {
        return try {
            val response = userApi.getUserById(id)
            val user = userMapper.toDomain(response)
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun createUser(user: User): Result<User> {
        return try {
            val dto = userMapper.toDto(user)
            val response = userApi.createUser(dto)
            val createdUser = userMapper.toDomain(response)
            Result.success(createdUser)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun updateUser(user: User): Result<User> {
        return try {
            val dto = userMapper.toDto(user)
            val response = userApi.updateUser(user.id, dto)
            val updatedUser = userMapper.toDomain(response)

            // Update cache
            userDao.updateUser(userMapper.toEntity(response))

            Result.success(updatedUser)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun deleteUser(id: String): Result<Unit> {
        return try {
            userApi.deleteUser(id)
            userDao.deleteUserById(id)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

**Example Mapper:**
```kotlin
class UserMapper @Inject constructor() {

    fun toDomain(dto: UserDto): User {
        return User(
            id = dto.id,
            name = dto.name,
            email = dto.email,
            avatarUrl = dto.avatar_url,
            createdAt = dto.created_at
        )
    }

    fun toDomain(entity: UserEntity): User {
        return User(
            id = entity.id,
            name = entity.name,
            email = entity.email,
            avatarUrl = entity.avatarUrl,
            createdAt = entity.createdAt
        )
    }

    fun toDto(user: User): UserDto {
        return UserDto(
            id = user.id,
            name = user.name,
            email = user.email,
            avatar_url = user.avatarUrl,
            created_at = user.createdAt
        )
    }

    fun toEntity(dto: UserDto): UserEntity {
        return UserEntity(
            id = dto.id,
            name = dto.name,
            email = dto.email,
            avatarUrl = dto.avatar_url,
            createdAt = dto.created_at
        )
    }
}
```

## Dependency Injection Setup

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindUserRepository(
        impl: UserRepositoryImpl
    ): UserRepository
}

@Module
@InstallIn(SingletonComponent::class)
object DataModule {

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}
```

## Benefits of Clean Architecture

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Clear separation of concerns
3. **Scalability**: Easy to add new features
4. **Independence**: Business logic independent of frameworks
5. **Flexibility**: Easy to change data sources or UI

## Data Flow Example

```
User clicks button
        ↓
UI calls ViewModel.onAction()
        ↓
ViewModel calls UseCase()
        ↓
UseCase calls Repository (interface)
        ↓
Repository (implementation) calls API/Database
        ↓
Data flows back through layers
        ↓
ViewModel updates State
        ↓
UI recomposes with new State
```

## Related Skills
- **android-mvvm-architecture**: For ViewModel and state management patterns
- **android-repository-pattern**: For detailed repository implementation
- **android-hilt-di**: For dependency injection setup
- **android-coroutines**: For async operations in use cases
- **android-compose-ui**: For presentation layer UI implementation

## Best Practices

1. **Single Responsibility**: Each use case should do one thing
2. **Dependency Inversion**: Depend on abstractions, not implementations
3. **Result Wrapper**: Use `Result<T>` for error handling
4. **Mapper Pattern**: Always map between layer-specific models
5. **Repository as Single Source**: Repository decides cache strategy
6. **No Android Dependencies in Domain**: Keep domain layer pure Kotlin
7. **Use Cases Are Optional**: For simple apps, ViewModels can call repositories directly
8. **Modularization**: Consider separate modules for each layer in large projects
