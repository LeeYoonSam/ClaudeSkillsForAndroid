---
name: android-paging3
description: Implement pagination with Paging 3 library for efficient large dataset loading. Use when displaying lists with network or database pagination.
---

# Paging 3

Implement efficient pagination for large datasets.

## When to Use
- Loading large lists from network/database
- Infinite scroll
- Efficient memory usage
- Network + Database caching

## Dependencies

```kotlin
implementation("androidx.paging:paging-runtime-ktx:3.3.6")
implementation("androidx.paging:paging-compose:3.3.6")
```

## PagingSource

```kotlin
class UserPagingSource(
    private val api: UserApi
) : PagingSource<Int, User>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, User> {
        return try {
            val page = params.key ?: 1
            val response = api.getUsers(page, params.loadSize)

            LoadResult.Page(
                data = response.map { it.toDomain() },
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (response.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, User>): Int? {
        return state.anchorPosition?.let { anchorPosition ->
            state.closestPageToPosition(anchorPosition)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchorPosition)?.nextKey?.minus(1)
        }
    }
}
```

## Repository

```kotlin
class UserRepository @Inject constructor(
    private val api: UserApi
) {
    fun getUsers(): Flow<PagingData<User>> {
        return Pager(
            config = PagingConfig(
                pageSize = 20,
                prefetchDistance = 5,
                enablePlaceholders = false
            ),
            pagingSourceFactory = { UserPagingSource(api) }
        ).flow
    }
}
```

## ViewModel

```kotlin
@HiltViewModel
class UserListViewModel @Inject constructor(
    repository: UserRepository
) : ViewModel() {

    val users: Flow<PagingData<User>> = repository.getUsers()
        .cachedIn(viewModelScope)
}
```

## Compose UI

```kotlin
@Composable
fun UserListScreen(viewModel: UserListViewModel = hiltViewModel()) {
    val users = viewModel.users.collectAsLazyPagingItems()

    LazyColumn {
        items(
            count = users.itemCount,
            key = { index -> users[index]?.id ?: index }
        ) { index ->
            users[index]?.let { user ->
                UserItem(user = user)
            }
        }

        users.apply {
            when (loadState.refresh) {
                is LoadState.Loading -> {
                    item { LoadingItem() }
                }
                is LoadState.Error -> {
                    item { ErrorItem { users.retry() } }
                }
                else -> {}
            }

            when (loadState.append) {
                is LoadState.Loading -> {
                    item { LoadingItem() }
                }
                is LoadState.Error -> {
                    item { ErrorItem { users.retry() } }
                }
                else -> {}
            }
        }
    }
}
```

## Best Practices
1. Use `cachedIn(viewModelScope)` to cache
2. Handle loading states (refresh, append, prepend)
3. Provide item keys for Compose
4. Set appropriate `pageSize` and `prefetchDistance`
5. Use `RemoteMediator` for network + DB caching
