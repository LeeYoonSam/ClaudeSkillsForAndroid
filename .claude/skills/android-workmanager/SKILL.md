---
name: android-workmanager
description: Schedule background work with WorkManager for deferrable tasks. Use when implementing periodic sync, uploads, or tasks that must run even if app exits.
---

# WorkManager

Schedule deferrable background work guaranteed to execute.

## When to Use
- Periodic data sync
- Upload logs/analytics
- Background processing
- Tasks that must complete

## Dependencies

```kotlin
implementation("androidx.work:work-runtime-ktx:2.9.0")
implementation("androidx.hilt:hilt-work:1.2.0")
ksp("androidx.hilt:hilt-compiler:1.2.0")
```

## Worker

```kotlin
@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val repository: DataRepository
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        return try {
            val data = inputData.getString("user_id") ?: return Result.failure()

            repository.syncData(data)

            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure()
            }
        }
    }
}
```

## Scheduling Work

```kotlin
class WorkScheduler @Inject constructor(
    private val workManager: WorkManager
) {
    fun scheduleSync() {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()

        val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>()
            .setConstraints(constraints)
            .setInputData(workDataOf("user_id" to "123"))
            .setBackoffCriteria(
                BackoffPolicy.EXPONENTIAL,
                10, TimeUnit.SECONDS
            )
            .build()

        workManager.enqueue(syncRequest)
    }

    fun schedulePeriodicSync() {
        val periodicRequest = PeriodicWorkRequestBuilder<SyncWorker>(
            15, TimeUnit.MINUTES
        ).setConstraints(
            Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()
        ).build()

        workManager.enqueueUniquePeriodicWork(
            "periodic_sync",
            ExistingPeriodicWorkPolicy.KEEP,
            periodicRequest
        )
    }
}
```

## Hilt Integration

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object WorkManagerModule {

    @Provides
    @Singleton
    fun provideWorkManager(
        @ApplicationContext context: Context
    ): WorkManager = WorkManager.getInstance(context)
}

class HiltWorkerFactory @Inject constructor(
    private val workerFactory: WorkerFactory
) : Configuration.Provider {
    override fun getWorkManagerConfiguration() =
        Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()
}
```

## Best Practices
1. Use for deferrable work only
2. Set appropriate constraints
3. Handle retries with backoff
4. Use unique work for periodic tasks
5. Don't use for immediate execution
