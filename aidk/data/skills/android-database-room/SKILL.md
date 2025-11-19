---
name: android-database-room
description: Create local database with Room including entities, DAOs, and database setup with migrations. Use when implementing local data persistence with type-safe SQL queries.
---

# Room Database

Implement local database with Room for type-safe SQL access.

## When to Use
- Local data persistence
- Offline-first architecture
- Caching network data
- Complex queries with relations

## Dependencies

```kotlin
// libs.versions.toml
[versions]
room = "2.6.1"

[libraries]
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

// build.gradle.kts
dependencies {
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
}
```

## Entity

```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey
    val id: String,
    val name: String,
    val email: String,
    val avatarUrl: String?,
    val createdAt: Long
)

@Entity(
    tableName = "products",
    indices = [Index(value = ["categoryId"])]
)
data class ProductEntity(
    @PrimaryKey
    val id: String,
    val name: String,
    val price: Double,
    val categoryId: String,
    @ColumnInfo(name = "image_url")
    val imageUrl: String?,
    val createdAt: Long = System.currentTimeMillis()
)
```

## DAO (Data Access Object)

```kotlin
@Dao
interface UserDao {

    @Query("SELECT * FROM users ORDER BY createdAt DESC")
    suspend fun getAllUsers(): List<UserEntity>

    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: String): UserEntity?

    @Query("SELECT * FROM users ORDER BY createdAt DESC")
    fun observeUsers(): Flow<List<UserEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUsers(users: List<UserEntity>)

    @Update
    suspend fun updateUser(user: UserEntity)

    @Delete
    suspend fun deleteUser(user: UserEntity)

    @Query("DELETE FROM users WHERE id = :id")
    suspend fun deleteUserById(id: String)

    @Query("DELETE FROM users")
    suspend fun deleteAllUsers()

    @Query("SELECT * FROM users WHERE name LIKE '%' || :query || '%' OR email LIKE '%' || :query || '%'")
    suspend fun searchUsers(query: String): List<UserEntity>
}
```

## Database

```kotlin
@Database(
    entities = [
        UserEntity::class,
        ProductEntity::class,
        OrderEntity::class
    ],
    version = 1,
    exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun userDao(): UserDao
    abstract fun productDao(): ProductDao
    abstract fun orderDao(): OrderDao

    companion object {
        const val DATABASE_NAME = "app_database"
    }
}
```

## Database Injection (Hilt)

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
            AppDatabase.DATABASE_NAME
        )
            .fallbackToDestructiveMigration() // Remove in production
            .build()
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

## Relations

### One-to-Many

```kotlin
@Entity(tableName = "categories")
data class CategoryEntity(
    @PrimaryKey val id: String,
    val name: String
)

@Entity(
    tableName = "products",
    foreignKeys = [
        ForeignKey(
            entity = CategoryEntity::class,
            parentColumns = ["id"],
            childColumns = ["categoryId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class ProductEntity(
    @PrimaryKey val id: String,
    val name: String,
    val categoryId: String
)

data class CategoryWithProducts(
    @Embedded val category: CategoryEntity,
    @Relation(
        parentColumn = "id",
        entityColumn = "categoryId"
    )
    val products: List<ProductEntity>
)

@Dao
interface CategoryDao {
    @Transaction
    @Query("SELECT * FROM categories")
    suspend fun getCategoriesWithProducts(): List<CategoryWithProducts>
}
```

### Many-to-Many

```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String
)

@Entity(tableName = "groups")
data class GroupEntity(
    @PrimaryKey val id: String,
    val name: String
)

@Entity(
    tableName = "user_group_cross_ref",
    primaryKeys = ["userId", "groupId"]
)
data class UserGroupCrossRef(
    val userId: String,
    val groupId: String
)

data class UserWithGroups(
    @Embedded val user: UserEntity,
    @Relation(
        parentColumn = "id",
        entityColumn = "id",
        associateBy = Junction(
            value = UserGroupCrossRef::class,
            parentColumn = "userId",
            entityColumn = "groupId"
        )
    )
    val groups: List<GroupEntity>
)
```

## Migrations

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE users ADD COLUMN age INTEGER DEFAULT 0 NOT NULL")
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        // Create new table
        db.execSQL("""
            CREATE TABLE IF NOT EXISTS products_new (
                id TEXT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
        """)

        // Copy data
        db.execSQL("""
            INSERT INTO products_new (id, name, price, description)
            SELECT id, name, price, '' FROM products
        """)

        // Remove old table
        db.execSQL("DROP TABLE products")

        // Rename new table
        db.execSQL("ALTER TABLE products_new RENAME TO products")
    }
}

@Provides
@Singleton
fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
    return Room.databaseBuilder(
        context,
        AppDatabase::class.java,
        AppDatabase.DATABASE_NAME
    )
        .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
        .build()
}
```

## Type Converters

```kotlin
class Converters {

    @TypeConverter
    fun fromTimestamp(value: Long?): Date? {
        return value?.let { Date(it) }
    }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? {
        return date?.time
    }

    @TypeConverter
    fun fromStringList(value: String?): List<String>? {
        return value?.split(",")?.map { it.trim() }
    }

    @TypeConverter
    fun toStringList(list: List<String>?): String? {
        return list?.joinToString(",")
    }

    @TypeConverter
    fun fromJson(value: String?): UserMetadata? {
        return value?.let { Gson().fromJson(it, UserMetadata::class.java) }
    }

    @TypeConverter
    fun toJson(metadata: UserMetadata?): String? {
        return metadata?.let { Gson().toJson(it) }
    }
}

@Database(
    entities = [UserEntity::class],
    version = 1
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    // ...
}
```

## Testing

```kotlin
@RunWith(AndroidJUnit4::class)
class UserDaoTest {

    private lateinit var database: AppDatabase
    private lateinit var userDao: UserDao

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(
            context,
            AppDatabase::class.java
        ).build()
        userDao = database.userDao()
    }

    @After
    fun teardown() {
        database.close()
    }

    @Test
    fun insertAndGetUser() = runTest {
        // Given
        val user = UserEntity("1", "John", "john@example.com", null, 0)

        // When
        userDao.insertUser(user)
        val retrieved = userDao.getUserById("1")

        // Then
        assertEquals(user, retrieved)
    }

    @Test
    fun observeUsers() = runTest {
        // Given
        val users = listOf(
            UserEntity("1", "John", "john@example.com", null, 0),
            UserEntity("2", "Jane", "jane@example.com", null, 1)
        )

        // When
        userDao.insertUsers(users)

        // Then
        userDao.observeUsers().first { it.size == 2 }
    }
}
```

## Related Skills
- **android-repository-pattern**: For repository implementation
- **android-hilt-di**: For database injection
- **android-coroutines**: For async database operations

## Best Practices
1. **Use suspend functions**: For async operations
2. **Flow for observables**: Reactive database queries
3. **Indices**: Add indices for frequently queried columns
4. **Migrations**: Always provide migrations for production
5. **Type Converters**: For complex types
6. **Foreign Keys**: Use for referential integrity
7. **Transactions**: Use @Transaction for multiple operations
8. **In-Memory DB for tests**: Fast and isolated testing
