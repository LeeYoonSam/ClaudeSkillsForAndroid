---
name: android-repository-pattern
description: Implement repository pattern with single source of truth for data access. Use when abstracting data sources (network, database, cache) in the data layer.
---

# Repository Pattern

Implement repository pattern as single source of truth for data access.

## When to Use
- Abstracting data sources
- Implementing caching strategy
- Coordinating multiple data sources
- Clean Architecture data layer

## Repository Interface (Domain Layer)

```kotlin
interface UserRepository {
    suspend fun getUsers(): Result<List<User>>
    suspend fun getUserById(id: String): Result<User>
    suspend fun createUser(user: User): Result<User>
    suspend fun updateUser(user: User): Result<User>
    suspend fun deleteUser(id: String): Result<Unit>
    fun observeUsers(): Flow<List<User>>
}
```

## Repository Implementation (Data Layer)

```kotlin
class UserRepositoryImpl @Inject constructor(
    private val userApi: UserApi,
    private val userDao: UserDao,
    private val userMapper: UserMapper,
    @IoDispatcher private val dispatcher: CoroutineDispatcher
) : UserRepository {

    override suspend fun getUsers(): Result<List<User>> = withContext(dispatcher) {
        try {
            // Try cache first
            val cachedUsers = userDao.getAllUsers()
            if (cachedUsers.isNotEmpty()) {
                return@withContext Result.success(cachedUsers.map { userMapper.toDomain(it) })
            }

            // Fetch from network
            val response = userApi.getUsers()
            val users = response.map { userMapper.toDomain(it) }

            // Update cache
            userDao.insertUsers(response.map { userMapper.toEntity(it) })

            Result.success(users)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getUserById(id: String): Result<User> = withContext(dispatcher) {
        try {
            val response = userApi.getUserById(id)
            val user = userMapper.toDomain(response)

            // Update cache
            userDao.insertUser(userMapper.toEntity(response))

            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun createUser(user: User): Result<User> = withContext(dispatcher) {
        try {
            val dto = userMapper.toDto(user)
            val response = userApi.createUser(dto)
            val createdUser = userMapper.toDomain(response)

            // Cache new user
            userDao.insertUser(userMapper.toEntity(response))

            Result.success(createdUser)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun updateUser(user: User): Result<User> = withContext(dispatcher) {
        try {
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

    override suspend fun deleteUser(id: String): Result<Unit> = withContext(dispatcher) {
        try {
            userApi.deleteUser(id)
            userDao.deleteUserById(id)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override fun observeUsers(): Flow<List<User>> {
        return userDao.observeUsers()
            .map { entities -> entities.map { userMapper.toDomain(it) } }
            .flowOn(dispatcher)
    }
}
```

## Caching Strategies

### Cache-First (Offline-First)

```kotlin
override suspend fun getUsers(): Result<List<User>> {
    return try {
        // 1. Return cache immediately
        val cached = userDao.getAllUsers()
        if (cached.isNotEmpty()) {
            // 2. Refresh in background
            refreshUsers()
            return Result.success(cached.map { userMapper.toDomain(it) })
        }

        // 3. No cache, fetch from network
        val response = userApi.getUsers()
        userDao.insertUsers(response.map { userMapper.toEntity(it) })
        Result.success(response.map { userMapper.toDomain(it) })
    } catch (e: Exception) {
        Result.failure(e)
    }
}
```

### Network-First

```kotlin
override suspend fun getUsers(): Result<List<User>> {
    return try {
        // 1. Try network first
        val response = userApi.getUsers()
        userDao.insertUsers(response.map { userMapper.toEntity(it) })
        Result.success(response.map { userMapper.toDomain(it) })
    } catch (e: Exception) {
        // 2. Fallback to cache on network error
        val cached = userDao.getAllUsers()
        if (cached.isNotEmpty()) {
            Result.success(cached.map { userMapper.toDomain(it) })
        } else {
            Result.failure(e)
        }
    }
}
```

### Cache with Timeout

```kotlin
class UserRepositoryImpl @Inject constructor(
    private val userApi: UserApi,
    private val userDao: UserDao,
    private val cacheManager: CacheManager
) : UserRepository {

    override suspend fun getUsers(): Result<List<User>> {
        return try {
            // Check if cache is still valid
            if (cacheManager.isCacheValid("users")) {
                val cached = userDao.getAllUsers()
                if (cached.isNotEmpty()) {
                    return Result.success(cached.map { userMapper.toDomain(it) })
                }
            }

            // Cache expired or empty, fetch from network
            val response = userApi.getUsers()
            userDao.insertUsers(response.map { userMapper.toEntity(it) })
            cacheManager.updateCacheTime("users")

            Result.success(response.map { userMapper.toDomain(it) })
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

## Data Mapper

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

## Dependency Injection

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
object DispatcherModule {

    @Provides
    @IoDispatcher
    fun provideIoDispatcher(): CoroutineDispatcher = Dispatchers.IO
}
```

## Testing Repository

```kotlin
class UserRepositoryImplTest {

    private lateinit var repository: UserRepositoryImpl
    private lateinit var userApi: UserApi
    private lateinit var userDao: UserDao
    private lateinit var mapper: UserMapper

    @Before
    fun setup() {
        userApi = mockk()
        userDao = mockk()
        mapper = UserMapper()
        repository = UserRepositoryImpl(userApi, userDao, mapper, Dispatchers.Unconfined)
    }

    @Test
    fun `getUsers returns cached data when available`() = runTest {
        // Given
        val entities = listOf(UserEntity("1", "John", "john@example.com", null, 0))
        coEvery { userDao.getAllUsers() } returns entities

        // When
        val result = repository.getUsers()

        // Then
        assertTrue(result.isSuccess)
        assertEquals(1, result.getOrNull()?.size)
        coVerify(exactly = 0) { userApi.getUsers() }
    }
}
```

## Related Skills
- **android-clean-architecture**: For overall architecture
- **android-database-room**: For local data source
- **android-networking-retrofit**: For remote data source
- **android-hilt-di**: For dependency injection

## Best Practices
1. **Single Source of Truth**: Repository decides data source
2. **Result Wrapper**: Use Result<T> for error handling
3. **Mapper Pattern**: Map between DTOs, Entities, and Domain models
4. **IO Dispatcher**: Use IO dispatcher for database/network operations
5. **Cache Strategy**: Choose appropriate caching strategy
6. **Flow for Observables**: Use Flow for reactive data
7. **Error Handling**: Handle all exceptions gracefully
